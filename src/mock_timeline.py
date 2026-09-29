"""Estimated-duration timeline for layout previews (no audio needed).
PROJECT=<id> python3 src/mock_timeline.py te  -> build/<id>/te/timeline_mock.json"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.environ.get("PROJECT", "")
C = f"{ROOT}/content/addons/{P}" if P else f"{ROOT}/content"
B = f"{ROOT}/build/{P}" if P else f"{ROOT}/build"
lang = sys.argv[1]
sc = json.load(open(f"{C}/scenes.json", encoding="utf-8")); n = json.load(open(f"{C}/narration.{lang}.json", encoding="utf-8"))
t = 0; out = []
for s in sc:
    if s["type"] == "chapter":
        out.append({**s, "start": t, "dur": 2.6, "sentences": []}); t += 2.6; continue
    loc = 0.55; ss = []
    for x in n[s["id"]]:
        txt = x if isinstance(x, str) else (x.get("q") or x.get("t")); who = "q" if isinstance(x, dict) and "q" in x else "a"
        d = len(txt) / 13; ss.append({"text": txt, "who": who, "start": loc, "end": loc + d}); loc += d + 0.4
    out.append({**s, "start": t, "dur": loc + 0.4, "sentences": ss}); t += loc + 0.4
os.makedirs(f"{B}/{lang}", exist_ok=True)
json.dump({"lang": lang, "total": t, "scenes": out}, open(f"{B}/{lang}/timeline_mock.json", "w", encoding="utf-8"), ensure_ascii=False)
print(",".join(str(round(s["start"] + s["dur"] * 0.85, 1)) for s in out))
