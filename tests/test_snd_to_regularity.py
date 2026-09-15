"""SND-to-regularity implication: shell cut, missing drift, circularity named."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "SND-TO-REGULARITY.md"
PLAIN = ROOT / "docs" / "SND-H-PLAIN.md"
PLAN = ROOT / "docs" / "UNAUGMENTED-R4-VORTICITY-PLAN.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
TINY = ROOT / "docs" / "TINY.txt"
LATEST = ROOT / "docs" / "LATEST.md"
ISSUES = ROOT / "docs" / "ISSUES-SHEET.md"
BONY = ROOT / "docs" / "TRACK-B-BONY-T.md"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "")


class SndToRegularityTests(unittest.TestCase):
    def test_page_names_what_the_shell_condition_controls(self):
        text = _plain(PAGE)
        for needle in (
            "shell condition",
            "3-CONC",
            "SPREAD",
            "occupation",
            "EQ3",
            "diagonal",
            "low paraproduct",
            "T2 Lemma 1",
            "SND-C",
            "Pi_{j_*}",
        ):
            self.assertIn(needle, text)
        self.assertIn("does not", text.lower())
        self.assertIn("|omega|_infty", text.replace(" ", ""))
        self.assertIn("not a bound on X", text)
        self.assertIn("strain-axis", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("almost proved", text.lower())

    def test_page_names_frequency_drift_still_needed(self):
        text = _plain(PAGE)
        for needle in (
            "frequency drift",
            "dj*/dt",
            "from the field",
            "Prescribed climb is not NS",
            "c=8",
            "Frozen support",
            "Occupation time is a clock",
            "Leakage",
        ):
            self.assertIn(needle, text)
        self.assertIn("B12e", text)
        self.assertIn("B11d", text)
        self.assertIn("B10b", text)
        self.assertIn("B8b", text)
        self.assertIn("B7c", text)

    def test_page_names_circularity(self):
        text = _plain(PAGE)
        for needle in (
            "Theorem E",
            "does not start the a priori",
            "Theorem F",
            "4^{N-1}",
            "Theorem G",
            "G is dead",
            "Ring",
            "REPAIR",
            "Prescribed c=8",
            "Frozen-support ceiling",
        ):
            self.assertIn(needle, text)
        self.assertIn("circular", text.lower())

    def test_page_does_not_close_ns_or_retitle_leftovers(self):
        text = PAGE.read_text()
        self.assertIn("SND sitting is not a bound on", text.replace("\\", ""))
        self.assertIn("Not leftover 1", text)
        self.assertIn("Do not weld", text)
        self.assertIn("Catalog B open stays 1", text)
        self.assertIn("Do not merge PR 48", text)
        self.assertIn("NS not solved", text)
        self.assertNotIn("the implication sits", text.lower())
        self.assertNotIn("regularity sits", text.lower())

    def test_omega_infty_is_named_as_uncontrolled(self):
        text = _plain(PAGE)
        self.assertIn("|omega|_infty", text.replace(" ", ""))
        self.assertIn("What the cut does not control", text)

    def test_tape_and_pointers_name_the_page(self):
        for path in (PLAIN, PLAN, TAPE, TINY, LATEST, ISSUES, BONY):
            self.assertTrue(path.exists(), msg=str(path))
        self.assertIn("SND-TO-REGULARITY.md", PLAIN.read_text())
        self.assertIn("SND-TO-REGULARITY.md", PLAN.read_text())
        self.assertIn("SND-TO-REGULARITY.md", TAPE.read_text())
        self.assertIn("SND-TO-REGULARITY.md", TINY.read_text())
        self.assertIn("SND-TO-REGULARITY.md", LATEST.read_text())
        self.assertIn("SND-TO-REGULARITY.md", ISSUES.read_text())
        issues = ISSUES.read_text()
        self.assertIn("not a thirteenth leftover", issues.lower())
        self.assertIn("Catalog B open count is 1", issues)
        tape = _plain(TAPE)
        self.assertIn("G is dead", tape)
        self.assertIn("SND sitting is not a bound on X", tape)
        self.assertIn("Theorem E", tape)
        self.assertIn("Theorem F", tape)


if __name__ == "__main__":
    unittest.main()
