"""One-cycle loss law: quadratic prediction vs nonlinear measurement."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.one_cycle_loss import (  # noqa: E402
    nonlinear_stationarity,
    prediction_measurement_test,
    quadratic_minimizer,
)


class QuadraticLawTests(unittest.TestCase):
    def test_closed_form(self):
        c = [1, -1, 1, -1]
        w = [1.0, 2.0, 3.0, 4.0]
        delta = 0.2
        out = quadratic_minimizer(c, w, delta)
        s = sum(ci * ci / wi for ci, wi in zip(c, w))
        self.assertAlmostEqual(out["S"], s, places=12)
        self.assertAlmostEqual(out["one_minus_objective"], (delta ** 2) / (2.0 * s), places=12)
        self.assertAlmostEqual(out["loss"], out["one_minus_objective"], places=12)
        self.assertAlmostEqual(out["constraint"], delta, places=12)
        for i, (ci, wi) in enumerate(zip(c, w)):
            self.assertAlmostEqual(out["eps"][i], delta * (ci / wi) / s, places=12)

    def test_formula_string(self):
        out = quadratic_minimizer([1, 1], [1.0, 1.0], 0.1)
        self.assertIn("δ²", out["formula"])


class NonlinearTests(unittest.TestCase):
    def test_small_delta_matches_quadratic(self):
        c = [1, -1, 1]
        w = [1.0, 1.0, 2.0]
        delta = 0.05
        test = prediction_measurement_test(c, w, delta, rel_tol=0.05)
        self.assertTrue(test["pass_small_delta"])
        self.assertEqual(test["scale_rate"], "OPEN")
        self.assertIn("δ²", test["boxed"])

    def test_stationarity_equation(self):
        c = [1, -2, 1]
        w = [2.0, 3.0, 4.0]
        delta = 0.08
        out = nonlinear_stationarity(c, w, delta)
        self.assertTrue(out["reachable"])
        self.assertTrue(out["not_optimizer_evidence"])
        for ci, wi, e in zip(c, w, out["eps"]):
            self.assertAlmostEqual(wi * math.sin(e), out["lambda"] * ci, places=8)
        self.assertAlmostEqual(out["constraint"], delta, places=8)

    def test_zero_holonomy_recovers_tree_objective(self):
        c = [1, -1, 1, -1]
        w = [1.0, 1.5, 2.0, 2.5]
        out = nonlinear_stationarity(c, w, 0.0)
        self.assertAlmostEqual(out["one_minus_objective"], 0.0, places=10)
        self.assertAlmostEqual(out["objective_normalized"], 1.0, places=10)


if __name__ == "__main__":
    unittest.main()
