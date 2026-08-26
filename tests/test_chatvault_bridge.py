#!/usr/bin/env python3
"""ChatVault drain from Domain Architect — export format, origin, no auto-PROVED."""

from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from domain_architect.chatvault_bridge import drain_audit
from domain_architect.cli import main
from domain_architect.drain_server import DrainQueue


class TestDrainAuditFormat(unittest.TestCase):
    def test_export_is_chatvault_bundle_not_a_proof(self):
        payload = drain_audit("∇²Φ = 4π G ρ")
        self.assertEqual(payload["format"], "chatvault-export")
        self.assertEqual(payload["schema_version"], "chatvault-engine-0.3.0")
        self.assertEqual(payload["source"], "domain-architect")
        self.assertEqual(payload["count"], 1)
        self.assertEqual(len(payload["entries"]), 1)

        entry = payload["entries"][0]
        self.assertEqual(entry["origin_class"], "human_record")
        self.assertEqual(entry["source_type"], "da_audit")
        self.assertEqual(entry["source_ai"], "DomainArchitect")
        self.assertIn("Not a proof", entry["summary"])
        self.assertEqual(entry["key_claims"], [])
        self.assertEqual(entry["theorems"], [])
        self.assertEqual(entry["open_gaps"], [])
        blob = json.dumps(payload)
        self.assertNotIn('"status": "PROVED"', blob)
        self.assertNotIn('"status":"PROVED"', blob)

    def test_queue_consume_stays_chatvault_export(self):
        queue = DrainQueue()
        payload = drain_audit("x = y")
        queued = queue.push(payload)
        self.assertEqual(queued, 1)
        consumed = queue.consume()
        self.assertEqual(consumed["format"], "chatvault-export")
        self.assertEqual(consumed["count"], 1)
        self.assertEqual(consumed["entries"][0]["origin_class"], "human_record")
        self.assertEqual(len(queue), 0)

    def test_queue_rejects_non_export(self):
        queue = DrainQueue()
        with self.assertRaises(ValueError):
            queue.push({"format": "not-chatvault", "entries": []})


class TestDrainCli(unittest.TestCase):
    def test_drain_chatvault_writes_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "da-drain.json"
            rc = main(["--drain-chatvault", "∇²Φ = 4π G ρ", "-o", str(out)])
            self.assertEqual(rc, 0)
            self.assertTrue(out.is_file())
            payload = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(payload["format"], "chatvault-export")
            entry = payload["entries"][0]
            self.assertEqual(entry["origin_class"], "human_record")
            self.assertEqual(entry["source_type"], "da_audit")
            self.assertEqual(entry["source_ai"], "DomainArchitect")
            self.assertNotIn("PROVED", json.dumps(entry.get("key_claims")))
            self.assertNotIn("PROVED", json.dumps(entry.get("theorems")))


class TestDaHomepageChatVault(unittest.TestCase):
    def test_homepage_is_not_under_construction(self):
        page = Path(__file__).resolve().parents[1] / "domain_architect" / "static" / "index.html"
        html = page.read_text(encoding="utf-8")
        self.assertNotIn("under construction", html.lower())
        self.assertIn("OS for your AI", html)
        self.assertIn("ChatVault", html)
        self.assertIn("cv-search-form", html)
        self.assertIn("/chatvault/", html)
        self.assertIn("chatvault-mark-dark.jpg", html)

    def test_cli_module_advertises_site(self):
        from domain_architect import cli

        src = Path(cli.__file__).read_text(encoding="utf-8")
        self.assertIn("--site", src)
        self.assertIn("serve_site", src)


if __name__ == "__main__":
    unittest.main()
