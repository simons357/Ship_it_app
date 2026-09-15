"""SND-H review: displayed Theorem H fails even with X<=M; F_j bound sits."""

from __future__ import annotations

import unittest
from decimal import Decimal
from fractions import Fraction
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from snd_h_review import (  # noqa: E402
    PACKET_N,
    PACKET_Q,
    PACKET_TABLE,
    displayed_ratio,
    packet_row,
    shell_weights,
    viscous_tail,
)

PAGE = ROOT / "docs" / "SND-H-REVIEW.md"
PLAIN = ROOT / "docs" / "SND-H-PLAIN.md"
PLAN = ROOT / "docs" / "UNAUGMENTED-R4-VORTICITY-PLAN.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
TINY = ROOT / "docs" / "TINY.txt"
LATEST = ROOT / "docs" / "LATEST.md"
ISSUES = ROOT / "docs" / "ISSUES-SHEET.md"
IMPL = ROOT / "docs" / "SND-TO-REGULARITY.md"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "")


class SndHReviewArithmeticTests(unittest.TestCase):
    def test_shell_weights_match_packet(self):
        a, b, x, j = shell_weights(PACKET_Q, PACKET_N)
        self.assertEqual(a, Fraction(1, 11))
        self.assertEqual(b, Fraction(1, 22))
        self.assertEqual(x, Fraction(1))
        self.assertEqual(j, Fraction(1, 11))
        self.assertEqual(j / x, Fraction(1, 11))

    def test_packet_table_ratios(self):
        for k, expected in PACKET_TABLE.items():
            got = packet_row(k)
            # Packet printed eight significant digits after the leading group.
            rel = abs(got - expected) / expected
            self.assertLess(rel, Decimal("5e-9"), msg=f"K={k} got={got} expected={expected}")

    def test_ratio_grows_with_k(self):
        r24 = packet_row(24)
        r28 = packet_row(28)
        r32 = packet_row(32)
        self.assertGreater(r28, r24)
        self.assertGreater(r32, r28)
        self.assertGreater(r32, Decimal("1e8"))

    def test_viscous_tail_is_the_whole_flux_on_shears(self):
        a, b, x, j = shell_weights(PACKET_Q, PACKET_N)
        s = viscous_tail(Fraction(1), b, PACKET_N, 24)
        self.assertGreater(s, 0)
        # Denominator of the displayed bound stays order-one in the low block.
        r = displayed_ratio(Fraction(1), PACKET_Q, PACKET_N, 24)
        self.assertGreater(r, Decimal("1e6"))


class SndHReviewPageTests(unittest.TestCase):
    def test_page_names_the_quantity_change(self):
        text = _plain(PAGE)
        for needle in (
            "F_j",
            "S_j",
            "drops S_j",
            "absolute-value",
            "viscous tail",
            "Two names for two quantities",
        ):
            self.assertIn(needle, text)

    def test_page_names_the_shear_kill_even_with_m(self):
        text = _plain(PAGE)
        for needle in (
            "not established even with",
            "Xle M",
            "u_K",
            "(u_K·∇)u_K=0",
            "3.57924234",
            "5.72307770",
            "9.15690113",
            "Proved under",
            "must be replaced",
        ):
            self.assertIn(needle, text)

    def test_page_names_valid_f_j_bound_and_limits(self):
        text = _plain(PAGE)
        for needle in (
            "M-dependent bound for F_j only",
            "do not supply a new",
            "Remove M from this same estimate",
            "A^3",
            "No universal SND floor",
            "rho(0)=1/L",
        ):
            self.assertIn(needle, text)

    def test_page_names_embeddings_and_errata(self):
        text = _plain(PAGE)
        for needle in (
            "Invalid embeddings",
            "H^1 controls L^6, not L^infty",
            "subcritical",
            "X>= c_* J is not equivalent",
            "definition/claim mismatch",
            "First equation to write",
            "(1/2)",
        ):
            self.assertIn(needle, text)
        self.assertIn("Do not write", PAGE.read_text())
        self.assertIn("definition/claim mismatch", text)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)
        self.assertNotIn("almost proved", text.lower())

    def test_replacement_wording_sits(self):
        text = PAGE.read_text()
        self.assertIn("Replacement wording", text)
        self.assertIn("not established even with", text)
        self.assertIn("drops a viscous tail", text)
        self.assertIn("rebuild the required", text)
        self.assertIn("Not leftover 1", text)
        self.assertIn("Catalog B open stays 1", text)

    def test_pointers(self):
        for path in (PLAIN, PLAN, TAPE, TINY, LATEST, ISSUES, IMPL):
            self.assertIn("SND-H-REVIEW.md", path.read_text(), msg=str(path))
        tape = _plain(TAPE)
        self.assertIn("Theorem H is not established even with X<=M", tape)
        self.assertIn("definition/claim mismatch", tape)
        issues = ISSUES.read_text().lower()
        self.assertIn("not a thirteenth leftover", issues)
        plan = _plain(PLAN)
        self.assertIn("object under review", plan)
        self.assertIn("Displayed absolute-flux estimate FAILS", plan)


if __name__ == "__main__":
    unittest.main()
