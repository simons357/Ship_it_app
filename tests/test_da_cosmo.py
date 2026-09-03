"""Official Cosmo 16 catalog smoke tests."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_cosmo import COSMO_SIXTEEN, FATE_KEYS, run  # noqa: E402


class DaCosmoTests(unittest.TestCase):
    def test_official_sixteen_named_and_produce_fails(self):
        tmp = Path(tempfile.mkdtemp()) / "da_cosmo_test.json"
        payload = run(out=tmp)
        self.assertTrue(payload["meta"]["cosmos_list_found"])
        self.assertFalse(payload["meta"]["cosmos_core_equation_public"])
        self.assertFalse(payload["meta"]["this_list_is_reconstructed_R"])
        self.assertEqual(len(payload["sixteen"]), 16)
        self.assertEqual(len(COSMO_SIXTEEN), 16)
        self.assertEqual(payload["sixteen"][-1]["name"], "Σ m_ν")
        self.assertTrue(payload["produce_all_fail"])
        self.assertEqual(payload["nature4"]["verdict"], "fail")
        self.assertEqual(payload["gauge3"]["verdict"], "fail")
        self.assertFalse(payload["collapsed"])
        by_name = {a["name"]: a for a in payload["app_level"]}
        self.assertEqual(by_name["DA_predicts_16_of_16"]["verdict"], "fail")
        self.assertEqual(by_name["manifold_lambda_ratio_is_cos_theta_W"]["verdict"], "fail")
        self.assertEqual(by_name["public_producing_map_F"]["verdict"], "fail")

    def test_each_slot_has_the_same_five_questions(self):
        for row in COSMO_SIXTEEN:
            keys = [h["name"] for h in row["hand"]]
            self.assertEqual(keys, list(FATE_KEYS), row["name"])
            prod = next(h for h in row["hand"] if h["name"] == "produce")
            self.assertEqual(prod["verdict"], "fail", row["name"])
            self.assertFalse(row["public_F"])

    def test_koide_and_planck_are_clusters_not_extra_hits(self):
        tmp = Path(tempfile.mkdtemp()) / "da_cosmo_test.json"
        payload = run(out=tmp)
        groups = payload["clusters"]["groups"]
        self.assertEqual(len(groups["koide"]), 3)
        self.assertEqual(len(groups["planck"]), 2)
        self.assertEqual(payload["clusters"]["n_clusters"], 13)
        self.assertLess(payload["clusters"]["n_clusters"], payload["clusters"]["n_slots"])
        self.assertTrue(payload["overlap_with_reconstructed_16"]["do_not_glue"])
        self.assertFalse(payload["split_55"]["names_extracted"])


if __name__ == "__main__":
    unittest.main()
