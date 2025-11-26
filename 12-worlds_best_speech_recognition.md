# World's best speech recognition
Nvidia has released open speech recognition models (parakeet and canary)  which are currently (November 2025) considered to be one of the best models. And the best part they run on consumer gpus. One problem I found is that to transcribe my lecture (45min) I would need a professional gpu with a lot of VRAM. But for 5 minutes it was very good. So I thought lets use our newly aquired programming skill to divide the lecture into small 5 mintutes overlapping parts and then put the recognized text properly together and voilá: I finally found a method to transcribe my videos. All other method failed up to date. Even asking somebody to write it down. Under windows the following should be best run under wsl. The nice thing is [wsl has full access to gpu](https://learn.microsoft.com/en-us/windows/ai/directml/gpu-cuda-in-wsl).

```bash
git clone  https://huggingface.co/spaces/nvidia/canary-1b-v2
cd canary-1b-v2/
sudo apt-get install python3-venv
#tested with python3.12
python3 -m venv ai
source ai/bin/activate

pip install -r requirements.txt
pip install gradio spaces
pip install cuda-python==12.9
python3 app.py --share
```

but we want to modify the program to do the segmentation:
app.py should look like:
```python
from nemo.collections.asr.models import ASRModel
import torch
import gradio as gr
import spaces
import gc
import shutil
from pathlib import Path
from pydub import AudioSegment, effects
import numpy as np
import os
import gradio.themes as gr_themes
import csv
import datetime
from supported_languages import SUPPORTED_LANGS_MAP
import math
import sys
import glob, os


device = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME="nvidia/canary-1b-v2"

model = ASRModel.from_pretrained(model_name=MODEL_NAME)
model.eval()

AVAILABLE_SRC_LANGS = list(SUPPORTED_LANGS_MAP.keys())
DEFAULT_SRC_LANG = "English"
AVAILABLE_TGT_LANGS = list(SUPPORTED_LANGS_MAP.keys())
DEFAULT_TGT_LANG = "English"


def format_srt_time(seconds: float) -> str:
    """Converts seconds to SRT time format HH:MM:SS,mmm using datetime.timedelta"""
    sanitized_total_seconds = max(0.0, seconds)
    delta = datetime.timedelta(seconds=sanitized_total_seconds)
    total_int_seconds = int(delta.total_seconds())

    hours = total_int_seconds // 3600
    remainder_seconds_after_hours = total_int_seconds % 3600
    minutes = remainder_seconds_after_hours // 60
    seconds_part = remainder_seconds_after_hours % 60
    milliseconds = delta.microseconds // 1000

    return f"{hours:02d}:{minutes:02d}:{seconds_part:02d},{milliseconds:03d}"

def generate_srt_content(segment_timestamps: list) -> str:
    """Generates SRT formatted string from segment timestamps."""
    srt_content = []
    for i, ts in enumerate(segment_timestamps):
        start_time = format_srt_time(ts['start'])
        end_time = format_srt_time(ts['end'])
        text = ts['segment']
        srt_content.append(str(i + 1))
        srt_content.append(f"{start_time} --> {end_time}")
        srt_content.append(text)
        srt_content.append("")
    return "\n".join(srt_content)


def start_session(request: gr.Request):
    session_hash = request.session_hash
    session_dir = Path(f'/tmp/{session_hash}')
    session_dir.mkdir(parents=True, exist_ok=True)

    print(f"Session with hash {session_hash} started.")
    return session_dir.as_posix()

def end_session(request: gr.Request):
    session_hash = request.session_hash
    session_dir = Path(f'/tmp/{session_hash}')

    if session_dir.exists():
        shutil.rmtree(session_dir)

    print(f"Session with hash {session_hash} ended.")

def sec_to_hrs(seconds):
    seconds = round(seconds)
    return str(datetime.timedelta(seconds=seconds))

def update_src_lang_dropdown(selected_value):
    if selected_value == DEFAULT_SRC_LANG:
        tgt_langs = AVAILABLE_TGT_LANGS
        default_tgt_lang = DEFAULT_TGT_LANG
    else:
        tgt_langs = [DEFAULT_TGT_LANG, selected_value]
        default_tgt_lang = selected_value
    return gr.Dropdown(choices=tgt_langs, value=default_tgt_lang, interactive=True)

def update_button_intstruction(src_lang, tgt_lang):
    if src_lang == tgt_lang:
        instruction = "Transcribe"
    else:
        instruction = "Translate"
    return (gr.Button(f"{instruction} Uploaded File", variant="primary"), gr.Button(f"{instruction} Microphone Input", variant="primary"))


def match_target_amplitude(sound, target_dBFS):
    change_in_dBFS = target_dBFS - sound.dBFS
    return sound.apply_gain(change_in_dBFS)

def get_audio_segment(audio_path, start_second, end_second):
    if not audio_path or not Path(audio_path).exists():
        print(f"Warning: Audio path '{audio_path}' not found or invalid for clipping.")
        return None
    try:
        start_ms = int(start_second * 1000)
        end_ms = int(end_second * 1000)

        start_ms = max(0, start_ms)
        if end_ms <= start_ms:
            print(f"Warning: End time ({end_second}s) is not after start time ({start_second}s). Adjusting end time.")
            end_ms = start_ms + 100

        audio = AudioSegment.from_file(audio_path)
        clipped_audio = audio[start_ms:end_ms]

        samples = np.array(clipped_audio.get_array_of_samples())
        if clipped_audio.channels == 2:
            samples = samples.reshape((-1, 2)).mean(axis=1).astype(samples.dtype)

        frame_rate = clipped_audio.frame_rate
        if frame_rate <= 0:
             print(f"Warning: Invalid frame rate ({frame_rate}) detected for clipped audio.")
             frame_rate = audio.frame_rate

        if samples.size == 0:
             print(f"Warning: Clipped audio resulted in empty samples array ({start_second}s to {end_second}s).")
             return None

        return (frame_rate, samples)
    except FileNotFoundError:
        print(f"Error: Audio file not found at path: {audio_path}")
        return None
    except Exception as e:
        print(f"Error clipping audio {audio_path} from {start_second}s to {end_second}s: {e}")
        return None

@spaces.GPU
def get_transcripts_and_raw_times(audio_path, session_dir, source_lang, target_lang):
    if not audio_path:
        gr.Error("No audio file path provided for transcription.", duration=None)
        # Return an update to hide the buttons
        return [], [], None, gr.DownloadButton(label="Download Transcript (CSV)", visible=False), gr.DownloadButton(label="Download Transcript (SRT)", visible=False)

    vis_data = [["N/A", "N/A", "Processing failed"]]
    raw_times_data = [[0.0, 0.0]]
    processed_audio_path = None
    csv_file_path = None
    srt_file_path = None
    original_path_name = Path(audio_path).name
    audio_name = Path(audio_path).stem

    # Initialize button states
    csv_button_update = gr.DownloadButton(label="Download Transcript (CSV)", visible=False)
    srt_button_update = gr.DownloadButton(label="Download Transcript (SRT)", visible=False)

    try:
        offset = 0
        segment_timestamps=[]
        try:
            gr.Info(f"Loading audio: {original_path_name}", duration=2)
            audio = AudioSegment.from_file(audio_path)
            print('Audio loaded successfully')
        except Exception as load_e:
            gr.Error(f"Failed to load audio file {original_path_name}: {load_e}", duration=None)
            return [["Error", "Error", "Load failed"]], [[0.0, 0.0]], audio_path, csv_button_update, srt_button_update

        resampled = False
        mono = False

        target_sr = 16000
        if audio.frame_rate != target_sr:
            try:
                audio = audio.set_frame_rate(target_sr)
                resampled = True
            except Exception as resample_e:
                 gr.Error(f"Failed to resample audio: {resample_e}", duration=None)
                 return [["Error", "Error", "Resample failed"]], [[0.0, 0.0]], audio_path, csv_button_update, srt_button_update

        if audio.channels == 2:
            try:
                audio = audio.set_channels(1)
                mono = True
            except Exception as mono_e:
                 gr.Error(f"Failed to convert audio to mono: {mono_e}", duration=None)
                 return [["Error", "Error", "Mono conversion failed"]], [[0.0, 0.0]], audio_path, csv_button_update, srt_button_update
        elif audio.channels > 2:
             gr.Error(f"Audio has {audio.channels} channels. Only mono (1) or stereo (2) supported.", duration=None)
             return [["Error", "Error", f"{audio.channels}-channel audio not supported"]], [[0.0, 0.0]], audio_path, csv_button_update, srt_button_update

        #if resampled or mono:
        divlen=240000 #240 seconds = 4 min
        overlap=30000 #30 seconds
        multiplier=divlen - overlap
        audiolen=math.ceil(audio.duration_seconds*1000.)
        looprange=audiolen//divlen +1
        output = [None]*looprange
        for i in range(looprange):
            try:
                processed_audio_path = Path(session_dir, f"{audio_name}_resampled.wav")
                gr.Info(f"Splitting audio: {processed_audio_path.as_posix()}part{i}.wav", duration=2)
                #normalizedsound = effects.normalize(audio[multiplier*i:multiplier*(i+1)+overlap])
                normalizedsound2 = effects.compress_dynamic_range(audio[multiplier*i:multiplier*(i+1)+overlap], -60.0, 4.0)
                #normalizedsound = effects.normalize(normalizedsound2)
                normalizedsound = match_target_amplitude(normalizedsound2, 0.0)
                normalizedsound.export(f"{processed_audio_path.as_posix()}part{i}.wav", format="wav")
                transcribe_path = f"{processed_audio_path.as_posix()}part{i}.wav"
                info_path_name = f"{original_path_name} (processed)"
            except Exception as export_e:
                gr.Error(f"Failed to export processed audio: {export_e}", duration=None)
                if processed_audio_path and os.path.exists(processed_audio_path):
                    os.remove(processed_audio_path)
                    for f in glob.glob(f"{processed_audio_path.as_posix()}part*.wav"):
                        os.remove(f)
                return [["Error", "Error", "Export failed"]], [[0.0, 0.0]], audio_path, csv_button_update, srt_button_update
       # else:
        #    transcribe_path = audio_path
         #   info_path_name = original_path_name
        # save segments
        for i in range(looprange):
            try:
                model.to(device)
                if source_lang == target_lang:
                    task = "Transcribing"
                else:
                    task = "Translating"
                gr.Info(f"{task} {processed_audio_path.as_posix()}part{i}.wav from {source_lang} to {target_lang}", duration=2)

                output[i] = model.transcribe([f"{processed_audio_path.as_posix()}part{i}.wav"],timestamps=True, source_lang=SUPPORTED_LANGS_MAP[source_lang], target_lang=SUPPORTED_LANGS_MAP[target_lang])

                if not output[i] or not isinstance(output[i], list) or not output[i][0] or not hasattr(output[i][0], 'timestamp') or not output[i][0].timestamp or 'segment' not in output[i][0].timestamp:
                    gr.Error("Prediction failed or produced unexpected output format.", duration=None)
                    return [["Error", "Error", "Prediction Format Issue"]], [[0.0, 0.0]], audio_path, csv_button_update, srt_button_update
                segment_timestamps += [ {'start': x['start'] + offset, 'end': x['end'] + offset, 'segment': x['segment']} for x in output[i][0].timestamp['segment']]
                offset +=multiplier/1000.
                if i==looprange-1:
                    segment_timestamps2=[]
                    currentend=0
                    lastjumpend=0
                    prevx=None
                    prevx2=None
                    for x in segment_timestamps:
                        print('1:',x['start'],x['end'],x['segment'])
                        if x['start']>=currentend:
                            if x['start']>=lastjumpend:
                                print('A:',x['start'],x['end'],x['segment'])
                                segment_timestamps2.append(x)
                        else:
                            segment_timestamps2.pop()
                            lastjumpend=prevx2['end']
                        currentend=x['end']
                        prevx2=prevx
                        prevx=x

                    print(segment_timestamps)
                    print("++++++++++++++++++++++++++++++++++++++++++++++++++++")
                    print(segment_timestamps2)
                    csv_headers = ["Start (HH:MM:SS)", "End (HH:MM:SS)", "Segment"]
                    vis_data = [[f"{sec_to_hrs(ts['start'])}", f"{sec_to_hrs(ts['end'])}", ts['segment']] for ts in segment_timestamps2]
                    raw_times_data = [[ts['start'], ts['end']] for ts in segment_timestamps2]

                    # CSV file generation
                    try:
                        csv_file_path = Path(session_dir, f"{task}_{audio_name}_{source_lang}_{target_lang}.csv")
                        writer = csv.writer(open(csv_file_path, 'w'))
                        writer.writerow(csv_headers)
                        writer.writerows(vis_data)
                        print(f"CSV transcript saved to temporary file: {csv_file_path}")
                        csv_button_update = gr.DownloadButton(value=csv_file_path, visible=True, label="Download Transcript (CSV)")
                    except Exception as csv_e:
                        gr.Error(f"Failed to create transcript CSV file: {csv_e}", duration=None)
                        print(f"Error writing CSV: {csv_e}")

                    # SRT file generation
                    if segment_timestamps2:
                        try:
                            srt_content = generate_srt_content(segment_timestamps2)
                            srt_file_path = Path(session_dir, f"{task}_{audio_name}_{source_lang}_{target_lang}.srt")
                            with open(srt_file_path, 'w', encoding='utf-8') as f:
                                f.write(srt_content)
                            print(f"SRT transcript saved to temporary file: {srt_file_path}")
                            srt_button_update = gr.DownloadButton(value=srt_file_path, visible=True, label="Download Transcript (SRT)")
                        except Exception as srt_e:
                            gr.Warning(f"Failed to create transcript SRT file: {srt_e}", duration=5)
                            print(f"Error writing SRT: {srt_e}")

                    gr.Info(f"{task} complete.", duration=2)
                    #for f in glob.glob(f"{processed_audio_path.as_posix()}part*.wav"):
                        #os.remove(f)
                    return vis_data, raw_times_data, audio_path, csv_button_update, srt_button_update

            except torch.cuda.OutOfMemoryError as e:
                error_msg = 'CUDA out of memory. Please try a shorter audio or reduce GPU load.'
                print(f"CUDA OutOfMemoryError: {e}")
                gr.Error(error_msg, duration=None)
                return [["OOM", "OOM", error_msg]], [[0.0, 0.0]], audio_path, csv_button_update, srt_button_update

            except FileNotFoundError:
                error_msg = f"Audio file for transcription not found: {Path(transcribe_path).name}."
                print(f"Error: Transcribe audio file not found at path: {transcribe_path}")
                gr.Error(error_msg, duration=None)
                return [["Error", "Error", "File not found for transcription"]], [[0.0, 0.0]], audio_path, csv_button_update, srt_button_update

            except Exception as e:
                error_msg = f"Prediction failed: {e}"
                print(f"Error during prediction processing: {e}")
                gr.Error(error_msg, duration=None)
                vis_data = [["Error", "Error", error_msg]]
                raw_times_data = [[0.0, 0.0]]
                return vis_data, raw_times_data, audio_path, csv_button_update, srt_button_update
            finally:
                try:
                    if 'model' in locals() and hasattr(model, 'cpu'):
                        if device == 'cuda':
                            model.cpu()
                    gc.collect()
                    if device == 'cuda':
                        torch.cuda.empty_cache()
                except Exception as cleanup_e:
                    print(f"Error during model cleanup: {cleanup_e}")
                    gr.Warning(f"Issue during model cleanup: {cleanup_e}", duration=5)

    finally:
        if processed_audio_path and os.path.exists(processed_audio_path):
            try:
                os.remove(processed_audio_path)
                print(f"Temporary audio file {processed_audio_path} removed.")

            except Exception as e:
                print(f"Error removing temporary audio file {processed_audio_path}: {e}")

def play_segment(evt: gr.SelectData, raw_ts_list, current_audio_path):
    if not isinstance(raw_ts_list, list):
        print(f"Warning: raw_ts_list is not a list ({type(raw_ts_list)}). Cannot play segment.")
        return gr.Audio(value=None, label="Selected Segment")

    if not current_audio_path:
        print("No audio path available to play segment from.")
        return gr.Audio(value=None, label="Selected Segment")

    selected_index = evt.index[0]

    if selected_index < 0 or selected_index >= len(raw_ts_list):
         print(f"Invalid index {selected_index} selected for list of length {len(raw_ts_list)}.")
         return gr.Audio(value=None, label="Selected Segment")

    if not isinstance(raw_ts_list[selected_index], (list, tuple)) or len(raw_ts_list[selected_index]) != 2:
         print(f"Warning: Data at index {selected_index} is not in the expected format [start, end].")
         return gr.Audio(value=None, label="Selected Segment")

    start_time_s, end_time_s = raw_ts_list[selected_index]

    print(f"Attempting to play segment: {current_audio_path} from {start_time_s:.2f}s to {end_time_s:.2f}s")

    segment_data = get_audio_segment(current_audio_path, start_time_s, end_time_s)

    if segment_data:
        print("Segment data retrieved successfully.")
        return gr.Audio(value=segment_data, autoplay=True, label=f"Segment: {start_time_s:.2f}s - {end_time_s:.2f}s", interactive=False)
    else:
        print("Failed to get audio segment data.")
        return gr.Audio(value=None, label="Selected Segment")

article = (
    "<p style='font-size: 1.1em;'>"
    "This demo showcases <code><a href='https://huggingface.co/nvidia/canary-1b-v2'>canary-1b-v2</a></code>, a 1-billion-parameter model built for high-quality speech transcription and translation across 25 European languages."
    "</p>"
    "<p><strong style='color: #ffb300; font-size: 1.2em;'>Key Features:</strong></p>"
    "<ul style='font-size: 1.1em;'>"
    "    <li>Support for <strong>25 European languages</strong></li>"
    "    <li>Automatic <strong>punctuation and capitalization</strong></li>"
    "    <li>Accurate <strong>word-level and segment-level timestamps</strong></li>"
    "    <li><strong>Segment-level timestamps</strong> for translated outputs</li>"
    "</ul>"
    "<p style='font-size: 1.1em;'>"
    "This model is <strong>available for commercial and non-commercial use</strong>."
    "</p>"
    "<p style='text-align: center;'>"
    "<a href='https://huggingface.co/nvidia/canary-1b-v2' target='_blank'>🎙️ Learn more  about the Model</a> | "
    "<a href='https://github.com/NVIDIA/NeMo' target='_blank'>🧑‍💻 NeMo Repository</a> | "
    "<a href='https://arxiv.org/abs/2509.14128' target='_blank'>🔍 Technical Report </a>"
    "</p>"
)

examples = [
    ["data/example-yt_saTD1u8PorI.mp3"],
]

# Define an NVIDIA-inspired theme
nvidia_theme = gr_themes.Default(
    primary_hue=gr_themes.Color(
        c50="#FFF9E6", # Lightest yellow
        c100="#FFF2CC",
        c200="#FFEB99",
        c300="#FFE066",
        c400="#FFD633",
        c500="#ffb300", # Canary Yellow
        c600="#ffb300",
        c700="#CC9900",
        c800="#B38600",
        c900="#996600", # Orange-brown
        c950="#805500"
    ),
    neutral_hue="gray", # Use gray for neutral elements
    font=[gr_themes.GoogleFont("Inter"), "ui-sans-serif", "system-ui", "sans-serif"],
).set()

# Apply the custom theme
with gr.Blocks(theme=nvidia_theme) as demo:
    model_display_name = MODEL_NAME.split('/')[-1] if '/' in MODEL_NAME else MODEL_NAME
    gr.HTML(f"""
    <h1 style='text-align: center; margin-bottom: 0;'>🐤 Transcribe and Translate with {model_display_name}</h1>
    <h3 style='text-align: center; margin-top: 5px; margin-bottom: 20px;'>in 25 European Languages</h3>
    """)
    gr.HTML(article)

    current_audio_path_state = gr.State(None)
    raw_timestamps_list_state = gr.State([])

    session_dir = gr.State()
    demo.load(start_session, outputs=[session_dir])

    gr.Markdown("---")

    with gr.Row():
        with gr.Column():
            gr.HTML("<p style='color: #ffb300; font-weight: bold; margin-bottom: 8px;'>🗣️ Select Source Language (Audio)</p>")
            source_lang_dropdown = gr.Dropdown(
                            choices=AVAILABLE_SRC_LANGS,
                            value=DEFAULT_SRC_LANG,
                            label="",
                            interactive=True)

        with gr.Column():
            gr.HTML("<p style='color: #ffb300; font-weight: bold; margin-bottom: 8px;'>💬 Select Target Language (Output Text)</p>")
            target_lang_dropdown = gr.Dropdown(
                choices=AVAILABLE_TGT_LANGS,
                value=DEFAULT_TGT_LANG,
                label="",
                interactive=True)

    with gr.Tabs():
        with gr.TabItem("Audio File"):
            file_input = gr.Audio(sources=["upload"], type="filepath", label="Upload Audio File")
            gr.Examples(examples=examples, inputs=[file_input], label="Example Audio Files (Click to Load)")
            file_transcribe_btn = gr.Button("Transcribe Uploaded File", variant="primary")

        with gr.TabItem("Microphone"):
            mic_input = gr.Audio(sources=["microphone"], type="filepath", label="Record Audio")
            mic_transcribe_btn = gr.Button("Transcribe Microphone Input", variant="primary")

    gr.Markdown("---")
    gr.HTML("<h3 style='text-align: center'>Ready to dive in? Click on the text to jump to the part you need!</h3>")

    # Define the DownloadButtons *before* the DataFrame
    with gr.Row():
        download_btn_csv = gr.DownloadButton(label="Download CSV", visible=False)
        download_btn_srt = gr.DownloadButton(label="Download SRT", visible=False)

    vis_timestamps_df = gr.DataFrame(
        headers=["Start (HH:MM:SS)", "End (HH:MM:SS)", "Segment"],
        datatype=["number", "number", "str"],
        wrap=True,
        label="Segments"
    )

    # selected_segment_player was defined after download_btn previously, keep it after df for layout
    selected_segment_player = gr.Audio(label="Selected Segment", interactive=False)

    source_lang_dropdown.select(
                    fn=update_src_lang_dropdown,
                    inputs=[source_lang_dropdown],
                    outputs=[target_lang_dropdown]
                    )

    target_lang_dropdown.select(
                    fn=update_button_intstruction,
                    inputs=[source_lang_dropdown, target_lang_dropdown],
                    outputs=[file_transcribe_btn, mic_transcribe_btn]
                    )

    mic_transcribe_btn.click(
        fn=get_transcripts_and_raw_times,
        inputs=[mic_input, session_dir, source_lang_dropdown, target_lang_dropdown],
        outputs=[vis_timestamps_df, raw_timestamps_list_state, current_audio_path_state, download_btn_csv, download_btn_srt],
        api_name="transcribe_mic"
    )

    file_transcribe_btn.click(
        fn=get_transcripts_and_raw_times,
        inputs=[file_input, session_dir, source_lang_dropdown, target_lang_dropdown],
        outputs=[vis_timestamps_df, raw_timestamps_list_state, current_audio_path_state, download_btn_csv, download_btn_srt],
        api_name="transcribe_file"
    )

    vis_timestamps_df.select(
        fn=play_segment,
        inputs=[raw_timestamps_list_state, current_audio_path_state],
        outputs=[selected_segment_player],
    )

    demo.unload(end_session)

if __name__ == "__main__":
    print("Launching Gradio Demo...")
    demo.queue()
    demo.launch()
```

