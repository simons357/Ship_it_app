"""Hardy → I_tube: packet class lives; all-data domination dies."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_hardy_tube import run  # noqa: E402


class TrackBHardyTubeTests(unittest.TestCase):
    def test_packet_pass_all_data_fail(self):
        tmp = Path(tempfile.mkdtemp()) / "hardy_tube_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B4c_packet_hardy_tube"]["verdict"], "pass")
        self.assertEqual(by["B4d_wall_matches_off_axis"]["verdict"], "pass")
        self.assertEqual(by["B4b_hardy_not_I_tube"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        packets = by["B4c_packet_hardy_tube"]["scan"]["ratios"]
        self.assertLess(packets[-1], packets[0])
        killers = by["B4b_hardy_not_I_tube"]["killer"]["ratios"]
        self.assertGreater(killers[-1], 3.0 * killers[0])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-HARDY-TUBE.md").is_file())


if __name__ == "__main__":
    unittest.main()
