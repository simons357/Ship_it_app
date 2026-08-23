"""Compatibility of proposed mechanism replacements.

A correspondence is DIRECTLY COMPATIBLE, TRANSFORMABLE, or INCOMPATIBLE.
Transformable pairs must carry an explicit map T.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping

from .checks import Dim
from .schema import CompatibilityClass, CorrespondenceKind, MathType
from .signature import FunctionalSignature


INVARIANT_KEYS = (
    "linearity",
    "time_invariance",
    "passivity",
    "self_adjoint",
    "causality",
    "positivity",
    "hyperbolic",
    "elliptic",
    "conservation",
)


@dataclass
class Transformation:
    """Explicit map M_B --T--> M̃_B that makes a substitution legal."""

    name: str
    mapping: dict[str, str]
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "mapping": dict(self.mapping), "notes": self.notes}


@dataclass
class CompatibilityReport:
    left: str
    right: str
    verdict: CompatibilityClass
    kind: CorrespondenceKind
    interface_match: bool
    dimension_match: bool | None
    preserved: list[str] = field(default_factory=list)
    broken: list[str] = field(default_factory=list)
    assumptions: list[str] = field(default_factory=list)
    confidence: float = 0.0
    transformation: Transformation | None = None
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "left": self.left,
            "right": self.right,
            "verdict": self.verdict.value,
            "kind": self.kind.value,
            "interface_match": self.interface_match,
            "dimension_match": self.dimension_match,
            "preserved": list(self.preserved),
            "broken": list(self.broken),
            "assumptions": list(self.assumptions),
            "confidence": self.confidence,
            "transformation": None
            if self.transformation is None
            else self.transformation.to_dict(),
            "reasons": list(self.reasons),
        }


def _types_compatible(a: MathType, b: MathType) -> bool:
    if a == MathType.UNKNOWN or b == MathType.UNKNOWN:
        return False
    return a == b


def _dims_equal(a: Dim | None, b: Dim | None) -> bool | None:
    if a is None or b is None:
        return None
    return a == b


def classify_compatibility(
    left_name: str,
    left: FunctionalSignature,
    right_name: str,
    right: FunctionalSignature,
    *,
    transformation: Transformation | None = None,
    shared_invariants: Mapping[str, bool] | None = None,
    assumptions: list[str] | None = None,
) -> CompatibilityReport:
    """Decide whether M_right may replace M_left."""
    interface = _types_compatible(left.math_type, right.math_type) and (
        left.domain == right.domain or left.domain == "unspecified" or right.domain == "unspecified"
    )
    # Role agreement is evidence of analogous function, not of substitutability.
    same_role = left.role == right.role
    dim_match = _dims_equal(left.units, right.units)

    preserved: list[str] = []
    broken: list[str] = []
    if same_role:
        preserved.append(f"functional_role:{left.role.value}")
    else:
        broken.append(f"functional_role:{left.role.value}≠{right.role.value}")
    if interface:
        preserved.append("interface_types")
    else:
        broken.append("interface_types")
    if dim_match is True:
        preserved.append("si_dimensions")
    elif dim_match is False:
        broken.append("si_dimensions")

    shared = dict(shared_invariants or {})
    for key in sorted(left.symmetry | right.symmetry | set(shared)):
        left_has = key in left.symmetry
        right_has = key in right.symmetry
        forced = shared.get(key)
        if forced is True or (left_has and right_has):
            preserved.append(key)
        elif forced is False or (left_has != right_has):
            broken.append(key)

    reasons: list[str] = []
    if dim_match is True and interface and same_role and transformation is None:
        verdict = CompatibilityClass.DIRECTLY_COMPATIBLE
        kind = CorrespondenceKind.STRUCTURE_PRESERVING_EQUIVALENCE
        confidence = 0.8
        reasons.append("Matching role, interface and SI dimensions with no residual map.")
    elif transformation is not None:
        if "si_dimensions" in broken:
            reasons.append(
                "SI dimensions differ; substitution is legal only after the "
                f"explicit transformation {transformation.name}."
            )
        verdict = CompatibilityClass.TRANSFORMABLE
        kind = CorrespondenceKind.MATHEMATICAL_CORRESPONDENCE
        confidence = 0.7 if same_role else 0.45
        reasons.append(
            "An explicit transformation was supplied. This is a mathematical "
            "correspondence, not physical equivalence."
        )
    else:
        verdict = CompatibilityClass.INCOMPATIBLE
        kind = CorrespondenceKind.ANALOGY if same_role else CorrespondenceKind.ANALOGY
        confidence = 0.2 if same_role else 0.05
        if same_role:
            reasons.append(
                "Roles are described similarly, but no explicit transformation "
                "was supplied. Superficial analogy is not a legal substitution."
            )
        else:
            reasons.append("Roles, interfaces or dimensions do not match and no map T was given.")

    return CompatibilityReport(
        left=left_name,
        right=right_name,
        verdict=verdict,
        kind=kind,
        interface_match=interface,
        dimension_match=dim_match,
        preserved=list(dict.fromkeys(preserved)),
        broken=list(dict.fromkeys(broken)),
        assumptions=list(assumptions or []),
        confidence=confidence,
        transformation=transformation,
        reasons=reasons,
    )
