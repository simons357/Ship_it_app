"""First-variation gate. Lemma A unaltered. NS is not solved."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.first_variation_gate import (  # noqa: E402
    BOTH_SIGNS,
    NO_NEIGHBOR,
    ONE_SIGN,
    ZERO_ONLY,
    L1_N,
    R2_N,
    classify_signs,
    finite_gap_split,
    first_variation_check,
    seed_A_plus,
    synthetic_family,
)


class FiniteGapTests(unittest.TestCase):
    def test_exact_split_uses_live_T(self):
        row = finite_gap_split([4.0, 9.0, 16.0], [1.0, -0.25, -0.75], 9.0)
        self.assertAlmostEqual(row["T_c"], row["sum"], places=12)
        self.assertLess(row["abs_err"], 1e-12)

    def test_L1_does_not_silently_use_live_T(self):
        lams = [8.5, 9.0, 10.0]
        T0 = [0.2, -0.05, -0.15]
        T = [0.5, -0.1, -0.4]
        Lambda = 9.0
        d = [lam - Lambda for lam in lams]
        live = finite_gap_split(lams, T, Lambda)
        L1 = L1_N(Lambda, d, T0)
        self.assertNotAlmostEqual(L1, live["Lambda_dot_delta_T"], places=8)
        chk = first_variation_check(lams, T, T0, Lambda)
        self.assertAlmostEqual(chk["R2"], R2_N(chk["T_c"], Lambda, d, T0), places=12)
        self.assertTrue(chk["used_T0_in_L1_only"])


class RemainderOrderTests(unittest.TestCase):
    def test_legitimate_family_R2_is_quadratic(self):
        rows = [synthetic_family(eps, scramble=False, seed=1) for eps in (0.1, 0.05, 0.025)]
        scaled = [row["R2"] / (row["eps"] ** 2) for row in rows]
        # Same leading coefficient to a few digits as eps halves.
        self.assertAlmostEqual(scaled[1], scaled[2], places=1)
        self.assertLess(abs(rows[2]["R2"]), abs(rows[0]["R2"]))

    def test_scrambled_T_fails_the_order_check(self):
        legit = synthetic_family(0.05, scramble=False, seed=2)
        bad = synthetic_family(0.05, scramble=True, seed=2)
        self.assertGreater(abs(bad["R2_over_delta2"]), 2.0 * abs(legit["R2_over_delta2"]) + 0.1)


class OutcomeTreeTests(unittest.TestCase):
    def test_four_categories(self):
        self.assertEqual(classify_signs(0.4, -0.5, 0.2, True), BOTH_SIGNS)
        self.assertEqual(classify_signs(0.4, 0.01, 0.2, True), ONE_SIGN)
        self.assertEqual(classify_signs(0.01, -0.01, 0.2, True), ZERO_ONLY)
        self.assertEqual(classify_signs(0.4, -0.5, 0.2, False), NO_NEIGHBOR)

    def test_seed_keeps_the_field(self):
        seed = seed_A_plus(
            N=4,
            modes=((1, 0, 0), (0, 1, 0)),
            helicities=(1, -1),
            polarizations=((0.0, 1.0, 0.0), (1.0, 0.0, 0.0)),
            amplitudes=(1.0 + 0.5j, 0.2j),
            delta=(0.01, -0.01),
            T0=(0.3, -0.3),
        )
        self.assertEqual(seed["tag"], "A_N^+")
        self.assertEqual(seed["modes"][0], [1, 0, 0])
        self.assertEqual(len(seed["helicities"]), 2)
        self.assertIn("re", seed["amplitudes"][0])
        self.assertIn("polarizations", seed)
        self.assertIn("Save the field", seed["note"])


if __name__ == "__main__":
    unittest.main()
