#!/usr/bin/env python3
"""Brand mark: scientific mandala is the logo; Metatron cube is not."""

from __future__ import annotations

import unittest
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PORTFOLIO = ROOT / "docs" / "portfolio"


class TestBrandLogo(unittest.TestCase):
    def test_canonical_logo_is_square_jpeg_on_black(self):
        path = ROOT / "assets" / "logo.jpg"
        self.assertTrue(path.is_file(), path)
        im = Image.open(path)
        self.assertEqual(im.format, "JPEG")
        self.assertEqual(im.size[0], im.size[1])
        self.assertGreaterEqual(im.size[0], 800)
        # Corner pixels stay black — no white box around the circular art.
        rgb = im.convert("RGB")
        for xy in ((0, 0), (im.size[0] - 1, 0), (0, im.size[1] - 1)):
            self.assertLessEqual(max(rgb.getpixel(xy)), 20, xy)

    def test_portfolio_page_uses_mandala_not_metatron(self):
        html = (PORTFOLIO / "index.html").read_text(encoding="utf-8")
        lower = html.lower()
        self.assertIn('src="logo.jpg"', html)
        self.assertIn('href="favicon.png"', html)
        self.assertIn('rel="apple-touch-icon"', html)
        self.assertNotIn("metatron", lower)
        self.assertNotIn("6db85dd22_logo", lower)
        self.assertTrue((PORTFOLIO / "logo.jpg").is_file())
        self.assertTrue((PORTFOLIO / "favicon.png").is_file())
        self.assertTrue((PORTFOLIO / "apple-touch-icon.png").is_file())

    def test_repo_html_has_no_metatron_branding(self):
        hits = []
        for path in ROOT.rglob("*"):
            if ".git" in path.parts or "results" in path.parts or not path.is_file():
                continue
            if path.suffix.lower() not in {".html", ".md", ".css", ".js", ".svg", ".json"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore").lower()
            if "metatron" in text:
                hits.append(str(path.relative_to(ROOT)))
        self.assertEqual(hits, [])


if __name__ == "__main__":
    unittest.main()
