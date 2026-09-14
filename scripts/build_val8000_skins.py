#!/usr/bin/env python3
"""Build VAL8000 accessory overlay PNGs and a walkthrough sheet.

Overlays are transparent layers for the same 1024 square as
val8000-mouth-line.png. They do not redraw the eye or the idle mouth.
"""

from __future__ import annotations

from pathlib import Path

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "cosmic-graffiti" / "assets"
SKINS = ASSETS / "skins"
IDLE = ASSETS / "val8000-mouth-line.png"
SHEET = Path("/opt/cursor/artifacts/val8000_skins_sheet.png")

GOLD = (201, 162, 39, 255)
GOLD_LT = (243, 217, 138, 255)
NAVY = (10, 16, 28, 255)
NAVY_MID = (22, 38, 68, 230)
RED = (193, 18, 31, 255)
RED_LT = (220, 70, 70, 255)
WHITE = (248, 244, 232, 255)


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = Path("/usr/share/fonts/truetype/dejavu") / name
    if path.is_file():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _blank(scale: int = 2) -> tuple[Image.Image, ImageDraw.ImageDraw, int]:
    size = 1024 * scale
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im, "RGBA"), scale


def _down(im: Image.Image, scale: int) -> Image.Image:
    return im.resize((1024, 1024), Image.Resampling.LANCZOS)


def overlay_frequency() -> Image.Image:
    im, d, s = _blank()
    # Gold ribbon across the top of the dark panel.
    y0, y1 = 92 * s, 168 * s
    d.polygon(
        [
            (110 * s, y0 + 18 * s),
            (914 * s, y0),
            (918 * s, y1 - 10 * s),
            (106 * s, y1),
        ],
        fill=GOLD,
    )
    d.polygon(
        [
            (122 * s, y0 + 28 * s),
            (902 * s, y0 + 14 * s),
            (904 * s, y1 - 24 * s),
            (120 * s, y1 - 16 * s),
        ],
        fill=NAVY,
    )
    # Fold tab
    d.polygon(
        [
            (106 * s, y1),
            (148 * s, y1),
            (128 * s, y1 + 28 * s),
        ],
        fill=(160, 120, 20, 255),
    )
    font = _font(36 * s, bold=True)
    text = "FREQUENCY"
    bbox = d.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    d.text(((1024 * s - tw) / 2, y0 + 38 * s), text, font=font, fill=GOLD_LT)
    return _down(im, s)


def overlay_weekend_update() -> Image.Image:
    im, d, s = _blank()
    # Thin gold glasses sitting on the one-eye square.
    stroke = max(5 * s, 8)
    left = (360 * s, 390 * s, 500 * s, 530 * s)
    right = (524 * s, 390 * s, 664 * s, 530 * s)
    d.ellipse(left, outline=GOLD, width=stroke)
    d.ellipse(right, outline=GOLD_LT, width=stroke)
    d.line((500 * s, 458 * s, 524 * s, 458 * s), fill=GOLD, width=stroke)
    d.line((280 * s, 430 * s, 360 * s, 448 * s), fill=GOLD, width=max(3 * s, 6))
    d.line((664 * s, 448 * s, 744 * s, 430 * s), fill=GOLD, width=max(3 * s, 6))
    return _down(im, s)


def overlay_issue1() -> Image.Image:
    im, d, s = _blank()
    # Two red capsules on a small gold pin plate. Both red — Jon's gag.
    plate = (118 * s, 720 * s, 310 * s, 900 * s)
    d.rounded_rectangle(plate, radius=28 * s, fill=NAVY, outline=GOLD, width=4 * s)
    font = _font(18 * s, bold=True)
    d.text((148 * s, 736 * s), "ISSUE 1", font=font, fill=GOLD_LT)

    def capsule(cx: int, cy: int) -> None:
        box = (cx - 28 * s, cy - 54 * s, cx + 28 * s, cy + 54 * s)
        d.rounded_rectangle(box, radius=28 * s, fill=RED, outline=GOLD_LT, width=3 * s)
        d.ellipse(
            (cx - 12 * s, cy - 44 * s, cx + 8 * s, cy - 22 * s),
            fill=RED_LT,
        )

    capsule(175 * s, 820 * s)
    capsule(248 * s, 820 * s)
    return _down(im, s)


