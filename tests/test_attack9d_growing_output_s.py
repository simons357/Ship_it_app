"""9D has no close. Growing-s is the team 9B-counting sweep."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.attack9b_output_counting import run  # noqa: E402

SOT = ROOT / "docs" / "math" / "ns_attacks" / "ATTACK_9D_THETA_M2_LOCKED_PHASE.md"
SCRIPT = ROOT / "scripts" / "ns_attacks" / "attack9d_growing_output_s.py"


class Attack9DNoClaimTests(unittest.TestCase):
    def test_doc_does_not_claim_and_points_at_team_script(self):
        text = SOT.read_text()
        self.assertIn("No 9D close", text)
        self.assertIn("NS not solved", text)
        self.assertIn("attack9b_output_counting.py", text)
        self.assertIn("attack9d_growing_output_s.py", text)
        self.assertIn("Do not rebuild", text)
        self.assertNotIn("**Not implemented.**", text)
        self.assertTrue(SCRIPT.is_file())
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Lemma★ is closed", text)

    def test_wrapper_math_is_the_counting_sweep(self):
        summary = run(seed=1390, n_trials=1)
        self.assertIs(summary["ns_solved"], False)
        self.assertEqual(summary["lemma_star"], "OPEN")
        self.assertEqual(summary["growing"]["kill_lane"], "LIVE")
        self.assertTrue(summary["verdict"].startswith("FIXED_S_EXCLUDED"))


if __name__ == "__main__":
    unittest.main()
