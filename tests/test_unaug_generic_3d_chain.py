"""Lock the 11 Sep 2026 unaugmented generic 3-D NS proof chain.

Lemma Star is finished bookkeeping. The remainder is T_{j←j}.
Generic regularity is not claimed. Swirl is not Step 7.
"""

from __future__ import annotations

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CHAIN = ROOT / "docs" / "ns-review" / "UNAUG-GENERIC-3D-PROOF-CHAIN.md"
SWIRL = ROOT / "docs" / "SWIRL_AXIAL_REDUCTION.md"
PROGRESS = ROOT / "docs" / "NS3D_PROGRESS_NOTE.md"
POST = ROOT / "docs" / "PROGRESS_POST.md"
HONESTY = ROOT / "docs" / "ns-review" / "UNAUG-PROOF-CHAIN.md"
DATA = ROOT / "data" / "ns_proof_chain" / "2026-09-11.json"
NS_REVIEW = ROOT / "docs" / "ns-review" / "README.md"
README = ROOT / "README.md"
PHI_KEEP = ROOT / "docs" / "ns-review" / "PHI-RENORM-WHAT-IS-KEPT.md"

FORBIDDEN_CLAIMS = (
    "NS is solved",
    "Clay is solved",
    "Clay Statement B is proved",
    "global regularity is proved",
    "almost proved",
)


