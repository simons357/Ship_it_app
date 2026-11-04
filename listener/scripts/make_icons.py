#!/usr/bin/env python3
"""Write LISTENER PNG icons without third-party deps."""
from __future__ import annotations

import struct
import zlib
from pathlib import Path

OUT = Path(__file__).resolve().parents[1]


def png(w: int, h: int, rgba) -> bytes:
    raw = bytearray()
    for y in range(h):
        raw.append(0)
        raw.extend(rgba[y * w * 4 : (y + 1) * w * 4])

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(bytes(raw), 9)) + chunk(b"IEND", b"")


def field_icon(size: int) -> bytes:
    px = bytearray(size * size * 4)
    cx = cy = size / 2
    for y in range(size):
        for x in range(size):
            dx = (x - cx) / size
            dy = (y - cy) / size
            d = (dx * dx + dy * dy) ** 0.5
            g = int(8 + 22 * (1 - min(1, d * 1.6)))
            r = int(2 + 10 * (1 - min(1, d)))
            b = int(4 + 8 * (1 - min(1, d)))
            glow = max(0, 1 - abs(d - 0.08) * 18)
            r = min(255, r + int(125 * glow))
            g = min(255, g + int(255 * glow))
            b = min(255, b + int(165 * glow))
            i = (y * size + x) * 4
            px[i : i + 4] = bytes((r, g, b, 255))
    return png(size, size, px)


def main() -> None:
    web = OUT / "app" / "icons"
    web.mkdir(parents=True, exist_ok=True)
    ios = OUT / "ios" / "Listener" / "Assets.xcassets" / "AppIcon.appiconset"
    ios.mkdir(parents=True, exist_ok=True)
    (web / "icon-192.png").write_bytes(field_icon(192))
    (web / "icon-512.png").write_bytes(field_icon(512))
    (web / "icon-180.png").write_bytes(field_icon(180))
    (ios / "AppIcon.png").write_bytes(field_icon(1024))


if __name__ == "__main__":
    main()
