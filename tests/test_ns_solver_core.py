"""Solver-core locks: S1–S3. Classical NS stays open."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_solver_core import (  # noqa: E402
    fft,
    ifft,
    instantaneous_energy_check,
    make_grid,
    project,
    run_once,
    taylor_green,
)


class SolverCoreTests(unittest.TestCase):
    def test_taylor_green_is_divergence_free(self):
        n = 12
        kx, ky, kz, _, k2_safe, _ = make_grid(n)
        u, v, w = taylor_green(n)
        uh, vh, wh = project(fft(u), fft(v), fft(w), kx, ky, kz, k2_safe)
        div = ifft(1j * kx * uh + 1j * ky * vh + 1j * kz * wh)
        self.assertLess(float(np.max(np.abs(div))), 1e-12)

    def test_instantaneous_residual_beats_retired_3e4(self):
        """S1/S3: the live check is not the misleading 3–5e-4 number."""
        n = 12
        kx, ky, kz, k2, k2_safe, dealias = make_grid(n)
        u, v, w = taylor_green(n)
        uh, vh, wh = project(fft(u), fft(v), fft(w), kx, ky, kz, k2_safe)
        u, v, w = ifft(uh), ifft(vh), ifft(wh)
        for eps in (0.0, 0.2):
            check = instantaneous_energy_check(
                u,
                v,
                w,
                kx=kx,
                ky=ky,
                kz=kz,
                k2=k2,
                k2_safe=k2_safe,
                dealias=dealias,
                nu=0.02,
                eps=eps,
                alpha=1.0,
                beta=0.5,
            )
            self.assertLess(check["residual"], 3e-4)
            self.assertLess(check["relative_residual"], 1e-6)

    def test_short_run_accepted_state_div_and_energy(self):
        """S2: after the step, div is on the accepted field."""
        r = run_once(n=12, nu=0.05, eps=0.0, alpha=1.0, beta=0.5, t_end=0.08, dt=0.02)
        self.assertGreater(r.energy0, 0.0)
        self.assertLess(r.energy_t, r.energy0)
        self.assertLess(r.residual, 1e-6)
        self.assertLess(r.max_div, 1e-10)
        self.assertEqual(r.energy_check, "instantaneous_inner_product")


if __name__ == "__main__":
    unittest.main()