class TestUnaugGeneric3dChain(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.chain = CHAIN.read_text(encoding="utf-8")
        cls.swirl = SWIRL.read_text(encoding="utf-8")
        cls.progress = PROGRESS.read_text(encoding="utf-8")
        cls.post = POST.read_text(encoding="utf-8")
        cls.honesty = HONESTY.read_text(encoding="utf-8")
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_sources_present(self) -> None:
        self.assertTrue(CHAIN.is_file())
        self.assertTrue(SWIRL.is_file())
        self.assertTrue(PROGRESS.is_file())
        self.assertTrue(POST.is_file())
        self.assertTrue(HONESTY.is_file())
        self.assertTrue(DATA.is_file())

    def test_machine_lock(self) -> None:
        self.assertEqual(self.data["id"], "unaug_generic_3d_proof_chain")
        self.assertEqual(self.data["date"], "2026-09-11")
        self.assertFalse(self.data["headline"])
        self.assertFalse(self.data["scoreboard"])
        self.assertFalse(self.data["closes_regularity"])
        self.assertEqual(self.data["clay_b"], "not_claimed")
        self.assertFalse(self.data["scope"]["augmentation"])
        self.assertFalse(self.data["scope"]["force"])
        self.assertFalse(self.data["scope"]["q_operator"])
        self.assertEqual(self.data["lemma_star"]["status"], "finished")
        self.assertEqual(self.data["lemma_star"]["kind"], "bookkeeping_identity")
        self.assertFalse(self.data["lemma_star"]["controls_Lambda"])
        self.assertFalse(self.data["lemma_star"]["bounds_Tc"])
        self.assertFalse(self.data["lemma_star"]["is_ratio_bound_Rstar"])
        self.assertEqual(self.data["remainder"], "T_j_leftarrow_j")
        self.assertFalse(self.data["A_proved"])
        self.assertFalse(self.data["B_proved"])
        self.assertTrue(self.data["C_is_subclass"])
        self.assertFalse(self.data["swirl_is_step_7"])
        self.assertEqual(
            self.data["rho_j_lt_nu"]["belongs_to"],
            "A_enstrophy_palinstrophy",
        )
        self.assertFalse(
            self.data["rho_j_lt_nu"]["is_shell_energy_absorption_into_nu_Zj"]
        )
        self.assertFalse(self.data["rho_j_lt_nu"]["proved_for_generic_data"])
        self.assertFalse(self.data["cross_scale_bounds_supplied"])
        self.assertFalse(self.data["measurements"]["are_theorems"])
        self.assertFalse(self.data["measurements"]["pass_to_Kmax_infinity"])
        self.assertFalse(self.data["measurements"]["pass_to_generic_data"])
        self.assertFalse(self.data["measurements"]["occupancy_1_is_depletion"])
        self.assertFalse(self.data["measurements"]["alignment_half_is_depletion"])
        self.assertEqual(
            self.data["forbidden_in_remainder_bound"],
            ["dot_e_j", "dot_Z", "Lambda_prime"],
        )
        self.assertEqual(self.data["steps"]["0_energy"], "closed")
        self.assertEqual(self.data["steps"]["1_lemma_star"], "finished_bookkeeping")
        self.assertEqual(self.data["steps"]["5_A_or_B"], "not_proved_generic_3d")
        self.assertEqual(
            self.data["steps"]["6_absorb_BKM"],
            "shape_only_hypothesis_missing",
        )

    def test_claim_line(self) -> None:
        self.assertIn("Lemma Star is in the generic 3-D chain and is finished", self.chain)
        self.assertIn(r"T_{j\leftarrow j}", self.chain)
        self.assertIn("Generic unaugmented 3-D regularity is not claimed", self.chain)
        self.assertIn("not a proof of global regularity", self.chain)

    def test_scope_is_classical_unaugmented(self) -> None:
        self.assertIn("No extra field", self.chain)
        self.assertIn("No force", self.chain)
        self.assertIn(r"No \(Q\)-operator", self.chain)
        self.assertIn(r"\mathbb{T}^3", self.chain)
        self.assertIn(r"\mathbb{R}^3", self.chain)

    def test_lemma_star_is_bookkeeping_not_a_bound(self) -> None:
        self.assertIn("This is bookkeeping", self.chain)
        self.assertIn("It is not a bound on", self.chain)
        self.assertIn(r"\omega_\ast", self.chain)
        self.assertIn("Do not claim it controls", self.chain)
        lowered = self.chain.lower()
        self.assertIn("later unrestricted ratio bound", lowered)
        self.assertIn("bookkeeping", lowered)

    def test_energy_and_triads_kept(self) -> None:
        self.assertIn("Step 0", self.chain)
        self.assertIn("No remainder. Keep", self.chain)
        self.assertIn("closed as an identity", self.chain)
        self.assertIn("Do not bound", self.chain)
        self.assertIn(r"\Lambda'", self.chain)

    def test_remainder_and_missing_hypothesis(self) -> None:
        self.assertIn("Same-scale block", self.chain)
        self.assertIn("None of (A)–(B) is proved", self.chain)
        self.assertIn("The missing hypothesis is (A) or (B)", self.chain)
        self.assertIn("Lemma Star is used before (A), not instead of (A)", self.chain)
        self.assertIn(r"\dot e_j", self.chain)
        self.assertIn(r"\dot Z", self.chain)

    def test_rho_is_not_shell_energy_absorption(self) -> None:
        self.assertIn(r"\nu Z_j", self.chain)
        self.assertIn("not an absorption criterion", self.chain)
        self.assertIn("enstrophy–palinstrophy", self.chain)
        self.assertIn("does not close", self.chain)
        self.assertIn("not supplied", self.chain)
        self.assertIn("not an absorption criterion", self.honesty)
        self.assertIn(r"\nu Z_j", self.honesty)
        self.assertIn("Not supplied", self.honesty)
        self.assertIn("not absorption into the shell-energy viscous term", self.post)

    def test_measurements_are_not_theorems(self) -> None:
        self.assertIn("not theorems", self.chain)
        self.assertIn(r"10^{-16}", self.chain)
        self.assertIn("Occupancy", self.chain)
        self.assertIn(r"\approx 1/2", self.chain)
        self.assertIn("do not pass to", self.chain)
        self.assertIn("Phase lock and geometric depletion are different facts", self.progress)
        self.assertIn("not theorems", self.progress)
        self.assertIn("do not pass to", self.progress)

    def test_swirl_is_not_step_7(self) -> None:
        self.assertIn("not a step in this chain", self.chain)
        self.assertIn("Do not insert it as", self.chain)
        self.assertIn("not Step 7", self.swirl)
        self.assertIn("subclass", self.swirl)
        self.assertIn(r"T_{\mathrm{ax}}", self.swirl)
        self.assertIn(r"F=u^\theta/r", self.swirl)
        self.assertIn(r"G=\omega^\theta/r", self.swirl)
        self.assertIn("Young", self.swirl)
        self.assertNotIn("Step 7 of generic 3-D is swirl", self.chain)

    def test_public_language_does_not_overclaim(self) -> None:
        self.assertIn("not a proof of global regularity", self.post)
        self.assertIn("Lemma Star", self.post)
        self.assertIn("bookkeeping", self.post)
        self.assertIn(r"T_{j\leftarrow j}", self.post)
        self.assertIn("not claimed", self.post)
        self.assertIn("subclass", self.post)

    def test_pages_refuse_false_closes(self) -> None:
        for text in (self.chain, self.swirl, self.progress, self.post, self.honesty):
            for phrase in FORBIDDEN_CLAIMS:
                self.assertNotIn(phrase, text)

    def test_index_pages_point_here(self) -> None:
        ns_review = NS_REVIEW.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        keep = PHI_KEEP.read_text(encoding="utf-8")
        self.assertIn("UNAUG-GENERIC-3D-PROOF-CHAIN.md", ns_review)
        self.assertIn("UNAUG-PROOF-CHAIN.md", ns_review)
        self.assertIn("UNAUG-GENERIC-3D-PROOF-CHAIN.md", readme)
        self.assertIn("not Step 7", ns_review)
        self.assertIn("SWIRL_AXIAL_REDUCTION.md", keep)


if __name__ == "__main__":
    unittest.main()
