#!/usr/bin/env python3
"""VAL8000 is CG's rap commentator: original red-eye mark, public name VAL8000."""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "cosmic-graffiti" / "val8000.md"
ASSETS = ROOT / "docs" / "cosmic-graffiti" / "assets"
LIVE_PY = ROOT / "domain_architect"


def _public_post(text: str) -> str:
    match = re.search(
        r"<!-- PUBLIC-POST:BEGIN -->(.*)<!-- PUBLIC-POST:END -->",
        text,
        re.S,
    )
    if not match:
        raise AssertionError("public posting notes markers are missing")
    return match.group(1)


class TestVal8000Persona(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = DOC.read_text(encoding="utf-8")

    def test_guide_and_original_marks_exist(self) -> None:
        self.assertTrue(DOC.is_file())
        mark = ASSETS / "val8000-eye-mark.png"
        header = ASSETS / "val8000-eye-header.png"
        svg = ASSETS / "val8000-eye.svg"
        self.assertGreater(mark.stat().st_size, 20_000)
        self.assertGreater(header.stat().st_size, 20_000)
        svg_text = svg.read_text(encoding="utf-8")
        self.assertIn("VAL8000", svg_text)
        self.assertNotIn("HAL", svg_text)
        self.assertIn("#c1121f", svg_text)

    def test_house_brief_keeps_the_eye_and_the_rename(self) -> None:
        self.assertIn("the red camera eye of HAL", self.text)
        self.assertIn("VAL8000", self.text)
        self.assertIn("so we do not get sued", self.text)
        self.assertIn("original marks", self.text.lower())
        self.assertIn("not a person", self.text.lower())
        self.assertIn("does not fly the ship", self.text.lower())

    def test_public_post_does_not_use_the_other_name(self) -> None:
        public = _public_post(self.text)
        self.assertIn("VAL8000 is an AI commentator", public)
        self.assertNotIn("HAL 9000", public)
        self.assertNotIn("HAL9000", public)
        self.assertNotIn("I'm sorry Dave", public)
        self.assertNotIn("pod bay", public.lower())

    def test_he_comments_after_the_news_and_does_not_fake_closes(self) -> None:
        lower = self.text.lower()
        self.assertIn("the frequency", lower)
        self.assertIn("raps the comment", lower)
        self.assertNotIn("ns solved", lower)
        self.assertNotIn("rh proved", lower)
        self.assertNotIn("riemann hypothesis is proved", lower)
        self.assertIn("navier–stokes regularity stays open", lower)

    def test_live_da_python_does_not_import_val8000(self) -> None:
        for path in LIVE_PY.rglob("*.py"):
            blob = path.read_text(encoding="utf-8")
            self.assertNotIn("VAL8000", blob)
            self.assertNotIn("val8000", blob)
            self.assertNotIn("HAL 9000", blob)


if __name__ == "__main__":
    unittest.main()
