"""Dual-SFE (or dual-expression) conflict/compare — \"put SFE in twice\".

Audits two registry candidates (or the same expression twice / two
historical SFE strings) and shows structural conflict/compare.

Canonical SFE status stays unresolved. This path must never invent or
select a canonical SFE.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .audit import audit_expression
from .hb_loop import compare_reports
from .registry import EquationRegistry
from .report import AuditReport
from .schema import CANONICAL_SFE_STATUS, ConflictRelation


@dataclass
class SFEDualCompare:
    left_id: str
    right_id: str
    left_expression: str
    right_expression: str
    left_family: str
    right_family: str
    same_expression: bool
    compare: dict[str, Any]
    registry_relation: str
    registry_evidence: str
    existing_conflicts: list[dict[str, Any]] = field(default_factory=list)
    canonical_sfe_status: str = CANONICAL_SFE_STATUS
    statement: str = ""
    left_audit: dict[str, Any] | None = None
    right_audit: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "left_id": self.left_id,
            "right_id": self.right_id,
            "left_expression": self.left_expression,
            "right_expression": self.right_expression,
            "left_family": self.left_family,
            "right_family": self.right_family,
            "same_expression": self.same_expression,
            "compare": self.compare,
            "registry_relation": self.registry_relation,
            "registry_evidence": self.registry_evidence,
            "existing_conflicts": self.existing_conflicts,
            "canonical_sfe_status": self.canonical_sfe_status,
            "statement": self.statement,
            "left_audit": self.left_audit,
            "right_audit": self.right_audit,
        }

    def narrative(self) -> str:
        lines = [
            "Domain Architect — dual SFE / dual-expression audit",
            "",
            "\"Put SFE in twice\": compare two candidates without merging them.",
            f"Canonical SFE status: {self.canonical_sfe_status}.",
            "",
            f"Left:  [{self.left_id}] ({self.left_family}) {self.left_expression}",
            f"Right: [{self.right_id}] ({self.right_family}) {self.right_expression}",
            "",
            f"Same original string: {self.same_expression}",
            f"Registry relation: {self.registry_relation}",
            f"Evidence: {self.registry_evidence}",
            "",
        ]
        if self.existing_conflicts:
            lines.append("Existing registry conflicts involving this pair:")
            for c in self.existing_conflicts:
                lines.append(
                    f"  - {c.get('left_id')} vs {c.get('right_id')}: "
                    f"{c.get('relation')} ({c.get('status')})"
                )
            lines.append("")
        # Structural HB compare summary
        cmp = self.compare
        lines.append("Structural HB compare:")
        lines.append(f"  shared roles: {', '.join(cmp.get('shared_roles') or []) or '(none)'}")
        lines.append(f"  only left: {', '.join(cmp.get('only_left') or []) or '(none)'}")
        lines.append(f"  only right: {', '.join(cmp.get('only_right') or []) or '(none)'}")
        for w in cmp.get("why_not_working") or []:
            lines.append(f"  - {w}")
        lines.append("")
        lines.append(self.statement)
        lines.append("")
        lines.append(
            "No hybrid equation is synthesized. Both candidates remain "
            "archived; unresolved is a valid outcome."
        )
        return "\n".join(lines)


def _resolve_side(
    spec: str,
    registry: EquationRegistry,
) -> tuple[str, str, str, str]:
    """Return (id, expression, family, source_kind)."""
    if spec in registry.equations:
        rec = registry.equations[spec]
        return rec.equation_id, rec.original_expression, rec.family, "registry"
    # Alias lookup
    for rec in registry.equations.values():
        if rec.alias and rec.alias == spec:
            return rec.equation_id, rec.original_expression, rec.family, "registry_alias"
    # Raw expression
    return "EXPR", spec, "expression", "literal"


def compare_sfe_pair(
    left_spec: str,
    right_spec: str,
    *,
    registry: EquationRegistry | None = None,
    include_audits: bool = True,
) -> SFEDualCompare:
    """Audit and compare two SFE candidates or arbitrary expressions."""
    reg = registry or EquationRegistry.load_default()
    left_id, left_expr, left_fam, _ = _resolve_side(left_spec, reg)
    right_id, right_expr, right_fam, _ = _resolve_side(right_spec, reg)

    left_report = audit_expression(left_expr)
    right_report = audit_expression(right_expr)
    cmp = compare_reports(left_report, right_report)

    existing = [
        c.to_dict()
        for c in reg.conflicts
        if {c.left_id, c.right_id} == {left_id, right_id}
        or (
            left_id != "EXPR"
            and right_id != "EXPR"
            and left_id in (c.left_id, c.right_id)
            and right_id in (c.left_id, c.right_id)
        )
    ]

    same = left_expr.strip() == right_expr.strip()
    both_sfe = left_fam == "SFE" and right_fam == "SFE"

    if same and left_id == right_id:
        relation = ConflictRelation.IDENTICAL.value
        evidence = "Same registry id / identical expression audited twice."
        statement = (
            "Same candidate entered twice. Structural maps match by construction; "
            "this does not elevate the expression to a canonical SFE."
        )
    elif same:
        relation = ConflictRelation.IDENTICAL.value
        evidence = "Identical original expression strings; distinct ids may still exist historically."
        statement = (
            "Expressions match textually. Domain Architect still refuses to "
            "declare a canonical SFE."
        )
    elif both_sfe:
        relation = ConflictRelation.INCOMPATIBLE.value
        evidence = (
            "Distinct historical SFE candidates with no checked transformation "
            "that would justify merging."
        )
        statement = (
            "Two SFE registry candidates conflict at the provenance layer. "
            f"Canonical SFE status remains {CANONICAL_SFE_STATUS}. "
            "Hybrid synthesis is forbidden."
        )
    else:
        relation = ConflictRelation.COMPATIBLE_DISTINCT.value
        if left_fam != right_fam:
            relation = ConflictRelation.INCOMPATIBLE.value
            evidence = (
                f"Different families ({left_fam} vs {right_fam}); shared "
                "letters do not imply shared physics."
            )
        else:
            evidence = "Distinct expressions; compare is structural only."
        statement = (
            "Dual-expression compare complete. No canonical equation is selected."
        )

    return SFEDualCompare(
        left_id=left_id,
        right_id=right_id,
        left_expression=left_expr,
        right_expression=right_expr,
        left_family=left_fam,
        right_family=right_fam,
        same_expression=same,
        compare=cmp.to_dict(),
        registry_relation=relation,
        registry_evidence=evidence,
        existing_conflicts=existing,
        statement=statement,
        left_audit=left_report.to_dict() if include_audits else None,
        right_audit=right_report.to_dict() if include_audits else None,
    )


def list_sfe_candidates(registry: EquationRegistry | None = None) -> list[dict[str, str]]:
    reg = registry or EquationRegistry.load_default()
    out = []
    for rec in reg.equations.values():
        if rec.family == "SFE":
            out.append(
                {
                    "equation_id": rec.equation_id,
                    "alias": rec.alias,
                    "disposition": rec.audit_disposition,
                    "expression": rec.original_expression,
                }
            )
    return out
