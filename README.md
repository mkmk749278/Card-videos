# Credit Card Bill Not Paid? — Public awareness video (Hinglish + Telugu)

A ~13-minute animated explainer for the general public: what really happens,
day by day, when a credit card bill goes unpaid in India. It covers what banks
can and cannot do, how recovery agents apply pressure, what RBI rules actually
say, how to complain, a practical action plan, and how to settle safely.

| Version | Narration | Captions |
|---|---|---|
| Hinglish | Hindi + English terms (neural voice `hi-IN-MadhurNeural`) | Devanagari + English |
| Telugu-English | Telugu + English terms (neural voice `te-IN-MohanNeural`) | Telugu + English |

On-screen graphics are in English (numbers, rules, key terms), so both
versions share the same visuals.

## Chapters

1. The interest trap: rates, the minimum-due trap, 12-month growth, card rotation
2. Day-by-day timeline: Day 0–3 → 4–30 → 31–60 → 61–90 (SMA-2) → 90+ (NPA) → 180+ (write-off) → 1 year+
3. What banks can and can't do: civil vs criminal exposure
4. How recovery agents pressure you: tactics, WhatsApp scare messages, myth vs reality
5. What RBI actually says: recovery-agent rules (12 Aug 2022), Credit Card Master Direction 2022, complaint ladder, evidence
6. What to say: ready-made lines for calls, relatives and the doorstep
7. Your action plan: 7 steps, before-90-days vs after-NPA
8. Settlement the right way: checklist, "Settled" vs "Closed"
9. Cautions, summary and disclaimer

## How it is made

The full production process — tools, voice choices, gotchas and a checklist for the next video — is in **[docs/PROCESS.md](docs/PROCESS.md)**.

## Build

Requirements: Python 3.10+, Node 18+, Chromium (Playwright). Run `./setup.sh` once.

```bash
npm install
pip install edge-tts imageio-ffmpeg numpy
./build.sh hi      # Hinglish  -> output/credit-card-default-hinglish.mp4
./build.sh te      # Telugu    -> output/credit-card-default-telugu.mp4
```

Pipeline:

| Step | File | Output |
|---|---|---|
| 1. Narration (one clip per sentence) + timeline | `src/tts.py` | `build/<lang>/timeline.json` |
| 2. Music bed (synthesised, royalty-free) + SFX + ducking | `src/audio.py` | `build/<lang>/mix.wav` |
| 3. Frame-accurate HTML animation → H.264 | `src/player.html`, `src/render.js` | `build/<lang>/video.mp4` |
| 4. Mux | `build.sh` | `output/*.mp4` |

To edit the content, change `content/scenes.json` (visuals) and
`content/narration.<lang>.json` (spoken lines). Each `cue` index says which
spoken sentence reveals an item on screen, so keep sentence counts in sync.
To check layouts before a full render:
`node src/render.js hi preview 10,60,120` writes stills to `build/hi/preview/`.

## Content sources

- RBI Master Direction — Credit Card and Debit Card (Issuance and Conduct) Directions, 2022
- RBI circular on recovery agents / outsourcing of financial services, 12 Aug 2022
- RBI Framework for Compromise Settlements and Technical Write-offs, 8 Jun 2023
- Reserve Bank – Integrated Ombudsman Scheme, 2021 (cms.rbi.org.in, 14448)
- Limitation Act 1963 s.18–19; NI Act s.138; Payment and Settlement Systems Act 2007 s.25

The 12-month growth chart is illustrative (3.6% per month interest, a ₹1,300
late fee each month, 18% GST). Actual numbers vary by bank.

**Disclaimer:** this is general awareness material, not legal or financial
advice.
