"""Grow s on the 9B family. Designed 9D stays dead. Finite K is not C0."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from estimate_audit import classify_paragraph  # noqa: E402
from ns_attacks.attack9b_grow_s import run  # noqa: E402

PAGE = ROOT / "docs" / "ATTACK-9D-GROW-S.md"
SETUP = ROOT / "docs" / "ATTACK-9D-SETUP.md"


class Attack9BGrowSTests(unittest.TestCase):
    def test_page_is_historical_not_a_close(self):
        text = PAGE.read_text()
        self.assertIn("Historical", text)
        self.assertIn("Designed", text)
        self.assertIn("attack9d_theta_m2_locked_phase.py", text)
        self.assertIn("\\Pi_\\beta B", text)
        self.assertIn("16s", text)
        self.assertIn("0.456", text)
        self.assertIn("C_0", text)
        self.assertIn("not a kill", text)
        self.assertIn("killed", text.lower())
        self.assertNotIn("NS is solved", text)
        self.assertNotIn("Clay is solved", text)

    def test_tiny_sweep_keeps_inequalities_and_stays_open(self):
        summary = run(seed=1390, kmax=3, n_trials=1)
        g = summary["growing"]
        self.assertGreaterEqual(g["n_fields"], 1)
        self.assertEqual(g["n_fail_pairs_le_m"], 0)
        self.assertEqual(g["n_fail_cs"], 0)
        self.assertEqual(g["n_fail_K_le_16s"], 0)
        self.assertIs(summary["ns_solved"], False)
        self.assertEqual(summary["lemma_star"], "KILLED")
        self.assertEqual(summary["kill_lane"], "CLOSED_BY_V_N")
        self.assertTrue(summary["verdict"].startswith("GROW_S"))
        self.assertIn("theta", summary["not"])

    def test_designed_9d_stays_dead_on_setup(self):
        text = SETUP.read_text()
        self.assertIn("Do **not** implement Attack 9D", text)
        self.assertIn("attack9d_theta_m2_locked_phase.py", text)

    def test_page_passes_discard_filter(self):
        cls = classify_paragraph(PAGE.read_text())
        self.assertTrue(cls["allowed_in_estimate"])
        self.assertEqual(cls["discard_hits"], [])


if __name__ == "__main__":
    unittest.main()
