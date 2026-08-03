#!/usr/bin/env python3
"""Prime Field Technologies logo — Borromean rings mark + gold wordmark."""

from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "assets"
ARTIFACTS = Path("/opt/cursor/artifacts")
FONTS = Path("/workspace/linkedin-crna/assets/fonts")

BLACK = (0, 0, 0)
GOLD = (212, 175, 88)
GOLD_HI = (245, 220, 140)
GOLD_LO = (150, 110, 45)
BLUE = (120, 190, 220)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    for base in (FONTS, Path("/usr/share/fonts/truetype/dejavu")):
        path = base / name
        if path.exists():
            return ImageFont.truetype(str(path), size=size)
    # Fallbacks
    for p in [
        FONTS / "SourceSans3-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    ]:
        if Path(p).exists():
            return ImageFont.truetype(p, size=size)
    return ImageFont.load_default()


def gold_color(t: float) -> tuple[int, int, int]:
    t = max(0.0, min(1.0, t))
    if t < 0.5:
        u = t * 2
        return tuple(int(GOLD_LO[i] + (GOLD[i] - GOLD_LO[i]) * u) for i in range(3))
    u = (t - 0.5) * 2
    return tuple(int(GOLD[i] + (GOLD_HI[i] - GOLD[i]) * u) for i in range(3))


def draw_network_disc(img: Image.Image, cx: float, cy: float, radius: float) -> None:
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    # Concentric node rings
    nodes = []
    for ring in range(1, 7):
        r = radius * (ring / 6.5)
        n = 6 + ring * 5
        for i in range(n):
            a = (i / n) * math.tau + ring * 0.15
            x = cx + r * math.cos(a)
            y = cy + r * math.sin(a)
            nodes.append((x, y, ring))
    # faint connections to nearby nodes
    for i, (x1, y1, r1) in enumerate(nodes):
        for x2, y2, r2 in nodes[i + 1 : i + 4]:
            if abs(r1 - r2) <= 1:
                d.line((x1, y1, x2, y2), fill=(*BLUE, 28), width=1)
    for x, y, ring in nodes:
        rad = 1.6 + (6 - ring) * 0.25
        alpha = 50 + ring * 12
        d.ellipse((x - rad, y - rad, x + rad, y + rad), fill=(*BLUE, alpha))
    # soft circular vignette edge
    mask = Image.new("L", img.size, 0)
    md = ImageDraw.Draw(mask)
    md.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(2))
    cropped = Image.new("RGBA", img.size, (0, 0, 0, 0))
    cropped.paste(overlay, (0, 0), mask)
    base = img.convert("RGBA")
    composed = Image.alpha_composite(base, cropped)
    img.paste(composed.convert("RGB"))


def ring_center(i: int, cx: float, cy: float, offset: float) -> tuple[float, float]:
    # Equilateral triangle arrangement
    angles = [-math.pi / 2, math.pi / 6, 5 * math.pi / 6]  # top, bottom-right, bottom-left
    a = angles[i]
    return cx + offset * math.cos(a), cy + offset * math.sin(a)


def draw_borromean(img: Image.Image, cx: float, cy: float, R: float, thickness: float) -> None:
    """Draw gold Borromean rings with approximate interlacing via arc segments."""
    offset = R * 0.62
    centers = [ring_center(i, cx, cy, offset) for i in range(3)]

    # Each ring drawn as several arcs so overlaps read as weaving
    # Order chosen for classic Borromean occlusion pattern
    segments = [
        # ring 0 (top)
        (0, -40, 140),
        (0, 140, 260),
        (0, 260, 320),
        # ring 1 (bottom right)
        (1, 80, 220),
        (1, 220, 360),
        (1, 0, 80),
        # ring 2 (bottom left)
        (2, 200, 340),
        (2, -20, 100),
        (2, 100, 200),
    ]

    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    sd = ImageDraw.Draw(shadow)

    def draw_arc(draw, cxy, start, end, fill, width):
        x, y = cxy
        bbox = (x - R, y - R, x + R, y + R)
        # Pillow arcs: 0° at 3 o'clock, counter-clockwise
        draw.arc(bbox, start=start, end=end, fill=fill, width=width)

    # Soft drop shadow
    for i in range(3):
        draw_arc(sd, (centers[i][0] + 4, centers[i][1] + 6), 0, 360, (0, 0, 0, 90), int(thickness))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))

    # Metallic stroke: dark outer, mid, highlight inner feel via layered arcs
    for ring_i, start, end in segments:
        cxy = centers[ring_i]
        # subtle angle-based gold shift
        mid = (start + end) / 2
        t = 0.45 + 0.35 * math.sin(math.radians(mid))
        col = gold_color(t)
        draw_arc(od, cxy, start, end, (*col, 255), int(thickness))
        # inner highlight rim
        hi = gold_color(min(1.0, t + 0.35))
        draw_arc(od, cxy, start, end, (*hi, 160), max(2, int(thickness * 0.28)))

    base = img.convert("RGBA")
    base = Image.alpha_composite(base, shadow)
    base = Image.alpha_composite(base, overlay)
    img.paste(base.convert("RGB"))


