"""DA nowwhat: lost-operator council; not a vote."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_next import is_lost_ask  # noqa: E402
from da_nowwhat import CLAIMS, COUNCIL, HISTORY, run  # noqa: E402


class DaNowwhatTests(unittest.TestCase):
    def test_council_answers_from_papers(self):
        tmp = Path(tempfile.mkdtemp()) / "da_nowwhat_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["N1"]["verdict"], "pass")
        self.assertEqual(by["N2"]["verdict"], "pass")
        self.assertEqual(by["N3"]["verdict"], "fail")
        self.assertEqual(by["N4"]["verdict"], "fail")
        self.assertEqual(by["N5"]["verdict"], "fail")
        self.assertEqual(by["N6"]["verdict"], "open")
        self.assertEqual(by["N7"]["verdict"], "pass")
        self.assertEqual(by["N8"]["verdict"], "fail")
        self.assertEqual(by["N9"]["verdict"], "fail")
        self.assertEqual(by["N10"]["verdict"], "fail")
        self.assertEqual(by["N11"]["verdict"], "fail")
        self.assertEqual(by["N12"]["verdict"], "open")
        self.assertTrue(payload["meta"]["papers_not_minds"])
        self.assertTrue(payload["meta"]["not_a_vote"])
        self.assertTrue(payload["meta"]["not_a_seance"])
        self.assertTrue(payload["meta"]["does_not_write_X"])
        self.assertGreaterEqual(payload["counts"]["asked"], 12)
        self.assertLessEqual(payload["counts"]["asked"], 25)
        self.assertEqual(len(COUNCIL), payload["counts"]["asked"])
        self.assertGreaterEqual(payload["counts"]["history"], 12)
        self.assertLessEqual(payload["counts"]["history"], 15)
        self.assertEqual(len(HISTORY), payload["counts"]["history"])
        names = [row["who"] for row in COUNCIL]
        self.assertEqual(len(names), len(set(names)))
        hist = [row["who"] for row in HISTORY]
        self.assertEqual(len(hist), len(set(hist)))
        self.assertTrue(set(names).isdisjoint(hist))
        for row in COUNCIL:
            self.assertTrue(row["would_try"])
            self.assertTrue(row["cannot"])
            self.assertIn(row["bench"], ("living", "past"))
        for row in HISTORY:
            self.assertTrue(row["would_try"])
            self.assertTrue(row["cannot"])
            self.assertEqual(row["bench"], "history")
        self.assertIn("X", payload["target"])
        self.assertNotIn("F is the NS", payload["missing"])
        self.assertTrue((ROOT / "docs" / "DA-NOWWHAT.md").is_file())
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))

    def test_lost_ask_routes_to_council(self):
        self.assertTrue(is_lost_ask(""))
        self.assertTrue(is_lost_ask("now what"))
        self.assertTrue(is_lost_ask("what would you try"))
        self.assertTrue(is_lost_ask("I am lost"))
        self.assertTrue(is_lost_ask("the smartest people in history"))
        self.assertTrue(is_lost_ask("what would you do now"))
        self.assertFalse(is_lost_ask("is the target F"))
        self.assertFalse(is_lost_ask("what do we do from here"))


if __name__ == "__main__":
    unittest.main()
