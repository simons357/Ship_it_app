# VAL8000 skins — accessories on the same square

Skins are **accessories**, like a seasonal logo hat. Same little square: red
circular lens on a dark panel. Same character. Public name **VAL8000**.

Default skin: the naked square.

Skins are accessories, not a new character.

Idle mouth stays a straight line under every skin.

He still types in the box. No TTS. No stock voice.

## How to change

Clip-on for the always-in-the-view square (sibling widget HTML stays theirs):

1. Keep the face image as the idle line (`val8000-mouth-line.png`).
2. Add an empty `<img class="val8000-accessory" alt="" hidden>` on
   `.val8000-square`.
3. Include [`assets/val8000-skins.css`](assets/val8000-skins.css) and
   [`assets/val8000-skins.js`](assets/val8000-skins.js).
4. Set `data-skin` on `.val8000-square`, or call
   `VAL8000_applySkin(squareEl, "frequency")`.

Catalog: [`assets/skins/skins.json`](assets/skins/skins.json).

| `data-skin` | Accessory | Overlay |
|---|---|---|
| `naked` (default) | none | — |
| `frequency` | tiny gold Frequency ribbon | [`skins/overlay-frequency.svg`](assets/skins/overlay-frequency.svg) |
| `weekend-update` | Weekend Update glasses | [`skins/overlay-weekend-update.svg`](assets/skins/overlay-weekend-update.svg) |
| `issue1` | two red pills, both red | [`skins/overlay-issue1.svg`](assets/skins/overlay-issue1.svg) |
| `scientist` | scientist visor | [`skins/overlay-scientist.svg`](assets/skins/overlay-scientist.svg) |
| `music-art` | quiet music / art room pin | [`skins/overlay-music-art.svg`](assets/skins/overlay-music-art.svg) |

How to change: set `data-skin`.

Masthead stays the naked square with the idle straight line. Accessories
are issue / night looks, not a second face.

## Mouth still wins

Accessories sit **on** the square. They do not rewrite the mouth:

- Idle: straight line.
- After a normal answer: smile.
- Teeth: compliment, funny joke, or sarcasm. Never idle. Never masthead.

## Legal fence (house)

- Original overlays. No film stills. No studio logos. No Google marks.
- Public name VAL8000. Do not print the other computer’s name as the
  character name.
- Rebuild overlays with `python3 scripts/build_val8000_skins.py`.
