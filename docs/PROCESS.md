# How these videos are made — the full process

A playbook for producing the next explainer video with this repo. It covers the
pipeline, the tools and why each was chosen, the gotchas we hit, and exact
commands. Nothing here needs a GPU or paid service.

---

## 1. What the pipeline produces

| Output | Made by |
|---|---|
| 1080p 30 fps MP4, animated infographic scenes | `src/player.html` + `src/render.js` (headless Chromium, frame by frame) |
| Natural two-voice narration (expert + questioner) with emotion styles | `src/svara_tts.py` (open-source **svara-TTS**, Apache-2.0) |
| Burned-in captions synced to speech | `src/player.html` (per-sentence timing from the TTS step) |
| Royalty-free music bed, whooshes, stamps, voice ducking | `src/audio.py` (all synthesised with numpy) |
| YouTube title, description with chapter timestamps, disclaimer, tags | `src/description.py` |
| Recording script (if a human wants to voice it) | `src/script_doc.py` |
| Add-on clips, and splicing them into a main video | `run_addons.sh`, `src/splice.py` |

## 2. Pipeline at a glance

```
content/*.json ──► src/tts.py ──► build/<lang>/voice_svara/*.wav + timeline.json
                        │  (uses src/pronounce.py + src/svara_tts.py)
                        ▼
                  src/audio.py ──► build/<lang>/mix.wav   (voice + music + SFX, ducked)
                        ▼
      src/render.js + src/player.html ──► build/<lang>/video.mp4   (silent, 1080p)
                        ▼
                  ffmpeg mux ──► output/*.mp4 ──► Gofile upload
```

Every step is **resumable**. Voice clips are cached by a hash of their text,
style and gender, so editing one line regenerates only that line.

## 3. Content model — what you edit

### 3.1 `scenes.json` — the visuals (English on-screen text, shared by all languages)

A list of scenes. Each has an `id`, a `type` and type-specific fields.

| type | Use it for |
|---|---|
| `title`, `addon`, `chapter` | Opening hero, add-on title card, chapter bumpers (no narration) |
| `dialogue` | Worried person ⟷ expert conversation (two avatars, active speaker glows) |
| `bullets`, `rules`, `checklist`, `plan` | Lists that reveal item by item |
| `table` | Comparison tables (`colorLast: true` colours the last column) |
| `compare`, `secured`, `cancant` | Two-column contrasts |
| `stat`, `growth`, `stack`, `gauge` | Numbers: big stats, bar chart, stacked principal-vs-total bar, credit-score gauge |
| `timeline` | Day-by-day stage with a progress track |
| `tactics`, `chat`, `myths` | Harassment tactics, fake WhatsApp threats with stamp, myth → reality flip |
| `faq` | One question and answer at a time with a counter |
| `why`, `disclaimer`, `addonend` | Purpose + helpline, disclaimers, add-on outro |

**Cues.** `"cue": [1, 2, 2, 3]` means item *i* appears when narration sentence
`cue[i]` starts, so visuals land exactly on the spoken words. Keep the sentence
count per scene ≥ the highest cue index. `tts.py` asserts this.

### 3.2 `narration.<lang>.json` — the voice

```json
{
 "_engine": "svara", "_fx": "A", "_lang": "Telugu",
 "_styles": {"rates": "clear"},
 "cold": [
   {"q": "అన్నా... police వస్తారా?", "style": "fear"},
   "ఆగండి, ముందు ఊపిరి తీసుకోండి."
 ]
}
```

- A plain string is spoken by the **expert** (male) in the scene's default style
  (`chat`, or whatever `_styles` sets).
- `{"q": …}` is the **questioner** (female voice, amber captions).
- `{"t": …, "style": "sad"}` is the expert with a specific emotion.
- Styles: `chat`, `clear`, `happy`, `sad`, `fear`, `anger`, `surprise`, `formal`, `neutral`.
- Write English terms in Latin script (captions stay readable), and numbers as
  words ("ఒకటి నాలుగు నాలుగు ఒకటి ఆరు"). Voices read words more reliably than digits.

### 3.3 Writing style that sounds human

