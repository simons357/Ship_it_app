"""Repaired F_j bound sits; A.3 is a Dini ceiling, not a floor."""

from __future__ import annotations

import unittest
from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from snd_h_repair import (  # noqa: E402
    a2_scales,
    equal_shell_rho,
    rho_dot_exact_mode,
)
from snd_h_review import PACKET_N, PACKET_Q, PACKET_TABLE  # noqa: E402

PAGE = ROOT / "docs" / "SND-H-REPAIR.md"
REVIEW = ROOT / "docs" / "SND-H-REVIEW.md"
PLAIN = ROOT / "docs" / "SND-H-PLAIN.md"
PLAN = ROOT / "docs" / "UNAUGMENTED-R4-VORTICITY-PLAN.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
TINY = ROOT / "docs" / "TINY.txt"
LATEST = ROOT / "docs" / "LATEST.md"
ISSUES = ROOT / "docs" / "ISSUES-SHEET.md"
IMPL = ROOT / "docs" / "SND-TO-REGULARITY.md"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "")


class SndHRepairArithmeticTests(unittest.TestCase):
    def test_shear_a3_equals_exact_rho_dot_when_f_is_zero(self):
        for k in PACKET_TABLE:
            left, right = rho_dot_exact_mode(Fraction(1), PACKET_Q, PACKET_N, k)
            self.assertEqual(left, right, msg=f"K={k}")
            # High tail makes Ẋ more negative, so ρ̇ more positive.
            # Not a 0=0 identity: dissipation and quotient both sit.
            self.assertNotEqual(left, 0)

    def test_high_k_makes_rho_rise_faster_on_shears(self):
        r24, _ = rho_dot_exact_mode(Fraction(1), PACKET_Q, PACKET_N, 24)
        r32, _ = rho_dot_exact_mode(Fraction(1), PACKET_Q, PACKET_N, 32)
        self.assertGreater(r32, r24)
        self.assertGreater(r24, 0)

    def test_amplitude_quadratic_vs_cubic(self):
        quad, cubic = a2_scales(Fraction(3))
        self.assertEqual(quad, 9)
        self.assertEqual(cubic, 27)

    def test_equal_shell_floor_obstruction(self):
        self.assertEqual(equal_shell_rho(11), Fraction(1, 11))
        self.assertEqual(equal_shell_rho(1), 1)
        self.assertLess(equal_shell_rho(100), Fraction(1, 10))


class SndHRepairPageTests(unittest.TestCase):
    def test_page_does_not_restore_theorem_h(self):
        text = _plain(PAGE)
        self.assertIn("Theorem H stays withdrawn", text)
        self.assertIn("Does not: a floor", text)
        self.assertIn("not a floor", text.lower())
        self.assertIn("definition/claim mismatch", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())

    def test_page_names_a2_and_dini_direction(self):
        text = _plain(PAGE)
        raw = PAGE.read_text()
        for needle in (
            "Sitting bound on (F_j)",
            "upper bound on (D^+rho)",
            "comparison ceiling",
            "Last term, without Bony",
            "global enstrophy identity",
            "Propagation unwritten",
            "cancel stays dropped",
            "Ring stays **REPAIR**",
        ):
            self.assertIn(needle, text)
        self.assertIn("not 0≤0", raw)

    def test_erratum_sits_alongside_audit(self):
        text = PAGE.read_text()
        self.assertIn("Cover-sheet erratum", text)
        self.assertIn("alongside that audit", text)
        self.assertIn("SND-H-REVIEW.md", text)
        self.assertIn("Not leftover 1", text)
        self.assertIn("Catalog B open stays 1", text)

    def test_pointers(self):
        for path in (REVIEW, PLAIN, PLAN, TAPE, TINY, LATEST, ISSUES, IMPL):
            self.assertIn("SND-H-REPAIR.md", path.read_text(), msg=str(path))
        tape = _plain(TAPE)
        self.assertIn("A.2 sits", tape)
        self.assertIn("A.3 is a ceiling", tape)
        plan = _plain(PLAN)
        self.assertIn("object under review", plan)


if __name__ == "__main__":
    unittest.main()
