"""Working session: colleagues talk; a conversation cannot close."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_session import CLAIMS, KINGDOMS, SPEAKERS, TURNS, run  # noqa: E402


class DaSessionTests(unittest.TestCase):
    def test_session_is_process_not_a_close(self):
        tmp = Path(tempfile.mkdtemp()) / "da_session_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["S1"]["verdict"], "pass")
        self.assertEqual(by["S2"]["verdict"], "pass")
        self.assertEqual(by["S3"]["verdict"], "pass")
        self.assertEqual(by["S4"]["verdict"], "pass")
        self.assertEqual(by["S5"]["verdict"], "fail")
        self.assertEqual(by["S6"]["verdict"], "fail")
        self.assertEqual(by["S7"]["verdict"], "fail")
        self.assertEqual(by["S8"]["verdict"], "fail")
        self.assertEqual(by["S9"]["verdict"], "fail")
        self.assertEqual(by["S10"]["verdict"], "fail")
        self.assertEqual(by["S11"]["verdict"], "pass")
        self.assertEqual(by["S12"]["verdict"], "pass")
        self.assertEqual(by["S13"]["verdict"], "fail")
        self.assertEqual(by["S14"]["verdict"], "fail")
        self.assertEqual(payload["meta"]["regularity_after"], "open")
        self.assertTrue(payload["meta"]["not_a_vote"])
        self.assertTrue(payload["meta"]["not_a_close"])
        self.assertTrue(payload["meta"]["virtual_seance"])
        self.assertTrue(payload["meta"]["not_channeling"])
        self.assertIn("kingdoms", payload["meta"]["valuable_part"])
        self.assertIn("I_tube", payload["meta"]["next_write"])
        self.assertTrue((ROOT / "docs" / "DA-SESSION.md").is_file())
        who = {k["who"] for k in KINGDOMS}
        self.assertTrue(any("Leray" in w for w in who))
        self.assertTrue(any("Ladyzhenskaya" in w for w in who))
        self.assertGreaterEqual(len(KINGDOMS), 10)

    def test_they_talk_to_each_other(self):
        names = set(SPEAKERS)
        for must in (
            "Leray",
            "Kato",
            "Beale",
            "Majda",
            "Caffarelli",
            "Ladyzhenskaya",
            "Feynman",
            "Tesla",
            "Einstein",
            "Operator",
        ):
            self.assertIn(must, names)
        self.assertGreaterEqual(len(TURNS), 12)
        addressed = [t for t in TURNS if t["to"]]
        self.assertEqual(len(addressed), len(TURNS))
        # At least one fluids person is spoken to by another fluids person.
        fluids = {"Leray", "Kato", "Beale", "Majda", "Caffarelli", "Kohn", "Constantin", "Fefferman"}
        cross = [
            t
            for t in TURNS
            if t["speaker"] in fluids and fluids.intersection(t["to"])
        ]
        self.assertGreaterEqual(len(cross), 4)
        lady = next(t for t in TURNS if t["speaker"] == "Ladyzhenskaya")
        self.assertEqual(lady["slot"], "A")
        self.assertIn("Leray", lady["to"])
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))


if __name__ == "__main__":
    unittest.main()
