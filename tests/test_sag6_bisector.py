"""SAG-6 bisector stack. Not a decay theorem."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.sag6_bisector import (  # noqa: E402
    enumerate_bisector,
    incidences,
    scan,
    stack_rho,
)


class Sag6BisectorTests(unittest.TestCase):
    def test_records_keep_geometry(self):
        k = (0, 0, 2)
        rows = enumerate_bisector(k, 4)
        self.assertGreater(len(rows), 0)
        for row in rows:
            r = row["r"]
            mr = row["minus_r"]
            p, q = row["p"], row["q"]
            self.assertEqual(mr, (-r[0], -r[1], -r[2]))
            self.assertEqual(
                (p[0] + q[0], p[1] + q[1], p[2] + q[2]),
                k,
            )
            self.assertEqual(p[0] * p[0] + p[1] * p[1] + p[2] * p[2], row["alpha"])
            self.assertEqual(r[0] * k[0] + r[1] * k[1] + r[2] * k[2], 0)
            self.assertIn("kperp_hat", row)
            self.assertIn("triangle_normal", row)
            self.assertIn("circle_id", row)

    def test_r_identified_once(self):
        rows = enumerate_bisector((0, 0, 2), 5)
        keys = [tuple(sorted((row["r"], row["minus_r"]))) for row in rows]
        self.assertEqual(len(keys), len(set(keys)))

    def test_input_modes_disjoint_across_circles(self):
        for k, rmax in (((0, 0, 2), 8), ((2, 2, 0), 6)):
            inc = incidences(enumerate_bisector(k, rmax))
            self.assertEqual(inc["n_cross_circle_input_modes"], 0)
            self.assertEqual(inc["shared_input_modes"], {})

    def test_rho_is_one_on_the_coherent_family(self):
        row = stack_rho((0, 0, 2), 8)
        self.assertTrue(row["mode_disjoint"])
        self.assertAlmostEqual(row["rho_adversary"]["rho"], 1.0, places=9)
        self.assertAlmostEqual(row["rho_common_axis"]["rho"], 1.0, places=9)
        self.assertGreater(row["incidences"]["n_circles"], 8)

    def test_rho_does_not_decay_with_cutoff(self):
        out = scan((0, 0, 2), [2, 6, 10])
        rhos = out["rho_adversary_list"]
        self.assertEqual(len(rhos), 3)
        for rho in rhos:
            self.assertGreater(rho, 0.99)
        self.assertIn("COHERENT FAMILY", out["verdict_6D"])

    def test_tilted_k_also_aligns(self):
        row = stack_rho((2, 2, 0), 6)
        self.assertTrue(row["mode_disjoint"])
        self.assertAlmostEqual(row["rho_adversary"]["rho"], 1.0, places=9)


if __name__ == "__main__":
    unittest.main()
