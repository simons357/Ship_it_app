# VAL8000 little square — type now, voice later

Product truth for the magazine overlay in [`magazine/`](magazine/).

VAL8000 is a **persistent little square** in the view: red-eye panel,
idle mouth a straight line, smile after he replies. He lives on the
existing Issue 1 stack. He is not the lead. He is not a second magazine.

## Interaction

He **types** in the box. That is the whole mouth for now.

- Typed transcript in the box
- Help line for unanswered questions, then a smile
- No audio
- No Autoplay
- No `val8000_speak.py` from the UI
- No espeak / Mac `say`
- No stock ElevenLabs

Voice later: only after Jon’s real ElevenLabs **clone** is wired.
Stock library voices are forbidden. Until then he only TYPES.

## Mouth

| State | Asset | When |
|---|---|---|
| Idle | `assets/val8000-mouth-line.png` | Waiting. Straight line. |
| After he types | `assets/val8000-mouth-smile.png` | Default post-answer face. |
| Lens-only | `assets/val8000-eye-mark.png` | Eye without the mouth, if a crop needs it. |

Metal teeth stay off this square.

## Honesty (the box may not break these)

- He does not invent theorems.
- He does not stamp TRANSFORMABLE without a real T.
- **DA-VC-01 stays FAIL.**
- Unaugmented leftover stays OPEN.
- Reported ≠ certified.
- Issue 1 stays Issue 1.

Unanswered questions get a help line that already carries those locks,
then he smiles. He does not fill silence with a fake close.

## Files

- [`magazine/val8000/val8000-box.js`](magazine/val8000/val8000-box.js) — magazine square + typed transcript
- [`magazine/val8000/val8000-comments.js`](magazine/val8000/val8000-comments.js) — help line + honesty catalog
- Domain Architect dock: `domain_architect/static/val8000/` (same type-now rule)
- Persona: [`val8000.md`](val8000.md)

Preview: `docs/cosmic-graffiti/magazine/preview.sh` then open Issue 1.
The live production site is not wiped by this overlay.
