"""Saturated integer kernel via column HNF.

ker_Z(M) = { x ∈ Z^n : M x = 0 }. The last n−r columns of the
unimodular U in M U = H are a Z-basis of this kernel. Because U
is unimodular, the basis saturates: it is not a finite-index
sublattice of the true integer kernel.

This is the repair required by SPEC-MIN-CYCLE-VERIFIER-V2:
search over the saturated integer kernel, not over a lattice
obtained by clearing denominators from a rational nullspace.
"""

from __future__ import annotations

from math import gcd
from typing import List, Sequence, Tuple

from min_cycle_verifier_v2.hnf import column_hnf, matmul, transpose
from min_cycle_verifier_v2.validate import require_integer_matrix, require_integer_vector

Matrix = List[List[int]]
Vector = List[int]


def _content_normalize(v: Sequence[int]) -> Vector:
    g = 0
    for x in v:
        g = gcd(g, x)
    if g == 0:
        return list(v)
    if g < 0:
        g = -g
    out = [x // g for x in v]
    for x in out:
        if x != 0:
            if x < 0:
                out = [-y for y in out]
            break
    return out


def _vec_key(v: Sequence[int]) -> Tuple[int, ...]:
    return tuple(v)


def right_kernel_saturated(M: Sequence[Sequence[int]]) -> List[Vector]:
    """Z-basis of ker_Z(M), saturated, as a list of column-vectors."""
    A, m, n = require_integer_matrix(M)
    rec = column_hnf(A)
    r = rec.rank
    basis: List[Vector] = []
    for j in range(r, n):
        vec = [rec.U[i][j] for i in range(n)]
        # Column j of H must be zero.
        if any(rec.H[i][j] != 0 for i in range(m)):
            raise RuntimeError("HNF kernel column of H is not zero")
        if any(vec):
            basis.append(_content_normalize(vec))
    basis.sort(key=_vec_key)
    return basis


def left_kernel_saturated(M: Sequence[Sequence[int]]) -> List[Vector]:
    """Z-basis of ker_Z(M^T) = { c : c^T M = 0 }."""
    A, _, _ = require_integer_matrix(M)
    return right_kernel_saturated(transpose(A))


def kernel_certificate(M: Sequence[Sequence[int]]) -> dict:
    """Full HNF certificate for the saturated right kernel."""
    A, m, n = require_integer_matrix(M)
    rec = column_hnf(A)
    basis = right_kernel_saturated(A)
    HU = matmul(A, rec.U)
    return {
        "m": m,
        "n": n,
        "rank": rec.rank,
        "ker_dim": n - rec.rank,
        "H": rec.H,
        "U": rec.U,
        "H_equals_MU": HU == rec.H,
        "det_sign_running": rec.det_sign,
        "every_op_unimodular": rec.every_op_unimodular(),
        "n_ops": len(rec.ops),
        "ops": [op.describe() for op in rec.ops],
        "pivot_rows": list(rec.pivot_rows),
        "basis": basis,
        "search_space": "saturated integer kernel ker_Z(M)",
        "not_a_rational_nullspace": True,
    }


def in_right_kernel(M: Sequence[Sequence[int]], v: Sequence[int]) -> bool:
    A, m, n = require_integer_matrix(M)
    x = require_integer_vector(v, n=n, name="v")
    for i in range(m):
        s = 0
        for j in range(n):
            s += A[i][j] * x[j]
        if s != 0:
            return False
    return True
