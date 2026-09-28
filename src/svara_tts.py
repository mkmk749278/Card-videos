"""Local svara-TTS v1 (Orpheus-style, Apache-2.0) on CPU via llama.cpp + SNAC.

Runs inside the separate TTS virtualenv (see README):
    /opt/tts-env/bin/python src/svara_tts.py <jobs.json>
jobs.json: [{"out": "path.wav", "lang": "Telugu", "gender": "Male", "text": "...", "style": "chat"}, ...]
Existing outputs are skipped, so the job can be resumed after an interruption.
"""
import json, os, sys, time

import soundfile as sf
import torch
from huggingface_hub import hf_hub_download
from llama_cpp import Llama
from snac import SNAC
from transformers import AutoTokenizer

QUANT = os.environ.get("SVARA_QUANT", "Q5_K_M")
THREADS = int(os.environ.get("THREADS", "4"))
torch.set_num_threads(THREADS)

gguf = hf_hub_download("mradermacher/svara-tts-v1-GGUF", f"svara-tts-v1.{QUANT}.gguf")
tok = AutoTokenizer.from_pretrained("kenpath/svara-tts-v1")
snac = SNAC.from_pretrained("hubertsiuzdak/snac_24khz").eval()
LLMS = {}


def llm(seed):
    if seed not in LLMS:
        LLMS.clear()
        LLMS[seed] = Llama(model_path=gguf, n_ctx=4096, n_threads=THREADS, seed=seed, verbose=False)
    return LLMS[seed]


def prompt_ids(lang, gender, text, style):
    tail = f" <{style}>" if style and style != "neutral" else ""
    return [128259] + tok(f"{lang} ({gender}): {text}{tail}").input_ids + [128009, 128260]


def decode(codes):
    codes = codes[: len(codes) // 7 * 7]
    l1, l2, l3 = [], [], []
    for i in range(len(codes) // 7):
        c = codes[7 * i: 7 * i + 7]
        l1.append(c[0]); l2.append(c[1] - 4096)
        l3 += [c[2] - 2 * 4096, c[3] - 3 * 4096]
        l2.append(c[4] - 4 * 4096)
        l3 += [c[5] - 5 * 4096, c[6] - 6 * 4096]
    if not l1:
        return None
    t = [torch.tensor(x).unsqueeze(0) for x in (l1, l2, l3)]
    with torch.inference_mode():
        return snac.decode(t).squeeze().numpy()


def synth(job, seed, temp=0.65, top_p=0.8, rep=1.1):
    m = llm(seed)
    m.reset()
    out = []
    # ~85 audio tokens per second of speech; cap well above the expected length
    cap = int(min(4000, 85 * (len(job["text"]) / 6 + 6)))
    for t in m.generate(prompt_ids(job["lang"], job["gender"], job["text"], job.get("style", "chat")),
                        temp=temp, top_p=top_p, repeat_penalty=rep, reset=True):
        if t == 128258 or len(out) >= cap:
            break
        out.append(t)
    if 128257 in out:
        out = out[len(out) - out[::-1].index(128257):]
    return decode([t - 128266 for t in out if t >= 128266])


def plausible(audio, text):
    # speech runs roughly 10–20 characters per second; outside that is garbled or truncated
    if audio is None:
        return False
    secs = len(audio) / 24000
    return len(text) / 25 <= secs <= len(text) / 6 + 3


if __name__ == "__main__":
    jobs = json.load(open(sys.argv[1], encoding="utf-8"))
    todo = [j for j in jobs if not os.path.exists(j["out"])]
    print(f"{len(todo)} of {len(jobs)} clips to generate", flush=True)
    for n, job in enumerate(todo, 1):
        os.makedirs(os.path.dirname(job["out"]), exist_ok=True)
        t = time.time()
        audio = None
        for seed in (11, 23, 37):
            audio = synth(job, seed)
            if plausible(audio, job["text"]):
                break
            print(f"  retry {os.path.basename(job['out'])} (seed {seed} implausible)", flush=True)
        if audio is None:
            print(f"  FAILED {job['out']}", flush=True)
            continue
        sf.write(job["out"], audio, 24000)
        print(f"[{n}/{len(todo)}] {os.path.basename(job['out'])}: {len(audio) / 24000:.1f}s in {time.time() - t:.0f}s", flush=True)
