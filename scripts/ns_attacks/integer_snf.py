"""Smith normal form over Z.

Standard computational algebra: for M in Z^{m x n} there exist
unimodular U in GL(m,Z), V in GL(n,Z) with

    U M V = S = diag(s_1, ..., s_r, 0, ..., 0),

s_i > 0 and s_i divides s_{i+1}. This file implements that
certificate. It does not claim a new theorem.

Progress measure: the least nonzero |entry| in the active
submatrix strictly decreases after each remainder step, so
the Euclidean loops terminate.
"""

from __future__ import annotations

from math import gcd
from typing import List, Sequence, Tuple

Matrix = List[List[int]]


def identity(n: int) -> Matrix:
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def zeros(m: int, n: int) -> Matrix:
    return [[0] * n for _ in range(m)]


def shape(A: Sequence[Sequence[int]]) -> Tuple[int, int]:
    m = len(A)
    n = len(A[0]) if m else 0
    return m, n


def copy_matrix(A: Sequence[Sequence[int]]) -> Matrix:
    return [list(row) for row in A]


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


def _swap_rows(A: Matrix, i: int, j: int) -> None:
    if i != j:
        A[i], A[j] = A[j], A[i]


def _swap_cols(A: Matrix, i: int, j: int) -> None:
    if i == j:
        return
    for row in A:
        row[i], row[j] = row[j], row[i]


def _neg_row(A: Matrix, i: int) -> None:
    A[i] = [-x for x in A[i]]


def _add_row(A: Matrix, i: int, src: int, q: int) -> None:
    if q == 0 or i == src:
        return
    A[i] = [A[i][t] + q * A[src][t] for t in range(len(A[i]))]


def _add_col(A: Matrix, j: int, src: int, q: int) -> None:
    if q == 0 or j == src:
        return
    for row in A:
        row[j] += q * row[src]


def _min_entry(S: Matrix, k: int) -> Tuple[int, int] | None:
    m, n = shape(S)
    best = None
    best_abs = None
    for i in range(k, m):
        for j in range(k, n):
            v = abs(S[i][j])
            if v == 0:
                continue
            if best_abs is None or v < best_abs:
                best_abs = v
                best = (i, j)
    return best


def smith_normal_form(A: Sequence[Sequence[int]]) -> Tuple[Matrix, Matrix, Matrix]:
    """Return (U, S, V) with U A V = S in Smith form, U and V unimodular."""
    m, n = shape(A)
    S = copy_matrix(A) if m else []
    U = identity(m)
    V = identity(n)
    if m == 0 or n == 0:
        return U, S, V

    for k in range(min(m, n)):
        while True:
            pos = _min_entry(S, k)
            if pos is None:
                return U, S, V
            pi, pj = pos
            _swap_rows(S, k, pi)
            _swap_rows(U, k, pi)
            _swap_cols(S, k, pj)
            _swap_cols(V, k, pj)
            if S[k][k] < 0:
                _neg_row(S, k)
                _neg_row(U, k)
            pivot = S[k][k]
            if pivot == 0:
                return U, S, V

            # Remainder-reduce the rest of row k and column k.
            for i in range(k + 1, m):
                q = S[i][k] // pivot
                _add_row(S, i, k, -q)
                _add_row(U, i, k, -q)
            for j in range(k + 1, n):
                q = S[k][j] // pivot
                _add_col(S, j, k, -q)
                _add_col(V, j, k, -q)

            col_clear = all(S[i][k] == 0 for i in range(k + 1, m))
            row_clear = all(S[k][j] == 0 for j in range(k + 1, n))
            if not (col_clear and row_clear):
                # A leftover remainder is strictly smaller than |pivot|.
                continue

            # Fold any trailing entry not divisible by the pivot.
            mixed = False
            for i in range(k + 1, m):
                for j in range(k + 1, n):
                    if S[i][j] % pivot != 0:
                        _add_row(S, k, i, 1)
                        _add_row(U, k, i, 1)
                        mixed = True
                        break
                if mixed:
                    break
            if not mixed:
                break

    _force_divisibility_chain(S, U, V)
    return U, S, V


