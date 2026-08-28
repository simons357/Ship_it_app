# AI Surgeon

Phone-first surgical residency prototype from Simons Medical Innovations.
See one. Do one. Teach one. Independent of ChatVault and Domain Architect —
clinical training game, not a research face, **not a medical device**.

## Run it

From the repo root (dedicated port **8770**, not Domain Architect's 8765):

```bash
python3 -m ai_surgeon
```

Then open:

- Hub: http://127.0.0.1:8770/
- Prefixed: http://127.0.0.1:8770/ai-surgeon/
- Open appendectomy: http://127.0.0.1:8770/ai-surgeon-prototype.html
- Tube thoracostomy (trauma): http://127.0.0.1:8770/ai-surgeon-module02-trauma.html
- Phone stills (identify / lab / verse / anatomy): http://127.0.0.1:8770/screens.html
- Brochure PDF: http://127.0.0.1:8770/generators/AI-Surgeon-Brochure.pdf
- Phone stills: http://127.0.0.1:8770/screens.html

From this directory, relative assets also work with:

```bash
python3 -m http.server 8770
```

## What is playable vs stubbed

| Path | Status |
| --- | --- |
| Hub `index.html` | Playable map. Two modules open; the rest are honest pitch cards. |
| `ai-surgeon-prototype.html` | **Playable.** Open appendectomy — study / see / do / teach, profile, ask-the-attending, handover. |
| `ai-surgeon-module02-trauma.html` | **Playable.** Tube thoracostomy — live monitor, needle decays, tube holds, patient loss on. |
| `screens.html` | **Playable chrome** on the design stills (identify / lab / verse / pen). Not a replacement for the 3D modules. |
| Teach One (supervise a junior) | Specified in the progression note; the HTML is still the multiple-choice placeholder. |
| `screens.html` | **Playable stills.** Identify-before-cut, The Lab, Study/See/Do One, The Pen, The Nib, Verse seats, Case 07 phone still. |
| Hardware ladder / art fidelity / tablet+mat / twist-stylus hardware | Pitch stills on `screens.html`. |
| Skills lab, finger I&D, lap chole, hernia, anastomosis, cric, DCL, chief, anaesthesia track | Pitch · not playable. Module 04 The Pen is a still, not the full ladder. |

How to rebuild the brochure and mockup PNGs: [`SCREENS.md`](SCREENS.md).

## Source of truth

- `docs/AI-Surgeon-Storyboard.pdf` — 31 beats, HUD, four phases (product bible)
- `docs/AI-Surgeon-Systems-and-Progression.md` — two-axis load, handover scoring, competencies
- `docs/SOURCE-LOCK.md` — what the dropped docs locked
- `docs/CITATIONS.md` — sources named in the 2025 plans, not invented papers
- `docs/bible/` — 2025 final plan / extracts (archived investor voice)
- `ai-surgeon-systems.js` — shared engine (`AISS`) wired into both playable modules
- `trauma_physiology.js` — trauma vitals loop shared with the headless playtest
- `art/hero-surgical-table.jpg` — hub hero, appendectomy card, load field
- `art/key-art-x.jpg` — brand mark, trauma card / load screen

Prototype anatomy is still placeholder geometry (the storyboard says so). Not a clinical reference.

```bash
python3 -m unittest tests.test_ai_surgeon tests.test_ai_surgeon_hub tests.test_ai_surgeon_docs tests.test_ai_surgeon_screens
node --test ai_surgeon/tests/*.mjs
```
