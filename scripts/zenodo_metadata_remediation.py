#!/usr/bin/env python3
"""Zenodo deposit remediation for Jonathan R. Simons records.

Enforces the presentation rule:
  - PUBLIC TOP: clean scholarly title + honest abstract/PDF
  - UNDERNEATH: correction/errata notice in description (never in title)

Also packages / optionally uploads the PhiRenorm June 30 file fix
(record 21071991: \\dot H^{2.6} → \\dot H^{1.3}).

Usage:
  python3 scripts/zenodo_metadata_remediation.py audit
  python3 scripts/zenodo_metadata_remediation.py audit --json
  python3 scripts/zenodo_metadata_remediation.py manual-instructions
  python3 scripts/zenodo_metadata_remediation.py dry-run
  python3 scripts/zenodo_metadata_remediation.py apply
  python3 scripts/zenodo_metadata_remediation.py write-docs
  python3 scripts/zenodo_metadata_remediation.py package-files
  python3 scripts/zenodo_metadata_remediation.py token-help
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import textwrap
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
METADATA_PATH = ROOT / "data" / "zenodo" / "deposit_metadata.json"
DOCS_DIR = ROOT / "docs" / "zenodo" / "deposits"
UPLOAD_PACKS = ROOT / "data" / "zenodo" / "upload_packs"
MANUAL_OUT = ROOT / "docs" / "zenodo" / "MANUAL-INSTRUCTIONS.md"
ZENODO_API = "https://zenodo.org/api"
ERRATA_TITLE_RE = re.compile(
    r"^\s*\[(?:claim\s+withdrawn|superseded|withdrawn|errata)[^\]]*\]\s*",
    re.IGNORECASE,
)
CORRECTION_MARKER = "Correction notice (August 2026)"
FILE_FIX_MARKER = "File correction notice (September 2026)"


def load_inventory() -> dict[str, Any]:
    with METADATA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def get_token() -> str | None:
    return os.environ.get("ZENODO_ACCESS_TOKEN") or os.environ.get("ZENODO_TOKEN")


def http_json(
    url: str,
    method: str = "GET",
    payload: dict | None = None,
    token: str | None = None,
    data: bytes | None = None,
    content_type: str | None = None,
) -> dict:
    body = data
    headers = {"Accept": "application/json", "User-Agent": "ShipIt-ZenodoRemediation/1.1"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if content_type:
        headers["Content-Type"] = content_type
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
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
    cleaned = ERRATA_TITLE_RE.sub("", title).strip()
    if cleaned.endswith('"') and cleaned.count('"') == 1:
        cleaned = cleaned[:-1].rstrip()
    return cleaned


def build_errata_description_block(deposit: dict[str, Any], inventory: dict[str, Any]) -> str:
    status_url = inventory.get("status_index_url", "")
    withdrawn = deposit.get("claims_withdrawn") or []
    superseded_by = deposit.get("superseded_by")
    disposition = deposit.get("disposition", "")

    if disposition == "KEEP":
        lines = [
            f"<h3>{FILE_FIX_MARKER if deposit.get('needs_file_fix') or (deposit.get('file_fix') or {}).get('needed') else CORRECTION_MARKER}</h3>",
            "<p>This deposit remains in the <strong>KEEP</strong> set. "
            "The title is a scholarly title without editorial banners.</p>",
        ]
        if deposit.get("needs_file_fix") or (deposit.get("file_fix") or {}).get("needed"):
            lines.append(
                "<p><strong>File correction:</strong> energy / dual norms previously labeled "
                "<code>\\dot H^{2.6}</code> are relabeled <code>\\dot H^{1.3}</code> "
                "(22 Aug 2026 audit). The open barrier "
                "<code>||u^r/r||_∞</code> / <code>op:gronwall</code> is unchanged. "
                "This is a <em>conditional</em> reduction — not a global regularity proof, "
                "not Clay Statement (B).</p>"
            )
    elif disposition == "REVIEW":
        lines = [
            f"<h3>{CORRECTION_MARKER}</h3>",
            "<p>This deposit is <strong>not</strong> in the current KEEP set. "
            "Treat it as exploratory / under review. The title has no editorial banners.</p>",
        ]
    else:
        lines = [
            f"<h3>{CORRECTION_MARKER}</h3>",
            "<p>This deposit is kept as <strong>dated archive</strong>. "
            "The title above is the original scholarly title without editorial banners.</p>",
            "<p><strong>Do not cite</strong> load-bearing claims in the original files as proved results.</p>",
        ]

    if withdrawn:
        items = "".join(f"<li>{item}</li>" for item in withdrawn)
        lines.append(f"<p><strong>Withdrawn / not claimed:</strong></p><ul>{items}</ul>")
    if superseded_by:
        lines.append(
            f"<p><strong>Corrected public note:</strong> "
            f'<a href="https://doi.org/{superseded_by}">{superseded_by}</a></p>'
        )
    if status_url:
        lines.append(
            f"<p>See the author status index: "
            f'<a href="{status_url}">{inventory.get("status_index_doi", status_url)}</a></p>'
        )
    lines.append(
        "<p><em>Credit for this DOI:</em> timestamp / history of work. "
        "Not current submit text unless listed in the KEEP set on the status index.</p>"
    )
    return "\n".join(lines)


def merge_description(existing: str, errata_block: str) -> str:
    markers = (CORRECTION_MARKER, FILE_FIX_MARKER)
    base = existing
    for marker in markers:
        if marker in base:
            # Drop prior auto-inserted block(s)
            parts = re.split(r"<h3>(?:Correction notice|File correction notice)[^<]*</h3>", base, maxsplit=1)
            base = parts[0]
            # Also strip a leading <hr/> we may have inserted
            break
    base = re.sub(r"(?:<hr\s*/?>\s*)+$", "", base.rstrip()).rstrip()
    if base:
        return f"{base}\n<hr/>\n{errata_block}"
    return errata_block


def audit_deposit(deposit: dict[str, Any], live: dict[str, Any] | None) -> dict[str, Any]:
    record_id = deposit.get("record_id")
    expected_clean = deposit.get("clean_title") or ""
    result: dict[str, Any] = {
        "slug": deposit.get("slug"),
        "record_id": record_id,
        "doi": deposit.get("doi"),
        "disposition": deposit.get("disposition"),
        "expected_clean_title": expected_clean,
        "live_title": None,
        "errata_in_title_live": None,
        "needs_title_fix": False,
        "needs_description_errata": False,
        "needs_file_fix": bool(
            deposit.get("needs_file_fix") or (deposit.get("file_fix") or {}).get("needed")
        ),
        "files_live": [],
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
    title_mismatch = strip_errata_banner(live_title) != expected_clean and live_title != expected_clean
    result["needs_title_fix"] = bool(result["errata_in_title_live"] or title_mismatch)
    desc = meta.get("description") or ""
    has_notice = CORRECTION_MARKER in desc or FILE_FIX_MARKER in desc
    result["needs_description_errata"] = (
        deposit.get("disposition") in ("PARK_ARCHIVE", "REVIEW") and not has_notice
    ) or (result["needs_file_fix"] and FILE_FIX_MARKER not in desc and CORRECTION_MARKER not in desc)
    result["files_live"] = [f.get("key") for f in (live.get("files") or []) if f.get("key")]

    if result["needs_title_fix"] or result["needs_description_errata"] or result["needs_file_fix"]:
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
    print("Zenodo deposit remediation audit")
    print("=" * 72)
    for row in results:
        if row["status"] == "repo_only":
            print(f"[REPO ONLY] {row['slug']}")
            continue
        flag = "FIX" if row["status"] == "needs_fix" else "OK"
        print(f"[{flag}] {row['record_id']} {row['doi']}")
        print(f"  disposition: {row['disposition']}")
        if row.get("live_title"):
            print(f"  live title:  {row['live_title'][:110]}")
        if row.get("errata_in_title_live"):
            print("  *** ERRATA BANNER IN TITLE ***")
        issues = []
        if row.get("needs_title_fix"):
            issues.append("title")
        if row.get("needs_description_errata"):
            issues.append("description-errata")
        if row.get("needs_file_fix"):
            issues.append("file-pack")
        if issues:
            print(f"  needs: {', '.join(issues)}")
        print()


def build_manual_instructions(inventory: dict[str, Any], deposit: dict[str, Any]) -> str:
    record_id = deposit.get("record_id")
    doi = deposit.get("doi")
    clean_title = deposit.get("clean_title", "")
    errata_block = build_errata_description_block(deposit, inventory)
    lines = [
        f"## Record {record_id} — `{doi}`",
        "",
        f"- Disposition: **{deposit.get('disposition')}**",
        f"- Alias: {deposit.get('alias')}",
        "",
        "1. Open https://doi.org/" + (doi or ""),
        "2. Click **New version**.",
        "3. **Title** — paste exactly (no banners):",
        "",
        f"   `{clean_title}`",
        "",
        "4. **Description** — keep any honest original abstract at the top, then append:",
        "",
        "```html",
        errata_block,
        "```",
        "",
    ]
    file_fix = deposit.get("file_fix") or {}
    if file_fix.get("needed"):
        pack = file_fix.get("upload_pack", "")
        replace = ", ".join(file_fix.get("replace_files") or [])
        lines.extend(
            [
                "5. **Files** — delete the old TeX/PDF on the new version draft, then upload from:",
                f"   `{pack}/`",
                f"   Replace: {replace}",
                "6. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.",
                "7. Publish version.",
                "",
            ]
        )
    else:
        lines.extend(
            [
                "5. Do **not** put ERRATA / WITHDRAWN / Superseded banners in the title.",
                "6. Publish version.",
                "",
            ]
        )
    return "\n".join(lines)


def write_manual_instructions_file(inventory: dict[str, Any], results: list[dict[str, Any]]) -> Path:
    needing = {r["record_id"] for r in results if r["status"] == "needs_fix"}
    parts = [
        "# Zenodo remediation — manual instructions",
        "",
        "Generated for deposits that still need a live fix.",
        "Presentation rule: clean title on top; correction notice only in description.",
        "",
        "## If you have an API token",
        "",
        "```bash",
        "export ZENODO_ACCESS_TOKEN='<token from zenodo.org/account/settings/applications/>'",
        "python3 scripts/zenodo_metadata_remediation.py apply",
        "# optional single record:",
        "python3 scripts/zenodo_metadata_remediation.py apply --record-id 21071991",
        "```",
        "",
        "Token scopes needed: `deposit:write` + `deposit:actions`.",
        "",
        "## Copy-paste per record",
        "",
    ]
    for deposit in inventory.get("deposits", []):
        rid = deposit.get("record_id")
        if rid is None or rid not in needing:
            continue
        parts.append(build_manual_instructions(inventory, deposit))
        parts.append("---")
        parts.append("")
    MANUAL_OUT.parent.mkdir(parents=True, exist_ok=True)
    MANUAL_OUT.write_text("\n".join(parts), encoding="utf-8")
    return MANUAL_OUT


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
    links = payload.get("links", {})
    new_version_url = links.get("newversion")
    if not new_version_url:
        # Fall back to deposit API latest concept
        raise RuntimeError(
            f"Record {record_id} has no public newversion link; "
            "open the deposit UI or use deposit API with owner token."
        )
    new_payload = http_json(new_version_url, method="POST", token=token)
    new_id = new_payload.get("id") or (new_payload.get("links", {}).get("latest_draft") or "").rstrip("/").split("/")[-1]
    return int(new_id)


def upload_file_to_deposition(deposition_id: int, path: Path, token: str) -> None:
    # Zenodo deposit files API
    meta = http_json(
        f"{ZENODO_API}/deposit/depositions/{deposition_id}",
        token=token,
    )
    bucket = meta.get("links", {}).get("bucket")
    if not bucket:
        raise RuntimeError(f"Deposition {deposition_id} has no bucket link")
    data = path.read_bytes()
    http_json(
        f"{bucket}/{path.name}",
        method="PUT",
        token=token,
        data=data,
        content_type="application/octet-stream",
    )


def apply_metadata_fix(
    deposit: dict[str, Any],
    inventory: dict[str, Any],
    token: str,
    dry_run: bool,
    upload_files: bool = True,
) -> dict[str, Any]:
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
    file_fix = deposit.get("file_fix") or {}
    result: dict[str, Any] = {
        "record_id": record_id,
        "title": clean_title,
        "will_upload_files": bool(file_fix.get("needed") and upload_files),
        "description_preview": new_description[:500],
    }
    if dry_run:
        result["dry_run"] = True
        return result

    deposition_id = create_new_version_deposit(record_id, token)
    http_json(
        f"{ZENODO_API}/deposit/depositions/{deposition_id}",
        method="PUT",
        payload=update_payload,
        token=token,
    )
    if file_fix.get("needed") and upload_files:
        pack = ROOT / file_fix["upload_pack"]
        for name in file_fix.get("replace_files") or []:
            upload_file_to_deposition(deposition_id, pack / name, token)
    publish_url = f"{ZENODO_API}/deposit/depositions/{deposition_id}/actions/publish"
    published = http_json(publish_url, method="POST", token=token)
    result.update(
        {
            "published_id": published.get("id"),
            "doi": published.get("doi") or published.get("metadata", {}).get("doi"),
            "title_published": published.get("metadata", {}).get("title"),
        }
    )
    return result


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
            | Needs description errata | `{deposit.get('needs_description_errata')}` |
            | Needs title fix | `{deposit.get('needs_title_fix')}` |
            | Needs file fix | `{deposit.get('needs_file_fix') or (deposit.get('file_fix') or {}).get('needed')}` |

            ## Clean title (use this — no banners)

            {deposit.get('clean_title')}

            ## Current live title

            {deposit.get('current_title_live') or '—'}

            ## Errata banner in live title?

            `{deposit.get('errata_in_title')}`

            ## Withdrawn / not claimed

            """
        )
        claims = deposit.get("claims_withdrawn") or []
        if claims:
            for claim in claims:
                content += f"- {claim}\n"
        else:
            content += "- _(none listed)_\n"
        if deposit.get("superseded_by"):
            content += f"\n**Superseded by:** `{deposit['superseded_by']}`\n"
        if deposit.get("supersedes_record_ids"):
            content += "\n**This record supersedes:** "
            content += ", ".join(str(x) for x in deposit["supersedes_record_ids"]) + "\n"
        if deposit.get("file_fix"):
            content += "\n## File fix\n\n"
            content += f"```json\n{json.dumps(deposit['file_fix'], indent=2)}\n```\n"
        content += "\n## Description block (paste under original abstract)\n\n"
        content += errata_block + "\n"
        content += f"\n## Notes\n\n{deposit.get('notes', '')}\n"
        path.write_text(content, encoding="utf-8")


