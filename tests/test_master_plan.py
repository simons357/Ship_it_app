"""Master plan and report audit: star is killed; C10 not seated; no H repair."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "docs" / "MASTER-PLAN.md"
AUDIT = ROOT / "docs" / "REPORT-AUDIT.md"
STATUS = ROOT / "docs" / "NS-STATUS.md"
TAPE = ROOT / "docs" / "YES-NO-OPEN.md"
TINY = ROOT / "docs" / "TINY.txt"
LATEST = ROOT / "docs" / "LATEST.md"
ISSUES = ROOT / "docs" / "ISSUES-SHEET.md"


def _plain(path: Path) -> str:
    return path.read_text().replace("\\", "")


class MasterPlanTests(unittest.TestCase):
    def test_plan_does_not_close(self):
        text = _plain(PLAN)
        raw = PLAN.read_text()
        self.assertIn("Not a proof", raw)
        self.assertIn("seated close", text)
        self.assertIn("Route A", raw)
        self.assertIn("Route B", raw)
        self.assertIn("Death condition", raw)
        self.assertIn("useful", text)
        self.assertIn("Do not start leftover 1", raw)
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("almost proved", text.lower())
        self.assertIn("Yes for", raw)
        self.assertIn("this plan", text)
        self.assertIn("unaugmented", text)
        self.assertIn("A is not B", raw)
        self.assertIn("Peer recommendations", raw)
        self.assertIn("Kato", raw)

    def test_audit_catches_gpt_star_error(self):
        text = _plain(AUDIT)
        raw = AUDIT.read_text()
        self.assertIn("WRONG", raw)
        self.assertIn("KILLED", raw)
        self.assertIn("Most dangerous error", raw)
        self.assertIn("OVERCLAIM", raw)
        self.assertIn("REJECT as primary", raw)
        self.assertIn("Do not write", raw)
        self.assertIn("Yes for a plan", raw)
        self.assertIn("No for a close", raw)
        self.assertIn("Kato", raw)
        self.assertIn("Global Regularity Program", raw)
        self.assertIn("ACCEPT", raw)
        self.assertIn("Rocks", raw)
        self.assertIn("singularity", text)
        self.assertIn("Do not switch", raw)
        self.assertIn("living handoff", text)
        self.assertIn("H1/H", raw)
        self.assertIn("Do not mail a panel", raw)
        self.assertIn("Neither, from this desk", raw)
        self.assertIn("wrong Dini", text)
        self.assertIn("Do not write those two pages", raw)
        self.assertNotIn("Exact-shell 9D — claimed", raw)
        self.assertNotIn("NS is solved", text)
        tape = _plain(TAPE)
        self.assertIn("KILLED", tape)
        self.assertIn("GPT board had this wrong", tape)

    def test_pointers(self):
        for path in (STATUS, TAPE, TINY, LATEST, ISSUES):
            body = path.read_text()
            self.assertIn("MASTER-PLAN.md", body, msg=str(path))
            self.assertIn("REPORT-AUDIT.md", body, msg=str(path))


if __name__ == "__main__":
    unittest.main()
