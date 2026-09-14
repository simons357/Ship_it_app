#!/usr/bin/env python3
"""VAL8000 skins are accessories on the same square. Default is naked."""

from __future__ import annotations

import json
import re
import struct
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CG = ROOT / "docs" / "cosmic-graffiti"
DOC = CG / "val8000.md"
SKINS_DOC = CG / "val8000-skins.md"
ASSETS = CG / "assets"
SKINS_DIR = ASSETS / "skins"
CATALOG = SKINS_DIR / "skins.json"
TESSELLATION = SKINS_DIR / "tessellation"
CSS = ASSETS / "val8000-skins.css"
JS = ASSETS / "val8000-skins.js"
BASE_SVG = ASSETS / "val8000-eye.svg"
MOUTH_EYE = (
    "val8000-mouth-line.png",
    "val8000-mouth-smile.png",
    "val8000-mouth-teeth.png",
    "val8000-eye-mark.png",
    "val8000-eye-header.png",
    "val8000-eye.svg",
)
KINDS = {"glasses", "hat", "tessellation", "pin", "other"}

NAMED = ("frequency", "weekend-update", "issue1", "scientist", "music-art")
GLASSES = ("glasses-ordinary", "glasses-camera")


def _png_ihdr(path: Path) -> tuple[int, int, int]:
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise AssertionError(f"{path.name} is not a PNG")
    width, height = struct.unpack(">II", data[16:24])
    return width, height, data[25]


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
        self.assertEqual(ids["naked"]["files"], [])
        self.assertEqual(ids["naked"]["kind"], "other")
        self.assertIn("no accessory", ids["naked"]["notes"].lower())
        self.assertIn("unadorned", ids["naked"]["name"].lower())
        self.assertIn("Default skin: the naked square.", self.spec)
        self.assertIn("unadorned square", self.spec.lower())
        self.assertIn("Skins are accessories, not a new character.", self.spec)
        self.assertNotIn("overlay-", self.base_svg)
        self.assertNotIn("accessory-frequency", self.base_svg)
        self.assertIn('id="mouth-line"', self.base_svg)
        self.assertIn("<line", self.base_svg)
        for name in MOUTH_EYE:
            self.assertTrue((ASSETS / name).is_file(), name)
            self.assertFalse((SKINS_DIR / name).exists(), name)

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


