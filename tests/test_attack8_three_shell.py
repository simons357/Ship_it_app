"""Attack 8: three-shell closing triad. Not a proof."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.attack8_three_shell import (  # noqa: E402
    best_three_shell,
    frozen_three_shell,
    two_shell_control,
)
from ns_attacks.stokes_moments import (  # noqa: E402
    probe,
    scale_field,
    three_shell_field,
    three_shell_keys,
    two_shell_shift_field,
)


class Attack8Tests(unittest.TestCase):
    def test_triad_closes(self):
        k0, k1, k2 = three_shell_keys((6, 0, 0), (0, 1, 0))
        self.assertEqual(k1, (6, 1, 0))
        self.assertEqual(k2, (12, 1, 0))
        self.assertEqual(
            (k0[0] + k1[0], k0[1] + k1[1], k0[2] + k1[2]),
            k2,
        )

    def test_rejects_collapsed_e(self):
        with self.assertRaises(ValueError):
            three_shell_field((4, 0, 0), (0, 0, 0))

    def test_rbox_amplitude_invariant(self):
        f = three_shell_field((6, 0, 0), (0, 1, 0), amp0=1.0, amp1=0.2, amp2=0.2)
        r1 = probe(f)
        r5 = probe(scale_field(f, 5.0))
        self.assertTrue(np.isfinite(r1.ratio_box))
        self.assertAlmostEqual(r1.ratio_box, r5.ratio_box, places=8)

    def test_three_shell_can_have_nonzero_tc(self):
        rng = np.random.Generator(np.random.PCG64(0))
        row = best_three_shell((4, 0, 0), (0, 1, 0), rng, n_phase=4, amps=(0.2, 0.5))
        self.assertIsNotNone(row)
        self.assertGreater(abs(row["Tc"]), 1e-12)

    def test_two_shell_is_a_different_family(self):
        f2 = two_shell_shift_field((6, 0, 0), (0, 1, 0))
        f3 = three_shell_field((6, 0, 0), (0, 1, 0))
        self.assertEqual(len(f2), 4)  # k, -k, k+e, -(k+e)
        self.assertEqual(len(f3), 6)
        rng = np.random.Generator(np.random.PCG64(1))
        ctrl = two_shell_control((6, 0, 0), (0, 1, 0), rng, n_phase=6)
        self.assertIn("max_|Tc|", ctrl)
        self.assertEqual(ctrl["max_|Tc|"], 0.0)

    def test_frozen_dilation_is_exactly_flat(self):
        a = frozen_three_shell((2, 0, 0), (0, 2, 0))
        b = frozen_three_shell((8, 0, 0), (0, 8, 0))
        self.assertIsNotNone(a["ratio_box"])
        self.assertAlmostEqual(a["ratio_box"], b["ratio_box"], places=12)

    def test_frozen_additive_e_is_not_that_symmetry(self):
        small = frozen_three_shell((2, 0, 0), (0, 1, 0))
        large = frozen_three_shell((16, 0, 0), (0, 1, 0))
        self.assertGreater(small["ratio_box"], 5.0 * large["ratio_box"])


if __name__ == "__main__":
    unittest.main()
