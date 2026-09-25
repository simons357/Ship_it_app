"""Schema v5 process objects: stamps, runs, promotion, ledger records.

This module is the engineering contract for Process Console. Scientific
outcome fields are stored for display but are never inputs to verdict
or promotion.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

from .schema import (
    OPAQUE_STAMP_LABELS,
    SCHEMA_VERSION,
    PromotionDecision,
    ProcessStatus,
    StampKind,
)


class SchemaError(ValueError):
    """Malformed v5 process object."""


def _require(cond: bool, message: str) -> None:
    if not cond:
        raise SchemaError(message)


def normalize_stamp_token(raw: str) -> str:
    return " ".join(raw.strip().upper().replace("_", "-").split())


def parse_stamp_kind(raw: str) -> StampKind:
    token = normalize_stamp_token(raw)
    if token in OPAQUE_STAMP_LABELS or token.replace("-", " ") in {
        "DA STAMPED",
        "DA STAMP",
    }:
        raise SchemaError(
            "opaque stamp label is not a v5 stamp kind: "
            f"{raw!r}. Use proved, reproduced, or consistency_check."
        )
    aliases = {
        "PROVED": StampKind.PROVED,
        "REPRODUCED": StampKind.REPRODUCED,
        "CONSISTENCY CHECK": StampKind.CONSISTENCY_CHECK,
        "CONSISTENCY-CHECK": StampKind.CONSISTENCY_CHECK,
        "CONSISTENCY_CHECK": StampKind.CONSISTENCY_CHECK,
    }
    if token in aliases:
        return aliases[token]
    try:
        return StampKind(raw.strip().lower())
    except ValueError as exc:
        raise SchemaError(f"unknown stamp kind: {raw!r}") from exc


@dataclass(frozen=True)
class StampRecord:
    kind: StampKind
    statement: str
    status: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "label": self.kind.label,
            "statement": self.statement,
            "status": self.status,
            "notes": self.notes,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "StampRecord":
        return cls(
            kind=parse_stamp_kind(str(payload["kind"])),
            statement=str(payload.get("statement", "")),
            status=str(payload.get("status", "")),
            notes=str(payload.get("notes", "")),
        )


@dataclass(frozen=True)
class ConsistencyCheck:
    check_id: str
    stipulated_formula: str
    implementation: str
    passed: bool
    detail: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ConsistencyCheck":
        return cls(
            check_id=str(payload["check_id"]),
            stipulated_formula=str(payload["stipulated_formula"]),
            implementation=str(payload["implementation"]),
            passed=bool(payload["passed"]),
            detail=str(payload.get("detail", "")),
        )


@dataclass(frozen=True)
class DecisionWindow:
    window_id: str
    admission: dict[str, Any]
    locked: bool = True
    changed_by_da: bool = False
    change_note: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "window_id": self.window_id,
            "admission": dict(self.admission),
            "locked": self.locked,
            "changed_by_da": self.changed_by_da,
            "change_note": self.change_note,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "DecisionWindow":
        return cls(
            window_id=str(payload["window_id"]),
            admission=dict(payload.get("admission") or {}),
            locked=bool(payload.get("locked", True)),
            changed_by_da=bool(payload.get("changed_by_da", False)),
            change_note=str(payload.get("change_note", "")),
        )


Q4_DECISION_WINDOW = DecisionWindow(
    window_id="Q4-DECISION-WINDOW-2026-09-25",
    admission={
        "T_c_positive": True,
        "alpha_c_near_one": True,
        "note": "Same window as Q4-0 / Q4-1 v1 unless DA changes it beforehand.",
    },
    locked=True,
    changed_by_da=False,
)


@dataclass
class ProcessRun:
    """A recorded scientific run. Verdict ignores scientific_outcome."""

    run_id: str
    title: str
    version: str
    lane: str
    process_status: ProcessStatus
    scientific_outcome: str
    executed: bool
    preregistered: bool
    decision_window: DecisionWindow
    consistency_checks: list[ConsistencyCheck] = field(default_factory=list)
    stamps: list[StampRecord] = field(default_factory=list)
    protocol_hash: str = ""
    code_hashes: dict[str, str] = field(default_factory=dict)
    diagnostics: dict[str, Any] = field(default_factory=dict)
    inherited_evidence_ids: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    historical: bool = False
    defective: bool = False

    @property
    def failed_consistency_checks(self) -> list[ConsistencyCheck]:
        return [c for c in self.consistency_checks if not c.passed]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": SCHEMA_VERSION,
            "run_id": self.run_id,
            "title": self.title,
            "version": self.version,
            "lane": self.lane,
            "process_status": self.process_status.value,
            "scientific_outcome": self.scientific_outcome,
            "executed": self.executed,
            "preregistered": self.preregistered,
            "decision_window": self.decision_window.to_dict(),
            "consistency_checks": [c.to_dict() for c in self.consistency_checks],
            "stamps": [s.to_dict() for s in self.stamps],
            "protocol_hash": self.protocol_hash,
            "code_hashes": dict(self.code_hashes),
            "diagnostics": dict(self.diagnostics),
            "inherited_evidence_ids": list(self.inherited_evidence_ids),
            "notes": list(self.notes),
            "historical": self.historical,
            "defective": self.defective,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "ProcessRun":
        version = str(payload.get("schema_version") or SCHEMA_VERSION)
        _require(
            version == SCHEMA_VERSION,
            f"Process Console reads schema {SCHEMA_VERSION} only, got {version!r}",
        )
        return cls(
            run_id=str(payload["run_id"]),
            title=str(payload["title"]),
            version=str(payload.get("version", "")),
            lane=str(payload.get("lane", "research")),
            process_status=ProcessStatus(str(payload["process_status"])),
            scientific_outcome=str(payload.get("scientific_outcome", "")),
            executed=bool(payload.get("executed", False)),
            preregistered=bool(payload.get("preregistered", False)),
            decision_window=DecisionWindow.from_dict(payload["decision_window"]),
            consistency_checks=[
                ConsistencyCheck.from_dict(c)
                for c in payload.get("consistency_checks") or []
            ],
            stamps=[StampRecord.from_dict(s) for s in payload.get("stamps") or []],
            protocol_hash=str(payload.get("protocol_hash", "")),
            code_hashes=dict(payload.get("code_hashes") or {}),
            diagnostics=dict(payload.get("diagnostics") or {}),
            inherited_evidence_ids=list(payload.get("inherited_evidence_ids") or []),
            notes=list(payload.get("notes") or []),
            historical=bool(payload.get("historical", False)),
            defective=bool(payload.get("defective", False)),
        )


def compute_process_status(run: ProcessRun) -> ProcessStatus:
    """Verdict from process fields only. Scientific outcome is ignored."""
    if run.process_status is ProcessStatus.WITHDRAWN:
        return ProcessStatus.WITHDRAWN
    if run.failed_consistency_checks or run.defective:
        return ProcessStatus.INCONCLUSIVE
    if run.process_status is ProcessStatus.CLOSED_NEGATIVE:
        return ProcessStatus.CLOSED_NEGATIVE
    if run.preregistered and not run.executed:
        return ProcessStatus.PREREGISTERED
    if run.executed:
        return ProcessStatus.EXECUTED
    return run.process_status


def promotion_decision(run: ProcessRun) -> tuple[PromotionDecision, str]:
    status = compute_process_status(run)
    if status is ProcessStatus.INCONCLUSIVE:
        return (
            PromotionDecision.PROHIBITED,
            "INCONCLUSIVE runs cannot be promoted to evidence.",
        )
    if status is ProcessStatus.WITHDRAWN:
        return (
            PromotionDecision.PROHIBITED,
            "WITHDRAWN records are provenance only.",
        )
    if status is ProcessStatus.PREREGISTERED:
        return (
            PromotionDecision.PROHIBITED,
            "Preregistered runs are not evidence until executed under the locked window.",
        )
    if run.failed_consistency_checks:
        return (
            PromotionDecision.PROHIBITED,
            "A failed consistency check blocks promotion.",
        )
    if any(s.status.lower() == "failed" for s in run.stamps):
        return (
            PromotionDecision.PROHIBITED,
            "A failed stamp blocks promotion.",
        )
    if status is ProcessStatus.CLOSED_NEGATIVE:
        return (
            PromotionDecision.PROHIBITED,
            "A closed negative result is a map entry, not positive evidence.",
        )
    return (
        PromotionDecision.PROHIBITED,
        "Schema v5 default: promotion requires an explicit later DA action; "
        "this console never auto-promotes.",
    )
