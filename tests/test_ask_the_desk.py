#!/usr/bin/env python3
"""Ask the Desk Q&A tray: exists, live lab named, no fake closes."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DESK = ROOT / "docs" / "cosmic-graffiti" / "ask-the-desk.md"
PICTURE = ROOT / "docs" / "cosmic-graffiti" / "assets" / "ask-the-desk.png"
LIVE = ROOT / "domain_architect"

FORBIDDEN = (
    "NS solved",
    "ns solved",
    "RH proved",
    "rh proved",
    "we solved navier",
    "riemann hypothesis is proved",
    "millennium prize",
    "millennium-prize",
)

FAKE_CLOSES = (
    "navier–stokes is solved",
    "navier-stokes is solved",
    "ns is solved",
    "rh is proved",
    "sfe breathing φ is expansion",
    "sfe breathing phi is expansion",
)


def desk_text() -> str:
    return DESK.read_text(encoding="utf-8")


class TestAskTheDeskExists(unittest.TestCase):
    def test_standing_file_exists(self) -> None:
        self.assertTrue(DESK.is_file(), DESK)
        self.assertGreater(DESK.stat().st_size, 4000, DESK)

    def test_picture_exists_as_png(self) -> None:
        self.assertTrue(PICTURE.is_file(), PICTURE)
        self.assertGreater(PICTURE.stat().st_size, 20_000, PICTURE)
        self.assertEqual(PICTURE.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")


class TestAskTheDeskCopy(unittest.TestCase):
    def test_domain_architect_is_the_live_lab(self) -> None:
        text = desk_text()
        self.assertIn("Domain Architect", text)
        self.assertIn("live", text.lower())
        self.assertIn("DECOMPOSE", text)
        self.assertIn("CROSS-DOMAIN TRANSLATE", text)
        self.assertIn("SYNTHESIZE", text)
        self.assertIn("magazine is the public table", text.lower())

    def test_identity_split(self) -> None:
        text = desk_text().lower()
        self.assertIn("cosmic graffiti", text)
        self.assertIn("the frequency", text)
        self.assertIn("ask the desk", text)
        self.assertIn("news desk", text)
        self.assertIn("q&a", text)

    def test_starter_questions_are_written(self) -> None:
        text = desk_text()
        self.assertIn("cream swirl in coffee", text.lower())
        self.assertIn("Navier–Stokes", text)
        self.assertIn("prime", text.lower())
        self.assertIn("night sky", text.lower())
        self.assertIn("a(t)", text)
        self.assertIn(r"\Phi = u_\theta/r", text)
        self.assertIn("golden ratio", text.lower())
        self.assertIn("What is Domain Architect?", text)

    def test_how_the_desk_works(self) -> None:
        text = desk_text().lower()
        self.assertIn("substack", text)
        self.assertIn("skool", text)
        self.assertIn("known", text)
        self.assertIn("open", text)
        self.assertIn("picture", text)
        self.assertIn("never fake a close", text)

    def test_empty_trays_and_skool_notes(self) -> None:
        text = desk_text()
        self.assertIn("Tray for Jon", text)
        self.assertIn("Tray for readers", text)
        self.assertIn("Ask us anything in this thread", text)
        self.assertIn("Example prompts", text)

    def test_answers_do_not_fake_a_close(self) -> None:
        text = desk_text()
        lower = text.lower().replace("–", "-")
        for needle in FORBIDDEN + FAKE_CLOSES:
            self.assertNotIn(needle.lower(), lower, needle)
        self.assertNotIn("Clay", text)
        self.assertNotIn("CLAY", text)

    def test_expansion_is_not_sfe_breathing(self) -> None:
        text = desk_text()
        self.assertIn("scale factor", text.lower())
        self.assertRegex(text, r"not.*SFE breathing")
        self.assertIn("challenge, not a pass", text.lower())

    def test_patents_remain_a_plan(self) -> None:
        text = desk_text().lower()
        self.assertIn("plan", text)
        self.assertIn("does not file patents", text)

    def test_live_python_untouched_by_this_tray(self) -> None:
        hits = []
        for path in LIVE.rglob("*.py"):
            body = path.read_text(encoding="utf-8")
            if any(tag in body for tag in ("NAV-42", "Fluid-Q", "Chat Vault", "2.2 Hz")):
                hits.append(path)
        self.assertEqual(hits, [])


if __name__ == "__main__":
    raise SystemExit(unittest.main())
