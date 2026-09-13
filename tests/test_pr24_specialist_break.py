"""Specialist break Q&A: answers sit; 16/9 stays claimed; NS not solved."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "PR24-SPECIALIST-BREAK.md"
BOUND = ROOT / "docs" / "ATTACK-9D-FULL-SUPPORT-BOUND.md"
KILL = ROOT / "docs" / "LEMMA-STAR-GROWING-LAYER.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"


class Pr24SpecialistBreakTests(unittest.TestCase):
    def test_page_answers_the_break_list(self):
        text = PAGE.read_text()
        for needle in (
            "T_c(v_n)",
            "every n",  # plaintext, not only \(n\)
            "Instantaneous admissible class",
            "Not Ring",
            "overline",
            "no such factor",
            "no extra",
            "exactly",
            "Both polarizations",
            "2/3",
            "K>1",
            "does not repair",
            "different theorem",
            "Reads only",
            "human-checkable",
            "None sits",
            "Not BKM",
        ):
            self.assertIn(needle, text.replace("\\", ""))
        self.assertIn("CLAIMED", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertNotIn("hygiene", text.lower())

    def test_bound_page_carries_5_to_10_and_14(self):
        bound = BOUND.read_text()
        self.assertIn("Specialist break lines", bound)
        self.assertIn("Not Ring", bound)
        self.assertIn("overline", bound.replace("\\", ""))
        self.assertIn("Nothing divides", bound)
        self.assertIn("half the symmetrization", bound)
        self.assertIn("exactly", bound)
        self.assertIn("Both transverse", bound)
        self.assertIn("does not repair", bound)
        self.assertIn("different theorem", bound)
        self.assertIn("PR24-SPECIALIST-BREAK.md", bound)

    def test_kill_page_carries_1_to_4(self):
        kill = KILL.read_text()
        self.assertIn("Specialist break lines", kill)
        self.assertIn("n=1", kill)
        self.assertIn("for every", kill)
        self.assertIn("Instantaneous admissible", kill)
        self.assertIn("not a trajectory", kill.lower())
        tape = TAPE.read_text()
        self.assertIn("PR24-SPECIALIST-BREAK.md", tape)
        self.assertIn("does not repair", tape)


if __name__ == "__main__":
    unittest.main()
