#!/usr/bin/env python3
"""Build VAL8000 accessory overlay PNGs and a walkthrough sheet.

Overlays are transparent layers for the same 1024 square as
val8000-mouth-line.png. They do not redraw the eye or the idle mouth.
"""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

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


def overlay_glasses_ordinary(camera: bool = False) -> Image.Image:
    """Round original frames on the square. Optional small camera on the rim."""
    scale = 2
    size = 1024 * scale
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    cx, cy = 512 * scale, 461 * scale
    gold = (201, 162, 39, 255)
    gold_dark = (92, 70, 18, 255)
    gold_light = (236, 210, 120, 255)
    r = 124 * scale
    dx = 134 * scale
    ly = cy - 6
    lx, rx = cx - dx, cx + dx

    def bbox(x, y, rad):
        return [x - rad, y - rad, x + rad, y + rad]

    temple_y = ly + 12
    temple_end_y = temple_y + 40
    d.line([(lx - r + 10, temple_y), (200, temple_end_y)], fill=gold_dark, width=20)
    d.line([(lx - r + 10, temple_y), (200, temple_end_y)], fill=gold, width=12)
    d.line([(rx + r - 10, temple_y), (size - 200, temple_end_y)], fill=gold_dark, width=20)
    d.line([(rx + r - 10, temple_y), (size - 200, temple_end_y)], fill=gold, width=12)
    for ex, ey in ((200, temple_end_y), (size - 200, temple_end_y)):
        d.ellipse([ex - 10, ey - 10, ex + 10, ey + 10], fill=gold)
        d.ellipse([ex - 6, ey - 6, ex + 6, ey + 6], fill=gold_light)

    glass = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glass, "RGBA")
    for x in (lx, rx):
        gd.ellipse(bbox(x, ly, r - 8), fill=(186, 210, 230, 38))
        gd.arc(bbox(x - 20, ly - 36, r - 78), start=200, end=300, fill=(255, 255, 255, 90), width=16)
    layer = Image.alpha_composite(layer, glass.filter(ImageFilter.GaussianBlur(radius=4)))
    d = ImageDraw.Draw(layer, "RGBA")
    for x in (lx, rx):
        d.ellipse(bbox(x, ly, r + 8), outline=gold_dark, width=16)
        d.ellipse(bbox(x, ly, r), outline=gold, width=24)
        d.ellipse(bbox(x, ly, r - 12), outline=gold_light, width=6)
    d.arc([lx + r - 36, ly - 88, rx - r + 36, ly + 70], start=210, end=330, fill=gold_dark, width=18)
    d.arc([lx + r - 36, ly - 88, rx - r + 36, ly + 70], start=210, end=330, fill=gold, width=11)
    for hx, hy in ((lx - r + 4, ly + 10), (rx + r - 4, ly + 10)):
        d.ellipse([hx - 16, hy - 16, hx + 16, hy + 16], fill=gold_dark)
        d.ellipse([hx - 10, hy - 10, hx + 10, hy + 10], fill=gold_light)
    if camera:
        cam_cx, cam_cy = rx + r - 4, ly - 56
        d.ellipse([cam_cx - 48, cam_cy - 48, cam_cx + 48, cam_cy + 48], fill=(55, 55, 58, 255))
        d.ellipse([cam_cx - 44, cam_cy - 44, cam_cx + 44, cam_cy + 44], fill=(28, 28, 32, 255))
        d.ellipse([cam_cx - 40, cam_cy - 40, cam_cx + 40, cam_cy + 40], outline=(190, 190, 195, 255), width=6)
        d.ellipse([cam_cx - 26, cam_cy - 26, cam_cx + 26, cam_cy + 26], fill=(12, 14, 18, 255))
        d.ellipse([cam_cx - 12, cam_cy - 12, cam_cx + 12, cam_cy + 12], fill=(24, 30, 38, 255))
        d.ellipse([cam_cx + 14, cam_cy - 30, cam_cx + 28, cam_cy - 16], fill=(64, 72, 66, 255))
        d.ellipse([cam_cx - 16, cam_cy - 18, cam_cx - 4, cam_cy - 6], fill=(220, 230, 240, 200))
    return layer.resize((1024, 1024), Image.Resampling.LANCZOS)


