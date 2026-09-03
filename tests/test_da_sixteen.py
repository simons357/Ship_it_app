"""Four-family 16-list and singleton-fit checks."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_sixteen import FAMILIES, SIXTEEN, possibility_clue, run  # noqa: E402


class DaSixteenTests(unittest.TestCase):
    def test_four_families_of_four(self):
        self.assertEqual(len(SIXTEEN), 16)
        self.assertEqual(SIXTEEN[-1], "R")
        for fam, members in FAMILIES.items():
            self.assertEqual(len(members), 4, fam)
        self.assertEqual(sum(len(v) for v in FAMILIES.values()), 16)

    def test_possibility_is_dimension_count(self):
        clue = possibility_clue()
        self.assertTrue(clue["generic_existence"])
        self.assertEqual(clue["verdict"], "open")
        self.assertGreater(clue["n_knobs"], clue["k_with_leftovers"])

    def test_run_names_sixteenth_and_finds_core(self):
        tmp = Path(tempfile.mkdtemp()) / "da_sixteen_test.json"
        payload = run(n=80, seed=1, out=tmp)
        self.assertFalse(payload["meta"]["cosmos_app_list_found"])
        self.assertEqual(payload["meta"]["sixteenth"], "R (realization / teleology)")
        self.assertIn("log_cc_ratio", payload["fits_that_move_R"])
        self.assertIn("log_hierarchy", payload["fits_that_move_R"])
        sixteenth = payload["each_one"][-1]
        self.assertEqual(sixteenth["name"], "R")
        self.assertEqual(sixteenth["fits"], "target")
        self.assertFalse(payload["survivors_locked"]["couplings_collapse"])
        osc = payload["candidate_F"]["from_oscillator_and_teleology"]
        self.assertEqual(osc["verdict"], "fail")
        self.assertFalse(osc["beats_null"])


if __name__ == "__main__":
    unittest.main()
