"""Serve Domain Architect homepage + ChatVault on one loopback origin.

    python -m domain_architect --site

http://127.0.0.1:8765/           DA homepage (ChatVault search dock)
http://127.0.0.1:8765/chatvault/ ChatVault PWA (same localStorage origin)
POST /api/audit                  FRA audit JSON
GET/POST /api/drain/...          ChatVault drain queue
"""

from __future__ import annotations

import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from .audit import audit_expression
from .chatvault_bridge import CHATVAULT_EXPORT_FORMAT, drain_audit
from .drain_server import QUEUE, _json_response

REPO = Path(__file__).resolve().parents[1]
STATIC = Path(__file__).resolve().parent / "static"
CHATVAULT = REPO / "chatvault"
DEFAULT_SITE_PORT = 8765


def _safe(root: Path, rel: str) -> Path | None:
    target = (root / rel).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return None
    return target


def _content_type(path: Path) -> str:
    if path.suffix == ".mjs":
        return "text/javascript; charset=utf-8"
    if path.suffix == ".js":
        return "text/javascript; charset=utf-8"
    guessed, _ = mimetypes.guess_type(str(path))
    return guessed or "application/octet-stream"


class SiteHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return

    def do_OPTIONS(self) -> None:  # noqa: N802
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _file(self, path: Path) -> None:
        if not path.is_file():
            _json_response(self, 404, {"ok": False, "error": "not found"})
            return
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", _content_type(path))
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:  # noqa: N802
        path = unquote(urlparse(self.path).path)
        if path in ("/api/drain/health", "/api/drain"):
            _json_response(
                self,
                200,
                {"ok": True, "service": "chatvault-da-site", "queued": len(QUEUE)},
            )
            return
        if path == "/api/drain/queue":
            _json_response(self, 200, QUEUE.consume())
            return
        if path.startswith("/chatvault/"):
            rel = path[len("/chatvault/") :] or "index.html"
            target = _safe(CHATVAULT, rel)
            if target and target.is_dir():
                target = target / "index.html"
            if target:
                self._file(target)
                return
            _json_response(self, 404, {"ok": False, "error": "not found"})
            return
        rel = path.lstrip("/") or "index.html"
        target = _safe(STATIC, rel)
        if target and target.is_dir():
            target = target / "index.html"
        if target:
            self._file(target)
            return
        _json_response(self, 404, {"ok": False, "error": "not found"})

    def _read_json(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        return json.loads(raw.decode("utf-8") or "{}")

    def do_POST(self) -> None:  # noqa: N802
        path = unquote(urlparse(self.path).path)
        try:
            data = self._read_json()
        except json.JSONDecodeError:
            _json_response(self, 400, {"ok": False, "error": "invalid JSON"})
            return
        if path == "/api/audit":
            expression = str(data.get("expression") or "")
            if not expression.strip():
                _json_response(self, 400, {"ok": False, "error": "expression required"})
                return
            report = audit_expression(expression)
            _json_response(self, 200, report.to_dict())
            return
        if path == "/api/drain/queue":
            try:
                if data.get("format") != CHATVAULT_EXPORT_FORMAT:
                    expression = str(data.get("expression") or "")
                    if not expression.strip():
                        raise ValueError("expression or chatvault-export required")
                    data = drain_audit(expression)
                QUEUE.push(data)
            except (ValueError, TypeError) as err:
                _json_response(self, 400, {"ok": False, "error": str(err)})
                return
            _json_response(self, 200, data)
            return
        _json_response(self, 404, {"ok": False, "error": "not found"})


def serve_site(host: str = "127.0.0.1", port: int = DEFAULT_SITE_PORT) -> None:
    if host not in ("127.0.0.1", "localhost"):
        raise ValueError("Site server binds loopback only.")
    httpd = ThreadingHTTPServer((host, port), SiteHandler)
    print(f"Domain Architect + ChatVault at http://{host}:{port}/")
    print(f"ChatVault app at http://{host}:{port}/chatvault/")
    httpd.serve_forever()