def overlay_monocle() -> Image.Image:
    """One original round gold lens on the red-eye square. Same CG gold as ordinary glasses."""
    scale = 2
    size = 1024 * scale
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    cx, cy = 512 * scale, 461 * scale
    gold = (201, 162, 39, 255)
    gold_dark = (92, 70, 18, 255)
    gold_light = (236, 210, 120, 255)
    r = 152 * scale
    ly = cy - 6

    def bbox(x, y, rad):
        return [x - rad, y - rad, x + rad, y + rad]

    glass = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glass, "RGBA")
    gd.ellipse(bbox(cx, ly, r - 8), fill=(186, 210, 230, 38))
    gd.arc(
        bbox(cx - 24, ly - 40, r - 86),
        start=200,
        end=300,
        fill=(255, 255, 255, 90),
        width=16,
    )
    layer = Image.alpha_composite(layer, glass.filter(ImageFilter.GaussianBlur(radius=4)))
    d = ImageDraw.Draw(layer, "RGBA")
    d.ellipse(bbox(cx, ly, r + 8), outline=gold_dark, width=16)
    d.ellipse(bbox(cx, ly, r), outline=gold, width=24)
    d.ellipse(bbox(cx, ly, r - 12), outline=gold_light, width=6)

    attach_ang = math.radians(28)
    hx = cx + int((r - 4) * math.cos(attach_ang))
    hy = ly + int((r - 4) * math.sin(attach_ang))
    d.ellipse([hx - 16, hy - 16, hx + 16, hy + 16], fill=gold_dark)
    d.ellipse([hx - 10, hy - 10, hx + 10, hy + 10], fill=gold_light)

    chain_end = (cx + 250 * scale, ly + 250 * scale)
    ctrl = (cx + 210 * scale, ly + 110 * scale)
    start = (hx + 8, hy + 10)

    def quad(t: float) -> tuple[int, int]:
        mt = 1 - t
        x = mt * mt * start[0] + 2 * mt * t * ctrl[0] + t * t * chain_end[0]
        y = mt * mt * start[1] + 2 * mt * t * ctrl[1] + t * t * chain_end[1]
        return int(x), int(y)

    chain_pts = [quad(i / 24) for i in range(25)]
    d.line(chain_pts, fill=gold_dark, width=10)
    d.line(chain_pts, fill=gold, width=6)
    for i in (6, 12, 18):
        px, py = chain_pts[i]
        d.ellipse([px - 12, py - 12, px + 12, py + 12], outline=gold_dark, width=6)
        d.ellipse([px - 12, py - 12, px + 12, py + 12], outline=gold, width=3)
    ex, ey = chain_pts[-1]
    d.ellipse([ex - 22, ey - 22, ex + 22, ey + 22], outline=gold_dark, width=8)
    d.ellipse([ex - 22, ey - 22, ex + 22, ey + 22], outline=gold, width=5)
    d.ellipse([ex - 8, ey - 8, ex + 8, ey + 8], fill=gold_light)
    return layer.resize((1024, 1024), Image.Resampling.LANCZOS)


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
    ordinary = overlay_glasses_ordinary(False)
    camera = overlay_glasses_ordinary(True)
    (SKINS / "glasses-ordinary.png").parent.mkdir(parents=True, exist_ok=True)
    ordinary.save(SKINS / "glasses-ordinary.png", "PNG")
    camera.save(SKINS / "glasses-camera.png", "PNG")
    print("wrote", SKINS / "glasses-ordinary.png")
    print("wrote", SKINS / "glasses-camera.png")
    composite(idle, ordinary).save(SKINS / "worn-glasses-ordinary.png", "PNG")
    composite(idle, camera).save(SKINS / "worn-glasses-camera.png", "PNG")
    monocle = overlay_monocle()
    monocle.save(SKINS / "monocle.png", "PNG")
    print("wrote", SKINS / "monocle.png")
    composite(idle, monocle).save(SKINS / "worn-monocle.png", "PNG")
    print("wrote", SKINS / "worn-monocle.png")
    sheet(idle, built, SHEET)


if __name__ == "__main__":
    main()
