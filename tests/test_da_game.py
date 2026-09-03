"""Cooperative-game smoke tests."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from da_game import MUST_HIT, run  # noqa: E402


class DaGameTests(unittest.TestCase):
    def test_shapley_recovers_core_and_does_not_write_f(self):
        tmp = Path(tempfile.mkdtemp()) / "da_game_test.json"
        payload = run(n=40, n_perm=60, seed=1, out=tmp)
        self.assertIn("log_cc_ratio", payload["game_R"]["top4"])
        self.assertIn("log_hierarchy", payload["game_R"]["top4"])
        self.assertLess(payload["game_R"]["efficiency_err"], 0.05)
        self.assertIn("write F", payload["what_it_cannot_do"])
        for name in MUST_HIT:
            self.assertGreater(payload["game_U"]["shapley"][name], 0.0)
        self.assertEqual(payload["game_U"]["shapley"]["A_mean"], 0.0)


if __name__ == "__main__":
    unittest.main()
