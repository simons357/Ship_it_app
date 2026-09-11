"""Library indexer — map what is in the user's library; report gaps honestly."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .shape_texture import MathObject, extract_object, extract_shape, extract_texture
from .theory_splicer import load_millennium_registry


REPO_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_DATA = REPO_ROOT / "data" / "domain_architect"
MANIFEST_PATH = PACKAGE_DATA / "library_manifest.json"
DOCS_NS = REPO_ROOT / "docs" / "ns-review"
DOCS_DA = REPO_ROOT / "docs" / "domain-architect"
ZENODO_META = REPO_ROOT / "data" / "zenodo" / "deposit_metadata.json"

LIBRARY_SOURCES = {
    "historical_equations": PACKAGE_DATA / "historical_equations.json",
    "snd_claim_inventory": PACKAGE_DATA / "snd_claim_inventory.json",
    "millennium_books": PACKAGE_DATA / "millennium_books.json",
    "snd_tweet_equations": PACKAGE_DATA / "snd_tweet_equations.json",
    "conflicts": PACKAGE_DATA / "conflicts.json",
}

KEEP_DISPOSITIONS = frozenset({"RETAIN", "REFERENCE", "KEEP"})
PARK_DISPOSITIONS = frozenset({"RETIRE", "PARK", "REFUSE"})
STATUS_FROM_DISPOSITION = {
    "RETAIN": "KEEP",
    "REFERENCE": "KEEP",
    "KEEP": "KEEP",
    "CONDITIONAL": "HYPOTHESIS",
    "OPEN": "HYPOTHESIS",
    "UNRESOLVED": "HYPOTHESIS",
    "RETIRE": "PARK",
    "REFUSE": "PARK",
    "REVISE": "HYPOTHESIS",
}


@dataclass
class ScanReport:
    scanned_at: str
    source_files: list[str]
    objects: list[dict[str, Any]]
    object_count: int
    keep_count: int
    hypothesis_count: int
    park_count: int
    coverage_gaps: list[str]
    millennium_coverage: dict[str, int]
    zenodo_refs: list[str] = field(default_factory=list)
    doc_refs: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _load_json(path: Path) -> Any:
    if not path.exists():
        return None
    return json.loads(path.read_text())


def _millennium_tags_for_family(family: str, domain: str = "", claim_id: str = "") -> list[str]:
    tags: list[str] = []
    fam = (family or "").upper()
    dom = (domain or "").lower()
    cid = (claim_id or "").upper()
    if any(x in fam for x in ("NS", "SND", "NAVIER")) or "navier" in dom:
        tags.append("NS")
    if any(x in fam for x in ("RH", "RIEMANN", "ZETA", "Q6")) or "zeta" in dom:
        tags.append("RH")
    if "CLAY" in fam or "CLAY" in cid:
        tags.extend(["NS", "CLAY"])
    if "FRA" in fam or "UHF" in fam:
        tags.append("FRA")
    if "SFE" in fam:
        tags.append("SFE")
    return sorted(set(tags))


def _status_from_row(
    disposition: str = "",
    status: str = "",
    status_detail: str = "",
) -> str:
    disp = (disposition or status or "").upper()
    if disp in KEEP_DISPOSITIONS:
        return "KEEP"
    if disp in PARK_DISPOSITIONS:
        return "PARK"
    if "conditional" in (status_detail or "").lower() or disp == "CONDITIONAL":
        return "HYPOTHESIS"
    return STATUS_FROM_DISPOSITION.get(disp, "HYPOTHESIS")


def _object_from_equation(eq: dict[str, Any]) -> dict[str, Any]:
    expr = eq.get("audited_expression") or eq.get("original_expression") or ""
    eid = eq.get("equation_id", "unknown")
    shape = extract_shape(expr)
    texture = extract_texture(expr)
    texture.book_id = eid
    tags = _millennium_tags_for_family(eq.get("family", ""), eq.get("domain", ""), eid)
    status = _status_from_row(eq.get("audit_disposition", ""))
    obj = MathObject(
        object_id=f"obj-eq-{eid}",
        label=f"{eid}: {expr[:50]}",
        shape=shape,
        texture=texture,
        millennium_tags=tags,
        status=status,
        source_refs=[f"historical_equations.json#{eid}"],
    )
    return obj.to_dict()


def _object_from_tweet(eq: dict[str, Any]) -> dict[str, Any]:
    expr = eq.get("da_expression") or eq.get("plain_text") or ""
    eid = eq.get("equation_id", "tweet-unknown")
    shape = extract_shape(expr)
    texture = extract_texture(expr)
    tags = _millennium_tags_for_family(eq.get("family", ""), claim_id=eid)
    status = _status_from_row(eq.get("audit_disposition", ""))
    obj = MathObject(
        object_id=f"obj-tweet-{eid}",
        label=eq.get("label", eid),
        shape=shape,
        texture=texture,
        millennium_tags=tags,
        status=status,
        source_refs=[f"snd_tweet_equations.json#{eid}"],
    )
    return obj.to_dict()


def _object_from_claim(claim: dict[str, Any]) -> dict[str, Any]:
    cid = claim.get("claim_id", "claim")
    definition = claim.get("definition", claim.get("label", ""))
    shape = extract_shape(definition)
    texture = extract_texture(definition)
    tags: list[str] = []
    clay = (claim.get("clay_relevance") or "").lower()
    if "statement b" in clay or "navier" in clay:
        tags.append("NS")
    if cid.startswith("CLAY"):
        tags.append("NS")
    if "snd" in cid.lower():
        tags.append("NS")
    status_map = {
        "open": "HYPOTHESIS",
        "conditional": "HYPOTHESIS",
        "not_resolved": "PARK",
        "refuted_as_written": "PARK",
        "analogy_only": "PARK",
    }
    status = status_map.get(claim.get("status", ""), "HYPOTHESIS")
    refs = ["snd_claim_inventory.json#" + cid]
    if claim.get("zenodo_keep_doi"):
        refs.append(f"zenodo:KEEP:{claim['zenodo_keep_doi']}")
    if claim.get("zenodo_park_doi"):
        refs.append(f"zenodo:PARK:{claim['zenodo_park_doi']}")
    obj = MathObject(
        object_id=f"obj-claim-{cid}",
        label=claim.get("label", cid),
        shape=shape,
        texture=texture,
        millennium_tags=sorted(set(tags)),
        status=status,
        source_refs=refs,
    )
    return obj.to_dict()


def _object_from_book(raw: dict[str, Any], millennium_id: str) -> dict[str, Any]:
    bid = raw.get("book_id", "book")
    expr = raw.get("expression", bid)
    shape = extract_shape(bid)
    texture = extract_texture(bid)
    book_status = raw.get("status", "OPEN")
    status = _status_from_row(book_status)
    obj = MathObject(
        object_id=f"obj-book-{bid}",
        label=raw.get("label", bid),
        shape=shape,
        texture=texture,
        millennium_tags=[millennium_id],
        status=status,
        source_refs=[f"millennium_books.json#{bid}"],
    )
    return obj.to_dict()


def _scan_docs() -> tuple[list[str], list[str]]:
    doc_refs: list[str] = []
    gaps: list[str] = []
    for folder, label in ((DOCS_NS, "ns-review"), (DOCS_DA, "domain-architect")):
        if not folder.exists():
            gaps.append(f"Missing docs folder: docs/{label}/")
            continue
        for path in sorted(folder.glob("*.md")):
            doc_refs.append(str(path.relative_to(REPO_ROOT)))
    return doc_refs, gaps


def _scan_zenodo() -> tuple[list[str], list[str]]:
    meta = _load_json(ZENODO_META)
    refs: list[str] = []
    gaps: list[str] = []
    if meta is None:
        gaps.append("data/zenodo/deposit_metadata.json not present — Zenodo KEEP/PARK not indexed")
        return refs, gaps
    deposits = meta.get("deposits") or meta.get("records") or []
    if isinstance(deposits, dict):
        deposits = list(deposits.values())
    for dep in deposits:
        doi = dep.get("doi") or dep.get("conceptdoi") or ""
        disposition = dep.get("disposition") or dep.get("status") or "unknown"
        if doi:
            refs.append(f"zenodo:{disposition}:{doi}")
    return refs, gaps


def scan_library(*, write_manifest: bool = True) -> dict[str, Any]:
    """Scan library assets and build object inventory."""
    objects: list[dict[str, Any]] = []
    source_files: list[str] = []
    coverage_gaps: list[str] = []
    seen_ids: set[str] = set()

    def _add(obj: dict[str, Any]) -> None:
        oid = obj.get("object_id", "")
        if oid and oid not in seen_ids:
            seen_ids.add(oid)
            objects.append(obj)

    # historical_equations.json
    hist = _load_json(LIBRARY_SOURCES["historical_equations"])
    if hist is None:
        coverage_gaps.append("historical_equations.json missing")
    else:
        source_files.append("data/domain_architect/historical_equations.json")
        for eq in hist if isinstance(hist, list) else hist.get("equations", []):
            _add(_object_from_equation(eq))

    # snd_tweet_equations.json
    tweets = _load_json(LIBRARY_SOURCES["snd_tweet_equations"])
    if tweets is None:
        coverage_gaps.append("snd_tweet_equations.json missing")
    else:
        source_files.append("data/domain_architect/snd_tweet_equations.json")
        for eq in tweets.get("equations", []):
            _add(_object_from_tweet(eq))

    # snd_claim_inventory.json
    claims = _load_json(LIBRARY_SOURCES["snd_claim_inventory"])
    if claims is None:
        coverage_gaps.append("snd_claim_inventory.json missing")
    else:
        source_files.append("data/domain_architect/snd_claim_inventory.json")
        for claim in claims.get("claims", []):
            _add(_object_from_claim(claim))

    # millennium_books.json
    millennium = _load_json(LIBRARY_SOURCES["millennium_books"])
    if millennium is None:
        coverage_gaps.append("millennium_books.json missing")
    else:
        source_files.append("data/domain_architect/millennium_books.json")
        for pid, prob in millennium.get("problems", {}).items():
            for book in prob.get("books", []):
                _add(_object_from_book(book, pid))

    doc_refs, doc_gaps = _scan_docs()
    coverage_gaps.extend(doc_gaps)
    zenodo_refs, zenodo_gaps = _scan_zenodo()
    coverage_gaps.extend(zenodo_gaps)

    keep = sum(1 for o in objects if o.get("status") == "KEEP")
    hyp = sum(1 for o in objects if o.get("status") == "HYPOTHESIS")
    park = sum(1 for o in objects if o.get("status") == "PARK")

    millennium_coverage: dict[str, int] = {}
    for o in objects:
        for tag in o.get("millennium_tags") or []:
            millennium_coverage[tag] = millennium_coverage.get(tag, 0) + 1

    report = ScanReport(
        scanned_at=datetime.now(timezone.utc).isoformat(),
        source_files=source_files,
        objects=objects,
        object_count=len(objects),
        keep_count=keep,
        hypothesis_count=hyp,
        park_count=park,
        coverage_gaps=coverage_gaps,
        millennium_coverage=millennium_coverage,
        zenodo_refs=zenodo_refs,
        doc_refs=doc_refs,
    )
    payload = report.to_dict()
    payload["honesty"] = (
        "Library scan maps what exists — does not invent missing proofs."
    )

    if write_manifest:
        MANIFEST_PATH.parent.mkdir(parents=True, exist_ok=True)
        MANIFEST_PATH.write_text(json.dumps(payload, indent=2, default=str) + "\n")

    return payload


def load_manifest(path: Path | None = None) -> dict[str, Any]:
    """Load cached manifest or scan if missing."""
    p = path or MANIFEST_PATH
    data = _load_json(p)
    if data is None:
        return scan_library(write_manifest=True)
    return data


def inventory_summary(manifest: dict[str, Any] | None = None) -> str:
    """One-paragraph human summary of library inventory."""
    m = manifest or load_manifest()
    gaps = m.get("coverage_gaps") or []
    gap_note = f" Gaps: {'; '.join(gaps[:3])}." if gaps else ""
    mc = m.get("millennium_coverage") or {}
    mc_str = ", ".join(f"{k}={v}" for k, v in sorted(mc.items()))
    return (
        f"Library manifest: {m.get('object_count', 0)} objects "
        f"({m.get('keep_count', 0)} KEEP, "
        f"{m.get('hypothesis_count', 0)} HYPOTHESIS, "
        f"{m.get('park_count', 0)} PARK). "
        f"Millennium tags: {mc_str or 'none'}.{gap_note}"
    )
