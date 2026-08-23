"""Evidence-aware report generation and language enforcement."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from .schema import (
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
         "represents the Newtonian Poisson equation using functional roles"),
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
    architecture_pretty: str = ""
    pattern: str = ""
    language_flags: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def narrative(self) -> str:
        lines = [
            "Domain Architect — Functional Role Decomposition",
            "",
            PRODUCT_DESCRIPTION,
            "",
            f"Primary operations: {ORGANIZING_GRAMMAR}",
            f"Highest evidence level actually supported: {self.highest_evidence_level.label}",
            "",
            f"Input: {self.input_expression}",
        ]
        if self.pattern:
            lines.extend(["", f"Detected pattern: {self.pattern}"])
        lines.extend(
            [
                "",
                "Abstract syntax tree:",
                self.ast_pretty or "(unparsed)",
            ]
        )
        if self.architecture_pretty:
            lines.extend(["", "Functional architecture:", self.architecture_pretty])
        lines.extend(
            [
                "",
                "Role assignments (role + confidence + rationale):",
            ]
        )
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
                "Independently necessary structures: " + ", ".join(self.extra_structures)
            )
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
            "architecture_pretty": self.architecture_pretty,
            "pattern": self.pattern,
            "role_assignments": self.role_assignments,
            "warnings": self.warnings,
            "confidence": self.confidence.as_dict(),
            "recovery_kind": self.recovery_kind,
            "recovery_statement": self.recovery_statement,
            "poisson_compatibility": self.poisson_compatibility,
            "identifiability": self.identifiability,
            "index_audit": self.index_audit,
            "extra_structures": self.extra_structures,
            "language_flags": self.language_flags,
            "notes": self.notes,
            "narrative": self.narrative(),
        }
