"""Analysis-mode entry: DECOMPOSE plus mathematical checks."""

from __future__ import annotations

from typing import Any

import numpy as np

from .checks import (
    GeometryRecord,
    TypeRecord,
    check_types,
    classify_permission,
    decompose_source_state,
    expand_environment,
    ScaleResponseRecord,
    warn_scale_ambiguity,
)
from .decompose import decompose
from .gravity import newtonian_role_map, solve_periodic_poisson
from .identifiability import analyze_product_abx
from .parser import NodeKind
from .recovery import classify_recovery
from .report import AuditReport, ConfidenceTaxonomy
from .schema import (
    EvidenceLevel,
    MathType,
    MathValidationStatus,
    PhysicalValidationStatus,
)


def _looks_like_product_abx(parsed) -> bool:
    if parsed.tree is None or parsed.tree.kind != NodeKind.EQUALITY:
        return False
    left, right = parsed.tree.children
    if (left.name or "").lower() != "y":
        return False
    symbols = [s.lower() for s in right.symbols()]
    return set(symbols) >= {"a", "b", "x"}


def _looks_like_einstein(text: str) -> bool:
    compact = text.replace(" ", "").replace("_", "")
    return "G" in text and ("T" in text) and ("mu" in compact or "ν" in text or "\\mu" in text)


def _looks_like_linearized_gravity(text: str) -> bool:
    return (
        "Box" in text
        or "square" in text.lower()
        or "□" in text
        or "bar h" in text.lower()
        or "barh" in text.replace(" ", "").lower()
    )


