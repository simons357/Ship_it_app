"""Honesty locks for the 10 Sep Lemma★ shape-form lock."""

from __future__ import annotations

import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from lemma_star_shape_lock import (  # noqa: E402
    prove_Ds_equivalences,
    prove_all,
    prove_homogeneity,
    prove_single_shell_vacuous,
)

PACKET = ROOT / "packets" / "LEMMA-STAR-SHAPE-FORM-2026-09-10.md"
LOCK = ROOT / "data" / "lemma_star_shape_form_2026-09-10.json"


class TestLemmaStarShapeLock(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.page = PACKET.read_text(encoding="utf-8")
        cls.lock = json.loads(LOCK.read_text(encoding="utf-8"))
        cls.proofs = prove_all()

    def test_open_locks(self) -> None:
        self.assertFalse(self.lock["ns_solved"])
        self.assertEqual(self.lock["lemma_star"], "OPEN")
        self.assertEqual(self.lock["da_ns_2"], "OPEN")
        self.assertEqual(self.lock["kill_lane"], "LIVE")
        self.assertFalse(self.lock["kill_lane_closed"])
        self.assertTrue(self.lock["shape_not_viscosity"])
        self.assertFalse(self.lock["K_alpha_beta_is_full_lemma"])
        self.assertFalse(self.lock["legacy_ratio_star_is_R_star"])
        self.assertIn("NS is NOT solved", self.page)
        self.assertIn("does **not** prove", self.page)
        self.assertFalse(self.proofs["ns_solved"])

    def test_does_not_ship_other_gates(self) -> None:
        self.assertFalse(
            (ROOT / "packets" / "DA-GATE-RMS-CORE-TAIL-SBP-2026-09-24.md").exists()
        )
        self.assertFalse(
            (ROOT / "packets" / "FOURIER-TRIANGLES-AUDIT-2026-09-20.md").exists()
        )
        self.assertFalse(
            (ROOT / "packets" / "DA-GATE-STATIC-FRONTIER-2026-09-24.md").exists()
        )

    def test_signed_Im_stays_required(self) -> None:
        self.assertTrue(self.lock["do_not_replace_Im_by_abs"])
        self.assertIn("Do not", self.page)
        self.assertIn("absolute values", self.page)

    def test_Ds_equivalences(self) -> None:
        d = prove_Ds_equivalences()
        self.assertTrue(d["moment_vs_variance"])
        self.assertTrue(d["moment_vs_double"])
        self.assertTrue(d["moment_vs_two_shell"])
        self.assertTrue(d["nonnegative"])

    def test_homogeneity_and_dilation(self) -> None:
        h = prove_homogeneity()
        for key in (
            "Tc_scales_a3",
            "Ds_scales_a2",
            "E_scales_a2",
            "Y_scales_a2",
            "Lambda_invariant",
            "R_star_scale_invariant",
            "R_star_dilation_invariant",
            "legacy_ratio_star_is_not_invariant",
        ):
            self.assertTrue(h[key], key)

    def test_single_shell_is_vacuous(self) -> None:
        s = prove_single_shell_vacuous()
        self.assertTrue(s["Ds_zero"])
        self.assertTrue(s["Tc_plus_zero"])
        self.assertIn("vacuous", self.page)

    def test_kill_lane_not_closed(self) -> None:
        self.assertIn("The kill lane is closed", self.lock["retired_false"])
        self.assertIn("FALSE", self.page)
        self.assertIn("LIVE", self.page)
        self.assertIn("Do not splice", self.page)


if __name__ == "__main__":
    unittest.main()
