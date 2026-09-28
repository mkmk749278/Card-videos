"""Generate narration (one clip per sentence) and the scene timeline.

Usage: python3 src/tts.py hi|te
Output: build/<lang>/voice/*.wav and build/<lang>/timeline.json
"""
import asyncio, hashlib, json, os, subprocess, sys, wave

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


# Voice finishing for depth and clarity: slight pitch-down + slower pace (rubberband),
# low-shelf warmth, presence boost for consonants, de-essing and gentle compression.
_COMMON = "highpass=f=60,deesser=i=0.4,acompressor=threshold=-20dB:ratio=3:attack=8:release=160:makeup=2"
VOICE_FX = {
    "A": {"a": f"rubberband=tempo=0.93:pitch=0.95,lowshelf=g=3:f=170,equalizer=f=3200:t=h:w=1500:g=3,{_COMMON}",
          "q": f"rubberband=tempo=0.95:pitch=0.98,lowshelf=g=1.5:f=200,equalizer=f=3200:t=h:w=1500:g=2.5,{_COMMON}"},
    "B": {"a": f"rubberband=tempo=0.90:pitch=0.92,lowshelf=g=4.5:f=160,equalizer=f=3000:t=h:w=1500:g=4,{_COMMON}",
          "q": f"rubberband=tempo=0.93:pitch=0.97,lowshelf=g=2:f=200,equalizer=f=3200:t=h:w=1500:g=3,{_COMMON}"},
}


def to_wav(mp3, wav, fx=None):
    # trim leading/trailing silence so our own gaps control pacing
    af = ("silenceremove=start_periods=1:start_threshold=-50dB,"
          "areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse")
    if fx:
        af = f"{fx},{af},asetpts=N/SR/TB"
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", mp3, "-af", af,
                    "-ar", "48000", "-ac", "1", wav], check=True)
    with wave.open(wav) as w:
        return w.getnframes() / w.getframerate()


def norm(line, default_style):
    """Narration lines: "text" (narrator) | {"t": text, "style": s} | {"q": text, "style": s} (questioner)."""
    if isinstance(line, str):
        return {"who": "a", "text": line, "style": default_style}
    who = "q" if "q" in line else "a"
    return {"who": who, "text": line.get("q") or line.get("t"), "style": line.get("style", "chat")}


def synth_svara(narr, scenes, lang, vdir):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from pronounce import speakable
    jobs = []
    for s in scenes:
        for i, ln in enumerate(narr.get(s["id"], [])):
            gender = "Female" if ln["who"] == "q" else "Male"
            spoken = speakable(lang, ln["text"], warn=True)
            h = hashlib.md5(f"{spoken}|{ln['style']}|{gender}".encode()).hexdigest()[:8]
            out = f"{vdir}/{s['id']}_{i:02d}_{h}_raw.wav"
            ln["raw"] = out
            jobs.append({"out": out, "lang": narr["_lang"], "gender": gender, "text": spoken, "style": ln["style"]})
    jf = f"{vdir}/jobs.json"
    json.dump(jobs, open(jf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    py = os.environ.get("TTS_PY", "/opt/tts-env/bin/python")
    subprocess.run([py, os.path.join(os.path.dirname(os.path.abspath(__file__)), "svara_tts.py"), jf], check=True)


async def main(lang):
    scenes = json.load(open(f"{ROOT}/content/scenes.json", encoding="utf-8"))
    narr = json.load(open(f"{ROOT}/content/narration.{lang}.json", encoding="utf-8"))
    engine = narr.get("_engine", "edge")
    styles = narr.get("_styles", {})
    for k, v in list(narr.items()):
        if not k.startswith("_"):
            narr[k] = [norm(x, styles.get(k, "chat")) for x in v]
    vdir = f"{ROOT}/build/{lang}/voice_{engine}"
    os.makedirs(vdir, exist_ok=True)

    if engine == "svara":
        synth_svara(narr, scenes, lang, vdir)
        src = lambda sid, i: narr[sid][i]["raw"]
    else:
        voice, rate = narr["_voice"], narr["_rate"]
        sem = asyncio.Semaphore(4)
        jobs = []
        for s in scenes:
            for i, ln in enumerate(narr.get(s["id"], [])):
                mp3 = f"{vdir}/{s['id']}_{i:02d}.mp3"
                if not os.path.exists(mp3) or os.path.getsize(mp3) < 1000:
                    jobs.append(synth(ln["text"], voice, rate, mp3, sem))
        await asyncio.gather(*jobs)
        src = lambda sid, i: f"{vdir}/{sid}_{i:02d}.mp3"

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
        for i, ln in enumerate(lines):
            raw = src(s["id"], i)
            if not os.path.exists(raw):
                print(f"missing audio {raw}", file=sys.stderr)
                continue
            wav = f"{vdir}/{s['id']}_{i:02d}.wav"
            fx = VOICE_FX.get(narr.get("_fx", ""), {}).get(ln["who"]) if engine == "svara" else None
            d = to_wav(raw, wav, fx)
            # a speaker change gets a slightly longer pause, like a real conversation
            if sents and sents[-1]["who"] != ln["who"]:
                local += 0.25
            sents.append({"text": ln["text"], "who": ln["who"], "start": round(local, 3), "end": round(local + d, 3),
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
