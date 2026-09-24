"""Honesty locks and machine checks for the 20 Sep Fourier-triangle audit."""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from fourier_triangles_audit import (  # noqa: E402
    prove_S_decomposition,
    prove_all,
    prove_cosine_example,
    prove_equal_length_form,
    prove_even_output_sum,
    prove_hilbert_regressions,
    prove_16_9_polynomial,
    prove_shear_ratio,
    prove_unequal_defect,
)

PACKET = ROOT / "packets" / "FOURIER-TRIANGLES-AUDIT-2026-09-20.md"
LOCK = ROOT / "data" / "fourier_triangles_audit_2026-09-20.json"


class TestFourierTrianglesAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = PACKET.read_text(encoding="utf-8")
        cls.lock = json.loads(LOCK.read_text(encoding="utf-8"))
        cls.proofs = prove_all()

    def test_open_locks(self) -> None:
        self.assertFalse(self.lock["ns_solved"])
        self.assertEqual(self.lock["da_ns_2"], "OPEN")
        self.assertEqual(self.lock["missing_theorem_17"], "OPEN")
        self.assertFalse(self.lock["W_ij_reconstructed"])
        self.assertTrue(self.lock["does_not_revert_to_census_only"])
        self.assertTrue(self.lock["does_not_alter_sbp_gate"])
        self.assertTrue(self.lock["does_not_alter_static_frontier"])
        self.assertIn("NS not solved", self.page)
        self.assertIn("has not been proved here", self.page)
        self.assertFalse(self.proofs["ns_solved"])
        self.assertEqual(self.proofs["missing_theorem_17"], "OPEN")

    def test_I3_is_realizability_not_remainder(self) -> None:
        self.assertIn("wavevectors", self.lock["I3_is"])
        self.assertIn("NS remainder", self.lock["I3_is_not"])
        self.assertIn("not velocity coefficients", self.page)
        self.assertFalse(self.proofs["I3_determines_amplitudes"])

    def test_does_not_ship_other_gates(self) -> None:
        self.assertFalse(
            (ROOT / "packets" / "DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md").exists()
        )
        self.assertFalse(
            (ROOT / "packets" / "DA-GATE-STATIC-FRONTIER-2026-09-24.md").exists()
        )

    def test_polarization_identities(self) -> None:
        s = prove_S_decomposition()
        self.assertTrue(s["S_identity"])
        self.assertTrue(s["p_on_shell"])
        self.assertTrue(s["div_free_p"])
        eq = prove_equal_length_form()
        self.assertTrue(eq["equal_length_normal_form"])
        self.assertTrue(eq["in_plane_cancels"])
        self.assertTrue(prove_unequal_defect()["defect_identity"])

    def test_weighted_arithmetic(self) -> None:
        self.assertTrue(prove_16_9_polynomial()["identity"])
        ev = prove_even_output_sum()
        self.assertTrue(ev["closed_form"])
        self.assertTrue(ev["numeric_a_1_to_8"])

    def test_hilbert_regressions(self) -> None:
        h = prove_hilbert_regressions()
        self.assertTrue(h["all_match_audit"])
        self.assertTrue(h["odd_alpha_monochromatic_impossible"])
        self.assertIn("Fails at", self.page)

    def test_finite_transfer_example(self) -> None:
        c = prove_cosine_example()
        self.assertTrue(c["all_match"])
        self.assertTrue(c["generated_mode_3_-2_0"]["matches_3i_e3"])

    def test_shear_field(self) -> None:
        sh = prove_shear_ratio()
        self.assertTrue(sh["E_is_3_over_2"])
        self.assertTrue(sh["twelve_nonzero"])
        self.assertTrue(sh["output_norm_3_over_4"])

    def test_routes_stay_distinct(self) -> None:
        self.assertFalse(self.lock["routes"]["equivalent"])
        self.assertIn("distinct sufficient routes", self.page)
        self.assertIn("Do not splice", self.page)
        self.assertTrue(self.lock["reported_not_rerun"]["S(1)"]["three_cutoffs_do_not_prove_uniformity"])


if __name__ == "__main__":
    unittest.main()
