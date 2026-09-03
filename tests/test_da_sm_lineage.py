"""SM lineage: backwards limits and forwards assembly."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_sm_lineage import LINEAGE, LIMITS, run  # noqa: E402


class DaSmLineageTests(unittest.TestCase):
    def test_recovers_ancestors_not_einstein_or_ns(self):
        tmp = Path(tempfile.mkdtemp()) / "da_sm_lineage_test.json"
        payload = run(out=tmp)
        by = {r["name"]: r for r in payload["forwards"]}
        self.assertEqual(by["Maxwell"]["back_verdict"], "pass")
        self.assertEqual(by["QED"]["back_verdict"], "pass")
        self.assertEqual(by["Fermi_4fermion"]["back_verdict"], "pass")
        self.assertEqual(by["Yang_Mills"]["back_verdict"], "pass")
        self.assertEqual(by["GWS_electroweak"]["back_verdict"], "pass")
        self.assertEqual(by["QCD"]["back_verdict"], "pass")
        self.assertEqual(by["Einstein_plus_T"]["back_verdict"], "fail")
        lim = {r["name"]: r for r in payload["limits"]}
        self.assertEqual(lim["SM_to_QED"]["verdict"], "pass")
        self.assertEqual(lim["SM_to_Maxwell"]["verdict"], "pass")
        self.assertEqual(lim["SM_to_Fermi"]["verdict"], "pass")
        self.assertEqual(lim["SM_to_YM"]["verdict"], "pass")
        self.assertEqual(lim["SM_to_one_group"]["verdict"], "fail")
        self.assertEqual(lim["SM_to_Einstein"]["verdict"], "fail")
        self.assertEqual(lim["SM_to_NS"]["verdict"], "fail")
        self.assertGreaterEqual(payload["counts"]["recoverable_from_SM"], 8)
        self.assertEqual(len(LINEAGE), len({r["name"] for r in LINEAGE}))
        self.assertEqual(len(LIMITS), len({r["name"] for r in LIMITS}))


if __name__ == "__main__":
    unittest.main()