def overlay_scientist() -> Image.Image:
    im, d, s = _blank()
    # Lab visor across the lens. Does not cover the idle mouth line.
    d.rounded_rectangle(
        (250 * s, 318 * s, 774 * s, 428 * s),
        radius=36 * s,
        fill=NAVY_MID,
        outline=GOLD,
        width=5 * s,
    )
    d.rectangle((270 * s, 348 * s, 754 * s, 368 * s), fill=(180, 220, 255, 70))
    d.line((270 * s, 400 * s, 754 * s, 400 * s), fill=GOLD_LT, width=2 * s)
    return _down(im, s)


def overlay_music_art() -> Image.Image:
    im, d, s = _blank()
    # Quiet music / art-room pin, lower right.
    cx, cy, r = 812 * s, 812 * s, 78 * s
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=NAVY, outline=GOLD, width=5 * s)
    # Tiny frame
    d.rounded_rectangle(
        (cx - 40 * s, cy - 28 * s, cx - 4 * s, cy + 22 * s),
        radius=4 * s,
        outline=GOLD_LT,
        width=3 * s,
    )
    d.rectangle((cx - 32 * s, cy - 16 * s, cx - 12 * s, cy + 10 * s), fill=GOLD)
    # Note
    d.ellipse((cx + 6 * s, cy + 6 * s, cx + 34 * s, cy + 28 * s), fill=GOLD_LT)
    d.rectangle((cx + 28 * s, cy - 28 * s, cx + 34 * s, cy + 18 * s), fill=GOLD_LT)
    d.polygon(
        [
            (cx + 34 * s, cy - 28 * s),
            (cx + 54 * s, cy - 18 * s),
            (cx + 34 * s, cy - 8 * s),
        ],
        fill=GOLD,
    )
    return _down(im, s)


OVERLAYS = {
    "frequency": overlay_frequency,
    "weekend-update": overlay_weekend_update,
    "issue1": overlay_issue1,
    "scientist": overlay_scientist,
    "music-art": overlay_music_art,
}


def composite(base: Image.Image, overlay: Image.Image) -> Image.Image:
    out = base.convert("RGBA")
    layer = overlay.convert("RGBA")
    if layer.size != out.size:
        layer = layer.resize(out.size, Image.Resampling.LANCZOS)
    out.alpha_composite(layer)
    return out.convert("RGB")


def sheet(idle: Image.Image, overlays: dict[str, Image.Image], path: Path) -> None:
    cells = [
        (None, "DEFAULT  ·  naked square"),
        ("frequency", "FREQUENCY  ·  gold ribbon"),
        ("weekend-update", "WEEKEND UPDATE  ·  glasses"),
        ("issue1", "ISSUE 1  ·  two red pills"),
    ]
    cell, pad, label_h = 520, 24, 64
    cols = 4
    canvas = Image.new(
        "RGB",
        (pad + cols * (cell + pad), pad + cell + label_h + pad),
        (18, 18, 18),
    )
    draw = ImageDraw.Draw(canvas)
    font = _font(22)
    for i, (key, label) in enumerate(cells):
        face = idle.copy() if key is None else composite(idle, overlays[key])
        face.thumbnail((cell, cell), Image.Resampling.LANCZOS)
        x = pad + i * (cell + pad) + (cell - face.width) // 2
        y = pad + (cell - face.height) // 2
        canvas.paste(face, (x, y))
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(
            (pad + i * (cell + pad) + cell // 2 - tw // 2, pad + cell + 16),
            label,
            font=font,
            fill=(232, 232, 232),
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(path, "PNG")
    print("sheet", path, canvas.size)


def main() -> None:
    SKINS.mkdir(parents=True, exist_ok=True)
    idle = Image.open(IDLE).convert("RGB")
    built: dict[str, Image.Image] = {}
    for name, fn in OVERLAYS.items():
        overlay = fn()
        dest = SKINS / f"overlay-{name}.png"
        overlay.save(dest, "PNG")
        built[name] = overlay
        print("wrote", dest, overlay.size, overlay.mode)
    sheet(idle, built, SHEET)


if __name__ == "__main__":
    main()