def _force_divisibility_chain(S: Matrix, U: Matrix, V: Matrix) -> None:
    """Enforce s_i | s_{i+1} on the nonzero diagonal."""
    m, n = shape(S)
    r = min(m, n)
    for i in range(r - 1):
        a = S[i][i]
        b = S[i + 1][i + 1]
        if a == 0 or b == 0:
            continue
        if b % a == 0:
            continue
        g = gcd(a, b)
        # Mix: replace (a, b) by (g, lcm). Unimodular 2x2 on those axes.
        # Add column i+1 into column i so gcd appears in the 2x2,
        # then clear.
        _add_col(S, i, i + 1, 1)
        _add_col(V, i, i + 1, 1)
        # Now S[i][i] = a, S[i+1][i] = b (off-diag from the next pivot
        # after adding col i+1 into col i: S[i+1][i] += S[i+1][i+1] = b).
        # Euclidean on column i between rows i and i+1.
        aa, bb = S[i][i], S[i + 1][i]
        g2, x, y = _extended_gcd(aa, bb)
        # [x y; -bb/g aa/g] on rows
        ri = [x * S[i][t] + y * S[i + 1][t] for t in range(n)]
        rj = [-(bb // g2) * S[i][t] + (aa // g2) * S[i + 1][t] for t in range(n)]
        ui = [x * U[i][t] + y * U[i + 1][t] for t in range(m)]
        uj = [-(bb // g2) * U[i][t] + (aa // g2) * U[i + 1][t] for t in range(m)]
        S[i], S[i + 1] = ri, rj
        U[i], U[i + 1] = ui, uj
        if S[i][i] == 0:
            continue
        if S[i][i + 1] != 0:
            q = S[i][i + 1] // S[i][i]
            _add_col(S, i + 1, i, -q)
            _add_col(V, i + 1, i, -q)
        if S[i][i] < 0:
            _neg_row(S, i)
            _neg_row(U, i)
        if S[i + 1][i + 1] < 0:
            _neg_row(S, i + 1)
            _neg_row(U, i + 1)


def _extended_gcd(a: int, b: int) -> Tuple[int, int, int]:
    old_r, r = a, b
    old_s, s = 1, 0
    old_t, t = 0, 1
    while r != 0:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
        old_t, t = t, old_t - q * t
    g = old_r
    x, y = old_s, old_t
    if g < 0:
        g, x, y = -g, -x, -y
    return g, x, y


def integer_rank(A: Sequence[Sequence[int]]) -> int:
    if not A or not A[0]:
        return 0
    _, S, _ = smith_normal_form(A)
    m, n = shape(S)
    r = 0
    for i in range(min(m, n)):
        if S[i][i] != 0:
            r += 1
    return r


def smith_invariants(A: Sequence[Sequence[int]]) -> List[int]:
    if not A or not A[0]:
        return []
    _, S, _ = smith_normal_form(A)
    m, n = shape(S)
    return [S[i][i] for i in range(min(m, n)) if S[i][i] != 0]


def left_kernel_primitive(A: Sequence[Sequence[int]]) -> List[List[int]]:
    """Primitive Z-basis of ker_Z(A^T) = {c : A^T c = 0}.

    If U A V = S with S = diag(s_1,...,s_r,0,...), then
    ker A^T is spanned by those rows of U whose corresponding
    diagonal entry of S is zero (and, if m > n, the extra rows
    of U past n).
    """
    m, n = shape(A)
    if m == 0:
        return []
    U, S, _ = smith_normal_form(A)
    basis: List[List[int]] = []
    limit = min(m, n)
    for i in range(m):
        diag = S[i][i] if i < limit else 0
        if diag != 0:
            continue
        vec = list(U[i])
        g = 0
        for v in vec:
            g = gcd(g, v)
        if g > 1:
            vec = [v // g for v in vec]
        for v in vec:
            if v != 0:
                if v < 0:
                    vec = [-u for u in vec]
                break
        if any(vec):
            basis.append(vec)
    return basis
