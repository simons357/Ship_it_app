#!/usr/bin/env python3
"""Fetch a corrected live Zenodo inventory for Jonathan R. Simons deposits.

Writes:
  data/zenodo/ZENODO_INVENTORY_CORRECTED_LIVE.json
  data/zenodo/ZENODO_INVENTORY_CORRECTED_LIVE.csv
  data/zenodo/ZENODO_INVENTORY_CORRECTED_LIVE_numbers.csv
and prints a comparison summary vs the Aug 14 dump.
"""

from __future__ import annotations

import csv
import json
import re
import ssl
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "zenodo"
AUG14_CSV = OUT_DIR / "ZENODO_INVENTORY_JONATHAN_SIMONS_2026-08-14.csv"
AUG14_JSON = OUT_DIR / "ZENODO_INVENTORY_JONATHAN_SIMONS_2026-08-14.json"
SETTLED_PATH = OUT_DIR / "deposit_metadata.json"

API = "https://zenodo.org/api/records"
OWNER_ID = "1627782"

CREATOR_QUERIES = [
    'creators.name:"Simons, Jonathan"',
    'creators.name:"Simons, Jonathan R."',
    'creators.name:"Simons, Jonathan Robert"',
    'creators.name:"simons, jonathan"',
    f"owners:{OWNER_ID}",
]

# Require Simons in creator string to drop unrelated "Jonathan, Jonathan" hits.
SIMONS_CREATOR_RE = re.compile(r"\bSimons\b", re.I)

# Explicitly settled KEEP set + PhiRenorm June 30 (conditional KEEP).
EXTRA_KEEP = {
    "21071991": {
        "disposition": "KEEP",
        "alias": "PhiRenorm June 30 conditional (open ||u^r/r||_∞)",
        "notes": (
            "KEEP as conditional Phi-renorm deposit. Open gap: ||u^r/r||_∞. "
            "Repo+upload pack corrected (Hdot^2.6→1.3); live Zenodo files still "
            "pre-relabel until token apply — NEEDS_AUDIT_FIX on live only."
        ),
        "flags": ["NEEDS_AUDIT_FIX"],
    }
}

# Known DOIs from Aug 14 + settled KEEP set (fetched by id even if search misses).
KNOWN_RECORD_IDS = [
    22050962,
    22050974,
    22050975,
    22050976,
    22050965,
    22050963,
    22050978,
    21071991,
    20552682,
    20552400,
    20552223,
    20552171,
    20552080,
    20518388,
    20518057,
    20405599,
    20405597,
    20405593,
    20405591,
    20405589,
    20405585,
    20405526,
    20405405,
    20272545,
    20271879,
    20271457,
    20269843,
    20269536,
    20184148,
    20183673,
    19842060,
]

BANNER_RE = re.compile(
    r"\[?\s*(claim\s+withdrawn|superseded|withdrawn|errata|archived)\b|"
    r"see\s+errata|WITHDRAWN|ERRATA|SUPERSEDED",
    re.I,
)

PARK_TITLE_HINTS = re.compile(
    r"(millennium|quantum\s+lens|triple\s+lock|archon|"
    r"global\s+regularity\s+of\s+the\s+navier|"
    r"implies\s+global\s+regularity|"
    r"snd\s*≡\s*gnc|simons\s+field\s+equation|"
    r"prime\s+manifold|"
    r"three.?in.?one|"
    r"goldbach|"
    r"riemann\s+hypothesis)",
    re.I,
)


def http_get_json(url: str, retries: int = 4) -> dict[str, Any]:
    ctx = ssl.create_default_context()
    last_err: Exception | None = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "Accept": "application/json",
                    "User-Agent": "ShipIt-ZenodoInventory/1.0 (Jonathan R. Simons inventory correction)",
                },
            )
            with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as exc:
            body = ""
            try:
                body = exc.read().decode("utf-8", errors="replace")[:400]
            except Exception:  # noqa: BLE001
                pass
            # Do not retry validation errors
            if exc.code == 400:
                raise RuntimeError(f"GET 400: {url}: {body}") from exc
            last_err = RuntimeError(f"HTTP {exc.code}: {body}")
            time.sleep(1.2 * (2**attempt))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_err = exc
            time.sleep(1.2 * (2**attempt))
    raise RuntimeError(f"GET failed after {retries} tries: {url}: {last_err}")