def audit_expression(
    expression: str,
    *,
    context: dict[str, Any] | None = None,
    rho: np.ndarray | None = None,
    permission_matrix: np.ndarray | None = None,
    type_records: list[TypeRecord] | None = None,
    geometry: GeometryRecord | None = None,
    scale_records: list[ScaleResponseRecord] | None = None,
) -> AuditReport:
    """Decompose one expression. Does not invent a unified theory."""
    context = dict(context or {})
    dec = decompose(expression, context=context)
    parsed = dec.parsed
    classification = dec.classification
    warnings = list(dec.warnings)
    extra = list(classification.extra_structures)
    evidence = EvidenceLevel.COHERENT_CLASSIFICATION
    recovery_kind = None
    recovery_statement = None
    poisson = None
    ident = None
    notes: list[str] = []
    math_status = MathValidationStatus.NOT_PERFORMED
    phys_status = PhysicalValidationStatus.NONE

    if dec.dimensions is not None:
        if dec.dimensions.consistent is True:
            math_status = MathValidationStatus.PASSED
            evidence = max(evidence, EvidenceLevel.MATHEMATICAL_COMPATIBILITY)
        elif dec.dimensions.consistent is False:
            math_status = MathValidationStatus.FAILED

    if parsed.tree is not None:
        warnings.extend(check_types(type_records or [], parsed.tree))

    if scale_records:
        warnings.extend(warn_scale_ambiguity(scale_records))

    if permission_matrix is not None:
        perm = classify_permission(permission_matrix)
        notes.append(f"Permission object: {perm.label}. {perm.details}")
        if not perm.is_projector:
            warnings.append(
                "Permission object failed P² = P. It is not called a "
                "mathematical projector."
            )

    if classification.source_state_unresolved:
        split = decompose_source_state(rule=context.get("source_state_rule"))
        if split.warning:
            warnings.append(split.warning)

    if parsed.ok and _looks_like_poisson(parsed.tree, expression):
        rec = classify_recovery(
            known_equation_rewritten=True,
            independent_broader_model=False,
            target_theory="Newtonian Poisson gravity",
        )
        recovery_kind = rec.kind.value
        recovery_statement = rec.statement
        evidence = rec.evidence_level
        phys_status = PhysicalValidationStatus.BENCHMARK_REPRESENTATION
        notes.append(newtonian_role_map()["label"])
        extra.extend(["geometry", "boundary", "zero_mode_solvability"])
        if rho is not None:
            solved = solve_periodic_poisson(
                rho,
                mean_policy=context.get("mean_policy", "reject"),
            )
            poisson = {
                "source_mean": solved.compatibility.source_mean,
                "zero_mode_removed": solved.compatibility.zero_mode_removed,
                "mean_subtraction_performed": solved.compatibility.mean_subtraction_performed,
                "potential_gauge": solved.compatibility.potential_gauge,
                "compatible": solved.compatibility.compatible,
                "message": solved.compatibility.message,
                "divided_by_k_squared": solved.divided_by_k_squared,
            }
            warnings.append(solved.compatibility.message)
            if not solved.compatibility.compatible:
                math_status = MathValidationStatus.FAILED
                evidence = EvidenceLevel.COHERENT_CLASSIFICATION

    if _looks_like_product_abx(parsed):
        report = analyze_product_abx(np.array([1.0, 2.0, 3.0]))
        ident = {
            "statement": report.statement,
            "rank": report.rank,
            "locally_full_rank": report.locally_full_rank,
            "global_status": report.global_status,
            "warnings": report.warnings,
            "product_ambiguities": report.product_ambiguities,
        }
        evidence = max(evidence, EvidenceLevel.MATHEMATICAL_COMPATIBILITY)

    if _looks_like_einstein(expression):
        extra.extend(
            [
                "spacetime geometry",
                "metric g_{μν}",
                "curvature",
                "stress-energy T_{μν}",
                "coupling",
                "gauge/diffeomorphism freedom",
                "constraints",
                "initial_data",
            ]
        )
        warnings.append(
            "General relativity is not reduced to a five-component mapping. "
            "Independently necessary structure is recorded explicitly."
        )
        notes.append(
            "Domain Architect may organize GR objects by function; it does not "
            "claim that GR consists of a fixed role list."
        )

    if _looks_like_linearized_gravity(expression):
        extra.extend(["wave operator D", "metric perturbation", "harmonic gauge"])
        notes.append(
            "Linearized gravity example: D = wave operator (state transition), "
            "metric perturbation = state, T = forcing, gauge = constraint."
        )

    if geometry is not None:
        extra.extend(f"{k}={v}" for k, v in expand_environment(geometry).items())

    notes.append("SFE, UHF, DHFA and the Harmonic Blueprint are archived historical reference.")
    notes.append(
        "Functional correspondence is a hypothesis to investigate, not evidence "
        "of physical equivalence."
    )

    role_assignments = []
    for a in classification.assignments:
        payload = {
            "symbol": a.symbol,
            "candidate_role": a.candidate_role,
            "subtype": a.subtype,
            "math_type": a.math_type.value if isinstance(a.math_type, MathType) else a.math_type,
            "confidence": a.confidence,
            "justification": a.justification,
        }
        role_assignments.append(payload)

    report = AuditReport(
        input_expression=expression,
        highest_evidence_level=evidence,
        ast_pretty=parsed.tree.pretty() if parsed.tree is not None else "",
        role_assignments=role_assignments,
        warnings=_unique(warnings),
        confidence=ConfidenceTaxonomy(
            parser_confidence=parsed.parser_confidence,
            role_classification_confidence=classification.role_classification_confidence,
            definition_completeness=classification.definition_completeness,
            mathematical_validation_status=math_status.value,
            physical_validation_status=phys_status.value,
        ),
        recovery_kind=recovery_kind,
        recovery_statement=recovery_statement,
        poisson_compatibility=poisson,
        identifiability=ident,
        extra_structures=_unique(extra),
        architecture_pretty=dec.tree.pretty(),
        pattern=classification.pattern,
        notes=_unique(notes),
    )
    report.narrative()
    return report


def _looks_like_poisson(tree, expression: str) -> bool:
    text = expression.lower()
    if "nabla" in text or "laplacian" in text or "∇" in expression:
        if "rho" in text or "ρ" in expression:
            return True
    if tree is None:
        return False
    ops = [n.name for n in tree.walk() if getattr(n, "name", None)]
    return "Laplacian" in ops and any(s.lower() == "rho" for s in tree.symbols())


def _unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(items))
