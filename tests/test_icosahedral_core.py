"""Centered icosahedron: exact Q(φ) geometry and rational-shell Taylor test."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.fourier import nrm2  # noqa: E402
from ns_attacks.icosahedral import (  # noqa: E402
    PHI,
    PhiNum,
    finite_difference_check,
    icosa_geometry,
    one_shell_field,
    quadratic_output_modes,
    rational_shell,
)


class IcosahedralCoreTests(unittest.TestCase):
    def test_phi_minimal_polynomial(self):
        self.assertEqual(PHI * PHI, PhiNum(1, 1))  # φ² = φ+1

    def test_abstract_geometry(self):
        g = icosa_geometry()
        self.assertEqual(g["n_vertices"], 12)
        self.assertTrue(g["sum_zero"])
        self.assertTrue(g["radius_ok"])
        self.assertTrue(g["second_moment_isotropic"])
        self.assertTrue(g["pair_sums_leave_shell"])
        self.assertTrue(g["not_a_Z3_orbit"])
        # Distinct non-antipodal pair sums: 4 and 4+4φ in Q(φ).
        vals = set(g["pair_sum_R2_values"])
        self.assertIn((4, 0), vals)
        self.assertIn((4, 4), vals)  # 4+4φ

    def test_rational_shell_one_shell_center(self):
        shell = rational_shell(3, 2)
        self.assertEqual(len(shell), 12)
        K = nrm2(shell[0])
        self.assertTrue(all(nrm2(k) == K for k in shell))
        self.assertEqual(K, 13)
        f = one_shell_field(shell, rng=np.random.default_rng(3))
        outs = quadratic_output_modes(shell)
        rec = finite_difference_check(f, outs, K, dt=1e-5, nu=0.0)
        self.assertLess(abs(rec["T_c0"]), 1e-10)
        self.assertLess(abs(rec["D_s0"]), 1e-10)
        self.assertAlmostEqual(rec["Lambda0"], float(K), places=10)
        self.assertGreater(rec["analytic_Tc_prime"], 0.0)
        self.assertGreater(rec["analytic_Ds_second"], 0.0)
        self.assertEqual(rec["outward_active"], 1.0)
        self.assertLess(rec["Tc_prime_err"] / max(1.0, abs(rec["analytic_Tc_prime"])), 5e-3)
        self.assertLess(rec["Ds_second_rel_err"], 5e-2)

    def test_ratio_window(self):
        with self.assertRaises(ValueError):
            rational_shell(1, 1)
        with self.assertRaises(ValueError):
            rational_shell(2, 1)  # 2 > √3


if __name__ == "__main__":
    unittest.main()
