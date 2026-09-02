"""Structural role classification for Domain Architect v1.0.

A familiar symbol name is never sufficient to assign a physical identity.
``H`` is not a Hamiltonian, ``P`` is not a prime selector, and ``λ`` is
not automatically a wavelength. Context and tree position contribute;
unresolved roles stay unresolved. Ambiguous assignments are retained.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .parser import (
    ASTNode,
    NodeKind,
    ParseResult,
    derivative_base,
    derivative_order,
    flatten_sum,
)
from .lab_cases import (
    BOTH_BOOKS_WARNING,
    Q6_HN_WARNINGS,
    RING_SND_WARNINGS,
    SIMPLEX_LEFTOVER_WARNINGS,
    SWIRL_LEFTOVER_WARNINGS,
    tokens_look_like_q6_hn,
    tokens_look_like_ring_snd,
    tokens_look_like_simplex_leftover,
    tokens_look_like_swirl_leftover,
)
from .schema import FunctionalRole, MathType, SOURCE_STATE_WARNING
from .signature import FunctionalSignature, RoleHypothesis


# Names that must never auto-promote to a physical interpretation.
NAME_GUARD = {
    "H": "H is an identifier. It is not automatically a Hamiltonian or coupling.",
    "HN": "H_N is an identifier. It is not FRA coupling H and not a Hamiltonian.",
    "P": "P is an identifier. It is not automatically a projector or a prime selector.",
    "lambda": "λ is an identifier. It is not automatically a wavelength or eigenvalue.",
    "Phi": "Φ is an identifier. It is not automatically a gravitational potential.",
    "phi": "φ is an identifier. It is not automatically the golden ratio.",
    "psi": "ψ is an identifier. It is not automatically a quantum state.",
    "S": "S is an identifier. It is not automatically a source.",
}


@dataclass
class RoleAssignment:
    """Backward-compatible view of a RoleHypothesis."""

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
    hypotheses: list[RoleHypothesis] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    role_classification_confidence: float = 0.0
    definition_completeness: float = 0.0
    source_state_unresolved: bool = False
    scale_ambiguity: bool = False
    extra_structures: list[str] = field(default_factory=list)
    pattern: str = "unclassified"

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
        if name in NAME_GUARD and name not in context:
            result.warnings.append(NAME_GUARD[name])

    if parsed.tree.kind == NodeKind.EQUALITY:
        _classify_equality(parsed.tree, result, context)
    else:
        _classify_term(parsed.tree, result, context, side="expression")

    if not result.assignments:
        result.role_classification_confidence = 0.2
        result.definition_completeness = 0.1
    else:
        declared = sum(1 for a in result.assignments if a.confidence >= 0.6)
        result.role_classification_confidence = min(0.85, 0.25 + 0.15 * declared)
        result.definition_completeness = min(1.0, declared / max(len(unique), 1))
    result.warnings.extend(_book_collision_warnings(parsed.tokens))
    return result


def _book_collision_warnings(tokens: list[str]) -> list[str]:
    """Name the book a lab string belongs to. Do not glue books."""
    warnings: list[str] = []
    ring = tokens_look_like_ring_snd(tokens)
    q6 = tokens_look_like_q6_hn(tokens)
    swirl_left = tokens_look_like_swirl_leftover(tokens)
    simplex = tokens_look_like_simplex_leftover(tokens)
    if ring:
        warnings.extend(RING_SND_WARNINGS)
    if q6:
        warnings.append(Q6_HN_WARNINGS[0])
        if "D" in set(tokens):
            warnings.append(Q6_HN_WARNINGS[1])
    if swirl_left:
        warnings.extend(SWIRL_LEFTOVER_WARNINGS)
    if simplex:
        warnings.extend(SIMPLEX_LEFTOVER_WARNINGS)
    n_books = sum([ring, q6, swirl_left, simplex])
    if ring and q6:
        warnings.append(BOTH_BOOKS_WARNING)
    elif n_books >= 2:
        warnings.append(
            "These tokens mix leftover books. Do not glue them. "
            "A shared concentration shape is not a structure map T."
        )
    return warnings


def _add(
    result: Classification,
    symbol: str,
    role: FunctionalRole,
    *,
    confidence: float,
    rationale: str,
    math_type: MathType = MathType.UNKNOWN,
    subtype: str = "unknown",
    domain: str = "unspecified",
    codomain: str = "unspecified",
    symmetry: frozenset[str] | None = None,
    constraints: frozenset[str] | None = None,
    alternate: list[str] | None = None,
) -> None:
    sig = FunctionalSignature(
        role=role,
        math_type=math_type,
        domain=domain,
        codomain=codomain,
        symmetry=symmetry or frozenset(),
        constraints=constraints or frozenset(),
    )
    result.hypotheses.append(
        RoleHypothesis(
            symbol=symbol,
            role=role,
            confidence=confidence,
            rationale=rationale,
            signature=sig,
            subtype=subtype,
            alternate_roles=alternate or [],
        )
    )
    result.assignments.append(
        RoleAssignment(
            symbol=symbol,
            candidate_role=role.value,
            subtype=subtype,
            math_type=math_type,
            confidence=confidence,
            justification=rationale,
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
        result.pattern = "elliptic_poisson"
        _assign_poisson_like(left, right, result, context)
        return
    if "dAlembertian" in left_ops or "Box" in left.symbols():
        result.extra_structures.extend(
            ["spacetime geometry", "metric", "gauge", "initial_data"]
        )
        result.pattern = "hyperbolic_wave"
        _assign_wave_like(left, right, result, context)
        return
    if _looks_like_second_order_ode(tree):
        result.pattern = "second_order_linear_ode"
        _assign_second_order_ode(tree, result, context)
        return
    _classify_term(left, result, context, side="left")
    _classify_term(right, result, context, side="right")


def _looks_like_second_order_ode(tree: ASTNode) -> bool:
    if tree.kind != NodeKind.EQUALITY:
        return False
    orders = [
        derivative_order(n)
        for n in tree.walk()
        if n.kind == NodeKind.DERIVATIVE
    ]
    return max(orders, default=0) >= 1


def _term_coeff_and_state(term: ASTNode) -> tuple[list[str], str | None, int]:
    """Return (coefficient symbols, state symbol, derivative order) for a term."""
    if term.kind == NodeKind.DERIVATIVE:
        return [], derivative_base(term), derivative_order(term)
    if term.kind == NodeKind.SYMBOL:
        return [], term.name, 0
    if term.kind == NodeKind.NUMBER:
        return [], None, 0
    if term.kind == NodeKind.MUL:
        coeffs: list[str] = []
        state = None
        order = 0
        for child in term.children:
            if child.kind == NodeKind.DERIVATIVE:
                state = derivative_base(child)
                order = max(order, derivative_order(child))
            elif child.kind == NodeKind.SYMBOL:
                if state is None and order == 0 and not coeffs:
                    # first symbol may be either coeff or state; decided later
                    coeffs.append(child.name or "?")
                else:
                    coeffs.append(child.name or "?")
            elif child.kind == NodeKind.NUMBER:
                continue
            else:
                nested_c, nested_s, nested_o = _term_coeff_and_state(child)
                coeffs.extend(nested_c)
                if nested_s:
                    state = nested_s
                order = max(order, nested_o)
        if state is None and coeffs:
            # last identifier is treated as the undifferentiated state
            state = coeffs.pop()
        return coeffs, state, order
    return [], derivative_base(term), derivative_order(term)


def _assign_second_order_ode(
    tree: ASTNode, result: Classification, context: dict
) -> None:
    left, right = tree.children
    terms = flatten_sum(left)
    by_order: dict[int, list[tuple[list[str], str | None]]] = {}
    for _sign, term in terms:
        coeffs, state, order = _term_coeff_and_state(term)
        by_order.setdefault(order, []).append((coeffs, state))

    states = [
        state
        for items in by_order.values()
        for _c, state in items
        if state
    ]
    state_name = states[0] if states else "x"
    _add(
        result,
        state_name,
        FunctionalRole.STATE,
        confidence=0.8,
        rationale=(
            "Appears as the differentiated unknown of a time-evolution "
            "equation. This is the DA state x(t), not a physical identity "
            "inferred from the letter."
        ),
        math_type=MathType.SCALAR,
        subtype="dynamic_state",
        domain="time",
        codomain="state_space",
        symmetry=frozenset({"lumped"}),
    )

    order_roles = {
        2: (
            FunctionalRole.STATE_TRANSITION,
            "inertia",
            "Coefficient of the second time derivative: structural candidate "
            "for an inertial / state-transition mechanism.",
        ),
        1: (
            FunctionalRole.DISSIPATION,
            "linear_damping",
            "Coefficient of the first time derivative: structural candidate "
            "for a dissipative mechanism. Alternate hypothesis: gyroscopic "
            "or transport term.",
        ),
        0: (
            FunctionalRole.INTERACTION,
            "restoring",
            "Undifferentiated state term: structural candidate for a "
            "restoring / interaction mechanism.",
        ),
    }
    for order, (role, subtype, rationale) in order_roles.items():
        for coeffs, _state in by_order.get(order, []):
            if not coeffs:
                continue
            symbol = coeffs[0]
            alternate = ["transport"] if order == 1 else []
            _add(
                result,
                symbol,
                role,
                confidence=0.72 if order else 0.68,
                rationale=rationale,
                math_type=MathType.SCALAR,
                subtype=subtype,
                domain="state_space",
                codomain="force_like",
                symmetry=frozenset({"linear", "time_invariant"}),
                alternate=alternate,
            )

    rhs_syms = [
        s
        for s in right.symbols()
        if s != state_name and s.lower() not in {"pi"}
    ]
    # Derivative symbols on the right are still the same state.
    if right.kind == NodeKind.NUMBER and right.value == 0:
        result.warnings.append(
            "Homogeneous right-hand side. No independent forcing role was "
            "identified; a missing forcing mechanism remains a live hypothesis "
            "if observations are biased."
        )
    elif rhs_syms:
        _add(
            result,
            rhs_syms[0],
            FunctionalRole.FORCING,
            confidence=0.7,
            rationale=(
                "Occupies the inhomogeneous term of the evolution equation. "
                "Structural candidate for forcing / control input u(t)."
            ),
            math_type=MathType.SCALAR,
            subtype="input",
            domain="time",
            codomain="force_like",
        )
    result.extra_structures.extend(["time", "initial_data", "causality"])
    _ = context


def _assign_poisson_like(
    left: ASTNode, right: ASTNode, result: Classification, context: dict
) -> None:
    left_syms = left.symbols()
    right_syms = [s for s in right.symbols() if s.lower() not in {"pi"}]
    if left_syms:
        _add(
            result,
            left_syms[0],
            FunctionalRole.STATE,
            confidence=0.7,
            rationale=(
                "Occupies the left-hand side of an elliptic equation. "
                "Structural candidate for the realized field / state, "
                "not a derivation of gravity."
            ),
            math_type=MathType.FIELD,
            subtype="potential_field",
            domain="geometry",
            codomain="scalars_on_geometry",
            constraints=frozenset({"elliptic", "boundary_value"}),
            alternate=["output"],
        )
    _add(
        result,
        "Laplacian",
        FunctionalRole.CONSTRAINT,
        confidence=0.75,
        rationale=(
            "The Laplacian is an elliptic operator. In DA it is a constraint "
            "/ state-transition mechanism relating a field to its source, "
            "not a universal field equation."
        ),
        math_type=MathType.OPERATOR,
        subtype="elliptic_operator",
        domain="H^2",
        codomain="L2",
        symmetry=frozenset({"self_adjoint", "translation_on_R_n"}),
        alternate=["state_transition"],
    )
    if "G" in right_syms:
        _add(
            result,
            "G",
            FunctionalRole.INTERACTION,
            confidence=0.55,
            rationale=(
                "Appears as a coefficient on the source side of a Poisson "
                "equation. Classification uses position, not the letter G."
            ),
            math_type=MathType.SCALAR,
            subtype="coupling_constant",
            domain="source",
            codomain="source",
        )
    if any(s.lower() == "rho" for s in right_syms):
        rho_name = next(s for s in right_syms if s.lower() == "rho")
        _add(
            result,
            rho_name,
            FunctionalRole.FORCING,
            confidence=0.7,
            rationale=(
                "Occupies the inhomogeneous term of an elliptic equation. "
                "Kept as one source object unless a decomposition rule is "
                "supplied."
            ),
            math_type=MathType.FIELD,
            subtype="density",
            domain="geometry",
            codomain="scalars_on_geometry",
        )
        result.source_state_unresolved = "source_state_rule" not in context
        if result.source_state_unresolved:
            result.warnings.append(SOURCE_STATE_WARNING)
    result.extra_structures.extend(["geometry", "boundary", "zero_mode_solvability"])


def _assign_wave_like(
    left: ASTNode, right: ASTNode, result: Classification, context: dict
) -> None:
    left_syms = left.symbols()
    if left_syms:
        _add(
            result,
            left_syms[0],
            FunctionalRole.STATE,
            confidence=0.6,
            rationale=(
                "Left-hand operand of a wave operator. Additional geometric "
                "structure (gauge, metric, constraints) is recorded separately."
            ),
            math_type=MathType.TENSOR,
            subtype="metric_perturbation",
            alternate=["output"],
        )
    if any(s.lower() in {"t", "tmunu"} or s.startswith("T") for s in right.symbols()):
        t_name = next(
            (s for s in right.symbols() if s.startswith("T") or s.lower() == "t"),
            "T",
        )
        _add(
            result,
            t_name,
            FunctionalRole.FORCING,
            confidence=0.6,
            rationale="Inhomogeneous term of a linearized wave equation.",
            math_type=MathType.TENSOR,
            subtype="stress_energy",
        )
    _add(
        result,
        "D",
        FunctionalRole.STATE_TRANSITION,
        confidence=0.7,
        rationale="Wave operator declared as an independent evolution mechanism.",
        math_type=MathType.OPERATOR,
        subtype="wave_operator",
        domain="spacetime fields",
        codomain="spacetime fields",
        symmetry=frozenset({"hyperbolic"}),
    )


def _classify_term(
    tree: ASTNode, result: Classification, context: dict, side: str
) -> None:
    if tree.kind == NodeKind.MUL and len(tree.children) == 2:
        left, right = tree.children
        if left.kind == NodeKind.SYMBOL and right.kind == NodeKind.SYMBOL:
            _add(
                result,
                left.name or "?",
                FunctionalRole.UNRESOLVED,
                confidence=0.25,
                rationale=(
                    f"Occupies the left factor of a product on the {side} "
                    "side. Structural position is recorded; no physical "
                    "identity is inferred from the symbol name."
                ),
                subtype="unresolved_left_factor",
                alternate=["interaction"],
            )
            # Keep the historical candidate_role string for Test A.
            result.assignments[-1].candidate_role = "unresolved_left_factor"
            _add(
                result,
                right.name or "?",
                FunctionalRole.UNRESOLVED,
                confidence=0.25,
                rationale=(
                    "Occupies the right factor of a product. Not inferred "
                    "to be a state vector from the symbol name."
                ),
                subtype="unresolved_right_factor",
                alternate=["state"],
            )
            result.assignments[-1].candidate_role = "unresolved_right_factor"
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
            role = FunctionalRole(declared) if declared in {r.value for r in FunctionalRole} else (
                FunctionalRole.UNRESOLVED
            )
            if declared and declared not in {r.value for r in FunctionalRole}:
                role = FunctionalRole.UNRESOLVED
            _add(
                result,
                node.name,
                role if declared else FunctionalRole.UNRESOLVED,
                confidence=0.55 if declared else 0.15,
                rationale=(
                    "Declared in supplied context."
                    if declared
                    else "Symbol present; role withheld pending definition."
                ),
                subtype=declared or "unknown",
            )
            if not declared:
                result.assignments[-1].candidate_role = "unresolved"
