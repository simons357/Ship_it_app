"""TRANSLATE: cross-domain functional and mathematical correspondence."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .compatibility import CompatibilityReport, Transformation, classify_compatibility
from .decompose import Decomposition, decompose
from .schema import CompatibilityClass, CorrespondenceKind, FunctionalRole
from .signature import FunctionalSignature


@dataclass
class TranslationRecord:
    """T = (mapping, preserved, broken, assumptions, confidence)."""

    left_name: str
    right_name: str
    mapping: dict[str, str]
    preserved: list[str]
    broken: list[str]
    assumptions: list[str]
    confidence: float
    kind: CorrespondenceKind
    compatibility: list[CompatibilityReport] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "left": self.left_name,
            "right": self.right_name,
            "mapping": dict(self.mapping),
            "preserved": list(self.preserved),
            "broken": list(self.broken),
            "assumptions": list(self.assumptions),
            "confidence": self.confidence,
            "kind": self.kind.value,
            "compatibility": [c.to_dict() for c in self.compatibility],
            "notes": list(self.notes),
        }


# Mechanical force vs electrical voltage in SI base (M, L, T, I, Θ, N, J).
_FORCE: tuple[int, ...] = (1, 1, -2, 0, 0, 0, 0)
_VOLTAGE: tuple[int, ...] = (1, 2, -3, -1, 0, 0, 0)
_MASS: tuple[int, ...] = (1, 0, 0, 0, 0, 0, 0)
_INDUCTANCE: tuple[int, ...] = (1, 2, -2, -2, 0, 0, 0)
_DAMPING: tuple[int, ...] = (1, 0, -1, 0, 0, 0, 0)
_RESISTANCE: tuple[int, ...] = (1, 2, -3, -2, 0, 0, 0)
_STIFFNESS: tuple[int, ...] = (1, 0, -2, 0, 0, 0, 0)
_ELASTANCE: tuple[int, ...] = (1, 2, -4, -2, 0, 0, 0)  # 1/C


MECHANICAL_ELECTRICAL_MAP = {
    "x": "q",
    "xd": "i",
    "m": "L",
    "c": "R",
    "k": "1/C",
    "f": "v",
}


def translate(left: Decomposition, right: Decomposition) -> TranslationRecord:
    """Search for functional/mathematical correspondences between two architectures."""
    if (
        left.classification.pattern == "second_order_linear_ode"
        and right.classification.pattern == "second_order_linear_ode"
    ):
        return _translate_second_order(left, right)
    return _translate_generic(left, right)


def translate_expressions(
    left_expr: str,
    right_expr: str,
    *,
    left_name: str | None = None,
    right_name: str | None = None,
) -> TranslationRecord:
    return translate(
        decompose(left_expr, name=left_name),
        decompose(right_expr, name=right_name),
    )


def mechanical_electrical_translation() -> TranslationRecord:
    """Canonical TRANSFORMABLE pair used as the first cross-domain test."""
    left = decompose("m*xdd + c*xd + k*x = f", name="mechanical_oscillator")
    right = decompose("L*qdd + R*qd + kC*q = v", name="series_rlc")
    record = translate(left, right)
    record.mapping = dict(MECHANICAL_ELECTRICAL_MAP)
    record.mapping["kC"] = "k → 1/C (elastance)"
    record.assumptions = [
        "lumped elements",
        "linear time-invariant",
        "through/across variable analogy (force–voltage)",
    ]
    record.notes.append(
        "SI dimensions of force and voltage differ. The map is legal only "
        "as a structure-preserving transformation, not as a unit-preserving "
        "identity."
    )
    return record


def _role_of(dec: Decomposition, role: FunctionalRole) -> list[str]:
    return [h.symbol for h in dec.hypotheses() if h.role == role]


def _hypothesis_signature(dec: Decomposition, symbol: str) -> FunctionalSignature | None:
    for hyp in dec.hypotheses():
        if hyp.symbol == symbol:
            return hyp.signature
    return None


def _translate_second_order(left: Decomposition, right: Decomposition) -> TranslationRecord:
    mapping: dict[str, str] = {}
    pairs = [
        (FunctionalRole.STATE, "state"),
        (FunctionalRole.STATE_TRANSITION, "inertia"),
        (FunctionalRole.DISSIPATION, "dissipation"),
        (FunctionalRole.INTERACTION, "restoring"),
        (FunctionalRole.FORCING, "forcing"),
    ]
    compat: list[CompatibilityReport] = []
    preserved = [
        "second_order_ode",
        "linearity",
        "time_invariance",
        "causal_evolution",
    ]
    broken = ["si_dimensions", "physical_carriers"]
    t = Transformation(
        name="lumped_second_order_analogy",
        mapping={},
        notes="Maps coefficients of matching derivative order.",
    )
    for role, label in pairs:
        a = _role_of(left, role)
        b = _role_of(right, role)
        if a and b:
            mapping[a[0]] = b[0]
            t.mapping[a[0]] = b[0]
            sa = _hypothesis_signature(left, a[0])
            sb = _hypothesis_signature(right, b[0])
            if sa and sb:
                # Attach SI dimensions for the canonical mechanical/electrical pair.
                sa = _with_known_units(sa, a[0])
                sb = _with_known_units(sb, b[0])
                compat.append(
                    classify_compatibility(
                        a[0],
                        sa,
                        b[0],
                        sb,
                        transformation=t,
                        shared_invariants={
                            "linearity": True,
                            "time_invariance": True,
                            "causality": True,
                        },
                        assumptions=["same derivative order", "lumped"],
                    )
                )
        elif a or b:
            broken.append(f"unpaired_{label}")

    verdicts = {c.verdict for c in compat}
    if compat and verdicts <= {CompatibilityClass.TRANSFORMABLE, CompatibilityClass.DIRECTLY_COMPATIBLE}:
        kind = CorrespondenceKind.MATHEMATICAL_CORRESPONDENCE
        confidence = min(c.confidence for c in compat)
    elif mapping:
        kind = CorrespondenceKind.ANALOGY
        confidence = 0.35
    else:
        kind = CorrespondenceKind.ANALOGY
        confidence = 0.1

    return TranslationRecord(
        left_name=left.tree.name,
        right_name=right.tree.name,
        mapping=mapping,
        preserved=preserved,
        broken=list(dict.fromkeys(broken)),
        assumptions=["matching derivative order is the structure that T preserves"],
        confidence=confidence,
        kind=kind,
        compatibility=compat,
        notes=[
            "Functional correspondence is a hypothesis. The systems are not "
            "claimed to be physically equivalent."
        ],
    )


def _with_known_units(sig: FunctionalSignature, symbol: str) -> FunctionalSignature:
    units = {
        "m": _MASS,
        "c": _DAMPING,
        "k": _STIFFNESS,
        "f": _FORCE,
        "L": _INDUCTANCE,
        "R": _RESISTANCE,
        "kC": _ELASTANCE,
        "v": _VOLTAGE,
    }.get(symbol)
    if units is None:
        return sig
    return FunctionalSignature(
        role=sig.role,
        math_type=sig.math_type,
        domain=sig.domain,
        codomain=sig.codomain,
        units=units,  # type: ignore[arg-type]
        symmetry=sig.symmetry,
        constraints=sig.constraints,
    )


def _translate_generic(left: Decomposition, right: Decomposition) -> TranslationRecord:
    mapping: dict[str, str] = {}
    for h in left.hypotheses():
        matches = [g.symbol for g in right.hypotheses() if g.role == h.role]
        if matches:
            mapping[h.symbol] = matches[0]
    return TranslationRecord(
        left_name=left.tree.name,
        right_name=right.tree.name,
        mapping=mapping,
        preserved=[r for r in mapping],
        broken=["no_checked_structure_map"],
        assumptions=["role-name matching only"],
        confidence=0.2 if mapping else 0.05,
        kind=CorrespondenceKind.ANALOGY,
        notes=[
            "Only role labels were aligned. This is analogy until a structure "
            "map is supplied."
        ],
    )
