#!/usr/bin/env python3
"""VAL8000 metal teeth occupy the inner camera rings. No cartoon jaw."""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "cosmic-graffiti" / "val8000.md"
ASSETS = ROOT / "docs" / "cosmic-graffiti" / "assets"
MOUTH_LINE = ASSETS / "val8000-mouth-line.png"
MOUTH_SMILE = ASSETS / "val8000-mouth-smile.png"
MOUTH_TEETH = ASSETS / "val8000-mouth-teeth.png"
MOUTH_SHEET = ASSETS / "val8000-mouth-sheet.png"
EYE_MARK = ASSETS / "val8000-eye-mark.png"
BUILD = ROOT / "scripts" / "build_val8000_mouth.py"

sys.path.insert(0, str(ROOT / "scripts"))
import build_val8000_mouth as mouth  # noqa: E402


def _public_post(text: str) -> str:
    match = re.search(
        r"<!-- PUBLIC-POST:BEGIN -->(.*)<!-- PUBLIC-POST:END -->",
        text,
        re.S,
    )
    if not match:
        raise AssertionError("public posting notes markers are missing")
    return match.group(1)


def _polar(shape: tuple[int, ...]) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    h, w = shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    dx = xx - np.float32(mouth.LENS_CX)
    dy = yy - np.float32(mouth.LENS_CY)
    return xx, yy, np.hypot(dx, dy)


