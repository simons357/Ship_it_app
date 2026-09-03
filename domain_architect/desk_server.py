"""Simple Domain Architect desk — inquire, see, compute.

This is the scientific product you can open in a browser. It is not
ChatVault, not CosmoEvolution, and not the kitchen-sink PWA on PR #43.
Connor / Aron / a Zeta-zero app are not in this git; live compute here
is Domain Architect itself. Track Q is an honest arithmetic face, not a
zero-prover.
"""

from __future__ import annotations

import json
import mimetypes
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

from .audit import audit_expression
from .desk import proceed_report, refuse_splice
from .jigsaw import jigsaw_report
from .ns_tube import tube_estimate
from .schema import CANONICAL_SFE_STATUS, PRODUCT_DESCRIPTION
from .think_tank import consult
from .visual import write_see


REPO = Path(__file__).resolve().parents[1]
STATIC = Path(__file__).resolve().parent / "desk_static"
SEE = REPO / "docs" / "domain-architect"
DEFAULT_PORT = 8765
ALLOWED_HOSTS = frozenset({"127.0.0.1", "localhost", "0.0.0.0"})
MAX_POST = 64 * 1024


def resolve_host(explicit: str | None = None) -> str:
    host = (explicit or "").strip() or (
        "0.0.0.0"
        if os.environ.get("REPL_ID") or os.environ.get("REPLIT_DEV_DOMAIN")
        else "127.0.0.1"
    )
    if host not in ALLOWED_HOSTS:
        raise ValueError("Desk binds loopback, or 0.0.0.0 for Replit.")
    return host


def resolve_port(explicit: int | None = None) -> int:
    if explicit is not None:
        return int(explicit)
    raw = os.environ.get("PORT")
    return int(raw) if raw else DEFAULT_PORT


def _safe(root: Path, rel: str) -> Path | None:
    target = (root / rel).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return None
    return target


def _json(handler: BaseHTTPRequestHandler, code: int, payload: dict[str, Any]) -> None:
    data = json.dumps(payload, indent=2, default=str).encode("utf-8")
    handler.send_response(code)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(data)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(data)


class DeskHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return

    def _file(self, path: Path) -> None:
        if not path.is_file():
            _json(self, 404, {"ok": False, "error": "not found"})
            return
        blob = path.read_bytes()
        ctype, _ = mimetypes.guess_type(str(path))
        if path.suffix == ".svg":
            ctype = "image/svg+xml"
        self.send_response(200)
        self.send_header("Content-Type", ctype or "application/octet-stream")
        self.send_header("Content-Length", str(len(blob)))
        self.end_headers()
        self.wfile.write(blob)

    def do_GET(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        if path in {"/", "/index.html"}:
            self._file(STATIC / "index.html")
            return
        if path.startswith("/static/"):
            rel = path[len("/static/") :]
            target = _safe(STATIC, rel)
            if target:
                self._file(target)
                return
        if path.startswith("/see/"):
            rel = path[len("/see/") :]
            target = _safe(SEE, rel)
            if target:
                self._file(target)
                return
        if path == "/api/health":
            _json(
                self,
                200,
                {
                    "ok": True,
                    "product": "Domain Architect",
                    "canonical_sfe_status": CANONICAL_SFE_STATUS,
                    "not_chatvault": True,
                    "not_cosmo": True,
                    "not_a_proof": True,
                },
            )
            return
        if path == "/api/proceed":
            _json(self, 200, proceed_report())
            return
        if path == "/api/jigsaw":
            qs = parse_qs(parsed.query)
            book = (qs.get("book") or ["B"])[0]
            _json(self, 200, jigsaw_report(book))
            return
        if path == "/api/tube":
            _json(self, 200, tube_estimate())
            return
        if path == "/api/consult":
            qs = parse_qs(parsed.query)
            topic = (qs.get("topic") or ["jigsaw"])[0]
            _json(self, 200, consult(topic))
            return
        if path in {"/api/inbox", "/api/inquiry", "/api/drain", "/api/drain/queue"}:
            _json(
                self,
                404,
                {
                    "ok": False,
                    "error": "no vault drain on this desk",
                    "not_chatvault": True,
                },
            )
            return
        _json(self, 404, {"ok": False, "error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        parsed = urlparse(self.path)
        path = unquote(parsed.path)
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_POST:
            _json(self, 413, {"ok": False, "error": "too large"})
            return
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            _json(self, 400, {"ok": False, "error": "bad json"})
            return
        if not isinstance(body, dict):
            _json(self, 400, {"ok": False, "error": "object required"})
            return
        if path == "/api/audit":
            expr = str(body.get("expression") or "").strip()
            if not expr:
                _json(self, 400, {"ok": False, "error": "expression required"})
                return
            report = audit_expression(expr)
            payload = report.to_dict()
            payload["ok"] = True
            payload["not_a_proof"] = True
            _json(self, 200, payload)
            return
        if path == "/api/refuse":
            src = str(body.get("source") or "")
            dst = str(body.get("target") or "")
            decision = refuse_splice(src, dst)
            _json(self, 200, decision.to_dict())
            return
        if path in {"/api/inbox", "/api/inquiry", "/api/drain", "/api/drain/queue"}:
            _json(
                self,
                404,
                {
                    "ok": False,
                    "error": "no vault drain on this desk",
                    "not_chatvault": True,
                },
            )
            return
        _json(self, 404, {"ok": False, "error": "not found"})


def serve_site(host: str | None = None, port: int | None = None) -> None:
    write_see()
    bind_host = resolve_host(host)
    bind_port = resolve_port(port)
    httpd = ThreadingHTTPServer((bind_host, bind_port), DeskHandler)
    display = "127.0.0.1" if bind_host in {"0.0.0.0", "127.0.0.1"} else bind_host
    print(PRODUCT_DESCRIPTION)
    print(f"Simple desk: http://{display}:{bind_port}/")
    print("Inquire + see + compute. Not ChatVault. Not Cosmo. Not a proof.")
    print("PR #43 is the kitchen-sink PWA. This is the small scientific product.")
    httpd.serve_forever()
