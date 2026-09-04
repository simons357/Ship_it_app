"""Regularity leftover as an a priori: leftover knobs do not decide X."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_object import run  # noqa: E402


class TrackBObjectTests(unittest.TestCase):
    def test_leftover_knobs_do_not_decide_regularity(self):
        tmp = Path(tempfile.mkdtemp()) / "object_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B36_object_readable"]["verdict"], "pass")
        self.assertEqual(by["B36a_object_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B36b_object_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B36c_object_not_ns"]["verdict"], "fail")
        self.assertEqual(by["B36d_object_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B36e_object_not_regularity"]["verdict"], "fail")
        self.assertEqual(by["B36f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertFalse(payload["meta"]["spawned_n64"])
        self.assertGreater(by["B36_object_readable"]["T_long"], by["B36_object_readable"]["t_room"])
        self.assertLess(by["B36_object_readable"]["c_inc_max"], by["B36_object_readable"]["c_save"])
        self.assertIn("B35e", payload["next_da_move"])
        self.assertIn("B34e", payload["next_da_move"])
        self.assertIn("B23e", payload["next_da_move"])
        self.assertIn("B14d", payload["next_da_move"])
        self.assertIn("Regularity stays open", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-OBJECT.md").is_file())


if __name__ == "__main__":
    unittest.main()