class TestVal8000MouthArtSpec(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = DOC.read_text(encoding="utf-8")
        cls.public = _public_post(cls.text)

    def test_spec_puts_teeth_in_the_inner_rings(self) -> None:
        text = self.text
        self.assertIn("### Mouth / art", text)
        self.assertIn("thin line BELOW the lens", text)
        self.assertIn("(those are not teeth)", text)
        self.assertIn("INNER CONCENTRIC CAMERA RINGS", text)
        self.assertIn("The aperture lines become the grille.", text)
        self.assertIn("The lens IS the mouth.", text)
        self.assertIn(
            "No chin, no separate jaw, no teeth hanging off the bottom of the square.",
            text,
        )
        self.assertIn("No cartoon jaw under the square.", text)
        self.assertIn("No smile-line-plus-teeth-below.", text)
        self.assertIn("looking INTO the camera and seeing teeth in the rings", text)
        self.assertIn("val8000-mouth-sheet.png", text)
        self.assertIn("teeth in the rings", text.lower())
        self.assertIn("Gold-free.", text)
        self.assertIn("No HAL 9000 wordmark.", text)
        self.assertIn("No film stills.", text)

    def test_spec_forbids_cartoon_jaw_and_under_square_teeth(self) -> None:
        lower = self.text.lower()
        self.assertIn("no cartoon jaw under the square", lower)
        self.assertIn("no teeth hanging off the bottom of the square", lower)
        self.assertIn("hang a cartoon jaw", lower)
        self.assertIn("put teeth under the lens as a separate mouth", lower)
        self.assertIn("no smile-line-plus-teeth-below", lower)
        self.assertNotIn("jaw under the square as the mouth", lower)

    def test_public_post_says_teeth_live_in_the_rings(self) -> None:
        public = self.public
        self.assertIn("inner concentric camera rings", public.lower())
        self.assertIn("the lens is the mouth", public.lower())
        self.assertIn("not a cartoon jaw", public.lower())
        self.assertIn("val8000-mouth-sheet.png", public)
        self.assertIn("val8000-mouth-teeth.png", public)
        self.assertNotIn("HAL 9000", public)
        self.assertNotIn("HAL9000", public)

    def test_build_script_keeps_teeth_inside_the_housing(self) -> None:
        self.assertTrue(BUILD.is_file())
        src = BUILD.read_text(encoding="utf-8")
        self.assertIn("INNER CONCENTRIC", src)
        self.assertIn("No chin", src)
        self.assertNotIn("HAL 9000", src)
        self.assertNotIn("HAL9000", src)
        outer = max(r1 for _r0, r1, _n in mouth.RING_TEETH)
        self.assertLess(outer, mouth.HOUSING_R)
        self.assertGreater(mouth.INNER_R0, mouth.PUPIL_R)
        self.assertLess(mouth.INNER_R1, mouth.HOUSING_R)


class TestVal8000RingsOccupancy(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.teeth = np.asarray(Image.open(MOUTH_TEETH).convert("RGB"))
        cls.mark = np.asarray(Image.open(EYE_MARK).convert("RGB"))
        cls.line = np.asarray(Image.open(MOUTH_LINE).convert("RGB"))
        cls.smile = np.asarray(Image.open(MOUTH_SMILE).convert("RGB"))

    def test_assets_exist_and_are_original_squares(self) -> None:
        for path in (MOUTH_LINE, MOUTH_SMILE, MOUTH_TEETH, MOUTH_SHEET, EYE_MARK):
            self.assertTrue(path.is_file(), path.name)
            self.assertGreater(path.stat().st_size, 20_000, path.name)
        self.assertEqual(self.teeth.shape[0], self.teeth.shape[1])
        self.assertEqual(self.teeth.shape[1], 1024)
        sheet = Image.open(MOUTH_SHEET)
        self.assertGreaterEqual(sheet.size[0], 1200)
        self.assertGreater(sheet.size[0], sheet.size[1])

    def test_red_pupil_stays_in_the_center(self) -> None:
        _xx, _yy, rho = _polar(self.teeth.shape)
        pupil = rho < mouth.PUPIL_R
        rgb = self.teeth[pupil].astype(np.float32)
        self.assertGreater(rgb[:, 0].mean(), 140.0)
        self.assertLess(rgb[:, 1].mean(), 90.0)
        self.assertLess(rgb[:, 2].mean(), 100.0)
        self.assertGreater(rgb[:, 0].mean() - rgb[:, 1].mean(), 80.0)

    def test_metal_occupies_inner_rings_not_a_jaw(self) -> None:
        xx, yy, rho = _polar(self.teeth.shape)
        lum = self.teeth.mean(axis=2)
        chroma = self.teeth.max(axis=2) - self.teeth.min(axis=2)
        panel = (
            (xx > 80)
            & (xx < 944)
            & (yy > 80)
            & (yy < 900)
            & (self.mark.mean(axis=2) < 80)
        )
        metal = (lum > 110) & (chroma < 32) & panel
        inner = (rho > mouth.INNER_R0) & (rho < mouth.INNER_R1)
        jaw = (rho > 200) & (yy > mouth.LENS_CY + 180) & panel
        self.assertGreater(int(metal[inner].sum()), 8_000)
        self.assertEqual(int(metal[jaw].sum()), 0)
        self.assertGreater(int(metal[inner].sum()), int(metal[jaw].sum()) + 8_000)
        # Nothing new hangs off the bottom of the square (studio backdrop is the mark).
        below = yy > 940
        diff = np.abs(self.teeth.astype(np.int16) - self.mark.astype(np.int16)).sum(axis=2)
        self.assertEqual(int(diff[below].max()), 0)

    def test_teeth_change_is_in_the_lens_not_under_it(self) -> None:
        _xx, yy, rho = _polar(self.teeth.shape)
        diff = np.abs(self.teeth.astype(np.int16) - self.mark.astype(np.int16)).sum(axis=2)
        hot = diff > 50
        inner = (rho > mouth.INNER_R0) & (rho < mouth.INNER_R1)
        jaw = (rho > 200) & (yy > mouth.LENS_CY + 180)
        self.assertGreater(float(hot[inner].mean()), 0.35)
        self.assertEqual(float(hot[jaw].mean()), 0.0)
        self.assertLess(abs(float(yy[hot].mean()) - mouth.LENS_CY), 20.0)

    def test_teeth_are_not_a_smile_line_plus_teeth_below(self) -> None:
        band = np.s_[768:777, 370:651]
        # Idle line lives on that band. Teeth must not add a mouth under the lens.
        self.assertEqual(np.abs(self.teeth[band].astype(int) - self.mark[band].astype(int)).sum(), 0)
        self.assertGreater(
            np.abs(self.line[band].astype(int) - self.teeth[band].astype(int)).mean(),
            20.0,
        )
        self.assertFalse(np.array_equal(self.teeth, self.smile))
        self.assertFalse(np.array_equal(self.teeth, self.line))

    def test_gold_free_and_no_hal_wordmark_in_art_files(self) -> None:
        r = self.teeth[:, :, 0].astype(np.int16)
        g = self.teeth[:, :, 1].astype(np.int16)
        b = self.teeth[:, :, 2].astype(np.int16)
        gold = (r > 150) & (g > 110) & (b < 100) & (g > b + 30)
        self.assertEqual(int(gold.sum()), 0)
        for path in (MOUTH_TEETH, MOUTH_SHEET):
            blob = path.read_bytes()
            self.assertNotIn(b"HAL 9000", blob)
            self.assertNotIn(b"HAL9000", blob)
            self.assertNotIn(b"I'm sorry Dave", blob)


if __name__ == "__main__":
    unittest.main()