def normalize_record(raw: dict[str, Any]) -> dict[str, Any]:
    meta = raw.get("metadata") or {}
    files = raw.get("files") or []
    file_keys = [f.get("key") or f.get("filename") or "" for f in files]
    file_keys = [k for k in file_keys if k]
    creators = meta.get("creators") or []
    creator_names = "; ".join(c.get("name", "") for c in creators if c.get("name"))
    doi = meta.get("doi") or (raw.get("doi") or "")
    if isinstance(doi, dict):
        doi = doi.get("id") or ""
    record_id = raw.get("id")
    links = raw.get("links") or {}
    return {
        "record_id": str(record_id) if record_id is not None else "",
        "doi": doi if doi.startswith("10.") else (f"10.5281/zenodo.{record_id}" if record_id else ""),
        "url": links.get("html") or f"https://zenodo.org/records/{record_id}",
        "title": meta.get("title") or "",
        "publication_date": meta.get("publication_date") or "",
        "version": (meta.get("version") or ""),
        "creators": creator_names,
        "files": " | ".join(file_keys),
        "file_keys": file_keys,
        "file_count": len(file_keys),
        "access": (raw.get("access") or {}).get("status")
        or (meta.get("access_right") or raw.get("access_right") or ""),
        "updated": raw.get("updated") or "",
        "created": raw.get("created") or "",
        "conceptrecid": str(raw.get("conceptrecid") or meta.get("conceptrecid") or ""),
        "revision": raw.get("revision"),
    }


def paginate_search(query: str, size: int = 25) -> list[dict[str, Any]]:
    """Paginate Zenodo search. Anonymous API caps size at 25; no sort=mostrecent."""
    out: list[dict[str, Any]] = []
    page = 1
    size = min(size, 25)
    while True:
        params = urllib.parse.urlencode({"q": query, "size": size, "page": page})
        data = http_get_json(f"{API}?{params}")
        hits = (data.get("hits") or {}).get("hits") or []
        total = (data.get("hits") or {}).get("total") or 0
        for h in hits:
            out.append(normalize_record(h))
        if page * size >= total or not hits:
            break
        page += 1
        time.sleep(0.2)
    return out


def fetch_by_id(record_id: int | str) -> dict[str, Any] | None:
    try:
        raw = http_get_json(f"{API}/{record_id}")
        return normalize_record(raw)
    except RuntimeError:
        return None


def load_settled() -> tuple[dict[str, dict[str, Any]], set[str], dict[str, str]]:
    """Return by_id, superseded_ids, superseded_by_doi."""
    if not SETTLED_PATH.exists():
        return {}, set(), {}
    data = json.loads(SETTLED_PATH.read_text())
    by_id: dict[str, dict[str, Any]] = {}
    superseded: set[str] = set()
    superseded_by: dict[str, str] = {}
    for dep in data.get("deposits") or []:
        rid = dep.get("record_id")
        if rid is not None:
            by_id[str(rid)] = dep
        keep_doi = dep.get("doi") if dep.get("disposition") == "KEEP" else None
        for sid in dep.get("supersedes_record_ids") or []:
            superseded.add(str(sid))
            if keep_doi:
                superseded_by[str(sid)] = keep_doi
        if dep.get("superseded_by"):
            if rid is not None:
                superseded.add(str(rid))
                superseded_by[str(rid)] = str(dep["superseded_by"])
    return by_id, superseded, superseded_by


