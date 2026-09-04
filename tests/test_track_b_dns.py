"""DNS as an a priori: packet runs are a check, not a bound."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_dns import T_LONG, T_ROOM, run  # noqa: E402


class TrackBDnsTests(unittest.TestCase):
    def test_dns_not_an_a_priori(self):
        tmp = Path(tempfile.mkdtemp()) / "dns_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B23_dns_readable"]["verdict"], "pass")
        self.assertEqual(by["B23a_dns_not_a_priori"]["verdict"], "fail")
        self.assertEqual(by["B23b_room_time_not_continuation"]["verdict"], "fail")
        self.assertEqual(by["B23c_packet_not_all_data"]["verdict"], "fail")
        self.assertEqual(by["B23d_no_blow_not_bounded"]["verdict"], "fail")
        self.assertEqual(by["B23e_finer_still_open"]["verdict"], "open")
        self.assertEqual(by["B23f_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertTrue(payload["meta"]["climb_dns_dead_end"])
        self.assertGreater(T_LONG, T_ROOM)
        self.assertIn("B22e", payload["next_da_move"])
        self.assertIn("B14d", payload["next_da_move"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-DNS.md").is_file())


if __name__ == "__main__":
    unittest.main()
