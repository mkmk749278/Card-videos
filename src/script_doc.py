"""Print the narration as a recording script (scene by scene, with timings).

Usage: python3 src/script_doc.py hi|te -> output/narration-script-<lang>.md
"""
import json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ts(s):
    return f"{int(s) // 60}:{int(s) % 60:02d}"


def main(lang):
    tl = json.load(open(f"{ROOT}/build/{lang}/timeline.json", encoding="utf-8"))
    name = "Hinglish" if lang == "hi" else "Telugu"
    out = [f"# Narration script — {name}\n",
           "Record **one audio file per scene**, named with the scene number (e.g. `03.m4a`).",
           "Leave ~1 second of silence at the start and end. Chapter cards (🎬) have no voice.\n"]
    n = 0
    for s in tl["scenes"]:
        if s["type"] == "chapter":
            out.append(f"\n---\n\n## 🎬 Chapter {s['num']}: {s['title']}  ·  {ts(s['start'])}\n")
            continue
        n += 1
        head = s.get("heading") or s.get("title") or s.get("days") or s["id"]
        if s["type"] == "timeline":
            head = f"{s['days']} — {s['title']}"
        out.append(f"### Scene {n:02d} · {head}  ·  {ts(s['start'])} ({round(s['dur'])}s)\n")
        out += [f"{i + 1}. {x['text']}" for i, x in enumerate(s["sentences"])]
        out.append("")
    p = f"{ROOT}/output/narration-script-{lang}.md"
    open(p, "w", encoding="utf-8").write("\n".join(out))
    print(p, n, "scenes")


if __name__ == "__main__":
    main(sys.argv[1])
