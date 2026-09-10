"""Original five-lane JSON from PR 48 is on disk. ★ not proved."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.stokes_moments import (  # noqa: E402
    Ds_two_shell,
    almost_single_shell_field,
    high_triad_field,
    probe,
    scale_field,
)

COMPUTE = ROOT / "docs" / "five-lane-export" / "COMPUTE.md"
RUN = ROOT / "results" / "ns_five_lane_2026-09-10"
SHAPE = ROOT / "results" / "ns_five_lane_shape_star"
SCRIPTS = ROOT / "scripts" / "ns_attacks"


class FiveLaneComputeTests(unittest.TestCase):
    def test_compute_page_points_at_original_json(self):
        text = COMPUTE.read_text()
        self.assertIn("results/ns_five_lane_2026-09-10", text)
        self.assertIn("K0_DEAD_Cstar_SURVIVES_numeric", text)
        self.assertIn("run_all_five.py", text)
        self.assertIn("FIVE_LANES.md", text)
        self.assertIn("NS not solved", text)
        self.assertNotIn("NS is solved", text)

    def test_original_headline_verdicts(self):
        syn = json.loads((RUN / "SYNTHESIS_RUNTIME.json").read_text())
        h = syn["headline"]
        self.assertEqual(h["attack1"], "SURVIVE_numeric_NOT_proof")
        self.assertEqual(h["attack2"], "K0_DEAD_Cstar_SURVIVES_numeric")
        self.assertEqual(h["attack3"], "HH_CHANNEL_LIVE_BOTTLENECK_no_closure")
        self.assertEqual(h["attack4"], "STOKES_IDENTITIES_OK_absorption_needs_remainder")
        self.assertEqual(h["attack5"], "SURVIVE_numeric_gap_remains")
        self.assertIs(h["LemmaStar_C0_killed"], False)
        self.assertIs(syn["ns_solved"], False)
        self.assertEqual(syn["kill_lane"], "LIVE")
        self.assertEqual(syn["lemma_star"], "OPEN")
        a5 = json.loads((RUN / "attack5.json").read_text())
        self.assertEqual(a5["n_samples"], 978)
        self.assertAlmostEqual(a5["abs_ratio_preyoung_max"], 5.088092305509681, places=10)
        self.assertAlmostEqual(a5["abs_ratio_cstar_max"], 0.04064733078460401, places=12)
        shape5 = json.loads((SHAPE / "attack5.json").read_text())
        self.assertAlmostEqual(shape5["max_R_star_shape"], 0.02271065269757461, places=12)
        self.assertIs(shape5["LemmaStar_C0_killed"], False)

    def test_scripts_present(self):
        for name in (
            "run_all_five.py",
            "attack1_covariance.py",
            "attack2_triad_k0_cstar.py",
            "attack3_bony_hh_l.py",
            "attack4_stokes.py",
            "attack5_route2_kill.py",
        ):
            self.assertTrue((SCRIPTS / name).is_file(), name)

    def test_ratio_box_aliases_and_almost_shell(self):
        r = probe(high_triad_field(amp=1.0), label="triad")
        self.assertAlmostEqual(r.ratio_box, r.ratio_R_star_shape)
        self.assertAlmostEqual(r.ratio_box, r.ratio_R_star)
        self.assertGreaterEqual(r.Tc_plus, 0.0)
        import numpy as np

        rng = np.random.Generator(np.random.PCG64(0))
        f = almost_single_shell_field(rng, n_pert=2, eps=1e-3)
        p = probe(f, label="almost")
        self.assertGreater(p.E, 0.0)
        self.assertGreaterEqual(p.Ds, -1e-12)
        ds = Ds_two_shell(1.0, 4.0, 1.0, 1.0)
        self.assertGreater(ds, 0.0)

    def test_attack2_k0_still_dead_on_triad(self):
        base = high_triad_field(amp=1.0)
        r_lo = probe(scale_field(base, 0.1))
        r_hi = probe(scale_field(base, 100.0))
        self.assertGreater(abs(r_hi.ratio_k0), 10.0 * abs(r_lo.ratio_k0))
        self.assertAlmostEqual(r_lo.ratio_cstar, r_hi.ratio_cstar, places=10)


if __name__ == "__main__":
    unittest.main()
