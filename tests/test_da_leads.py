"""Full-roll lead sweep: every chair asked; glue refused."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_leads import CLAIMS, LEADS, MUST_SIT, run  # noqa: E402


class DaLeadsTests(unittest.TestCase):
    def test_every_chair_asked(self):
        tmp = Path(tempfile.mkdtemp()) / "da_leads_test.json"
        payload = run(out=tmp)
        names = {row["who"] for row in LEADS}
        self.assertEqual(MUST_SIT, names)
        self.assertEqual(payload["meta"]["missing_chairs"], [])
        self.assertEqual(payload["counts"]["asked"], len(MUST_SIT))
        self.assertEqual(payload["counts"]["unique"], len(MUST_SIT))
        self.assertTrue({"A", "B", "Q", "U", "meta"} <= set(payload["counts"]["slots"]))
        self.assertTrue((ROOT / "docs" / "DA-LEADS.md").is_file())

    def test_sweep_is_process_not_a_close(self):
        tmp = Path(tempfile.mkdtemp()) / "da_leads_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["R1"]["verdict"], "pass")
        self.assertEqual(by["R2"]["verdict"], "pass")
        self.assertEqual(by["R3"]["verdict"], "fail")
        self.assertEqual(by["R4"]["verdict"], "fail")
        self.assertEqual(by["R5"]["verdict"], "fail")
        self.assertEqual(by["R6"]["verdict"], "fail")
        self.assertEqual(by["R7"]["verdict"], "open")
        self.assertEqual(by["R8"]["verdict"], "fail")
        self.assertEqual(by["R9"]["verdict"], "pass")
        self.assertEqual(by["R10"]["verdict"], "fail")
        self.assertEqual(by["R11"]["verdict"], "fail")
        self.assertEqual(by["R12"]["verdict"], "fail")
        self.assertEqual(by["R13"]["verdict"], "fail")
        self.assertEqual(by["R14"]["verdict"], "fail")
        self.assertEqual(by["R15"]["verdict"], "fail")
        self.assertEqual(by["R16"]["verdict"], "fail")
        self.assertEqual(by["R17"]["verdict"], "fail")
        self.assertEqual(by["R18"]["verdict"], "fail")
        self.assertEqual(by["R19"]["verdict"], "fail")
        self.assertEqual(by["R20"]["verdict"], "fail")
        self.assertEqual(by["R21"]["verdict"], "fail")
        self.assertEqual(by["R22"]["verdict"], "fail")
        self.assertEqual(by["R23"]["verdict"], "fail")
        self.assertEqual(by["R24"]["verdict"], "fail")
        self.assertEqual(by["R25"]["verdict"], "fail")
        self.assertEqual(by["R26"]["verdict"], "fail")
        self.assertEqual(by["R27"]["verdict"], "fail")
        self.assertEqual(by["R28"]["verdict"], "fail")
        self.assertEqual(by["R29"]["verdict"], "fail")
        self.assertEqual(by["R30"]["verdict"], "fail")
        self.assertEqual(by["R31"]["verdict"], "fail")
        self.assertEqual(by["R32"]["verdict"], "fail")
        self.assertEqual(by["R33"]["verdict"], "fail")
        self.assertEqual(by["R34"]["verdict"], "fail")
        self.assertEqual(by["R35"]["verdict"], "fail")
        self.assertEqual(by["R36"]["verdict"], "fail")
        self.assertEqual(by["R37"]["verdict"], "fail")
        self.assertEqual(by["R38"]["verdict"], "fail")
        self.assertEqual(by["R39"]["verdict"], "fail")
        self.assertEqual(by["R40"]["verdict"], "fail")
        self.assertEqual(by["R41"]["verdict"], "fail")
        self.assertEqual(by["R42"]["verdict"], "fail")
        self.assertEqual(by["R43"]["verdict"], "fail")
        self.assertEqual(by["R44"]["verdict"], "fail")
        self.assertEqual(by["R45"]["verdict"], "fail")
        self.assertEqual(by["R46"]["verdict"], "fail")
        self.assertEqual(by["R47"]["verdict"], "fail")
        self.assertEqual(by["R48"]["verdict"], "fail")
        self.assertEqual(by["R49"]["verdict"], "fail")
        self.assertEqual(by["R50"]["verdict"], "fail")
        self.assertEqual(by["R51"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["regularity_after"], "open")
        self.assertEqual(payload["meta"]["possible_to_close_X"], "open")
        self.assertTrue(payload["meta"]["glue_refused"])
        self.assertTrue(payload["meta"]["not_a_vote"])
        self.assertIn("residual", payload["meta"]["next_write"])

    def test_slots_do_not_glue(self):
        by_slot = {}
        for row in LEADS:
            by_slot.setdefault(row["slot"], []).append(row["who"])
        self.assertIn("Ladyzhenskaya", by_slot["A"])
        self.assertIn("LMFDB / analytic NT", by_slot["Q"])
        self.assertIn("Leray", by_slot["B"])
        self.assertIn("Einstein", by_slot["U"])
        self.assertIn("LVK", by_slot["U"])
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))


if __name__ == "__main__":
    unittest.main()
