#!/usr/bin/env python3
"""Mirror published Replit (and similar) frontends into titan-x-web/apps/."""

from __future__ import annotations

import re
import urllib.request
from pathlib import Path
from urllib.parse import urljoin, urlparse

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / "titan-x-web" / "apps"
UA = {"User-Agent": "Mozilla/5.0 (compatible; PrimeFieldMirror/1.0)"}

APPS = [
    {
        "slug": "field-lock",
        "base": "https://field-lock.replit.app/",
        "title": "Field Lock — Learning Kiosk",
    },
    {
        "slug": "nav-42",
        "base": "https://nav-42.replit.app/",
        "title": "NAV-42 Adaptive Lattice",
    },
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        if r.status >= 400:
            raise RuntimeError(f"{r.status} {url}")
        return r.read()


def local_paths(html: str) -> set[str]:
    found = set()
    found.update(re.findall(r"""(?:src|href)=["'](/[^"']+)["']""", html))
    found.update(re.findall(r"""url\(["']?(/[^"')]+)["']?\)""", html))
    found.update(re.findall(r"""content=["'](https?://[^"']+\.(?:png|jpg|jpeg|webp|svg|ico))["']""", html))
    return found


def rewrite_html(html: str, prefix: str) -> str:
    html = re.sub(r'(src|href)="/', rf'\1="{prefix}', html)
    html = re.sub(r"url\(/", f"url({prefix}", html)
    return html


def mirror(app: dict) -> None:
    slug, base = app["slug"], app["base"]
    dest = DEST / slug
    dest.mkdir(parents=True, exist_ok=True)
    print(f"=== {app['title']} ({base}) ===")
    html = fetch(base).decode("utf-8", "replace")
    if "This app isn't live yet" in html or "MonacoEnvironment" in html:
        print("  skip: not a public app shell")
        return
    (dest / "index.html").write_text(rewrite_html(html, "./"), encoding="utf-8")
    extras = {"/favicon.png", "/favicon.ico", "/manifest.json", "/robots.txt"}
    for path in sorted(local_paths(html) | extras):
        parsed = urlparse(path)
        if parsed.scheme in {"http", "https"}:
            url = path
            rel = Path(parsed.path).name
            out = dest / "og" / rel
        else:
            if path in {"/", "#"}:
                continue
            url = urljoin(base, path)
            rel = path.lstrip("/")
            out = dest / rel
        try:
            data = fetch(url)
        except Exception as e:
            print(f"  miss {path}: {e}")
            continue
        if data.startswith(b"<!DOCTYPE") and not rel.endswith(".html"):
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        print(f"  {out.relative_to(DEST)} ({len(data)} bytes)")


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    for app in APPS:
        mirror(app)


if __name__ == "__main__":
    main()
