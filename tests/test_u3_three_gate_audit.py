"""Lock the 2 Oct 2026 ||u||_3 three-gate audit.

The ||u||_3 derivation is not present. Do not invent it.
Existing ||∇u||_3 work is a different object; ∫g², if assumed, is BdV (2,3).
"""

from __future__ import annotations

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "ns-review" / "U3-THREE-GATE-AUDIT.md"
DATA = ROOT / "data" / "ns_proof_chain" / "u3-three-gate-2026-10-02.json"
CHAIN = ROOT / "docs" / "ns-review" / "UNAUG-GENERIC-3D-PROOF-CHAIN.md"
HONESTY = ROOT / "docs" / "ns-review" / "UNAUG-PROOF-CHAIN.md"
NS_REVIEW = ROOT / "docs" / "ns-review" / "README.md"

FORBIDDEN_CLAIMS = (
    "NS is solved",
    "Clay is solved",
    "||u||_3 derivation is proved",
    "new regularity mechanism is proved",
)


class TestU3ThreeGateAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.audit = AUDIT.read_text(encoding="utf-8")
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_sources_present(self) -> None:
        self.assertTrue(AUDIT.is_file())
        self.assertTrue(DATA.is_file())
        self.assertTrue(CHAIN.is_file())
        self.assertTrue(HONESTY.is_file())

    def test_machine_lock(self) -> None:
        self.assertEqual(self.data["id"], "u3_three_gate_audit")
        self.assertEqual(self.data["date"], "2026-10-02")
        self.assertFalse(self.data["headline"])
        self.assertFalse(self.data["closes_regularity"])
        self.assertEqual(self.data["clay_b"], "not_claimed")
        self.assertFalse(self.data["u3_derivation_present"])
        self.assertTrue(self.data["do_not_invent_u3_derivation"])
        self.assertEqual(
            self.data["attack_surface_when_back"],
            "implication_chain_not_just_algebra",
        )
        self.assertTrue(self.data["gates"]["2_regularity_value"]["q3_forces_p_infinity"])
        self.assertTrue(
            self.data["gates"]["2_regularity_value"]["nabla_u_3_in_L2_t_is_bdv_2_3"]
        )
        self.assertFalse(
            self.data["gates"]["2_regularity_value"][
                "assuming_known_class_is_new_mechanism"
            ]
        )
        self.assertFalse(self.data["existing_nabla_u_3"]["is_the_u3_derivation"])
        self.assertEqual(self.data["existing_nabla_u_3"]["int_g2_dt"], "open")
        self.assertEqual(
            self.data["existing_nabla_u_3"]["int_g2_if_assumed"],
            "Beirao_da_Veiga_2_3_reformulation",
        )

    def test_three_gates_named(self) -> None:
        self.assertIn("Gate 1 — Derivation", self.audit)
        self.assertIn("Gate 2 — Regularity value", self.audit)
        self.assertIn("Gate 3 — Novelty", self.audit)
        self.assertIn("cutoff-uniform", self.audit)
        self.assertIn("no hidden higher norm", self.audit)
        self.assertIn("Escauriaza–Seregin–Šverák", self.audit)
        self.assertIn(r"L^\infty_t L^3_x", self.audit)
        self.assertIn(r"\frac2p+\frac3q=1", self.audit)
        self.assertIn("Beirão da Veiga", self.audit)

    def test_u3_derivation_not_invented(self) -> None:
        self.assertIn("not in this deposit", self.audit)
        self.assertIn("Do not invent it", self.audit)
        self.assertIn("not back", self.audit)
        self.assertIn("implication chain", self.audit)

    def test_microscope_and_scaling(self) -> None:
        self.assertIn("growth-capable portion", self.audit)
        self.assertIn("without first assuming", self.audit)
        self.assertIn("reformulation, not a new regularity mechanism", self.audit)
        self.assertIn(r"p=\infty", self.audit)
        self.assertIn(r"(p,q)=(2,3)", self.audit)
        self.assertIn("Kato 1984", self.audit)

    def test_nabla_u3_is_not_relabelled(self) -> None:
        self.assertIn(r"g=\|\nabla u\|_3", self.audit)
        self.assertIn("not", self.audit)
        self.assertIn("Do not relabel", self.audit)
        self.assertIn("KILLED", self.audit)
        self.assertIn("proved implication", self.audit)

    def test_pages_refuse_false_closes(self) -> None:
        for phrase in FORBIDDEN_CLAIMS:
            self.assertNotIn(phrase, self.audit)

    def test_index_points_here(self) -> None:
        ns_review = NS_REVIEW.read_text(encoding="utf-8")
        self.assertIn("U3-THREE-GATE-AUDIT.md", ns_review)
        self.assertIn("not back", ns_review)


if __name__ == "__main__":
    unittest.main()
