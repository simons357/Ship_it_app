"""Centered flux: barycenter identity packaging. Not DA-NS-2."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.fourier import cube_modes  # noqa: E402
from ns_attacks.galerkin import flux_stats, random_cube  # noqa: E402
from ns_attacks.reset_safe import charge_covariance  # noqa: E402


class CenteredFluxIdentityTests(unittest.TestCase):
    def test_energy_pairing_vanishes(self):
        rng = np.random.default_rng(0)
        f = random_cube(1, rng)
        st = flux_stats(f, cube_modes(1))
        self.assertLess(abs(st["energy_pairing"]), 1e-12)

    def test_variance_nonnegative(self):
        rng = np.random.default_rng(1)
        f = random_cube(2, rng)
        st = flux_stats(f, cube_modes(2))
        self.assertGreaterEqual(st["D_s"], -1e-10)
        self.assertGreater(st["X"], 0.0)
        self.assertAlmostEqual(st["Lambda"], st["Y"] / st["X"], places=12)

    def test_two_triad_kills_charge_only(self):
        s = charge_covariance()
        self.assertAlmostEqual(s["Q_a_Gamma"], 0.0, places=12)
        self.assertAlmostEqual(s["T_c_1"], s["R_1"] * s["Q_a_1"], places=10)
        self.assertAlmostEqual(s["T_c_2"], s["R_2"] * s["Q_a_2"], places=10)
        self.assertAlmostEqual(s["T_c_het_Gamma"], s["T_from_RQ"], places=10)
        self.assertAlmostEqual(s["T_c_het_Gamma"], s["boxed"], places=10)
        self.assertAlmostEqual(s["T_c_het_Gamma"], s["rho"], places=10)
        self.assertGreater(s["T_c_het_Gamma"], 0.0)

    def test_log_lambda_packaging(self):
        t_c, nu, d_s, y = 0.3, 1.0, 0.1, 4.0
        log_p = 2.0 * (t_c - nu * d_s) / y
        self.assertAlmostEqual(log_p, 0.1, places=12)


if __name__ == "__main__":
    unittest.main()
