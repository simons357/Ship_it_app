"""Lock the 16 Sep 2026 NS endgame notes: gaps named, no close."""

from __future__ import annotations

import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
NOTES = ROOT / "docs" / "NS-ENDGAME-NOTES.md"
DATA = ROOT / "data" / "ns_endgame" / "2026-09-16.json"
SVG = ROOT / "docs" / "ns-endgame" / "gaps.svg"

FORBIDDEN = ("clay", "prize", "qed", "solved")


class TestNsEndgameNotes(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.notes = NOTES.read_text(encoding="utf-8")
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))

    def test_sources_present(self) -> None:
        self.assertTrue(NOTES.is_file())
        self.assertTrue(DATA.is_file())
        self.assertTrue(SVG.is_file())

    def test_working_notes_not_a_headline(self) -> None:
        self.assertFalse(self.data["headline"])
        self.assertFalse(self.data["scoreboard"])
        self.assertFalse(self.data["closes_regularity"])
        self.assertIn("In the file, not the headline", self.notes)
        self.assertIn("Working notes", self.notes)
        self.assertIn("does not close the regularity statement", self.notes.lower())

    def test_scope_is_classical_unaugmented(self) -> None:
        self.assertTrue(self.data["scope"]["A_is_not_B"])
        self.assertEqual(self.data["scope"]["catalog"], "B_regularity")
        self.assertIn("classical unaugmented Navier–Stokes", self.notes)
        self.assertIn("A is not B", self.notes)

    def test_three_gaps(self) -> None:
        ids = [g["id"] for g in self.data["gaps"]]
        self.assertEqual(
            ids,
            ["uniform_triadic_bound", "m_half_heuristic", "H1_cylinder"],
        )
        self.assertEqual(self.data["gaps"][0]["status"], "not_a_theorem")
        self.assertTrue(self.data["gaps"][0]["load_bearing"])
        self.assertEqual(self.data["gaps"][1]["status"], "unresolved")
        self.assertFalse(self.data["gaps"][1]["lattice_realization"])
        self.assertFalse(self.data["gaps"][2]["folded_into_main_line"])
        self.assertIn("Uniform triadic bound is not a theorem", self.notes)
        self.assertIn("no lattice realization", self.notes)
        self.assertIn("H1 on the cylinder is a separate track", self.notes)

    def test_exhaustion_is_not_more_cases(self) -> None:
        self.assertIn("covering", self.data["exhaustion_routes"][0])
        self.assertIn("A case list is necessary and not sufficient", self.notes)
        self.assertIn("More case-work does not exhaust the space", self.notes)

    def test_refused_glue(self) -> None:
        refused = set(self.data["refused_glue"])
        self.assertIn("q6_to_track_b", refused)
        self.assertIn("ring_as_sitting_lemma", refused)
        self.assertIn("phi_renorm_to_regularity", refused)
        self.assertIn("case_list_as_covering", refused)
        self.assertIn("Do not glue slot Q into Track B", self.notes)
        self.assertIn("Ring is REPAIR", self.notes)
        self.assertIn("Barrier", self.notes)
        self.assertIn("SND sitting is not a bound on", self.notes)

    def test_cstar_not_confused_with_attack2(self) -> None:
        self.assertIn("attack2_Cstar_as_coprime_cstar", self.data["refused_glue"])
        self.assertIn("not Attack-2", self.notes)

    def test_public_notes_avoid_banned_claim_words(self) -> None:
        text = self.notes.lower()
        for word in FORBIDDEN:
            self.assertNotRegex(
                text,
                rf"\b{re.escape(word)}\b",
                msg=f"notes contain banned claim word {word!r}",
            )
        blob = json.dumps(self.data).lower()
        for word in FORBIDDEN:
            self.assertNotRegex(blob, rf"\b{re.escape(word)}\b")
        svg = SVG.read_text(encoding="utf-8").lower()
        for word in FORBIDDEN:
            self.assertNotRegex(svg, rf"\b{re.escape(word)}\b")


if __name__ == "__main__":
    unittest.main()
