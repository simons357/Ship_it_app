"""Exact one-cycle law: branch enumeration, quadratic/quartic, Heavy test."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.one_cycle_loss import (  # noqa: E402
    SMALL_HOLONOMY_LIMIT,
    cycle_moments,
    exact_one_cycle_optimum,
    heavy_one_cycle_test,
    holonomy_delta,
    nonlinear_stationarity,
    prediction_measurement_test,
    quadratic_minimizer,
    quartic_prediction,
    wrap_pi,
)


class WrapTests(unittest.TestCase):
    def test_interval_is_open_at_minus_pi(self):
        self.assertAlmostEqual(wrap_pi(0.0), 0.0, places=12)
        self.assertAlmostEqual(wrap_pi(math.pi), math.pi, places=12)
        self.assertAlmostEqual(wrap_pi(-math.pi), math.pi, places=12)
        self.assertAlmostEqual(wrap_pi(3.0 * math.pi), math.pi, places=12)
        self.assertGreater(wrap_pi(-math.pi + 1e-12), -math.pi)

    def test_holonomy_from_b(self):
        c = [1, -1, 1]
        b = [0.4, 0.1, 0.2]
        self.assertAlmostEqual(holonomy_delta(c, b), wrap_pi(0.4 - 0.1 + 0.2), places=12)


class QuadraticLawTests(unittest.TestCase):
    def test_closed_form(self):
        c = [1, -1, 1, -1]
        w = [1.0, 2.0, 3.0, 4.0]
        delta = 0.2
        out = quadratic_minimizer(c, w, delta)
        mom = cycle_moments(c, w)
        s, W = mom["S"], mom["W"]
        self.assertAlmostEqual(out["S"], s, places=12)
        self.assertAlmostEqual(out["one_minus_objective"], (delta ** 2) / (2.0 * s), places=12)
        self.assertAlmostEqual(out["one_minus_rho"], (delta ** 2) / (2.0 * W * s), places=12)
        self.assertAlmostEqual(out["loss_unnormalized"], out["one_minus_objective"], places=12)
        self.assertAlmostEqual(out["constraint"], delta, places=12)
        for i, (ci, wi) in enumerate(zip(c, w)):
            self.assertAlmostEqual(out["eps"][i], delta * (ci / wi) / s, places=12)

    def test_off_cycle_channels_are_zero(self):
        c = [1, 0, -1, 0]
        w = [1.0, 5.0, 2.0, 7.0]
        out = quadratic_minimizer(c, w, 0.3)
        self.assertEqual(out["eps"][1], 0.0)
        self.assertEqual(out["eps"][3], 0.0)
        self.assertTrue(out["off_cycle_zero"])

    def test_formula_string(self):
        out = quadratic_minimizer([1, 1], [1.0, 1.0], 0.1)
        self.assertIn("2 W S", out["formula"])


class QuarticTests(unittest.TestCase):
    def test_negative_quartic_correction(self):
        c = [1, -1, 1]
        w = [1.0, 2.0, 3.0]
        delta = 0.4
        q = quartic_prediction(c, w, delta)
        self.assertLess(q["quartic_correction"], 0.0)
        self.assertAlmostEqual(
            q["one_minus_rho"],
            q["quadratic_term"] + q["quartic_correction"],
            places=12,
        )
        self.assertAlmostEqual(q["rho_max"], 1.0 - q["one_minus_rho"], places=12)

    def test_series_lambda(self):
        c = [1, -2, 1]
        w = [2.0, 3.0, 4.0]
        mom = cycle_moments(c, w)
        delta = 0.15
        q = quartic_prediction(c, w, delta)
        expected = delta / mom["S"] - (mom["Q"] / (6.0 * mom["S"] ** 4)) * (delta ** 3)
        self.assertAlmostEqual(q["lambda_series"], expected, places=12)


class ExactStationarityTests(unittest.TestCase):
    def test_stationarity_equation_on_winner(self):
        c = [1, -2, 1]
        w = [2.0, 3.0, 4.0]
        delta = 0.08
        out = exact_one_cycle_optimum(c, w, delta)
        self.assertTrue(out["reachable"])
        self.assertTrue(out["lambda_bound_ok"])
        self.assertLessEqual(abs(out["lambda"]), out["lambda_max"] + 1e-12)
        for ci, wi, e in zip(c, w, out["eps"]):
            self.assertAlmostEqual(wi * math.sin(e), out["lambda"] * ci, places=8)
        self.assertAlmostEqual(out["constraint"], delta, places=8)

    def test_does_not_accept_the_first_root(self):
        c = [1, -1, 1, -1]
        w = [1.0, 1.5, 2.0, 2.5]
        exact = exact_one_cycle_optimum(c, w, 0.2)
        self.assertGreaterEqual(exact["n_candidates"], 1)
        self.assertEqual(exact["method"], "branch-enumeration")
        self.assertTrue(exact["principal_branch"])

    def test_off_cycle_locked_at_zero(self):
        c = [1, 0, -1]
        w = [1.0, 9.0, 2.0]
        out = exact_one_cycle_optimum(c, w, 0.25)
        self.assertEqual(out["eps"][1], 0.0)
        self.assertTrue(out["off_cycle_zero"])

    def test_zero_holonomy_is_perfect_alignment(self):
        c = [1, -1, 1, -1]
        w = [1.0, 1.5, 2.0, 2.5]
        out = nonlinear_stationarity(c, w, 0.0)
        self.assertAlmostEqual(out["one_minus_objective"], 0.0, places=10)
        self.assertAlmostEqual(out["objective_normalized"], 1.0, places=10)
        self.assertTrue(out["principal_branch"])
        for e in out["eps"]:
            self.assertAlmostEqual(e, 0.0, places=10)


class HeavyProtocolTests(unittest.TestCase):
    def test_small_delta_quadratic_and_quartic(self):
        c = [1, -1, 1]
        w = [1.0, 1.0, 2.0]
        delta = 0.05
        test = prediction_measurement_test(c, w, delta, rel_tol=0.05)
        self.assertTrue(test["pass_small_delta"])
        self.assertEqual(test["stamp"], "SMALL-HOLONOMY REGIME")
        self.assertEqual(test["scale_rate"], "OPEN")
        self.assertIn("2 W S", test["boxed"])

    def test_channel_by_channel_prediction(self):
        c = [1, 0, -2, 1]
        w = [1.0, 4.0, 2.0, 3.0]
        delta = 0.12
        heavy = heavy_one_cycle_test(c, w, delta)
        self.assertTrue(heavy["pass_channels"])
        self.assertTrue(heavy["pass_off_cycle"])
        self.assertEqual(heavy["eps2"][1], 0.0)
        self.assertAlmostEqual(heavy["exact"]["eps"][1], 0.0, places=12)

    def test_quartic_is_closer_and_quadratic_overestimates(self):
        c = [1, -1, 1, -1]
        w = [1.0, 2.0, 1.5, 2.5]
        delta = 0.35
        heavy = heavy_one_cycle_test(c, w, delta)
        self.assertTrue(heavy["in_small_holonomy_regime"])
        self.assertTrue(heavy["pass_small_delta"])
        self.assertTrue(heavy["quartic_closer_than_quadratic"])
        # Negative quartic: quadratic slightly overestimates true loss.
        self.assertGreater(heavy["one_minus_rho2"], heavy["measurement"] - 1e-12)

    def test_outside_small_holonomy_is_stamped_not_scored(self):
        c = [1, -1]
        w = [1.0, 1.0]
        delta = 0.5 * math.pi + 0.2
        self.assertGreater(abs(delta), SMALL_HOLONOMY_LIMIT)
        heavy = heavy_one_cycle_test(c, w, delta)
        self.assertFalse(heavy["in_small_holonomy_regime"])
        self.assertEqual(heavy["stamp"], "OUTSIDE PREREGISTERED SMALL-HOLONOMY REGIME")
        self.assertFalse(heavy["pass_quadratic"])
        self.assertFalse(heavy["pass_quartic"])
        self.assertTrue(heavy["exact"]["reachable"])
        self.assertIsNotNone(heavy["exact"]["rho"])

    def test_lambda_bound(self):
        c = [1, -3]
        w = [2.0, 3.0]
        mom = cycle_moments(c, w)
        self.assertAlmostEqual(mom["lambda_max"], min(2.0 / 1.0, 3.0 / 3.0), places=12)
        heavy = heavy_one_cycle_test(c, w, 0.2)
        self.assertLessEqual(abs(heavy["exact"]["lambda"]), mom["lambda_max"] + 1e-12)


if __name__ == "__main__":
    unittest.main()
