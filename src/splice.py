"""Insert finished add-on clips into a finished main video at chapter boundaries.

    python3 src/splice.py te        -> output/v2-credit-card-default-telugu-FULL.mp4

Placement lives in INSERT_BEFORE (main-video chapter id -> add-on clips placed
just before that chapter's title card). Each add-on's own end card is dropped.
Everything is re-encoded once so the joins are frame-accurate.
"""
import json, os, shlex, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAMES = {"te": "telugu", "hi": "hinglish"}
INSERT_BEFORE = {
    "ch5": ["a5-principal"],                         # after "Principal vs what the bank shows"
    "ch6": ["a1-multiple-cards", "a3-lok-adalat"],    # after "Settlement: how much & when"
    "ch7": ["a2-20-lakh-auction"],                   # after "Your property & family"
    "ch10": ["a4-notices"],                          # after "What RBI actually says"
    "ch11": ["a6-more-answers"],                     # after "Quick answers"
}


def main(lang):
    tl = json.load(open(f"{ROOT}/build/{lang}/timeline.json", encoding="utf-8"))
    start = {s["id"]: s["start"] for s in tl["scenes"]}
    main_mp4 = f"{ROOT}/output/v2-credit-card-default-{NAMES[lang]}.mp4"
    order = [c for c in sorted(INSERT_BEFORE, key=lambda c: start[c])]
    cuts = [0.0] + [start[c] for c in order] + [tl["total"]]
    clips = sorted({a for v in INSERT_BEFORE.values() for a in v})
    inputs = [main_mp4] + [f"{ROOT}/output/addons/{lang}/{a}.mp4" for a in clips]
    idx = {a: i + 1 for i, a in enumerate(clips)}

    def body_len(a):  # add-on length without its closing card
        t = json.load(open(f"{ROOT}/build/{a}/{lang}/timeline.json", encoding="utf-8"))
        return next(s["start"] for s in t["scenes"] if s["type"] == "addonend")

    f, n = [], 0
    for i in range(len(cuts) - 1):
        a, b = cuts[i], cuts[i + 1]
        f.append(f"[0:v]trim={a:.3f}:{b:.3f},setpts=PTS-STARTPTS[v{n}];[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS[a{n}]"); n += 1
        for clip in (INSERT_BEFORE[order[i]] if i < len(order) else []):
            L, j = body_len(clip), idx[clip]
            f.append(f"[{j}:v]trim=0:{L:.3f},setpts=PTS-STARTPTS[v{n}];[{j}:a]atrim=0:{L:.3f},asetpts=PTS-STARTPTS[a{n}]"); n += 1
    f.append("".join(f"[v{k}][a{k}]" for k in range(n)) + f"concat=n={n}:v=1:a=1[v][a]")
    out = f"{ROOT}/output/v2-credit-card-default-{NAMES[lang]}-FULL.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for p in inputs:
        cmd += ["-i", p]
    cmd += ["-filter_complex", ";".join(f), "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-preset", "medium",
            "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-movflags", "+faststart", out]
    print(" ".join(shlex.quote(c) for c in cmd[:6]), "…", out)
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main(sys.argv[1])
