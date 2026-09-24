"""Fourier-triangle reconstruction audit. Identities, not a close."""

from __future__ import annotations

import math
import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.fourier_triangle_geom import (  # noqa: E402
    even_output_sum,
    sixteen_ninths_gap,
    triangle_invariants,
)
from ns_attacks.i3_primes import (  # noqa: E402
    REGRESSIONS,
    criterion_12,
    hilbert,
    monochromatic_necessary,
    report as i3_report,
)
from ns_attacks.triangle_examples import (  # noqa: E402
    identity_1_check,
    identity_3_check,
    missing_theorem,
    odd_field_report,
    phase_twin_report,
    polynomial_checks,
    report,
    shear_report,
)


class GeometryTests(unittest.TestCase):
    def test_invariants_match_definitions(self):
        inv = triangle_invariants((2, 0, 0), (0, 3, 0))
        self.assertEqual(inv["k"], (2, 3, 0))
        self.assertEqual(inv["a"], 4)
        self.assertEqual(inv["b"], 9)
        self.assertEqual(inv["c"], 13)
        self.assertEqual(inv["s"], 0)
        self.assertEqual(inv["s_from_c"], 0)
        self.assertEqual(inv["Delta"], 36)
        self.assertEqual(inv["cross_sq"], 36)
        self.assertTrue(inv["triangle_ineq"])

    def test_identity_1_and_4(self):
        geom = identity_1_check()
        self.assertTrue(geom["S_identity"])
        self.assertTrue(geom["defect_identity"])
        self.assertTrue(geom["div_free"])
        self.assertTrue(geom["slot_identities"])

    def test_identity_3_equal_length(self):
        eq = identity_3_check()
        self.assertLess(eq["equal_formula_err"], 1e-10)
        self.assertLess(eq["in_plane_component"], 1e-10)
        self.assertLess(eq["in_plane_inputs_kill_normal"], 1e-10)


class PhaseTwinTests(unittest.TestCase):
    def test_quadratic_moments_and_signed_T(self):
        twins = phase_twin_report()
        self.assertTrue(twins["quadratic_lock"])
        self.assertTrue(twins["sign_lock"])
        self.assertTrue(twins["energy_sum_zero"])
        for row, expected in zip(twins["rows"], (0.0, 24.0, -24.0)):
            self.assertAlmostEqual(row["T"], expected, places=9)
            self.assertAlmostEqual(row["E"], 6.0)
            self.assertAlmostEqual(row["X"], 52.0)
            self.assertAlmostEqual(row["Y"], 532.0)

    def test_generated_mode_is_3i_e3(self):
        twins = phase_twin_report()
        self.assertTrue(twins["generated_mode"]["matches_3i_e3"])


class ShearAndOddTests(unittest.TestCase):
    def test_shear_ratio(self):
        sh = shear_report()
        self.assertTrue(sh["locks"]["E_3_over_2"])
        self.assertTrue(sh["locks"]["output_3_over_4"])
        self.assertTrue(sh["locks"]["twelve_outputs"])
        self.assertTrue(sh["locks"]["ratio_2_over_3"])

    def test_odd_field_X_dot(self):
        odd = odd_field_report()
        self.assertAlmostEqual(odd["X"], 52.0 * 24.0 ** 2)
        self.assertAlmostEqual(odd["Y"], 532.0 * 24.0 ** 2)
        self.assertAlmostEqual(odd["T"], 24.0 * 24.0 ** 3)
        self.assertAlmostEqual(odd["X_dot"], 50688.0)
        self.assertTrue(odd["positive_X_dot"])


class PolynomialTests(unittest.TestCase):
    def test_even_output_closed_form(self):
        for a in (1, 2, 3, 5, 8, 13, 21):
            got = even_output_sum(a)
            self.assertLess(got["err"], 1e-10)
            # exact rational
            acc = Fraction(0)
            for b in range(2, 4 * a + 1, 2):
                acc += Fraction((b - a) ** 2) * (1 - Fraction(b, 4 * a))
            self.assertEqual(acc, Fraction(a ** 3) - Fraction(a ** 2, 2))

    def test_sixteen_ninths_identity(self):
        poly = polynomial_checks()
        self.assertTrue(poly["sixteen_ninths_rational_exact"])
        self.assertTrue(poly["sixteen_ninths_float"])
        self.assertLess(abs(sixteen_ninths_gap(2.0)), 1e-15)


class I3PrimeTests(unittest.TestCase):
    def test_regressions(self):
        for spec in REGRESSIONS:
            got = criterion_12(spec["a"], spec["b"], spec["s"])
            self.assertEqual(got["passes"], spec["expect_pass"], spec)
            if spec["expect_fail"]:
                self.assertEqual(set(got["failed_primes"]), set(spec["expect_fail"]), spec)

    def test_odd_alpha_impossible(self):
        for alpha in (1, 3, 5, 7, 9, 11):
            row = monochromatic_necessary(alpha)
            self.assertTrue(row["odd_impossible"])
            self.assertFalse(row["even_passes_12"])

    def test_even_alpha_necessary_not_sufficient(self):
        # alpha=2: s=-1, (2,2,-1) is a locked PASS.
        self.assertTrue(monochromatic_necessary(2)["even_passes_12"])
        # alpha=6: s=-3, Delta=36-9=27. Local test may fail; even is not enough.
        six = monochromatic_necessary(6)
        self.assertTrue(six["even_necessary_not_sufficient"])

    def test_hilbert_multiplicativity_sign(self):
        # (a,bc)_p = (a,b)_p (a,c)_p
        for ell in (2, 3, 5, 7):
            self.assertEqual(
                hilbert(6, 35, ell),
                hilbert(6, 5, ell) * hilbert(6, 7, ell),
            )

    def test_report_matches(self):
        self.assertTrue(i3_report()["all_match"])


class RemainingTheoremTests(unittest.TestCase):
    def test_17_stays_open(self):
        miss = missing_theorem()
        self.assertEqual(miss["status"], "OPEN")
        self.assertTrue(miss["not_proved_here"])
        self.assertTrue(miss["does_not_follow_from_I3_primes"])

    def test_full_report_locks(self):
        rep = report()
        self.assertTrue(all(rep["locks"].values()), rep["locks"])
        self.assertFalse(rep["board"]["NS_solved"])


if __name__ == "__main__":
    unittest.main()
