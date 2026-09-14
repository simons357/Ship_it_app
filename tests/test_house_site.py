#!/usr/bin/env python3
"""House site: three doors, $99 is a plan, DA does not file patents."""

from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOUSE = ROOT / "docs" / "house"
CATALOG = HOUSE / "catalog.json"
SITE = HOUSE / "SITE.md"
HTML = HOUSE / "public" / "index.html"
LIVE_PY = ROOT / "domain_architect"


class TestHouseDoors(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.data = json.loads(CATALOG.read_text(encoding="utf-8"))
        cls.site = SITE.read_text(encoding="utf-8")
        cls.html = HTML.read_text(encoding="utf-8")
        cls.blob = "\n".join([cls.site, cls.html, json.dumps(cls.data)]).lower()

    def test_files_exist(self) -> None:
        self.assertTrue(CATALOG.is_file())
        self.assertTrue(SITE.is_file())
        self.assertTrue(HTML.is_file())
        self.assertTrue((HOUSE / "CATALOG.md").is_file())

    def test_three_doors_and_paywall_off(self) -> None:
        self.assertEqual(self.data["paywall"], "off")
        self.assertEqual(self.data["studio_price_usd"], 99)
        self.assertEqual(self.data["studio_status"], "plan")
        self.assertEqual(self.data["doors"]["studio"]["status"], "plan")
        self.assertIn("not wired", self.html.lower())
        self.assertIn("sign, not a lock", self.html.lower())
        self.assertNotIn("paywall is live", self.blob)
        self.assertNotIn("checkout now", self.blob)

    def test_live_lab_and_patents(self) -> None:
        self.assertEqual(self.data["live_lab"], "Domain Architect")
        self.assertIn("does not file patents", self.data["patents"].lower())
        self.assertIn("decompose", self.html.lower())
        self.assertIn("not da filings", self.blob)

    def test_cli_does_not_charge(self) -> None:
        proc = subprocess.run(
            ["python3", str(ROOT / "scripts" / "cg_house.py"), "doors"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("plan", proc.stdout.lower())
        self.assertIn("does not take a card", proc.stdout.lower())

    def test_live_da_python_stays_clean(self) -> None:
        for path in LIVE_PY.rglob("*.py"):
            blob = path.read_text(encoding="utf-8")
            self.assertNotIn("NAV-42", blob)
            self.assertNotIn("Chat Vault", blob)
            self.assertNotIn("2.2 Hz", blob)


if __name__ == "__main__":
    unittest.main()
