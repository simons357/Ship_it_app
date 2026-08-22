"""Smoke tests for Track A Q1-augmented NS verifier."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from augmented_ns_verify import fft, ifft, make_grid, project, run_once, taylor_green  # noqa: E402


class AugmentedNSVerifyTests(unittest.TestCase):
    def test_taylor_green_is_divergence_free(self):
        n = 12
        kx, ky, kz, _, k2_safe, _ = make_grid(n)
        u, v, w = taylor_green(n)
        uh, vh, wh = project(fft(u), fft(v), fft(w), kx, ky, kz, k2_safe)
        div = ifft(1j * kx * uh + 1j * ky * vh + 1j * kz * wh)
        self.assertLess(float(np.max(np.abs(div))), 1e-12)

    def test_energy_identity_short_run(self):
        r = run_once(n=12, nu=0.05, eps=0.1, alpha=1.0, beta=0.5, t_end=0.1, dt=0.01)
        self.assertGreater(r.energy0, 0.0)
        self.assertGreater(r.diss_q1, 0.0)
        self.assertLess(r.residual / r.energy0, 1e-3)
        self.assertLess(r.max_div, 1e-10)


if __name__ == "__main__":
    unittest.main()
