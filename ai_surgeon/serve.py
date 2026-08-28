"""Serve the AI Surgeon hub on a dedicated loopback port.

    python3 -m ai_surgeon
    python3 -m ai_surgeon --port 8770

http://127.0.0.1:8770/              hub (index)
http://127.0.0.1:8770/ai-surgeon/   same hub, prefixed path
http://127.0.0.1:8770/ai-surgeon-prototype.html
http://127.0.0.1:8770/ai-surgeon-module02-trauma.html

Does not bind Domain Architect's 8765 and does not mount DA faces.
From this directory, `python3 -m http.server 8770` also works; relative
asset paths are the same either way.
"""

from __future__ import annotations

import argparse
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

from . import DEFAULT_PORT, ROOT

PREFIX = "/ai-surgeon"


def _safe(root: Path, rel: str) -> Path | None:
    target = (root / rel).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError:
        return None
    return target


def _content_type(path: Path) -> str:
    if path.suffix == ".js":
        return "text/javascript; charset=utf-8"
    if path.suffix == ".mjs":
        return "text/javascript; charset=utf-8"
    if path.suffix == ".md":
        return "text/markdown; charset=utf-8"
    if path.suffix == ".pdf":
        return "application/pdf"
    if path.suffix in {".jpg", ".jpeg"}:
        return "image/jpeg"
    if path.suffix == ".png":
        return "image/png"
    if path.suffix == ".webp":
        return "image/webp"
    if path.suffix == ".svg":
        return "image/svg+xml"
    if path.suffix.lower() == ".mp4":
        return "video/mp4"
    if path.suffix.lower() == ".webm":
        return "video/webm"
    if path.suffix == ".html":
        return "text/html; charset=utf-8"
    if path.suffix == ".txt":
        return "text/plain; charset=utf-8"
    if path.suffix == ".pages":
        return "application/octet-stream"
    if path.suffix == ".docx":
        return "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    if path.suffix == ".css":
        return "text/css; charset=utf-8"
    if path.suffix == ".json":
        return "application/json; charset=utf-8"
    guessed, _ = mimetypes.guess_type(str(path))
    return guessed or "application/octet-stream"


def public_path(url_path: str) -> str:
    """Strip an optional /ai-surgeon prefix and map directories to index.html."""
    path = unquote(urlparse(url_path).path)
    if path == PREFIX or path.startswith(PREFIX + "/"):
        path = path[len(PREFIX) :] or "/"
    if path in ("", "/"):
        return "index.html"
    if path.endswith("/"):
        path = path + "index.html"
    return path.lstrip("/")


class SurgeonHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return

    def do_GET(self) -> None:  # noqa: N802
        rel = public_path(self.path)
        target = _safe(ROOT, rel)
        if target and target.is_dir():
            target = target / "index.html"
        if not target or not target.is_file():
            body = b'{"ok":false,"error":"not found"}'
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        data = target.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", _content_type(target))
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)


def serve(host: str = "127.0.0.1", port: int = DEFAULT_PORT) -> None:
    if host not in ("127.0.0.1", "localhost"):
        raise ValueError("AI Surgeon binds loopback only.")
    httpd = ThreadingHTTPServer((host, port), SurgeonHandler)
    print(f"AI Surgeon hub at http://{host}:{port}/")
    print(f"Prefixed path     http://{host}:{port}{PREFIX}/")
    print(f"Appendectomy      http://{host}:{port}/ai-surgeon-prototype.html")
    print(f"Trauma module 02  http://{host}:{port}/ai-surgeon-module02-trauma.html")
    print(f"Phone screens     http://{host}:{port}/screens.html")
    print(f"The Pen           http://{host}:{port}/pen.html")
    print(f"Manga gift        http://{host}:{port}/manga/")
    print(f"Cartoon dojo      http://{host}:{port}/dojo.html")
    print(f"Brochure PDF      http://{host}:{port}/generators/AI-Surgeon-Brochure.pdf")
    httpd.serve_forever()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Serve the AI Surgeon residency hub.")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    args = parser.parse_args(argv)
    serve(host=args.host, port=args.port)
    return 0
