"""H1 on one cylinder: J and thinness. Not a proof."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np

from h1_one_cylinder import (  # noqa: E402
    burgers_field,
    score_abc,
    score_burgers,
    score_gaussian,
    sweep,
    lemmas,
)


class H1OneCylinderTests(unittest.TestCase):
    def test_abc_is_beltrami(self):
        row = score_abc(24, 1.0)
        self.assertLess(row["beltrami_l2"], 1e-8)

    def test_abc_j_tracks_amplitude(self):
        a = score_abc(24, 1.0)
        b = score_abc(24, 2.0)
        self.assertGreater(a["J_ec"], 0.0)
        ratio = b["J_ec"] / a["J_ec"]
        self.assertAlmostEqual(ratio, 2.0, delta=0.2)
        self.assertAlmostEqual(
            b["stretch_inf_plus"] / a["stretch_inf_plus"], 2.0, delta=0.2
        )
        self.assertLess(b["J_over_X"], a["J_over_X"])

    def test_burgers_aligned_stretch_is_gamma(self):
        gamma = 1.0
        row = score_burgers(24, 2.0, gamma=gamma, nu=0.1, box=3.0)
        self.assertLess(row["J_ec"], 1e-4)
        self.assertAlmostEqual(row["stretch_inf_plus"], gamma, delta=0.15)
        self.assertAlmostEqual(row["waiting_rho2_over_nu"], 4.0, delta=1e-9)

    def test_burgers_field_omega_is_axial(self):
        _u, _v, _w, ox, oy, oz, *_rest = burgers_field(16, 1.0, 1.0, 0.1, 3.0)
        self.assertLess(float(np.max(np.abs(ox))), 1e-15)
        self.assertLess(float(np.max(np.abs(oy))), 1e-15)
        self.assertGreater(float(np.max(oz)), 0.0)

    def test_gaussian_pair_thinness_finite(self):
        row = score_gaussian(32, 4.0, 0.40)
        self.assertGreater(row["E_tube"], 0.0)
        self.assertGreater(row["thinness_ratio_tube"], 0.05)
        self.assertLess(row["thinness_ratio_tube"], 80.0)
        self.assertLess(row["stretch_inf_plus"], 0.5)

    def test_lemmas_do_not_close_h1(self):
        payload = sweep(n=24, quick=True)
        rows = {r["name"]: r for r in lemmas(payload)}
        self.assertEqual(rows["H1t_abc_stretch_tracks_amp"]["verdict"], "fail")
        self.assertEqual(rows["H1t_burgers_not_h1"]["verdict"], "fail")
        self.assertEqual(rows["H1t_not_a_close"]["verdict"], "fail")
        self.assertEqual(rows["H1t_not_gcd"]["verdict"], "fail")
        self.assertEqual(rows["H1t_ring_not_proved"]["verdict"], "fail")
        self.assertEqual(rows["H1t_abc_j_tracks_amp"]["verdict"], "pass")


if __name__ == "__main__":
    unittest.main()
