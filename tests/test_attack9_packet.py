"""Attack 9: coherent triad packets. Not a proof."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.stokes_moments import (  # noqa: E402
    coherent_packet_field,
    hh_l_fan_field,
    probe,
    two_eigenvalue_closed_triad,
    two_shell_shift_field,
)
from ns_attacks.attack9_packet import two_key_control, two_shell_live  # noqa: E402


class Attack9Tests(unittest.TestCase):
    def test_two_keys_tc_vanishes(self):
        row = two_key_control()
        self.assertEqual(row["Tc"], 0.0)

    def test_two_shells_can_be_live(self):
        rng = np.random.Generator(np.random.PCG64(2))
        row = two_shell_live(rng, n_phase=8)
        self.assertGreater(abs(row["Tc"]), 1e-10)

    def test_example_keys_are_two_shells(self):
        p, q, r = (1, 1, 0), (1, -1, 0), (2, 0, 0)
        self.assertEqual(
            (p[0] + q[0], p[1] + q[1], p[2] + q[2]),
            r,
        )
        self.assertEqual(p[0] ** 2 + p[1] ** 2 + p[2] ** 2, 2)
        self.assertEqual(q[0] ** 2 + q[1] ** 2 + q[2] ** 2, 2)
        self.assertEqual(r[0] ** 2 + r[1] ** 2 + r[2] ** 2, 4)

    def test_packet_m2_finite(self):
        f = coherent_packet_field(2)
        r = probe(f)
        self.assertGreater(r.E, 0.0)
        self.assertAlmostEqual(r.E, 1.0, places=8)

    def test_fan_populates_low_mode(self):
        rng = np.random.Generator(np.random.PCG64(0))
        f = hh_l_fan_field(3, rng=rng, randomize=True)
        self.assertIn((2, 0, 0), f)
        r = probe(f)
        self.assertGreater(r.E, 0.0)


if __name__ == "__main__":
    unittest.main()
