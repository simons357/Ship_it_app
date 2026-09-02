"""Subset lock-score sanity checks."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from unifier_combo import INPUTS, lock_score, r_batch, sample_matrix  # noqa: E402


class UnifierComboTests(unittest.TestCase):
    def test_locking_everything_gives_almost_one(self):
        rng = np.random.default_rng(0)
        base = sample_matrix(32, rng)
        r = lock_score(base, tuple(INPUTS))
        self.assertGreater(r, 0.999)

    def test_locking_the_two_hierarchies_beats_baseline(self):
        rng = np.random.default_rng(0)
        base = sample_matrix(64, rng)
        base_r = float(np.mean(r_batch(base)))
        locked = lock_score(base, ("log_hierarchy", "log_cc_ratio"))
        self.assertGreater(locked, base_r)


if __name__ == "__main__":
    unittest.main()
