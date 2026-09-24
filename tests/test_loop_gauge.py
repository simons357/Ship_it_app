"""Loop-gauge test. Topology is not a phase-frustration theorem."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.loop_gauge import (  # noqa: E402
    PARALLELOGRAM,
    STAR_WITNESS,
    additive_gauge_family,
    apply_B,
    constrained_cosine_max,
    convolution_phases_vanish,
    holonomy,
    incidence_matrix,
    left_kernel_basis,
    locked_cycle_vector,
    loop_gauge_test,
    parallelogram_report,
    star_report,
)


class IncidenceTests(unittest.TestCase):
    def test_star_has_empty_left_kernel(self):
        closed, modes, B = incidence_matrix(STAR_WITNESS)
        self.assertEqual(len(closed), 2)
        self.assertIn((-1, 0, 0), modes)
        ker = left_kernel_basis(B)
        self.assertEqual(ker, [])

    def test_parallelogram_has_the_locked_cycle(self):
        closed, modes, B = incidence_matrix(PARALLELOGRAM)
        self.assertEqual(len(closed), 4)
        ker = left_kernel_basis(B)
        self.assertEqual(len(ker), 1)
        locked = locked_cycle_vector()
        # Basis vector is a unit multiple of the locked generator.
        c = ker[0]
        self.assertEqual(len(c), 4)
        scale = None
        for a, b in zip(c, locked):
            if b != 0:
                self.assertEqual(a % b, 0)
                scale = a // b
                break
        self.assertIsNotNone(scale)
        self.assertEqual(c, [scale * x for x in locked])
        # c^T B = 0 exactly
        for j in range(len(modes)):
            s = sum(c[e] * B[e][j] for e in range(4))
            self.assertEqual(s, 0)

    def test_rejects_unclosed_triad(self):
        with self.assertRaises(ValueError):
            incidence_matrix([((1, 0, 0), (0, 1, 0), (1, 0, 0))])


class GaugeTests(unittest.TestCase):
    def test_translation_kills_every_convolution_phase(self):
        _, modes, B = incidence_matrix(PARALLELOGRAM)
        g = convolution_phases_vanish(B, modes)
        self.assertTrue(g["translation_in_right_kernel"])
        self.assertTrue(g["constant_gives_all_ones"])
        family = additive_gauge_family(modes)
        # ξ · k
        for vec in family[:3]:
            residual = apply_B(B, vec)
            for x in residual:
                self.assertAlmostEqual(x, 0.0, places=12)
        # constant → all-ones
        residual = apply_B(B, family[3])
        for x in residual:
            self.assertAlmostEqual(x, 1.0, places=12)

    def test_star_translation_gauge_also_vanishes(self):
        _, modes, B = incidence_matrix(STAR_WITNESS)
        g = convolution_phases_vanish(B, modes)
        self.assertTrue(g["translation_in_right_kernel"])


class HolonomyTests(unittest.TestCase):
    def test_star_is_phase_unfrustrated(self):
        rep = star_report()
        test = rep["loop_gauge"]
        self.assertTrue(test["tree_combinatorial"])
        self.assertEqual(test["dim_ker_BT"], 0)
        self.assertTrue(test["phase_holonomy_vanishes"])
        self.assertEqual(test["Gamma_cyc_phase"], 1)
        self.assertIn("PASS", test["loop_gauge"])

    def test_zero_chi_has_vanishing_holonomy_on_the_loop(self):
        # Independently optimal b = 0 (χ = 0, Φ^* = 0) is always realizable.
        _, _, B = incidence_matrix(PARALLELOGRAM)
        ker = left_kernel_basis(B)
        self.assertTrue(ker)
        for c in ker:
            self.assertAlmostEqual(holonomy(c, [0.0, 0.0, 0.0, 0.0]), 0.0, places=12)

    def test_artificial_chi_is_detected(self):
        c = locked_cycle_vector()
        # b = (π/2, 0, 0, 0) has Ω = π/2 ≠ 0.
        om = holonomy(c, [0.5 * math.pi, 0.0, 0.0, 0.0])
        self.assertAlmostEqual(om, 0.5 * math.pi, places=12)

    def test_helical_parallelogram_is_a_certified_comparison(self):
        rep = parallelogram_report()
        test = rep["loop_gauge"]
        self.assertFalse(test["tree_combinatorial"])
        self.assertEqual(test["dim_ker_BT"], 1)
        self.assertTrue(test["gauge"]["translation_in_right_kernel"])
        # Geometric coupling phases produce a frame-invariant 2π/3 holonomy.
        self.assertAlmostEqual(rep["Omega_locked"], 2.0 * math.pi / 3.0, places=12)
        self.assertFalse(test["phase_holonomy_vanishes"])
        self.assertIsNone(test["Gamma_cyc_phase"])
        self.assertTrue(rep["frames"]["Omega_frame_invariant"])
        cert = rep["certified"]
        self.assertGreater(cert["tree"], 0.0)
        self.assertLess(cert["loop"] + 1e-12, cert["tree"])
        self.assertAlmostEqual(cert["Gamma_cyc"], cert["loop"] / cert["tree"], places=12)
        self.assertGreater(cert["Gamma_cyc"], 0.8)
        self.assertLess(cert["Gamma_cyc"], 1.0)

    def test_constrained_max_recovers_the_tree_when_omega_vanishes(self):
        out = constrained_cosine_max([1.0, 2.0, 3.0, 4.0], [1, -1, 1, -1], 0.0)
        self.assertAlmostEqual(out["loop"], 10.0, places=10)
        self.assertAlmostEqual(out["Gamma_cyc"], 1.0, places=12)

    def test_loop_gauge_test_on_parallelogram_runs(self):
        test = loop_gauge_test(PARALLELOGRAM)
        self.assertEqual(test["n_triads"], 4)
        self.assertEqual(test["n_modes"], 6)
        self.assertIn("loop topology", test["gauge"]["boxed"])


if __name__ == "__main__":
    unittest.main()
