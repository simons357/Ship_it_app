"""Cycle enumeration with the coeff_max caveat attached to every result.

coeff_max bounds coordinates in the chosen saturated basis, not
||c||_∞. A reported minimum from that enumeration is not a global
minimum over integer cycles. Entry-bounded enumeration is provided
for certification that actually needs ||c||_∞.
"""

from __future__ import annotations

from itertools import product
from typing import List, Sequence

from min_cycle_verifier_v2.exceptions import DisarmedError
from min_cycle_verifier_v2.kernel import in_right_kernel, right_kernel_saturated
from min_cycle_verifier_v2.status import (
    ARMED,
    COEFF_MAX_CAVEAT,
    FIRST_REAL_MIN_CYCLE_RUN_PERMITTED,
    P2_ARMED,
    status_record,
)
from min_cycle_verifier_v2.validate import require_int, require_integer_matrix

Vector = List[int]


def _dot_combo(basis: Sequence[Sequence[int]], coeffs: Sequence[int]) -> Vector:
    n = len(basis[0])
    out = [0] * n
    for a, vec in zip(coeffs, basis):
        if a == 0:
            continue
        for i in range(n):
            out[i] += a * vec[i]
    return out


def enumerate_basis_coeffs(
    M: Sequence[Sequence[int]],
    coeff_max: int,
) -> dict:
    """All nonzero combinations Σ a_i b_i with |a_i| ≤ coeff_max.

    Every record carries COEFF_MAX_CAVEAT. This is not a live
    MIN-CYCLE run and does not arm P2.
    """
    require_integer_matrix(M)
    require_int(coeff_max, where="coeff_max")
    if coeff_max < 0:
        raise ValueError("coeff_max must be >= 0")
    if ARMED or P2_ARMED or FIRST_REAL_MIN_CYCLE_RUN_PERMITTED:
        raise DisarmedError("verifier is disarmed; this branch must stay unreachable")

    basis = right_kernel_saturated(M)
    k = len(basis)
    found: List[dict] = []
    if k == 0 or coeff_max == 0:
        return _pack(M, basis, coeff_max, found, mode="basis_coeffs")

    rng = range(-coeff_max, coeff_max + 1)
    seen = set()
    for coeffs in product(rng, repeat=k):
        if all(c == 0 for c in coeffs):
            continue
        vec = _dot_combo(basis, coeffs)
        key = tuple(vec)
        if key in seen:
            continue
        seen.add(key)
        found.append(
            {
                "c": vec,
                "basis_coeffs": list(coeffs),
                "inf_norm": max(abs(x) for x in vec) if vec else 0,
                "support": sum(1 for x in vec if x != 0),
            }
        )
    found.sort(key=lambda rec: (rec["support"], rec["inf_norm"], rec["c"]))
    return _pack(M, basis, coeff_max, found, mode="basis_coeffs")


def enumerate_entry_bounded(
    M: Sequence[Sequence[int]],
    inf_max: int,
) -> dict:
    """All nonzero c in ker_Z(M) with ||c||_∞ ≤ inf_max.

    Exhaustive for that box. Use this when a global minimum-support
    claim would depend on a coordinate bound rather than basis coeffs.
    """
    require_integer_matrix(M)
    require_int(inf_max, where="inf_max")
    if inf_max < 0:
        raise ValueError("inf_max must be >= 0")
    if ARMED or P2_ARMED or FIRST_REAL_MIN_CYCLE_RUN_PERMITTED:
        raise DisarmedError("verifier is disarmed; this branch must stay unreachable")

    A, m, n = require_integer_matrix(M)
    basis = right_kernel_saturated(A)
    found: List[dict] = []
    if inf_max == 0:
        return _pack(A, basis, inf_max, found, mode="entry_bounded")

    rng = range(-inf_max, inf_max + 1)
    for coords in product(rng, repeat=n):
        if all(x == 0 for x in coords):
            continue
        if not in_right_kernel(A, coords):
            continue
        vec = list(coords)
        found.append(
            {
                "c": vec,
                "inf_norm": max(abs(x) for x in vec),
                "support": sum(1 for x in vec if x != 0),
            }
        )
    found.sort(key=lambda rec: (rec["support"], rec["inf_norm"], rec["c"]))
    return _pack(A, basis, inf_max, found, mode="entry_bounded")


def _pack(M, basis, bound, found, *, mode: str) -> dict:
    return {
        "mode": mode,
        "bound": bound,
        "basis": [list(b) for b in basis],
        "n_found": len(found),
        "cycles": found,
        "coeff_max_caveat": COEFF_MAX_CAVEAT,
        "is_global_inf_norm_minimum": mode == "entry_bounded",
        "status": status_record(),
        "disarmed": True,
        "p2_data_used": False,
        "canonical_labels_used": False,
    }
