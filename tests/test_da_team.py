"""Dream-team roster: paper + experiment, no vote-to-close."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_team import TEAM, run  # noqa: E402


class DaTeamTests(unittest.TestCase):
    def test_paper_and_nature_no_vote(self):
        tmp = Path(tempfile.mkdtemp()) / "da_team_test.json"
        payload = run(out=tmp)
        self.assertTrue(payload["meta"]["vote_cannot_close"])
        self.assertTrue(payload["consensus"]["not_a_vote"])
        sides = {m["side"] for m in payload["team"]}
        self.assertIn("paper", sides)
        self.assertIn("nature", sides)
        slots = {m["slot"] for m in TEAM}
        self.assertTrue({"A", "B", "U", "meta"} <= slots)
        names = {m["name"] for m in TEAM}
        self.assertIn("Leray", names)
        self.assertIn("Einstein", names)
        self.assertIn("experiment / PDG", names)
        self.assertNotIn("Cosmo Superagent", names)
        self.assertIn("I_tube", payload["consensus"]["B"])
        self.assertIn("open", payload["consensus"]["B"])


if __name__ == "__main__":
    unittest.main()