class TestVal8000SkinsDrawer(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
        cls.spec = SKINS_DOC.read_text(encoding="utf-8")
        cls.by_id = {row["id"]: row for row in cls.catalog["skins"]}
        cls.js = JS.read_text(encoding="utf-8")

    def test_skins_file_exists(self) -> None:
        self.assertTrue(SKINS_DOC.is_file())
        self.assertGreater(SKINS_DOC.stat().st_size, 400)
        self.assertIn("this is the drawer", self.spec.lower())
        self.assertIn("How to add a skin", self.spec)
        self.assertEqual(self.catalog["drawer"], "docs/cosmic-graffiti/val8000-skins.md")
        self.assertEqual(self.catalog["default_skin"], "naked")

    def test_glasses_skins_listed(self) -> None:
        kinds_glasses = [
            row["id"] for row in self.catalog["skins"] if row["kind"] == "glasses"
        ]
        self.assertIn("glasses-ordinary", kinds_glasses)
        self.assertIn("glasses-camera", kinds_glasses)
        self.assertIn("weekend-update", kinds_glasses)
        for skin_id in GLASSES:
            row = self.by_id[skin_id]
            self.assertEqual(row["kind"], "glasses")
            self.assertTrue(row["files"])
            png = SKINS_DIR / row["overlay"]
            svg = SKINS_DIR / row["svg"]
            self.assertTrue(png.is_file(), png.name)
            self.assertTrue(svg.is_file(), svg.name)
            width, height, color_type = _png_ihdr(png)
            self.assertEqual((width, height), (1024, 1024), png.name)
            self.assertEqual(color_type, 6, f"{png.name} must be RGBA overlay")
            svg_text = svg.read_text(encoding="utf-8")
            self.assertIn("VAL8000", svg_text)
            self.assertNotIn("HAL", svg_text)
            self.assertNotIn("mouth-line", svg_text)
            self.assertNotIn("Google", svg_text)
            self.assertIn(skin_id, self.js)
        self.assertIn("Ordinary glasses", self.spec)
        self.assertIn("Camera-frame glasses", self.spec)
        self.assertIn("still types in the box", self.spec.lower())
        camera_notes = self.by_id["glasses-camera"]["notes"].lower()
        self.assertIn("accessory", camera_notes)
        self.assertIn("not a surveillance product", camera_notes)
        self.assertIn("not a keylogger", camera_notes)
        self.assertIn("analog", camera_notes)

    def test_tessellation_tray_exists(self) -> None:
        self.assertTrue(TESSELLATION.is_dir())
        readme = TESSELLATION / "README.md"
        self.assertTrue(readme.is_file())
        tray_text = readme.read_text(encoding="utf-8").lower()
        self.assertIn("tessellation", tray_text)
        self.assertIn("not in this repo", tray_text)
        self.assertIn("not physics", tray_text)
        self.assertIn("nav-42", tray_text)
        row = self.by_id["tessellation-tray"]
        self.assertEqual(row["kind"], "tessellation")
        self.assertEqual(row["files"], [])
        self.assertIsNone(row["overlay"])
        self.assertEqual(list(TESSELLATION.glob("*.png")), [])
        self.assertIn("tessellation-tray", self.js)

    def test_catalog_rows_have_kind_and_files(self) -> None:
        for row in self.catalog["skins"]:
            self.assertIn(row["kind"], KINDS, row["id"])
            self.assertIn("name", row)
            self.assertIn("files", row)
            self.assertIn("notes", row)
            self.assertIsInstance(row["files"], list)
        self.assertIn("No TTS this round", self.spec)
        lower = self.spec.lower()
        self.assertIn("no tts", lower)
        self.assertIn("not a product photo", lower)
        self.assertIn("not physics", lower)
        self.assertIn("fluid-q", lower)
        self.assertIn("q os", lower)
        self.assertNotIn("HAL 9000", self.spec)
        self.assertNotIn("Clay", self.spec)

    def test_worn_previews_do_not_replace_face_files(self) -> None:
        for name in (
            "worn-glasses-ordinary.png",
            "worn-glasses-camera.png",
            "worn-monocle.png",
        ):
            path = SKINS_DIR / name
            self.assertTrue(path.is_file(), name)
            width, height, _color = _png_ihdr(path)
            self.assertEqual((width, height), (1024, 1024), name)
        line = ASSETS / "val8000-mouth-line.png"
        worn = SKINS_DIR / "worn-glasses-ordinary.png"
        self.assertNotEqual(line.read_bytes(), worn.read_bytes())
        self.assertNotEqual(line.read_bytes(), (SKINS_DIR / "worn-monocle.png").read_bytes())

    def test_monocle_listed_default_still_naked_idle_unchanged(self) -> None:
        ids = [row["id"] for row in self.catalog["skins"]]
        self.assertIn("monocle", ids)
        row = self.by_id["monocle"]
        self.assertEqual(row["kind"], "glasses")
        self.assertEqual(row["overlay"], "monocle.png")
        self.assertEqual(row["svg"], "monocle.svg")
        png = SKINS_DIR / "monocle.png"
        svg = SKINS_DIR / "monocle.svg"
        self.assertTrue(png.is_file(), png.name)
        self.assertTrue(svg.is_file(), svg.name)
        width, height, color_type = _png_ihdr(png)
        self.assertEqual((width, height), (1024, 1024), png.name)
        self.assertEqual(color_type, 6, f"{png.name} must be RGBA overlay")
        svg_text = svg.read_text(encoding="utf-8")
        self.assertIn("VAL8000", svg_text)
        self.assertNotIn("HAL", svg_text)
        self.assertNotIn("mouth-line", svg_text)
        self.assertNotIn("Google", svg_text)
        self.assertIn("monocle", self.js)
        notes = row["notes"].lower()
        self.assertIn("swap skin", notes)
        self.assertIn("not automatic on insult", notes)
        self.assertIn("tongue", notes)
        self.assertIn("go deeper", notes)
        self.assertEqual(self.catalog["default"], "naked")
        self.assertEqual(self.catalog["default_skin"], "naked")
        self.assertIsNone(self.by_id["naked"]["overlay"])
        self.assertEqual(self.catalog["idle_mouth"], "straight line under every skin")
        self.assertIn("Idle mouth stays a straight line under every skin.", self.spec)
        self.assertIn("not automatic on insult (insult is tongue)", self.spec)
        self.assertIn("`monocle`", self.spec)
        self.assertNotIn("HAL 9000", self.spec)
        self.assertNotIn("Clay", self.spec)


if __name__ == "__main__":
    unittest.main()
