"""Track B lemma checks. Identities may pass; regularity stays open."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_lemmas import run  # noqa: E402


class TrackBLemmaTests(unittest.TestCase):
    def test_identities_pass_regularity_open(self):
        tmp = Path(tempfile.mkdtemp()) / "track_b_test.json"
        payload = run(out=tmp)
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertTrue(payload["meta"]["not_a_regularity_proof"])
        self.assertTrue(payload["meta"]["no_q1"])
        self.assertTrue(payload["meta"]["no_A_implies_B"])
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B1_t2_low_flux"]["verdict"], "pass")
        self.assertEqual(by["B1b_t2_lemma2_dropped"]["verdict"], "fail")
        self.assertEqual(by["B2_regime_cover"]["verdict"], "pass")
        self.assertEqual(by["B3_three_shell_ring"]["verdict"], "pass")
        self.assertEqual(by["B3b_ring_is_not_depletion"]["verdict"], "fail")
        self.assertEqual(by["B4_tube_hardy"]["verdict"], "pass")
        self.assertEqual(by["B4b_hardy_not_I_tube"]["verdict"], "fail")
        self.assertEqual(by["B4c_packet_hardy_tube"]["verdict"], "pass")
        self.assertEqual(by["B4d_wall_matches_off_axis"]["verdict"], "pass")
        self.assertEqual(by["B5_swirl_visc_identity"]["verdict"], "pass")
        self.assertEqual(by["B5b_tube_vs_viscosity"]["verdict"], "open")
        self.assertEqual(by["B6_energy_not_enough"]["verdict"], "fail")
        self.assertEqual(by["B_phi_not_estimate_variable"]["verdict"], "fail")
        self.assertEqual(by["B7_bony_split"]["verdict"], "pass")
        self.assertEqual(by["B7a_self_is_t2"]["verdict"], "pass")
        self.assertEqual(by["B7b_low_T_energy_class"]["verdict"], "pass")
        self.assertEqual(by["B7c_low_T_not_rho_uniform"]["verdict"], "fail")
        self.assertEqual(by["B8_occupation_clock"]["verdict"], "pass")
        self.assertEqual(by["B8a_high_jstar_short"]["verdict"], "pass")
        self.assertEqual(by["B8b_leray_not_occupation"]["verdict"], "fail")
        self.assertEqual(by["B8c_occupation_not_X_bound"]["verdict"], "open")
        self.assertEqual(by["B_regularity"]["verdict"], "open")
        self.assertLess(by["B1_t2_low_flux"]["rel_residual"], 1e-10)

    def test_no_regularity_pass_in_the_list(self):
        tmp = Path(tempfile.mkdtemp()) / "track_b_test.json"
        payload = run(out=tmp)
        for row in payload["lemmas"]:
            if "regular" in row["name"] or row["name"] == "B_regularity":
                self.assertNotEqual(row["verdict"], "pass", row["name"])


if __name__ == "__main__":
    unittest.main()
