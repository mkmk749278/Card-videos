#!/usr/bin/env bash
# Build all add-on clips for one language: ./run_addons.sh te
# Voices for every clip first (the slow part), then render + upload each.
# Resumable: finished voice clips and finished videos are skipped.
set -uo pipefail
cd "$(dirname "$0")"
L=${1:-te}
FF=$(python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
# never run two voice generators at once
while pgrep -f "[s]vara_tts.py" >/dev/null; do sleep 10; done
python3 content/addons/build_addons.py
IDS=$(ls -d content/addons/*/ | xargs -n1 basename)
mkdir -p output/addons/$L
for P in $IDS; do
  [ -f content/addons/$P/narration.$L.json ] || continue
  echo "=== $P: voices"; PROJECT=$P THREADS=4 python3 src/tts.py $L >> build/addons_tts_$L.log 2>&1 || echo "tts $P failed"
done
for P in $IDS; do
  OUT=output/addons/$L/$P.mp4
  [ -f "$OUT" ] && { echo "=== $P: already built"; continue; }
  [ -f content/addons/$P/narration.$L.json ] || continue
  echo "=== $P: audio+render"
  # re-run tts (all clips cached) so the timeline carries the latest scene design
  PROJECT=$P python3 src/tts.py $L >> build/addons_tts_$L.log 2>&1 || { echo "timeline $P failed"; continue; }
  PROJECT=$P python3 src/audio.py $L && rm -f build/$P/$L/part*.mp4 && PROJECT=$P node src/render.js $L video 3 || { echo "render $P failed"; continue; }
  "$FF" -y -loglevel error -i build/$P/$L/video.mp4 -i build/$P/$L/mix.wav -c:v copy -c:a aac -b:a 160k -ar 48000 \
      -shortest -movflags +faststart "$OUT.tmp.mp4" && mv "$OUT.tmp.mp4" "$OUT"
  curl -sS -m 1500 -F "file=@$OUT" https://upload.gofile.io/uploadfile > build/$P/$L/gofile.json
  python3 -c "import json;d=json.load(open('build/$P/$L/gofile.json'));print('LINK $P', d['data'].get('downloadPage'))"
done
echo "=== ADDONS $L DONE"
