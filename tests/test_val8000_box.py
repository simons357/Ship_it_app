#!/usr/bin/env python3
"""VAL8000 little box on the live magazine stack: not the lead, no fake theorems."""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MAG = ROOT / "docs" / "cosmic-graffiti" / "magazine"
COMMENTS = MAG / "val8000" / "val8000-comments.js"
BOX_JS = MAG / "val8000" / "val8000-box.js"
BOX_CSS = MAG / "val8000" / "val8000-box.css"
FEED = MAG / "frequency" / "feed.json"

PAGES = {
    "home": MAG / "index.html",
    "issue1": MAG / "issue1.html",
    "record": MAG / "for-the-record.html",
    "credit": MAG / "credit.html",
    "frequency": MAG / "frequency" / "index.html",
    "progress": MAG / "open-progress" / "index.html",
}

BANNED = (
    "HAL 9000",
    "HAL9000",
    "I'm sorry Dave",
    "I'm sorry, Dave",
    "pod bay",
    "Clay",
    "Millennium Prize",
    "millennium prize",
    "NAV-42",
    "Fluid-Q",
    "Chat Vault",
    "2.2 Hz",
    "val8000-mouth-teeth",
    "red lens is out",
    "ns solved",
    "RH proved",
    "riemann hypothesis is proved",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _magazine_blob() -> str:
    parts = [_read(p) for p in PAGES.values()]
    parts.append(_read(COMMENTS))
    parts.append(_read(BOX_JS))
    parts.append(_read(BOX_CSS))
    parts.append(_read(FEED))
    return "\n".join(parts)


class TestMagazineStillLooksLikeIssue1(unittest.TestCase):
    def test_home_lead_is_issue1_red_pills_not_val(self) -> None:
        home = _read(PAGES["home"])
        self.assertIn("<h1>Make science cool again</h1>", home)
        self.assertIn("Ten thousand agents", home)
        self.assertIn("ISSUE1-portrait-redpills.webp", home)
        self.assertIn('class="kicker">Lead · Issue 1', home)
        self.assertNotRegex(home, r"<h1>[^<]*VAL8000")
        self.assertIn('data-val-entry="home"', home)

    def test_issue1_headline_is_the_swarm_story(self) -> None:
        issue = _read(PAGES["issue1"])
        self.assertIn("<h1>Ten thousand agents</h1>", issue)
        self.assertIn("smooth external force", issue)
        self.assertIn("Reported · not DA-certified", issue)
        self.assertIn('data-val-entry="issue1"', issue)
        self.assertNotRegex(issue, r"<h1>[^<]*VAL8000")

    def test_other_shelves_keep_their_titles(self) -> None:
        self.assertIn("<h1>For the Record</h1>", _read(PAGES["record"]))
        self.assertIn("<h1>Open Progress Report</h1>", _read(PAGES["progress"]))
        self.assertIn("<h1>Quiet credit</h1>", _read(PAGES["credit"]))
        self.assertIn("<h1>the Frequency</h1>", _read(PAGES["frequency"]))


class TestValBoxWiredOnEveryPage(unittest.TestCase):
    def test_box_assets_exist(self) -> None:
        for path in (
            BOX_JS,
            BOX_CSS,
            COMMENTS,
            MAG / "val8000" / "assets" / "val8000-eye-mark.png",
            MAG / "val8000" / "assets" / "val8000-mouth-line.png",
            MAG / "val8000" / "art" / "cg-around-us-coffee-swirl.png",
            MAG / "val8000" / "art" / "cg-humor-letters-collide.png",
        ):
            self.assertTrue(path.is_file(), path)

    def test_each_page_loads_the_box_after_the_story(self) -> None:
        for entry, path in PAGES.items():
            html = _read(path)
            self.assertIn("val8000-box.css", html, path.name)
            self.assertIn("val8000-box.js", html, path.name)
            self.assertIn(f'data-val-entry="{entry}"', html, path.name)
            self.assertLess(html.index("<h1>"), html.index("val8000-box.js"))
            self.assertNotIn("val8000-mouth-teeth", html)

    def test_js_is_a_toggle_box_with_red_eye_and_line_mouth(self) -> None:
        js = _read(BOX_JS)
        self.assertIn("val8000-launcher", js)
        self.assertIn("Go deeper", js)
        self.assertIn("Weekend Update", js)
        self.assertIn("val8000-eye-mark.png", js)
        self.assertIn("val8000-mouth-line.png", js)
        self.assertNotIn("val8000-mouth-teeth", js)
        self.assertIn("aria-expanded", js)
        self.assertIn("val=open", js)


class TestHonestyInTheBox(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.blob = _magazine_blob()
        cls.comments = _read(COMMENTS)

    def test_banned_strings_stay_out_of_user_facing_magazine(self) -> None:
        blob = self.blob
        for phrase in BANNED:
            self.assertNotIn(phrase, blob, phrase)

    def test_issue1_copy_keeps_forced_vs_unforced_and_open_locks(self) -> None:
        c = self.comments
        self.assertIn("smooth external force", c)
        self.assertIn("classical unforced", c)
        self.assertIn("Reported. Not certified", c)
        self.assertIn("DA-VC-01 stays FAIL", c)
        self.assertIn("unaugmented leftover stays", c.lower())
        self.assertIn("TRANSFORMABLE without a real T", c)
        self.assertIn("not Cosmic Graffiti staff", c)

    def test_open_progress_keeps_two_statements(self) -> None:
        c = self.comments
        self.assertIn("peer review pending", c)
        self.assertIn("Classical unaugmented", c)
        self.assertIn("OPEN", c)
        self.assertIn("I will not flatten OPEN to closed", c)

    def test_record_and_swirl_beats(self) -> None:
        c = self.comments
        self.assertIn("Coat check, not a trophy shelf", c)
        self.assertIn("swirl Φ = u_θ/r", c)
        self.assertIn("art can slap", c)
        self.assertIn("not proofs", c)

    def test_feed_still_points_at_the_live_shelves(self) -> None:
        data = json.loads(_read(FEED))
        hrefs = {it["href"] for it in data["items"]}
        self.assertEqual(
            hrefs,
            {"open-progress/", "for-the-record.html", "credit.html", "issue1.html"},
        )


class TestBoxChromeIsMathPlusMusic(unittest.TestCase):
    def test_visualizer_canvas_and_eq_bars_exist(self) -> None:
        js = _read(BOX_JS)
        css = _read(BOX_CSS)
        self.assertIn("val8000-viz", js)
        self.assertIn("fillRect", js)
        self.assertIn("val8000-viz", css)
        self.assertIn("repeating-radial-gradient", css)


if __name__ == "__main__":
    unittest.main()
