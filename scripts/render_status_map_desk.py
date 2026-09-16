#!/usr/bin/env python3
"""Print the 16 Sep 2026 status verbs onto the desk still-life folio."""

from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
STILL = ROOT / "assets" / "status-map" / "still-life-2026-09-16.png"
OUT = ROOT / "assets" / "status-map" / "desk-2026-09-16.png"
DATA = ROOT / "data" / "status_map" / "2026-09-16.json"

# Folio on the 1280x720 still-life (flood-fill of the blank page).
FOLIO = (499, 135, 925, 563)


def _font(size: int, *, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    names = (
        "/usr/share/fonts/truetype/macos/Inter-SemiBold.ttf"
        if bold
        else "/usr/share/fonts/truetype/macos/Inter-Regular.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    )
    for path in names:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def verbs_from_record() -> list[str]:
    record = json.loads(DATA.read_text(encoding="utf-8"))
    live = [item["verb"] + "." for item in record["buckets"]["live"]]
    return live + ["Record."]


def render() -> Path:
    image = Image.open(STILL).convert("RGB")
    draw = ImageDraw.Draw(image)
    title = _font(20, bold=True)
    small = _font(13)
    verb = _font(26, bold=True)
    left, top, right, bottom = FOLIO
    ink = (18, 20, 26)
    muted = (74, 67, 56)
    gold = (138, 109, 47)

    x = left + 32
    draw.text((x, top + 28), "Status map - 16 Sep 2026", font=title, fill=ink)
    draw.text((x, top + 56), "Open work. Instruments.", font=small, fill=muted)
    draw.line((x, top + 82, right - 36, top + 82), fill=(212, 181, 106), width=1)

    y = top + 100
    for line in verbs_from_record():
        draw.text((x, y), line, font=verb, fill=ink)
        y += 34

    draw.text((x, bottom - 52), "Prime Field Technologies LLC", font=small, fill=gold)
    draw.text((x, bottom - 34), "Savannah / for the record", font=small, fill=gold)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUT, "PNG")
    return OUT


if __name__ == "__main__":
    path = render()
    print(path)
