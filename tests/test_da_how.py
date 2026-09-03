"""How-it-knew enumerator smoke tests."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_how import run  # noqa: E402


class DaHowTests(unittest.TestCase):
    def test_only_p1_is_possible_without_names(self):
        tmp = Path(tempfile.mkdtemp()) / "da_how_test.json"
        payload = run(out=tmp)
        by_id = {row["id"]: row for row in payload["possible"]}
        self.assertFalse(by_id["P1"]["needs_names"])
        self.assertFalse(by_id["P1"]["needs_F"])
        self.assertEqual(by_id["P3"]["verdict"], "fail")
        self.assertEqual(by_id["P4"]["verdict"], "fail")

    def test_enumerator_possible_by_count_and_robust(self):
        tmp = Path(tempfile.mkdtemp()) / "da_how_test.json"
        payload = run(out=tmp)
        enum = payload["enumerator"]
        self.assertGreater(enum["X_eligible"], enum["k_nature"])
        self.assertTrue(enum["possible_by_count"])
        self.assertFalse(payload["meta"]["cosmos_internals_found"])
        self.assertTrue(payload["meta"]["cosmos_app_list_found"])
        self.assertTrue(payload["meta"]["hand_not_capped_at_five"])
        for row in payload["drop_one_type"]:
            self.assertTrue(row["still_possible"], row["drop_type"])


if __name__ == "__main__":
    unittest.main()
