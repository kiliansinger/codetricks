# Cutting edge Optical-Character-Recognition

Optical-Character-Recognition (OCR) had quite some difficulties with formulas. As a physics or math student this was always very tedious to transcribe the formulas into latex notation.

Recent progress in the use of AI led to a very powerfull tool:
try the [jupyter notebook](.ocr/notebook.ipynb)

The good part is that because it is a single model that does all parts of OCR, from segmentation, character recognition to transcribing you can use the finetuning skills also on OCR. 
The possibilities are broad ranging from training the AI to read you special very illegible handwriting to reading doctor's prescriptions and even scanning through your physics and maths lecture transcripts:
For finetuning see the model's page and select the fine tuning link: [LightOnOCR-1B-1025](https://huggingface.co/lightonai/LightOnOCR-1B-1025).

here is the corresponding local notebook for [finetuning](./ocr/finetune_LightOnOCR.ipynb)

