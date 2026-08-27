"""SND / Theorem H / Clay B claim anatomizer for Domain Architect.

Encodes the honest distinction:

* SND-U — open hypothesis (needed for Clay B)
* SND-C — conditional under a priori X <= M (what Theorem H proves)
* Clay B — NOT resolved

Refuses routing of "unconditional regularity" / Clay-solved language.
Does not prove or disprove any PDE theorem; audit tooling only.
"""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any


PACKAGE_DATA = Path(__file__).resolve().parent.parent / "data" / "domain_architect"
INVENTORY_PATH = PACKAGE_DATA / "snd_claim_inventory.json"

# Phrases that must never be auto-routed as proved / resolved.
REFUSAL_PATTERNS: tuple[tuple[str, str], ...] = (
    (
        r"unconditional\s+(global\s+)?regularity",
        "REFUSE: unconditional regularity is not an allowed routing target",
    ),
    (
        r"clay\s+(statement\s+)?b\s+(resolved|solved|proved|closed)",
        "REFUSE: Clay Statement (B) is NOT resolved",
    ),
    (
        r"millennium\s+(prize\s+)?(solved|proved|resolved)",
        "REFUSE: Millennium / Clay packaging must stay PARK / open",
    ),
    (
        r"snd\s+(for\s+all\s+data|unconditionally)\s+(proved|holds|established)",
        "REFUSE: SND-U remains an open hypothesis",
    ),
    (
        r"theorem\s+h\s+(is|=|equals|means)\s+(unconditional\s+)?snd",
        "REFUSE: Theorem H as written is SND-C under X<=M, not SND-U",
    ),
    (
        r"clay\s+(statement\s+)?b\s*(<=>|<->|iff|equivalent\s+to)\s*\[?snd",
        "REFUSE: Clay⇔SND equivalence is not established; broken weld TH-H2",
    ),
    (
        r"global\s+regularity.*(proved|resolved|no\s+(finite-time\s+)?blowup)",
        "REFUSE: unconditional global regularity / Clay B is NOT resolved",
    ),
    (
        r"c\s*\*\s*=\s*6\s*/\s*pi\s*\^\s*2.*(fluids|ns|navier|snd\s+floor|threshold)",
        "REFUSE: c*=6/pi^2 is arithmetic analogy, not continuum SND floor",
    ),
)

SND_U_MARKERS = (
    "snd-u",
    "unconditional snd",
    "snd for all",
    "inf j/x",
    "spectral non-dispersal unconditional",
)
SND_C_MARKERS = (
    "snd-c",
    "theorem h",
    "x<=m",
    "x ≤ m",
    "a priori enstrophy",
    "shell-conditioned",
    "spread regime",
)
CLAY_MARKERS = (
    "clay statement b",
    "clay (b)",
    "clay b",
    "millennium",
    "global regularity prize",
)


@dataclass
class ClaimHit:
    claim_id: str
    status: str
    status_detail: str
    matched_markers: list[str] = field(default_factory=list)


@dataclass
class SNDClaimAudit:
    input_text: str
    refused: bool
    refusal_reasons: list[str]
    hits: list[ClaimHit]
    inventory_summary: dict[str, str]
    notes: list[str]
    allowed_routing: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_text": self.input_text,
            "refused": self.refused,
            "refusal_reasons": self.refusal_reasons,
            "hits": [asdict(h) for h in self.hits],
            "inventory_summary": self.inventory_summary,
            "notes": self.notes,
            "allowed_routing": self.allowed_routing,
        }


def load_inventory(path: Path | None = None) -> dict[str, Any]:
    target = path or INVENTORY_PATH
    with target.open(encoding="utf-8") as fh:
        return json.load(fh)


def inventory_status_map(inventory: dict[str, Any] | None = None) -> dict[str, str]:
    inv = inventory or load_inventory()
    return {c["claim_id"]: c["status"] for c in inv["claims"]}


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().replace("≤", "<=").replace("−", "-"))


