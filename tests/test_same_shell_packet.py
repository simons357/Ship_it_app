#!/usr/bin/env python3
"""Combinatorial checks for the same-shell packet probe.

Does not claim a triadic bound or Navier–Stokes regularity.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from same_shell_packet_probe import (  # noqa: E402
    lattice_sphere,
    probe_pair,
    two_shell_Ds,
)


class TestLatticeSpheres(unittest.TestCase):
    def test_user_key_counts(self):
        self.assertEqual(len(lattice_sphere(9)), 30)
        self.assertEqual(len(lattice_sphere(10)), 24)
        self.assertEqual(len(lattice_sphere(89)), 144)
        self.assertEqual(len(lattice_sphere(90)), 120)

    def test_n9_d1_has_48_mixed_closures(self):
        row = probe_pair(9, 1)
        self.assertEqual(row["r3_n"], 30)
        self.assertEqual(row["r3_n_plus_d"], 24)
        self.assertEqual(row["mixed_closures_n_n_np"], 48)

    def test_n89_d1_has_288_mixed_closures(self):
        row = probe_pair(89, 1)
        self.assertEqual(row["r3_n"], 144)
        self.assertEqual(row["r3_n_plus_d"], 120)
        self.assertEqual(row["m_keys"], 264)
        self.assertEqual(row["mixed_closures_n_n_np"], 288)

    def test_closures_not_quadratic_in_m(self):
        small = probe_pair(9, 1)
        large = probe_pair(89, 1)
        m_ratio = large["m_keys"] / small["m_keys"]
        c_ratio = large["mixed_closures_n_n_np"] / small["mixed_closures_n_n_np"]
        self.assertLess(c_ratio, m_ratio * m_ratio * 0.5)
        self.assertGreater(c_ratio, 0.5 * m_ratio)

    def test_d2_no_mixed_landings_on_reported_shells(self):
        for n in (9, 17, 25, 41, 49, 89):
            self.assertEqual(probe_pair(n, 2)["mixed_closures_n_n_np"], 0, n)

    def test_d3_sporadic(self):
        hits = {n: probe_pair(n, 3)["mixed_closures_n_n_np"] for n in (9, 17, 25, 41, 49, 89)}
        self.assertEqual(hits[9], 24)
        self.assertEqual(hits[17], 0)
        self.assertEqual(hits[89], 0)
        self.assertGreater(hits[41], 0)

    def test_Ds_is_theta_n_for_fixed_gap(self):
        small = two_shell_Ds(9, 1)
        large = two_shell_Ds(89, 1)
        self.assertGreater(small["D_s"], 0.0)
        ratio = large["D_s"] / small["D_s"]
        n_ratio = 89 / 9
        self.assertLess(abs(ratio / n_ratio - 1.0), 0.2)


if __name__ == "__main__":
    unittest.main()
