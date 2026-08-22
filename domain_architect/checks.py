"""Mathematical checks: projectors, types, dimensions, tensors, source-state."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Mapping

import numpy as np

from .parser import ASTNode, NodeKind
from .schema import (
    MathType,
    PermissionSubtype,
    PROJECTOR_SUBTYPES,
    SOURCE_STATE_WARNING,
    ScaleResponseSubtype,
    COORDINATE_LIKE_SCALE,
    RESPONSE_LIKE_SCALE,
)


@dataclass
class ProjectorCheck:
    subtype: PermissionSubtype
    residual: float | None
    is_projector: bool
    label: str
    details: str


def classify_permission(
    matrix: np.ndarray | None = None,
    *,
    declared: PermissionSubtype | None = None,
    weights: np.ndarray | None = None,
    binary: np.ndarray | None = None,
    atol: float = 1e-8,
) -> ProjectorCheck:
    """Name an admissibility object by mathematics, not by the letter P.

    A genuine projector must satisfy P² = P (within ``atol``). Otherwise the
    report uses selector, filter, or constraint language.
    """
    if weights is not None:
        w = np.asarray(weights, dtype=float)
        if np.allclose(w * w, w, atol=atol) and set(np.unique(np.round(w, 8))).issubset(
            {0.0, 1.0}
        ):
            return ProjectorCheck(
                subtype=PermissionSubtype.BINARY_SELECTOR,
                residual=0.0,
                is_projector=False,
                label="binary selector",
                details="Weights are 0/1. This is a selector, not a tested projector.",
            )
        return ProjectorCheck(
            subtype=PermissionSubtype.SOFT_FILTER,
            residual=None,
            is_projector=False,
            label="soft filter",
            details="Non-idempotent weights. Report as a filter, not a projector.",
        )
    if binary is not None:
        mask = np.asarray(binary, dtype=float)
        residual = float(np.linalg.norm(mask * mask - mask))
        return ProjectorCheck(
            subtype=PermissionSubtype.BINARY_SELECTOR,
            residual=residual,
            is_projector=False,
            label="binary selector",
            details="Binary mode mask. Projective only in a declared basis.",
        )
    if matrix is None:
        subtype = declared or PermissionSubtype.UNKNOWN
        label = (
            "projector"
            if subtype in PROJECTOR_SUBTYPES
            else subtype.value.replace("_", " ")
        )
        return ProjectorCheck(
            subtype=subtype,
            residual=None,
            is_projector=False,
            label=label,
            details="No matrix supplied; projector identity was not established.",
        )

    p = np.asarray(matrix, dtype=complex)
    if p.ndim != 2 or p.shape[0] != p.shape[1]:
        return ProjectorCheck(
            subtype=PermissionSubtype.UNKNOWN,
            residual=None,
            is_projector=False,
            label="operator",
            details="Object is not a square matrix; projector test withheld.",
        )
    residual = float(np.linalg.norm(p @ p - p))
    if residual <= atol * max(1.0, float(np.linalg.norm(p))):
        hermitian = np.allclose(p, p.conjugate().T, atol=atol)
        subtype = (
            PermissionSubtype.ORTHOGONAL_PROJECTOR
            if hermitian
            else PermissionSubtype.OBLIQUE_PROJECTOR
        )
        return ProjectorCheck(
            subtype=subtype,
            residual=residual,
            is_projector=True,
            label="orthogonal projector" if hermitian else "oblique projector",
            details=f"P² − P residual = {residual:.3e}. Projector identity established.",
        )
    return ProjectorCheck(
        subtype=PermissionSubtype.WEIGHTING_OPERATOR,
        residual=residual,
        is_projector=False,
        label="weighting operator",
        details=(
            f"P² − P residual = {residual:.3e}. The object is not a "
            "mathematical projector; use selector, filter, or constraint."
        ),
    )


@dataclass
class ScaleResponseRecord:
    symbol: str
    subtype: ScaleResponseSubtype
    expression: str | None = None


def warn_scale_ambiguity(records: Iterable[ScaleResponseRecord]) -> list[str]:
    """Warn when one symbol is used as both a coordinate and its response."""
    by_symbol: dict[str, set[ScaleResponseSubtype]] = {}
    for rec in records:
        by_symbol.setdefault(rec.symbol, set()).add(rec.subtype)
    warnings: list[str] = []
    for symbol, kinds in by_symbol.items():
        if kinds & COORDINATE_LIKE_SCALE and kinds & RESPONSE_LIKE_SCALE:
            warnings.append(
                f"Symbol {symbol} is used simultaneously as a spectral "
                "coordinate and as a response function. Prefer κ_n for the "
                "coordinate and R(κ_n) for the transfer function."
            )
    return warnings


@dataclass
class SourceStateResult:
    resolved: bool
    source: str | None
    state: str | None
    rule: str | None
    warning: str | None
    amplitudes: np.ndarray | None = None
    phases: np.ndarray | None = None


def decompose_source_state(
    values: np.ndarray | None = None,
    *,
    rule: str | None = None,
    source_name: str = "rho",
) -> SourceStateResult:
    """Split a source only when a unique or conventional rule is declared.

    Polar decomposition ρ = A e^{iθ} is accepted. An arbitrary product
    ρ = S ψ is rejected as nonunique.
    """
    if rule is None:
        return SourceStateResult(
            resolved=False,
            source=source_name,
            state=None,
            rule=None,
            warning=SOURCE_STATE_WARNING,
        )
    if rule in {"polar", "amplitude_phase"}:
        if values is None:
            return SourceStateResult(
                resolved=True,
                source="A",
                state="exp(iθ)",
                rule=rule,
                warning=None,
            )
        z = np.asarray(values, dtype=complex)
        amp = np.abs(z)
        phase = np.ones_like(z, dtype=complex)
        nonzero = amp > 0
        phase[nonzero] = z[nonzero] / amp[nonzero]
        return SourceStateResult(
            resolved=True,
            source="A",
            state="exp(iθ)",
            rule=rule,
            warning=None,
            amplitudes=amp,
            phases=phase,
        )
    return SourceStateResult(
        resolved=False,
        source=source_name,
        state=None,
        rule=rule,
        warning=SOURCE_STATE_WARNING + f" Declared rule {rule!r} is not unique.",
    )


# SI base: mass, length, time, current, temperature, amount, luminosity
Dim = tuple[int, int, int, int, int, int, int]

DIM_ZERO: Dim = (0, 0, 0, 0, 0, 0, 0)

KNOWN_UNITS: dict[str, Dim] = {
    "G": ( -1, 3, -2, 0, 0, 0, 0),   # L^3 M^-1 T^-2
    "c": (0, 1, -1, 0, 0, 0, 0),
    "rho": (1, -3, 0, 0, 0, 0, 0),
    "Phi": (0, 2, -2, 0, 0, 0, 0),
    "pi": DIM_ZERO,
    "k": (0, -1, 0, 0, 0, 0, 0),
    "kappa": (0, -1, 0, 0, 0, 0, 0),
}


def _add(a: Dim, b: Dim) -> Dim:
    return tuple(x + y for x, y in zip(a, b))  # type: ignore[return-value]


def _sub(a: Dim, b: Dim) -> Dim:
    return tuple(x - y for x, y in zip(a, b))  # type: ignore[return-value]


def _mul(a: Dim, n: int) -> Dim:
    return tuple(x * n for x in a)  # type: ignore[return-value]


@dataclass
class DimensionalResult:
    consistent: bool | None
    left: Dim | None
    right: Dim | None
    message: str
    unknown: list[str] = field(default_factory=list)


def _dim_of(node: ASTNode, env: Mapping[str, Dim], unknown: list[str]) -> Dim | None:
    if node.kind == NodeKind.NUMBER:
        return DIM_ZERO
    if node.kind in {NodeKind.SYMBOL, NodeKind.INDEXED}:
        name = node.name or ""
        if name in env:
            return env[name]
        if name.lower() in env:
            return env[name.lower()]
        unknown.append(name)
        return None
    if node.kind == NodeKind.MUL:
        dims = [_dim_of(c, env, unknown) for c in node.children]
        if any(d is None for d in dims):
            return None
        acc = DIM_ZERO
        for d in dims:
            acc = _add(acc, d)  # type: ignore[arg-type]
        return acc
    if node.kind == NodeKind.DIV:
        a = _dim_of(node.children[0], env, unknown)
        b = _dim_of(node.children[1], env, unknown)
        if a is None or b is None:
            return None
        return _sub(a, b)
    if node.kind == NodeKind.ADD or node.kind == NodeKind.SUB:
        dims = [_dim_of(c, env, unknown) for c in node.children]
        if any(d is None for d in dims):
            return None
        if len({d for d in dims}) != 1:
            return None
        return dims[0]
    if node.kind == NodeKind.POW:
        base = _dim_of(node.children[0], env, unknown)
        exp = node.children[1]
        if base is None:
            return None
        if exp.kind == NodeKind.NUMBER and isinstance(exp.value, (int, float)):
            return _mul(base, int(exp.value))
        unknown.append("non-integer exponent")
        return None
    if node.kind == NodeKind.APPLY and node.name == "Laplacian":
        inner = _dim_of(node.children[0], env, unknown) if node.children else None
        if inner is None:
            return None
        return _add(inner, (0, -2, 0, 0, 0, 0, 0))
    if node.kind == NodeKind.APPLY and node.name == "dAlembertian":
        inner = _dim_of(node.children[0], env, unknown) if node.children else None
        if inner is None:
            return None
        return _add(inner, (0, 0, -2, 0, 0, 0, 0))
    if node.children:
        return _dim_of(node.children[0], env, unknown)
    unknown.append(node.name or node.kind.value)
    return None


def check_dimensions(
    tree: ASTNode,
    units: Mapping[str, Dim] | None = None,
) -> DimensionalResult:
    env = dict(KNOWN_UNITS)
    if units:
        env.update(units)
    unknown: list[str] = []
    if tree.kind != NodeKind.EQUALITY or len(tree.children) != 2:
        return DimensionalResult(
            consistent=None,
            left=None,
            right=None,
            message="Dimensional consistency cannot yet be established.",
            unknown=["no equality"],
        )
    left = _dim_of(tree.children[0], env, unknown)
    right = _dim_of(tree.children[1], env, unknown)
    unknown = list(dict.fromkeys(unknown))
    if left is None or right is None or unknown:
        return DimensionalResult(
            consistent=None,
            left=left,
            right=right,
            message="Dimensional consistency cannot yet be established.",
            unknown=unknown,
        )
    if left == right:
        return DimensionalResult(
            consistent=True,
            left=left,
            right=right,
            message="Both sides have the same dimensions under the supplied units.",
            unknown=[],
        )
    return DimensionalResult(
        consistent=False,
        left=left,
        right=right,
        message="Dimensional inconsistency: the two sides do not match.",
        unknown=[],
    )


@dataclass
class TypeRecord:
    symbol: str
    math_type: MathType
    domain: str | None = None
    symmetry: str | None = None
    units: str | None = None
    role: str | None = None
    rank: int | None = None
    indices: list[str] = field(default_factory=list)
    variance: list[str] = field(default_factory=list)


INCOMPATIBLE_TYPE_PAIRS = {
    (MathType.SET, MathType.OPERATOR),
    (MathType.MANIFOLD, MathType.SCALAR),
}


def check_types(records: Iterable[TypeRecord], tree: ASTNode | None = None) -> list[str]:
    warnings: list[str] = []
    recs = list(records)
    by_name = {r.symbol: r for r in recs}
    for a in recs:
        for b in recs:
            if (a.math_type, b.math_type) in INCOMPATIBLE_TYPE_PAIRS:
                warnings.append(
                    f"Type warning: {a.symbol} ({a.math_type.value}) combined "
                    f"with {b.symbol} ({b.math_type.value})."
                )
    if tree is not None and tree.kind == NodeKind.EQUALITY:
        left_idx = _free_indices(tree.children[0], by_name)
        right_idx = _free_indices(tree.children[1], by_name)
        if left_idx != right_idx:
            warnings.append(
                "Free-index mismatch: "
                f"left has {sorted(left_idx)} while right has {sorted(right_idx)}."
            )
    return warnings


def _free_indices(node: ASTNode, env: Mapping[str, TypeRecord]) -> set[str]:
    counts: dict[str, int] = {}
    for n in node.walk():
        idxs = list(n.indices)
        if n.name and n.name in env:
            idxs = idxs or list(env[n.name].indices)
        for idx in idxs:
            counts[idx] = counts.get(idx, 0) + 1
    return {k for k, v in counts.items() if v == 1}


@dataclass
class GeometryRecord:
    geometry: str | None = None
    metric: str | None = None
    dimension: int | None = None
    topology: str | None = None
    coordinate_system: str | None = None
    connection: str | None = None
    curvature: str | None = None
    gauge: str | None = None
    boundary: str | None = None
    initial_data: str | None = None

    def declared_fields(self) -> dict[str, str | int]:
        out: dict[str, str | int] = {}
        for key, value in self.__dict__.items():
            if value is not None:
                out[key] = value
        return out


def expand_environment(geometry: GeometryRecord) -> dict[str, str | int]:
    """E must expand when geometry, gauge, or data are independently specified."""
    return geometry.declared_fields()
