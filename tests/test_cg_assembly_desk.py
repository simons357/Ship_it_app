#!/usr/bin/env python3
"""Honesty locks for the Cosmic Graffiti assembly desk.

Three outs exist. VAL is not the lead. Issue 1 stays reported, not certified.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CG = ROOT / "docs" / "cosmic-graffiti"
DESK = CG / "desk"
ASSEMBLY = CG / "ASSEMBLY.md"
RUNDOWN = DESK / "rundown.json"
CLI = ROOT / "scripts" / "cg_desk.py"
PUBLIC = DESK / "public"


def _strip_urls(text: str) -> str:
    text = re.sub(r"https?://\S+", " ", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    return text


def _desk_blob() -> str:
    parts: list[str] = []
    for path in [ASSEMBLY, RUNDOWN, DESK / "README.md"]:
        parts.append(path.read_text(encoding="utf-8"))
    for path in DESK.rglob("*"):
        if path.suffix.lower() in {".md", ".html", ".css", ".json"}:
            parts.append(path.read_text(encoding="utf-8"))
    parts.append(CLI.read_text(encoding="utf-8"))
    return "\n".join(parts)


def _run_cli(*args: str) -> str:
    proc = subprocess.run(
        [sys.executable, str(CLI), *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return proc.stdout


class TestDeskLayout(unittest.TestCase):
    def test_spec_and_rundown_exist(self) -> None:
        self.assertTrue(ASSEMBLY.is_file())
        self.assertTrue(RUNDOWN.is_file())
        self.assertTrue(CLI.is_file())
        self.assertTrue((PUBLIC / "index.html").is_file())
        self.assertTrue((PUBLIC / "styles.css").is_file())
        self.assertTrue((PUBLIC / "issue-1.html").is_file())

    def test_rundown_has_expected_cards(self) -> None:
        data = json.loads(RUNDOWN.read_text(encoding="utf-8"))
        slugs = [row["slug"] for row in data["entries"]]
        for needed in (
            "issue-1",
            "open-progress",
            "for-the-record",
            "teaching-pictures",
            "frequency-2026-09-14",
            "ask-the-desk",
            "cosmo-evolution",
            "val-weekend-update",
        ):
            self.assertIn(needed, slugs, needed)
        self.assertTrue(any(row["slug"] == "photos" for row in data["entries"]))
        self.assertTrue(any(row["slug"] == "jon-story" for row in data["entries"]))
        self.assertTrue(any(row["slug"] == "later-frequency" for row in data["entries"]))
        statuses = {row["slug"]: row["status"] for row in data["entries"]}
        self.assertEqual(statuses["issue-1"], "live")
        self.assertEqual(statuses["open-progress"], "live")
        self.assertEqual(statuses["for-the-record"], "live")
        self.assertEqual(statuses["teaching-pictures"], "draft")
        self.assertEqual(statuses["frequency-2026-09-14"], "draft")
        self.assertEqual(statuses["ask-the-desk"], "tray")
        self.assertEqual(statuses["cosmo-evolution"], "tray")
        self.assertEqual(statuses["val-weekend-update"], "tray")
        self.assertEqual(data["paywall"], "off")
        self.assertEqual(data["substack"], "https://jonathansimonscrna.substack.com")
        self.assertIn("substack_not", data)
        self.assertIn("jonathansimons.substack.com", data["substack_not"])

    def test_seeded_entries_have_three_outs_and_assets(self) -> None:
        data = json.loads(RUNDOWN.read_text(encoding="utf-8"))
        seeded = [row for row in data["entries"] if row.get("seeded")]
        self.assertGreaterEqual(len(seeded), 2)
        self.assertLessEqual(len(seeded), 4)
        slugs = {row["slug"] for row in seeded}
        self.assertIn("issue-1", slugs)
        self.assertTrue("open-progress" in slugs or "for-the-record" in slugs)
        self.assertIn("teaching-pictures", slugs)
        for row in seeded:
            folder = DESK / "entries" / row["slug"]
            for name in ("magazine.md", "substack.md", "skool.md"):
                path = folder / name
                self.assertTrue(path.is_file(), path)
                self.assertGreater(path.stat().st_size, 80, path)
            assets = folder / "assets"
            self.assertTrue(assets.is_dir(), assets)
            self.assertTrue(any(assets.iterdir()), f"empty assets {assets}")
            if row.get("val"):
                self.assertTrue((folder / "val.md").is_file(), row["slug"])


class TestValIsNotTheLead(unittest.TestCase):
    def test_val_copy_is_not_the_lead(self) -> None:
        data = json.loads(RUNDOWN.read_text(encoding="utf-8"))
        for row in data["entries"]:
            if not row.get("seeded"):
                continue
            mag = (DESK / "entries" / row["slug"] / "magazine.md").read_text(encoding="utf-8")
            stripped = mag.lstrip()
            first_heading = ""
            for line in stripped.splitlines():
                if line.startswith("# "):
                    first_heading = line[2:].strip()
                    break
            self.assertTrue(first_heading, row["slug"])
            self.assertFalse(
                first_heading.upper().startswith("VAL"),
                f"VAL is the lead on {row['slug']}: {first_heading}",
            )
            self.assertNotIn("VAL8000", first_heading)
            if row.get("val"):
                val = (DESK / "entries" / row["slug"] / "val.md").read_text(encoding="utf-8")
                self.assertGreater(len(val.strip()), 40)
                mag_lower = mag.lower()
                self.assertTrue(
                    "after" in mag_lower and "val" in mag_lower,
                    f"{row['slug']} magazine should point at VAL after the story",
                )

    def test_spec_says_val_is_the_box_not_the_lead(self) -> None:
        spec = ASSEMBLY.read_text(encoding="utf-8").lower()
        self.assertIn("little box", spec)
        self.assertIn("never the story lead", spec)
        self.assertIn("after", spec)
        self.assertIn("val8000", spec)


class TestHonestyLocks(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.blob = _desk_blob()
        cls.prose = _strip_urls(cls.blob)
        cls.lower = cls.prose.lower()

    def test_no_hal_9000_product_name(self) -> None:
        self.assertNotIn("HAL 9000", self.blob)
        self.assertNotIn("Hal 9000", self.blob)
        self.assertNotIn("hal 9000", self.lower)

    def test_substack_handle_is_jonathansimonscrna(self) -> None:
        self.assertIn("jonathansimonscrna.substack.com", self.blob)
        rundown = json.loads(RUNDOWN.read_text(encoding="utf-8"))
        self.assertEqual(rundown["substack"], "https://jonathansimonscrna.substack.com")
        self.assertNotEqual(rundown["substack"], "https://jonathansimons.substack.com")
        # Namesake URL is allowed only as the "not this" field.
        for path in DESK.rglob("*"):
            if path.suffix.lower() not in {".md", ".html", ".css"}:
                continue
            text = path.read_text(encoding="utf-8")
            self.assertNotIn(
                "https://jonathansimons.substack.com",
                text,
                f"namesake URL in {path}",
            )
            if "substack.com" in text:
                self.assertIn("jonathansimonscrna.substack.com", text, path)

    def test_issue_1_reported_not_certified(self) -> None:
        mag = (DESK / "entries" / "issue-1" / "magazine.md").read_text(encoding="utf-8")
        sub = (DESK / "entries" / "issue-1" / "substack.md").read_text(encoding="utf-8")
        skool = (DESK / "entries" / "issue-1" / "skool.md").read_text(encoding="utf-8")
        blob = f"{mag}\n{sub}\n{skool}"
        self.assertIn("Reported · not DA-certified", blob)
        self.assertIn("not da-certified", blob.lower())
        self.assertNotIn("DA-certified close", blob)
        self.assertNotIn("we certify", blob.lower())
        html = (PUBLIC / "issue-1.html").read_text(encoding="utf-8")
        self.assertIn("not DA-certified", html)

    def test_unaugmented_not_closed(self) -> None:
        self.assertIn("da-vc-01", self.lower)
        self.assertIn("fail", self.lower)
        self.assertIn("unaugmented leftover", self.lower)
        self.assertNotIn("da-vc-01 as pass", self.lower)
        self.assertNotIn("da-vc-01 remains pass", self.lower)
        self.assertNotIn("unaugmented leftover closed", self.lower)
        self.assertNotRegex(self.lower, r"navier[–\- ]stokes (is|are|was) solved")
        open_prog = (DESK / "entries" / "open-progress" / "magazine.md").read_text(encoding="utf-8")
        self.assertIn("Open · In Progress", open_prog)
        self.assertIn("FAIL", open_prog)

    def test_paywall_off_and_no_fake_stripe(self) -> None:
        self.assertIn("paywall", self.lower)
        self.assertNotIn("paywall is live", self.lower)
        self.assertNotIn("subscribe to unlock", self.lower)
        self.assertNotIn("sk_live", self.blob)
        self.assertNotIn("stripe", self.lower)
        spec = ASSEMBLY.read_text(encoding="utf-8").lower()
        self.assertIn("paywall stays **off**", spec)

    def test_letters_and_correspondence_labels(self) -> None:
        spec = ASSEMBLY.read_text(encoding="utf-8").lower()
        self.assertIn("correspondence ≠ physical equivalence", spec)
        self.assertIn("letters collide", spec)
        self.assertIn("does **not** file patents", spec)

    def test_no_prize_packaging_in_prose(self) -> None:
        self.assertNotIn("Clay", self.prose)
        self.assertNotIn("Millennium Prize", self.prose)
        self.assertNotIn("millennium prize", self.lower)


class TestCli(unittest.TestCase):
    def test_list_show_substack_skool(self) -> None:
        listing = _run_cli("list")
        self.assertIn("issue-1", listing)
        self.assertIn("Ten thousand agents", listing)
        self.assertIn("jonathansimonscrna.substack.com", listing)
        self.assertNotIn("HAL 9000", listing)
        shown = _run_cli("show", "issue-1")
        self.assertIn("Ten thousand agents", shown)
        self.assertIn("Reported · not DA-certified", shown)
        self.assertIn("VAL8000", shown)
        self.assertIn("after the news", shown.lower())
        # VAL heading is not the magazine title.
        self.assertNotRegex(shown, r"^# VAL", re.M)
        sub = _run_cli("substack", "issue-1")
        self.assertIn("jonathansimonscrna.substack.com", sub)
        self.assertIn("ISSUE1-portrait-redpills.webp", sub)
        self.assertIn("Alt:", sub)
        self.assertIn("Paywall: off", sub)
        skool = _run_cli("skool", "issue-1")
        self.assertIn("Ask in this thread", skool)
        self.assertIn("Reported · not DA-certified", skool)

    def test_teaching_pictures_cli(self) -> None:
        shown = _run_cli("show", "teaching-pictures")
        self.assertIn("Fourier space bookkeeping, not cosmology", shown)
        self.assertIn("OPEN", shown)
        skool = _run_cli("skool", "teaching-pictures")
        self.assertIn("Ask in this thread", skool)


class TestBoardChrome(unittest.TestCase):
    def test_board_is_workspace_not_second_brand(self) -> None:
        html = (PUBLIC / "index.html").read_text(encoding="utf-8")
        self.assertIn("Assembly desk", html)
        self.assertIn("not a second brand", html.lower())
        self.assertIn("cosmic-graffiti-magazine.vercel.app", html)
        self.assertIn("jonathansimonscrna.substack.com", html)
        self.assertIn("Ten thousand agents", html)
        self.assertIn("val-box", html.lower() + (PUBLIC / "issue-1.html").read_text(encoding="utf-8").lower())
        css = (PUBLIC / "styles.css").read_text(encoding="utf-8")
        self.assertIn("#050a14", css)
        self.assertIn("#c9a227", css)

    def test_issue1_html_has_three_outs_and_val_after(self) -> None:
        html = (PUBLIC / "issue-1.html").read_text(encoding="utf-8")
        self.assertIn("data-out=\"magazine\"", html)
        self.assertIn("data-out=\"substack\"", html)
        self.assertIn("data-out=\"skool\"", html)
        self.assertIn("Reported · not DA-certified", html)
        self.assertIn("Ask in this thread", html)
        self.assertIn("val-box", html)
        self.assertIn("VAL8000", html)
        self.assertNotIn("HAL 9000", html)
        # VAL block appears after the story heading, not as h1.
        h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        self.assertIsNotNone(h1)
        self.assertIn("Ten thousand agents", h1.group(1))
        self.assertNotIn("VAL8000", h1.group(1))


if __name__ == "__main__":
    raise SystemExit(unittest.main())
