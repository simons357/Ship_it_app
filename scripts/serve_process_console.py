#!/usr/bin/env python3
"""Serve Process Console v5 on localhost."""

from __future__ import annotations

import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from domain_architect.process_console import ProcessConsole


def make_handler(console: ProcessConsole):
    snapshot = console.snapshot()
    html = console.render_html()
    ledger = json.dumps(snapshot.to_dict(), indent=2).encode()

    class Handler(BaseHTTPRequestHandler):
        def _send(self, code: int, body: bytes, content_type: str) -> None:
            self.send_response(code)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)

        def do_GET(self) -> None:  # noqa: N802
            if self.path in {"/", "/index.html"}:
                self._send(200, html.encode(), "text/html; charset=utf-8")
                return
            if self.path in {"/api/ledger", "/ledger.json"}:
                self._send(200, ledger, "application/json")
                return
            if self.path.startswith("/api/runs/"):
                run_id = self.path.rsplit("/", 1)[-1]
                try:
                    view = snapshot.view_for(run_id)
                except KeyError:
                    self._send(404, b'{"error":"unknown run"}', "application/json")
                    return
                self._send(
                    200,
                    json.dumps(view.to_dict(), indent=2).encode(),
                    "application/json",
                )
                return
            self._send(404, b"not found", "text/plain; charset=utf-8")

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/api/promote":
                self._send(404, b"not found", "text/plain; charset=utf-8")
                return
            length = int(self.headers.get("Content-Length", "0") or 0)
            raw = self.rfile.read(length) if length else b"{}"
            try:
                payload = json.loads(raw.decode() or "{}")
            except json.JSONDecodeError:
                payload = {}
            run_id = str(payload.get("run_id") or "")
            try:
                result = console.promote(run_id)
            except KeyError:
                self._send(404, b'{"error":"unknown run"}', "application/json")
                return
            code = 200 if result["allowed"] else 409
            self._send(code, json.dumps(result).encode(), "application/json")

        def log_message(self, fmt: str, *args: object) -> None:
            sys.stderr.write("console: " + (fmt % args) + "\n")

    return Handler


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Serve Process Console v5")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    args = parser.parse_args(argv)
    console = ProcessConsole()
    console.write_static()
    server = ThreadingHTTPServer((args.host, args.port), make_handler(console))
    print(f"Process Console v5 at http://{args.host}:{args.port}/")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
