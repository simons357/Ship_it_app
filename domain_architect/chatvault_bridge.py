"""Drain a Domain Architect audit into a ChatVault export.

ChatVault is the conversation / record vault (OS for your AI).
Domain Architect is a Functional Role Analysis auditor. This bridge
writes ChatVault JSON so a finished audit can slide into ingest.

It does not:
- turn Domain Architect into a chat app
- prove Navier–Stokes, Riemann, or any theorem
- auto-mark CLAIM_LEDGER items PROVED
- host ChatVault in the cloud
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

from .audit import audit_expression
from .report import AuditReport

CHATVAULT_SCHEMA_VERSION = "chatvault-engine-0.3.0"
CHATVAULT_EXPORT_FORMAT = "chatvault-export"
DRAIN_PROTOCOL = "chatvault-drain-0.1.0"
DEFAULT_DRAIN_HOST = "127.0.0.1"
DEFAULT_DRAIN_PORT = 7847


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def audit_to_entry(report: AuditReport) -> dict[str, Any]:
    payload = report.to_dict()
    narrative = str(payload.get("narrative") or report.narrative())
    expression = str(payload.get("input_expression") or report.input_expression)
    evidence = payload.get("highest_evidence_label") or "n/a"
    status = payload.get("canonical_sfe_status") or "unresolved"
    ingested = _now()
    return {
        "schema_version": CHATVAULT_SCHEMA_VERSION,
        "id": f"da_{uuid.uuid4().hex[:12]}",
        "title": f"DA audit: {expression[:72]}",
        "source_type": "da_audit",
        "source_ai": "DomainArchitect",
        "origin_class": "human_record",
        "source_file": "",
        "project_tags": ["domain-architect"],
        "project_category": "Domain Architect",
        "content_text": narrative,
        "raw_content": narrative,
        "summary": (
            f"Domain Architect FRA audit. Evidence: {evidence}. "
            f"Canonical SFE status: {status}. Not a proof."
        ),
        "file_url": "",
        "key_claims": [],
        "theorems": [],
        "open_gaps": [],
        "action_items": [],
        "open_questions": [],
        "related_projects": ["Domain Architect"],
        "related_entities": [],
        "search_tags": ["domain-architect", "fra", "da_audit"],
        "linked_files": [],
        "extraction_types": [],
        "item_date": ingested[:10],
        "ingested_at": ingested,
        "updated_at": ingested,
        "visibility": "professional",
        "starred": False,
        "archived": False,
        "harmonic_note": "",
    }


def drain_report(report: AuditReport) -> dict[str, Any]:
    entry = audit_to_entry(report)
    return {
        "format": CHATVAULT_EXPORT_FORMAT,
        "schema_version": CHATVAULT_SCHEMA_VERSION,
        "source": "domain-architect",
        "drain_protocol": DRAIN_PROTOCOL,
        "exported_at": _now(),
        "count": 1,
        "entries": [entry],
    }


def drain_audit(expression: str) -> dict[str, Any]:
    return drain_report(audit_expression(expression))


def inquire(text: str, *, drain: bool = False) -> dict[str, Any]:
    """FRA inquiry for the DA/ChatVault inquiry box. Not a search ranker."""
    from .route_c import (
        face as route_c_face,
        looks_like_route_c_operator,
        looks_like_superseded_june_route_c,
        superseded_june_face,
    )
    from .universe import (
        face as universe_face,
        looks_like_universe_inquiry,
    )

    inquiry = str(text or "").strip()
    if not inquiry:
        raise ValueError("inquiry required")
    report = audit_expression(inquiry)
    route_c = looks_like_route_c_operator(inquiry)
    june = looks_like_superseded_june_route_c(inquiry)
    universe = (not route_c) and (not june) and looks_like_universe_inquiry(inquiry)
    drain_refused = None
    if drain and (route_c or june):
        drain = False
        drain_refused = (
            "Route C stays in Domain Architect. Not filed into ChatVault."
        )
    if drain and universe:
        drain = False
        drain_refused = (
            "Universe / SFE picture stays in Domain Architect inquiry. "
            "Unresolved. Not filed into ChatVault."
        )
    payload: dict[str, Any] = {
        "ok": True,
        "lane": "inquiry",
        "inquiry": inquiry,
        "audit": report.to_dict(),
        "canonical_sfe_status": report.canonical_sfe_status,
        "drain": drain_report(report) if drain else None,
    }
    if route_c:
        payload["route_c"] = route_c_face()
        payload["chatvault"] = False
    if june:
        payload["route_c_superseded"] = superseded_june_face()
        payload["chatvault"] = False
    if universe:
        payload["universe"] = universe_face()
        payload["chatvault"] = False
    if drain_refused:
        payload["drain_refused"] = drain_refused
    return payload


def write_drain(payload: dict[str, Any], path: str | Path) -> Path:
    out = Path(path)
    out.write_text(json.dumps(payload, indent=2, default=str), encoding="utf-8")
    return out


def try_enqueue(
    payload: dict[str, Any],
    *,
    host: str = DEFAULT_DRAIN_HOST,
    port: int = DEFAULT_DRAIN_PORT,
    timeout: float = 1.5,
) -> bool:
    """POST a ChatVault export to the local drain server if it is running."""
    body = json.dumps(payload, default=str).encode("utf-8")
    urls = [
        f"http://{host}:{port}/queue",
        f"http://{host}:{port}/api/drain/queue",
        f"http://{host}:8765/api/drain/queue",
    ]
    for url in urls:
        req = Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(req, timeout=timeout) as resp:
                if 200 <= getattr(resp, "status", 200) < 300:
                    return True
        except (URLError, OSError, TimeoutError):
            continue
    return False
