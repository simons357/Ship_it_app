"""The leftover-object app sits. Honest OPEN. Not a proof."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "apps" / "the-object"
PHONE = ROOT / "docs" / "THE-OBJECT-APP.md"
JSON = APP / "data" / "object.json"
HTML = APP / "index.html"
STILLS = APP / "stills"


class TheObjectAppTests(unittest.TestCase):
    def test_release_folder_and_phone(self):
        self.assertTrue((APP / "index.html").is_file())
        self.assertTrue((APP / "app.js").is_file())
        self.assertTrue((APP / "style.css").is_file())
        self.assertTrue((APP / "data.js").is_file())
        self.assertTrue(PHONE.is_file())
        phone = PHONE.read_text()
        self.assertIn("NS not solved", phone)
        self.assertIn("apps/the-object/", phone)

    def test_payload_is_open_and_has_geometry(self):
        data = json.loads(JSON.read_text())
        self.assertIs(data["ns_solved"], False)
        self.assertEqual(data["lemma_star"], "OPEN")
        self.assertEqual(data["kill_lane"], "LIVE")
        self.assertGreater(data["featured"]["K"], 0.0)
        self.assertLess(data["featured"]["K"], 2.0)
        self.assertEqual(len(data["shells"]["alpha"]), 6)
        self.assertGreaterEqual(len(data["aligned"]), 5)
        mis = [row["R_star"] for row in data["misaligned"]]
        ali = [row["R_star"] for row in data["aligned"]]
        self.assertLess(max(mis), 0.05)
        self.assertGreater(ali[-1], 0.2)

    def test_page_does_not_announce_a_solve(self):
        html = HTML.read_text()
        self.assertIn("OPEN", html)
        self.assertIn("NS not solved", html)
        self.assertNotIn("NS is solved", html)
        self.assertNotIn("millennium", html.lower())
        js = (APP / "app.js").read_text()
        self.assertIn("OBJECT_DATA", js)

    def test_stills_exist(self):
        for name in (
            "object_shells.png",
            "object_aligned.png",
            "object_quotient.png",
            "object_samples.png",
        ):
            p = STILLS / name
            self.assertTrue(p.is_file(), name)
            self.assertGreater(p.stat().st_size, 1000)


if __name__ == "__main__":
    unittest.main()
