"""Checks for inverse-GCD floor certificates and restricted Rayleigh helpers."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from spectral_floor_explore import (  # noqa: E402
    bridge_star_values,
    certificates,
    lambda_min,
    prime_subspace_min,
    qtilde,
    raw_q,
    rayleigh,
)


class SpectralFloorExploreTests(unittest.TestCase):
    def test_withdrawn_full_spectrum_certificates(self):
        cert = certificates()
        self.assertLess(cert["q10_min"], -0.5)
        self.assertLess(cert["qt20_min"], -0.5)
        self.assertAlmostEqual(cert["q10_min"], -1.90, places=1)

    def test_bridge_star_pair_stays_above_half(self):
        vals = bridge_star_values(40)
        self.assertTrue(vals)
        self.assertGreater(min(vals), -0.5)
        r23 = 0.5 * (0.25 + 1 / 9) - 1 / math.sqrt(6)
        self.assertGreater(r23, -0.5)
        self.assertLess(r23, 0.0)

    def test_nonnegative_vector_has_nonnegative_qt_form(self):
        qt = qtilde(20)
        v = np.ones(20)
        self.assertGreaterEqual(rayleigh(qt, v), 0.0)

    def test_raw_q_symmetric(self):
        q = raw_q(12)
        self.assertTrue(np.allclose(q, q.T))
        ev, _ = lambda_min(q)
        self.assertTrue(math.isfinite(ev))

    def test_prime_subspace_floor_minus_quarter(self):
        for n in (3, 10, 20, 40, 80):
            self.assertGreaterEqual(prime_subspace_min(n), -0.25)


if __name__ == "__main__":
    unittest.main()
