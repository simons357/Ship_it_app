#!/usr/bin/env python3
"""Simple Domain Architect desk: inquire, see, compute — not ChatVault."""

from __future__ import annotations

import json
import threading
import unittest
from http.client import HTTPConnection
from pathlib import Path

from domain_architect.desk_server import DeskHandler
from http.server import ThreadingHTTPServer


ROOT = Path(__file__).resolve().parents[1]


class TestSimpleDesk(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.httpd = ThreadingHTTPServer(("127.0.0.1", 0), DeskHandler)
        cls.port = cls.httpd.server_address[1]
        cls.thread = threading.Thread(target=cls.httpd.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls):
        cls.httpd.shutdown()
        cls.httpd.server_close()

    def _get(self, path: str):
        conn = HTTPConnection("127.0.0.1", self.port, timeout=10)
        conn.request("GET", path)
        res = conn.getresponse()
        body = res.read()
        conn.close()
        return res.status, res.getheader("Content-Type"), body

    def _post(self, path: str, payload: dict):
        raw = json.dumps(payload).encode("utf-8")
        conn = HTTPConnection("127.0.0.1", self.port, timeout=10)
        conn.request(
            "POST",
            path,
            body=raw,
            headers={"Content-Type": "application/json"},
        )
        res = conn.getresponse()
        body = res.read()
        conn.close()
        return res.status, json.loads(body.decode("utf-8"))

    def test_home_is_simple_not_kitchen_sink(self):
        status, ctype, body = self._get("/")
        html = body.decode("utf-8").lower()
        self.assertEqual(status, 200)
        self.assertIn("text/html", ctype or "")
        self.assertIn("domain architect", html)
        self.assertIn("inquire", html)
        self.assertIn("see-jigsaw.svg", html)
        self.assertIn("see-relations.svg", html)
        self.assertIn("not chatvault", html)
        self.assertNotIn("open chatvault", html)
        self.assertNotIn("route c", html)
        self.assertNotIn("clay", html)
        self.assertNotIn("file in vault", html)
        self.assertNotIn("inquire + file", html)

    def test_no_vault_drain(self):
        status, ctype, body = self._get("/api/inbox")
        payload = json.loads(body.decode("utf-8"))
        self.assertEqual(status, 404)
        self.assertEqual(payload["error"], "no vault drain on this desk")
        status, payload = self._post("/api/inquiry", {"inquiry": "laplacian Phi = 4 * pi * G * rho", "drain": True})
        self.assertEqual(status, 404)
        self.assertTrue(payload["not_chatvault"])

    def test_audit_and_jigsaw(self):
        status, payload = self._post(
            "/api/audit", {"expression": "laplacian Phi = 4 * pi * G * rho"}
        )
        self.assertEqual(status, 200)
        self.assertTrue(payload["ok"])
        self.assertEqual(payload["canonical_sfe_status"], "unresolved")
        self.assertIn("narrative", payload)
        status, ctype, body = self._get("/api/jigsaw?book=B")
        data = json.loads(body.decode("utf-8"))
        self.assertEqual(status, 200)
        self.assertTrue(data["goal"]["over"])
        self.assertFalse(data["reconstruct"]["floor"])
        self.assertNotIn("clay", json.dumps(data).lower())

    def test_q_is_not_a_zero_prover(self):
        status, ctype, body = self._get("/api/jigsaw?book=Q")
        data = json.loads(body.decode("utf-8"))
        self.assertEqual(status, 200)
        self.assertEqual(data["book"], "Q")
        notes = json.dumps(data["reconstruct"]).lower()
        self.assertIn("does_not", notes)


if __name__ == "__main__":
    unittest.main()
