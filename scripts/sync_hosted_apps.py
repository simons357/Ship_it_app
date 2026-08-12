#!/usr/bin/env python3
"""Mirror published *.base44.app and *.replit.app frontends into titan-x-web/apps/."""

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
        "slug": "explorer",
        "base": "https://sfe-rh-explorer-v1-07f8121c.base44.app/",
        "title": "Primefield Explorer",
        "routes": [],
    },
    {
        "slug": "solenne",
        "base": "https://solenne.base44.app/",
        "title": "Solenne",
        "routes": [],
    },
    {
        "slug": "maritime",
        "base": "https://maritime-coherence-dashboard-100b68c0.base44.app/",
        "title": "Maritime Coherence Dashboard",
        "routes": [],
    },
    {
        "slug": "primefield",
        "base": "https://primefield.tech/",
        "title": "Prime Field Technologies",
        "routes": ["chatvault", "field-lock", "games", "pacman", "qstack", "risk"],
    },
    {
        "slug": "exoratio",
        "base": "https://exo-ratio-014dea2d.base44.app/",
        "title": "ExoRatio",
        "routes": [],
    },
    {
        "slug": "field-lock",
        "base": "https://field-lock.replit.app/",
        "title": "Field Lock — Learning Kiosk",
        "routes": [],
    },
    {
        "slug": "nav-42",
        "base": "https://nav-42.replit.app/",
        "title": "NAV-42 Adaptive Lattice",
        "routes": [],
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
    return found


def rewrite_html(html: str, prefix: str) -> str:
    html = re.sub(r'(src|href)="/', rf'\1="{prefix}', html)
    html = re.sub(r"url\(/", f"url({prefix}", html)
    return html


def write_html(path: Path, html: str, prefix: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(rewrite_html(html, prefix), encoding="utf-8")


def is_spa_route(path: str) -> bool:
    if path in {"/", "#"}:
        return False
    name = path.strip("/").split("/")[0]
    if not name or "." in name:
        return False
    if name in {"assets", "static", "api", "manifest.json"}:
        return False
    return name[:1].isupper() or name in {
        "chatvault",
        "field-lock",
        "games",
        "Home",
        "Settings",
        "Resources",
        "HarmonicInsights",
        "ManagePanels",
    }


def mirror(app: dict) -> None:
    slug, base = app["slug"], app["base"]
    dest = DEST / slug
    dest.mkdir(parents=True, exist_ok=True)
    print(f"=== {app['title']} ({base}) ===")
    try:
        raw = fetch(base)
    except Exception as e:
        print(f"  skip: {e}")
        return
    html = raw.decode("utf-8", "replace")
    if "This app isn't live yet" in html or "MonacoEnvironment" in html:
        print("  skip: not a public app shell")
        return

    write_html(dest / "index.html", html, "./")
    extras = {"/favicon.png", "/favicon.ico", "/manifest.json", "/robots.txt"}
    routes = set(app.get("routes") or [])
    for path in sorted(local_paths(html) | extras):
        if path in {"/", "#"}:
            continue
        if is_spa_route(path):
            routes.add(path.strip("/").split("/")[0])
            continue
        url = urljoin(base, path)
        rel = path.lstrip("/")
        out = dest / rel
        try:
            data = fetch(url)
        except Exception as e:
            print(f"  miss {path}: {e}")
            continue
        if data.startswith(b"<!DOCTYPE") and not rel.endswith((".html", ".htm")):
            continue
        if len(data) > 400_000 and not rel.endswith((".js", ".css")):
            print(f"  skip large {rel} ({len(data)} bytes)")
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(data)
        print(f"  {out.relative_to(DEST)} ({len(data)} bytes)")

    for route in sorted(routes):
        try:
            page = fetch(urljoin(base, route)).decode("utf-8", "replace")
        except Exception:
            page = html
        if "MonacoEnvironment" in page:
            continue
        write_html(dest / route / "index.html", page, "../")
        print(f"  route {route}/")


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    for app in APPS:
        mirror(app)


if __name__ == "__main__":
    main()
