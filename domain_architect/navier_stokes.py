"""Classical Navier–Stokes (Track B) organizational FRA router.

Five-finger roles here are a translator / organizational map for unaugmented
classical NS. This module does not claim regularity, Clay/Millennium closure,
or derivation of NS from an SFE. Gravity already has a representation-recovery
path; NS routing stops at Level 0–1 organizational classification.
"""

from __future__ import annotations

from dataclasses import dataclass

from .parser import ASTNode, NodeKind, ParseResult
from .schema import (
    CANONICAL_SFE_STATUS,
    EvidenceLevel,
    MathType,
    REPRESENTATION_NOT_DERIVATION,
)


DOMAIN_ID = "NS-B"
BOOK_LABEL = "Track B classical Navier–Stokes book"

# Provisional Level 0–1 organizational map (not a Theory of Everything).
CLASSICAL_NS_ROLE_MAP: dict[str, dict[str, str]] = {
    "P": {
        "candidate_role": "admissibility",
        "subtype": "leray_projector",
        "label": "admissible / divergence-free (Leray projector)",
        "math_type": MathType.OPERATOR.value,
    },
    "H": {
        "candidate_role": "interaction",
        "subtype": "nonlinear_advection",
        "label": "nonlinear advection / vortex stretching interaction",
        "math_type": MathType.OPERATOR.value,
    },
    "psi": {
        "candidate_role": "state",
        "subtype": "velocity_or_vorticity",
        "label": "velocity (or vorticity) state",
        "math_type": MathType.FIELD.value,
    },
    "lambda": {
        "candidate_role": "scale_response",
        "subtype": "viscosity",
        "label": "viscosity / dissipative scale ν",
        "math_type": MathType.SCALAR.value,
    },
    "Phi": {
        "candidate_role": "realized_output",
        "subtype": "observed_response",
        "label": "observed response (pressure, strain, enstrophy production)",
        "math_type": MathType.FIELD.value,
    },
    "E": {
        "candidate_role": "environment",
        "subtype": "fluids_extras",
        "label": "domain R^3, IC/BC, Biot–Savart",
        "math_type": MathType.UNKNOWN.value,
    },
}

NS_EXTRA_STRUCTURES = (
    "domain R^3",
    "initial_conditions",
    "boundary_conditions",
    "Biot-Savart reconstruction",
    "incompressibility constraint",
)

NS_SCOPE_STATEMENT = (
    "Organizational Functional Role Analysis of classical Navier–Stokes "
    f"({DOMAIN_ID}). Roles are a translator for the {BOOK_LABEL}; they are "
    "not a Theory of Everything and do not derive NS from a canonical SFE."
)

NS_NO_MILLENNIUM = (
    "Track B classical NS book only. No Millennium / Clay regularity claim "
    "and no SFE-glue language."
)


@dataclass(frozen=True)
class NSDetection:
    matched: bool
    form: str  # "vorticity" | "velocity" | "incompressibility" | ""
    reasons: tuple[str, ...]


def classical_ns_fra_map() -> dict[str, str]:
    """Declared fluids organizational map for audit context / tests."""
    return {
        "domain": DOMAIN_ID,
        "book": BOOK_LABEL,
        "recovery_kind": "none",
        "label": NS_SCOPE_STATEMENT,
        "statement": (
            "Classical NS is routed as a separate book. "
            f"Canonical SFE status: {CANONICAL_SFE_STATUS}."
        ),
        "evidence_level": str(int(EvidenceLevel.COHERENT_CLASSIFICATION)),
        "canonical_sfe_used": "false",
        "P": CLASSICAL_NS_ROLE_MAP["P"]["label"],
        "H": CLASSICAL_NS_ROLE_MAP["H"]["label"],
        "psi": CLASSICAL_NS_ROLE_MAP["psi"]["label"],
        "lambda": CLASSICAL_NS_ROLE_MAP["lambda"]["label"],
        "Phi": CLASSICAL_NS_ROLE_MAP["Phi"]["label"],
        "E": CLASSICAL_NS_ROLE_MAP["E"]["label"],
        # Coupled-pair reminder from the frozen reconstruction checkpoint.
        "coupled_pair": "H <-> psi (resonance/coupling <-> coherence/phase)",
        "mechanism_sketch": "P, lambda configure; H psi -> Phi",
        "note": REPRESENTATION_NOT_DERIVATION.replace(
            "Newtonian Poisson solution",
            "classical Navier–Stokes equations",
        ),
    }


def declared_fluids_roles() -> dict[str, str]:
    """Symbol → role name suitable for classify_parse context['roles']."""
    return {
        "P": CLASSICAL_NS_ROLE_MAP["P"]["candidate_role"],
        "H": CLASSICAL_NS_ROLE_MAP["H"]["candidate_role"],
        "psi": CLASSICAL_NS_ROLE_MAP["psi"]["candidate_role"],
        "lambda": CLASSICAL_NS_ROLE_MAP["lambda"]["candidate_role"],
        "Phi": CLASSICAL_NS_ROLE_MAP["Phi"]["candidate_role"],
        "nu": CLASSICAL_NS_ROLE_MAP["lambda"]["candidate_role"],
        "u": CLASSICAL_NS_ROLE_MAP["psi"]["candidate_role"],
        "omega": CLASSICAL_NS_ROLE_MAP["psi"]["candidate_role"],
        "p": CLASSICAL_NS_ROLE_MAP["Phi"]["candidate_role"],
    }


