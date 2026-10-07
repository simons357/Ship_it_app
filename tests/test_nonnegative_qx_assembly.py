"""First assembly test locks: nonnegative Q_x forces θ ≥ 1/2."""

from __future__ import annotations

import sys
import unittest
from math import isclose
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from ns_attacks.nonnegative_qx_assembly import report, single_triad_ratio, subnet_ratio
from ns_attacks.qx_kernel import C_abc, similar_seed_triad


class TestNonnegativeQxAssembly(unittest.TestCase):
    def test_C_abc_homogeneous_degree_three(self) -> None:
        _u, _v, _w, a, b, c = similar_seed_triad(4)
        C0 = C_abc(a, b, c)
        C1 = C_abc(4 * a, 4 * b, 4 * c)
        self.assertGreater(C0, 0.0)
        self.assertTrue(isclose(C1, 8.0 * C0, rel_tol=1e-12))

    def test_similar_triad_forces_theta_half(self) -> None:
        r4 = single_triad_ratio(4)
        r8 = single_triad_ratio(8)
        self.assertEqual(r8["Lambda"] / r4["Lambda"], 4)
        self.assertTrue(isclose(r8["C_abc"] / r4["C_abc"], 8.0, rel_tol=1e-12))
        self.assertTrue(isclose(r8["Omega"] / r4["Omega"], 4.0, rel_tol=1e-12))
        self.assertTrue(
            isclose(r8["Q2_over_Omega"] / r4["Q2_over_Omega"], 2.0, rel_tol=1e-9)
        )

    def test_report_locks(self) -> None:
        payload = report()
        lemma = payload["lemma_similar_triad"]
        self.assertTrue(lemma["C_scales_as_n3"])
        self.assertTrue(lemma["Omega_scales_as_n2"])
        self.assertTrue(lemma["ratio_scales_as_n"])
        self.assertTrue(lemma["theta_equals_half_on_this_family"])
        self.assertTrue(isclose(lemma["mean_theta_hat"], 0.5, rel_tol=1e-9, abs_tol=1e-9))
        locks = payload["locks"]
        self.assertTrue(locks["requires_theta_ge_half"])
        self.assertTrue(locks["theta_optimal_open"])
        self.assertTrue(locks["cannot_gain_by_regrouping_this_majorant"])
        self.assertTrue(locks["next_test_must_preserve_signed_cancellation"])
        self.assertFalse(locks["theta_proved_equal_half_uniformly"])
        self.assertFalse(locks["theorem_17_proved"])
        self.assertEqual(locks["gate_A"], "UNRESOLVED / DIAGNOSTIC ONLY")

    def test_subnet_cs_and_positive_Q(self) -> None:
        row = subnet_ratio(8)
        self.assertGreater(row["n_triads"], 0)
        self.assertTrue(row["cs_holds"])
        self.assertGreater(row["Q2_over_Omega"], 0.0)
        self.assertGreater(row["T_plus"], 0.0)

    def test_docs_state_the_lemma(self) -> None:
        note = (ROOT / "docs" / "GATE-B-SIGNED-CANCELLATION-TEST.md").read_text(
            encoding="utf-8"
        )
        self.assertTrue(r"\tfrac12" in note or "1/2" in note)
        self.assertIn("signed cancellation", note.lower())
        self.assertNotIn("NS is solved", note)
        self.assertIn("OPEN", note)
        src = (
            ROOT / "docs" / "GATE-B-SOURCE-ASSEMBLY-AND-CONCENTRATION-TEST.md"
        ).read_text(encoding="utf-8")
        self.assertIn(r"\theta\ge\tfrac12", src)


if __name__ == "__main__":
    unittest.main()
