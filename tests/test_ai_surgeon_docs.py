#!/usr/bin/env python3
"""The AI-Surgeon bible is on disk, transcribed, and not invented."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "ai_surgeon" / "docs"
BIBLE = DOCS / "bible"


class TestBiblePresent(unittest.TestCase):
    def test_canonical_pdf_and_citations_txt(self):
        pdf = BIBLE / "AI-Surgeon-Final-Final.pdf"
        txt = BIBLE / "AI-Surgeon-Final-With-Citations.txt"
        self.assertTrue(pdf.is_file(), pdf)
        self.assertGreater(pdf.stat().st_size, 10_000)
        self.assertTrue(txt.is_file(), txt)
        body = txt.read_text(encoding="utf-8", errors="replace")
        self.assertIn("AI SURGEON", body)
        self.assertIn("11. References & Citations", body)

    def test_pages_and_bigbiz_and_claude(self):
        for name in (
            "AI-Surgeon-Final-Final.pages",
            "AI-Surgeon-Final-Final.pages.extracted.txt",
            "AI-Surgeon-Final-Final.extracted.txt",
            "AI-Surgeon-VR-Business-Plan.pages",
            "AI-Surgeon-VR-Business-Plan.extracted.txt",
            "claude_ai.pdf",
            "claude_ai.extracted.txt",
        ):
            path = BIBLE / name
            self.assertTrue(path.is_file(), path)
            self.assertGreater(path.stat().st_size, 500, name)

    def test_source_lock_and_citations_index(self):
        self.assertTrue((DOCS / "CITATIONS.md").is_file())
        self.assertTrue((DOCS / "SOURCE-LOCK.md").is_file())
        lock = (DOCS / "SOURCE-LOCK.md").read_text(encoding="utf-8")
        self.assertIn("Not a medical-device claim", lock)
        self.assertIn("phone → tablet + mat → VR", lock)
        self.assertIn("except metaverse", lock)
        self.assertIn("two seats", lock.lower())
        self.assertTrue((DOCS / "VOICE-LOCK.md").is_file())
        self.assertTrue((DOCS / "THEIRS-medical-big-picture.md").is_file())
        self.assertTrue((DOCS / "HARRISONS-arthurian-lady-of-the-lake.md").is_file())
        self.assertTrue((DOCS / "WARRIOR-SURGEON.md").is_file())
        self.assertTrue((DOCS / "THE-PEN.md").is_file())
        pen = (DOCS / "THE-PEN.md").read_text(encoding="utf-8")
        self.assertIn("twist", pen.lower())
        self.assertIn("squeeze", pen.lower())
        lock = (DOCS / "WARRIOR-SURGEON.md").read_text(encoding="utf-8")
        self.assertIn("Playable UI follows the HTML prototypes", lock)
        self.assertIn("The repo HTML won", lock)


class TestCitationsAreTranscribedNotInvented(unittest.TestCase):
    NAMED = (
        "Market Research Future (2024)",
        "HolonIQ (2024)",
        "Stanford University Study (2023)",
        "Harvard Medical School (2023)",
        "Newzoo",
        "U.S. Department of Education (2024)",
        "Bloomberg Technology (2024)",
    )

    def test_seven_named_sources_from_cited_plan(self):
        cites = (DOCS / "CITATIONS.md").read_text(encoding="utf-8")
        for name in self.NAMED:
            self.assertIn(name, cites)
        self.assertIn("does not invent", cites.lower())
        self.assertIn("Jonathan Simons, CRNA", cites)
        # Do not invent a paper the plans never named.
        self.assertNotRegex(cites, r"doi\.org", "do not mint DOIs")
        self.assertNotIn("arXiv:", cites)

    def test_cited_txt_contains_the_same_seven(self):
        body = (BIBLE / "AI-Surgeon-Final-With-Citations.txt").read_text(
            encoding="utf-8", errors="replace"
        )
        self.assertIn("Market Research Future (2024)", body)
        self.assertIn("HolonIQ (2024)", body)
        self.assertIn("Stanford University Study (2023)", body)
        self.assertIn("Harvard Medical School (2023)", body)
        self.assertIn("Newzoo Global Esports Market Report (2024)", body)
        self.assertIn("U.S. Department of Education (2024)", body)
        self.assertIn("Bloomberg Technology (2024)", body)

    def test_claude_constraint_is_no_metaverse(self):
        claude = (BIBLE / "claude_ai.extracted.txt").read_text(
            encoding="utf-8", errors="replace"
        ).lower()
        self.assertIn("except metaverse", claude)
        self.assertIn("ability to generate a pdf", claude)


if __name__ == "__main__":
    unittest.main()
