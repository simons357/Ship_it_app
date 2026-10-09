"""Gate D integrating-factor solver: measurements, not a budget theorem."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from gate_d_fourier_budget import (  # noqa: E402
    broadband_ic,
    cutoff_compare,
    local_extrema,
    run_budget,
)
from ns_solver_core import make_grid, max_div, project_state  # noqa: E402


class TestLocalExtrema(unittest.TestCase):
    def test_regeneration_and_turnover(self):
        series = [1.0, 0.4, 0.8, 0.3, 0.9, 0.2]
        ext = local_extrema(series)
        self.assertGreaterEqual(ext["regeneration_events"], 1)
        self.assertGreaterEqual(ext["n_peaks"], 1)
        self.assertIsInstance(ext["turnover_gaps_steps"], list)


class TestIntegratingFactorRun(unittest.TestCase):
    def test_broadband_is_divergence_free(self):
        n = 8
        kx, ky, kz, _, k2_safe, _ = make_grid(n)
        u, v, w = broadband_ic(n, seed=1)
        u, v, w = project_state(u, v, w, kx, ky, kz, k2_safe)
        self.assertLess(max_div(u, v, w, kx, ky, kz), 1e-10)

    def test_short_unforced_run_decays_and_stays_df(self):
        r = run_budget(
            n=8, nu=0.08, t_end=0.08, dt=0.02, seed=0, ic="broadband"
        )
        self.assertTrue(r["energy_decayed"])
        self.assertLess(r["max_div_end"], 1e-8)
        self.assertFalse(r["cutoff_independent_budget"])
        self.assertFalse(r["ns_solved"])
        self.assertGreater(r["energy0"], 0.0)

    def test_taylor_green_energy_drops(self):
        r = run_budget(
            n=8, nu=0.1, t_end=0.06, dt=0.02, ic="taylor_green"
        )
        self.assertLess(r["energy_end"], r["energy0"])
        self.assertFalse(r["ns_solved"])

    def test_cutoff_compare_refuses_the_budget(self):
        a = run_budget(n=8, nu=0.1, t_end=0.04, dt=0.02, seed=2)
        b = run_budget(n=8, nu=0.1, t_end=0.04, dt=0.02, seed=2)
        cmp_ = cutoff_compare(a, b)
        self.assertFalse(cmp_["cutoff_independent_budget"])
        self.assertTrue(cmp_["same_episode_count"])


if __name__ == "__main__":
    unittest.main()