def package_files() -> dict[str, Any]:
    """Ensure 21071991 upload pack matches corrected swirl SoT."""
    src_tex = ROOT / "docs/papers/swirl/Simons_PhiRenorm_Swirl_2026-06-30.tex"
    src_pdf = ROOT / "docs/papers/swirl/Simons_PhiRenorm_Swirl_2026-06-30.pdf"
    dest = UPLOAD_PACKS / "21071991"
    dest.mkdir(parents=True, exist_ok=True)
    if not src_tex.exists() or not src_pdf.exists():
        raise FileNotFoundError("Corrected PhiRenorm TeX/PDF missing under docs/papers/swirl/")
    tex_text = src_tex.read_text(encoding="utf-8")
    if r"\dot H^{2.6}" in tex_text:
        raise RuntimeError("SoT TeX still contains \\dot H^{2.6}; refuse to package")
    if r"\dot H^{1.3}" not in tex_text:
        raise RuntimeError("SoT TeX missing \\dot H^{1.3} labels")
    shutil.copy2(src_tex, dest / src_tex.name)
    shutil.copy2(src_pdf, dest / src_pdf.name)
    # Keep phi-renorm mirror in sync
    phi = ROOT / "docs/papers/phi-renorm/Simons_PhiRenorm_Swirl_2026-06-30.tex"
    phi.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_tex, phi)
    readme = dest / "README.md"
    readme.write_text(
        textwrap.dedent(
            r"""
            # Upload pack — Zenodo record 21071991

            **Disposition:** KEEP conditional (open `||u^r/r||_∞` / `op:gronwall`).

            ## Fix

            Relabel energy / dual norms `\dot H^{2.6}` → `\dot H^{1.3}` (22 Aug 2026 audit).
            Do **not** claim global regularity or Clay Statement (B).

            ## Files

            | File | Role |
            | --- | --- |
            | `Simons_PhiRenorm_Swirl_2026-06-30.tex` | Corrected SoT TeX |
            | `Simons_PhiRenorm_Swirl_2026-06-30.pdf` | Recompiled PDF with `\dot H^{1.3}` |

            ## Apply

            ```bash
            export ZENODO_ACCESS_TOKEN=...
            python3 scripts/zenodo_metadata_remediation.py apply --record-id 21071991
            ```

            Or manually: New version on https://doi.org/10.5281/zenodo.21071991 →
            replace both files → append description file-correction notice → publish.
            """
        ).lstrip(),
        encoding="utf-8",
    )
    return {
        "pack": str(dest.relative_to(ROOT)),
        "tex_bytes": (dest / src_tex.name).stat().st_size,
        "pdf_bytes": (dest / src_pdf.name).stat().st_size,
        "hdot_26_in_tex": False,
        "hdot_13_in_tex": True,
    }


