"""SM Lagrangian broken to atoms and reassembled."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_sm_break import leaves, run, tree  # noqa: E402


class DaSmBreakTests(unittest.TestCase):
    def test_more_than_five_blocks_and_reassembly(self):
        tmp = Path(tempfile.mkdtemp()) / "da_sm_break_test.json"
        payload = run(out=tmp)
        self.assertTrue(payload["meta"]["five_blocks_not_enough"])
        self.assertGreater(payload["meta"]["n_leaves"], 5)
        self.assertGreater(payload["counts"]["leaves"], 20)
        self.assertEqual(len(payload["tree"]["fingers"]), 6)
        self.assertTrue(payload["reassembly"]["still_not_F"])
        self.assertTrue(payload["reassembly"]["still_not_NS"])
        steps = {s["step"]: s for s in payload["reassembly"]["steps"]}
        self.assertEqual(steps[3]["verdict"], "pass")
        self.assertEqual(steps[6]["verdict"], "pass")
        self.assertEqual(steps[7]["verdict"], "fail")
        eq = payload["reassembly"]["put_back"]["equation"]
        self.assertIn("T_μν[SM]", eq)

    def test_drop_ghosts_keeps_sm_drop_su3_does_not(self):
        tmp = Path(tempfile.mkdtemp()) / "da_sm_break_test.json"
        payload = run(out=tmp)
        by = {d["drop"]: d for d in payload["drop_one"]}
        self.assertTrue(by["ghosts"]["still_SM"])
        self.assertFalse(by["SU3"]["still_SM"])
        self.assertFalse(by["higgs_doublet"]["still_SM"])
        self.assertTrue(by["G_N"]["still_SM"])
        names = {x["name"] for x in leaves(tree())}
        self.assertIn("g_s", names)
        self.assertIn("G_N", names)
        self.assertIn("dim4", names)


if __name__ == "__main__":
    unittest.main()