def detect_refusal(text: str) -> list[str]:
    norm = _normalize(text)
    reasons: list[str] = []
    for pattern, reason in REFUSAL_PATTERNS:
        if re.search(pattern, norm, flags=re.IGNORECASE):
            reasons.append(reason)
    return list(dict.fromkeys(reasons))


def _marker_hits(norm: str, markers: tuple[str, ...]) -> list[str]:
    return [m for m in markers if m in norm]


def anatomize_claim(text: str, inventory: dict[str, Any] | None = None) -> SNDClaimAudit:
    """Classify SND/Clay claim language; refuse overclaims."""
    inv = inventory or load_inventory()
    status = inventory_status_map(inv)
    norm = _normalize(text)
    refusal = detect_refusal(text)
    hits: list[ClaimHit] = []
    notes: list[str] = [
        "SND-U is open/hypothesis; SND-C is conditional under X<=M; Clay B is NOT resolved.",
        "Favorable ARCHON panel consensus is roleplay, not peer review.",
    ]

    for claim_id, markers in (
        ("SND-U", SND_U_MARKERS),
        ("SND-C", SND_C_MARKERS),
        ("CLAY-B", CLAY_MARKERS),
    ):
        matched = _marker_hits(norm, markers)
        if matched:
            meta = next(c for c in inv["claims"] if c["claim_id"] == claim_id)
            hits.append(
                ClaimHit(
                    claim_id=claim_id,
                    status=meta["status"],
                    status_detail=meta["status_detail"],
                    matched_markers=matched,
                )
            )

    if "6/pi^2" in norm or "6/π^2" in text.lower() or "6/pi²" in norm:
        meta = next(c for c in inv["claims"] if c["claim_id"] == "CSTAR-ARITHMETIC")
        hits.append(
            ClaimHit(
                claim_id="CSTAR-ARITHMETIC",
                status=meta["status"],
                status_detail=meta["status_detail"],
                matched_markers=["6/pi^2"],
            )
        )
        notes.append("c*=6/pi^2 flagged as arithmetic analogy only.")

    allowed: str | None
    if refusal:
        allowed = None
        notes.append("Routing refused: overclaim language detected.")
    elif any(h.claim_id == "SND-C" for h in hits):
        allowed = "SND-C_conditional_under_X_le_M"
        notes.append("Allowed routing: conditional SND-C / Theorem H-as-written.")
    elif any(h.claim_id == "SND-U" for h in hits):
        allowed = "SND-U_hypothesis_open"
        notes.append("Allowed routing: SND-U as open hypothesis only.")
    elif any(h.claim_id == "CLAY-B" for h in hits):
        allowed = "CLAY-B_not_resolved"
        notes.append("Allowed routing: Clay B recorded as not resolved.")
    else:
        allowed = "no_snd_clay_claim_detected"
        notes.append("No SND/Clay claim markers detected.")

    return SNDClaimAudit(
        input_text=text,
        refused=bool(refusal),
        refusal_reasons=refusal,
        hits=hits,
        inventory_summary=status,
        notes=notes,
        allowed_routing=allowed,
    )


def assert_not_unconditional_regularity(text: str) -> None:
    """Raise ValueError if text requests unconditional regularity routing."""
    reasons = detect_refusal(text)
    if reasons:
        raise ValueError("; ".join(reasons))


def refuse_unconditional_regularity_routing(text: str) -> dict[str, Any]:
    """Public helper for audits / CLI: always returns a structured refusal result."""
    audit = anatomize_claim(text)
    return {
        "ok": not audit.refused,
        "refused": audit.refused,
        "allowed_routing": audit.allowed_routing,
        "refusal_reasons": audit.refusal_reasons,
        "inventory_summary": audit.inventory_summary,
        "hits": [asdict(h) for h in audit.hits],
        "notes": audit.notes,
    }
