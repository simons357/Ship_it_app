"""Replaceable LISTENER hub. Session/node presence + event queue. Not a classifier."""
from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent / "data"
ROOT.mkdir(exist_ok=True)


def _path(*parts: str) -> Path:
    p = ROOT.joinpath(*parts)
    p.parent.mkdir(parents=True, exist_ok=True)
    return p


class Hub(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        return

    def _json(self, code, payload):
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("content-type", "application/json")
        self.send_header("access-control-allow-origin", "*")
        self.send_header("access-control-allow-headers", "content-type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        self._json(204, {})

    def do_GET(self):
        parts = urlparse(self.path).path.strip("/").split("/")
        if parts[:2] == ["v1", "health"]:
            return self._json(200, {"ok": True, "role": "hub"})
        if parts[:2] == ["v1", "presence"]:
            path = _path("presence.json")
            if not path.exists():
                return self._json(200, [])
            return self._json(200, json.loads(path.read_text()))
        if parts[:2] == ["v1", "sessions"] and len(parts) == 4 and parts[3] == "events":
            path = _path(parts[2], "events.json")
            if not path.exists():
                return self._json(200, [])
            return self._json(200, json.loads(path.read_text()))
        return self._json(404, {"error": "not found"})

    def do_POST(self):
        n = int(self.headers.get("content-length") or 0)
        raw = self.rfile.read(n) if n else b"{}"
        try:
            event = json.loads(raw.decode() or "{}")
        except json.JSONDecodeError:
            return self._json(400, {"error": "bad json"})
        parts = urlparse(self.path).path.strip("/").split("/")
        payload = event.get("payload") or {}
        session_id = payload.get("sessionId") or event.get("sessionId") or "unknown"
        if parts[:2] == ["v1", "presence"]:
            path = _path("presence.json")
            rows = json.loads(path.read_text()) if path.exists() else []
            rows.append({**event, "receivedAt": __import__("time").time()})
            path.write_text(json.dumps(rows))
            return self._json(200, {"ok": True, "role": "hub", "stored": True})
        path = _path(session_id, "events.json")
        rows = json.loads(path.read_text()) if path.exists() else []
        rows.append(event)
        path.write_text(json.dumps(rows))
        return self._json(200, {"ok": True, "queued": False, "stored": True})


def main():
    server = ThreadingHTTPServer(("127.0.0.1", 7744), Hub)
    print("LISTENER hub http://127.0.0.1:7744")
    server.serve_forever()


if __name__ == "__main__":
    main()
