#!/usr/bin/env python3
"""ChatVault drain from Domain Architect — export format, origin, no auto-PROVED."""

from __future__ import annotations

import json
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

from domain_architect.chatvault_bridge import drain_audit, inquire
from domain_architect.cli import main
from domain_architect.drain_server import DrainQueue
from domain_architect.site_server import SiteHandler


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

    def test_inquire_is_fra_lane_and_optional_drain(self):
        payload = inquire("x = y")
        self.assertEqual(payload["lane"], "inquiry")
        self.assertEqual(payload["ok"], True)
        self.assertIsNone(payload["drain"])
        self.assertEqual(payload["canonical_sfe_status"], "unresolved")
        self.assertIn("narrative", payload["audit"])
        filed = inquire("∇²Φ = 4π G ρ", drain=True)
        self.assertEqual(filed["drain"]["format"], "chatvault-export")
        self.assertEqual(filed["drain"]["entries"][0]["source_type"], "da_audit")
        self.assertNotIn("PROVED", json.dumps(filed["drain"]["entries"][0].get("theorems")))

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
        self.assertIn("da-inquiry-form", html)
        self.assertIn("Inquiry", html)
        self.assertIn("Two boxes", html)
        self.assertLess(html.find('id="da-inquiry-card"'), html.find('id="da-program"'))
        self.assertIn("/chatvault/", html)
        self.assertIn("chatvault-mark-dark.jpg", html)
        self.assertIn("apple-mobile-web-app-capable", html)
        self.assertIn("Domain Architect", html)
        self.assertIn("cv-file-search", html)
        self.assertIn("File into ChatVault", html)
        self.assertIn("Does not have to be a whole conversation", html)
        self.assertIn("da-ideas", html)
        self.assertIn("cv-web-dive", html)
        self.assertIn("Not this product", html)
        self.assertIn("in-vault web crawler", html)

    def test_homepage_engines_catalog_is_honest(self):
        page = Path(__file__).resolve().parents[1] / "domain_architect" / "static" / "index.html"
        html = page.read_text(encoding="utf-8")
        self.assertIn("cv-search-form", html)
        self.assertIn('id="da-engines"', html)
        self.assertIn("Engines Jonathan can offer", html)
        self.assertIn("chatvault-hybrid-0.2.0", html)
        self.assertIn("chatvault/js/search.mjs", html)
        self.assertIn("Not in this workshop yet", html)
        self.assertIn("Tanto", html)
        self.assertIn("VibraScan", html)
        self.assertIn("locate and attach", html)
        self.assertIn("Field Lock", html)
        self.assertIn("teaching kiosk", html)
        self.assertIn("field-lock.replit.app", html)
        self.assertIn("engines/fieldlock/", html)
        self.assertIn("Domain Architect FRA", html)
        self.assertNotIn("we license Tanto", html.lower())
        self.assertNotIn("Evernote", html)
        self.assertNotIn("Stripe", html)

    def test_manifest_is_combined_origin_pwa(self):
        manifest_path = (
            Path(__file__).resolve().parents[1] / "domain_architect" / "static" / "manifest.webmanifest"
        )
        payload = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(payload["name"], "Domain Architect")
        self.assertEqual(payload["short_name"], "DA")
        self.assertEqual(payload["start_url"], "/")
        self.assertEqual(payload["scope"], "/")
        self.assertEqual(payload["display"], "standalone")
        self.assertEqual(payload["theme_color"], "#141816")
        self.assertEqual(payload["share_target"]["action"], "/")
        self.assertEqual(payload["share_target"]["method"], "GET")
        self.assertEqual(payload["share_target"]["params"]["title"], "title")
        self.assertEqual(payload["share_target"]["params"]["text"], "text")
        self.assertEqual(payload["share_target"]["params"]["url"], "url")

    def test_cli_module_advertises_site(self):
        from domain_architect import cli

        src = Path(cli.__file__).read_text(encoding="utf-8")
        self.assertIn("--site", src)
        self.assertIn("serve_site", src)
        self.assertIn("--ingest-chatvault", src)


class TestDaSiteServiceWorker(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), SiteHandler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()
        cls.origin = f"http://127.0.0.1:{cls.port}"

    @classmethod
    def tearDownClass(cls) -> None:
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def test_sw_is_javascript_and_skips_chatvault(self) -> None:
        with urllib.request.urlopen(f"{self.origin}/da-sw.js") as res:
            ctype = res.headers.get("Content-Type", "")
            self.assertIn("javascript", ctype)
            self.assertEqual(res.headers.get("Service-Worker-Allowed"), "/")
            body = res.read().decode("utf-8")
        self.assertIn("/chatvault/", body)
        self.assertIn('req.method !== "GET"', body)

    def test_audit_post_still_works(self) -> None:
        req = urllib.request.Request(
            f"{self.origin}/api/audit",
            data=json.dumps({"expression": "x = y"}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as res:
            self.assertEqual(res.status, 200)
            payload = json.loads(res.read().decode("utf-8"))
        self.assertIn("narrative", payload)
        self.assertEqual(payload.get("canonical_sfe_status"), "unresolved")
        blob = json.dumps(payload)
        self.assertNotIn('"status": "PROVED"', blob)

    def test_inquiry_post_is_fra_and_can_file_without_proving(self) -> None:
        req = urllib.request.Request(
            f"{self.origin}/api/inquiry",
            data=json.dumps({"inquiry": "∇²Φ = 4π G ρ", "drain": True}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as res:
            self.assertEqual(res.status, 200)
            payload = json.loads(res.read().decode("utf-8"))
        self.assertEqual(payload.get("ok"), True)
        self.assertEqual(payload.get("lane"), "inquiry")
        self.assertIn("narrative", payload.get("audit") or {})
        self.assertEqual(payload.get("canonical_sfe_status"), "unresolved")
        drain = payload.get("drain") or {}
        self.assertEqual(drain.get("format"), "chatvault-export")
        entry = drain["entries"][0]
        self.assertEqual(entry["origin_class"], "human_record")
        self.assertEqual(entry["source_type"], "da_audit")
        self.assertEqual(entry["source_ai"], "DomainArchitect")
        blob = json.dumps(payload)
        self.assertNotIn('"status": "PROVED"', blob)

    def test_inquiry_rejects_empty_box(self) -> None:
        req = urllib.request.Request(
            f"{self.origin}/api/inquiry",
            data=json.dumps({"inquiry": "   "}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(urllib.error.HTTPError) as caught:
            urllib.request.urlopen(req)
        self.assertEqual(caught.exception.code, 400)

    def test_manifest_content_type(self) -> None:
        with urllib.request.urlopen(f"{self.origin}/manifest.webmanifest") as res:
            self.assertIn("manifest", res.headers.get("Content-Type", ""))
            payload = json.loads(res.read().decode("utf-8"))
        self.assertEqual(payload["scope"], "/")


if __name__ == "__main__":
    unittest.main()
