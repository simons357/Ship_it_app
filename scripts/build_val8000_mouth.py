#!/usr/bin/env python3
"""Original VAL8000 mouth art: metal teeth occupy the INNER CONCENTRIC CAMERA RINGS.

Idle and smile stay thin lines BELOW the lens (those are not teeth).
The teeth PNG paints a concentric metallic aperture grille INTO the
existing red circular lens. No chin. No cartoon jaw under the square.
PIL / numpy only. No film stills. No HAL 9000 wordmark. Gold-free.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "docs" / "cosmic-graffiti" / "assets"
MARK = ASSETS / "val8000-eye-mark.png"
LINE = ASSETS / "val8000-mouth-line.png"
SMILE = ASSETS / "val8000-mouth-smile.png"
TEETH = ASSETS / "val8000-mouth-teeth.png"
SHEET = ASSETS / "val8000-mouth-sheet.png"

# Geometry of the existing original lens (1024 square).
LENS_CX = 510.8
LENS_CY = 461.5
PUPIL_R = 24.0
GLOW_R = 42.0
INNER_R0 = 48.0
INNER_R1 = 154.0
HOUSING_R = 232.0

# Aperture rails = the existing inner concentric camera rings.
# Each tuple is (r_inner, r_outer, n_teeth). Metal lives on these bands.
RING_TEETH = (
    (50.0, 72.0, 14),    # innermost row, facing the pupil
    (78.0, 96.0, 18),    # first camera ring
    (108.0, 128.0, 22),  # second camera ring
    (138.0, 154.0, 26),  # inner lip of the housing, still inside the lens
)
RAILS = (50.0, 72.0, 78.0, 96.0, 108.0, 128.0, 138.0, 154.0)

STEEL_HI = np.array([220.0, 224.0, 230.0], dtype=np.float32)
STEEL_MID = np.array([156.0, 160.0, 166.0], dtype=np.float32)
STEEL_LO = np.array([64.0, 66.0, 70.0], dtype=np.float32)
GUM = np.array([12.0, 8.0, 9.0], dtype=np.float32)
RED_BOUNCE = np.array([28.0, 3.0, 5.0], dtype=np.float32)


def _polar(h: int, w: int) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx = xx - np.float32(LENS_CX)
    dy = yy - np.float32(LENS_CY)
    rho = np.hypot(dx, dy)
    theta = np.arctan2(dy, dx)
    return dx, dy, rho, theta


def _smoothstep(edge0: float, edge1: float, x: np.ndarray) -> np.ndarray:
    t = np.clip((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _ring_teeth(rho: np.ndarray, theta: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Metal coverage, bevel, and tip highlight, confined to concentric rings."""
    metal = np.zeros(rho.shape, dtype=np.float32)
    bevel = np.zeros(rho.shape, dtype=np.float32)
    tip = np.zeros(rho.shape, dtype=np.float32)
    for r0, r1, n in RING_TEETH:
        band = _smoothstep(r0 - 1.2, r0 + 0.8, rho) * (
            1.0 - _smoothstep(r1 - 0.8, r1 + 1.2, rho)
        )
        sector = (2.0 * np.pi) / n
        ph = np.mod(theta + 0.5 * sector, sector) / sector
        t_rad = np.clip((rho - r0) / (r1 - r0), 0.0, 1.0)
        # Point inward: narrower at the inner edge, like a tooth facing the pupil.
        half = 0.16 + 0.22 * t_rad
        dist = np.abs(ph - 0.5)
        edge = _smoothstep(half - 0.04, half, dist)
        tooth = np.clip(1.0 - edge, 0.0, 1.0) * (dist < half).astype(np.float32)
        across = np.clip((ph - (0.5 - half)) / (2.0 * half + 1e-6), 0.0, 1.0)
        metal = np.maximum(metal, band * tooth)
        bevel = np.maximum(bevel, band * tooth * (0.50 + 0.50 * np.cos(across * np.pi)))
        tip = np.maximum(
            tip,
            band * tooth * np.exp(-0.5 * ((t_rad - 0.12) / 0.16) ** 2),
        )
    return metal, bevel, tip


