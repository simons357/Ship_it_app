"""Low Bony T: energy class lives; uniform ρ^{1/2} dies."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_bony_t import run  # noqa: E402


class TrackBBonyTTests(unittest.TestCase):
    def test_split_pass_rho_uniform_fail(self):
        tmp = Path(tempfile.mkdtemp()) / "bony_t_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B7_bony_split"]["verdict"], "pass")
        self.assertEqual(by["B7a_self_is_t2"]["verdict"], "pass")
        self.assertEqual(by["B7b_low_T_energy_class"]["verdict"], "pass")
        self.assertEqual(by["B7c_low_T_not_rho_uniform"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        hope = by["B7c_low_T_not_rho_uniform"]["scan"]["inf_over_rho_hope"]
        self.assertGreater(hope[-1], 1.3 * hope[0])
        energy = by["B7b_low_T_energy_class"]["scan"]["inf_over_energy"]
        self.assertLess(max(energy), 8.0)

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-BONY-T.md").is_file())


if __name__ == "__main__":
    unittest.main()
