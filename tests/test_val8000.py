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

MOUTH_LINE = ASSETS / "val8000-mouth-line.png"
MOUTH_SMILE = ASSETS / "val8000-mouth-smile.png"
MOUTH_TEETH = ASSETS / "val8000-mouth-teeth.png"


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
        self.assertIn('id="mouth-line"', svg_text)
        self.assertIn("<line", svg_text)
        self.assertIn("Not a smile", svg_text)
        self.assertNotIn("<path", svg_text)

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

    def test_spray_can_fear_face_rewrite_stays_out(self) -> None:
        lower = self.text.lower()
        self.assertNotIn("red lens is out", lower)
        self.assertNotIn("not a terminator, not a skull", lower)
        self.assertNotIn("spray-can", lower)


class TestVal8000Mouth(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = DOC.read_text(encoding="utf-8")
        cls.public = _public_post(cls.text)

    def test_three_mouth_marks_exist(self) -> None:
        for path in (MOUTH_LINE, MOUTH_SMILE, MOUTH_TEETH):
            self.assertTrue(path.is_file(), path.name)
            self.assertGreater(path.stat().st_size, 20_000, path.name)

    def test_idle_line_is_not_the_smile_asset(self) -> None:
        self.assertNotEqual(
            MOUTH_LINE.read_bytes(),
            MOUTH_SMILE.read_bytes(),
            "idle line and after-answer smile must be different marks",
        )
        self.assertNotEqual(MOUTH_LINE.read_bytes(), MOUTH_TEETH.read_bytes())

    def test_guide_locks_idle_line_and_smile_after_answer(self) -> None:
        text = self.text
        self.assertIn("val8000-mouth-line.png", text)
        self.assertIn("val8000-mouth-smile.png", text)
        self.assertIn("val8000-mouth-teeth.png", text)
        self.assertIn("Idle mouth: a straight line.", text)
        self.assertIn("Idle is not a smile.", text)
        self.assertIn("After he answers, he usually smiles.", text)
        self.assertIn("The smile is the default post-answer face.", text)
        self.assertIn("Masthead is idle: a straight line.", text)
        self.assertIn("Masthead does not use a smile while idle.", text)
        self.assertIn("Metal teeth are rare.", text)
        self.assertIn("Teeth are not after ordinary answers.", text)
        self.assertIn("Teeth are never idle.", text)
        self.assertIn("Teeth stay off the masthead.", text)
        self.assertNotIn("Smile when the joke earns it.", text)
        self.assertNotIn("Masthead uses the line, or a slight smile.", text)
        self.assertNotIn("slight smile", text.lower())

    def test_public_post_idle_line_smile_after_answer_not_hal(self) -> None:
        public = self.public
        self.assertIn("val8000-mouth-line.png", public)
        self.assertIn("val8000-mouth-smile.png", public)
        self.assertNotIn("val8000-mouth-teeth.png", public)
        self.assertIn("Idle / masthead", public)
        self.assertIn("After he answers", public)
        self.assertIn("straight line while idle", public)
        self.assertIn("Not the teeth", public)
        self.assertNotIn("slight smile", public.lower())
        self.assertNotIn("HAL 9000", public)
        self.assertNotIn("HAL9000", public)
        self.assertNotIn("I'm sorry Dave", public)
        self.assertIn("VAL8000", public)


if __name__ == "__main__":
    unittest.main()
