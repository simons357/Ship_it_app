"""Waveform-rule smoke tests. Additive; does not touch A/B/Q."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_wave import RULES, run  # noqa: E402


class DaWaveTests(unittest.TestCase):
    def test_not_collapsed_and_unfalsifiable_fails(self):
        tmp = Path(tempfile.mkdtemp()) / "da_wave_test.json"
        payload = run(out=tmp)
        self.assertFalse(payload["waveform"]["collapsed"])
        self.assertFalse(payload["waveform"]["emerged"])
        self.assertTrue(payload["meta"]["unfalsifiable_is_not_true"])
        self.assertEqual(payload["meta"]["does_not_change_slots"], ["A", "B", "Q"])
        by_name = {row["name"]: row for row in payload["falsification"]}
        self.assertEqual(by_name["unfalsifiable_might_be_true"]["verdict"], "fail")
        self.assertFalse(by_name["unfalsifiable_might_be_true"]["falsifiable"])
        self.assertEqual(by_name["F_exists"]["verdict"], "fail")
        self.assertEqual(by_name["possible_by_count"]["verdict"], "open")
        self.assertIn("possible_by_count", payload["waveform"]["still_in_superposition"])

    def test_rules_include_falsification_and_collapse(self):
        self.assertIn("falsification", RULES)
        self.assertIn("collapse", RULES)
        self.assertIn("do_not_mess_up_da", RULES)

    def test_must_hits_entangled_oscillators_not(self):
        tmp = Path(tempfile.mkdtemp()) / "da_wave_test.json"
        payload = run(out=tmp)
        edges = {(e["a"], e["b"]): e["entangled"] for e in payload["entanglement"]}
        self.assertTrue(edges[("unifier_claim", "log_cc_ratio")])
        self.assertFalse(edges[("oscillators_teleology", "four_couplings")])


if __name__ == "__main__":
    unittest.main()
