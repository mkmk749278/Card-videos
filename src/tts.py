"""Generate narration (one clip per sentence) and the scene timeline.

Usage: python3 src/tts.py hi|te
Output: build/<lang>/voice/*.wav and build/<lang>/timeline.json
"""
import asyncio, json, os, subprocess, sys, wave

import certifi

# The sandbox proxy needs its CA bundle; harmless elsewhere.
CA = os.environ.get("TTS_CA_BUNDLE", "/root/.ccr/ca-bundle.crt")
if os.path.exists(CA):
    certifi.where = lambda: CA
import edge_tts  # noqa: E402  (must import after the certifi patch)
import imageio_ffmpeg  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()

LEAD_IN = 0.55      # silence before first sentence of a scene
GAP = 0.38          # pause between sentences
TAIL = 0.75         # hold after the last sentence
CHAPTER_DUR = 2.6   # chapter bumpers have no narration


async def synth(text, voice, rate, out_mp3, sem):
    async with sem:
        for attempt in range(4):
            try:
                c = edge_tts.Communicate(text, voice, rate=rate, proxy=os.environ.get("HTTPS_PROXY"))
                await c.save(out_mp3)
                if os.path.getsize(out_mp3) > 1000:
                    return
            except Exception as e:  # network hiccup: retry with backoff
                print("retry", attempt, e, file=sys.stderr)
            await asyncio.sleep(2 ** attempt)
        raise RuntimeError(f"TTS failed: {text[:40]}")


def to_wav(mp3, wav):
    # trim leading/trailing silence so our own gaps control pacing
    af = ("silenceremove=start_periods=1:start_threshold=-50dB,"
          "areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", mp3, "-af", af,
                    "-ar", "48000", "-ac", "1", wav], check=True)
    with wave.open(wav) as w:
        return w.getnframes() / w.getframerate()


async def main(lang):
    scenes = json.load(open(f"{ROOT}/content/scenes.json", encoding="utf-8"))
    narr = json.load(open(f"{ROOT}/content/narration.{lang}.json", encoding="utf-8"))
    voice, rate = narr["_voice"], narr["_rate"]
    vdir = f"{ROOT}/build/{lang}/voice"
    os.makedirs(vdir, exist_ok=True)

    sem = asyncio.Semaphore(4)
    jobs = []
    for s in scenes:
        for i, text in enumerate(narr.get(s["id"], [])):
            mp3 = f"{vdir}/{s['id']}_{i:02d}.mp3"
            if not os.path.exists(mp3) or os.path.getsize(mp3) < 1000:
                jobs.append(synth(text, voice, rate, mp3, sem))
    await asyncio.gather(*jobs)

    t = 0.0
    out = []
    for s in scenes:
        lines = narr.get(s["id"], [])
        if s["type"] == "chapter":
            out.append({**s, "start": round(t, 3), "dur": CHAPTER_DUR, "sentences": []})
            t += CHAPTER_DUR
            continue
        assert lines, f"no narration for {s['id']} ({lang})"
        for key in ("cue", "cueCannot"):
            if key in s:
                assert max(s[key]) < len(lines), f"{s['id']}: {key} beyond sentence count ({lang})"
        local = LEAD_IN
        sents = []
        for i, text in enumerate(lines):
            mp3 = f"{vdir}/{s['id']}_{i:02d}.mp3"
            wav = mp3[:-4] + ".wav"
            d = to_wav(mp3, wav)
            sents.append({"text": text, "start": round(local, 3), "end": round(local + d, 3),
                          "wav": os.path.relpath(wav, ROOT)})
            local += d + GAP
        dur = local - GAP + TAIL
        out.append({**s, "start": round(t, 3), "dur": round(dur, 3), "sentences": sents})
        t += dur

    json.dump({"lang": lang, "total": round(t, 3), "scenes": out},
              open(f"{ROOT}/build/{lang}/timeline.json", "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"{lang}: {len(out)} scenes, {t/60:.2f} min")


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1]))
