"""Attack 9B original JSON sits. Finite max K is not a kill. ★ open."""

from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.attack9b_exact_shell_K import (  # noqa: E402
    K_of_w,
    build_exact_shell_field,
    normalize_field,
)
from ns_attacks.stokes_moments import moments, sum_Tk  # noqa: E402

PAGE = ROOT / "docs" / "five-lane-export" / "ATTACK_9B.md"
JSON = ROOT / "results" / "ns_five_lane_2026-09-10" / "attack9b_exact_shell" / "attack9b.json"
SCRIPT = ROOT / "scripts" / "ns_attacks" / "attack9b_exact_shell_K.py"
SOT = ROOT / "docs" / "math" / "ns_attacks" / "ATTACK_9B_EXACT_SHELL_CLOSING.md"


class Attack9BTests(unittest.TestCase):
    def test_phone_page_and_script(self):
        text = PAGE.read_text()
        self.assertIn("max K", text)
        self.assertIn("0.641", text)
        self.assertIn("attack9b_exact_shell_K.py", text)
        self.assertIn("NS not solved", text)
        self.assertIn("Freiman-AP", text)
        self.assertTrue(SCRIPT.is_file())
        sot = SOT.read_text()
        self.assertIn("K_{\\alpha,\\beta}", sot)
        self.assertIn("results/ns_five_lane_2026-09-10/attack9b_exact_shell", sot)

    def test_original_json_max_K_and_controls(self):
        data = json.loads(JSON.read_text())
        self.assertEqual(data["attack"], "9B")
        self.assertIs(data["ns_solved"], False)
        self.assertEqual(data["lemma_star"], "OPEN")
        self.assertEqual(data["kill_lane"], "LIVE")
        self.assertIs(data["controls_all_pass"], True)
        self.assertIs(data["eps_limit_all_pass"], True)
        mk = data["max_K"]
        self.assertEqual(mk["alpha"], 4)
        self.assertEqual(mk["beta"], 8)
        self.assertAlmostEqual(mk["K"], 0.6410131735094131, places=10)
        pair = next(p for p in data["per_pair"] if p["alpha"] == 4 and p["beta"] == 8)
        self.assertTrue(pair["eps_limit"]["limit_ok"])
        self.assertTrue(pair["controls"]["controls_pass"])
        self.assertLess(pair["eps_limit"]["rel_err_at_smallest_eps"], 1e-4)

    def test_exact_shell_K_finite_and_sum_Tk(self):
        import numpy as np

        modes = [(2, 0, 0), (0, 2, 0), (0, 0, 2)]
        amps = np.ones(3)
        thetas = np.array([0.2, 0.7, 1.1])
        phis = np.array([0.1, 0.4, 0.9])
        w = normalize_field(build_exact_shell_field(modes, amps, thetas, phis))
        m = moments(w)
        self.assertLess(abs(m["Ds"]), 1e-10)
        self.assertLess(abs(sum_Tk(w)), 1e-10)
        info = K_of_w(w, 4.0, 8.0)
        self.assertTrue(np.isfinite(info["K"]))
        self.assertGreaterEqual(info["K"], 0.0)


if __name__ == "__main__":
    unittest.main()
