#!/usr/bin/env python3
"""Restore Zenodo public titles via the deposit API.

One command, once a personal access token exists:

    python3 docs/zenodo-public-record/api_restore_titles.py --apply

Token env (first non-empty wins): ZENODO_TOKEN, ZENODO_ACCESS_TOKEN,
ZENODO_PAT, ZENODO_API_TOKEN.

Scopes: deposit:write, deposit:actions.
Never a zenodo.org password. Default is dry-run (no writes).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

PACK = Path(__file__).resolve().parent
API = "https://zenodo.org/api/deposit/depositions"
TOKEN_ENV_NAMES = (
    "ZENODO_TOKEN",
    "ZENODO_ACCESS_TOKEN",
    "ZENODO_PAT",
    "ZENODO_API_TOKEN",
)
TOKEN_CREATE_URL = "https://zenodo.org/account/settings/applications/tokens/new/"
APPLY_CMD = "python3 docs/zenodo-public-record/api_restore_titles.py --apply"


class ZenodoError(Exception):
    def __init__(self, method: str, url: str, code: int, detail: str) -> None:
        self.method = method
        self.url = url
        self.code = code
        self.detail = detail
        super().__init__(f"{method} {url} -> {code}: {detail}")


def load() -> dict:
    return json.loads((PACK / "titles.json").read_text(encoding="utf-8"))


def token_from_env() -> tuple[str, str]:
    for name in TOKEN_ENV_NAMES:
        val = os.environ.get(name, "").strip()
        if val:
            return name, val
    return "", ""


def owner_token_note() -> str:
    return (
        "No Zenodo personal access token in the environment.\n"
        "\n"
        "The only permission an agent needs is a Zenodo PAT:\n"
        f"  {TOKEN_CREATE_URL}\n"
        "  scopes: deposit:write, deposit:actions\n"
        "\n"
        "Send: “use this token” plus the token as env ZENODO_TOKEN "
        "(or ZENODO_ACCESS_TOKEN).\n"
        "Do not send the zenodo.org password. Do not click Edit on each record.\n"
        "\n"
        f"Then:\n  {APPLY_CMD}\n"
    )


def jobs(data: dict) -> list[dict]:
    rows = []
    st = data["status_note"]
    rows.append(
        {
            "id": st["latest_id"],
            "title": st["restore_title"],
            "description_html": st["description_html"],
        }
    )
    rows.append(
        {
            "id": 22045484,
            "title": st["restore_title"],
            "description_html": st["description_html"],
        }
    )
    pointer = data["calm_pointer_html"]
    for rec in data["restore"]:
        rows.append(
            {
                "id": rec["id"],
                "title": rec["restore_title"],
                "description_html": pointer,
            }
        )
    for rec in data.get("optional_rename", []):
        rows.append(
            {
                "id": rec["id"],
                "title": rec["restore_title"],
                "description_html": pointer,
                "optional": True,
            }
        )
    return rows


def request(method: str, url: str, token: str, body: dict | None = None) -> dict:
    data = None
    headers = {
        "Authorization": f"Bearer {token}",
        "User-Agent": "ShipItRestore/1.0 (title restore; deposit API)",
        "Accept": "application/json",
    }
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:800]
        raise ZenodoError(method, url, exc.code, detail) from exc


def apply_one(job: dict, token: str) -> None:
    rec_id = job["id"]
    try:
        request("POST", f"{API}/{rec_id}/actions/edit", token)
    except ZenodoError as exc:
        # Already in edit / unlocked is fine; anything else is fatal.
        blob = (exc.detail or "").lower()
        if exc.code not in (400, 409) and "already" not in blob:
            raise
    current = request("GET", f"{API}/{rec_id}", token)
    meta = dict(current.get("metadata") or {})
    meta["title"] = job["title"]
    meta.pop("doi", None)
    desc = meta.get("description") or ""
    # Drop screaming August paragraphs; append the calm pointer once.
    lowered = desc.lower()
    if "claim withdrawn" in lowered or "claims are withdrawn" in lowered:
        parts = desc.split("<p>")
        kept = []
        for part in parts:
            blob = part.lower()
            if "status note, august 2026" in blob or "claim withdrawn" in blob:
                continue
            if "full-spectrum spectral floor claims are withdrawn" in blob:
                continue
            kept.append(part)
        desc = "<p>".join(kept).strip()
    if "10.5281/zenodo.22050978" not in desc:
        desc = (desc.rstrip() + "\n\n" + job["description_html"]).strip()
    meta["description"] = desc
    request("PUT", f"{API}/{rec_id}", token, {"metadata": meta})
    request("POST", f"{API}/{rec_id}/actions/publish", token)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dry-run (default) or apply Zenodo title restores."
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Write titles on zenodo.org. Requires a PAT. Never a password.",
    )
    parser.add_argument(
        "--include-optional",
        action="store_true",
        help="Also rename 22045478.",
    )
    args = parser.parse_args()
    data = load()
    planned = [
        j
        for j in jobs(data)
        if args.include_optional or not j.get("optional")
    ]
    print("Planned title restores (this agent will not log in with a password):")
    for job in planned:
        print(f"  {job['id']}\t{job['title']}")
    print(f"\n{len(planned)} jobs. One command: {APPLY_CMD}")
    if not args.apply:
        print("\nDry-run only. Pass --apply with a Zenodo PAT to execute.")
        name, token = token_from_env()
        if token:
            print(f"Token present in {name} (not used: dry-run).")
        else:
            print("No PAT in env. Titles will not be written until one arrives.")
        return 0
    name, token = token_from_env()
    if not token:
        print(owner_token_note(), file=sys.stderr)
        return 2
    if " " in token or len(token) < 20:
        print(
            f"{name} does not look like a personal access token.",
            file=sys.stderr,
        )
        return 2
    for job in planned:
        print(f"applying {job['id']}…")
        try:
            apply_one(job, token)
        except ZenodoError as exc:
            print(f"FAILED {job['id']}: {exc}", file=sys.stderr)
            return 1
        print(f"  published {job['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
