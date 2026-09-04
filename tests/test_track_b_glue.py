"""Glue to X: high j* sits; low j* blows; sketch is not NS."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_glue import run  # noqa: E402


class TrackBGlueTests(unittest.TestCase):
    def test_high_sits_low_blows_ns_open(self):
        tmp = Path(tempfile.mkdtemp()) / "glue_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B9_glue_bookkeeping"]["verdict"], "pass")
        self.assertEqual(by["B9a_glue_high_jstar"]["verdict"], "pass")
        self.assertEqual(by["B9b_glue_low_jstar_blows"]["verdict"], "fail")
        self.assertEqual(by["B9c_glue_switching"]["verdict"], "pass")
        self.assertEqual(by["B9d_glue_not_X_a_priori"]["verdict"], "open")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertIn("not a jerk", payload["meta"]["tesla"])
        self.assertFalse(by["B9a_glue_high_jstar"]["run"]["blew"])
        self.assertTrue(by["B9b_glue_low_jstar_blows"]["run"]["blew"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-GLUE.md").is_file())


if __name__ == "__main__":
    unittest.main()
