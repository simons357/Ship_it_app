"""Smoke tests for the unifier-program exercise."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from unifier_exercise import INPUTS, OBS, observed_row, realization  # noqa: E402


class UnifierExerciseTests(unittest.TestCase):
    def test_target_state_is_perfect_on_the_defined_score(self):
        row = observed_row()
        self.assertGreater(row["R"], 0.999)
        self.assertLess(row["chi_ext"], 1e-18)

    def test_hierarchy_mismatch_kills_external_success(self):
        row = dict(observed_row())
        row["log_hierarchy"] = OBS["log_hierarchy"] + 5.0
        r, chi_ext, _chi_int, r_ext = realization(row)
        self.assertGreater(chi_ext, 20.0)
        self.assertLess(r_ext, 1e-4)
        self.assertLess(r, r_ext + 1e-12)

    def test_sixteen_coordinates(self):
        self.assertEqual(len(INPUTS), 15)
        self.assertIn("R", observed_row())


if __name__ == "__main__":
    unittest.main()