def draw_small_psi(draw: ImageDraw.ImageDraw, cx: int, cy: int, size: int, fill) -> None:
    """Minimal Psi mark as secondary accent."""
    # Stem
    stem_w = max(3, size // 10)
    draw.rounded_rectangle((cx - stem_w // 2, cy - size // 3, cx + stem_w // 2, cy + size // 2), radius=2, fill=fill)
    # Arms
    bbox = (cx - size // 2, cy - size // 2, cx + size // 2, cy + size // 8)
    draw.arc(bbox, start=200, end=340, fill=fill, width=stem_w + 1)


def make_logo(size: int = 1600) -> Image.Image:
    img = Image.new("RGB", (size, size), BLACK)
    draw = ImageDraw.Draw(img)

    cx = size / 2
    mark_cy = size * 0.36
    disc_r = size * 0.28
    ring_r = size * 0.145
    thickness = size * 0.034

    draw_network_disc(img, cx, mark_cy, disc_r)
    draw_borromean(img, cx, mark_cy, ring_r, thickness)

    # Wordmark
    title_f = font("SourceSans3-Bold.ttf", int(size * 0.075))
    sub_f = font("SourceSans3-Regular.ttf", int(size * 0.042))
    # Prefer semibold if available for title feel
    try:
        title_f = font("SourceSans3-Semibold.ttf", int(size * 0.078))
    except Exception:
        pass

    title = "PRIME FIELD"
    sub = "TECHNOLOGIES"
    draw = ImageDraw.Draw(img)

    tw = draw.textlength(title, font=title_f)
    sw = draw.textlength(sub, font=sub_f)
    title_y = int(size * 0.62)
    sub_y = int(size * 0.72)
    draw.text(((size - tw) / 2, title_y), title, font=title_f, fill=GOLD_HI)
    # letter-spaced subtitle
    spaced = "  ".join(list(sub))
    sw = draw.textlength(spaced, font=sub_f)
    draw.text(((size - sw) / 2, sub_y), spaced, font=sub_f, fill=GOLD)

    # Small Psi accent under wordmark
    draw_small_psi(draw, int(cx), int(size * 0.84), int(size * 0.07), GOLD)

    return img


def make_horizontal_lockup(height: int = 420) -> Image.Image:
    """Banner-style lockup: rings left, wordmark right — useful for page headers."""
    width = int(height * 3.2)
    img = Image.new("RGB", (width, height), BLACK)
    mark = make_logo(size=height * 2)
    # Crop mark (rings + a bit of space)
    crop = mark.crop((0, int(height * 0.15), height * 2, int(height * 1.35))).resize(
        (height, height), Image.Resampling.LANCZOS
    )
    # Actually cleaner: regenerate mark area only
    mark_sq = Image.new("RGB", (height, height), BLACK)
    dtmp = ImageDraw.Draw(mark_sq)
    draw_network_disc(mark_sq, height / 2, height / 2, height * 0.42)
    draw_borromean(mark_sq, height / 2, height / 2, height * 0.22, height * 0.05)
    img.paste(mark_sq, (int(height * 0.08), 0))

    draw = ImageDraw.Draw(img)
    title_f = font("SourceSans3-Bold.ttf", int(height * 0.22))
    sub_f = font("SourceSans3-Regular.ttf", int(height * 0.11))
    x = int(height * 1.15)
    draw.text((x, height * 0.28), "PRIME FIELD", font=title_f, fill=GOLD_HI)
    spaced = "  ".join(list("TECHNOLOGIES"))
    draw.text((x, height * 0.55), spaced, font=sub_f, fill=GOLD)
    draw_small_psi(draw, x + int(height * 1.55), int(height * 0.72), int(height * 0.14), GOLD)
    return img


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    logo = make_logo(1600)
    logo_path = OUT / "prime-field-logo.png"
    logo.save(logo_path, "PNG", optimize=True)
    logo.save(ARTIFACTS / "prime-field-logo.png", "PNG", optimize=True)

    # Also export icon-only (rings) for app/avatar use
    icon = Image.new("RGB", (1024, 1024), BLACK)
    draw_network_disc(icon, 512, 512, 430)
    draw_borromean(icon, 512, 512, 230, 52)
    icon_path = OUT / "prime-field-icon.png"
    icon.save(icon_path, "PNG", optimize=True)
    icon.save(ARTIFACTS / "prime-field-icon.png", "PNG", optimize=True)

    header = make_horizontal_lockup(420)
    header_path = OUT / "prime-field-header.png"
    header.save(header_path, "PNG", optimize=True)
    header.save(ARTIFACTS / "prime-field-header.png", "PNG", optimize=True)

    print("wrote", logo_path)
    print("wrote", icon_path)
    print("wrote", header_path)


if __name__ == "__main__":
    main()