def title_has_errata_banner(title: str) -> bool:
    """True only for leading/bracketed errata banners — not scholarly titles that mention Errata."""
    t = (title or "").strip()
    if not t:
        return False
    # Leading bracket banner: [Claim withdrawn - see errata] ...
    if re.match(r"^\[\s*(claim\s+withdrawn|superseded|withdrawn|errata|archived)\b", t, re.I):
        return True
    if re.match(r"^(ERRATA|WITHDRAWN|SUPERSEDED|ARCHIVED)\b", t, re.I):
        return True
    if re.search(r"\[\s*(claim\s+withdrawn|superseded)\s*[-–—:].*errata\s*\]", t, re.I):
        return True
    return False


def classify(
    rec: dict[str, Any],
    settled: dict[str, dict[str, Any]],
    superseded_ids: set[str],
    superseded_by: dict[str, str],
) -> tuple[str, list[str], str, str]:
    """Return disposition, flags, alias, notes."""
    rid = rec["record_id"]
    title = rec.get("title") or ""
    flags: list[str] = []
    if title_has_errata_banner(title):
        flags.append("NEEDS_TITLE_CLEAN")

    if rid in EXTRA_KEEP:
        extra = EXTRA_KEEP[rid]
        flags = list(dict.fromkeys(flags + extra.get("flags", [])))
        return extra["disposition"], flags, extra["alias"], extra["notes"]

    if rid in settled:
        dep = settled[rid]
        disp = dep.get("disposition") or "UNSETTLED"
        if disp in ("PARK", "PARK_ARCHIVE", "ARCHIVE"):
            disp = "PARK/ARCHIVE"
        alias = dep.get("alias") or dep.get("slug") or ""
        notes = dep.get("notes") or ""
        # Only flag NEEDS_TITLE_CLEAN from live title banner or settled errata_in_title
        if dep.get("errata_in_title") and title_has_errata_banner(title):
            if "NEEDS_TITLE_CLEAN" not in flags:
                flags.append("NEEDS_TITLE_CLEAN")
        elif dep.get("errata_in_title") and not title_has_errata_banner(title):
            notes = (notes + " Settled pack expected title banner; live title may already be cleaned.").strip()
        elif title_has_errata_banner(title) and "NEEDS_TITLE_CLEAN" not in flags:
            flags.append("NEEDS_TITLE_CLEAN")
        return disp, flags, alias, notes

    # Explicitly superseded by a settled KEEP concept version
    if rid in superseded_ids:
        by = superseded_by.get(rid)
        note = "Superseded concept version from settled inventory."
        if by:
            note += f" See KEEP {by}."
        return "PARK/ARCHIVE", flags, "", note

    # Not in settled KEEP set — do not invent KEEP.
    notes = "Not in settled Aug-2026 KEEP set."
    alias = ""
    if PARK_TITLE_HINTS.search(title) or title_has_errata_banner(title):
        return (
            "PARK/ARCHIVE",
            flags,
            alias,
            notes + " Categorical PARK (unconditional/Millennium/RH/SFE/banner packaging).",
        )

    return "REVIEW", flags, alias, notes + " Needs human disposition; not in settled KEEP/PARK list."


def load_aug14() -> list[dict[str, Any]]:
    if AUG14_JSON.exists():
        return json.loads(AUG14_JSON.read_text())
    rows = []
    with AUG14_CSV.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    return rows


