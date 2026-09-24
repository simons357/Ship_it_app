"""SAG-5 smallest hypergraphs. Not a proof."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.sag5_rho2 import (  # noqa: E402
    H2_IN,
    H2_OUT,
    H2_ROLE,
    H3_IN,
    coupling_map_rank,
    independent_denom,
    one_triangle_max,
    optimize_rho,
    rho2_in_exact,
    rho2_out_exact,
    rho3_in_exact,
)


class Sag5Tests(unittest.TestCase):
    def test_triangles_close(self):
        for family in (H2_IN, H2_OUT, H2_ROLE, H3_IN):
            for p, q, k in family:
                self.assertEqual(
                    (p[0] + q[0], p[1] + q[1], p[2] + q[2]),
                    k,
                )

    def test_rank_two_free_three_not(self):
        self.assertEqual(
            coupling_map_rank((2, 0, 0), [(2, 2, 0), (2, 0, 2)]),
            2,
        )
        self.assertEqual(
            coupling_map_rank((2, 0, 0), [(2, 2, 0), (2, 0, 2), (2, 2, 2)]),
            2,
        )
        self.assertLess(
            coupling_map_rank((2, 0, 0), [(2, 2, 0), (2, 0, 2), (2, 2, 2)]),
            3,
        )

    def test_one_triangle_max_is_kperp(self):
        self.assertAlmostEqual(one_triangle_max(H2_IN[0]), 2.0, places=12)
        self.assertAlmostEqual(one_triangle_max(H2_IN[1]), 2.0, places=12)
        self.assertAlmostEqual(independent_denom(H2_IN), 4.0, places=12)
        self.assertAlmostEqual(independent_denom(H2_OUT), 4.0, places=12)

    def test_stamped_two_vector_formula(self):
        from ns_attacks.sag5_rho2 import rho2_two_vector

        self.assertAlmostEqual(rho2_two_vector(1.0, 1.0, 0.0), 1.0 / math.sqrt(2.0), places=12)
        self.assertAlmostEqual(rho2_two_vector(3.0, 4.0, 1.0), 1.0, places=12)
        self.assertAlmostEqual(rho2_two_vector(1.0, 1.0, 1.0), 1.0, places=12)

    def test_named_exact_ratios(self):
        self.assertAlmostEqual(rho2_in_exact(), 1.0 / math.sqrt(2.0), places=12)
        self.assertAlmostEqual(rho2_out_exact(), 1.0 / math.sqrt(2.0), places=12)
        self.assertAlmostEqual(rho3_in_exact(), 2.0 * (math.sqrt(2.0) - 1.0), places=12)
        self.assertLess(rho2_in_exact(), 1.0)
        self.assertGreater(rho2_in_exact(), 0.0)

    def test_optimizer_recovers_h2_in(self):
        rng = np.random.Generator(np.random.PCG64(0))
        row = optimize_rho(H2_IN, rng, n_grid=20)
        self.assertAlmostEqual(row["rho"], rho2_in_exact(), places=6)
        self.assertEqual(row["kind"], "shared-input reduced")

    def test_optimizer_recovers_h2_out(self):
        rng = np.random.Generator(np.random.PCG64(3))
        row = optimize_rho(H2_OUT, rng, n_grid=20)
        self.assertAlmostEqual(row["rho"], rho2_out_exact(), places=6)
        self.assertEqual(row["kind"], "shared-output reduced")

    def test_optimizer_recovers_h3_in(self):
        rng = np.random.Generator(np.random.PCG64(1))
        row = optimize_rho(H3_IN, rng, n_grid=20)
        self.assertAlmostEqual(row["rho"], rho3_in_exact(), places=6)
        self.assertEqual(row["kind"], "shared-input reduced")

    def test_h2_role_is_a_defect(self):
        rng = np.random.Generator(np.random.PCG64(2))
        row = optimize_rho(H2_ROLE, rng, n_grid=22)
        self.assertEqual(row["kind"], "role-conflict reduced")
        self.assertGreater(row["denom"], 0.0)
        self.assertGreater(row["rho"], 0.0)
        self.assertLess(row["rho"], 1.0 - 1e-6)


if __name__ == "__main__":
    unittest.main()
