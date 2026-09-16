"""Lock the 16 Sep 2026 desk status map: instruments, no scoreboard."""

from __future__ import annotations

import json
import pathlib
import re
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "status_map" / "2026-09-16.json"
RECORD = ROOT / "docs" / "STATUS-MAP.md"
STREET = ROOT / "docs" / "status-map" / "STREET.txt"
HTML = ROOT / "docs" / "status-map" / "desk.html"
SVG = ROOT / "docs" / "status-map" / "desk.svg"
README = ROOT / "docs" / "status-map" / "README.md"
STILL = ROOT / "assets" / "status-map" / "still-life-2026-09-16.png"
DESK = ROOT / "assets" / "status-map" / "desk-2026-09-16.png"

FORBIDDEN = ("clay", "prize", "qed", "solved")
PUBLIC_TEXT = (RECORD, STREET, HTML, SVG, README)

LIVE_VERBS = (
    "Model",
    "Reconstruct",
    "Listen",
    "Brand",
    "Track",
    "Grow",
    "Map",
)
LIVE_NAMES = (
    "Swirl",
    "NS lemmas",
    "Listener",
    "Propos",
    "Vigilant Monitor / Anesthesia Program",
    "Lattice Edge",
    "FIELD MAPPER",
)


class TestStatusMap20260916(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(DATA.read_text(encoding="utf-8"))
        cls.record = RECORD.read_text(encoding="utf-8")
        cls.street = STREET.read_text(encoding="utf-8")

    def test_sources_present(self) -> None:
        for path in (DATA, RECORD, STREET, HTML, SVG, README, STILL, DESK):
            self.assertTrue(path.is_file(), f"missing {path}")

    def test_not_a_scoreboard(self) -> None:
        self.assertFalse(self.data["scoreboard"])
        self.assertEqual(self.data["kind"], "instruments")
        self.assertIn("No scoreboard", self.record)
        self.assertNotRegex(self.record, r"\b\d+\s*%")
        self.assertNotRegex(self.record, r"\b(ahead|behind|wins?|leaderboard)\b")

    def test_live_instruments(self) -> None:
        live = self.data["buckets"]["live"]
        self.assertEqual([item["name"] for item in live], list(LIVE_NAMES))
        self.assertEqual([item["verb"] for item in live], list(LIVE_VERBS))
        for item in live:
            self.assertTrue(item["gap"])

    def test_holding_is_instruments_not_claims(self) -> None:
        holding = {item["name"]: item for item in self.data["buckets"]["holding"]}
        self.assertIn("SFE / Harmonic Blueprint", holding)
        self.assertIn("unification stack still open", holding["SFE / Harmonic Blueprint"]["notes"])
        qstack = holding["QStack / NAV-42 / GCD shells / E8 cathedral"]
        self.assertEqual(qstack["notes"], "instruments, not claims")
        self.assertIn("Instruments, not claims", self.record)

    def test_cold_queue_stays_in_the_file(self) -> None:
        cold = [item["name"] for item in self.data["buckets"]["cold"]]
        self.assertIn("Journal / arXiv / Tao-addendum queue", cold)
        self.assertIn("In the file, not the headline.", self.record)

    def test_street_is_one_verb_per_line(self) -> None:
        lines = [line for line in self.street.splitlines() if line.strip()]
        self.assertEqual(
            lines,
            [
                "Model.",
                "Reconstruct.",
                "Listen.",
                "Brand.",
                "Track.",
                "Grow.",
                "Map.",
                "Record.",
            ],
        )
        for line in lines:
            self.assertRegex(line, r"^[A-Z][a-z]+\.$")
            self.assertEqual(len(line.split()), 1)

    def test_standing_rule(self) -> None:
        rule = self.data["standing_rule"]
        self.assertTrue(rule["rigor_first"])
        self.assertTrue(rule["gaps_named"])
        self.assertTrue(rule["visuals_and_code_make_the_math_real"])
        self.assertTrue(rule["public_output_closes_nothing"])
        self.assertIn("Rigor first", self.record)
        self.assertIn("Gaps named", self.record)
        self.assertIn("Visuals and code make the math real", self.record)

    def test_public_text_avoids_banned_claim_words(self) -> None:
        for path in PUBLIC_TEXT:
            text = path.read_text(encoding="utf-8").lower()
            for word in FORBIDDEN:
                self.assertNotRegex(
                    text,
                    rf"\b{re.escape(word)}\b",
                    msg=f"{path} contains banned claim word {word!r}",
                )

    def test_json_avoids_banned_claim_words(self) -> None:
        blob = json.dumps(self.data).lower()
        for word in FORBIDDEN:
            self.assertNotRegex(blob, rf"\b{re.escape(word)}\b")

    def test_desk_card_carries_street_copy(self) -> None:
        html = HTML.read_text(encoding="utf-8")
        svg = SVG.read_text(encoding="utf-8")
        for verb in LIVE_VERBS + ("Record",):
            self.assertIn(f"{verb}.", html)
            self.assertIn(f"{verb}.", svg)
        self.assertIn("og:image", html)
        self.assertIn("No scoreboard", html)

    def test_field_mapper_gap_named(self) -> None:
        mapper = self.data["buckets"]["live"][-1]
        self.assertEqual(mapper["name"], "FIELD MAPPER")
        self.assertIn("unresolved", mapper["gap"])
        self.assertIn("Canonical SFE status remains unresolved", self.record)

    def test_savannah_entity(self) -> None:
        self.assertEqual(self.data["operator"]["entity"], "Prime Field Technologies LLC")
        self.assertEqual(self.data["operator"]["place"], "Savannah")
        self.assertIn("Savannah", self.record)


if __name__ == "__main__":
    unittest.main()