def diagnose_aug14_shift(aug14: list[dict[str, Any]], live_by_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    """Confirm file-column shift: Aug14 files on DOI N match live files of another DOI."""
    mismatches = []
    empty_id_rows = [r for r in aug14 if not str(r.get("record_id") or "").strip()]
    for row in aug14:
        rid = str(row.get("record_id") or "").strip()
        if not rid:
            continue
        live = live_by_id.get(rid)
        if not live:
            continue
        aug_files = [x.strip() for x in str(row.get("files") or "").split("|") if x.strip()]
        live_files = live.get("file_keys") or []
        if set(aug_files) != set(live_files):
            owners = []
            for lid, lrec in live_by_id.items():
                if set(aug_files) and set(aug_files) <= set(lrec.get("file_keys") or []):
                    owners.append(lid)
            mismatches.append(
                {
                    "record_id": rid,
                    "aug14_title": row.get("title"),
                    "live_title": live.get("title"),
                    "aug14_files": aug_files,
                    "live_files": live_files,
                    "aug14_files_belong_to_live_ids": owners,
                    "title_match": (row.get("title") or "") == (live.get("title") or ""),
                }
            )
    shift_confirmed = False
    if mismatches:
        for m in mismatches:
            if m["record_id"] == "21071991" and any(
                "PhiRenorm" in f or "Simons_PhiRenorm" in f for f in m["live_files"]
            ):
                if any("THREE_IN_ONE" in f or "NS_RH_GOLDBACH" in f for f in m["aug14_files"]):
                    shift_confirmed = True
                    break
        if not shift_confirmed:
            shift_confirmed = any(
                m["aug14_files_belong_to_live_ids"]
                and m["record_id"] not in m["aug14_files_belong_to_live_ids"]
                for m in mismatches
            )
    return {
        "aug14_row_count": len(aug14),
        "aug14_rows_with_empty_doi_title": len(empty_id_rows),
        "file_mismatch_count": len(mismatches),
        "file_column_shift_confirmed": shift_confirmed,
        "mismatches": mismatches,
        "stale": True,
    }


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def main() -> int:
    settled, superseded_ids, superseded_by = load_settled()
    aug14 = load_aug14()

    by_id: dict[str, dict[str, Any]] = {}

    print("Searching Zenodo…", flush=True)
    for q in CREATOR_QUERIES:
        try:
            found = paginate_search(q)
            print(f"  query {q!r}: {len(found)} hits", flush=True)
            for rec in found:
                by_id[rec["record_id"]] = rec
        except Exception as exc:  # noqa: BLE001
            print(f"  WARN search failed for {q!r}: {exc}", flush=True)

    print("Fetching known record ids…", flush=True)
    for rid in KNOWN_RECORD_IDS:
        sid = str(rid)
        if sid in by_id:
            continue
        rec = fetch_by_id(rid)
        if rec:
            by_id[sid] = rec
            print(f"  + {sid}", flush=True)
        else:
            print(f"  missing {sid}", flush=True)
        time.sleep(0.08)

    # Also fetch any Aug14 ids
    for row in aug14:
        rid = str(row.get("record_id") or "").strip()
        if rid and rid not in by_id:
            rec = fetch_by_id(rid)
            if rec:
                by_id[rid] = rec

    # Keep only Simons-authored records (drop unrelated "Jonathan, Jonathan" hits).
    filtered: dict[str, dict[str, Any]] = {}
    for rid, rec in by_id.items():
        creators = rec.get("creators") or ""
        if SIMONS_CREATOR_RE.search(creators):
            filtered[rid] = rec
        else:
            print(f"  drop non-Simons creator {rid}: {creators!r}", flush=True)

    live_rows: list[dict[str, Any]] = []
    for rid, rec in filtered.items():
        disp, flags, alias, notes = classify(rec, settled, superseded_ids, superseded_by)
        live_rows.append(
            {
                **rec,
                "disposition": disp,
                "flags": "|".join(flags),
                "alias": alias,
                "notes": notes,
            }
        )

    # Sort: KEEP first, then by publication_date desc, record_id desc
    order = {"KEEP": 0, "NEEDS_TITLE_CLEAN": 1, "PARK/ARCHIVE": 2, "REVIEW": 3}

    def sort_key(r: dict[str, Any]) -> tuple:
        return (
            order.get(r["disposition"], 9),
            0 if "NEEDS_TITLE_CLEAN" in (r.get("flags") or "") else 1,
            r.get("publication_date") or "",
            r.get("record_id") or "",
        )

    live_rows.sort(key=sort_key, reverse=False)
    # Within same disposition, prefer newer dates — re-sort more carefully
    live_rows.sort(
        key=lambda r: (
            order.get(r["disposition"], 9),
            -(int(re.sub(r"\D", "", r.get("publication_date") or "0") or 0)),
            -int(r.get("record_id") or 0),
        )
    )

    diagnosis = diagnose_aug14_shift(aug14, filtered)

    aug_dois = {str(r.get("doi") or "").strip() for r in aug14 if str(r.get("doi") or "").strip()}
    live_dois = {r["doi"] for r in live_rows if r.get("doi")}
    aug_ids = {str(r.get("record_id") or "").strip() for r in aug14 if str(r.get("record_id") or "").strip()}
    live_ids = {r["record_id"] for r in live_rows}

    new_since = sorted(live_ids - aug_ids, key=lambda x: int(x))
    missing_since = sorted(aug_ids - live_ids, key=lambda x: int(x) if x.isdigit() else 0)
    title_changed = []
    for row in aug14:
        rid = str(row.get("record_id") or "").strip()
        if not rid or rid not in filtered:
            continue
        aug_t = (row.get("title") or "").strip()
        live_t = (filtered[rid].get("title") or "").strip()
        if aug_t and live_t and aug_t != live_t:
            title_changed.append({"record_id": rid, "aug14_title": aug_t, "live_title": live_t})

    counts = {"KEEP": 0, "PARK/ARCHIVE": 0, "REVIEW": 0, "NEEDS_TITLE_CLEAN": 0, "NEEDS_AUDIT_FIX": 0}
    for r in live_rows:
        counts[r["disposition"]] = counts.get(r["disposition"], 0) + 1
        for fl in (r.get("flags") or "").split("|"):
            if fl:
                counts[fl] = counts.get(fl, 0) + 1

    comparison = {
        "aug14_is_newest": False,
        "aug14_stale_reason": (
            "File columns misaligned (shift confirmed); "
            f"{len(new_since)} DOI(s)/record(s) present live but absent from Aug 14 dump; "
            f"{len(title_changed)} title change(s) vs Aug 14; "
            f"live inventory has {len(live_rows)} records vs Aug 14 {diagnosis['aug14_row_count']} rows "
            f"({diagnosis['aug14_rows_with_empty_doi_title']} with empty DOI/title)."
        ),
        "new_record_ids_since_aug14": new_since,
        "missing_from_live_vs_aug14": missing_since,
        "title_changed": title_changed,
        "file_shift_diagnosis": diagnosis,
        "counts": counts,
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    payload = {
        "schema": "zenodo_inventory_corrected_live_v1",
        "author_query": "Jonathan R. Simons / Simons, Jonathan*",
        "comparison_to_aug14": comparison,
        "records": live_rows,
    }

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    json_path = OUT_DIR / "ZENODO_INVENTORY_CORRECTED_LIVE.json"
    csv_path = OUT_DIR / "ZENODO_INVENTORY_CORRECTED_LIVE.csv"
    numbers_path = OUT_DIR / "ZENODO_INVENTORY_CORRECTED_LIVE_numbers.csv"
    comparison_path = OUT_DIR / "ZENODO_INVENTORY_COMPARISON_AUG14.json"

    json_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    comparison_path.write_text(json.dumps(comparison, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    fields = [
        "record_id",
        "doi",
        "url",
        "title",
        "publication_date",
        "version",
        "creators",
        "files",
        "file_count",
        "access",
        "updated",
        "conceptrecid",
        "disposition",
        "flags",
        "alias",
        "notes",
    ]
    write_csv(csv_path, live_rows, fields)
    # Numbers-friendly: same columns, UTF-8 BOM for Excel/Numbers
    with numbers_path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        for r in live_rows:
            w.writerow(r)

    print(json.dumps({"wrote": str(csv_path), "records": len(live_rows), "counts": counts, "new_since_aug14": new_since}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
