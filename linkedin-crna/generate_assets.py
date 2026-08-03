#!/usr/bin/env python3
"""Generate LinkedIn brand visuals for Jonathan Simons, CRNA."""

from __future__ import annotations

import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"
FONTS = ASSETS / "fonts"
OUT = ASSETS
ARTIFACTS = Path("/opt/cursor/artifacts")

# Brand tokens
INK = (10, 22, 40)
SLATE = (28, 46, 69)
TEAL = (31, 122, 120)
TEAL_LIGHT = (74, 168, 164)
MIST = (215, 230, 229)
FOG = (238, 244, 243)
STEEL = (143, 163, 181)
WHITE = (255, 255, 255)
WHITE_SOFT = (236, 244, 243)


def font(name: str, size: int) -> ImageFont.FreeTypeFont:
    path = FONTS / name
    return ImageFont.truetype(str(path), size=size)


def lerp(a: tuple[int, int, int], b: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def vertical_gradient(size: tuple[int, int], top: tuple[int, int, int], bottom: tuple[int, int, int]) -> Image.Image:
    w, h = size
    img = Image.new("RGB", size)
    px = img.load()
    for y in range(h):
        c = lerp(top, bottom, y / max(h - 1, 1))
        for x in range(w):
            px[x, y] = c
    return img


def radial_wash(img: Image.Image, center: tuple[float, float], radius: float, color: tuple[int, int, int], alpha: int) -> Image.Image:
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    cx, cy = center
    # Approximate soft radial with concentric ellipses
    for i in range(20, 0, -1):
        r = radius * (i / 20)
        a = int(alpha * (1 - i / 20) ** 2)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(*color, a))
    base = img.convert("RGBA")
    return Image.alpha_composite(base, overlay).convert("RGB")


def draw_waveform(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: tuple[int, int, int], width: int = 3) -> None:
    x0, y0, x1, y1 = box
    w = x1 - x0
    h = y1 - y0
    mid = y0 + h / 2
    points = []
    for i in range(w + 1):
        t = i / max(w, 1)
        # Clinical waveform: quiet baseline → complex segment → settle
        if 0.18 < t < 0.42:
            amp = h * 0.38
            y = mid - amp * math.sin((t - 0.18) * math.pi * 6) * math.exp(-((t - 0.3) ** 2) / 0.01)
            # QRS-like spike
            if 0.28 < t < 0.31:
                y = mid - h * 0.48
            elif 0.31 <= t < 0.33:
                y = mid + h * 0.22
        elif 0.55 < t < 0.78:
            amp = h * 0.18
            y = mid - amp * math.sin((t - 0.55) * math.pi * 4)
        else:
            y = mid + math.sin(t * 40) * 1.2
        points.append((x0 + i, y))
    draw.line(points, fill=color, width=width, joint="curve")


def draw_airway_arc(draw: ImageDraw.ImageDraw, cx: int, cy: int, scale: float, color: tuple[int, int, int, int]) -> None:
    # Abstract airway path — elegant curve, not a cartoon organ
    pts = []
    for i in range(60):
        t = i / 59
        x = cx + scale * (t * 2.2 - 0.4)
        y = cy + scale * (0.15 * math.sin(t * math.pi) - 0.55 * t + 0.2 * math.sin(t * math.pi * 2))
        pts.append((x, y))
    draw.line(pts, fill=color, width=max(2, int(scale * 0.08)), joint="curve")


def fit_text(draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.ImageFont, max_width: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    cur = ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font_obj) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def make_banner() -> Path:
    w, h = 1584, 396
    img = vertical_gradient((w, h), INK, SLATE)
    img = radial_wash(img, (1180, 180), 520, TEAL, 70)
    img = radial_wash(img, (200, 320), 380, TEAL_LIGHT, 28)

    # Soft grid / depth lines
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    for i in range(0, w, 48):
        od.line((i, 0, i, h), fill=(255, 255, 255, 8), width=1)
    for j in range(0, h, 48):
        od.line((0, j, w, j), fill=(255, 255, 255, 6), width=1)

    # Left accent bar
    od.rectangle((0, 0, 10, h), fill=(*TEAL, 230))

    # Abstract airway motif on right
    draw_airway_arc(od, 1180, 210, 160, (*TEAL_LIGHT, 160))
    draw_airway_arc(od, 1210, 230, 120, (*MIST, 90))

    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)

    # Waveform band
    draw_waveform(d, (72, 280, 720, 350), TEAL_LIGHT, width=3)
    d.line((72, 315, 720, 315), fill=(255, 255, 255, ), width=1)

    name_f = font("LibreBaskerville-Bold.ttf", 54)
    sub_f = font("SourceSans3-Semibold.ttf", 26)
    meta_f = font("SourceSans3-Regular.ttf", 20)

    d.text((72, 78), "Jonathan Simons, CRNA", font=name_f, fill=WHITE)
    d.text((72, 150), "Anesthesia  ·  Airway Innovation  ·  Medical Devices", font=sub_f, fill=MIST)
    d.text((72, 198), "Simons Medical Innovations  ·  Savannah, GA", font=meta_f, fill=STEEL)

    # Right label block
    d.rounded_rectangle((1120, 86, 1510, 170), radius=8, fill=SLATE, outline=TEAL, width=2)
    label_f = font("SourceSans3-Bold.ttf", 22)
    small_f = font("SourceSans3-Regular.ttf", 18)
    d.text((1148, 104), "CLINICAL → PRODUCT", font=label_f, fill=TEAL_LIGHT)
    d.text((1148, 134), "Papers · Patents · Devices", font=small_f, fill=MIST)

    out = OUT / "linkedin-banner.png"
    img.save(out, "PNG", optimize=True)
    return out


