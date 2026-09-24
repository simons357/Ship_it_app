"""SAG-6 equal-input lattice circle. Not a proof of depletion."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.sag6_lattice_circle import (  # noqa: E402
    ansatz_constant,
    ansatz_hemisphere,
    ansatz_radial,
    ansatz_tangential,
    circle_geometry,
    hemisphere_lower_bound,
    lattice_circle,
    probe_circle,
    ratios,
)


class Sag6Tests(unittest.TestCase):
    def test_eight_point_geometry(self):
        geo = circle_geometry((0, 0, 2), 6)
        self.assertEqual(geo["N"], 8)
        self.assertEqual(geo["beta"], 4)
        self.assertAlmostEqual(geo["r2"], 5.0, places=12)
        self.assertTrue(geo["radii_ok"])
        self.assertTrue(geo["pairs_close"])
        self.assertAlmostEqual(geo["kperp"] ** 2, 4.0 * (1.0 - 4.0 / 24.0), places=12)

    def test_p_dot_k_is_half_beta(self):
        for k, alpha in (((0, 0, 2), 6), ((2, 2, 2), 17), ((0, 0, 66), 2194)):
            target = (k[0] * k[0] + k[1] * k[1] + k[2] * k[2]) // 2
            for p in lattice_circle(k, alpha):
                self.assertEqual(p[0] * k[0] + p[1] * k[1] + p[2] * k[2], target)

    def test_naive_alignments_cancel(self):
        k, alpha = (0, 0, 2), 6
        pts = lattice_circle(k, alpha)
        for builder in (ansatz_constant, ansatz_radial, ansatz_tangential):
            row = ratios(k, alpha, builder(k, pts))
            self.assertLess(row["sigma"], 1e-9)

    def test_naive_alignments_cancel_on_tilt(self):
        k, alpha = (2, 2, 2), 17
        pts = lattice_circle(k, alpha)
        self.assertGreaterEqual(len(pts), 8)
        for builder in (ansatz_constant, ansatz_radial, ansatz_tangential):
            row = ratios(k, alpha, builder(k, pts))
            self.assertLess(row["sigma"], 1e-9)

    def test_hemisphere_beats_lower_bound_eight_point(self):
        row = probe_circle((0, 0, 2), 6)
        lb = hemisphere_lower_bound((0, 0, 2), 6, lattice_circle((0, 0, 2), 6))
        self.assertGreater(row["hemisphere_N_ratio"], lb - 1e-12)
        self.assertGreater(row["hemisphere_N_ratio"], 0.2)
        self.assertGreater(row["ansatze"]["hemisphere"]["sigma"], 1.0)

    def test_fat_circle_breaks_sqrtN(self):
        row = probe_circle((0, 0, 66), 2194)
        self.assertEqual(row["N"], 32)
        self.assertGreater(row["beta"] / row["alpha"], 1.5)
        self.assertGreater(row["hemisphere_sqrtN_ratio"], 1.0)
        self.assertGreater(
            row["hemisphere_sqrtN_ratio"],
            (1.0 / (2.0 * math.pi)) * math.sqrt(row["N"] * row["beta"] / row["alpha"]) - 1e-9,
        )

    def test_sqrtN_ratio_grows_with_populated_fat_circles(self):
        small = probe_circle((0, 0, 2), 6)
        fat = probe_circle((0, 0, 148), 11001)
        self.assertEqual(small["N"], 8)
        self.assertEqual(fat["N"], 48)
        self.assertGreater(fat["hemisphere_sqrtN_ratio"], small["hemisphere_sqrtN_ratio"] + 0.5)
        self.assertGreater(fat["hemisphere_sqrtN_ratio"], 2.0)

    def test_hemisphere_axis_y_matches_axis_z(self):
        a = probe_circle((0, 0, 2), 6)
        b = probe_circle((0, 2, 0), 6)
        self.assertEqual(a["N"], b["N"])
        self.assertAlmostEqual(a["hemisphere_N_ratio"], b["hemisphere_N_ratio"], places=6)


if __name__ == "__main__":
    unittest.main()
