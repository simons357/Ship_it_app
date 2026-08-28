# AI Surgeon — phone screens and generators

Same product as the residency hub in this folder, not a second app.
Surgery and anaesthesia are two seats of one case.

This is a training simulation. It is **not** a medical device and is
**not** cleared by any regulator.

## How to run the product

```bash
# from the repository root
python3 -m ai_surgeon
# hub:     http://127.0.0.1:8770/
# screens: http://127.0.0.1:8770/screens.html
```

Or, from this directory: `python3 -m http.server 8770`

## How to run brochure.py and mockups.py

Generators live next to their outputs so `brochure.py` can find the
phone PNGs `mockups.py` just wrote (same `OUT` directory).

```bash
cd ai_surgeon/generators
python3 mockups.py
# writes screen-01-study-one.png … screen-06-teach-one.png
# and matching .svg

python3 brochure.py
# writes AI-Surgeon-Brochure.pdf
# requires the six screen-*.png files from mockups.py
```

Dependencies: `reportlab` (brochure) and `cairosvg` (PNG raster from SVG).
DejaVu Sans must be on the machine for the mockup type.

```bash
pip install reportlab cairosvg
```

## Where the screens live

| Path | What |
|---|---|
| `stills/01-…png` … `stills/16-…png` | The 16 design stills (visual spec) |
| `screens.html` + `phone.js` | Phone-first playable chrome using those stills |
| `generators/screen-*.png` | Six generated phone UIs from `mockups.py` |
| `generators/AI-Surgeon-Brochure.pdf` | Concept brochure |
| `index.html` | Residency hub (sibling ingest). Links the screens. |
| `ai-surgeon-prototype.html` | Playable open appendectomy (sibling). Do not replace. |
| `ai-surgeon-module02-trauma.html` | Playable Module 21 trauma (sibling). Do not replace. |

## Playable vs pitch-only

**Playable on `screens.html` (hash routes):**

- `#identify` — ASK / MISS / HIT on the real cecum–appendix still
- `#lab` — FIELD / ADD / SUBTRACT layer toggles
- `#anatomy` — raw meshes A/B
- `#study` `#see` `#do` `#call` — Study / See / Do One + sterile back table
- `#anesthesia` — The Pen at the head of the bed: twist = plunger, airway MASK/LMA/ETT
- `#pen` — THEIRS instrument language: one stylus, exploration vs curriculum, twist / click / squeeze
- `#nib` — twist raises the tray, click takes the instrument (same Pen)
- `#verse` — surgeon / anaesthesia / scrub, case spin
- `#trauma` — Case 07 tension pneumothorax (phone still). Death enabled.

**Pitch-only stills** (hardware/art, not a sim):

- `#hardware` phone / iPad / VR ladder
- `#art` placeholder vs scanned mesh
- `#tablet` pencil + mat HUD
- `#stylus` twist-stylus hardware diagram
- Teach One debrief exists as a generated mockup (`screen-06-teach-one.png`)
  and in the brochure; it is not the real “supervise a junior” loop yet.

**Playable sibling modules (do not clobber):**

- Open appendectomy prototype
- Module 21 tube thoracostomy with live physiology

## Interaction rule

Twist to choose, touch to commit. No double-tap, no long-press, no dropdown.
On a phone without the physical nib, the on-screen knob / `Q` `E` / arrows
stand in for the twist; a click (tap / Enter) commits; `F` squeezes.
The dedicated trainer is [`pen.html`](pen.html). Spec: [`docs/THE-PEN.md`](docs/THE-PEN.md).
The Pen is the language, not a Kelly clamp. Not a tray of toy instruments.