def make_square_post(
    filename: str,
    eyebrow: str,
    title: str,
    subtitle: str,
    footer: str = "Jonathan Simons, CRNA",
) -> Path:
    size = 1080
    img = vertical_gradient((size, size), INK, (16, 34, 56))
    img = radial_wash(img, (820, 240), 420, TEAL, 60)
    img = radial_wash(img, (200, 900), 380, TEAL_LIGHT, 25)

    overlay = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.rectangle((0, 0, 14, size), fill=(*TEAL, 235))
    od.rectangle((0, size - 110, size, size), fill=(8, 16, 28, 180))
    draw_airway_arc(od, 860, 780, 180, (*TEAL_LIGHT, 100))
    img = Image.alpha_composite(img.convert("RGBA"), overlay).convert("RGB")
    d = ImageDraw.Draw(img)

    draw_waveform(d, (80, 860, 700, 960), TEAL, width=3)

    eye_f = font("SourceSans3-Bold.ttf", 28)
    title_f = font("LibreBaskerville-Bold.ttf", 58)
    sub_f = font("SourceSans3-Regular.ttf", 30)
    foot_f = font("SourceSans3-Semibold.ttf", 24)

    d.text((80, 88), eyebrow.upper(), font=eye_f, fill=TEAL_LIGHT)

    y = 160
    for line in fit_text(d, title, title_f, 900):
        d.text((80, y), line, font=title_f, fill=WHITE)
        y += 72

    y += 18
    for line in fit_text(d, subtitle, sub_f, 860):
        d.text((80, y), line, font=sub_f, fill=MIST)
        y += 42

    d.text((80, 1000), footer, font=foot_f, fill=STEEL)

    out = OUT / filename
    img.save(out, "PNG", optimize=True)
    return out


def make_profile_preview() -> Path:
    """Wide preview card showing how the profile reads together."""
    w, h = 1600, 900
    img = Image.new("RGB", (w, h), FOG)
    d = ImageDraw.Draw(img)

    # Fake LinkedIn chrome
    d.rounded_rectangle((60, 50, 1540, 850), radius=18, fill=WHITE)
    banner = Image.open(OUT / "linkedin-banner.png").resize((1480, 370), Image.Resampling.LANCZOS)
    img.paste(banner, (60, 50))

    # Avatar circle
    avatar = Image.new("RGBA", (180, 180), (0, 0, 0, 0))
    ad = ImageDraw.Draw(avatar)
    ad.ellipse((0, 0, 179, 179), fill=SLATE, outline=WHITE, width=8)
    ad.ellipse((20, 20, 159, 159), fill=TEAL)
    initials_f = font("LibreBaskerville-Bold.ttf", 48)
    ad.text((48, 58), "JS", font=initials_f, fill=WHITE)
    img.paste(avatar, (100, 340), avatar)

    name_f = font("LibreBaskerville-Bold.ttf", 40)
    head_f = font("SourceSans3-Regular.ttf", 24)
    meta_f = font("SourceSans3-Semibold.ttf", 20)

    d.text((110, 540), "Jonathan Simons, CRNA", font=name_f, fill=INK)
    headline = "CRNA · Airway & Anesthesia Device Inventor · Founder, Simons Medical Innovations"
    y = 600
    for line in fit_text(d, headline, head_f, 900):
        d.text((110, y), line, font=head_f, fill=SLATE)
        y += 34
    d.text((110, y + 10), "Savannah, Georgia  ·  Simons Medical Innovations", font=meta_f, fill=TEAL)

    # Right column about excerpt
    d.rounded_rectangle((1050, 430, 1480, 800), radius=12, fill=FOG)
    about_title = font("SourceSans3-Bold.ttf", 22)
    about_body = font("SourceSans3-Regular.ttf", 20)
    d.text((1080, 460), "ABOUT (excerpt)", font=about_title, fill=TEAL)
    excerpt = "I practice anesthesia with one obsession: make the airway safer, cleaner, and simpler."
    y = 510
    for line in fit_text(d, excerpt, about_body, 360):
        d.text((1080, y), line, font=about_body, fill=INK)
        y += 30
    d.text((1080, y + 24), "Posts: anesthesia · papers · products", font=about_body, fill=STEEL)

    out = OUT / "profile-preview.png"
    img.save(out, "PNG", optimize=True)
    return out


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    ARTIFACTS.mkdir(parents=True, exist_ok=True)

    banner = make_banner()
    posts = [
        make_square_post(
            "post-airway-first.png",
            "Pinned post",
            "I invent from the airway.",
            "25+ years as a CRNA. Patents, papers, and products that start in the OR.",
        ),
        make_square_post(
            "post-clinical-note.png",
            "Clinical note",
            "Speed and sterility are a design problem.",
            "Treat the laryngoscope like a sterile instrument—even when the room is moving fast.",
        ),
        make_square_post(
            "post-patent.png",
            "Patent spotlight",
            "Disposable blade cover for the laryngoscope.",
            "US 2010/0191061 A1 — cleaner intubation without slowing the clinician.",
        ),
        make_square_post(
            "post-product-wip.png",
            "Product WIP",
            "If it adds cognitive load, it isn’t ready.",
            "Design rule at Simons Medical Innovations for difficult-airway tools.",
        ),
        make_square_post(
            "post-carousel-cover.png",
            "Carousel",
            "5 airway setup checks before induction.",
            "Suction · oxygen plan · blade light · backup · contamination control.",
        ),
    ]
    preview = make_profile_preview()

    # Soft copies into artifacts for walkthrough
    for path in [banner, preview, *posts]:
        target = ARTIFACTS / path.name
        Image.open(path).save(target, "PNG", optimize=True)
        print(f"wrote {path} -> {target}")


if __name__ == "__main__":
    main()