def token_help() -> str:
    return textwrap.dedent(
        """\
        Jonathan — export a Zenodo token and apply live fixes:

          # 1. Create a personal access token at:
          #    https://zenodo.org/account/settings/applications/
          #    Scopes: deposit:write, deposit:actions

          export ZENODO_ACCESS_TOKEN='<paste-token-here>'

          # 2. From the repo root:
          python3 scripts/zenodo_metadata_remediation.py audit
          python3 scripts/zenodo_metadata_remediation.py apply

          # Or one record (PhiRenorm file fix):
          python3 scripts/zenodo_metadata_remediation.py apply --record-id 21071991

        Without a token, use:
          python3 scripts/zenodo_metadata_remediation.py manual-instructions
          # or open docs/zenodo/MANUAL-INSTRUCTIONS.md
        """
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Zenodo deposit remediation helper")
    parser.add_argument(
        "command",
        choices=[
            "audit",
            "manual-instructions",
            "dry-run",
            "apply",
            "write-docs",
            "package-files",
            "token-help",
        ],
        help="Operation to run",
    )
    parser.add_argument("--record-id", type=int, help="Limit apply/dry-run/audit to one record id")
    parser.add_argument("--all", action="store_true", help="Include OK records in manual-instructions")
    parser.add_argument("--json", action="store_true", help="Emit audit as JSON")
    parser.add_argument("--no-files", action="store_true", help="Skip file upload on apply")
    args = parser.parse_args(argv)

    if args.command == "token-help":
        print(token_help())
        return 0

    if args.command == "package-files":
        info = package_files()
        print(json.dumps(info, indent=2))
        return 0

    inventory = load_inventory()

    if args.command == "write-docs":
        write_deposit_docs(inventory)
        print(f"Wrote deposit remediation files under {DOCS_DIR}")
        return 0

    if args.command == "audit":
        results = run_audit(inventory)
        if args.record_id is not None:
            results = [r for r in results if r.get("record_id") == args.record_id]
        needs = sum(1 for r in results if r["status"] == "needs_fix")
        errata = sum(1 for r in results if r.get("errata_in_title_live"))
        files = sum(1 for r in results if r.get("needs_file_fix"))
        desc = sum(1 for r in results if r.get("needs_description_errata"))
        summary = {
            "needs_fix": needs,
            "title_banners": errata,
            "description_errata": desc,
            "file_packs": files,
        }
        if args.json:
            print(json.dumps({"summary": summary, "results": results}, indent=2))
        else:
            print_audit_table(results)
            print(
                f"Summary: {needs} need fix | {errata} title banners | "
                f"{desc} description errata | {files} file packs"
            )
        out = write_manual_instructions_file(inventory, results)
        if not args.json:
            print(f"Wrote {out}")
        return 0

    if args.command == "manual-instructions":
        print_manual_instructions(inventory, only_needing_fix=not args.all)
        results = run_audit(inventory)
        write_manual_instructions_file(inventory, results)
        print(f"(Also wrote {MANUAL_OUT})")
        return 0

    token = get_token()
    targets = [
        d
        for d in inventory["deposits"]
        if d.get("record_id") is not None
        and (args.record_id is None or d["record_id"] == args.record_id)
    ]
    if not targets:
        print("No matching deposits.", file=sys.stderr)
        return 1

    dry_run = args.command == "dry-run"
    if args.command == "apply" and not token:
        print(token_help(), file=sys.stderr)
        print(
            "ZENODO_ACCESS_TOKEN / ZENODO_TOKEN not set — cannot apply via API.\n"
            "In-repo pack is ready; run manual-instructions or export a token.",
            file=sys.stderr,
        )
        return 2

    # Only apply records that need work unless --record-id forced
    applied = []
    for deposit in targets:
        live = fetch_record(deposit["record_id"])
        audited = audit_deposit(deposit, live)
        if audited["status"] != "needs_fix" and args.record_id is None:
            continue
        result = apply_metadata_fix(
            deposit,
            inventory,
            token or "",
            dry_run=dry_run,
            upload_files=not args.no_files,
        )
        applied.append(result)
        print(json.dumps(result, indent=2))

    if not applied:
        print("Nothing to apply (all targeted records already OK).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
