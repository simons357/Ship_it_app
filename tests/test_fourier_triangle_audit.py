"""20 September 2026 Fourier-triangle audit.

Exact algebra and finite regressions. Equation (17) is not proved.
NS is not solved.
"""

from __future__ import annotations

import sys
import unittest
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.fourier_triangle_audit import (  # noqa: E402
    C,
    S_pq_boxed,
    S_pq_definition,
    S_pq_equal_boxed,
    bilinear_B,
    energy_transfer,
    enstrophy_transfer,
    even_output_closed,
    even_output_weighted_sum,
    example_field,
    exact_sphere_L2,
    generated_mode_B,
    hilbert_symbol,
    i3_criterion,
    i3_regression,
    monochromatic_s,
    moments_field,
    odd_triad_field,
    polarizations,
    report,
    scalene_I_and_T,
    shear_field,
    shear_output_on_beta2,
    sixteen_ninths_gap,
    triangle_frame,
    unequal_defect,
    young_rep_split,
)


class HilbertI3Tests(unittest.TestCase):
    def test_known_two_adic_values(self):
        self.assertEqual(hilbert_symbol(2, -1, 2), -1)
        self.assertEqual(hilbert_symbol(3, -1, 2), 1)

    def test_regression_table(self):
        rows = i3_regression()
        self.assertEqual(len(rows), 4)
        self.assertTrue(all(r["matches"] for r in rows))
        self.assertEqual(rows[0]["failing"], [2, 3])
        self.assertEqual(rows[1]["failing"], [2, 5])
        self.assertEqual(rows[2]["failing"], [])
        self.assertEqual(rows[3]["failing"], [])

    def test_criterion_is_existence_only(self):
        row = i3_criterion(2, 2, -1)
        self.assertTrue(row["passes"])
        self.assertTrue(row["real_ok"])
        # The test does not return amplitudes, phases, or transfer.
        self.assertNotIn("amplitude", row)
        self.assertNotIn("T", row)

    def test_odd_alpha_cannot_be_monochromatic(self):
        self.assertFalse(monochromatic_s(5).denominator == 1)
        self.assertTrue(monochromatic_s(6).denominator == 1)
        # Even α is necessary, not sufficient: (96,96,0) is not mono
        # and the mono even case still needs the local test.
        mono_even = i3_criterion(2, 2, -1)
        self.assertTrue(mono_even["passes"])


class BoxedIdentityTests(unittest.TestCase):
    def test_S_pq_decomposition(self):
        fr = triangle_frame((3, 0, 0), (0, 2, 0))
        A1, A2, B1, B2 = 1.0, -0.5, 0.25, 0.75
        up, uq = polarizations(fr, A1, A2, B1, B2)
        Sdef = S_pq_definition(fr, up, uq)
        Sbox = S_pq_boxed(fr, A1, A2, B1, B2)
        for i in range(3):
            self.assertAlmostEqual(Sdef[i], Sbox[i], places=10)

    def test_equal_length_cancels_inplane(self):
        fr = triangle_frame((1, 1, 0), (1, -1, 0))
        self.assertAlmostEqual(fr["a"], fr["b"], places=12)
        A1, A2, B1, B2 = 0.4, -0.3, 0.2, 0.8
        up, uq = polarizations(fr, A1, A2, B1, B2)
        Sdef = S_pq_definition(fr, up, uq)
        Sbox = S_pq_equal_boxed(fr, A1, A2, B1, B2)
        for i in range(3):
            self.assertAlmostEqual(Sdef[i], Sbox[i], places=10)
        e1 = (
            Sdef[0] * fr["e1"][0] + Sdef[1] * fr["e1"][1] + Sdef[2] * fr["e1"][2]
        )
        self.assertAlmostEqual(e1, 0.0, places=10)

    def test_unequal_defect_identity(self):
        fr = triangle_frame((3, 0, 0), (0, 2, 0))
        up, uq = polarizations(fr, 1.0, 0.5, -0.25, 0.8)
        S = S_pq_definition(fr, up, uq)
        left, right = unequal_defect(fr, up, uq, S)
        self.assertAlmostEqual(left, right, places=10)

    def test_sixteen_ninths_polynomial(self):
        for n in range(0, 17):
            r = Fraction(n, 4)
            gap = sixteen_ninths_gap(r)
            self.assertGreaterEqual(gap, 0)
        # r = 8/3 is the double root of (3r−8)
        self.assertEqual(sixteen_ninths_gap(Fraction(8, 3)), 0)

    def test_even_output_sum(self):
        for a in range(1, 12):
            self.assertEqual(even_output_weighted_sum(a), even_output_closed(a))

    def test_young_rep_split(self):
        self.assertTrue(young_rep_split(Fraction(4), Fraction(9), Fraction(1)))
        self.assertTrue(young_rep_split(Fraction(52), Fraction(532), Fraction(3, 2)))


