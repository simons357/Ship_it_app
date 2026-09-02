"""Functional signatures X = (r, τ, D, C, U, S, K)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .checks import Dim, DIM_ZERO
from .schema import FunctionalRole, MathType


@dataclass
class FunctionalSignature:
    role: FunctionalRole
    math_type: MathType = MathType.UNKNOWN
    domain: str = "unspecified"
    codomain: str = "unspecified"
    units: Dim | None = None
    symmetry: frozenset[str] = field(default_factory=frozenset)
    constraints: frozenset[str] = field(default_factory=frozenset)

    def as_tuple(self) -> tuple[str, str, str, str, Dim | None, tuple[str, ...], tuple[str, ...]]:
        return (
            self.role.value,
            self.math_type.value,
            self.domain,
            self.codomain,
            self.units,
            tuple(sorted(self.symmetry)),
            tuple(sorted(self.constraints)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "role": self.role.value,
            "math_type": self.math_type.value,
            "domain": self.domain,
            "codomain": self.codomain,
            "units": list(self.units) if self.units is not None else None,
            "symmetry": sorted(self.symmetry),
            "constraints": sorted(self.constraints),
        }


@dataclass
class RoleHypothesis:
    """A role assignment is a hypothesis: role + confidence + rationale."""

    symbol: str
    role: FunctionalRole
    confidence: float
    rationale: str
    signature: FunctionalSignature
    subtype: str = "unknown"
    alternate_roles: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "symbol": self.symbol,
            "role": self.role.value,
            "confidence": self.confidence,
            "rationale": self.rationale,
            "subtype": self.subtype,
            "signature": self.signature.to_dict(),
            "alternate_roles": list(self.alternate_roles),
        }


def dim_or_zero(units: Dim | None) -> Dim:
    return units if units is not None else DIM_ZERO
