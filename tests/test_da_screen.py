"""Unification-claim screen smoke tests."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_screen import run  # noqa: E402


class DaScreenTests(unittest.TestCase):
    def test_nothing_passes_nature4_mssm_open_as_gauge3(self):
        tmp = Path(tempfile.mkdtemp()) / "da_screen_test.json"
        payload = run(out=tmp)
        self.assertEqual(payload["passed_nature4"], [])
        self.assertEqual(payload["counts"]["nature4"]["pass"], 0)
        self.assertTrue(payload["still_open_as_gauge3"])
        by_name = {c["name"]: c for c in payload["claims"]}
        self.assertEqual(by_name["Georgi–Glashow SU(5)"]["gauge3_verdict"], "fail")
        self.assertEqual(by_name["SM running (no extra stuff)"]["gauge3_verdict"], "fail")
        self.assertEqual(by_name["MSSM / SUSY SU(5) or SO(10)"]["gauge3_verdict"], "open")
        self.assertEqual(by_name["MSSM / SUSY SU(5) or SO(10)"]["nature4_verdict"], "fail")
        self.assertEqual(by_name["This repo's reconstructed R / SFE knobs"]["nature4_verdict"], "fail")


if __name__ == "__main__":
    unittest.main()
