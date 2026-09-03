"""Ground-level destination: reconstruct, ablate, program review."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_ground import ABLATE, GROUND, MINDS, RECONSTRUCT, run  # noqa: E402


class DaGroundTests(unittest.TestCase):
    def test_destination_open_rebuild_math_not_couplings(self):
        tmp = Path(tempfile.mkdtemp()) / "da_ground_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["C1"]["verdict"], "pass")
        self.assertEqual(by["C2"]["verdict"], "fail")
        self.assertEqual(by["C3"]["verdict"], "open")
        self.assertEqual(by["C4"]["verdict"], "fail")
        self.assertEqual(by["C5"]["verdict"], "fail")
        self.assertEqual(by["C6"]["verdict"], "fail")
        self.assertEqual(by["C7"]["verdict"], "fail")
        self.assertEqual(by["C8"]["verdict"], "fail")
        self.assertTrue(payload["meta"]["hb_is_not_a_trigger"])
        self.assertTrue(payload["meta"]["program_review"])
        self.assertTrue(payload["meta"]["vote_cannot_close"])
        self.assertTrue(payload["meta"]["does_not_retune_nodes"])
        self.assertTrue(payload["meta"]["does_not_load_sfe_into_ns"])

        ground = {r["id"]: r for r in payload["ground"]}
        self.assertEqual(ground["G0"]["verdict"], "pass")
        self.assertEqual(ground["G1"]["verdict"], "pass")
        self.assertEqual(ground["G2"]["verdict"], "pass")
        self.assertEqual(ground["G5"]["verdict"], "fail")

        recon = {r["id"]: r for r in payload["reconstruct"]}
        self.assertEqual(recon["R1"]["verdict"], "pass")
        self.assertEqual(recon["R4"]["verdict"], "pass")
        self.assertEqual(recon["R5"]["verdict"], "fail")
        self.assertEqual(recon["R6"]["verdict"], "fail")
        self.assertEqual(recon["R7"]["verdict"], "fail")

    def test_minds_and_ablations_are_typed(self):
        names = {m["name"] for m in MINDS}
        self.assertIn("Einstein", names)
        self.assertIn("Tesla", names)
        self.assertIn("Feynman", names)
        self.assertIn("Weyl", names)
        self.assertIn("Wigner", names)
        self.assertIn("von Neumann", names)
        tesla = next(m for m in MINDS if m["name"] == "Tesla")
        self.assertIn("cannot derive SU(3)", tesla["cannot"])
        drop_d = next(r for r in ABLATE if r["id"] == "A1")
        self.assertEqual(drop_d["verdict"], "fail")
        keep_bag = next(r for r in ABLATE if r["id"] == "A4")
        self.assertEqual(keep_bag["verdict"], "pass")
        self.assertEqual(len(GROUND), len({r["id"] for r in GROUND}))
        self.assertEqual(len(RECONSTRUCT), len({r["id"] for r in RECONSTRUCT}))
        self.assertEqual(len(ABLATE), len({r["id"] for r in ABLATE}))
        self.assertEqual(len(MINDS), len(names))


if __name__ == "__main__":
    unittest.main()
