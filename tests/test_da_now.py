"""Living roster: papers, not a world genius census."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_now import CLAIMS, DEAD, WATCH, run, seated_living  # noqa: E402


class DaNowTests(unittest.TestCase):
    def test_roster_is_not_a_census(self):
        tmp = Path(tempfile.mkdtemp()) / "da_now_test.json"
        payload = run(out=tmp)
        by = {c["id"]: c for c in payload["claims"]}
        self.assertEqual(by["N1"]["verdict"], "pass")
        self.assertEqual(by["N2"]["verdict"], "fail")
        self.assertEqual(by["N3"]["verdict"], "fail")
        self.assertEqual(by["N4"]["verdict"], "fail")
        self.assertEqual(by["N5"]["verdict"], "fail")
        self.assertEqual(by["N6"]["verdict"], "fail")
        self.assertEqual(by["N7"]["verdict"], "pass")
        self.assertEqual(by["N8"]["verdict"], "fail")
        self.assertEqual(by["N9"]["verdict"], "fail")
        self.assertEqual(by["N10"]["verdict"], "open")
        self.assertTrue(payload["meta"]["genius_is_not_a_slot"])
        self.assertTrue(payload["meta"]["not_a_vote"])
        self.assertTrue(payload["meta"]["does_not_write_X"])
        self.assertTrue((ROOT / "docs" / "DA-NOW.md").is_file())

    def test_seated_excludes_dead_and_includes_fluids(self):
        names = set(seated_living())
        self.assertTrue(DEAD.isdisjoint(names))
        for must in ("Tao", "Sverak", "Barker", "Kukavica", "Hou"):
            self.assertIn(must, names)
        self.assertNotIn("Operator", names)
        self.assertNotIn("Shahmurov", names)
        watch = {row["name"] for row in WATCH}
        self.assertTrue(watch.isdisjoint(names))
        self.assertIn("Robinson", watch)
        self.assertIn("Kenig", watch)
        self.assertIn("Maynard", watch)
        self.assertEqual(len(CLAIMS), len({c["id"] for c in CLAIMS}))
        collab = {row["name"] for row in run(out=Path(tempfile.mkdtemp()) / "n.json")["collaborations"]}
        self.assertIn("LVK collaboration", collab)
        self.assertIn("ATLAS / CMS / LHCb", collab)


if __name__ == "__main__":
    unittest.main()
