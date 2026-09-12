"""9B counting: pairs per output ≤ m; K ≤ 16s. Fixed-s 9D excluded."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.attack9b_output_counting import (  # noqa: E402
    cs_rows,
    max_pairs_per_output,
    ordered_pairs_onto_k,
    random_exact_shell_w,
    run,
)
from ns_attacks.stokes_moments import enforce_reality, make_divfree_amp  # noqa: E402

DOC = ROOT / "docs" / "LEMMA-STAR-9B-COUNTING.md"


class CountingLockTests(unittest.TestCase):
    def test_doc_locks_the_exclusion(self):
        text = DOC.read_text()
        self.assertIn(r"most \(m\)", text)
        self.assertIn(r"K_{\alpha,\beta}(w)\le 16s", text)
        self.assertIn(r"C\frac{\alpha}{\sqrt{\beta}}", text)
        self.assertIn(r"Fixed \(s\)", text)
        self.assertIn("NS not solved", text)
        self.assertIn("**is this page** (9B uniform target)", text)
        self.assertIn("remaining packet falsifier", text)
        self.assertIn("Do not build a ★ sentence", text)
        self.assertNotIn("NS is solved", text)

    def test_9d_spec_does_not_claim_the_B_bound(self):
        stub = (ROOT / "docs" / "math" / "ns_attacks" / "ATTACK_9D_THETA_M2_LOCKED_PHASE.md").read_text()
        self.assertIn("do not implement this", stub.lower())
        self.assertIn("Freiman-AP", stub)
        grow = (ROOT / "docs" / "ATTACK-9D-GROW-S.md").read_text()
        self.assertIn("Historical", grow)
        self.assertIn("Full complex polarizations", grow)
        self.assertIn("frequency factors kept", grow.lower())
        self.assertIn(r"Same \(B\) as 9B", grow)

    def test_one_output_has_at_most_m_pairs(self):
        field = {}
        for k, seed in (
            ((1, 0, 0), (0.0, 1.0, 0.0)),
            ((0, 1, 0), (1.0, 0.0, 0.0)),
        ):
            field[k] = make_divfree_amp(k, seed)
        field = enforce_reality(field)
        support = list(field.keys())
        m = len(support)
        n = ordered_pairs_onto_k(support, (1, 1, 0))
        self.assertLessEqual(n, m)
        self.assertGreater(n, 0)
        best, m2 = max_pairs_per_output(support)
        self.assertEqual(m, m2)
        self.assertLessEqual(best, m)

    def test_K_le_16s_and_cs_on_random_shell(self):
        rng = np.random.default_rng(1390)
        w = random_exact_shell_w([(2, 0, 0), (0, 2, 0), (0, 0, 2)], rng)
        rec = cs_rows(w, 8.0)
        self.assertTrue(rec["pairs_le_m"])
        self.assertTrue(rec["cs_ok"])
        self.assertLessEqual(rec["cs_max_|B|/(|k|E)"], 1.0 + 1e-9)
        self.assertTrue(rec["K_le_16s"])
        self.assertTrue(rec["K_le_s_beta2_over_alpha2"])
        self.assertAlmostEqual(rec["sqrt_K"] ** 2, rec["K"], places=10)

    def test_small_sweep_does_not_break_inequalities(self):
        summary = run(seed=1390, n_trials=2)
        self.assertTrue(summary["pairs_at_most_m"])
        g = summary["growing"]
        self.assertEqual(g["n_fail_pairs_le_m"], 0)
        self.assertEqual(g["n_fail_cs"], 0)
        self.assertEqual(g["n_fail_K_le_16s"], 0)
        self.assertIs(summary["ns_solved"], False)
        self.assertEqual(summary["lemma_star"], "OPEN")
        self.assertTrue(summary["verdict"].startswith("FIXED_S_EXCLUDED"))


if __name__ == "__main__":
    unittest.main()
