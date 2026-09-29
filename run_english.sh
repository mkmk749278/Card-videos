#!/usr/bin/env bash
# Full English (Indian English) video: main content + deep-dive sections.
set -uo pipefail
cd "$(dirname "$0")"
export PROJECT=english CONTENT_DIR=content/english
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
while pgrep -f "[s]vara_tts.py" >/dev/null; do sleep 10; done
python3 content/english/build_english.py
echo "=== en: voices"; THREADS=4 python3 src/tts.py en >> build/tts_en.log 2>&1 || { echo "tts en failed"; exit 1; }
echo "=== en: audio"; python3 src/audio.py en && python3 src/description.py en && python3 src/script_doc.py en
echo "=== en: render"; rm -f build/english/en/part*.mp4
node src/render.js en video 3 || { echo "render en failed"; exit 1; }
"$FF" -y -loglevel error -i build/english/en/video.mp4 -i build/english/en/mix.wav -c:v copy -c:a aac -b:a 160k -ar 48000 \
    -shortest -movflags +faststart output/v2-credit-card-default-english-full.mp4
echo "=== en: upload"
curl -sS -m 3000 -F "file=@output/v2-credit-card-default-english-full.mp4" https://upload.gofile.io/uploadfile > build/english/gofile_en.json
python3 -c "import json;d=json.load(open('build/english/gofile_en.json'));print('LINK en', d['data'].get('downloadPage'))"
echo "=== en: DONE"
