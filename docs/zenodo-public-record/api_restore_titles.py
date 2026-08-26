#!/usr/bin/env python3
"""Optional later-agent helper: print (or apply) Zenodo title PATCHes.

Default is dry-run. Requires env ZENODO_TOKEN (personal access token with
deposit:write and deposit:actions). Never a zenodo.org password.
This script does not run against zenodo.org unless you pass --apply.
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


def load() -> dict:
    return json.loads((PACK / "titles.json").read_text(encoding="utf-8"))


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
    headers = {"Authorization": f"Bearer {token}"}
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
        raise SystemExit(f"{method} {url} -> {exc.code}: {detail}") from exc


def apply_one(job: dict, token: str) -> None:
    rec_id = job["id"]
    request("POST", f"{API}/{rec_id}/actions/edit", token)
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
        help="Actually PATCH zenodo.org. Requires ZENODO_TOKEN. Never a password.",
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
    if not args.apply:
        print("\nDry-run only. Pass --apply with env ZENODO_TOKEN to execute.")
        return 0
    token = os.environ.get("ZENODO_TOKEN", "").strip()
    if not token:
        print("ZENODO_TOKEN is not set. Create a personal access token; never a password.", file=sys.stderr)
        return 2
    if " " in token or len(token) < 20:
        print("ZENODO_TOKEN does not look like a personal access token.", file=sys.stderr)
        return 2
    for job in planned:
        print(f"applying {job['id']}…")
        apply_one(job, token)
        print(f"  published {job['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
