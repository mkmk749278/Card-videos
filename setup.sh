#!/usr/bin/env bash
# One-time environment setup (Linux, CPU only). Safe to re-run.
set -euo pipefail
cd "$(dirname "$0")"
# 1) Node: renderer (Playwright/Chromium), fonts, Fluent emoji icons
npm install
# 2) Main Python: pipeline glue, mixing, fallback Edge TTS
pip install edge-tts imageio-ffmpeg numpy
# 3) Separate TTS virtualenv (keeps torch & friends away from the main Python)
python3 -m venv /opt/tts-env
/opt/tts-env/bin/pip install torch==2.5.1 torchaudio==2.5.1 --index-url https://download.pytorch.org/whl/cpu
/opt/tts-env/bin/pip install snac transformers huggingface_hub soundfile \
  llama-cpp-python --extra-index-url https://abetlen.github.io/llama-cpp-python/whl/cpu
# optional: voice-cloning experiments (IndicF5) and reference transcription
# /opt/tts-env/bin/pip install git+https://github.com/ai4bharat/IndicF5.git faster-whisper
# 4) ffmpeg on PATH (some tools shell out to plain `ffmpeg`)
ln -sf "$(python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')" /usr/local/bin/ffmpeg
echo "setup done — models download on first use (~3 GB)"
