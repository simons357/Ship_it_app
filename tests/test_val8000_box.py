#!/usr/bin/env python3
"""VAL8000 square types in the view. No audio. Issue 1 stays Issue 1."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CG = ROOT / "docs" / "cosmic-graffiti"
MAG = CG / "magazine"
COMMENTS = MAG / "val8000" / "val8000-comments.js"
BOX_JS = MAG / "val8000" / "val8000-box.js"
BOX_CSS = MAG / "val8000" / "val8000-box.css"
BOX_DOC = CG / "val8000-box.md"
GUIDE = CG / "val8000.md"
FEED = MAG / "frequency" / "feed.json"
DA = ROOT / "domain_architect" / "static"
DOCK_JS = DA / "val8000" / "val8000-dock.js"
DOCK_CSS = DA / "val8000" / "val8000-dock.css"
DA_INDEX = DA / "index.html"

PAGES = {
    "home": MAG / "index.html",
    "issue1": MAG / "issue1.html",
    "record": MAG / "for-the-record.html",
    "credit": MAG / "credit.html",
    "frequency": MAG / "frequency" / "index.html",
    "progress": MAG / "open-progress" / "index.html",
}

HELP = (
    "Ask the Desk. I type what I already know. I do not invent theorems. "
    "I do not stamp TRANSFORMABLE without a real T. DA-VC-01 stays FAIL. "
    "Voice later — I only type in this box."
)

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

AUDIO_CALLS = (
    "<audio",
    "speechSynthesis",
    "webkitSpeech",
    "new Audio",
    "AudioContext",
    "webkitAudioContext",
    "val8000_speak.py",
    "elevenlabs.io",
    "val8000-viz",
    "fillRect",
    "<canvas",
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _widget_blob() -> str:
    return "\n".join(
        [
            _read(BOX_JS),
            _read(BOX_CSS),
            _read(DOCK_JS),
            _read(DOCK_CSS),
        ]
    )


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


class TestValSquareTypesInTheView(unittest.TestCase):
    def test_box_assets_exist(self) -> None:
        for path in (
            BOX_JS,
            BOX_CSS,
            COMMENTS,
            BOX_DOC,
            MAG / "val8000" / "assets" / "val8000-eye-mark.png",
            MAG / "val8000" / "assets" / "val8000-mouth-line.png",
            MAG / "val8000" / "assets" / "val8000-mouth-smile.png",
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
            self.assertNotIn("val8000_speak.py", html)

    def test_js_is_a_persistent_square_that_types(self) -> None:
        js = _read(BOX_JS)
        css = _read(BOX_CSS)
        self.assertIn("val8000-square", js)
        self.assertIn("always-visible square", js)
        self.assertIn("val8000-mouth-line.png", js)
        self.assertIn("val8000-mouth-smile.png", js)
        self.assertIn("val8000-eye-mark.png", js)
        self.assertIn("Help with unanswered", js)
        self.assertIn("Ask the Desk", js)
        self.assertIn("Type to VAL8000", js)
        self.assertIn("val8000-typed", js)
        self.assertIn("He types. Voice later.", js)
        self.assertIn('data-val-audio', js)
        self.assertIn("val=open", js)
        self.assertNotIn("Go deeper", js)
        self.assertNotIn("val8000-viz", js)
        self.assertNotIn("fillRect", js)
        self.assertIn("position: sticky", css)
        self.assertIn("7.2rem", css)
        self.assertNotIn(
            '.val8000-launcher[aria-expanded="true"] { display: none; }',
            css.replace("\n", " "),
        )


class TestNoAudioInTheWidget(unittest.TestCase):
    def test_widget_files_do_not_call_audio(self) -> None:
        blob = _widget_blob()
        lower = blob.lower()
        for phrase in AUDIO_CALLS:
            self.assertNotIn(phrase, blob, phrase)
            self.assertNotIn(phrase.lower(), lower, phrase)

    def test_docs_lock_type_now_voice_later(self) -> None:
        box = _read(BOX_DOC)
        guide = _read(GUIDE)
        self.assertIn("Type now", box + guide)
        self.assertIn("voice later", (box + guide).lower())
        self.assertIn("No audio", box)
        self.assertIn("val8000_speak.py", box)
        self.assertIn("DA-VC-01 stays FAIL", box)
        self.assertIn("TRANSFORMABLE", box)
        self.assertIn("The magazine square does **not** speak", guide)


class TestHonestyInTheBox(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.blob = _magazine_blob()
        cls.comments = _read(COMMENTS)

    def test_banned_strings_stay_out_of_user_facing_magazine(self) -> None:
        blob = self.blob
        for phrase in BANNED:
            self.assertNotIn(phrase, blob, phrase)

    def test_help_line_carries_the_locks(self) -> None:
        self.assertIn(HELP, self.comments)
        self.assertIn("DA-VC-01 stays FAIL", HELP)
        self.assertIn("TRANSFORMABLE without a real T", HELP)
        self.assertIn("I do not invent theorems", HELP)
        self.assertIn("VAL8000_reply", self.comments)

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

    def test_reply_function_help_fail_and_no_t(self) -> None:
        script = f"""
const fs = require('fs');
const vm = require('vm');
const src = fs.readFileSync({str(COMMENTS)!r}, 'utf8');
const ctx = {{}};
ctx.window = ctx;
ctx.globalThis = ctx;
vm.createContext(ctx);
vm.runInContext(src, ctx);
const help = ctx.VAL8000_HELP;
if (help !== {HELP!r}) {{ console.error('help mismatch', help); process.exit(1); }}
if (ctx.VAL8000_reply('what is the weather in mars') !== help) process.exit(2);
if (ctx.VAL8000_reply('') !== help) process.exit(3);
const fail = ctx.VAL8000_reply('Did DA-VC-01 pass?');
if (!fail.includes('DA-VC-01 stays FAIL')) process.exit(4);
if (!fail.includes('OPEN')) process.exit(5);
const noT = ctx.VAL8000_reply('stamp this TRANSFORMABLE');
if (!noT.includes('TRANSFORMABLE without a real T')) process.exit(6);
const talk = ctx.VAL8000_reply('please speak with elevenlabs');
if (!talk.toLowerCase().includes('do not talk yet')) process.exit(7);
console.log('ok');
"""
        proc = subprocess.run(
            ["node", "-e", script],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn("ok", proc.stdout)


class TestDaDockAlsoTypes(unittest.TestCase):
    def test_dock_is_a_square_with_typed_help(self) -> None:
        html = _read(DA_INDEX)
        js = _read(DOCK_JS)
        self.assertIn("val8000-square", html)
        self.assertIn("val8000-mouth-line.png", html)
        self.assertIn('data-val-audio="off"', html)
        self.assertIn("He types. Voice later.", html)
        self.assertIn("Help with unanswered", html)
        self.assertIn("Type to VAL8000", html)
        self.assertIn("DA-VC-01 stays FAIL", js)
        self.assertIn("TRANSFORMABLE without a real T", js)
        self.assertIn("I only type in this box", js)
        self.assertNotIn("val8000_speak.py", js)
        self.assertNotIn("speechSynthesis", js)
        self.assertTrue((DA / "val8000" / "val8000-mouth-line.png").is_file())
        self.assertTrue((DA / "val8000" / "val8000-mouth-smile.png").is_file())


if __name__ == "__main__":
    unittest.main()
