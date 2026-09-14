#!/usr/bin/env python3
"""Original VAL8000 stripe-body paint.

Cream / red / black angular tape on the square panel. Circular lens cutout
so the red camera eye (and teeth-in-rings) show through. Thin idle line.
Not a photo. No third-party wordmarks.
"""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "cosmic-graffiti" / "assets"
SKINS = ASSETS / "skins"
IDLE = ASSETS / "val8000-mouth-line.png"

OUT_OVERLAY = SKINS / "val8000-skin-stripe-body.png"
OUT_SHEET = SKINS / "val8000-skin-stripe-body-sheet.png"

# Geometry of val8000-mouth-line.png (1024 canvas).
LENS_CX, LENS_CY = 510.0, 461.0
LENS_R = 250.0  # outer bezel; stripes stop here so rings stay the face
PANEL = (70, 64, 952, 952)
PANEL_RADIUS = 36
MOUTH = ((373, 772), (650, 772))
NAME_Y = 834

CREAM = (247, 236, 208, 255)
TAPE_BLACK = (18, 16, 16, 255)
TAPE_RED = (163, 16, 26, 255)
TAPE_YELLOW = (196, 154, 48, 255)
LINE = (46, 46, 46, 255)
NAME = (250, 250, 250, 255)
NAME_SHADOW = (32, 28, 26, 220)

# Original tape pieces. A few bold families, cream islands, not a hash.
# (color, x0, y0, x1, y1, width, jag, phase) in 1024-space.
TAPES: list[tuple[str, float, float, float, float, float, float, float]] = [
    ("black", -160, 20, 1280, 390, 96, 9.0, 0.3),
    ("red", -160, 175, 1280, 560, 74, 7.5, 1.15),
    ("black", -160, 430, 1280, 820, 52, 6.0, 2.05),
    ("red", -180, -70, 1280, 210, 58, 6.5, 0.7),
    ("black", 250, -120, 40, 1280, 68, 8.0, 1.6),
    ("red", 1320, -80, 420, 1280, 88, 8.5, 0.45),
    ("black", 620, 1280, 1280, 430, 46, 5.5, 2.3),
    ("red", -120, 910, 560, 1280, 70, 7.0, 1.35),
    ("black", 1080, 80, 1280, 520, 38, 4.0, 0.9),
    ("yellow", 918, -30, 988, 1080, 8, 1.6, 0.4),
]


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = Path("/usr/share/fonts/truetype/dejavu") / name
    if path.is_file():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def _tape_polygon(
    p0: tuple[float, float],
    p1: tuple[float, float],
    width: float,
    jag: float,
    phase: float,
    samples: int = 36,
) -> list[tuple[int, int]]:
    dx = p1[0] - p0[0]
    dy = p1[1] - p0[1]
    length = math.hypot(dx, dy) or 1.0
    px, py = -dy / length, dx / length
    left: list[tuple[int, int]] = []
    right: list[tuple[int, int]] = []
    for i in range(samples + 1):
        t = i / samples
        j = jag * math.sin(t * 8.7 + phase) + 0.42 * jag * math.sin(t * 19.1 + phase * 1.6)
        if 0.28 + 0.04 * math.sin(phase) < t < 0.35 + 0.04 * math.sin(phase):
            j += jag * 0.85
        if 0.58 < t < 0.66:
            j -= jag * 0.5
        taper = 0.86 + 0.28 * t
        w = (width / 2.0) * taper + j
        x = p0[0] + dx * t
        y = p0[1] + dy * t
        left.append((int(round(x + px * w)), int(round(y + py * w))))
        right.append((int(round(x - px * w)), int(round(y - py * w))))
    return left + list(reversed(right))


def _draw_tape(
    draw: ImageDraw.ImageDraw,
    color: str,
    p0: tuple[float, float],
    p1: tuple[float, float],
    width: float,
    jag: float,
    phase: float,
) -> None:
    if color == "black":
        fill = TAPE_BLACK
    elif color == "red":
        fill = TAPE_RED
    else:
        fill = TAPE_YELLOW
    poly = _tape_polygon(p0, p1, width, jag, phase)
    draw.polygon(poly, fill=fill)


def _panel_mask(size: int, scale: int) -> Image.Image:
    mask = Image.new("L", (size, size), 0)
    d = ImageDraw.Draw(mask)
    x0, y0, x1, y1 = [c * scale for c in PANEL]
    d.rounded_rectangle([x0, y0, x1, y1], radius=PANEL_RADIUS * scale, fill=255)
    return mask.filter(ImageFilter.GaussianBlur(radius=0.6 * scale))


