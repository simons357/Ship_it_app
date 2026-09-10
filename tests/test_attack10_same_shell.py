"""Attack 10: same-shell coherent packet. Not a proof."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.stokes_moments import (  # noqa: E402
    integer_shell,
    probe,
    same_shell_packet_field,
)


class Attack10Tests(unittest.TestCase):
    def test_shell_two_has_twelve_keys(self):
        self.assertEqual(len(integer_shell(2)), 12)

    def test_same_shell_has_two_eigenvalues(self):
        _f, meta = same_shell_packet_field(2)
        self.assertEqual(meta["n_shells"], 2)
        self.assertIn(2, meta["shells"])
        self.assertNotEqual(meta["T"], 2)

    def test_energy_normalized(self):
        f, _meta = same_shell_packet_field(2)
        r = probe(f)
        self.assertAlmostEqual(r.E, 1.0, places=8)
        self.assertGreater(r.Ds, 0.0)

    def test_not_two_keys(self):
        _f, meta = same_shell_packet_field(2)
        self.assertGreater(meta["n_modes"], 4)
        self.assertGreater(meta["n_pairs"], 1)

    def test_small_m_keeps_pairs(self):
        """Edge-preserving subset: m=8 on N=14 is still a two-shell packet."""
        f, meta = same_shell_packet_field(14, m=8)
        self.assertGreater(meta["n_pairs"], 0)
        self.assertGreater(meta["n_modes"], 0)
        self.assertEqual(meta["n_shells"], 2)
        self.assertIn(14, meta["shells"])
        self.assertNotEqual(meta["T"], 14)
        r = probe(f)
        self.assertAlmostEqual(r.E, 1.0, places=8)
        self.assertGreater(r.Ds, 0.0)

    def test_ds_not_ap_width(self):
        """At fixed N, Ds is a shell gap: it does not track m the way an AP does."""
        f6, m6 = same_shell_packet_field(14, m=8)
        f12, m12 = same_shell_packet_field(14, m=24)
        r6 = probe(f6)
        r12 = probe(f12)
        self.assertGreater(m6["n_pairs"], 0)
        self.assertGreater(m12["n_pairs"], 0)
        self.assertGreater(r6.Ds, 0.0)
        self.assertGreater(r12.Ds, 0.0)
        ratio = max(r6.Ds, r12.Ds) / min(r6.Ds, r12.Ds)
        self.assertLess(ratio, 20.0)
        self.assertEqual(m6["N"], m12["N"])
        self.assertEqual(m6["T"], m12["T"])
        self.assertEqual(m6["n_shells"], 2)
        self.assertEqual(m12["n_shells"], 2)


if __name__ == "__main__":
    unittest.main()
