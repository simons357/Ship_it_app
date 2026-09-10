"""Attack 11: adjacent lattice spheres. Not a proof."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.stokes_moments import (  # noqa: E402
    adjacent_sphere_landings,
    adjacent_spheres_field,
    probe,
)


class Attack11Tests(unittest.TestCase):
    def test_n9_has_forty_eight_landings(self):
        _A, _B, pairs = adjacent_sphere_landings(9, 1)
        self.assertEqual(len(pairs), 48)

    def test_n89_sizes_and_landings(self):
        A, B, pairs = adjacent_sphere_landings(89, 1)
        self.assertEqual(len(A), 144)
        self.assertEqual(len(B), 120)
        self.assertEqual(len(pairs), 288)

    def test_d2_no_landings_on_tested_range(self):
        for n in (9, 17, 41, 89):
            _A, _B, pairs = adjacent_sphere_landings(n, 2)
            self.assertEqual(len(pairs), 0, msg=f"n={n}")

    def test_energy_normalized_two_shells(self):
        f, meta = adjacent_spheres_field(9, 1)
        self.assertEqual(meta["n_shells"], 2)
        self.assertEqual(meta["shells"], [9, 10])
        r = probe(f)
        self.assertAlmostEqual(r.E, 1.0, places=8)
        self.assertGreater(r.Ds, 0.0)

    def test_landings_not_quadratic_in_m(self):
        """Natural ensemble: closures track m, not m^2."""
        rows = []
        for n in (9, 41, 89):
            A, B, pairs = adjacent_sphere_landings(n, 1)
            m = len(A) + len(B)
            rows.append((m, len(pairs)))
        m0, p0 = rows[0]
        m1, p1 = rows[-1]
        lin = (p1 / m1) / (p0 / m0)
        quad = (p1 / (m1 ** 2)) / (p0 / (m0 ** 2))
        self.assertLess(abs(lin - 1.0), 2.0)
        self.assertLess(quad, 0.5)


if __name__ == "__main__":
    unittest.main()
