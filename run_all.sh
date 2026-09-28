#!/usr/bin/env bash
# Unattended: generate Telugu + Hindi voices in parallel (2 threads each),
# then build, render and publish each language as soon as its voices are done.
set -uo pipefail
cd "$(dirname "$0")"
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
THREADS=2 python3 src/tts.py te > build/tts_te.log 2>&1 & PID_te=$!
THREADS=2 python3 src/tts.py hi > build/tts_hi.log 2>&1 & PID_hi=$!
for L in te hi; do
  NAME=$([ "$L" = hi ] && echo hinglish || echo telugu)
  P=PID_$L; wait "${!P}"
  echo "=== $L: voices"; python3 src/tts.py "$L" || { echo "tts $L failed"; continue; }
  echo "=== $L: audio"; python3 src/audio.py "$L" && python3 src/description.py "$L" && python3 src/script_doc.py "$L"
  echo "=== $L: render"; rm -f build/$L/part*.mp4
  node src/render.js "$L" video 2 || { echo "render $L failed"; continue; }
  "$FF" -y -loglevel error -i build/$L/video.mp4 -i build/$L/mix.wav -c:v copy -c:a aac -b:a 160k -ar 48000 \
      -shortest -movflags +faststart output/v2-credit-card-default-$NAME.mp4
  echo "=== $L: upload"
  curl -sS -m 3000 -F "file=@output/v2-credit-card-default-$NAME.mp4" https://upload.gofile.io/uploadfile > build/gofile_v2_$L.json
  python3 -c "import json;d=json.load(open('build/gofile_v2_$L.json'));print('LINK $L', d['data'].get('downloadPage'))"
  echo "=== $L: DONE"
done