The single biggest quality lever was the **script**, not the voice engine:
- Write the way a friend talks: short sentences, "చూడండి…", "కదా?", "no?", "see…".
- Mix modes: conversation for worries, clear explanation for rules and numbers,
  direct narration for guidance.
- One idea per sentence. Put pauses in with commas and "…".

## 4. Voices — what we tried and why svara-TTS

| Engine | Result | Verdict |
|---|---|---|
| Microsoft Edge neural (edge-tts) | Clean but "reading" tone | Kept as a fast fallback (`_engine` omitted) |
| AI4Bharat **IndicF5** (voice cloning) | Can clone a real voice, but ~20× slower than real time on CPU and needs an exact reference transcript | Script kept in `tools/indicf5_clone.py` |
| AI4Bharat Indic Parler-TTS | Natural, but less expressive | Not used |
| **svara-TTS v1** (Orpheus-style, via llama.cpp GGUF Q5_K_M) | Most natural and conversational; emotion tags; Telugu, Hindi, Indian English; male and female | **Chosen** |
| Qwen3-TTS / XTTS / Chatterbox / Kokoro | Good English but **no Telugu** | Ruled out |

Online GPU Spaces (Hugging Face ZeroGPU) are faster, but they need a logged-in
token and have daily quotas.

**Speed on a 4-core CPU:** about 20× real time for Telugu/Hindi and about 11×
for English. So 25 minutes of Telugu speech takes about 8 hours. Running
languages in parallel gives **no** speed-up because generation is
memory-bandwidth bound, so run them one after another.

### 4.1 Pronunciation fix — `src/pronounce.py`

Indic voices read English words in Latin letters badly ("card" came out as
"car"). Before speaking, every Latin word is swapped for its native-script
spelling (card → కార్డ్ / कार्ड, RBI → ఆర్ బి ఐ). Captions keep the original.
Unknown words are printed as `[pronounce] no te entry for 'X'`. Add them to
`WORDS` before a long run.

### 4.2 Depth and clarity — voice finishing preset `_fx: "A"`

Applied per clip in `tts.py` (no regeneration needed): rubberband pitch 0.95 and
tempo 0.93 (deeper, slower), low-shelf warmth, a 3.2 kHz presence boost for
consonants, de-esser and a gentle compressor. The questioner gets a lighter
version. Preset `B` is stronger.

## 5. Rendering

- `player.html` is a single deterministic page: `render(t)` draws the frame at
  time *t*. There are no CSS animations, so every frame is reproducible.
- `render.js` screenshots each frame via CDP (JPEG) into ffmpeg (x264 CRF 20),
  split across N workers, then concatenates.
- Performance: blur filters and big repainted layers were the bottleneck. The
  backdrop is painted once to a canvas and blitted, and headless_shell is used.
  About 10 fps on 4 cores, so a 24-minute video takes about 75 minutes.
- **Check layouts before a long render** with a mock timeline (estimated durations):
  ```bash
  PROJECT=a1-multiple-cards python3 src/mock_timeline.py te      # prints preview times
  PROJECT=a1-multiple-cards TIMELINE=build/a1-multiple-cards/te/timeline_mock.json \
      node src/render.js te preview <t1,t2,…>                     # PNG stills
  ```

## 6. Projects: main video, add-ons, full English

| Project | Content | Build |
|---|---|---|
| Main video (te / hi) | `content/scenes.json`, `content/narration.<lang>.json` | `./run_all.sh` |
| Add-on clips | `content/addons/build_addons.py` (source of truth) → `content/addons/<id>/` | `./run_addons.sh te` |
| Main + add-ons spliced | uses finished MP4s | `python3 src/splice.py te` |
| Full English (main + deep dives built in) | `content/english/build_english.py` → `content/english/` | `./run_english.sh` |

`PROJECT=<id>` (and optionally `CONTENT_DIR=…`) scopes every script to
`content/addons/<id>` and `build/<id>/`.

## 7. Operating in the cloud container — important

- **The container sleeps when the chat session is idle**, which kills background
  jobs. Long runs only progress while the session is active. Keep it active with
  repeated ~9.5-minute wait loops, for example:
  `timeout 590 bash -c 'until grep -q DONE build/run_all.log; do sleep 20; done'`.
  Every script is resumable. If a run dies, just start it again.
