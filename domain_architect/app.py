"""Desktop Domain Architect application.

``python -m domain_architect app`` serves a local UI and opens it in the
browser. ``--install-shortcut`` writes a Desktop launcher.
"""

from __future__ import annotations

import json
import socket
import sys
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .audit import audit_expression
from .cycle import CycleSpec, run_cycle
from .historical import HISTORICAL_NOTE
from .pipeline import run_benchmarks, run_named_cycle
from .registry import EquationRegistry
from .schema import PRIMARY_OPERATIONS, PRODUCT_DESCRIPTION
from .synthesize import inverse_design_architecture
from .translate import mechanical_electrical_translation, translate_expressions

STATIC_DIR = Path(__file__).resolve().parent / "static"
ICON_SVG = Path(__file__).resolve().parent.parent / "assets" / "domain-architect.svg"
REPO_ROOT = Path(__file__).resolve().parent.parent


def _json_bytes(payload: object, status: int = 200) -> tuple[int, bytes, str]:
    body = json.dumps(payload, indent=2, default=str).encode("utf-8")
    return status, body, "application/json; charset=utf-8"


def handle_api(path: str, payload: dict) -> tuple[int, bytes, str]:
    try:
        if path == "/api/status":
            return _json_bytes(
                {
                    "product": "Domain Architect",
                    "operations": PRIMARY_OPERATIONS,
                    "description": PRODUCT_DESCRIPTION,
                    "version": "1.1.0",
                    "historical_note": HISTORICAL_NOTE,
                }
            )
        if path == "/api/decompose":
            expression = str(payload.get("expression") or "").strip()
            if not expression:
                return _json_bytes({"error": "expression is required"}, 400)
            report = audit_expression(expression)
            return _json_bytes(report.to_dict())
        if path == "/api/translate":
            example = payload.get("example")
            if example == "mechanical-electrical" or not (
                payload.get("left") and payload.get("right")
            ):
                record = mechanical_electrical_translation()
            else:
                record = translate_expressions(
                    str(payload["left"]),
                    str(payload["right"]),
                )
            return _json_bytes(record.to_dict())
        if path == "/api/synthesize":
            target = str(payload.get("target") or "").strip()
            if not target:
                return _json_bytes({"error": "target is required"}, 400)
            constraints = [str(c) for c in payload.get("constraints") or []]
            cand = inverse_design_architecture(target, constraints)
            return _json_bytes(cand.to_dict())
        if path == "/api/cycle":
            name = str(payload.get("name") or "missing-damping")
            report = run_named_cycle(name)
            return _json_bytes(report.to_dict())
        if path == "/api/inverse-cycle":
            spec = CycleSpec(
                target=str(payload.get("target") or "x★"),
                constraints=[str(c) for c in payload.get("constraints") or []],
                plant=payload.get("plant"),
            )
            report = run_cycle(spec, mode="synthesis")
            return _json_bytes(report.to_dict())
        if path == "/api/benchmark":
            return _json_bytes(run_benchmarks())
        if path == "/api/archive":
            registry = EquationRegistry.load_default()
            payload_out = registry.export()
            payload_out["note"] = HISTORICAL_NOTE
            return _json_bytes(payload_out)
    except Exception as exc:
        return _json_bytes({"error": str(exc)}, 400)
    return _json_bytes({"error": f"unknown endpoint {path}"}, 404)


class DomainArchitectHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def log_message(self, format: str, *args) -> None:
        sys.stderr.write("[da-app] " + (format % args) + "\n")

    def _send(self, status: int, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        parsed = urlparse(self.path)
        if parsed.path.startswith("/api/"):
            status, body, ctype = handle_api(parsed.path, {})
            self._send(status, body, ctype)
            return
        if parsed.path in {"/icon.svg", "/assets/domain-architect.svg"}:
            data = ICON_SVG.read_bytes() if ICON_SVG.exists() else b""
            self._send(200, data, "image/svg+xml")
            return
        if parsed.path == "/favicon.svg":
            fav = STATIC_DIR / "favicon.svg"
            self._send(200, fav.read_bytes() if fav.exists() else b"", "image/svg+xml")
            return
        if parsed.path == "/":
            self.path = "/index.html"
        return super().do_GET()

    def do_POST(self) -> None:
        parsed = urlparse(self.path)
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8") or "{}")
        except json.JSONDecodeError:
            payload = {}
        status, body, ctype = handle_api(parsed.path, payload if isinstance(payload, dict) else {})
        self._send(status, body, ctype)


def _free_port(preferred: int) -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.bind(("127.0.0.1", preferred))
            return preferred
        except OSError:
            sock.bind(("127.0.0.1", 0))
            return int(sock.getsockname()[1])


def serve(port: int = 8765, open_browser: bool = True) -> None:
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
    port = _free_port(port)
    server = ThreadingHTTPServer(("127.0.0.1", port), DomainArchitectHandler)
    url = f"http://127.0.0.1:{port}/"
    print(f"Domain Architect desktop app: {url}")
    print(PRIMARY_OPERATIONS)
    if open_browser:
        threading.Timer(0.4, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nDomain Architect stopped.")
        server.shutdown()


def install_desktop_shortcut(desktop: Path | None = None) -> Path:
    """Write a launcher onto the user's Desktop."""
    desktop = desktop or Path.home() / "Desktop"
    desktop.mkdir(parents=True, exist_ok=True)
    python = sys.executable
    workdir = str(REPO_ROOT)
    icon = str(ICON_SVG) if ICON_SVG.exists() else ""

    if sys.platform == "darwin":
        path = desktop / "Domain Architect.command"
        path.write_text(
            "#!/bin/bash\n"
            f'cd "{workdir}"\n'
            f'exec "{python}" -m domain_architect app\n',
            encoding="utf-8",
        )
        path.chmod(path.stat().st_mode | 0o111)
        return path

    path = desktop / "Domain Architect.desktop"
    path.write_text(
        "[Desktop Entry]\n"
        "Type=Application\n"
        "Name=Domain Architect\n"
        "Comment=Functional-role decompose, translate, synthesize\n"
        f"Exec={python} -m domain_architect app\n"
        f"Path={workdir}\n"
        f"Icon={icon}\n"
        "Terminal=false\n"
        "Categories=Science;Education;\n",
        encoding="utf-8",
    )
    path.chmod(path.stat().st_mode | 0o111)
    apps = Path.home() / ".local" / "share" / "applications"
    try:
        apps.mkdir(parents=True, exist_ok=True)
        app_copy = apps / "domain-architect.desktop"
        app_copy.write_text(path.read_text(encoding="utf-8"), encoding="utf-8")
        app_copy.chmod(app_copy.stat().st_mode | 0o111)
    except OSError:
        pass
    return path


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    if "--install-shortcut" in argv:
        print(install_desktop_shortcut())
        return 0
    port = 8765
    if "--port" in argv:
        port = int(argv[argv.index("--port") + 1])
    serve(port=port, open_browser="--no-browser" not in argv)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
