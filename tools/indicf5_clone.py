"""IndicF5 voice cloning on CPU without the torch.compile wrapper.

python f5.py <ref.wav> <ref_text_file> <out_dir> <lines.json> [speed] [nfe]
lines.json: {"name": "text", ...}  -> <out_dir>/<name>.wav (24 kHz)
"""
import json, os, sys, time

import numpy as np
import soundfile as sf
import torch
from huggingface_hub import hf_hub_download
from safetensors.torch import load_file
from vocos import Vocos

from f5_tts.infer.utils_infer import infer_process, load_model, preprocess_ref_audio_text
from f5_tts.model import DiT

torch.set_num_threads(int(os.environ.get("THREADS", "4")))
M = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models/IndicF5")

sd = load_file(f"{M}/model.safetensors")
model = load_model(DiT, dict(dim=1024, depth=22, heads=16, ff_mult=2, text_dim=512, conv_layers=4),
                   mel_spec_type="vocos", vocab_file=f"{M}/checkpoints/vocab.txt", device="cpu")
p = "ema_model._orig_mod."
missing = model.load_state_dict({k[len(p):]: v for k, v in sd.items() if k.startswith(p)}, strict=False)
print("model missing/unexpected:", len(missing.missing_keys), len(missing.unexpected_keys))
model.eval()

voc = Vocos.from_hparams(hf_hub_download("charactr/vocos-mel-24khz", "config.yaml"))
p = "vocoder._orig_mod."
voc.load_state_dict({k[len(p):]: v for k, v in sd.items() if k.startswith(p)})
voc.eval()

ref_wav, ref_txt_file, out_dir, lines_file = sys.argv[1:5]
speed = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
nfe = int(sys.argv[6]) if len(sys.argv) > 6 else 32
ref_audio, ref_text = preprocess_ref_audio_text(ref_wav, open(ref_txt_file, encoding="utf-8").read().strip())
os.makedirs(out_dir, exist_ok=True)
lines = json.load(open(lines_file, encoding="utf-8"))
for name, text in lines.items():
    out = f"{out_dir}/{name}.wav"
    if os.path.exists(out):
        continue
    t = time.time()
    torch.manual_seed(7)
    with torch.inference_mode():
        audio, sr, _ = infer_process(ref_audio, ref_text, text, model, voc, mel_spec_type="vocos",
                                     speed=speed, nfe_step=nfe, device="cpu")
    sf.write(out, np.asarray(audio, dtype=np.float32), sr)
    print(f"{name}: {len(audio) / sr:.1f}s audio in {time.time() - t:.1f}s", flush=True)
