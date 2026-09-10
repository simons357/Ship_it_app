"""N-shell R★ maximizer table sits. Target A not killed. Not a proof."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
JSON = ROOT / "results" / "rstar_shell_climb" / "maximizer.json"
PHONE = ROOT / "docs" / "RSTAR-SHELL-CLIMB.md"
SCRIPT = ROOT / "scripts" / "ns_attacks" / "maximize_rstar_shells.py"


class RstarShellClimbTests(unittest.TestCase):
    def test_phone_and_script(self):
        self.assertTrue(PHONE.is_file())
        text = PHONE.read_text()
        self.assertIn("Does not climb", text)
        self.assertIn("CS-REMAINDER.md", text)
        self.assertIn("NS not solved", text)
        self.assertTrue(SCRIPT.is_file())

    def test_table_saturates(self):
        data = json.loads(JSON.read_text())
        self.assertIs(data["ns_solved"], False)
        self.assertEqual(data["lemma_star"], "OPEN")
        self.assertIs(data["climbs"], False)
        two = [t for t in data["table"] if t["N"] == 2 and t["max_R"] is not None]
        self.assertGreaterEqual(len(two), 6)
        vals = [t["max_R"] for t in two]
        self.assertGreater(min(vals), 0.2)
        self.assertLess(max(vals), 1.0)
        self.assertLess(max(vals) / min(vals), 3.0)
        self.assertGreater(two[-1]["max_s"], two[0]["max_s"])


if __name__ == "__main__":
    unittest.main()