def _teeth_overlay(h: int, w: int) -> tuple[np.ndarray, np.ndarray]:
    """Return RGB overlay and alpha in the inner-ring annulus."""
    dx, dy, rho, theta = _polar(h, w)
    ann = _smoothstep(INNER_R0 - 2.0, INNER_R0 + 1.5, rho) * (
        1.0 - _smoothstep(INNER_R1 - 2.0, INNER_R1 + 2.5, rho)
    )

    tooth_w, bevel, tip = _ring_teeth(rho, theta)

    # Lighting matches the existing housing: key from upper-left.
    light = np.clip((-0.38 * dx - 0.62 * dy) / (rho + 8.0), -0.45, 0.85)
    light = 0.55 + 0.45 * light

    # Concentric rails: the aperture lines become the metal grille.
    rail = np.zeros((h, w), dtype=np.float32)
    for R in RAILS:
        width = 1.8
        rail = np.maximum(rail, np.exp(-0.5 * ((rho - R) / width) ** 2))

    # Short radial grille bars between rings, aligned to the teeth.
    n_bars = 18
    bar_sector = (2.0 * np.pi) / n_bars
    bar_ph = np.mod(theta, bar_sector) / bar_sector
    bar = np.exp(-0.5 * ((bar_ph - 0.5) / 0.045) ** 2)
    between = np.ones(rho.shape, dtype=np.float32)
    for r0, r1, _n in RING_TEETH:
        between = between * (
            1.0
            - _smoothstep(r0 - 0.5, r0 + 0.5, rho)
            * (1.0 - _smoothstep(r1 - 0.5, r1 + 0.5, rho))
        )
    grille = bar * between * ann * 0.55

    metal_amt = np.clip(tooth_w * 0.96 + rail * 0.90 + grille, 0.0, 1.0)
    shade = np.clip(0.30 + 0.70 * light * np.maximum(bevel, 0.35) + 0.40 * tip + 0.35 * rail, 0.0, 1.0)

    rgb = GUM[None, None, :] * (1.0 - metal_amt)[..., None]
    rgb = rgb + (
        STEEL_LO[None, None, :] * (1.0 - shade)[..., None]
        + STEEL_MID[None, None, :] * (shade * (1.0 - shade) * 2.0)[..., None]
        + STEEL_HI[None, None, :] * (shade ** 2)[..., None]
    ) * metal_amt[..., None]

    bounce = np.exp(-0.5 * ((rho - 62.0) / 16.0) ** 2) * metal_amt
    rgb = rgb + RED_BOUNCE[None, None, :] * bounce[..., None]

    keep_pupil = 1.0 - _smoothstep(GLOW_R - 6.0, GLOW_R + 2.0, rho)
    # Darken the throat between rings so the metal bands read as rings.
    alpha = np.clip(
        ann
        * (1.0 - 0.94 * keep_pupil)
        * (0.42 + 0.54 * metal_amt),
        0.0,
        0.97,
    )

    rgb = np.clip(rgb, 0.0, 255.0)
    return rgb, alpha


def render_teeth(base_path: Path = MARK) -> Image.Image:
    base = Image.open(base_path).convert("RGB")
    arr = np.asarray(base).astype(np.float32)
    h, w, _ = arr.shape
    rgb, alpha = _teeth_overlay(h, w)
    out = arr * (1.0 - alpha[..., None]) + rgb * alpha[..., None]
    out = np.clip(out, 0.0, 255.0).astype(np.uint8)
    return Image.fromarray(out, "RGB")


def _font(size: int, bold: bool = False) -> ImageFont.ImageFont:
    name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    path = Path("/usr/share/fonts/truetype/dejavu") / name
    if path.is_file():
        return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def render_sheet(
    line: Image.Image,
    smile: Image.Image,
    teeth: Image.Image,
) -> Image.Image:
    panel = 520
    pad = 28
    header = 88
    caption_h = 110
    width = pad * 4 + panel * 3
    height = header + panel + caption_h + pad
    canvas = Image.new("RGB", (width, height), (18, 18, 18))
    draw = ImageDraw.Draw(canvas)
    title_f = _font(28, bold=True)
    sub_f = _font(16, bold=True)
    body_f = _font(14)
    draw.text(
        (pad, 22),
        "VAL8000 mouth states",
        font=title_f,
        fill=(232, 232, 232),
    )
    draw.text(
        (pad, 56),
        "Idle and smile sit below the lens. Metal teeth occupy the inner concentric camera rings.",
        font=body_f,
        fill=(168, 168, 168),
    )
    labels = (
        (
            "LINE",
            "Idle / masthead. Thin line BELOW the lens. Not teeth.",
        ),
        (
            "SMILE",
            "After a normal answer. Thin curl BELOW the lens. Not teeth.",
        ),
        (
            "TEETH IN THE RINGS",
            "Inner concentric camera rings.\nAperture grille. The lens IS the mouth.\nNo cartoon jaw under the square.",
        ),
    )
    faces = (line, smile, teeth)
    for i, ((label, caption), face) in enumerate(zip(labels, faces)):
        x = pad + i * (panel + pad)
        y = header
        thumb = face.resize((panel, panel), Image.Resampling.LANCZOS)
        canvas.paste(thumb, (x, y))
        draw.rectangle([x, y, x + panel - 1, y + panel - 1], outline=(60, 60, 60))
        draw.text((x, y + panel + 10), label, font=sub_f, fill=(236, 236, 236))
        draw.multiline_text(
            (x, y + panel + 32),
            caption,
            font=body_f,
            fill=(176, 176, 176),
            spacing=3,
        )
    return canvas.filter(ImageFilter.UnsharpMask(radius=0.6, percent=40, threshold=2))


def build() -> dict[str, Path]:
    teeth = render_teeth()
    teeth.save(TEETH, "PNG", optimize=True)
    line = Image.open(LINE).convert("RGB")
    smile = Image.open(SMILE).convert("RGB")
    sheet = render_sheet(line, smile, teeth)
    sheet.save(SHEET, "PNG", optimize=True)
    return {"teeth": TEETH, "sheet": SHEET}


if __name__ == "__main__":
    written = build()
    for key, path in written.items():
        print(f"{key}\t{path}\t{path.stat().st_size}")
