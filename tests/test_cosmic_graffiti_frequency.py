#!/usr/bin/env python3
"""Honesty locks for the Cosmic Graffiti / Frequency working chapter.

Cheap copy tests. Not a physics engine. Not a paywall.
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CG = ROOT / "docs" / "cosmic-graffiti"
ISSUE = CG / "issues" / "2026-09-14-the-frequency.md"
SKOOL = CG / "issues" / "2026-09-14-skool-post.md"
README = CG / "README.md"
FEED = CG / "frequency" / "feed.json"
ASSETS = CG / "issues" / "assets"
TRAYS = CG / "issues" / "_trays"


def _strip_urls(text: str) -> str:
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


class TestCosmicGraffitiFiles(unittest.TestCase):
    def test_working_files_present(self) -> None:
        for path in (
            README,
            ISSUE,
            SKOOL,
            FEED,
            TRAYS / "jon-story.md",
            TRAYS / "photos.md",
            TRAYS / "later-frequency.md",
            TRAYS / "letters.md",
            ASSETS / "cg-frequency-masthead-2026-09-14.png",
            ASSETS / "cg-humor-letters-collide.png",
            ASSETS / "cg-around-us-coffee-swirl.png",
            ASSETS / "cg-frequency-mark.png",
            ASSETS / "cg-logo.webp",
        ):
            self.assertTrue(path.is_file(), f"missing {path}")

    def test_identity_is_one_magazine(self) -> None:
        readme = README.read_text(encoding="utf-8")
        issue = ISSUE.read_text(encoding="utf-8")
        self.assertIn("Cosmic Graffiti", readme)
        self.assertIn("The Frequency", readme)
        self.assertIn("not a second magazine", readme.lower() + " " + issue.lower())
        self.assertIn("Cosmic Graffiti", issue)
        self.assertIn("The Frequency", issue)
        self.assertNotIn("GRAFITTI", issue)


class TestFrequencySources(unittest.TestCase):
    def test_feed_items_have_https_urls(self) -> None:
        data = json.loads(FEED.read_text(encoding="utf-8"))
        items = data["items"]
        self.assertGreaterEqual(len(items), 3)
        self.assertLessEqual(len(items), 8)
        issue = ISSUE.read_text(encoding="utf-8")
        for item in items:
            self.assertTrue(str(item["href"]).startswith("https://"), item)
            self.assertGreaterEqual(len(item["sources"]), 1)
            for url in [item["href"], *item["sources"]]:
                self.assertTrue(str(url).startswith("https://"), url)
                self.assertIn(url, issue, f"chapter missing {url}")

    def test_chapter_names_the_live_product(self) -> None:
        issue = ISSUE.read_text(encoding="utf-8")
        self.assertIn("Domain Architect", issue)
        self.assertIn("DECOMPOSE", issue)
        self.assertIn("CROSS-DOMAIN TRANSLATE", issue)
        self.assertIn("SYNTHESIZE", issue)
        self.assertIn("accept grok table", issue)
        self.assertIn("shipped locally", issue)
        self.assertIn("not a public website", issue.lower())


class TestHonestyLocks(unittest.TestCase):
    def test_no_prize_packaging_in_prose(self) -> None:
        prose = _strip_urls(ISSUE.read_text(encoding="utf-8"))
        self.assertNotIn("Clay", prose)
        self.assertNotIn("Millennium Prize", prose)
        self.assertNotIn("millennium prize", prose.lower())

    def test_no_closed_theorems(self) -> None:
        issue = ISSUE.read_text(encoding="utf-8")
        prose = _strip_urls(issue).lower()
        self.assertIn("da-vc-01", prose)
        self.assertIn("fail", prose)
        self.assertNotIn("da-vc-01 as pass", prose)
        self.assertNotIn("da-vc-01 remains pass", prose)
        self.assertNotRegex(prose, r"navier[–\- ]stokes (is|are|was) solved")
        self.assertNotRegex(prose, r"regularity is (closed|proved|solved)")
        self.assertNotIn("we solved", prose)
        self.assertIn("not a claim that the riemann hypothesis is proved", prose)
        self.assertIn("does **not** certify", issue.lower() + issue)
        self.assertIn("does **not** certify", issue)

    def test_no_fake_paywall(self) -> None:
        issue = ISSUE.read_text(encoding="utf-8")
        skool = SKOOL.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        blob = f"{issue}\n{skool}\n{readme}".lower()
        self.assertIn("does **not** turn on a paywall", issue)
        self.assertIn("plan, not live", issue)
        self.assertNotIn("paywall is live", blob)
        self.assertNotIn("subscribe to unlock", blob)
        self.assertIn("do not:", skool.lower())
        self.assertIn("plan", skool.lower())

    def test_patents_are_archive_not_da_filings(self) -> None:
        issue = ISSUE.read_text(encoding="utf-8")
        readme = README.read_text(encoding="utf-8")
        self.assertIn("does **not** file patents", issue)
        self.assertIn("not suing", issue.lower())
        self.assertIn("**Not** DA filings", issue)
        self.assertNotIn("we patented the universe", issue.lower())
        self.assertNotIn("patented the universe", issue.lower())
        self.assertIn("does **not** file patents", readme)

    def test_shelf_book_is_not_live_theory(self) -> None:
        issue = ISSUE.read_text(encoding="utf-8")
        self.assertIn("unknown provenance", issue.lower())
        self.assertIn("shelf book", issue.lower())
        self.assertIn("not imported here", issue.lower())
        self.assertNotIn(
            "16228b707961bce72369a25446b3945ae2ceb5b1d6e78391a9a8dae912a25834",
            issue,
        )

    def test_letters_collide_humor(self) -> None:
        issue = ISSUE.read_text(encoding="utf-8")
        self.assertIn("## 5. Humor", issue)
        self.assertIn("SAME LETTER ≠ SAME OBJECT", issue)
        self.assertIn("cg-humor-letters-collide.png", issue)
        self.assertIn(r"\Phi = u_\theta/r", issue)

    def test_empty_trays_are_labeled(self) -> None:
        issue = ISSUE.read_text(encoding="utf-8")
        self.assertIn("## 8. Empty trays", issue)
        self.assertIn("8.1 Jon’s story", issue)
        self.assertIn("8.2 Photos", issue)
        self.assertIn("8.3 Later Frequency items", issue)
        jon = (TRAYS / "jon-story.md").read_text(encoding="utf-8")
        self.assertIn("empty", jon.lower())
        self.assertNotIn("once upon a time in childhood", jon.lower())


if __name__ == "__main__":
    raise SystemExit(unittest.main())
