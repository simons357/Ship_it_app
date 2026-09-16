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
LATEST = ROOT / "docs" / "LATEST.md"


class IncomingWriteupsTests(unittest.TestCase):
    def test_cannot_login_and_c10_word_is_locked(self):
        text = PAGE.read_text()
        self.assertIn("cannot log into", text.lower())
        self.assertIn("ChatGPT", text)
        self.assertIn("Claude", text)
        self.assertIn("Grok", text)
        self.assertIn("Leftover 5 stays OPEN", text)
        self.assertIn("C10 is not a theorem", text)
        self.assertIn("NS-SND-FINAL-STATUS-REPORT.md", text)
        report = ROOT / "docs" / "incoming" / "NS-SND-FINAL-STATUS-REPORT.md"
        self.assertTrue(report.is_file())
        report_text = report.read_text()
        self.assertIn("Download this file", report_text)
        self.assertIn("Not the tape itself", report_text)
        self.assertIn("NS not solved", report_text)
        self.assertIn("NS-SND-FINAL-STATUS-REPORT.md", TINY.read_text())
        self.assertIn("NS-SND-FINAL-STATUS-REPORT.md", LATEST.read_text())
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("almost proved", text.lower())

    def test_endgame_notes_are_incoming_not_tape(self):
        page = PAGE.read_text()
        self.assertIn("NOTES-ON-THE-ENDGAME.md", page)
        self.assertIn("Q-stack out", page)
        self.assertIn("Do not mail a panel", page)
        self.assertIn("Uniform triadic", page)
        endgame = ROOT / "docs" / "incoming" / "NOTES-ON-THE-ENDGAME.md"
        self.assertTrue(endgame.is_file())
        text = endgame.read_text()
        self.assertIn("Incoming paste", text)
        self.assertIn("Not the tape", text)
        self.assertIn("Q-stack out", text)
        self.assertIn("Ring is REPAIR", text)
        self.assertIn("KILLED", text)
        self.assertIn("Do not mail a panel", text)
        self.assertIn("Nobody asked", text)
        self.assertIn("Φ-renormalization", text)
        self.assertIn("QStack", text)
        self.assertIn("Borromean", text)
        self.assertIn("uniform triadic", text.lower())
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("almost proved", text.lower())
        tape = TAPE.read_text()
        self.assertIn("Endgame notes as the tape", tape)
        self.assertIn("NOTES-ON-THE-ENDGAME.md", AUDIT.read_text())
        self.assertIn("NOTES-ON-THE-ENDGAME.md", TINY.read_text())
        self.assertIn("NOTES-ON-THE-ENDGAME.md", LATEST.read_text())

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
