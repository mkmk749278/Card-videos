"""Mix narration + synthesized ambient music + transition SFX.

Usage: python3 src/audio.py hi|te   -> build/<lang>/mix.wav
Everything is generated here (no third-party music), so the soundtrack is
free of copyright issues.
"""
import json, os, sys, wave

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT = os.environ.get("PROJECT", "")
CONTENT = os.environ.get("CONTENT_DIR") or (f"{ROOT}/content/addons/{PROJECT}" if PROJECT else f"{ROOT}/content")
BUILD = f"{ROOT}/build/{PROJECT}" if PROJECT else f"{ROOT}/build"
SR = 48000
rng = np.random.default_rng(7)


def read_wav(p):
    with wave.open(p) as w:
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return a


def note(freq, dur, kind="pad"):
    t = np.arange(int(dur * SR)) / SR
    if kind == "pad":
        s = sum(np.sin(2 * np.pi * freq * d * t + p) for d, p in ((1, 0), (1.003, 1.1), (0.997, 2.3), (2.001, .4)))
        s = s / 4
        env = np.minimum(1, t / 1.2) * np.minimum(1, (dur - t) / 1.2)
    else:  # soft pluck
        s = np.sin(2 * np.pi * freq * t) + 0.3 * np.sin(4 * np.pi * freq * t)
        env = np.exp(-t * 5) * np.minimum(1, t / 0.005)
    return (s * env).astype(np.float32)


def music(total):
    # Am - F - C - G, 4 s per chord, loops
    chords = [[220.0, 261.63, 329.63], [174.61, 220.0, 261.63], [261.63, 329.63, 392.0], [196.0, 246.94, 293.66]]
    bass = [110.0, 87.31, 130.81, 98.0]
    bar = 4.0
    loop = np.zeros(int(bar * 4 * SR), np.float32)
    for i, ch in enumerate(chords):
        o = int(i * bar * SR)
        for f in ch:
            n = note(f, bar + 0.8)
            end = min(len(loop), o + len(n)); loop[o:end] += 0.18 * n[:end - o]
        b = note(bass[i], bar + 0.5)
        end = min(len(loop), o + len(b)); loop[o:end] += 0.22 * b[:end - o]
        # gentle arpeggio in eighths (≈ 120 bpm feel)
        arp = ch + [ch[1] * 2]
        for k in range(8):
            p = note(arp[k % len(arp)] * 2, 0.6, "pluck")
            s0 = o + int(k * bar / 8 * SR); e0 = min(len(loop), s0 + len(p))
            loop[s0:e0] += 0.05 * p[:e0 - s0]
    reps = int(np.ceil(total * SR / len(loop))) + 1
    m = np.tile(loop, reps)[: int(total * SR)]
    return m / (np.abs(m).max() + 1e-9)


def whoosh(dur=0.7, strength=1.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    noise = rng.standard_normal(n).astype(np.float32)
    # crude band sweep: mix of differently smoothed noise
    k = np.linspace(0, 1, n)
    smooth = np.convolve(noise, np.ones(40) / 40, mode="same")
    bright = noise - np.convolve(noise, np.ones(8) / 8, mode="same")
    s = smooth * (1 - k) + bright * k * 0.5
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 2
    return (s * env * 0.5 * strength).astype(np.float32)


def boom(dur=1.2):
    t = np.arange(int(dur * SR)) / SR
    f = 70 * np.exp(-t * 2) + 38
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.5)
    return (s * 0.8).astype(np.float32)


def thud():
    t = np.arange(int(0.35 * SR)) / SR
    s = np.sin(2 * np.pi * (120 * np.exp(-t * 18) + 50) * t) * np.exp(-t * 14)
    s += 0.25 * rng.standard_normal(len(t)) * np.exp(-t * 40)
    return (s * 0.9).astype(np.float32)


def add(buf, clip, at, gain=1.0):
    i = int(at * SR)
    if i < 0:  # clip starts before t=0 (e.g. whoosh ahead of the first scene)
        clip, i = clip[-i:], 0
    if i >= len(buf):
        return
    e = min(len(buf), i + len(clip))
    buf[i:e] += gain * clip[: e - i]


def main(lang):
    tl = json.load(open(f"{BUILD}/{lang}/timeline.json", encoding="utf-8"))
    total = tl["total"] + 1.0
    n = int(total * SR)
    voice = np.zeros(n, np.float32)
    sfx = np.zeros(n, np.float32)

    for sc in tl["scenes"]:
        for s in sc["sentences"]:
            clip = read_wav(f"{ROOT}/{s['wav']}")
            # level every clip to the same loudness so both voices sit evenly
            rms = float(np.sqrt(np.mean(clip ** 2))) + 1e-9
            clip = clip * min(0.1 / rms, 0.95 / (np.abs(clip).max() + 1e-9))
            add(voice, clip, sc["start"] + s["start"])
        if sc["type"] == "chapter":
            add(sfx, whoosh(0.9, 1.3), sc["start"] - 0.2, 0.9)
            add(sfx, boom(), sc["start"] + 0.45, 0.55)
        elif sc["type"] != "title":
            add(sfx, whoosh(0.6), sc["start"] - 0.25, 0.45)
        if sc["type"] == "title":
            add(sfx, boom(1.6), sc["start"] + 0.1, 0.6)
            add(sfx, thud(), sc["start"] + 2.25, 0.8)
        if sc["type"] == "chat":
            add(sfx, thud(), sc["start"] + sc["sentences"][sc["stampCue"]]["start"], 0.8)

    # normalise voice to a consistent level
    voice *= 0.89 / (np.abs(voice).max() + 1e-9)

    # music with sidechain ducking under the narration
    m = music(total)
    env = np.abs(voice)
    win = int(0.25 * SR)
    c = np.concatenate([[0], np.cumsum(env, dtype=np.float64)])
    idx = np.arange(n)
    lo, hi = np.clip(idx - win // 2, 0, n), np.clip(idx + win // 2, 0, n)
    env = ((c[hi] - c[lo]) / win).astype(np.float32)
    env = np.clip(env / 0.05, 0, 1)
    duck = 1 - 0.55 * env
    fade = np.minimum(1, np.arange(n) / (2 * SR)) * np.minimum(1, (n - np.arange(n)) / (3 * SR))
    mix = voice + m * 0.11 * duck * fade + sfx * 0.5
    mix /= max(1.0, np.abs(mix).max() / 0.97)

    out = f"{BUILD}/{lang}/mix.wav"
    with wave.open(out, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((mix * 32767).astype(np.int16).tobytes())
    print("wrote", out, f"{total:.1f}s")


if __name__ == "__main__":
    main(sys.argv[1])
