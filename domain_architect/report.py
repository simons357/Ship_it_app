"""Evidence-aware report generation and language enforcement."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from .schema import (
    CANONICAL_SFE_STATUS,
    FORBIDDEN_CLAIM_PHRASES,
    ORGANIZING_GRAMMAR,
    PRODUCT_DESCRIPTION,
    EvidenceLevel,
    MathValidationStatus,
    PhysicalValidationStatus,
)


@dataclass
class ConfidenceTaxonomy:
    parser_confidence: float = 0.0
    role_classification_confidence: float = 0.0
    definition_completeness: float = 0.0
    mathematical_validation_status: str = MathValidationStatus.NOT_PERFORMED.value
    physical_validation_status: str = PhysicalValidationStatus.NONE.value

    def as_dict(self) -> dict[str, Any]:
        return {
            "parser_confidence": self.parser_confidence,
            "role_classification_confidence": self.role_classification_confidence,
            "definition_completeness": self.definition_completeness,
            "mathematical_validation_status": self.mathematical_validation_status,
            "physical_validation_status": self.physical_validation_status,
        }


def sanitize_language(text: str) -> tuple[str, list[str]]:
    """Strip or flag claim verbs that exceed the evidence."""
    flags: list[str] = []
    lowered = text.lower()
    for phrase in FORBIDDEN_CLAIM_PHRASES:
        if phrase in lowered:
            flags.append(f"forbidden claim language: {phrase!r}")
    cleaned = text
    replacements = (
        (r"\bderives Newtonian gravity from the SFE\b",
         "expresses the Newtonian Poisson solution using Functional Role Analysis"),
        (r"\bderives gravity\b", "represents the stated gravity equation"),
        (r"\bproves\b", "is consistent with"),
        (r"\bdiscovers\b", "records"),
        (r"\bunified theory\b", "organizational correspondence"),
        (r"\bprime structure is fundamental\b",
         "prime selection is an experimental hypothesis"),
    )
    for pattern, repl in replacements:
        cleaned = re.sub(pattern, repl, cleaned, flags=re.IGNORECASE)
    return cleaned, flags


@dataclass
class AuditReport:
    input_expression: str
    highest_evidence_level: EvidenceLevel
    ast_pretty: str
    role_assignments: list[dict[str, Any]]
    warnings: list[str]
    confidence: ConfidenceTaxonomy
    recovery_kind: str | None = None
    recovery_statement: str | None = None
    poisson_compatibility: dict[str, Any] | None = None
    identifiability: dict[str, Any] | None = None
    index_audit: dict[str, Any] | None = None
    extra_structures: list[str] = field(default_factory=list)
    canonical_sfe_status: str = CANONICAL_SFE_STATUS
    language_flags: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    hb_map: dict[str, Any] | None = None
    reconstruction: dict[str, Any] | None = None
    tuning_export: dict[str, Any] | None = None
    incompleteness: dict[str, Any] | None = None
    decomposition: dict[str, Any] | None = None

    def narrative(self) -> str:
        lines = [
            "Domain Architect — Functional Role Analysis report",
            "",
            PRODUCT_DESCRIPTION,
            "",
            f"Organizing grammar (organizational, not a universal law): {ORGANIZING_GRAMMAR}",
            f"Highest evidence level actually supported: {self.highest_evidence_level.label}",
            f"Canonical SFE status: {self.canonical_sfe_status}.",
            "",
            f"Input: {self.input_expression}",
            "",
            "Abstract syntax tree:",
            self.ast_pretty or "(unparsed)",
            "",
            "Role assignments (structural candidates, not physical identities):",
        ]
        if not self.role_assignments:
            lines.append("  none — symbols were not assigned physical roles from their names")
        for item in self.role_assignments:
            lines.append(
                f"  {item.get('symbol')}: role={item.get('candidate_role')} "
                f"subtype={item.get('subtype')} confidence={item.get('confidence')}"
            )
            if item.get("justification"):
                lines.append(f"    {item['justification']}")
        lines.append("")
        lines.append("Confidence taxonomy:")
        for key, value in self.confidence.as_dict().items():
            lines.append(f"  {key}: {value}")
        lines.append(
            "A high role-classification score does not imply physical validity."
        )
        if self.recovery_kind:
            lines.append("")
            lines.append(f"Recovery kind: {self.recovery_kind}")
            if self.recovery_statement:
                lines.append(self.recovery_statement)
        if self.poisson_compatibility:
            lines.append("")
            lines.append("Poisson compatibility:")
            for key, value in self.poisson_compatibility.items():
                lines.append(f"  {key} = {value}")
        if self.identifiability:
            lines.append("")
            lines.append("Identifiability:")
            lines.append(f"  {self.identifiability.get('statement')}")
            for warning in self.identifiability.get("warnings", []):
                lines.append(f"  warning: {warning}")
            for amb in self.identifiability.get("product_ambiguities", []):
                lines.append(f"  {amb}")
        if self.index_audit:
            lines.append("")
            lines.append("Canonical index audit:")
            for key, value in self.index_audit.get("answers", {}).items():
                lines.append(f"  {key} {value}")
            for warning in self.index_audit.get("warnings", []):
                lines.append(f"  warning: {warning}")
        if self.extra_structures:
            lines.append("")
            lines.append(
                "Independently necessary structures recorded in E: "
                + ", ".join(self.extra_structures)
            )
        if self.reconstruction:
            lines.append("")
            lines.append("Reconstruction check (mapper fidelity, not a PDE solve):")
            lines.append(f"  passed: {self.reconstruction.get('passed')}")
            lines.append(f"  kind: {self.reconstruction.get('kind')}")
            lines.append(f"  {self.reconstruction.get('statement')}")
            missing = self.reconstruction.get("missing_roles") or []
            if missing:
                lines.append(f"  missing roles: {', '.join(missing)}")
            lines.append(
                f"  recomposed summary: {self.reconstruction.get('recomposed_summary')}"
            )
        if self.tuning_export:
            lines.append("")
            te = self.tuning_export
            lines.append("Auto tuning export (control variables for intervention apps)")
            lines.append(f"  domain_book: {te.get('domain_book')}")
            lines.append(f"  auto_assigned: {te.get('auto_assigned')}")
            lines.append("Free / selector controls:")
            controls = te.get("controls") or []
            shown = False
            for c in controls:
                if c.get("status") not in {"free", "protocol_selector"}:
                    continue
                shown = True
                lines.append(
                    f"  - {c.get('name')} [{c.get('status')}] "
                    f"role={c.get('role')}/{c.get('subtype')}: {c.get('why')}"
                )
                lines.append(f"      intervene: {c.get('default_intervention')}")
                if c.get("bridge_app_hint"):
                    lines.append(f"      bridge hint: {c.get('bridge_app_hint')}")
            if not shown:
                lines.append("  (none)")
            fixed = te.get("fixed_structure") or []
            if fixed:
                lines.append("Structural / fixed (do not casually retune):")
                for item in fixed:
                    lines.append(f"  - {item}")
            if te.get("statement"):
                lines.append(str(te["statement"]))
            if te.get("protocol_reminder"):
                lines.append(str(te["protocol_reminder"]))
        if self.incompleteness:
            lines.append("")
            inc = self.incompleteness
            lines.append("Incompleteness / math-complete candidates:")
            lines.append(f"  complete: {inc.get('is_complete')}")
            if inc.get("missing_roles"):
                lines.append(
                    f"  missing roles: {', '.join(inc['missing_roles'])}"
                )
            if inc.get("missing_terms"):
                lines.append(
                    f"  missing terms: {', '.join(inc['missing_terms'])}"
                )
            for c in inc.get("candidates") or []:
                lines.append(
                    f"  - [{c.get('kind')}/{c.get('confidence')}] "
                    f"{c.get('proposal')}"
                )
            if inc.get("equation_sketch"):
                lines.append(f"  book sketch: {inc['equation_sketch']}")
            if inc.get("statement"):
                lines.append(f"  {inc['statement']}")
        if self.decomposition:
            lines.append("")
            dec = self.decomposition
            lines.append("Drill-down + recompose:")
            lines.append(
                f"  book={dec.get('domain_book')} depth={dec.get('depth')} "
                f"terminals={dec.get('terminal_count')} "
                f"recompose_ok={dec.get('all_recompose_ok')}"
            )
            if dec.get("statement"):
                lines.append(f"  {dec['statement']}")
        if self.warnings:
            lines.append("")
            lines.append("Warnings:")
            for warning in self.warnings:
                lines.append(f"  - {warning}")
        if self.notes:
            lines.append("")
            for note in self.notes:
                lines.append(note)
        text = "\n".join(lines)
        cleaned, flags = sanitize_language(text)
        self.language_flags = flags
        return cleaned

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_expression": self.input_expression,
            "highest_evidence_level": int(self.highest_evidence_level),
            "highest_evidence_label": self.highest_evidence_level.label,
            "ast_pretty": self.ast_pretty,
            "role_assignments": self.role_assignments,
            "warnings": self.warnings,
            "confidence": self.confidence.as_dict(),
            "recovery_kind": self.recovery_kind,
            "recovery_statement": self.recovery_statement,
            "poisson_compatibility": self.poisson_compatibility,
            "identifiability": self.identifiability,
            "index_audit": self.index_audit,
            "extra_structures": self.extra_structures,
            "canonical_sfe_status": self.canonical_sfe_status,
            "language_flags": self.language_flags,
            "notes": self.notes,
            "hb_map": self.hb_map,
            "reconstruction": self.reconstruction,
            "tuning_export": self.tuning_export,
            "incompleteness": self.incompleteness,
            "decomposition": self.decomposition,
            "narrative": self.narrative(),
        }
