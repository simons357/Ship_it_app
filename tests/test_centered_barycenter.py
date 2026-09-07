"""Finite checks for overnight identities. Not DA-NS-2. Not RH."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from centered_barycenter import (  # noqa: E402
    log_lambda_prime,
    mobius_claimed_sum,
    modes_to_moments,
    two_triad_strike,
)


class CenteredBarycenterTests(unittest.TestCase):
    def test_variance_factorization(self):
        a = [1.0, 2.0, 5.0]
        mass = [0.4, 0.3, 0.2]
        m = modes_to_moments(a, mass)
        self.assertGreaterEqual(m["D_s"], -1e-12)
        self.assertAlmostEqual(m["D_s"], m["D_s_fact"], places=12)
        self.assertAlmostEqual(m["Lambda"], m["Lambda_from_p"], places=12)
        self.assertAlmostEqual(m["D_s"] / m["X"], m["D_s_over_X"], places=12)

    def test_log_identity_matches_lambda_over_lambda(self):
        t_c, nu, d_s, x, y = 0.3, 1.0, 0.1, 2.0, 4.0
        lam = y / x
        log_p = log_lambda_prime(t_c, nu, d_s, y)
        lam_p = 2.0 * (t_c - nu * d_s) / x
        self.assertAlmostEqual(log_p, lam_p / lam, places=12)

    def test_two_triad_kills_charge_only(self):
        s = two_triad_strike()
        self.assertAlmostEqual(s["Q_sum"], 0.0, places=12)
        self.assertAlmostEqual(s["T1"], s["R1"] * s["Q1"], places=10)
        self.assertAlmostEqual(s["T2"], s["R2"] * s["Q2"], places=10)
        self.assertAlmostEqual(s["T_sum"], s["T_from_RQ"], places=10)
        self.assertAlmostEqual(s["T_sum"], s["rho"], places=10)
        self.assertAlmostEqual(s["T_sum"], s["boxed"], places=10)
        self.assertGreater(s["T_sum"], 0.0)

    def test_mobius_identity_fails_at_two(self):
        self.assertAlmostEqual(mobius_claimed_sum(1), 1.0, places=12)
        self.assertAlmostEqual(mobius_claimed_sum(2), 0.75, places=12)
        self.assertNotAlmostEqual(mobius_claimed_sum(2), 0.5, places=6)


if __name__ == "__main__":
    unittest.main()
