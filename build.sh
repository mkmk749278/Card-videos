#!/usr/bin/env bash
# Build one language version end-to-end: ./build.sh hi|te [workers]
set -euo pipefail
cd "$(dirname "$0")"
LANG_CODE=${1:?usage: ./build.sh hi|te [workers]}
WORKERS=${2:-4}
NAME=$([ "$LANG_CODE" = hi ] && echo hinglish || echo telugu)
FFMPEG=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")

python3 src/tts.py "$LANG_CODE"
python3 src/audio.py "$LANG_CODE"
node src/render.js "$LANG_CODE" video "$WORKERS"

mkdir -p output
"$FFMPEG" -y -loglevel error -i "build/$LANG_CODE/video.mp4" -i "build/$LANG_CODE/mix.wav" \
  -c:v copy -c:a aac -b:a 160k -ar 48000 -shortest -movflags +faststart \
  "output/credit-card-default-$NAME.mp4"
echo "output/credit-card-default-$NAME.mp4"
