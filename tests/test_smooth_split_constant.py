#!/usr/bin/env python3
"""Checks for the 2 Oct 2026 smooth-split centered-constant note.

Does not claim Lemma★ or global NSE regularity.
"""

from __future__ import annotations

import pathlib
import sys
import unittest
from fractions import Fraction

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.centered_flux_q3 import flux_moments, near_shell_triad  # noqa: E402
from ns_attacks.smooth_split_constant import (  # noqa: E402
    F_X,
    am_gm_log_Lambda,
    bounds_hold,
    check_F_equals_N,
    check_F_grouping,
    check_product_rule,
    claimed_six_mode_N,
    field_to_numpy,
    flux_np,
    probe_six_mode,
    single_shell_field,
    six_mode_family,
    split_coefficient_bounds,
    spread_triad,
)


class TestProductRuleAndF(unittest.TestCase):
    def test_product_rule_on_near_shell(self) -> None:
        chk = check_product_rule(near_shell_triad(Fraction(1, 8)))
        self.assertTrue(chk["ok"], chk)
        self.assertGreater(abs(chk["lhs"]), 1.0)

    def test_F_equals_N(self) -> None:
        chk = check_F_equals_N(near_shell_triad(Fraction(1, 8)))
        self.assertTrue(chk["ok"], chk)
        self.assertEqual(chk["N"], 2.0)

    def test_F_grouping_on_six_mode(self) -> None:
        chk = check_F_grouping(six_mode_family(4))
        self.assertTrue(chk["ok"], chk)
        self.assertAlmostEqual(chk["N_minus_Nh"], -18.0, places=10)


class TestSplitBounds(unittest.TestCase):
    def test_spread_triad_bounds(self) -> None:
        b = split_coefficient_bounds(field_to_numpy(spread_triad()))
        self.assertTrue(bounds_hold(b), b)
        self.assertGreater(b["Lambda_grad_v"], 0.0)
        self.assertGreater(b["Lambda_h"], 0.0)

    def test_six_mode_bounds(self) -> None:
        b = split_coefficient_bounds(six_mode_family(5))
        self.assertTrue(bounds_hold(b), b)


class TestSixModeFamily(unittest.TestCase):
    def test_claimed_N(self) -> None:
        for j in (3, 4, 5, 6, 8):
            N = flux_np(six_mode_family(j))["N"]
            self.assertAlmostEqual(N, claimed_six_mode_N(j), places=10)

    def test_Lambda_N_quotient_falls(self) -> None:
        rows = [probe_six_mode(j, n_grid=32) for j in (3, 5, 8)]
        rhos = [abs(r["rho_Lambda_N"]) for r in rows]
        self.assertGreater(rhos[0], rhos[1])
        self.assertGreater(rhos[1], rhos[2])
        for r in rows:
            self.assertLess(r["Tc"], 0.0)
            self.assertEqual(r["R_star"], 0.0)

    def test_Ds_over_Lambda_Y_like_1_over_4j(self) -> None:
        r = probe_six_mode(8, n_grid=32)
        self.assertAlmostEqual(r["Ds_over_Lambda_Y"], 1.0 / (4 * 8), delta=0.005)


class TestDegenerateAndAlgebra(unittest.TestCase):
    def test_single_shell_is_vacuous(self) -> None:
        flux = flux_moments(single_shell_field())
        self.assertEqual(flux["Ds"], 0)
        self.assertEqual(flux["N"], 0)
        self.assertEqual(flux["Tc"], 0)

    def test_am_gm_log_Lambda(self) -> None:
        self.assertAlmostEqual(am_gm_log_Lambda(C=2.0, g=3.0, nu=0.5), 36.0)

    def test_F_X_active_and_idle(self) -> None:
        self.assertGreater(F_X(Cs=1.0, g=4.0, Lam=1.0, nu=0.1), 0.0)
        self.assertEqual(F_X(Cs=1.0, g=0.0, Lam=4.0, nu=1.0), 0.0)

    def test_honesty_lock(self) -> None:
        note = (ROOT / "docs" / "ns-review" / "SMOOTH-SPLIT-CENTERED-CONSTANT-2026-10-02.md").read_text()
        self.assertIn("NOT proved", note)
        self.assertIn("NS NOT solved", note)
        self.assertIn("OPEN", note)
        self.assertNotIn("Clay is closed", note)
        self.assertIn("instantaneous", note.lower())
        q3 = (ROOT / "docs" / "ns-review" / "CENTERED-FLUX-Q3-2026-10-01.md").read_text()
        self.assertIn("SMOOTH-SPLIT-CENTERED-CONSTANT-2026-10-02.md", q3)


if __name__ == "__main__":
    unittest.main()