- Don't run a video encode (ffmpeg/x264) at the same time as voice generation: llama.cpp threads get starved.
  One English clip took 33 minutes instead of 100 seconds.
- Never `pkill -f <pattern>` when your own command line contains the pattern:
  it kills your own shell. Use `pgrep -f "[p]attern"` or kill by PID.
- Large files: chat attachments are capped at 30 MB, so send a 540p/720p
  two-pass preview and share the full 1080p via Gofile
  (`curl -F file=@x.mp4 https://upload.gofile.io/uploadfile`). Free links can
  expire if nobody downloads them.
- `output/**/*.mp4` and `build/` are git-ignored. The repo holds source,
  scripts and docs only.

## 8. Content accuracy rules we followed

- Only claims backed by RBI directions, statutes or Supreme Court rulings are
  stated as rules: 3-day grace, 8 AM–7 PM calls, DRT ₹20 lakh per bank, wilful
  defaulter ₹25 lakh, Lok Adalat needs consent, and ₹100/day CIBIL compensation.
- Market experience (settlement %) is labelled **"commonly reported — not a
  rule"**, and example numbers are labelled **illustrative**.
- Suicide is mentioned once, briefly, never with method detail, and is always
  paired with hope and the Tele-MANAS helpline (14416), per YouTube's
  safe-messaging policy.
- No real person, bank customer or private data appears. The repo is public.
- Disclaimers go at the start and end, and in the YouTube description.
  Tick "altered or synthetic content" when uploading (AI voices).

## 9. Checklist for the next video

1. Research the topic and note sources and the exact rule behind each claim.
2. Write `scenes.json` (visual beats) and the narration in conversational style,
   with cues matching sentence numbers.
3. Run the pronunciation check. Add missing words to `src/pronounce.py`.
4. Do a mock-timeline preview of every scene, and fix layouts.
5. Generate a 30-second voice sample and get sign-off on voice, pace and tone.
6. Start the long run, and keep the session active.
7. Spot-check frames of the final MP4, send a phone preview, and upload the full file.
8. Generate the YouTube text (`src/description.py`) and push the source to the repo.

## 10. Setup

```bash
./setup.sh          # npm deps, Python deps, /opt/tts-env with torch/llama.cpp/SNAC
```
Models download on first use: svara-TTS GGUF (~2.7 GB), its tokenizer and the
SNAC decoder.

---

## 11. Status at hand-off (29 Sep 2026)

| Deliverable | State | Where |
|---|---|---|
| Telugu main video v2 (24:21) | ✅ Done | https://gofile.io/d/Z40avsUA |
| Telugu add-on clips 1–6 | ✅ Done | a1 https://gofile.io/d/7jzNmK6c · a2 https://gofile.io/d/ocDPMwIE · a3 https://gofile.io/d/lhOoZli7 · a4 https://gofile.io/d/jiAQovs0 · a5 https://gofile.io/d/MKABy4xZ · a6 https://gofile.io/d/Fm1MB3ta |
| **Telugu FULL** (main + add-ons spliced, 35:20) | ✅ Done | https://gofile.io/d/swWVCUE1 |
| Telugu YouTube text | ✅ Done | `output/youtube-te.md` |
| Hinglish v2 | ⏸ Script ready (`content/narration.hi.json`), voices not generated | `./run_all.sh` (Hindi half) |
| English full video | ⏸ Script ready (`content/english/`), ~40 of 323 Svara clips generated, then **paused on purpose** | see below |

Free Gofile links can expire if not downloaded; re-upload from `output/` if needed.

### Next step for English: switch the voice engine

Svara's English sounded robotic to the owner, since it is built for Indic
languages. Plan for the next session:
1. Test **Chatterbox / Chatterbox Turbo** (Resemble AI, open source, emotion
   "exaggeration" control, 3–6× faster than real time on CPU) using a short
   Indian-English reference clip (our own Svara output is rights-safe).
   Also compare **Kokoro-82M** and **MeloTTS EN-IN** on the same two lines.
2. Send the 3 samples to the owner and let them pick.
3. Add the chosen engine as `_engine` in `src/tts.py` (same job-file pattern
   as `src/svara_tts.py`), then run `./run_english.sh`.
