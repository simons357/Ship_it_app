"""Equation provenance, conflict engine, dispositions, and null registry.

Historical expressions are stored immutably. The software does not merge
equations because they share letters, and it does not synthesize a hybrid
canonical SFE.
"""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from .schema import CANONICAL_SFE_STATUS, ConflictRelation, Disposition


PACKAGE_DATA = Path(__file__).resolve().parent.parent / "data" / "domain_architect"


EQUATION_FIELDS = (
    "equation_id",
    "family",
    "date",
    "original_source",
    "original_expression",
    "audited_expression",
    "original_symbol_definitions",
    "original_stated_interpretation",
    "original_claimed_consequence",
    "domain",
    "units",
    "function_space",
    "operator_domain",
    "boundary_conditions",
    "initial_conditions",
    "geometry",
    "gauge_conditions",
    "source_terms",
    "nonlinearity",
    "couplings",
    "unknown_definitions",
    "dimensional_status",
    "known_limit_status",
    "conflicts",
    "audit_disposition",
    "alias",
    "notes",
)


@dataclass
class EquationRecord:
    equation_id: str
    family: str
    original_expression: str
    original_source: str = ""
    date: str = ""
    audited_expression: str = ""
    original_symbol_definitions: str = ""
    original_stated_interpretation: str = ""
    original_claimed_consequence: str = ""
    domain: str = ""
    units: str = "unknown"
    function_space: str = "unknown"
    operator_domain: str = "unknown"
    boundary_conditions: str = ""
    initial_conditions: str = ""
    geometry: str = ""
    gauge_conditions: str = ""
    source_terms: str = ""
    nonlinearity: str = ""
    couplings: str = ""
    unknown_definitions: str = ""
    dimensional_status: str = "unknown"
    known_limit_status: str = "not_claimed"
    conflicts: list[str] = field(default_factory=list)
    audit_disposition: str = Disposition.UNRESOLVED.value
    alias: str = ""
    notes: str = ""
    immutable_original: bool = True

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class ConflictRecord:
    left_id: str
    right_id: str
    relation: str
    evidence: str
    status: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class NullRecord:
    null_id: str
    kind: str
    statement: str
    evidence: str
    source: str = ""
    created_at: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class EquationRegistry:
    """Permanent historical equation store. Originals are never rewritten."""

    def __init__(self) -> None:
        self.equations: dict[str, EquationRecord] = {}
        self.conflicts: list[ConflictRecord] = []
        self.nulls: list[NullRecord] = []

    @classmethod
    def load_default(cls, data_dir: Path | None = None) -> "EquationRegistry":
        registry = cls()
        root = data_dir or PACKAGE_DATA
        eq_path = root / "historical_equations.json"
        cf_path = root / "conflicts.json"
        nl_path = root / "null_results.json"
        if eq_path.exists():
            for raw in json.loads(eq_path.read_text()):
                registry.add_equation(EquationRecord(**_filter_eq(raw)), overwrite=False)
        if cf_path.exists():
            for raw in json.loads(cf_path.read_text()):
                registry.add_conflict(ConflictRecord(**raw), allow_duplicate=True)
        if nl_path.exists():
            for raw in json.loads(nl_path.read_text()):
                registry.nulls.append(NullRecord(**raw))
        tweet_path = root / "snd_tweet_equations.json"
        if tweet_path.exists():
            payload = json.loads(tweet_path.read_text())
            for raw in payload.get("equations", []):
                mapped = {
                    "equation_id": raw["equation_id"],
                    "family": raw["family"],
                    "date": payload.get("source", {}).get("date", ""),
                    "original_source": payload.get("source", {}).get("tweet_url", ""),
                    "original_expression": raw.get("da_expression", raw.get("plain_text", "")),
                    "audited_expression": raw.get("da_expression", raw.get("plain_text", "")),
                    "original_symbol_definitions": raw.get("symbol_definitions", ""),
                    "original_stated_interpretation": raw.get("plain_text", ""),
                    "original_claimed_consequence": raw.get("tweet_status", ""),
                    "domain": raw.get("family", ""),
                    "conflicts": raw.get("conflicts", []),
                    "audit_disposition": raw.get("audit_disposition", Disposition.UNRESOLVED.value),
                    "alias": raw.get("label", ""),
                    "notes": raw.get("notes", ""),
                }
                registry.add_equation(
                    EquationRecord(**_filter_eq(mapped)),
                    overwrite=False,
                )
        return registry

    def add_equation(self, record: EquationRecord, *, overwrite: bool = False) -> None:
        if record.equation_id in self.equations and not overwrite:
            existing = self.equations[record.equation_id]
            if existing.original_expression != record.original_expression:
                raise ValueError(
                    f"{record.equation_id} already exists; original expressions "
                    "are immutable. Register a new ID instead of editing."
                )
            return
        self.equations[record.equation_id] = record

    def add_conflict(
        self, record: ConflictRecord, *, allow_duplicate: bool = False
    ) -> None:
        if record.relation not in {c.value for c in ConflictRelation}:
            raise ValueError(f"unknown conflict relation: {record.relation}")
        if not allow_duplicate:
            for existing in self.conflicts:
                ids = {existing.left_id, existing.right_id}
                if ids == {record.left_id, record.right_id} and existing.relation == record.relation:
                    return
        if self._would_merge_silently(record):
            raise ValueError(
                "refusing to merge equations from shared variable names; "
                "state an explicit transformation first"
            )
        self.conflicts.append(record)

    def _would_merge_silently(self, record: ConflictRecord) -> bool:
        return False

    def classify_pair(
        self,
        left_id: str,
        right_id: str,
        relation: str,
        evidence: str,
        status: str = "recorded",
        notes: str = "",
    ) -> ConflictRecord:
        if relation in {
            ConflictRelation.IDENTICAL.value,
            ConflictRelation.NOTATIONALLY_EQUIVALENT.value,
            ConflictRelation.EQUIVALENT_UNDER_SUBSTITUTION.value,
        } and not evidence.strip():
            raise ValueError(
                "equivalence requires an explicit checked transformation"
            )
        rec = ConflictRecord(
            left_id=left_id,
            right_id=right_id,
            relation=relation,
            evidence=evidence,
            status=status,
            notes=notes,
        )
        self.add_conflict(rec)
        if relation == ConflictRelation.INCOMPATIBLE.value:
            for eq_id in (left_id, right_id):
                if eq_id in self.equations:
                    if rec.left_id + "/" + rec.right_id not in self.equations[eq_id].conflicts:
                        self.equations[eq_id].conflicts.append(f"{left_id}/{right_id}")
        return rec

    def refuse_hybrid(self, left_id: str, right_id: str) -> str:
        """Keep both candidates and refuse to synthesize a third equation."""
        left = self.equations.get(left_id)
        right = self.equations.get(right_id)
        if left is None or right is None:
            return "INSUFFICIENT_INFORMATION"
        if left.original_expression != right.original_expression:
            self.classify_pair(
                left_id,
                right_id,
                ConflictRelation.INCOMPATIBLE.value
                if left.audit_disposition != right.audit_disposition
                or left.original_expression != right.original_expression
                else ConflictRelation.COMPATIBLE_DISTINCT.value,
                evidence="distinct original expressions; no checked transformation",
                status="unresolved",
                notes="hybrid synthesis is forbidden",
            )
            return "preserved_both_flagged_conflict"
        return "identical_originals"

    def set_disposition(self, equation_id: str, disposition: str, reason: str) -> None:
        rec = self.equations[equation_id]
        rec.audit_disposition = disposition
        rec.notes = (rec.notes + " | " if rec.notes else "") + reason

    def canonical_sfe_status(self) -> str:
        live = [
            r
            for r in self.equations.values()
            if r.family == "SFE"
            and r.audit_disposition == Disposition.RETAIN.value
            and "canonical" in (r.notes + r.original_stated_interpretation).lower()
        ]
        if live:
            return "unresolved — retained historical candidates are not canonical"
        return CANONICAL_SFE_STATUS

    def record_null(
        self,
        kind: str,
        statement: str,
        evidence: str,
        source: str = "domain_architect",
        null_id: str | None = None,
    ) -> NullRecord:
        rec = NullRecord(
            null_id=null_id or f"NULL-{len(self.nulls)+1:03d}",
            kind=kind,
            statement=statement,
            evidence=evidence,
            source=source,
            created_at=_now(),
        )
        self.nulls.append(rec)
        return rec

    def prominent_nulls(self) -> list[NullRecord]:
        return list(self.nulls)

    def export(self) -> dict[str, Any]:
        return {
            "canonical_sfe_status": self.canonical_sfe_status(),
            "equations": [r.to_dict() for r in self.equations.values()],
            "conflicts": [c.to_dict() for c in self.conflicts],
            "nulls": [n.to_dict() for n in self.nulls],
        }


def _filter_eq(raw: dict[str, Any]) -> dict[str, Any]:
    allowed = set(EquationRecord.__dataclass_fields__)
    return {k: v for k, v in raw.items() if k in allowed}


def seed_from_inventory() -> EquationRegistry:
    """Load the shipped historical inventory."""
    return EquationRegistry.load_default()


def format_conflict_table(conflicts: Iterable[ConflictRecord]) -> str:
    rows = ["Equation\tRelation\tEvidence\tStatus"]
    for item in conflicts:
        rows.append(
            f"{item.left_id} vs {item.right_id}\t{item.relation}\t"
            f"{item.evidence}\t{item.status}"
        )
    return "\n".join(rows)
