"""Similar-triad dilation locks θ ≥ 1/2 for nonnegative Q_x."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.nonnegative_qx_dilation import report, single_triad_ratio  # noqa: E402


class TestNonnegativeDilation(unittest.TestCase):
    def test_homogeneity_degree_three_in_t(self):
        r4 = single_triad_ratio(4)
        r8 = single_triad_ratio(8)
        self.assertAlmostEqual(
            r8["C_abc"] / r4["C_abc"], 8.0, places=9
        )  # (8/4)^3
        self.assertAlmostEqual(r4["ratio_over_n"], r8["ratio_over_n"], places=9)

    def test_mean_theta_is_half(self):
        payload = report()
        self.assertAlmostEqual(payload["mean_theta_hat"], 0.5, places=9)
        self.assertTrue(payload["requires_theta_ge_half"])
        self.assertTrue(payload["cs1_holds_on_family"])
        self.assertFalse(payload["depends_on_all_radii_counting"])
        self.assertFalse(payload["theta_proved_equal_half_uniformly"])
        self.assertFalse(payload["theorem_17_proved"])

    def test_cs1_on_each_row(self):
        for n in (4, 8, 16, 32):
            row = single_triad_ratio(n)
            self.assertTrue(row["cs1_holds"])


if __name__ == "__main__":
    unittest.main()
