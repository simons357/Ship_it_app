"""Serve Domain Architect homepage + ChatVault on one loopback origin.

    python -m domain_architect --site

http://127.0.0.1:8765/           DA homepage (ChatVault search dock + PWA)
http://127.0.0.1:8765/da-sw.js   Combined-origin service worker (skips /chatvault/)
http://127.0.0.1:8765/chatvault/ ChatVault PWA (same localStorage origin)
POST /api/audit                  FRA audit JSON (never cached by the DA worker)
GET/POST /api/drain/...          ChatVault drain queue
POST /api/inquiry                FRA inquiry JSON (optional drain export; never a proof)
GET  /api/route-c                Route C exploratory face metadata (not ChatVault)
GET  /faces/*.pdf                DA research faces (Route C PDF)
GET/POST /api/inbox              Repo inbox JSON sidecars (loopback POST, no binary upload)
"""

from __future__ import annotations

import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from .audit import audit_expression
from .chatvault_bridge import CHATVAULT_EXPORT_FORMAT, drain_audit, inquire
from .chatvault_ingest import list_inbox_files, write_inbox_payload
from .drain_server import QUEUE, _json_response
from .route_c import face as route_c_face

REPO = Path(__file__).resolve().parents[1]
STATIC = Path(__file__).resolve().parent / "static"
CHATVAULT = REPO / "chatvault"
DEFAULT_SITE_PORT = 8765
MAX_INBOX_POST_BYTES = 2 * 1024 * 1024


def _is_loopback(handler: BaseHTTPRequestHandler) -> bool:
    host = str(handler.client_address[0] if handler.client_address else "")
    return host in {"127.0.0.1", "::1", "localhost", "::ffff:127.0.0.1"}


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
    if path.suffix == ".pdf":
        return "application/pdf"
    if path.suffix == ".webmanifest":
        return "application/manifest+json"
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
        if path.name == "da-sw.js":
            self.send_header("Service-Worker-Allowed", "/")
            self.send_header("Cache-Control", "no-cache")
        if "inbox" in path.parts:
            self.send_header("Cache-Control", "no-store")
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
        if path == "/api/inbox":
            files = list_inbox_files(CHATVAULT / "inbox")
            _json_response(
                self,
                200,
                {
                    "ok": True,
                    "format": "chatvault-inbox-index",
                    "count": len(files),
                    "files": files,
                },
            )
            return
        if path == "/api/route-c":
            _json_response(self, 200, route_c_face())
            return
        if path.startswith("/chatvault/"):
            rel = path[len("/chatvault/") :] or "index.html"
            target = _safe(CHATVAULT, rel)
            if target and target.is_dir():
                html = target / "index.html"
                listing = target / "index.json"
                target = html if html.is_file() else listing if listing.is_file() else html
            if target:
                self._file(target)
                return
            _json_response(self, 404, {"ok": False, "error": "not found"})
            return
        if path.startswith("/faces/"):
            rel = path[len("/faces/") :]
            target = _safe(STATIC / "faces", rel)
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
        if path == "/api/inbox":
            self._post_inbox()
            return
        try:
            data = self._read_json()
        except json.JSONDecodeError:
            _json_response(self, 400, {"ok": False, "error": "invalid JSON"})
            return
        if path == "/api/audit":
            expression = str(data.get("expression") or data.get("inquiry") or "")
            if not expression.strip():
                _json_response(self, 400, {"ok": False, "error": "expression required"})
                return
            report = audit_expression(expression)
            _json_response(self, 200, report.to_dict())
            return
        if path == "/api/inquiry":
            text = str(data.get("inquiry") or data.get("expression") or "")
            try:
                payload = inquire(text, drain=bool(data.get("drain")))
            except ValueError as err:
                _json_response(self, 400, {"ok": False, "error": str(err)})
                return
            _json_response(self, 200, payload)
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

    def _post_inbox(self) -> None:
        if not _is_loopback(self):
            _json_response(self, 403, {"ok": False, "error": "inbox writes are loopback only"})
            return
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_INBOX_POST_BYTES:
            _json_response(
                self,
                413,
                {
                    "ok": False,
                    "error": (
                        f"JSON sidecar exceeds {MAX_INBOX_POST_BYTES} bytes. "
                        "CLI --ingest-chatvault copies media; POST is JSON only."
                    ),
                },
            )
            return
        raw = self.rfile.read(length) if length else b"{}"
        try:
            data = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            _json_response(self, 400, {"ok": False, "error": "invalid JSON"})
            return
        try:
            written = write_inbox_payload(data, CHATVAULT / "inbox")
        except ValueError as err:
            _json_response(self, 400, {"ok": False, "error": str(err)})
            return
        _json_response(
            self,
            200,
            {"ok": True, "written": [path.name for path in written], "count": len(written)},
        )


def serve_site(host: str = "127.0.0.1", port: int = DEFAULT_SITE_PORT) -> None:
    if host not in ("127.0.0.1", "localhost"):
        raise ValueError("Site server binds loopback only.")
    httpd = ThreadingHTTPServer((host, port), SiteHandler)
    print(f"Domain Architect + ChatVault at http://{host}:{port}/")
    print(f"ChatVault app at http://{host}:{port}/chatvault/")
    print(f"Repo inbox JSON at http://{host}:{port}/chatvault/inbox/")
    print(f"Route C PDF at http://{host}:{port}/faces/05_route_c_conditional.pdf")
    httpd.serve_forever()
