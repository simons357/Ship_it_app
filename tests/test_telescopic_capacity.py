"""Telescopic capacity. Do not count resets; do not use Λ-motion."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.telescopic_capacity import (  # noqa: E402
    W_from_moments,
    W_from_spectrum,
    midpoint_crossings,
    nearest_center,
    nearest_center_reset,
    reject_if_circular,
    report,
    reset_jump,
    telescopic_score,
)


class IdentityTests(unittest.TestCase):
    def test_W_equals_spectral_spread_about_K(self):
        # Locked §4 triad moments.
        row = W_from_moments(10.0, 14.0, 22.0, K=1.0)
        self.assertAlmostEqual(row["Lambda"], 1.4, places=12)
        self.assertAlmostEqual(row["D_s"], 2.4, places=12)
        self.assertTrue(row["identity_holds"])
        spec = W_from_spectrum([1.0, 1.0, 2.0], [3.0, 3.0, 2.0], K=1.0)
        self.assertAlmostEqual(spec["X"], 10.0, places=12)
        self.assertAlmostEqual(spec["Y"], 14.0, places=12)
        self.assertAlmostEqual(spec["Z"], 22.0, places=12)
        self.assertTrue(spec["spectral_matches"])
        self.assertAlmostEqual(spec["W"], row["W"], places=12)

    def test_nearest_center_kills_the_reset_cost(self):
        jump = nearest_center_reset(10.0, 1.4, 4.0, [1.0, 2.0, 4.0])
        self.assertEqual(jump["K_to"], 1.0)
        self.assertLessEqual(jump["dW"], 0.0)
        self.assertTrue(jump["design_kills_reset_cost"])
        # Moving away from Λ costs.
        away = reset_jump(10.0, 1.4, 1.0, 4.0)
        self.assertGreater(away["dW"], 0.0)

    def test_already_nearest_is_a_zero_jump(self):
        jump = nearest_center_reset(10.0, 1.4, 1.0, [1.0, 2.0, 4.0])
        self.assertAlmostEqual(jump["dW"], 0.0, places=12)

    def test_W_K_is_telescopic_at_reset(self):
        jump = nearest_center_reset(3.0, 5.5, 1.0, [1.0, 4.0, 9.0])
        score = telescopic_score(jump["dW"], paid=0.0)
        self.assertTrue(score["telescopic"])
        self.assertTrue(score["best_case"])


class CircularityTests(unittest.TestCase):
    def test_lambda_motion_proposals_are_rejected(self):
        a = reject_if_circular("few resets because Lambda cannot move much")
        b = reject_if_circular("sum |ΔK_e| ≤ C int |Lambda'| dt")
        c = reject_if_circular("bound #epochs by int |T_c - nu D_s|")
        self.assertTrue(a["rejected"])
        self.assertTrue(b["rejected"])
        self.assertTrue(c["rejected"])

    def test_nonpositive_jump_design_is_not_rejected(self):
        a = reject_if_circular("Q_{e+1}(u) ≤ Q_e(u) at every nearest-center reset")
        b = reject_if_circular("nearest-center ΔW ≤ 0, no motion hypothesis")
        self.assertFalse(a["rejected"])
        self.assertFalse(b["rejected"])

    def test_midpoint_count_is_marked_circular(self):
        path = [0.5, 1.6, 2.6, 3.6]
        row = midpoint_crossings(path, [1.0, 2.0, 3.0, 4.0])
        self.assertGreaterEqual(row["n_switches"], 1)
        self.assertTrue(row["circular"])
        self.assertIn("circular", row["reason"])

    def test_nearest_center_prefers_the_closer_chart(self):
        self.assertEqual(nearest_center(2.4, [1.0, 2.0, 4.0]), 2.0)
        self.assertEqual(nearest_center(3.2, [1.0, 2.0, 4.0]), 4.0)


class ReportTests(unittest.TestCase):
    def test_report_locks(self):
        rep = report()
        self.assertTrue(rep["locks"]["center_selection_reset_cost_killed_by_design"])
        self.assertTrue(rep["locks"]["reset_summability_not_solved"])
        self.assertTrue(rep["locks"]["epoch_count_is_the_wrong_target"])
        self.assertTrue(rep["locks"]["circular_lambda_motion_rejected"])
        self.assertTrue(rep["locks"]["not_a_close"])
        self.assertTrue(rep["note_triad_W"]["identity_holds"])
        names = [c["name"] for c in rep["candidates"]]
        self.assertIn("W_K", names)
        self.assertIn("epoch-count", names)


if __name__ == "__main__":
    unittest.main()
