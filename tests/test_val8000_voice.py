#!/usr/bin/env python3
"""VAL8000 is a comment voice, not a person, prophet, or closed theorem."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CG = ROOT / "docs" / "cosmic-graffiti"
GUIDE = CG / "val8000.md"
SAMPLES = CG / "val8000-samples.md"
POSTING = CG / "val8000-posting.md"
TRAY = CG / "issues" / "_trays" / "val8000-verses.md"
MARK = CG / "assets" / "val8000-mark.png"
PORTRAIT = CG / "assets" / "val8000-portrait.png"
ALT = CG / "assets" / "ALT-TEXT.md"

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


class TestVal8000VoiceGuide(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.guide = _read(GUIDE)
        cls.samples = _read(SAMPLES)
        cls.posting = _read(POSTING)
        cls.tray = _read(TRAY)
        cls.blob = "\n".join(
            [cls.guide, cls.samples, cls.posting, cls.tray, _read(ALT)]
        )
        cls.lower = cls.blob.lower()

    def test_files_exist(self) -> None:
        for path in (GUIDE, SAMPLES, POSTING, TRAY, MARK, PORTRAIT, ALT):
            self.assertTrue(path.is_file(), path)

    def test_pictures_are_png(self) -> None:
        for path in (MARK, PORTRAIT):
            self.assertTrue(path.read_bytes().startswith(PNG_MAGIC), path)

    def test_not_a_person_or_prophet(self) -> None:
        text = self.guide.lower()
        self.assertIn("not a person", text)
        self.assertIn("not a prophet", text)
        self.assertIn("not agi", text)
        self.assertIn("tool with a personality", text)

    def test_frequency_reports_first(self) -> None:
        text = self.guide.lower()
        self.assertIn("frequency reports first", text)
        self.assertIn("raps the comment", text)
        self.assertIn("drawer-3", text)

    def test_cannot_fake_a_theorem(self) -> None:
        text = self.guide.lower()
        self.assertIn("cannot fake a theorem", text)
        self.assertIn("we solved the swirl", text)
        self.assertIn("no riemann hypothesis proved", text)
        self.assertIn("primes are black holes", text)
        self.assertIn("rap can punch hype", text)

    def test_masthead_and_credit(self) -> None:
        self.assertIn("VAL8000 · AI rap commentator", self.guide)
        self.assertIn("AI rap commentator", self.posting)
        self.assertIn("nobody is tricked", self.posting.lower())

    def test_does_not_claim_ns_or_rh_closed(self) -> None:
        samples = self.samples.lower()
        self.assertNotIn("we solved the swirl", samples)
        self.assertNotIn("rh is proved", samples)
        self.assertNotIn("riemann hypothesis is proved", samples)
        self.assertNotIn("navier–stokes is solved", samples)
        self.assertNotIn("navier-stokes is solved", samples)
        self.assertIn("not certified", samples)
        self.assertIn("stays open", samples)
        self.assertIn("nobody in that paper claims 2", samples)
        self.assertIn("what we do not claim", samples)

    def test_no_prize_or_fear_face(self) -> None:
        samples = self.samples.lower()
        self.assertNotIn("millennium", samples)
        self.assertNotIn("clay mathematics", samples)
        self.assertNotIn("i will replace you", samples)
        guide = self.guide.lower()
        self.assertIn("glowing red eyes", guide)
        self.assertIn("red lens on a black tile", guide)
        self.assertIn("fear-face", guide)

    def test_no_archived_product_names_in_the_rap_files(self) -> None:
        rap = "\n".join([self.samples, self.tray]).lower()
        for name in ("nav-42", "fluid-q", "chat vault", "2.2 hz"):
            self.assertNotIn(name, rap)

    def test_samples_are_labeled_draft(self) -> None:
        head = self.samples.splitlines()[0:8]
        joined = "\n".join(head).lower()
        self.assertIn("draft", joined)
        self.assertIn("not a shipped tracklist", self.samples.lower())

    def test_empty_trays_are_empty(self) -> None:
        self.assertIn("**Status:** empty on purpose", self.tray)
        self.assertGreaterEqual(self.tray.count("```\n(empty)\n```"), 5)

    def test_alt_text_names_the_friendly_face(self) -> None:
        alt = _read(ALT).lower()
        self.assertIn("spray-paint can", alt)
        self.assertIn("tool with a personality", alt)
        self.assertNotIn("terminator", alt.split("not a terminator")[0])


if __name__ == "__main__":
    unittest.main()