class FiniteFieldTests(unittest.TestCase):
    def test_cosine_sin_transfers(self):
        expected = {"cos": 0, "sin": 24, "msin": -24}
        for kind, T_exp in expected.items():
            field = example_field(kind)
            m = moments_field(field)
            self.assertEqual(m["E"], 6)
            self.assertEqual(m["X"], 52)
            self.assertEqual(m["Y"], 532)
            self.assertEqual(m["Z"], 5980)
            self.assertEqual(enstrophy_transfer(field), T_exp)
            self.assertEqual(energy_transfer(field), 0)

    def test_generated_mode_cosine(self):
        field = example_field("cos")
        Bk = generated_mode_B(field, (3, -2, 0))
        self.assertEqual(Bk, (C(0), C(0), C(0, 3)))
        # Instantaneous transfer at an empty receiver is zero.
        self.assertNotIn((3, -2, 0), field)

    def test_odd_field_and_Xprime(self):
        field = odd_triad_field(Fraction(1))
        m = moments_field(field)
        self.assertEqual(m["X"], 52)
        self.assertEqual(m["Y"], 532)
        self.assertEqual(enstrophy_transfer(field), 24)
        A = Fraction(24)
        big = odd_triad_field(A)
        mb = moments_field(big)
        T = enstrophy_transfer(big)
        Xprime = 2 * T - 2 * mb["Y"]
        self.assertEqual(Xprime, 50688)
        self.assertGreater(Xprime, 0)

    def test_scalene_identity_7(self):
        field = odd_triad_field(Fraction(1))
        sc = scalene_I_and_T(field, 4, 9, 13)
        self.assertEqual(sc["T_abc"], enstrophy_transfer(field))

    def test_shear_ratio(self):
        field = shear_field()
        m = moments_field(field)
        out = shear_output_on_beta2(field)
        self.assertEqual(m["E"], Fraction(3, 2))
        self.assertEqual(out["n_nonzero"], 12)
        self.assertEqual(out["norm2"], Fraction(3, 4))
        w4 = m["E"] * m["E"]
        ratio = out["norm2"] / (Fraction(1, 2) * w4)
        self.assertEqual(ratio, Fraction(2, 3))

    def test_B_is_divergence_free(self):
        field = example_field("sin")
        for k in field:
            Bk = bilinear_B(field, k)
            from ns_attacks.fourier_triangle_audit import kdot

            self.assertEqual(kdot(k, Bk), C(0))


class SphereAndLocksTests(unittest.TestCase):
    def test_exact_sphere_small(self):
        out = exact_sphere_L2(1, 2)
        self.assertTrue(out["ok"])
        self.assertLessEqual(out["L2"], out["bound"])
        self.assertEqual(out["F"], 6)
        self.assertEqual(out["L2"], 48)
        self.assertEqual(out["bound"], 108)

    def test_report_locks(self):
        r = report()
        self.assertTrue(r["i3_all_match"])
        self.assertTrue(r["generated_3i_e3"])
        self.assertTrue(r["odd_unit"]["ok"])
        self.assertTrue(r["odd_A24"]["ok"])
        self.assertTrue(r["shear"]["ok"])
        self.assertTrue(r["even_output_ok"])
        self.assertTrue(r["sixteen_ninths_ok"])
        self.assertTrue(r["scalene_7_matches_T"])
        self.assertTrue(r["locks"]["not_a_close"])
        self.assertFalse(r["locks"]["theorem_17_proved"])
        self.assertTrue(r["locks"]["i3_is_lattice"])
        self.assertTrue(r["locks"]["i3_does_not_fix_amplitudes"])
        self.assertTrue(r["locks"]["lemma_A_unaltered"])
        self.assertTrue(r["locks"]["sign_gate_unaltered"])


if __name__ == "__main__":
    unittest.main()
