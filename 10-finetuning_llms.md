# Finetuning Large Language models
install python 3.12 as described in jupyternotebook setup description
and select it as your environment

Details see: https://dev.to/fahim_muntasir_073a441e2f/fine-tuning-small-language-models-with-unsloth-a-detailed-beginners-guide-446o

https://www.server-world.info/en/note?os=Debian_12&p=llama&f=3
https://colab.research.google.com/github/unslothai/notebooks/blob/main/nb/Phi_4-Conversational.ipynb
https://docs.unsloth.ai/get-started/unsloth-notebooks

adjusted from https://www.youtube.com/watch?v=pTaSDVz0gok

```python
import json

file = json.load(open("json_extraction_dataset_500.json", "r"))
print(file[1])
```
```python
%%capture
import os, re
if "COLAB_" not in "".join(os.environ.keys()):
    %pip install unsloth
else:

    # Do this only in Colab notebooks! Otherwise use pip install unsloth
​    import torch; v = re.match(r"[0-9\.]{3,}", str(torch.__version__)).group(0)
​    xformers = "xformers==" + ("0.0.32.post2" if v == "2.8.0" else "0.0.29.post3")
​    %pip install --no-deps bitsandbytes accelerate {xformers} peft trl triton cut_cross_entropy unsloth_zoo
​    %pip install sentencepiece protobuf "datasets>=3.4.1,<4.0.0" "huggingface_hub>=0.34.0" hf_transfer
​    %pip install --no-deps unsloth
%pip install transformers==4.56.2
%pip install --no-deps trl==0.22.2
```

# For GPU check
import torch
print(f"CUDA available: {torch.cuda.is_available()}")
print(f"GPU: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'}")
from unsloth import FastLanguageModel
import torch

model_name = "unsloth/Phi-3-mini-4k-instruct-bnb-4bit"

max_seq_length = 2048  # Choose sequence length
dtype = None  # Auto detection

# Load model and tokenizer
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name=model_name,
    max_seq_length=max_seq_length,
    dtype=dtype,
    load_in_4bit=True,
)
from datasets import Dataset

def format_prompt(example):
    return f"### Input: {example['input']}\n### Output: {json.dumps(example['output'])}<|endoftext|>"

formatted_data = [format_prompt(item) for item in file]
dataset = Dataset.from_dict({"text": formatted_data})
# Add LoRA adapters
model = FastLanguageModel.get_peft_model(
    model,
    r=64,  # LoRA rank - higher = more capacity, more memory
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",
        "gate_proj", "up_proj", "down_proj",
    ],
    lora_alpha=128,  # LoRA scaling factor (usually 2x rank)
    lora_dropout=0,  # Supports any, but = 0 is optimized
    bias="none",     # Supports any, but = "none" is optimized
    use_gradient_checkpointing="unsloth",  # Unsloth's optimized version
    random_state=3407,
    use_rslora=False,  # Rank stabilized LoRA
    loftq_config=None, # LoftQ
)

from trl import SFTConfig, SFTTrainer
trainer = SFTTrainer(
    model = model,
    tokenizer = tokenizer,
    train_dataset = dataset,
    dataset_text_field = "text",
    max_seq_length = max_seq_length,
    packing = False, # Can make training 5x faster for short sequences.
    args = SFTConfig(
        per_device_train_batch_size = 2,
        gradient_accumulation_steps = 4,
        warmup_steps = 5,
        max_steps = 60,
        learning_rate = 2e-4,
        logging_steps = 1,
        optim = "adamw_8bit",
        weight_decay = 0.001,
        lr_scheduler_type = "linear",
        seed = 3407,
        output_dir = "outputs",
        report_to = "none", # Use TrackIO/WandB etc
    ),
)
# Train the model
trainer_stats = trainer.train()
# Test the fine-tuned model
FastLanguageModel.for_inference(model) # Enable native 2x faster inference

# Test prompt
messages = [
    {"role": "user", "content": "Extract the product information:\n<div class='product'><h2>iPad Air</h2><span class='price'>$1344</span><span class='category'>audio</span><span class='brand'>Dell</span></div>"},
]

inputs = tokenizer.apply_chat_template(
    messages,
    tokenize=True,
    add_generation_prompt=True,
    return_tensors="pt",
).to("cuda")

# Generate response
outputs = model.generate(
    input_ids=inputs,
    max_new_tokens=256,
    use_cache=True,
    temperature=0.7,
    do_sample=True,
    top_p=0.9,
)

# Decode and print
response = tokenizer.batch_decode(outputs)[0]
print(response)
model.save_pretrained_gguf("gguf_model", tokenizer, quantization_method="q4_k_m")
from google.colab import files
import os

gguf_files = [f for f in os.listdir("gguf_model") if f.endswith(".gguf")]
if gguf_files:
    gguf_file = os.path.join("gguf_model", gguf_files[0])
    print(f"Downloading: {gguf_file}")
    files.download(gguf_file)