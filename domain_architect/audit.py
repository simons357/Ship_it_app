"""Top-level Functional Role Analysis pipeline."""

from __future__ import annotations

from typing import Any

import numpy as np

from .checks import (
    GeometryRecord,
    TypeRecord,
    check_dimensions,
    check_types,
    classify_permission,
    decompose_source_state,
    expand_environment,
    warn_scale_ambiguity,
    ScaleResponseRecord,
)
from .classify import classify_parse
from .gravity import newtonian_fra_map, solve_periodic_poisson
from .identifiability import analyze_product_abx
from .parser import NodeKind, parse_expression
from .recovery import classify_recovery
from .report import AuditReport, ConfidenceTaxonomy
from .track_b_mobius import (
    LOCKED_OPERATOR,
    looks_like_locked_operator,
    quarantined_operator_hit,
    verify_identities,
)
from .route_c import (
    JUNE_OPERATOR,
    ROUTE_C_OPERATOR,
    looks_like_route_c_operator,
    looks_like_superseded_june_route_c,
)
from .schema import (
    CANONICAL_SFE_STATUS,
    EvidenceLevel,
    MathType,
    MathValidationStatus,
    PhysicalValidationStatus,
    RecoveryKind,
    ScaleResponseSubtype,
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
    return "Box" in text or "square" in text.lower() or "□" in text or "bar h" in text.lower() or "barh" in text.replace(" ", "").lower()


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
    """Audit one expression. Does not invent a unified theory."""
    context = dict(context or {})
    parsed = parse_expression(expression)
    classification = classify_parse(parsed, context)
    warnings = list(parsed.warnings) + list(classification.warnings)
    extra = list(classification.extra_structures)
    evidence = EvidenceLevel.COHERENT_CLASSIFICATION
    recovery_kind = None
    recovery_statement = None
    poisson = None
    ident = None
    notes: list[str] = []
    math_status = MathValidationStatus.NOT_PERFORMED
    phys_status = PhysicalValidationStatus.NONE

    if parsed.tree is not None:
        dim = check_dimensions(parsed.tree, context.get("units"))
        warnings.append(dim.message)
        if dim.consistent is True:
            math_status = MathValidationStatus.PASSED
        elif dim.consistent is False:
            math_status = MathValidationStatus.FAILED

        type_warnings = check_types(type_records or [], parsed.tree)
        warnings.extend(type_warnings)

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
        notes.append(newtonian_fra_map()["label"])
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

    track_b = looks_like_locked_operator(expression)
    june = looks_like_superseded_june_route_c(expression)
    route_c = looks_like_route_c_operator(expression)
    quarantine = None if route_c else quarantined_operator_hit(expression)
    if quarantine:
        warnings.append(quarantine)
        notes.append(
            "RH Track B is locked to "
            f"{LOCKED_OPERATOR}. Historical inverse-GCD, positive-GCD, "
            "Route C −1/(2π), and the −1/2 moat are quarantined."
        )
    if june:
        extra.extend(
            [
                "June 2026 Route C poster SUPERSEDED",
                "inverse-GCD 1/gcd is not the live Route C operator",
                "RH_Riemann_final.tex / zenodo.20518388 archive",
            ]
        )
        notes.append(
            f"SUPERSEDED: June 2026 inverse-GCD poster {JUNE_OPERATOR}. "
            "Same family as RH_Riemann_final.tex. DOI 10.5281/zenodo.20518388 is archive."
        )
        notes.append(
            f"Use the August face instead: {ROUTE_C_OPERATOR} "
            "at /faces/05_route_c_conditional.pdf (DOI 10.5281/zenodo.22050963)."
        )
        notes.append(
            "Withdrawn on this operator: RH ⇔ λ_min/log N → -1/(2π), "
            "Ring Lemma / V_N* locked rows, and κ* = 6/π² as an RH floor. "
            "RH is not claimed. Not ChatVault."
        )
    if route_c:
        extra.extend(
            [
                "Route C exploratory face (not RH Track B)",
                "normalized inverse-GCD 1/(gcd √ij)",
                "Gap A and Gap B open",
            ]
        )
        notes.append(
            f"Route C operator locked: {ROUTE_C_OPERATOR}. "
            "August 2026 conditional preprint. PDF at /faces/05_route_c_conditional.pdf."
        )
        notes.append(
            "Gaps A and B remain open. Numerics are not theorems. "
            "RH is not claimed. This face is not ChatVault."
        )
        notes.append(
            "Do not import this operator or the −1/(2π) limit into RH Track B."
        )
    if track_b:
        extra.extend(
            [
                "RH Track B Möbius–GCD (not NS vorticity Track B)",
                "cubefree rank-one channels h(d) u_d u_d^T",
                "Littlewood–Mertens realization (not assumed)",
            ]
        )
        check = verify_identities(12)
        if check.ok:
            math_status = MathValidationStatus.PASSED
            evidence = max(evidence, EvidenceLevel.MATHEMATICAL_COMPATIBILITY)
            notes.append(
                f"Finite identities hold at N={check.n}: cubefree decomposition, "
                "first-row M(N)=e_1^T Q μ, and the quadratic split. These are "
                "algebraic. They are not RH."
            )
        else:
            math_status = MathValidationStatus.FAILED
            warnings.append(f"RH Track B identity check failed at N={check.n}.")
        notes.append(
            "Missing bridge: Track B operator control does not yet imply "
            "|M(N)|=O_ε(N^{1/2+ε}). First-row Hölder and the Q-form dual are "
            "obstructions. RH is not claimed."
        )
        notes.append(
            "This book is not classical NS Track B, SND, GNC, Goldbach, or "
            "the Harmonic Blueprint."
        )

    if (not track_b) and _looks_like_einstein(expression):
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
            "Independently necessary structure is recorded in E."
        )
        notes.append(
            "Functional Role Analysis may organize GR objects; it does not "
            "imply that GR consists of exactly P, H, ψ, λ, Φ."
        )

    if _looks_like_linearized_gravity(expression):
        extra.extend(["wave operator D", "metric perturbation", "harmonic gauge"])
        notes.append(
            "Linearized gravity FRA example: D = wave operator, Φ = metric "
            "perturbation, S = stress-energy, H = coupling, P or B = "
            "gauge/admissibility. Additional roles are declared, not hidden."
        )

    if geometry is not None:
        extra.extend(f"{k}={v}" for k, v in expand_environment(geometry).items())

    notes.append(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
    notes.append(
        "HB, UHF, SFE, and DHFA remain research constructs. Their status is "
        "determined by audit, not assumed in advance."
    )

    report = AuditReport(
        input_expression=expression,
        highest_evidence_level=evidence,
        ast_pretty=parsed.tree.pretty() if parsed.tree is not None else "",
        role_assignments=[a.__dict__ | {"math_type": a.math_type.value} for a in classification.assignments],
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
        canonical_sfe_status=CANONICAL_SFE_STATUS,
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
