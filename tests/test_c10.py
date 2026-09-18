"""Lock the C-10 phone card: (A) unseated, Route A parked, leftover 5 open."""

from __future__ import annotations

import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
CARD = ROOT / "docs" / "C10.md"
DATA = ROOT / "data" / "c10" / "2026-09-18.json"
README = ROOT / "README.md"
NS_REVIEW = ROOT / "docs" / "ns-review" / "README.md"

FORBIDDEN_CLAIMS = (
    "NS is solved",
    "Clay is solved",
    "almost proved",
    "leftover 5 closed",
    "C10 produces (A)",
)


class TestC10PhoneCard(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.card = CARD.read_text(encoding="utf-8")
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_sources_present(self) -> None:
        self.assertTrue(CARD.is_file())
        self.assertTrue(DATA.is_file())

    def test_machine_lock(self) -> None:
        self.assertEqual(self.data["id"], "C10")
        self.assertFalse(self.data["headline"])
        self.assertFalse(self.data["scoreboard"])
        self.assertFalse(self.data["closes_regularity"])
        self.assertEqual(self.data["clay_b"], "open")
        self.assertFalse(self.data["produces_A"])
        self.assertFalse(self.data["closer_than_bkm"])
        self.assertFalse(self.data["leftover_5_closed"])
        self.assertEqual(self.data["status"], "parked")
        self.assertEqual(self.data["arrow2"], "unresolved")
        self.assertEqual(self.data["energy_linear_A"], "false")
        self.assertEqual(self.data["route_A"], "parked")
        self.assertEqual(self.data["route_A1"]["verdict"], "UNRESOLVED")
        self.assertTrue(self.data["route_A1"]["no_noncircular_int_a_plus"])
        self.assertEqual(self.data["route_A1"]["next"], "Route B")
        self.assertFalse(self.data["independence"]["persistence_P"])
        self.assertEqual(self.data["independence"]["theorem_H"], "withdrawn")
        self.assertIn("grad_u_infinity", self.data["refused_repairs"])
        self.assertIn("merge_with_Tc_without_inequality", self.data["refused_repairs"])
        self.assertIn("A2_staircase", self.data["refused_repairs"])

    def test_card_states_A_and_failed_arrow(self) -> None:
        self.assertIn("(A), verbatim", self.card)
        self.assertIn(r"(T_{j\leftarrow j})_+", self.card)
        self.assertIn("Failed arrow", self.card)
        self.assertIn(r"a_+", self.card)
        self.assertIn("C10 does not produce (A)", self.card)
        self.assertIn("leftover stays OPEN", self.card)
        self.assertIn("park Route A", self.card)
        self.assertIn("No A2 staircase", self.card)
        self.assertIn("Move to Route B", self.card)

    def test_card_refuses_repairs_and_merges(self) -> None:
        self.assertIn(r"\|\nabla u\|_\infty", self.card)
        self.assertIn("Do not merge the lanes", self.card)
        self.assertIn("Do not repair Theorem H", self.card)
        self.assertIn("Energy-linear (A) is **false**", self.card)
        self.assertIn("Same unresolved hope in different clothes", self.card)

    def test_card_does_not_claim_a_close(self) -> None:
        for phrase in FORBIDDEN_CLAIMS:
            self.assertNotIn(phrase, self.card)
        self.assertIn("NS not solved", self.card)
        self.assertIn("Clay Statement B open", self.card)

    def test_pointers_from_index_pages(self) -> None:
        readme = README.read_text(encoding="utf-8")
        ns_review = NS_REVIEW.read_text(encoding="utf-8")
        self.assertIn("docs/C10.md", readme)
        self.assertIn("C-10", readme)
        self.assertIn("../C10.md", ns_review)
        self.assertIn("Route A parked", ns_review)


if __name__ == "__main__":
    unittest.main()
