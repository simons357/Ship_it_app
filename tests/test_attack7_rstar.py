"""Boxed ratio R★: exact reduction of Lemma★. Not a proof."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.attack7_rstar import unishell_field  # noqa: E402
from ns_attacks.stokes_moments import high_triad_field, probe, scale_field  # noqa: E402


class RstarTests(unittest.TestCase):
    def test_unishell_tc_vanishes_with_ds(self):
        uni = unishell_field()
        self.assertLess(abs(uni["Ds"]), 1e-10)
        self.assertLess(abs(uni["Tc"]), 1e-8)

    def test_rbox_amplitude_invariant(self):
        f = high_triad_field(amp=1.0)
        r1 = probe(f)
        r5 = probe(scale_field(f, 5.0))
        self.assertTrue(np.isfinite(r1.ratio_box))
        self.assertAlmostEqual(r1.ratio_box, r5.ratio_box, places=8)

    def test_rbox_finite_on_triad(self):
        r = probe(high_triad_field(amp=1.0))
        self.assertTrue(np.isfinite(r.ratio_box))
        self.assertGreaterEqual(r.ratio_box, 0.0)


if __name__ == "__main__":
    unittest.main()
