"""Column Hermite normal form over Z, with an explicit unimodular log.

Every recorded operation is elementary and unimodular:

- swap two columns          (det −1)
- negate a column           (det −1)
- add an integer multiple   (det +1)

No rational clearing, no division of a column by an integer other
than via these SL/GL column ops. The running determinant sign is
maintained and checked against det(U) at the end.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Sequence, Tuple

from min_cycle_verifier_v2.validate import (
    identity,
    require_integer_matrix,
    shape,
    zeros,
)

Matrix = List[List[int]]


@dataclass(frozen=True)
class UnimodularOp:
    """One elementary column operation of determinant ±1."""

    kind: str
    args: Tuple[int, ...]
    det_sign: int

    def describe(self) -> str:
        if self.kind == "swap_cols":
            return f"swap columns {self.args[0]} and {self.args[1]}"
        if self.kind == "neg_col":
            return f"negate column {self.args[0]}"
        if self.kind == "add_col":
            return (
                f"column {self.args[0]} += {self.args[2]} * column {self.args[1]}"
            )
        return f"{self.kind}{self.args}"


@dataclass
class ColumnHNF:
    H: Matrix
    U: Matrix
    ops: List[UnimodularOp] = field(default_factory=list)
    det_sign: int = 1
    pivot_rows: List[int] = field(default_factory=list)

    @property
    def rank(self) -> int:
        return len(self.pivot_rows)

    def every_op_unimodular(self) -> bool:
        return all(op.det_sign in (-1, 1) for op in self.ops) and all(
            op.kind in ("swap_cols", "neg_col", "add_col") for op in self.ops
        )


def _copy(A: Sequence[Sequence[int]]) -> Matrix:
    return [list(row) for row in A]


def _swap_cols(A: Matrix, i: int, j: int) -> None:
    if i == j:
        return
    for row in A:
        row[i], row[j] = row[j], row[i]


def _neg_col(A: Matrix, j: int) -> None:
    for row in A:
        row[j] = -row[j]


def _add_col(A: Matrix, dest: int, src: int, q: int) -> None:
    if q == 0 or dest == src:
        return
    for row in A:
        row[dest] += q * row[src]


def _det_small(A: Sequence[Sequence[int]]) -> int:
    """Exact determinant. Used to confirm |det U| = 1 for modest n."""
    n = len(A)
    if n == 0:
        return 1
    if n == 1:
        return A[0][0]
    # Bareiss algorithm, fraction-free.
    M = _copy(A)
    sign = 1
    prev = 1
    for k in range(n - 1):
        # Find a nonzero pivot at or below (k,k).
        piv = k
        while piv < n and M[piv][k] == 0:
            piv += 1
        if piv == n:
            return 0
        if piv != k:
            M[k], M[piv] = M[piv], M[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                val = M[i][j] * M[k][k] - M[i][k] * M[k][j]
                if prev != 1 and prev != -1 and prev != 0:
                    if val % prev != 0:
                        # Should not happen for integer matrices under Bareiss.
                        raise ArithmeticError("Bareiss integrality failed")
                    val //= prev
                elif prev == -1:
                    val = -val
                M[i][j] = val
        prev = M[k][k]
        if prev == 0:
            return 0
    return sign * M[n - 1][n - 1]


def column_hnf(M: Sequence[Sequence[int]]) -> ColumnHNF:
    """Column HNF: H = M U with U ∈ GL(n, Z).

    Convention (Cohen-style, columns): there are pivot rows
    i_0 < … < i_{r-1} and pivot columns 0..r-1 such that

    - H[i_k, k] > 0
    - H[i_k, j] = 0 for j > k
    - 0 ≤ H[i_k, j] < H[i_k, k] for j < k
    - rows without a pivot are Z-combinations of earlier pivot rows
      after the transform (they may be nonzero only in columns < r
      in ways already reduced by previous pivots)
    - columns r..n-1 of H are identically zero

    The last n−r columns of U are a Z-basis of ker_Z(M).
    """
    A, m, n = require_integer_matrix(M)
    H = _copy(A)
    U = identity(n)
    rec = ColumnHNF(H=H, U=U, ops=[], det_sign=1, pivot_rows=[])

    def swap(i: int, j: int) -> None:
        if i == j:
            return
        _swap_cols(H, i, j)
        _swap_cols(U, i, j)
        rec.ops.append(UnimodularOp("swap_cols", (i, j), -1))
        rec.det_sign *= -1

    def neg(j: int) -> None:
        _neg_col(H, j)
        _neg_col(U, j)
        rec.ops.append(UnimodularOp("neg_col", (j,), -1))
        rec.det_sign *= -1

    def add(dest: int, src: int, q: int) -> None:
        if q == 0 or dest == src:
            return
        _add_col(H, dest, src, q)
        _add_col(U, dest, src, q)
        rec.ops.append(UnimodularOp("add_col", (dest, src, q), 1))

    k = 0
    for i in range(m):
        if k >= n:
            break
        # Put gcd(H[i, k:]) into H[i, k] and zeros to the right,
        # mixing only columns >= k so earlier pivots survive.
        if all(H[i][j] == 0 for j in range(k, n)):
            continue

        for j in range(k + 1, n):
            while H[i][j] != 0:
                if H[i][k] == 0 or abs(H[i][j]) < abs(H[i][k]):
                    swap(k, j)
                q = H[i][j] // H[i][k]
                add(j, k, -q)

        if H[i][k] < 0:
            neg(k)

        piv = H[i][k]
        if piv == 0:
            continue

        for j in range(k):
            q = H[i][j] // piv
            add(j, k, -q)

        rec.pivot_rows.append(i)
        k += 1

    return rec


def matmul(A: Sequence[Sequence[int]], B: Sequence[Sequence[int]]) -> Matrix:
    m, k = shape(A)
    k2, n = shape(B)
    if k != k2:
        raise ValueError(f"matmul shape {m}x{k} vs {k2}x{n}")
    out = zeros(m, n)
    for i in range(m):
        for j in range(n):
            s = 0
            for t in range(k):
                s += A[i][t] * B[t][j]
            out[i][j] = s
    return out


def transpose(A: Sequence[Sequence[int]]) -> Matrix:
    m, n = shape(A)
    return [[A[i][j] for i in range(m)] for j in range(n)]


def det(A: Sequence[Sequence[int]]) -> int:
    return _det_small(A)


def apply_ops_to_identity(n: int, ops: Sequence[UnimodularOp]) -> Matrix:
    """Replay the unimodular log on I_n. Must recover U."""
    U = identity(n)
    for op in ops:
        if op.kind == "swap_cols":
            _swap_cols(U, op.args[0], op.args[1])
        elif op.kind == "neg_col":
            _neg_col(U, op.args[0])
        elif op.kind == "add_col":
            _add_col(U, op.args[0], op.args[1], op.args[2])
        else:
            raise ValueError(f"unknown op {op.kind}")
    return U


def is_column_hnf(H: Sequence[Sequence[int]], pivot_rows: Sequence[int]) -> bool:
    m, n = shape(H)
    r = len(pivot_rows)
    # Zero columns after rank.
    for j in range(r, n):
        for i in range(m):
            if H[i][j] != 0:
                return False
    for k, i in enumerate(pivot_rows):
        if H[i][k] <= 0:
            return False
        for j in range(k + 1, n):
            if H[i][j] != 0:
                return False
        piv = H[i][k]
        for j in range(k):
            if not (0 <= H[i][j] < piv):
                return False
        if k > 0 and i <= pivot_rows[k - 1]:
            return False
    return True
