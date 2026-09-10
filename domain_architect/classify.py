"""Structural role classification.

A familiar symbol name is never sufficient to assign a physical role.
``H`` is not a Hamiltonian, ``P`` is not a prime selector, and ``λ`` is
not automatically a wavelength. Context and tree position contribute;
unresolved roles stay unresolved.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .parser import ASTNode, NodeKind, ParseResult
from .schema import (
    MathType,
    PermissionSubtype,
    ScaleResponseSubtype,
    SOURCE_STATE_WARNING,
)


# Names that must never auto-promote to a physical interpretation.
NAME_GUARD = {
    "H": "H is an identifier. It is not automatically a Hamiltonian or coupling.",
    "P": "P is an identifier. It is not automatically a projector or a prime selector.",
    "lambda": "λ is an identifier. It is not automatically a wavelength or eigenvalue.",
    "Phi": "Φ is an identifier. It is not automatically a gravitational potential.",
    "phi": "φ is an identifier. It is not automatically the golden ratio.",
    "psi": "ψ is an identifier. It is not automatically a quantum state.",
    "S": "S is an identifier. It is not automatically a source.",
}


@dataclass
class RoleAssignment:
    symbol: str
    candidate_role: str
    subtype: str = "unknown"
    math_type: MathType = MathType.UNKNOWN
    confidence: float = 0.0
    justification: str = ""
    name_inferred: bool = False


@dataclass
class Classification:
    assignments: list[RoleAssignment] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    role_classification_confidence: float = 0.0
    definition_completeness: float = 0.0
    source_state_unresolved: bool = False
    scale_ambiguity: bool = False
    extra_structures: list[str] = field(default_factory=list)

    def assignment_for(self, symbol: str) -> RoleAssignment | None:
        for item in self.assignments:
            if item.symbol == symbol:
                return item
        return None


def classify_parse(parsed: ParseResult, context: dict | None = None) -> Classification:
    """Classify from AST structure. ``context`` may supply declared roles."""
    context = context or {}
    result = Classification()
    if parsed.tree is None:
        result.warnings.append("no AST available; classification withheld")
        return result

    symbols = parsed.tree.symbols()
    unique = list(dict.fromkeys(symbols))
    for name in unique:
        if name in NAME_GUARD and name not in context and "roles" not in context:
            result.warnings.append(NAME_GUARD[name])

    # Structural hints only. Never promote a name-only match to a physical law.
    if context.get("domain") == "NS-B" or context.get("fluids_book") == "NS-B":
        _assign_classical_ns(parsed, result, context)
    elif parsed.tree.kind == NodeKind.EQUALITY:
        _classify_equality(parsed.tree, result, context)
    else:
        _classify_term(parsed.tree, result, context, side="expression")

    if not result.assignments:
        result.role_classification_confidence = 0.2
        result.definition_completeness = 0.1
    else:
        declared = sum(1 for a in result.assignments if a.confidence >= 0.6)
        result.role_classification_confidence = min(
            0.85, 0.25 + 0.15 * declared
        )
        result.definition_completeness = min(1.0, declared / max(len(unique), 1))
    return result


def _assign_classical_ns(
    parsed: ParseResult, result: Classification, context: dict
) -> None:
    """Apply the declared classical NS organizational map (Level 0–1)."""
    from .navier_stokes import (
        CLASSICAL_NS_ROLE_MAP,
        DOMAIN_ID,
        NS_EXTRA_STRUCTURES,
        detect_classical_ns,
    )

    detection = detect_classical_ns(parsed.original, parsed)
    form = detection.form or context.get("ns_form", "vorticity")
    result.extra_structures.extend(NS_EXTRA_STRUCTURES)
    result.warnings.append(
        f"Routed to {DOMAIN_ID}: organizational FRA map only; not a "
        "derivation from SFE and not a regularity claim."
    )
    finger_symbols = {
        "P": "P",
        "H": "H",
        "psi": "u" if form in {"velocity", "incompressibility"} else "omega",
        "lambda": "nu",
        "Phi": "p" if form == "velocity" else "Phi",
    }
    for finger, default_symbol in finger_symbols.items():
        meta = CLASSICAL_NS_ROLE_MAP[finger]
        symbol = default_symbol
        present = {s for s in parsed.tree.symbols()}
        if finger == "psi":
            if "omega" in present and form != "velocity":
                symbol = "omega"
            elif "u" in present:
                symbol = "u"
        elif finger == "lambda" and "nu" in present:
            symbol = "nu"
        elif finger == "Phi" and "p" in present:
            symbol = "p"
        result.assignments.append(
            RoleAssignment(
                symbol=symbol,
                candidate_role=meta["candidate_role"],
                subtype=meta["subtype"],
                math_type=MathType(meta["math_type"]),
                confidence=0.7,
                justification=(
                    f"Declared classical NS ({DOMAIN_ID}) organizational map: "
                    f"{meta['label']}."
                ),
            )
        )
    e_meta = CLASSICAL_NS_ROLE_MAP["E"]
    result.assignments.append(
        RoleAssignment(
            symbol="E",
            candidate_role=e_meta["candidate_role"],
            subtype=e_meta["subtype"],
            math_type=MathType.UNKNOWN,
            confidence=0.7,
            justification=f"Extras for {DOMAIN_ID}: {e_meta['label']}.",
        )
    )


def _classify_equality(tree: ASTNode, result: Classification, context: dict) -> None:
    left, right = tree.children
    left_ops = [
        n.name
        for n in left.walk()
        if n.kind in {NodeKind.APPLY, NodeKind.OPERATOR} and n.name
    ]
    if "Laplacian" in left_ops:
        result.extra_structures.extend(["geometry", "boundary", "operator_domain"])
        _assign_poisson_like(left, right, result, context)
        return
    if "dAlembertian" in left_ops or "Box" in left.symbols():
        result.extra_structures.extend(
            ["spacetime geometry", "metric", "gauge", "initial_data"]
        )
        _assign_wave_like(left, right, result, context)
        return
    _classify_term(left, result, context, side="left")
    _classify_term(right, result, context, side="right")


def _assign_poisson_like(
    left: ASTNode, right: ASTNode, result: Classification, context: dict
) -> None:
    left_syms = left.symbols()
    right_syms = [s for s in right.symbols() if s.lower() not in {"pi"}]
    if left_syms:
        result.assignments.append(
            RoleAssignment(
                symbol=left_syms[0],
                candidate_role="realized_output",
                subtype="field",
                math_type=MathType.FIELD,
                confidence=0.7,
                justification=(
                    "Occupies the left-hand side of a Laplacian equation; "
                    "this is a structural candidate for Φ, not a derivation."
                ),
            )
        )
    coupling = [s for s in right_syms if s in {"G", "g"} or s == context.get("coupling")]
    sources = [s for s in right_syms if s.lower() in {"rho", "rho_n", "t"} or s == "rho"]
    if "G" in right_syms:
        result.assignments.append(
            RoleAssignment(
                symbol="G",
                candidate_role="coupling",
                subtype="coupling_constant",
                math_type=MathType.SCALAR,
                confidence=0.55,
                justification=(
                    "Appears as a coefficient on the source side of a Poisson "
                    "equation. Classification uses position, not the letter G."
                ),
            )
        )
    if any(s.lower() == "rho" for s in right_syms):
        rho_name = next(s for s in right_syms if s.lower() == "rho")
        result.assignments.append(
            RoleAssignment(
                symbol=rho_name,
                candidate_role="source",
                subtype="density",
                math_type=MathType.FIELD,
                confidence=0.7,
                justification=(
                    "Occupies the inhomogeneous term of a Laplacian equation. "
                    "Kept as one source/state object unless a decomposition "
                    "rule is supplied."
                ),
            )
        )
        result.source_state_unresolved = "source_state_rule" not in context
        if result.source_state_unresolved:
            result.warnings.append(SOURCE_STATE_WARNING)
    # Scale-response objects implied by the inverse Laplacian, not by λ's name.
    result.assignments.append(
        RoleAssignment(
            symbol="kappa",
            candidate_role="scale_response",
            subtype=ScaleResponseSubtype.SPECTRAL_COORDINATE.value,
            math_type=MathType.SCALAR,
            confidence=0.65,
            justification=(
                "Laplacian eigenmode label κ_n = k_n is a spectral coordinate, "
                "distinct from the inverse-Laplacian response R(κ)=1/κ²."
            ),
        )
    )
    result.assignments.append(
        RoleAssignment(
            symbol="R",
            candidate_role="scale_response",
            subtype=ScaleResponseSubtype.TRANSFER_FUNCTION.value,
            math_type=MathType.OPERATOR,
            confidence=0.65,
            justification=(
                "R_g(κ_n)=1/κ_n² is the spectral response of the inverse "
                "Laplacian. It is not interchangeable with the coordinate κ_n."
            ),
        )
    )
    result.scale_ambiguity = False
    _ = coupling
    _ = sources


def _assign_wave_like(
    left: ASTNode, right: ASTNode, result: Classification, context: dict
) -> None:
    left_syms = left.symbols()
    if left_syms:
        result.assignments.append(
            RoleAssignment(
                symbol=left_syms[0],
                candidate_role="realized_output",
                subtype="metric_perturbation",
                math_type=MathType.TENSOR,
                confidence=0.6,
                justification=(
                    "Left-hand operand of a wave operator. Additional GR "
                    "structure (gauge, metric, constraints) is recorded in E."
                ),
            )
        )
    if any(s.lower() in {"t", "tmunu"} or s.startswith("T") for s in right.symbols()):
        t_name = next(
            (s for s in right.symbols() if s.startswith("T") or s.lower() == "t"),
            "T",
        )
        result.assignments.append(
            RoleAssignment(
                symbol=t_name,
                candidate_role="source",
                subtype="stress_energy",
                math_type=MathType.TENSOR,
                confidence=0.6,
                justification="Inhomogeneous term of a linearized wave equation.",
            )
        )
    result.assignments.append(
        RoleAssignment(
            symbol="D",
            candidate_role="evolution_operator",
            subtype="wave_operator",
            math_type=MathType.OPERATOR,
            confidence=0.7,
            justification="Wave operator declared as an independent role D.",
        )
    )


def _classify_term(
    tree: ASTNode, result: Classification, context: dict, side: str
) -> None:
    if tree.kind == NodeKind.MUL and len(tree.children) == 2:
        left, right = tree.children
        if left.kind == NodeKind.SYMBOL and right.kind == NodeKind.SYMBOL:
            # Juxtaposition such as Hψ: left factor may be a coupling *candidate*
            # but is never promoted to Hamiltonian from the letter H.
            result.assignments.append(
                RoleAssignment(
                    symbol=left.name or "?",
                    candidate_role="unresolved_left_factor",
                    subtype="unknown",
                    math_type=MathType.UNKNOWN,
                    confidence=0.25,
                    justification=(
                        f"Occupies the left factor of a product on the {side} "
                        "side. Structural position is recorded; no physical "
                        "identity is inferred from the symbol name."
                    ),
                )
            )
            result.assignments.append(
                RoleAssignment(
                    symbol=right.name or "?",
                    candidate_role="unresolved_right_factor",
                    subtype="unknown",
                    math_type=MathType.UNKNOWN,
                    confidence=0.25,
                    justification=(
                        "Occupies the right factor of a product. Not inferred "
                        "to be a state vector from the symbol name."
                    ),
                )
            )
            if (left.name or "") == "H":
                result.warnings.append(
                    "Hψ is a product of two identifiers. Domain Architect "
                    "does not declare H a Hamiltonian from this token pattern."
                )
            return
    for node in tree.walk():
        if node.kind == NodeKind.SYMBOL and node.name and node.name not in {
            a.symbol for a in result.assignments
        }:
            declared = context.get("roles", {}).get(node.name)
            result.assignments.append(
                RoleAssignment(
                    symbol=node.name,
                    candidate_role=declared or "unresolved",
                    subtype="unknown",
                    math_type=MathType.UNKNOWN,
                    confidence=0.55 if declared else 0.15,
                    justification=(
                        "Declared in supplied context."
                        if declared
                        else "Symbol present; role withheld pending definition."
                    ),
                )
            )