def _lens_alpha(h: int, w: int, scale: int) -> np.ndarray:
    cy = LENS_CY * scale
    cx = LENS_CX * scale
    r = LENS_R * scale
    yy, xx = np.ogrid[:h, :w]
    dist = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
    aa = 2.2 * scale
    return np.clip((dist - r) / aa, 0.0, 1.0).astype(np.float32)


def _draw_spaced_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    cx: float,
    y: float,
    font: ImageFont.ImageFont,
    fill: tuple[int, int, int, int],
    spacing: float,
) -> None:
    widths = [draw.textlength(ch, font=font) for ch in text]
    total = float(sum(widths)) + spacing * (len(text) - 1)
    x = cx - total / 2.0
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=font, fill=fill)
        x += float(w) + spacing


def overlay_stripe_body(scale: int = 2) -> Image.Image:
    """RGBA overlay: painted panel, lens cut out, idle line, VAL8000 name."""
    size = 1024 * scale
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im, "RGBA")
    x0, y0, x1, y1 = [c * scale for c in PANEL]
    d.rounded_rectangle(
        [x0, y0, x1, y1],
        radius=PANEL_RADIUS * scale,
        fill=CREAM,
    )

    blacks = [t for t in TAPES if t[0] == "black"]
    reds = [t for t in TAPES if t[0] == "red"]
    yellows = [t for t in TAPES if t[0] == "yellow"]
    for color, x_a, y_a, x_b, y_b, width, jag, phase in blacks + reds + yellows:
        _draw_tape(
            d,
            color,
            (x_a * scale, y_a * scale),
            (x_b * scale, y_b * scale),
            width * scale,
            jag * scale,
            phase,
        )

    # Thin idle mouth — a line, not a pickguard jaw.
    mx0, my0 = MOUTH[0][0] * scale, MOUTH[0][1] * scale
    mx1, my1 = MOUTH[1][0] * scale, MOUTH[1][1] * scale
    d.line([(mx0, my0), (mx1, my1)], fill=LINE, width=max(3, int(3.6 * scale)))

    # Dark ring where paint meets the camera, then the hole is punched later.
    cx, cy, r = LENS_CX * scale, LENS_CY * scale, LENS_R * scale
    d.ellipse(
        [cx - r - 2, cy - r - 2, cx + r + 2, cy + r + 2],
        outline=(22, 18, 16, 200),
        width=max(2, 2 * scale),
    )

    font = _font(20 * scale, bold=True)
    _draw_spaced_text(
        d,
        "VAL8000",
        LENS_CX * scale,
        NAME_Y * scale,
        font,
        NAME_SHADOW,
        spacing=3 * scale,
    )
    _draw_spaced_text(
        d,
        "VAL8000",
        LENS_CX * scale - 1,
        NAME_Y * scale - 1 * scale,
        font,
        NAME,
        spacing=3 * scale,
    )

    arr = np.array(im)
    rng = np.random.RandomState(8000)
    grain = rng.randint(-7, 8, (size, size, 3), dtype=np.int16)
    rgb = arr[:, :, :3].astype(np.int16) + grain
    arr[:, :, :3] = np.clip(rgb, 0, 255).astype(np.uint8)

    panel = np.array(_panel_mask(size, scale), dtype=np.float32) / 255.0
    lens = _lens_alpha(size, size, scale)
    arr[:, :, 3] = (arr[:, :, 3].astype(np.float32) * panel * lens).astype(np.uint8)
    out = Image.fromarray(arr, "RGBA")
    if scale != 1:
        out = out.resize((1024, 1024), Image.Resampling.LANCZOS)
    return out


