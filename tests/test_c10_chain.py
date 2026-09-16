"""C10 is a named candidate, not a theorem. Exact-shell 9D stays CLAIMED."""

from __future__ import annotations

import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from c10_chain import (  # noqa: E402
    amplitude_powers,
    energy_linear_ratio_grows,
    shear_alpha_is_zero,
    tjj_e_false_powers,
)

PAGE = ROOT / "docs" / "C10-CHAIN.md"
NINE = ROOT / "docs" / "ATTACK-9D-FULL-SUPPORT-BOUND.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
TINY = ROOT / "docs" / "TINY.txt"
LATEST = ROOT / "docs" / "LATEST.md"
ISSUES = ROOT / "docs" / "ISSUES-SHEET.md"
SHELL = ROOT / "docs" / "AXISYM-SHELL.md"
NINE_SETUP = ROOT / "docs" / "ATTACK-9D-SETUP.md"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "")


class C10ArithmeticTests(unittest.TestCase):
    def test_energy_linear_ratio_grows_like_sqrt_lambda(self):
        self.assertEqual(tjj_e_false_powers(4)["T_over_D_sq"], 4)
        self.assertEqual(tjj_e_false_powers(16)["T_over_D_sq"], 16)
        self.assertTrue(energy_linear_ratio_grows(4, 16))

    def test_amplitude_a_plus_matches_cubic_energy_does_not(self):
        p = amplitude_powers(5)
        self.assertEqual(p["T"], p["a_plus_Z"])
        self.assertLess(p["energy_R"], p["T"])

    def test_shear_vanishes(self):
        self.assertTrue(shear_alpha_is_zero())


class C10PageTests(unittest.TestCase):
    def test_page_does_not_close(self):
        text = _plain(PAGE)
        raw = PAGE.read_text()
        self.assertIn("Named candidate", raw)
        self.assertIn("Not seated", raw)
        self.assertIn("Do not work on Theorem H", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())

    def test_chain_marks(self):
        text = _plain(PAGE)
        for needle in (
            "a_+",
            "NEW CLAIM",
            "EXACT",
            "STANDARD LEMMA",
            "Brutal question",
            "TJJ-template",
            "Do not merge",
            "BKM-from-spectral-decay as primary",
            "exact-shell 9D",
        ):
            self.assertIn(needle, text)

    def test_freeze_and_pointers(self):
        nine = NINE.read_text()
        self.assertIn("Freeze", nine)
        self.assertIn("No more sweeps", nine)
        self.assertIn("independent reproduction", nine.lower())
        for path in (TAPE, TINY, LATEST, ISSUES, SHELL, NINE_SETUP):
            self.assertIn("C10-CHAIN.md", path.read_text(), msg=str(path))
        tape = _plain(TAPE)
        self.assertIn("C10 is not a theorem", tape)
        self.assertIn("CLAIMED", nine)


if __name__ == "__main__":
    unittest.main()
