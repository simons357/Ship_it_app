#!/usr/bin/env python3
"""VAL8000 skins are accessories on the same square. Default is naked."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CG = ROOT / "docs" / "cosmic-graffiti"
DOC = CG / "val8000.md"
SKINS_DOC = CG / "val8000-skins.md"
ASSETS = CG / "assets"
SKINS_DIR = ASSETS / "skins"
CATALOG = SKINS_DIR / "skins.json"
CSS = ASSETS / "val8000-skins.css"
JS = ASSETS / "val8000-skins.js"
BASE_SVG = ASSETS / "val8000-eye.svg"

NAMED = ("frequency", "weekend-update", "issue1", "scientist", "music-art")


def _public_post(text: str) -> str:
    match = re.search(
        r"<!-- PUBLIC-POST:BEGIN -->(.*)<!-- PUBLIC-POST:END -->",
        text,
        re.S,
    )
    if not match:
        raise AssertionError("public posting notes markers are missing")
    return match.group(1)


class TestVal8000Skins(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        cls.spec = SKINS_DOC.read_text(encoding="utf-8")
        cls.persona = DOC.read_text(encoding="utf-8")
        cls.css = CSS.read_text(encoding="utf-8")
        cls.js = JS.read_text(encoding="utf-8")
        cls.base_svg = BASE_SVG.read_text(encoding="utf-8")

    def test_default_skin_is_naked_with_no_accessory(self) -> None:
        self.assertEqual(self.catalog["default"], "naked")
        ids = {s["id"]: s for s in self.catalog["skins"]}
        self.assertIsNone(ids["naked"]["overlay"])
        self.assertIn("Default skin: the naked square.", self.spec)
        self.assertIn("Skins are accessories, not a new character.", self.spec)
        self.assertNotIn("overlay-", self.base_svg)
        self.assertNotIn("accessory-frequency", self.base_svg)
        self.assertIn('id="mouth-line"', self.base_svg)
        self.assertIn("<line", self.base_svg)

    def test_named_skins_exist_as_svg_and_png_layers(self) -> None:
        ids = [s["id"] for s in self.catalog["skins"]]
        self.assertEqual(ids[0], "naked")
        for name in NAMED:
            self.assertIn(name, ids)
            png = SKINS_DIR / f"overlay-{name}.png"
            svg = SKINS_DIR / f"overlay-{name}.svg"
            self.assertTrue(png.is_file(), png.name)
            self.assertTrue(svg.is_file(), svg.name)
            self.assertGreater(png.stat().st_size, 400)
            svg_text = svg.read_text(encoding="utf-8")
            self.assertIn("VAL8000", svg_text)
            self.assertNotIn("HAL", svg_text)
            self.assertNotIn("mouth-line", svg_text)
            self.assertNotIn("Google", svg_text)

    def test_idle_line_unchanged_under_skins(self) -> None:
        self.assertIn("Idle mouth stays a straight line under every skin.", self.spec)
        self.assertEqual(self.catalog["idle_mouth"], "straight line under every skin")
        self.assertIn("Idle mouth: a straight line.", self.persona)
        self.assertIn('id="mouth-line"', self.base_svg)
        js = self.js
        self.assertNotIn("val8000-mouth-smile", js)
        self.assertNotIn("val8000-mouth-teeth", js)

    def test_how_to_change_is_data_skin_clip_on(self) -> None:
        self.assertIn("How to change: set `data-skin`.", self.spec)
        self.assertIn("data-skin", self.css)
        self.assertIn("VAL8000_applySkin", self.js)
        self.assertIn('DEFAULT_SKIN = "naked"', self.js)
        self.assertIn("No TTS", self.spec)
        self.assertTrue(self.catalog["types_in_the_box"])
        self.assertTrue(self.catalog["no_tts"])

    def test_public_name_stays_val8000(self) -> None:
        public = _public_post(self.persona)
        blob = "\n".join([self.spec, json.dumps(self.catalog), public])
        self.assertIn("VAL8000", blob)
        self.assertNotIn("HAL 9000", blob)
        self.assertNotIn("HAL9000", blob)
        self.assertNotIn("I'm sorry Dave", public)
        self.assertIn("VAL8000 is an AI commentator", public)


if __name__ == "__main__":
    unittest.main()
