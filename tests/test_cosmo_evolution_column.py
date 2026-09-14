#!/usr/bin/env python3
"""Honesty checks for the Cosmic Graffiti Cosmo Evolution beat.

This is a magazine-column guard, not live Domain Architect mathematics.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
COLUMN = ROOT / "docs" / "cosmic-graffiti" / "cosmo-evolution.md"
MARK = ROOT / "docs" / "cosmic-graffiti" / "assets" / "cosmo-evolution-three-drawers.jpg"
LIVE = ROOT / "domain_architect"


class TestCosmoEvolutionColumn(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.text = COLUMN.read_text(encoding="utf-8")
        cls.lower = cls.text.lower()

    def test_standing_file_and_column_mark_exist(self) -> None:
        self.assertTrue(COLUMN.is_file(), COLUMN)
        self.assertTrue(MARK.is_file(), MARK)
        self.assertGreater(MARK.stat().st_size, 10_000)

    def test_one_magazine_identity(self) -> None:
        self.assertIn("Cosmic Graffiti", self.text)
        self.assertIn("https://cosmic-graffiti-magazine.vercel.app/", self.text)
        self.assertIn("Cosmo Evolution is a Cosmic Graffiti beat", self.text)
        self.assertIn("This is the magazine", self.text)
        self.assertIn("Live lab remains Domain Architect", self.text)

    def test_three_drawers_named_and_not_mixed(self) -> None:
        for name in ("THE SKY", "THE ATTEMPT", "PULLED BACK"):
            self.assertIn(name, self.text)
        self.assertIn("Never mixed into one theorem", self.text)
        self.assertIn("three drawers", self.lower)

    def test_retraction_what_remains_pointer(self) -> None:
        self.assertIn("QNM_ZETA_WHAT_REMAINS.md", self.text)
        self.assertIn("docs/archive/hb-ringdown/QNM_ZETA_WHAT_REMAINS.md", self.text)
        self.assertIn("26 August", self.text)
        self.assertIn("retracted", self.lower)
        self.assertIn("withdrawn", self.lower)

    def test_sky_drawer_facts(self) -> None:
        self.assertIn("a(t)", self.text)
        self.assertIn(r"n \approx 0,1", self.text)
        self.assertIn("monodromy", self.lower)
        self.assertIn("Motl", self.text)
        self.assertIn("**not** the prime-counting function", self.lower)
        self.assertIn("Berti", self.text)
        self.assertIn("data/qnm_events.csv", self.text)

    def test_attempt_inventory_cites_archive(self) -> None:
        self.assertIn("QNM_Prime_Zeta_DA_Analysis_2026-08.md", self.text)
        self.assertIn("Prime Number Distribution in Black Hole", self.text)
        self.assertIn("primes → zeta", self.text)
        self.assertIn("docs/archive/", self.text)

    def test_pulled_back_experiment_01_and_breathing(self) -> None:
        self.assertIn("Experiment 01 is **closed**", self.text)
        self.assertIn("not** reject", self.lower)
        self.assertIn("prime-neighbor", self.lower)
        self.assertIn("not supported", self.lower)
        self.assertIn("Horizon spectral zeta was not computed", self.text)
        self.assertIn("does not see", self.lower)
        self.assertIn("n\\to\\infty", self.text)
        self.assertIn("SFE breathing", self.text)
        self.assertIn(r"not \(a(t)\)", self.text)

    def test_news_first_then_comment(self) -> None:
        self.assertIn("Print the measurement first", self.text)
        self.assertIn("Then Cosmo Evolution commentary", self.text)
        self.assertIn("Virgo", self.text)
        self.assertIn(
            "https://www.virgo-gw.eu/news/the-new-ligo-virgo-kagra-catalog-sets-new-records-in-precision-gravitational-astronomy/",
            self.text,
        )
        lead_at = self.text.index("Frequency lead (measurement, drawer 1)")
        comment_at = self.text.index("Cosmo Evolution comment (after)")
        self.assertLess(lead_at, comment_at)

    def test_vault_requires_split_note(self) -> None:
        self.assertIn("if and only if", self.lower)
        self.assertIn("Honesty is the product", self.text)
        self.assertIn("must travel", self.lower)

    def test_ask_the_desk_does_not_resurrect_arrow(self) -> None:
        self.assertIn("Ask the Desk", self.text)
        self.assertIn("must not resurrect the prime–QNM arrow as a theorem", self.text)

    def test_not_live_da(self) -> None:
        self.assertIn("Not Domain Architect", self.text)
        self.assertIn("DECOMPOSE → CROSS-DOMAIN TRANSLATE → SYNTHESIZE", self.text)
        self.assertIn("Do **not** file this beat under `domain_architect/`", self.text)
        self.assertFalse((LIVE / "cosmo_evolution.py").is_file())
        self.assertFalse((LIVE / "qnm_zeta.py").is_file())
        self.assertFalse((LIVE / "sfe.py").is_file())

    def test_hubble_h0_not_glued_to_experiment_null(self) -> None:
        self.assertIn("Two different", self.text)
        self.assertIn("Hubble", self.text)
        self.assertIn("Experiment 01", self.text)
        self.assertIn("Same letters. Different jobs.", self.text)

    def test_shelf_book_is_not_canon(self) -> None:
        self.assertIn("unknown provenance", self.lower)
        self.assertIn("Do not import it as Cosmo Evolution canon", self.text)

    def test_no_prize_talk_and_no_false_closes(self) -> None:
        self.assertNotIn("clay", self.lower)
        self.assertNotIn("prize", self.lower)
        self.assertNotIn("millennium", self.lower)
        self.assertNotRegex(self.lower, r"primes prove")
        self.assertNotRegex(self.lower, r"navier[–-]stokes solved")
        self.assertNotRegex(self.lower, r"\bns solved\b")
        self.assertNotRegex(self.lower, r"rh proved")
        self.assertNotRegex(self.lower, r"riemann hypothesis (is )?proved")
        self.assertNotRegex(self.lower, r"we prove")
        # Prohibitions may mention regularity; they must not declare a close.
        self.assertIsNone(
            re.search(r"(?<!not a close of )(?<!do not claim )navier[–-]stokes regularity is", self.lower)
        )

    def test_empty_trays_and_blurb_present(self) -> None:
        self.assertIn("Empty trays", self.text)
        self.assertIn("Paste-ready Substack / Skool blurb", self.text)
        self.assertIn("First column", self.text)
        self.assertIn("What Cosmo Evolution is (and is not)", self.text)


if __name__ == "__main__":
    unittest.main()
