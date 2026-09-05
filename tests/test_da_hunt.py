"""DA hunt: proof-chain hunter; not a closer."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_hunt import BLOCKED, CLAIMS, EDGES, LEGAL, MEANING, NODES, OBJECT, run  # noqa: E402


class DaHuntTests(unittest.TestCase):
    def test_hunter_is_graph_not_a_fill(self):
        tmp = Path(tempfile.mkdtemp()) / "da_hunt_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["H1"]["verdict"], "pass")
        self.assertEqual(by["H2"]["verdict"], "pass")
        self.assertEqual(by["H3"]["verdict"], "pass")
        self.assertEqual(by["H4"]["verdict"], "fail")
        self.assertEqual(by["H5"]["verdict"], "fail")
        self.assertEqual(by["H6"]["verdict"], "fail")
        self.assertEqual(by["H7"]["verdict"], "fail")
        self.assertEqual(by["H8"]["verdict"], "fail")
        self.assertEqual(by["H9"]["verdict"], "fail")
        self.assertEqual(by["H10"]["verdict"], "open")
        self.assertEqual(by["H11"]["verdict"], "pass")
        self.assertEqual(by["H12"]["verdict"], "pass")
        self.assertEqual(by["H13"]["verdict"], "fail")
        self.assertTrue(payload["meta"]["is_graph"])
        self.assertTrue(payload["meta"]["llm_does_not_fill"])
        self.assertTrue(payload["meta"]["uses_llm_to_phrase"])
        self.assertTrue(payload["meta"]["meaning_is_classify"])
        self.assertTrue(MEANING["uses_llm"])
        self.assertIn("classify", MEANING["meaning_that_sits"])
        self.assertTrue(payload["meta"]["object_window"])
        self.assertTrue(payload["meta"]["does_not_rerun_trackb"])
        self.assertIn("X", payload["object"]["math"])
        self.assertTrue(payload["object"]["look_is_not_a_bound"])
        self.assertGreaterEqual(len(NODES), 8)
        self.assertGreaterEqual(len(EDGES), 8)
        self.assertTrue(any(e["verdict"] == "open" for e in EDGES))
        ids = {n["id"] for n in NODES}
        for e in EDGES:
            self.assertIn(e["src"], ids)
            self.assertIn(e["dst"], ids)
        blocked_src = {b["src"] for b in BLOCKED}
        self.assertIn("LLM", blocked_src)
        self.assertIn("A", blocked_src)
        self.assertEqual(len(LEGAL), payload["counts"]["legal"])
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-HUNT.md").is_file())
        self.assertIn("X = ||omega||_2^2", OBJECT["window"])


if __name__ == "__main__":
    unittest.main()
