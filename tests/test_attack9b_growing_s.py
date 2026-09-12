"""9B growing-s: combinatorial room + field campaign. Not C0. ★ open."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.attack9b_growing_s import (  # noqa: E402
    close_shell,
    combinatorial_census,
    field_campaign,
    high_rep_pos_modes,
    loglog_slope,
    pair_census,
    plane_pos_modes,
    run,
)
from ns_attacks.attack9b_exact_shell_K import shells_up_to  # noqa: E402

DOC = ROOT / "docs" / "LEMMA-STAR-9B-GROWING.md"
COUNTING = ROOT / "docs" / "LEMMA-STAR-9B-COUNTING.md"
SPEC_9D = ROOT / "docs" / "math" / "ns_attacks" / "ATTACK_9D_THETA_M2_LOCKED_PHASE.md"
SCRIPT = ROOT / "scripts" / "ns_attacks" / "attack9b_growing_s.py"


class GrowingSTests(unittest.TestCase):
    def test_doc_locks_the_lane(self):
        text = DOC.read_text()
        self.assertIn("9B", text)
        self.assertIn("not a 9D object", text)
        self.assertIn("NS not solved", text)
        self.assertIn(r"not \(C_0\)", text)
        self.assertIn("attack9b_growing_s.py", text)
        self.assertIn("no seated exponent", text)
        self.assertIn("0.631", text)
        self.assertIn("36895", text)
        self.assertNotIn("NS is solved", text)
        self.assertTrue(SCRIPT.is_file())
        counting = COUNTING.read_text()
        self.assertIn("LEMMA-STAR-9B-GROWING.md", counting)
        spec = SPEC_9D.read_text()
        self.assertIn("attack9b_growing_s.py", spec)

    def test_pairs_per_output_at_most_m(self):
        pos = [(2, 0, 0), (0, 2, 0), (0, 0, 2)]
        rec = pair_census(close_shell(pos), 8)
        self.assertGreater(rec["s_geom"], 0)
        self.assertTrue(rec["pairs_le_m"])
        self.assertLessEqual(rec["max_rep"], rec["m"])
        self.assertGreater(rec["K_cs_ceiling"], 0.0)

    def test_plane_and_highrep_are_subsets(self):
        pos = shells_up_to(6)[5]
        plane = plane_pos_modes(pos)
        self.assertTrue(all(k[0] == 0 or k[1] == 0 or k[2] == 0 for k in plane))
        greedy = high_rep_pos_modes(pos, 10, 4)
        self.assertGreaterEqual(len(greedy), 2)
        self.assertLessEqual(len(greedy), 4)
        self.assertTrue(set(greedy).issubset(set(pos)))

    def test_loglog_slope_known(self):
        # y = 3 x^2 → slope 2
        pairs = [(2.0, 12.0), (4.0, 48.0), (8.0, 192.0)]
        sl = loglog_slope(pairs)
        self.assertIsNotNone(sl)
        self.assertAlmostEqual(sl, 2.0, places=6)
        self.assertIsNone(loglog_slope([(1.0, 1.0)]))

    def test_tiny_campaign_keeps_inequalities(self):
        rng = np.random.default_rng(1390)
        fields = field_campaign(
            rng,
            kmax=4,
            n_random=1,
            n_opt_trials=2,
            n_opt_refine=1,
            m_list=(2,),
        )
        self.assertGreater(fields["n_fields"], 0)
        self.assertEqual(fields["n_fail_pairs_le_m"], 0)
        self.assertEqual(fields["n_fail_cs"], 0)
        self.assertEqual(fields["n_fail_K_le_16s"], 0)
        self.assertIs(fields["ns_solved"], False)
        self.assertEqual(fields["lemma_star"], "OPEN")
        self.assertTrue(fields["verdict"].startswith("GROWING_S_SAMPLES"))
        self.assertLess(fields["max_K"], 16.0 * max(fields["max_s"], 1))

    def test_run_tiny_and_census(self):
        summary = run(
            seed=1390,
            kmax_census=6,
            kmax_fields=3,
            n_random=1,
            n_opt_trials=0,
            n_opt_refine=0,
            m_list=(2,),
        )
        self.assertEqual(summary["attack"], "9B-growing-s")
        self.assertIs(summary["ns_solved"], False)
        self.assertEqual(summary["lemma_star"], "OPEN")
        self.assertEqual(summary["census"]["n_fail_pairs_le_m"], 0)
        self.assertGreater(summary["census"]["n_pairs_with_sums"], 0)
        self.assertTrue(summary["verdict"].startswith("GROWING_S"))

    def test_census_cs_ceiling_tracks_s(self):
        c = combinatorial_census(8)
        self.assertEqual(c["n_fail_pairs_le_m"], 0)
        self.assertGreater(c["max_s_geom"], 0)
        self.assertAlmostEqual(c["max_cs_ceiling"], 16.0 * c["max_s_geom"], places=8)
        self.assertIn("alpha", c["max_rep_at"])
        self.assertLessEqual(c["max_rep_over_m"], 1.0)

    def test_results_json_is_a_sample_not_a_kill(self):
        import json

        path = ROOT / "results" / "attack9b_growing_s" / "attack9b_growing_s.json"
        self.assertTrue(path.is_file())
        data = json.loads(path.read_text())
        self.assertEqual(data["attack"], "9B-growing-s")
        self.assertIs(data["ns_solved"], False)
        self.assertEqual(data["lemma_star"], "OPEN")
        self.assertEqual(data["kill_lane"], "LIVE")
        self.assertTrue(data["verdict"].startswith("GROWING_S_SAMPLES"))
        self.assertEqual(data["census"]["n_fail_pairs_le_m"], 0)
        self.assertEqual(data["census"]["n_pairs_with_sums"], 36895)
        self.assertEqual(data["fields"]["n_fail_K_le_16s"], 0)
        self.assertLess(data["fields"]["max_K"], 1.0)
        self.assertGreater(data["fields"]["max_K"], 0.5)
        self.assertLess(data["fields"]["loglog_slope_K_vs_s"], 0.0)
        self.assertLess(data["fields"]["loglog_slope_K_vs_m"], 0.0)


if __name__ == "__main__":
    unittest.main()
