"""Attack 6: scale law for Lemma★ ratios. Not a proof."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.attack6_scale_law import best_phase_on_scaled_triad, coherent_fan  # noqa: E402
from ns_attacks.stokes_moments import high_triad_field, probe  # noqa: E402
import numpy as np


class Attack6Tests(unittest.TestCase):
    def test_probe_finite_on_unit_triad(self):
        r = probe(high_triad_field(amp=1.0), label="unit")
        self.assertTrue(np.isfinite(r.ratio_preyoung))
        self.assertTrue(np.isfinite(r.ratio_cstar))
        self.assertGreater(r.X, 0.0)

    def test_scale_s1_runs(self):
        rng = np.random.Generator(np.random.PCG64(0))
        row = best_phase_on_scaled_triad(1, rng, n_phase=2)
        self.assertIsNotNone(row)
        self.assertEqual(row["s"], 1)
        self.assertGreater(row["abs_pre"], 0.0)

    def test_preyoung_grows_like_s_cstar_does_not(self):
        r1 = probe(high_triad_field(amp=1.0, k1=(4, 2, 1), k2=(-3, 1, 1)))
        r2 = probe(high_triad_field(amp=1.0, k1=(8, 4, 2), k2=(-6, 2, 2)))
        self.assertGreater(abs(r2.ratio_preyoung), 1.5 * abs(r1.ratio_preyoung))
        self.assertLess(
            abs(abs(r2.ratio_cstar) - abs(r1.ratio_cstar)),
            0.01,
        )

    def test_fan_two_pairs_finite(self):
        row = coherent_fan(2)
        self.assertGreaterEqual(row["n_pairs"], 1)
        self.assertIsNotNone(row["abs_pre"])


if __name__ == "__main__":
    unittest.main()
