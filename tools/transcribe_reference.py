import sys, time
from faster_whisper import WhisperModel

path = sys.argv[1]
t = time.time()
m = WhisperModel("large-v3", device="cpu", compute_type="int8", cpu_threads=4)
segs, info = m.transcribe(path, beam_size=5, word_timestamps=True, vad_filter=True)
print("lang", info.language, round(info.language_probability, 2))
for s in segs:
    print(f"[{s.start:6.2f}-{s.end:6.2f}] {s.text.strip()}")
print("took", round(time.time() - t), "s")
