"""Arithmetic sign realizability. Loop-gauge board is not altered."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.sign_realizability import (  # noqa: E402
    energy_sum,
    exact_shell_triads,
    first_variation,
    helical_field,
    is_sum_of_three_squares,
    modal_transfers,
    moments,
    neighbor_deformations,
    report,
    scan_scale,
    verdict,
)


class ShellTests(unittest.TestCase):
    def test_three_squares_filter(self):
        self.assertTrue(is_sum_of_three_squares(6))
        self.assertFalse(is_sum_of_three_squares(7))
        self.assertFalse(is_sum_of_three_squares(15))

    def test_exact_shell_triads_close(self):
        # N=6 is the first even three-square shell that can host a triad.
        triads = exact_shell_triads(6)
        for p, q, k in triads:
            self.assertEqual((p[0] + q[0], p[1] + q[1], p[2] + q[2]), k)
            self.assertEqual(p[0] ** 2 + p[1] ** 2 + p[2] ** 2, 6)
            self.assertEqual(q[0] ** 2 + q[1] ** 2 + q[2] ** 2, 6)
            self.assertEqual(k[0] ** 2 + k[1] ** 2 + k[2] ** 2, 6)


class IdentityTests(unittest.TestCase):
    def test_exact_shell_Tc_vanishes(self):
        triads = exact_shell_triads(6)
        self.assertTrue(triads)
        p, q, k = triads[0]
        field = helical_field((p, q, k), (1, 1, -1))
        t = modal_transfers(field)
        self.assertLess(abs(energy_sum(t)), 1e-12)
        mom = moments(field, t)
        self.assertAlmostEqual(mom["Lambda"], 6.0, places=10)
        self.assertAlmostEqual(mom["T_c"], 0.0, places=10)
        self.assertLess(abs(mom["identity_residual"]), 1e-10)

    def test_finite_gap_identity_uses_actual_T(self):
        triads = exact_shell_triads(6)
        kids = neighbor_deformations(triads[0])
        self.assertTrue(kids)
        row = first_variation(triads[0], kids[0]["child"], (1, 1, -1))
        self.assertLess(abs(row["identity_N"]), 1e-8)
        self.assertLess(abs(row["energy_sum_N"]), 1e-10)
        # Neighboring T is retained and is not silently T^{(0)}.
        self.assertEqual(len(row["T_N_roles"]), 3)
        self.assertEqual(len(row["T_0_roles"]), 3)

    def test_L1_is_frozen_transfer(self):
        triads = exact_shell_triads(6)
        kids = neighbor_deformations(triads[0])
        row = first_variation(triads[0], kids[0]["child"], (1, -1, 1))
        self.assertAlmostEqual(
            row["L_1_N"],
            row["Lambda_N"] * row["inner_dT0"],
            places=10,
        )
        self.assertAlmostEqual(row["R_2_N"], row["T_c_N"] - row["L_1_N"], places=10)


class CategoryTests(unittest.TestCase):
    def test_empty_shell_is_no_neighbor(self):
        sc = scan_scale(7)
        self.assertEqual(sc["category"], "NO_NEIGHBOR")

    def test_verdict_has_required_categories(self):
        tree = verdict(
            [
                {
                    "N": 7,
                    "category": "NO_NEIGHBOR",
                    "samples": [],
                }
            ]
        )
        self.assertEqual(tree["outcome"], "NO_NEIGHBOR")
        self.assertIn("Arithmetic rigidity", tree["reading"])

    def test_report_does_not_touch_loop_gauge(self):
        rep = report(scales=[6, 7, 10])
        self.assertTrue(rep["locks"]["loop_gauge_unaltered"])
        self.assertTrue(rep["locks"]["T_neighbor_kept_separate"])
        self.assertTrue(rep["locks"]["no_silent_T0_substitution"])
        self.assertTrue(rep["locks"]["no_neighbor_is_own_category"])
        self.assertTrue(rep["locks"]["phase_twin_is_not_both_signs"])
        self.assertIn(rep["verdict"]["outcome"], {
            "BOTH_SIGNS",
            "ONE_SIGN_PLUS",
            "ONE_SIGN_MINUS",
            "ZERO_ONLY",
            "NO_HETERO_SIGNAL",
            "NO_NEIGHBOR",
        })

    def test_homochiral_parent_transfer_vanishes(self):
        triads = exact_shell_triads(6)
        field = helical_field(triads[0], (1, 1, 1))
        t = modal_transfers(field)
        mom = moments(field, t)
        self.assertAlmostEqual(mom["T_c"], 0.0, places=10)
        t_rms = math.sqrt(sum(v * v for v in t.values()) / max(len(t), 1))
        self.assertLess(t_rms, 1e-10)

    def test_remainder_is_higher_order_along_the_family(self):
        rep = report(scales=[6, 18, 50])
        order = {row["N"]: row["median_abs_R2_over_L1"] for row in rep["remainder_order"]}
        self.assertIn(6, order)
        self.assertIn(50, order)
        self.assertLess(order[50], order[6])
        self.assertEqual(rep["verdict"]["outcome"], "BOTH_SIGNS")
        self.assertTrue(rep["verdict"]["stop_static_closure"])
        seed = rep["verdict"]["seed_A_N_plus"]
        self.assertIn("integer_vectors", seed)
        self.assertIn("helicity", seed)
        self.assertIn("polarizations", seed)
        self.assertIn("amplitudes", seed)


if __name__ == "__main__":
    unittest.main()