def _op_names(tree: ASTNode | None) -> set[str]:
    if tree is None:
        return set()
    names: set[str] = set()
    for node in tree.walk():
        if node.kind in {NodeKind.APPLY, NodeKind.OPERATOR} and node.name:
            names.add(node.name)
    return names


def _symbol_names(tree: ASTNode | None) -> set[str]:
    if tree is None:
        return set()
    return {s.lower() for s in tree.symbols()}


def detect_classical_ns(
    expression: str,
    parsed: ParseResult | None = None,
) -> NSDetection:
    """Heuristic detection of classical (unaugmented) NS forms."""
    text = expression.lower()
    compact = (
        text.replace(" ", "")
        .replace("_", "")
        .replace("\\", "")
        .replace("{", "")
        .replace("}", "")
    )
    reasons: list[str] = []
    tree = parsed.tree if parsed is not None else None
    ops = _op_names(tree)
    syms = _symbol_names(tree)

    has_div_free = (
        "Divergence" in ops
        or "nabla·u=0" in compact
        or "nabla*u=0" in compact
        or "divu=0" in compact
        or "∇·u=0" in expression.replace(" ", "")
    )
    has_viscosity = (
        "nu" in syms
        or "ν" in expression
        or "laplacian" in ops
        or "Laplacian" in ops
        or "delta" in compact
        or "Δ" in expression
    )
    has_vorticity = "omega" in syms or "ω" in expression
    has_velocity = "u" in syms
    has_pressure = (
        "Gradient" in ops and ("p" in syms or "pressure" in text)
    ) or ("gradp" in compact) or ("nablap" in compact) or ("∇p" in expression)
    has_advection = (
        ("u" in syms and "nabla" in {s.lower() for s in (tree.symbols() if tree else [])})
        or "u·nabla" in compact
        or "u*nabla" in compact
        or "(u·∇)" in expression
        or "(u*nabla)" in compact
        or "vortex" in text
        or ("omega" in syms and "nabla" in text)
    )
    has_time = (
        "Partial" in ops
        or "partial" in text
        or "∂" in expression
        or "dt" in compact
    )

    # Augmented Track A markers — still NS family, but not classical NS-B.
    augmented = (
        "varepsilon" in compact
        or "epsilon^" in compact
        or "ε" in expression
        or "|nabla u|" in text
        or "lvertnablau" in compact
    )

    if augmented:
        return NSDetection(
            matched=False,
            form="",
            reasons=("augmented / Track A markers present; not routed as NS-B",),
        )

    if has_vorticity and has_viscosity and (has_advection or has_time):
        reasons.append("vorticity transport with viscous Laplacian")
        if has_div_free:
            reasons.append("incompressibility constraint present")
        return NSDetection(True, "vorticity", tuple(reasons))

    if has_velocity and has_viscosity and (has_pressure or has_advection) and has_time:
        reasons.append("velocity NS form with viscosity")
        if has_pressure:
            reasons.append("pressure gradient present")
        return NSDetection(True, "velocity", tuple(reasons))

    if has_div_free and has_velocity and not has_vorticity:
        # Standalone incompressibility still belongs to the classical NS book.
        reasons.append("divergence-free constraint for velocity")
        return NSDetection(True, "incompressibility", tuple(reasons))

    # Textual fallback when the AST is weak but classical NS tokens are clear.
    textual_vorticity = (
        ("omega" in compact or "ω" in expression)
        and ("nu" in compact or "ν" in expression)
        and ("delta" in compact or "Δ" in expression or "laplacian" in compact)
    )
    textual_velocity = (
        ("partial" in compact or "∂" in expression)
        and ("nu" in compact or "ν" in expression)
        and ("nabla p" in text or "∇p" in expression or "grad p" in text)
    )
    if textual_vorticity:
        return NSDetection(
            True,
            "vorticity",
            ("textual classical vorticity NS tokens",),
        )
    if textual_velocity:
        return NSDetection(
            True,
            "velocity",
            ("textual classical velocity NS tokens",),
        )

    return NSDetection(False, "", ())


def ns_role_assignments(form: str) -> list[dict]:
    """Build organizational role assignment dicts from the declared fluids map."""
    assignments: list[dict] = []
    finger_order = ("P", "H", "psi", "lambda", "Phi")
    for finger in finger_order:
        meta = CLASSICAL_NS_ROLE_MAP[finger]
        symbol = {
            "P": "P",
            "H": "H",
            "psi": "u" if form in {"velocity", "incompressibility"} else "omega",
            "lambda": "nu",
            "Phi": "p" if form == "velocity" else "Phi",
        }[finger]
        assignments.append(
            {
                "symbol": symbol,
                "finger": finger,
                "candidate_role": meta["candidate_role"],
                "subtype": meta["subtype"],
                "math_type": meta["math_type"],
                "confidence": 0.7,
                "justification": (
                    f"Declared classical NS ({DOMAIN_ID}) organizational map: "
                    f"{meta['label']}. Structural book routing only; not a "
                    "physical derivation."
                ),
                "name_inferred": False,
            }
        )
    # Environment extras are recorded as E, not as a fifth equality symbol.
    e_meta = CLASSICAL_NS_ROLE_MAP["E"]
    assignments.append(
        {
            "symbol": "E",
            "finger": "E",
            "candidate_role": e_meta["candidate_role"],
            "subtype": e_meta["subtype"],
            "math_type": e_meta["math_type"],
            "confidence": 0.7,
            "justification": (
                f"Independently necessary structures for {DOMAIN_ID}: "
                f"{e_meta['label']}."
            ),
            "name_inferred": False,
        }
    )
    return assignments
