"""S-measurement locks: unique count, invariance, numbers behind zero."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_solver_core import make_grid, project_state, taylor_green  # noqa: E402
from s_measurement import (  # noqa: E402
    PERM_COUNT,
    format_measurement,
    invariant_interaction,
    measure_field,
    permutation_invariance_check,
)


def _hand_triad():
    """One real, divergence-free triad k+p+q=0 with a nonzero kernel."""
    k = (1, 0, 0)
    p = (0, 1, 1)
    q = (-1, -1, -1)
    vk = np.array([0.0, 1.0, 0.0], dtype=complex)
    vp = np.array([1.0, 0.0, 0.0], dtype=complex)  # p·vp = 0
    vq = np.array([0.0, 1.0, -1.0], dtype=complex)
    # q·vq = -1-(-1)=0
    return k, p, q, vk, vp, vq


class SMeasurementTests(unittest.TestCase):
    def test_kernel_is_labeling_invariant(self):
        k, p, q, vk, vp, vq = _hand_triad()
        report = permutation_invariance_check(k, p, q, vk, vp, vq, tol=5e-13)
        self.assertEqual(report["perm_count"], PERM_COUNT)
        self.assertTrue(report["ok"], f"spread={report['spread']!r} values={report['values']!r}")
        self.assertLess(report["spread"], 1e-12)

    def test_overcount_is_six_times_unique(self):
        n = 8
        kx, ky, kz, _, k2_safe, _ = make_grid(n)
        x = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
        X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
        # Explicit real triad k+p+q=0 with k=(1,0,0), p=(0,1,1), q=(-1,-1,-1).
        u = np.cos(Y + Z) + 0.4 * np.sin(X)
        v = np.sin(X) + 0.3 * np.cos(Y + Z) - 0.2 * np.cos(X + Y + Z)
        w = -np.sin(Y + Z) + 0.2 * np.cos(X + Y + Z)
        u, v, w = project_state(u, v, w, kx, ky, kz, k2_safe)
        unique = measure_field(u, v, w, nu=0.02, overcount=False)
        sixfold = measure_field(u, v, w, nu=0.02, overcount=True)
        self.assertGreater(unique["n_unique_triangles"], 0)
        self.assertAlmostEqual(sixfold["n_counted"] / unique["n_unique_triangles"], 6.0, places=6)
        if unique["abs_transfer"] > 0.0:
            ratio = sixfold["abs_transfer"] / unique["abs_transfer"]
            self.assertAlmostEqual(ratio, 6.0, places=8)
        # Viscous amount is not multiplied by 6.
        self.assertAlmostEqual(unique["viscous"], sixfold["viscous"], places=10)
        # Coherence is a ratio: 6× cancels.
        self.assertAlmostEqual(unique["coherence"], sixfold["coherence"], places=10)

    def test_numbers_printed_when_s_is_zero(self):
        n = 8
        u, v, w = taylor_green(n)
        kx, ky, kz, _, k2_safe, _ = make_grid(n)
        u, v, w = project_state(u, v, w, kx, ky, kz, k2_safe)
        m = measure_field(u, v, w, nu=0.02)
        line = format_measurement(m, label="tg0 ")
        self.assertIn("transfer=", line)
        self.assertIn("viscous=", line)
        self.assertIn("coherence=", line)
        self.assertIn("|T|/visc=", line)
        self.assertIn("triangles=", line)
        if m["S_is_zero"]:
            self.assertIn("S=0", line)
            self.assertIsNotNone(m["numbers_behind_zero"]["abs_transfer_over_viscous"])

    def test_taylor_green_t0_transfer_below_viscous(self):
        n = 8
        u, v, w = taylor_green(n)
        kx, ky, kz, _, k2_safe, _ = make_grid(n)
        u, v, w = project_state(u, v, w, kx, ky, kz, k2_safe)
        m = measure_field(u, v, w, nu=0.02)
        self.assertGreater(m["viscous"], 0.0)
        self.assertLess(m["abs_transfer"], m["viscous"])
        self.assertTrue(m["S_is_zero"])
        self.assertEqual(m["S"], 0.0)


if __name__ == "__main__":
    unittest.main()
