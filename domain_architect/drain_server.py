"""Local ChatVault drain listener for Domain Architect.

Binds 127.0.0.1 only. ChatVault’s CSP may connect here so a finished
audit can be pulled into the PWA. Not a public backend and not a proof
service.

    GET  /health  — liveness
    GET  /queue   — consume queued ChatVault exports
    POST /queue   — enqueue a chatvault-export JSON body
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

from .chatvault_bridge import (
    CHATVAULT_EXPORT_FORMAT,
    CHATVAULT_SCHEMA_VERSION,
    DEFAULT_DRAIN_HOST,
    DEFAULT_DRAIN_PORT,
    DRAIN_PROTOCOL,
    drain_audit,
)


class DrainQueue:
    def __init__(self) -> None:
        self._payloads: list[dict[str, Any]] = []

    def push(self, payload: dict[str, Any]) -> int:
        if not payload or payload.get("format") != CHATVAULT_EXPORT_FORMAT:
            raise ValueError("POST body must be a ChatVault export (format=chatvault-export).")
        self._payloads.append(payload)
        return sum(len(item.get("entries") or []) for item in self._payloads)

    def consume(self) -> dict[str, Any]:
        entries: list[dict[str, Any]] = []
        for payload in self._payloads:
            entries.extend(payload.get("entries") or [])
        self._payloads = []
        return {
            "format": CHATVAULT_EXPORT_FORMAT,
            "schema_version": CHATVAULT_SCHEMA_VERSION,
            "source": "domain-architect",
            "drain_protocol": DRAIN_PROTOCOL,
            "count": len(entries),
            "entries": entries,
        }

    def __len__(self) -> int:
        return sum(len(item.get("entries") or []) for item in self._payloads)


QUEUE = DrainQueue()


def _json_response(handler: BaseHTTPRequestHandler, code: int, payload: dict[str, Any]) -> None:
    body = json.dumps(payload, default=str).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Access-Control-Allow-Origin", "*")
    handler.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    handler.send_header("Access-Control-Allow-Headers", "Content-Type")
    handler.end_headers()
    handler.wfile.write(body)


class DrainHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path in ("/health", "/"):
            _json_response(
                self,
                200,
                {
                    "ok": True,
                    "service": "chatvault-da-drain",
                    "drain_protocol": DRAIN_PROTOCOL,
                    "queued": len(QUEUE),
                },
            )
            return
        if path == "/queue":
            _json_response(self, 200, QUEUE.consume())
            return
        _json_response(self, 404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path != "/queue":
            _json_response(self, 404, {"ok": False, "error": "not found"})
            return
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            _json_response(self, 400, {"ok": False, "error": "invalid JSON"})
            return
        try:
            if isinstance(data, dict) and data.get("expression") and data.get("format") != CHATVAULT_EXPORT_FORMAT:
                data = drain_audit(str(data["expression"]))
            queued = QUEUE.push(data)
        except (ValueError, TypeError) as err:
            _json_response(self, 400, {"ok": False, "error": str(err)})
            return
        _json_response(self, 200, {"ok": True, "queued": queued})


def serve(host: str = DEFAULT_DRAIN_HOST, port: int = DEFAULT_DRAIN_PORT) -> None:
    if host not in ("127.0.0.1", "localhost"):
        raise ValueError("Drain server binds loopback only.")
    httpd = ThreadingHTTPServer((host, port), DrainHandler)
    print(f"ChatVault DA drain listening on http://{host}:{port}")
    print("Pull from ChatVault ingest → Drain, or GET /queue")
    httpd.serve_forever()
