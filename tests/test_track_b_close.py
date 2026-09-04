"""Leftover close as an a priori: scoring leftovers does not write X."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_close import run  # noqa: E402


class TrackBCloseTests(unittest.TestCase):
    def test_leftover_close_not_an_a_priori(self):
        tmp = Path(tempfile.mkdtemp()) / "close_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B35_close_readable"]["verdict"], "pass")
        self.assertEqual(by["B35a_close_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B35b_catalog_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B35c_fails_not_ns"]["verdict"], "fail")
        self.assertEqual(by["B35d_close_not_integral_max"]["verdict"], "fail")
        self.assertEqual(by["B35e_domain_leftover"]["verdict"], "fail")
        self.assertEqual(by["B35f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertFalse(payload["meta"]["spawned_n64"])
        self.assertGreater(by["B35_close_readable"]["T_long"], by["B35_close_readable"]["t_room"])
        self.assertLess(by["B35_close_readable"]["c_inc_max"], by["B35_close_readable"]["c_save"])
        self.assertIn("B35e", payload["next_da_move"])
        self.assertIn("B34e", payload["next_da_move"])
        self.assertIn("B23e", payload["next_da_move"])
        self.assertIn("B22e", payload["next_da_move"])
        self.assertIn("B14d", payload["next_da_move"])
        self.assertIn("Regularity stays open", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-CLOSE.md").is_file())


if __name__ == "__main__":
    unittest.main()
