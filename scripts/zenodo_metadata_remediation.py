#!/usr/bin/env python3
"""Zenodo metadata remediation helper for the Harmonic Blueprint spectral stack.

Audits live Zenodo titles for errata banners in titles (wrong presentation),
compares against data/zenodo/deposit_metadata.json, and optionally applies
metadata fixes via the Zenodo API when ZENODO_ACCESS_TOKEN is set.

Presentation rule enforced:
  - PUBLIC TOP: clean title + honest abstract/description
  - UNDERNEATH: correction/errata notice in description (never in title)

Usage:
  python scripts/zenodo_metadata_remediation.py audit
  python scripts/zenodo_metadata_remediation.py manual-instructions
  python scripts/zenodo_metadata_remediation.py dry-run
  python scripts/zenodo_metadata_remediation.py apply --record-id 20405526
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import textwrap
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = ROOT / "data" / "zenodo" / "deposit_metadata.json"
DOCS_DIR = ROOT / "docs" / "zenodo" / "deposits"
ZENODO_API = "https://zenodo.org/api"
ERRATA_TITLE_RE = re.compile(
    r"^\s*\[(?:claim\s+withdrawn|superseded|withdrawn|errata)[^\]]*\]\s*",
    re.IGNORECASE,
)


def load_inventory() -> dict[str, Any]:
    with METADATA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def http_json(url: str, method: str = "GET", payload: dict | None = None, token: str | None = None) -> dict:
    data = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {url} failed ({exc.code}): {detail}") from exc


def fetch_record(record_id: int) -> dict[str, Any]:
    return http_json(f"{ZENODO_API}/records/{record_id}")


def has_errata_banner(title: str) -> bool:
    lowered = title.lower()
    return bool(ERRATA_TITLE_RE.match(title)) or (
        "see errata" in lowered and title.strip().startswith("[")
    )


def strip_errata_banner(title: str) -> str:
    return ERRATA_TITLE_RE.sub("", title).strip()


def build_errata_description_block(deposit: dict[str, Any], inventory: dict[str, Any]) -> str:
    status_url = inventory.get("status_index_url", "")
    withdrawn = deposit.get("claims_withdrawn") or []
    superseded_by = deposit.get("superseded_by")
    disposition = deposit.get("disposition", "")

    lines = [
        "<h3>Correction notice (August 2026)</h3>",
        "<p>This deposit is kept as <strong>dated archive</strong>. "
        "The title above is the original scholarly title without editorial banners.</p>",
    ]
    if disposition == "PARK_ARCHIVE":
        lines.append(
            "<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>"
        )
    if withdrawn:
        items = "".join(f"<li>{item}</li>" for item in withdrawn)
        lines.append(f"<p><strong>Withdrawn claims:</strong></p><ul>{items}</ul>")
    if superseded_by:
        lines.append(
            f"<p><strong>Corrected public note:</strong> "
            f"<a href=\"https://doi.org/{superseded_by.replace('10.5281/', '')}\">{superseded_by}</a></p>"
        )
    if status_url:
        lines.append(
            f"<p>See the author status index: "
            f"<a href=\"{status_url}\">{inventory.get('status_index_doi', status_url)}</a></p>"
        )
    lines.append(
        "<p><em>Credit for this DOI:</em> timestamp / history of work. "
        "Not current submit text unless listed in the KEEP set on the status index.</p>"
    )
    return "\n".join(lines)


def merge_description(existing: str, errata_block: str) -> str:
    marker = "Correction notice (August 2026)"
    if marker in existing:
        base = existing.split("<h3>Correction notice", 1)[0].rstrip()
    else:
        base = existing.rstrip()
    if base:
        return f"{base}\n<hr/>\n{errata_block}"
    return errata_block


def audit_deposit(deposit: dict[str, Any], live: dict[str, Any] | None) -> dict[str, Any]:
    record_id = deposit.get("record_id")
    expected_clean = deposit.get("clean_title") or ""
    result = {
        "slug": deposit.get("slug"),
        "record_id": record_id,
        "doi": deposit.get("doi"),
        "disposition": deposit.get("disposition"),
        "expected_clean_title": expected_clean,
        "live_title": None,
        "errata_in_title_live": None,
        "needs_title_fix": False,
        "needs_description_errata": False,
        "status": "skipped",
        "notes": deposit.get("notes", ""),
    }
    if record_id is None:
        result["status"] = "repo_only"
        return result
    if live is None:
        result["status"] = "fetch_failed"
        return result

    meta = live.get("metadata", {})
    live_title = meta.get("title", "")
    result["live_title"] = live_title
    result["errata_in_title_live"] = has_errata_banner(live_title)
    result["needs_title_fix"] = result["errata_in_title_live"] or live_title != expected_clean
    desc = meta.get("description") or ""
    result["needs_description_errata"] = "Correction notice (August 2026)" not in desc
    if deposit.get("disposition") == "PARK_ARCHIVE":
        result["needs_description_errata"] = True
    if result["needs_title_fix"] or (
        deposit.get("disposition") == "PARK_ARCHIVE" and result["needs_description_errata"]
    ):
        result["status"] = "needs_fix"
    else:
        result["status"] = "ok"
    return result


def run_audit(inventory: dict[str, Any]) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for deposit in inventory.get("deposits", []):
        record_id = deposit.get("record_id")
        live = fetch_record(record_id) if record_id else None
        results.append(audit_deposit(deposit, live))
    return results


def print_audit_table(results: list[dict[str, Any]]) -> None:
    print("Zenodo metadata remediation audit")
    print("=" * 72)
    for row in results:
        if row["status"] == "repo_only":
            print(f"[REPO ONLY] {row['slug']}")
            continue
        flag = "FIX" if row["status"] == "needs_fix" else "OK"
        errata = row.get("errata_in_title_live")
        print(f"[{flag}] {row['record_id']} {row['doi']}")
        print(f"  disposition: {row['disposition']}")
        if row.get("live_title"):
            print(f"  live title:  {row['live_title'][:100]}")
        if errata:
            print("  *** ERRATA BANNER IN TITLE ***")
        if row.get("expected_clean_title"):
            print(f"  clean title: {row['expected_clean_title'][:100]}")
        print()


def build_manual_instructions(inventory: dict[str, Any], deposit: dict[str, Any]) -> str:
    record_id = deposit.get("record_id")
    doi = deposit.get("doi")
    clean_title = deposit.get("clean_title", "")
    errata_block = build_errata_description_block(deposit, inventory)
    lines = [
        f"Record {record_id} — {doi}",
        f"Disposition: {deposit.get('disposition')}",
        "",
        "1. Open https://doi.org/" + (doi or ""),
        "2. Click **New version** (metadata-only new version is fine).",
        "3. Title — paste exactly:",
        f"   {clean_title}",
        "4. Description — keep any honest original abstract at the top, then append:",
        textwrap.indent(errata_block, "   "),
        "5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.",
        "6. Publish version.",
        "",
    ]
    return "\n".join(lines)


def print_manual_instructions(inventory: dict[str, Any], only_needing_fix: bool = True) -> None:
    for deposit in inventory.get("deposits", []):
        if deposit.get("record_id") is None:
            continue
        if only_needing_fix:
            live = fetch_record(deposit["record_id"])
            audited = audit_deposit(deposit, live)
            if audited["status"] != "needs_fix":
                continue
        print(build_manual_instructions(inventory, deposit))
        print("-" * 72)


def create_new_version_deposit(record_id: int, token: str) -> int:
    payload = http_json(f"{ZENODO_API}/records/{record_id}", token=token)
    deposition_id = payload.get("metadata", {}).get("deposition_id") or payload.get("id")
    # Published records: create new version from latest deposition link when present.
    links = payload.get("links", {})
    new_version_url = links.get("newversion")
    if not new_version_url:
        raise RuntimeError(f"Record {record_id} has no newversion link; cannot auto-apply.")
    new_payload = http_json(new_version_url, method="POST", token=token)
    return int(new_payload["id"])


def apply_metadata_fix(deposit: dict[str, Any], inventory: dict[str, Any], token: str, dry_run: bool) -> dict[str, Any]:
    record_id = deposit["record_id"]
    live = fetch_record(record_id)
    meta = live.get("metadata", {})
    clean_title = deposit["clean_title"]
    errata_block = build_errata_description_block(deposit, inventory)
    new_description = merge_description(meta.get("description") or "", errata_block)
    update_payload = {
        "metadata": {
            "title": clean_title,
            "description": new_description,
        }
    }
    if dry_run:
        return {
            "record_id": record_id,
            "dry_run": True,
            "title": clean_title,
            "description_preview": new_description[:500],
        }

    deposition_id = create_new_version_deposit(record_id, token)
    http_json(
        f"{ZENODO_API}/deposit/depositions/{deposition_id}",
        method="PUT",
        payload=update_payload,
        token=token,
    )
    publish_url = f"{ZENODO_API}/deposit/depositions/{deposition_id}/actions/publish"
    published = http_json(publish_url, method="POST", token=token)
    return {
        "record_id": record_id,
        "published_id": published.get("id"),
        "doi": published.get("doi"),
        "title": published.get("metadata", {}).get("title"),
    }


def write_deposit_docs(inventory: dict[str, Any]) -> None:
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    for deposit in inventory.get("deposits", []):
        slug = deposit.get("slug")
        if not slug:
            continue
        path = DOCS_DIR / f"{slug}.md"
        errata_block = build_errata_description_block(deposit, inventory)
        content = textwrap.dedent(
            f"""\
            # Zenodo remediation — `{slug}`

            | Field | Value |
            | --- | --- |
            | Record ID | `{deposit.get('record_id')}` |
            | DOI | `{deposit.get('doi')}` |
            | Disposition | **{deposit.get('disposition')}** |
            | Alias | {deposit.get('alias')} |

            ## Clean title (use this — no banners)

            {deposit.get('clean_title')}

            ## Current live title (audit 2026-08-23)

            {deposit.get('current_title_live') or '—'}

            ## Errata in title?

            `{deposit.get('errata_in_title')}` (expected fix if live still has a banner)

            ## Withdrawn claims

            """
        )
        for claim in deposit.get("claims_withdrawn") or []:
            content += f"- {claim}\n"
        if deposit.get("superseded_by"):
            content += f"\n**Superseded by:** `{deposit['superseded_by']}`\n"
        if deposit.get("supersedes_record_ids"):
            content += "\n**This record supersedes:** "
            content += ", ".join(str(x) for x in deposit["supersedes_record_ids"]) + "\n"
        content += "\n## Description block (paste under original abstract)\n\n"
        content += errata_block + "\n"
        content += f"\n## Notes\n\n{deposit.get('notes', '')}\n"
        path.write_text(content, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Zenodo metadata remediation helper")
    parser.add_argument(
        "command",
        choices=["audit", "manual-instructions", "dry-run", "apply", "write-docs"],
        help="Operation to run",
    )
    parser.add_argument("--record-id", type=int, help="Limit apply/dry-run to one record id")
    parser.add_argument("--all", action="store_true", help="Include OK records in manual-instructions")
    args = parser.parse_args(argv)

    inventory = load_inventory()

    if args.command == "write-docs":
        write_deposit_docs(inventory)
        print(f"Wrote deposit remediation files under {DOCS_DIR}")
        return 0

    if args.command == "audit":
        results = run_audit(inventory)
        print_audit_table(results)
        needs = sum(1 for r in results if r["status"] == "needs_fix")
        errata = sum(1 for r in results if r.get("errata_in_title_live"))
        print(f"Summary: {needs} need fix, {errata} with errata banner in live title")
        return 0

    if args.command == "manual-instructions":
        print_manual_instructions(inventory, only_needing_fix=not args.all)
        return 0

    token = os.environ.get("ZENODO_ACCESS_TOKEN") or os.environ.get("ZENODO_TOKEN")
    targets = [
        d for d in inventory["deposits"]
        if d.get("record_id") is not None
        and (args.record_id is None or d["record_id"] == args.record_id)
    ]
    if not targets:
        print("No matching deposits.", file=sys.stderr)
        return 1

    dry_run = args.command == "dry-run"
    if args.command == "apply" and not token:
        print(
            "ZENODO_ACCESS_TOKEN not set. Cannot apply via API.\n"
            "Run: python scripts/zenodo_metadata_remediation.py manual-instructions",
            file=sys.stderr,
        )
        return 2

    for deposit in targets:
        if deposit.get("disposition") == "KEEP" and deposit.get("errata_in_title"):
            continue
        if deposit.get("disposition") == "KEEP" and not deposit.get("errata_in_title"):
            if args.record_id is None and args.command != "dry-run":
                continue
        result = apply_metadata_fix(deposit, inventory, token or "", dry_run=dry_run)
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
