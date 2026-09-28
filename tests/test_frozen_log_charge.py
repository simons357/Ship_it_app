"""Frozen logarithmic charge: identities and the fixed-(θ<1) strike."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.fourier import cube_modes  # noqa: E402
from ns_attacks.frozen_charge import R_nu1_bound, charge_split, nearly_equilateral_failfast  # noqa: E402
from ns_attacks.galerkin import flux_stats, random_cube, rk4_step  # noqa: E402
from ns_attacks.symmetry_2d3c import locked_seed  # noqa: E402


class FrozenLogChargeTests(unittest.TestCase):
    def test_identity_on_vector_galerkin(self):
        rng = np.random.default_rng(4)
        f = random_cube(1, rng)
        st = flux_stats(f, cube_modes(1))
        kappa = math.sqrt(st["Lambda"])
        split = charge_split(st, nu=0.3, theta=0.5, kappa_e=kappa)
        self.assertLess(split["recon_err"], 1e-12)

    def test_identity_on_locked_seed(self):
        f = locked_seed()
        st = flux_stats(f, f.modes())
        split = charge_split(st, nu=1.0, theta=0.99, kappa_e=math.sqrt(st["Lambda"]))
        self.assertLess(split["recon_err"], 1e-12)

    def test_finite_difference_matches_C_e_prime(self):
        f = locked_seed()
        modes = f.modes()
        nu = 0.2
        st0 = flux_stats(f, modes)
        kappa = math.sqrt(st0["Lambda"])
        split0 = charge_split(st0, nu=nu, theta=1.0, kappa_e=kappa)
        dt = 1e-5
        f1 = rk4_step(f, modes, nu, dt)
        st1 = flux_stats(f1, modes)
        Ce1 = math.log(st1["X"] / (kappa * st1["H_a"]))
        fd = (Ce1 - split0["C_e"]) / dt
        self.assertLess(abs(fd - split0["C_e_prime"]) / max(1.0, abs(split0["C_e_prime"])), 5e-3)

    def test_narrow_band_viscous_bound_10000(self):
        rng = np.random.default_rng(5)
        worst = 0.0
        n_ok = 0
        for _ in range(10000):
            a = 0.5 + rng.random()
            width = 0.05 + 0.5 * rng.random()
            b = a + width
            n = 8
            radii = a + (b - a) * rng.random(n)
            masses = rng.random(n)
            rec = R_nu1_bound(radii, masses)
            self.assertTrue(rec["ok"], rec)
            n_ok += 1
            worst = max(worst, rec["abs_R"] / max(rec["bound"], 1e-18))
        self.assertEqual(n_ok, 10000)
        self.assertLessEqual(worst, 1.0 + 1e-9)

    def test_theta_poison_is_explicit(self):
        rng = np.random.default_rng(0)
        f = random_cube(1, rng)
        st = flux_stats(f, cube_modes(1))
        kappa = math.sqrt(st["Lambda"])
        s1 = charge_split(st, nu=1.0, theta=1.0, kappa_e=kappa)
        s0 = charge_split(st, nu=1.0, theta=0.0, kappa_e=kappa)
        self.assertAlmostEqual(s0["R_nu_theta"] - s1["R_nu_1"], st["D_s"] / st["Y"], places=10)

    def test_failfast_positive_G_negative_charge(self):
        rec = nearly_equilateral_failfast()
        self.assertGreater(rec["radius_gap"], 0.0)
        self.assertGreater(rec["theta_0.99"]["poison"], 0.0)
        for key in ("theta_0.0", "theta_0.5", "theta_0.99", "theta_0.999"):
            self.assertTrue(rec[key]["strike"], msg=key)


if __name__ == "__main__":
    unittest.main()
