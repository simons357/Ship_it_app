"""Occupation time: clock covers; Leray does not shorten CONC."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_occupation import run  # noqa: E402


class TrackBOccupationTests(unittest.TestCase):
    def test_clock_pass_leray_fail_glue_open(self):
        tmp = Path(tempfile.mkdtemp()) / "occ_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B8_occupation_clock"]["verdict"], "pass")
        self.assertEqual(by["B8a_high_jstar_short"]["verdict"], "pass")
        self.assertEqual(by["B8b_leray_not_occupation"]["verdict"], "fail")
        self.assertEqual(by["B8c_occupation_not_X_bound"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        hot = by["B8a_high_jstar_short"]["decay"]["hot"]
        self.assertLess(hot[-1], 0.5 * hot[0])
        spike = by["B8b_leray_not_occupation"]["spike"]
        self.assertTrue(spike["occupies_almost_all"])
        self.assertTrue(spike["X_unbounded"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-OCCUPATION.md").is_file())


if __name__ == "__main__":
    unittest.main()
