"""Low-j CONC: energy ceiling holds; B9b blow is not NS; PDE not tuned."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from track_b_low_j import run  # noqa: E402


class TrackBLowJTests(unittest.TestCase):
    def test_ceiling_pass_frozen_blow_not_ns(self):
        tmp = Path(tempfile.mkdtemp()) / "low_j_test.json"
        payload = run(out=tmp)
        by = {row["name"]: row for row in payload["lemmas"]}
        self.assertEqual(by["B10_energy_ceiling"]["verdict"], "pass")
        self.assertEqual(by["B10a_frozen_blow_not_ns"]["verdict"], "fail")
        self.assertEqual(by["B10b_ceiling_not_climbing"]["verdict"], "fail")
        self.assertEqual(by["B10c_climbing_not_close"]["verdict"], "fail")
        self.assertEqual(by["B10d_not_a_pde_retune"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["domain_verdict"], "open")
        self.assertFalse(payload["meta"]["tuning_the_pde"])
        self.assertLessEqual(by["B10_energy_ceiling"]["worst_X_over_ceiling"], 1.0 + 1e-9)
        self.assertTrue(by["B10a_frozen_blow_not_ns"]["blow"]["blew"])

    def test_writeup_exists(self):
        self.assertTrue((ROOT / "docs" / "TRACK-B-LOW-J.md").is_file())


if __name__ == "__main__":
    unittest.main()
