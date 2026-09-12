"""Attack 9D: growing supports, full complex pol, |k| kept. ★ open."""

from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.attack9d_growing import (  # noqa: E402
    build_full_complex_field,
    full_complex_pol,
    optimize_full_complex,
    run,
)
from ns_attacks.attack9b_exact_shell_K import (  # noqa: E402
    normalize_field,
    pol_from_angles,
)
from ns_attacks.stokes_moments import enforce_reality  # noqa: E402

DOC = ROOT / "docs" / "math" / "ns_attacks" / "ATTACK_9D_THETA_M2_LOCKED_PHASE.md"
GROW = ROOT / "docs" / "ATTACK-9D-GROW-S.md"
LIVE = ROOT / "docs" / "LEMMA-STAR-LIVE.md"
REASON = ROOT / "docs" / "LEMMA-STAR-REASON.md"
SCRIPT = ROOT / "scripts" / "ns_attacks" / "attack9d_growing.py"
SEATED = ROOT / "scripts" / "ns_attacks" / "attack9b_grow_s.py"


class Attack9DTests(unittest.TestCase):
    def test_desk_has_two_live_writes(self):
        live = LIVE.read_text()
        self.assertIn("Attack 9D", live)
        self.assertIn("full complex", live.lower())
        self.assertIn("map, not a theorem", live)
        self.assertIn("0.456", live)
        self.assertIn("NS not solved", live)
        self.assertNotIn("NS is solved", live)
        reason = REASON.read_text()
        self.assertIn("map, not a theorem", reason)
        self.assertIn("HH", reason)
        self.assertIn("occupancy", reason.lower())
        grow = GROW.read_text()
        self.assertIn("Remaining packet falsifier", grow)
        self.assertIn("attack9b_grow_s.py", grow)
        self.assertIn("0.456", grow)
        spec = DOC.read_text()
        self.assertIn("do not implement this", spec.lower())
        self.assertIn("Freiman-AP", spec)
        self.assertTrue(SEATED.is_file())
        self.assertTrue(SCRIPT.is_file())

    def test_full_complex_is_divfree_and_wider_than_linear(self):
        k = (2, 0, 0)
        v = full_complex_pol(k, 0.4, 0.2, 1.7)
        self.assertAlmostEqual(float(np.vdot(v, v).real), 1.0, places=10)
        self.assertAlmostEqual(abs(np.dot(np.array(k, dtype=float), v)), 0.0, places=10)
        # Elliptical (φ1≠φ2) is not a global phase times a real plane vector.
        lin = pol_from_angles(k, 0.4, 0.2)
        overlap = abs(np.vdot(v, lin))
        self.assertLess(overlap, 0.999)

    def test_optimize_tiny_keeps_inequalities_and_k(self):
        rng = np.random.default_rng(1390)
        modes = [(2, 0, 0), (0, 2, 0), (0, 0, 2)]
        rec = optimize_full_complex(modes, 8.0, rng, n_trials=4, n_refine=2)
        self.assertTrue(rec["K_le_16s"])
        self.assertTrue(rec["cs_ok"])
        self.assertTrue(rec["pairs_le_m"])
        self.assertGreaterEqual(rec["K"], 0.0)
        self.assertTrue(math.isfinite(rec["K"]))
        # Frequency factor kept: target ratio is √K, not ||ΠB||/α.
        self.assertAlmostEqual(rec["sqrt_K"] ** 2, rec["K"], places=8)

    def test_run_tiny(self):
        summary = run(seed=1390, n_random=1, n_opt_trials=0, n_opt_refine=0)
        self.assertEqual(summary["attack"], "9D-growing-full-complex")
        self.assertIs(summary["ns_solved"], False)
        self.assertEqual(summary["lemma_star"], "OPEN")
        self.assertEqual(summary["kill_lane"], "LIVE")
        self.assertEqual(summary["star_reason"], "NOT written")
        self.assertEqual(summary["frequency_factors"], "kept")
        self.assertEqual(summary["n_fail_K_le_16s"], 0)
        self.assertTrue(summary["verdict"].startswith("9D_SAMPLES_FINITE"))
        self.assertLess(summary["max_K"], 16.0 * max(summary["max_s"], 1))

    def test_results_json_is_not_a_kill(self):
        import json

        path = ROOT / "results" / "attack9d_growing" / "attack9d_growing.json"
        self.assertTrue(path.is_file())
        data = json.loads(path.read_text())
        self.assertEqual(data["attack"], "9D-growing-full-complex")
        self.assertIs(data["ns_solved"], False)
        self.assertEqual(data["lemma_star"], "OPEN")
        self.assertEqual(data["kill_lane"], "LIVE")
        self.assertEqual(data["star_reason"], "NOT written")
        self.assertEqual(data["frequency_factors"], "kept")
        self.assertLess(data["max_K"], 1.0)
        self.assertEqual(data["n_fail_K_le_16s"], 0)
        headline = (ROOT / "results" / "attack9d_growing" / "HEADLINE.md").read_text()
        self.assertIn("NOT written", headline)
        self.assertIn("0.612", headline)


if __name__ == "__main__":
    unittest.main()
