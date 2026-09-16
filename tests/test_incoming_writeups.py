"""Incoming ChatGPT paste is filed; C10 dead is not leftover 5 closed."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph  # noqa: E402

PAGE = ROOT / "docs" / "INCOMING-WRITEUPS.md"
PASTE = ROOT / "docs" / "incoming" / "GLOBAL-REGULARITY-PROGRAM-2026-09-16.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
AUDIT = ROOT / "docs" / "REPORT-AUDIT.md"
C10 = ROOT / "docs" / "C10-CHAIN.md"
TINY = ROOT / "docs" / "TINY.txt"


class IncomingWriteupsTests(unittest.TestCase):
    def test_cannot_login_and_c10_word_is_locked(self):
        text = PAGE.read_text()
        self.assertIn("cannot log into", text.lower())
        self.assertIn("ChatGPT", text)
        self.assertIn("Claude", text)
        self.assertIn("Grok", text)
        self.assertIn("Leftover 5 stays OPEN", text)
        self.assertIn("C10 is not a theorem", text)
        self.assertIn("GLOBAL-REGULARITY-PROGRAM-2026-09-16.md", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("almost proved", text.lower())

    def test_paste_is_incoming_not_tape(self):
        paste = PASTE.read_text()
        self.assertIn("Incoming paste", paste)
        self.assertIn("Not the tape", paste)
        self.assertIn("C10", paste)
        self.assertIn("NO as a program death", paste)
        self.assertTrue(PASTE.is_file())
        tape = TAPE.read_text()
        self.assertIn("C10 died", tape)
        self.assertIn("INCOMING-WRITEUPS.md", TINY.read_text())
        self.assertIn("INCOMING-WRITEUPS.md", AUDIT.read_text())
        self.assertIn("Named candidate", C10.read_text())

    def test_filter(self):
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
