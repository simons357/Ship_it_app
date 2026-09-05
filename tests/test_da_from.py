"""DA from: walk mine to the break; not smoothness."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_from import BREAK, CLAIMS, MINE, NEEDED, is_from_ask, run  # noqa: E402


class DaFromTests(unittest.TestCase):
    def test_walks_mine_to_break(self):
        tmp = Path(tempfile.mkdtemp()) / "da_from_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["P1"]["verdict"], "pass")
        self.assertEqual(by["P2"]["verdict"], "pass")
        self.assertEqual(by["P3"]["verdict"], "fail")
        self.assertEqual(by["P4"]["verdict"], "fail")
        self.assertEqual(by["P5"]["verdict"], "fail")
        self.assertEqual(by["P6"]["verdict"], "fail")
        self.assertEqual(by["P7"]["verdict"], "fail")
        self.assertEqual(by["P8"]["verdict"], "pass")
        self.assertEqual(by["P9"]["verdict"], "open")
        self.assertTrue(payload["meta"]["takes_mine"])
        self.assertTrue(payload["meta"]["not_a_closer"])
        brk = next(s for s in MINE if s.get("break_here"))
        self.assertEqual(brk["id"], "S10")
        self.assertEqual(payload["break_id"], "S10")
        self.assertFalse(any(s["a_priori"] for s in MINE if s["verdict"] == "pass"))
        self.assertEqual(len(NEEDED), 4)
        self.assertIn("int_0^T R", BREAK["math"])
        self.assertTrue(is_from_ask("from my work"))
        self.assertTrue(is_from_ask("where it breaks"))
        self.assertTrue(is_from_ask("proceed to global regularity"))
        self.assertFalse(is_from_ask(""))
        self.assertFalse(is_from_ask("now what"))
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        self.assertTrue((ROOT / "docs" / "DA-FROM.md").is_file())


if __name__ == "__main__":
    unittest.main()
