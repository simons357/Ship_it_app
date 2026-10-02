#!/usr/bin/env python3
"""Six-mode identities and smooth-split board.  Does not prove the time budget."""

from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.exact_fourier import cascade, moments, verify_identities
from ns_attacks.six_mode_family import (
    claimed_N,
    evaluate_square_j,
    fx_ingredients,
    six_mode_field,
    six_mode_moments,
    square_j_values,
)
from ns_attacks.smooth_split_board import THEOREM, STATUS, main as board_main


class TestSixModeFamily(unittest.TestCase):
    def test_N_claim_on_square_j(self):
        for j in square_j_values(36):
            row = evaluate_square_j(j)
            self.assertTrue(row.identities_ok)
            self.assertTrue(row.N_matches_claim, f"j={j} N={row.N} claimed={row.claimed_N}")
            self.assertEqual(Fraction(row.N), claimed_N(j))

    def test_field_moments_match_closed_form(self):
        for j in (4, 9, 16):
            field = six_mode_field(j)
            self.assertTrue(verify_identities(field).ok)
            mom = moments(field)
            closed = six_mode_moments(j)
            self.assertEqual(mom.E, closed["E"])
            self.assertEqual(mom.X, closed["X"])
            self.assertEqual(mom.Y, closed["Y"])
            self.assertEqual(mom.D_s, closed["D_s"])
            cas = cascade(field, mom.Lambda)
            self.assertEqual(cas.T_c, cas.T_c_from_MN)
            self.assertEqual(cas.sum_T, 0)

    def test_Ds_over_Lambda_Y_leads_like_one_over_4j(self):
        # 4j D_s/(Λ Y) → 1 from above.
        ratios = []
        for j in range(3, 37):
            rec = six_mode_moments(j)
            ratios.append(rec["Ds_over_Lambda_Y"] / rec["claimed_Ds_over_Lambda_Y_lead"])
        self.assertGreater(ratios[0], Fraction(1))
        self.assertLess(abs(ratios[-1] - 1), Fraction(1, 20))
        self.assertLess(ratios[-1], ratios[0])

    def test_Lambda_N_quotient_decreases_with_j(self):
        vals = []
        for j in square_j_values(36):
            field = six_mode_field(j)
            mom = moments(field)
            cas = cascade(field, mom.Lambda)
            vals.append((cas.N * mom.Lambda) ** 2 / (mom.Y * mom.D_s))
        for a, b in zip(vals, vals[1:]):
            self.assertGreater(a, b)

    def test_fx_ingredients_are_exact_and_unpaid(self):
        rec = fx_ingredients(9)
        self.assertEqual(rec["j"], 9)
        self.assertIn("not a paid budget", rec["note"])
        self.assertEqual(rec["g_lb_sq"], rec["X"])
        Fraction(rec["g_ub_sixth"])  # exact


class TestSmoothSplitBoard(unittest.TestCase):
    def test_cli_verifies_identities_and_keeps_budget_open(self):
        self.assertIn("Mmult", THEOREM)
        self.assertIn("time budget OPEN", STATUS)
        self.assertIn("NOT established", STATUS)
        self.assertEqual(board_main(["--max-j", "16"]), 0)


if __name__ == "__main__":
    unittest.main()
