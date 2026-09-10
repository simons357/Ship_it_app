"""Attack 12: HH→L fan on a high sphere. Not a proof."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.stokes_moments import (  # noqa: E402
    hh_l_one_key_field,
    hh_l_sphere_pairs,
    hh_l_whole_shell_field,
    probe,
)


class Attack12Tests(unittest.TestCase):
    def test_one_key_pair_counts_are_small(self):
        k = (2, 0, 0)
        counts = [len(hh_l_sphere_pairs(k, a)) for a in (5, 9, 10, 17, 41)]
        self.assertTrue(all(2 <= c <= 12 for c in counts if c))
        self.assertEqual(len(hh_l_sphere_pairs(k, 5)), 2)

    def test_one_key_energy_and_two_shells(self):
        f, meta = hh_l_one_key_field((2, 0, 0), 5)
        self.assertGreater(meta["n_pairs"], 0)
        r = probe(f)
        self.assertAlmostEqual(r.E, 1.0, places=8)
        self.assertGreater(r.Ds, 0.0)
        self.assertEqual(meta["beta"], 4)
        self.assertEqual(meta["alpha"], 5)

    def test_whole_shell_ninety_six_high_at_41(self):
        _f, meta = hh_l_whole_shell_field(2, 41)
        self.assertEqual(meta["n_high"], 96)
        self.assertGreaterEqual(meta["n_pairs"], 48)
        self.assertLessEqual(meta["n_pairs"], 144)

    def test_whole_shell_normalized(self):
        f, meta = hh_l_whole_shell_field(2, 9)
        self.assertGreater(meta["n_pairs"], 0)
        r = probe(f)
        self.assertAlmostEqual(r.E, 1.0, places=8)


if __name__ == "__main__":
    unittest.main()