def draw_teeth_in_rings(face: Image.Image) -> Image.Image:
    """Sheet-only metal teeth inside an inner aperture ring. No chin."""
    im = face.convert("RGBA")
    layer = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer, "RGBA")
    cx, cy = LENS_CX, LENS_CY
    # Sit in the inner rings (r ~ 120–165), never below the bezel, never on the pupil.
    r_base = 158
    r_tip = 122
    n = 15
    arc0, arc1 = 22.0, 158.0
    for i in range(n):
        span = (arc1 - arc0) / n
        t0 = math.radians(arc0 + span * i + 0.6)
        t1 = math.radians(arc0 + span * (i + 0.82))
        tm = 0.5 * (t0 + t1)
        gum_a = (cx + (r_base + 6) * math.cos(t0), cy + (r_base + 6) * math.sin(t0))
        gum_b = (cx + (r_base + 6) * math.cos(t1), cy + (r_base + 6) * math.sin(t1))
        gum_c = (cx + (r_tip + 8) * math.cos(tm), cy + (r_tip + 8) * math.sin(tm))
        d.polygon([gum_a, gum_b, gum_c], fill=(48, 14, 16, 230))
        p_base_a = (cx + r_base * math.cos(t0), cy + r_base * math.sin(t0))
        p_base_b = (cx + r_base * math.cos(t1), cy + r_base * math.sin(t1))
        p_tip_l = (
            cx + r_tip * math.cos(tm - 0.03),
            cy + r_tip * math.sin(tm - 0.03),
        )
        p_tip_r = (
            cx + r_tip * math.cos(tm + 0.03),
            cy + r_tip * math.sin(tm + 0.03),
        )
        d.polygon(
            [p_base_a, p_base_b, p_tip_r, p_tip_l],
            fill=(214, 216, 220, 255),
        )
        d.polygon(
            [
                p_base_a,
                (
                    cx + (r_base - 10) * math.cos(t0 + 0.04),
                    cy + (r_base - 10) * math.sin(t0 + 0.04),
                ),
                p_tip_l,
            ],
            fill=(248, 248, 250, 255),
        )
        d.line([p_base_a, p_tip_l], fill=(90, 92, 98, 255), width=1)
        d.line([p_base_b, p_tip_r], fill=(120, 122, 128, 255), width=1)

    pupil_r = 48
    punch = Image.new("L", im.size, 0)
    pd = ImageDraw.Draw(punch)
    pd.ellipse(
        [cx - pupil_r, cy - pupil_r, cx + pupil_r, cy + pupil_r],
        fill=255,
    )
    layer.putalpha(ImageChops_subtract_alpha(layer, punch))
    out = Image.alpha_composite(im, layer)
    return out.convert("RGB")


def ImageChops_subtract_alpha(layer: Image.Image, punch: Image.Image) -> Image.Image:
    alpha = layer.getchannel("A")
    inverted = punch.point(lambda v: 255 - v)
    return ImageChops_multiply(alpha, inverted)


def ImageChops_multiply(a: Image.Image, b: Image.Image) -> Image.Image:
    aa = np.array(a, dtype=np.uint16)
    bb = np.array(b, dtype=np.uint16)
    return Image.fromarray(((aa * bb) // 255).astype(np.uint8), mode="L")


def _composite(base: Image.Image, overlay: Image.Image) -> Image.Image:
    out = base.convert("RGBA")
    layer = overlay.convert("RGBA")
    if layer.size != out.size:
        layer = layer.resize(out.size, Image.Resampling.LANCZOS)
    out.alpha_composite(layer)
    return out


def stripe_body_sheet(idle: Image.Image, overlay: Image.Image) -> Image.Image:
    idle_worn = _composite(idle, overlay).convert("RGB")
    teeth_worn = draw_teeth_in_rings(idle_worn)

    cell, pad, label_h = 520, 28, 72
    cols = 2
    canvas = Image.new(
        "RGB",
        (pad + cols * (cell + pad), pad + cell + label_h + pad),
        (18, 18, 18),
    )
    draw = ImageDraw.Draw(canvas)
    font = _font(22)
    cells = [
        (idle_worn, "STRIPE BODY  ·  idle line"),
        (teeth_worn, "STRIPE BODY  ·  teeth in rings"),
    ]
    for i, (face, label) in enumerate(cells):
        thumb = face.copy()
        thumb.thumbnail((cell, cell), Image.Resampling.LANCZOS)
        x = pad + i * (cell + pad) + (cell - thumb.width) // 2
        y = pad + (cell - thumb.height) // 2
        canvas.paste(thumb, (x, y))
        bbox = draw.textbbox((0, 0), label, font=font)
        tw = bbox[2] - bbox[0]
        draw.text(
            (pad + i * (cell + pad) + cell // 2 - tw // 2, pad + cell + 18),
            label,
            font=font,
            fill=(232, 232, 232),
        )
    return canvas


def build(dest_overlay: Path | None = None, dest_sheet: Path | None = None) -> tuple[Path, Path]:
    dest_overlay = dest_overlay or OUT_OVERLAY
    dest_sheet = dest_sheet or OUT_SHEET
    dest_overlay.parent.mkdir(parents=True, exist_ok=True)
    overlay = overlay_stripe_body()
    overlay.save(dest_overlay, "PNG")
    idle = Image.open(IDLE).convert("RGBA")
    sheet = stripe_body_sheet(idle, overlay)
    dest_sheet.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(dest_sheet, "PNG")
    print("wrote", dest_overlay, overlay.size, overlay.mode)
    print("wrote", dest_sheet, sheet.size, sheet.mode)
    return dest_overlay, dest_sheet


if __name__ == "__main__":
    build()
