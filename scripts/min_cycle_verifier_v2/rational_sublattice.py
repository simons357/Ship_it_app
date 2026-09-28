"""The old, incorrect lattice: Q-nullspace with denominators cleared.

This module exists only so DA can independently exhibit the
failure mode that v2 was required to repair. It is not the
search space of the verifier.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd, lcm
from typing import List, Sequence

from min_cycle_verifier_v2.validate import require_integer_matrix

Matrix = List[List[int]]
Vector = List[int]


def _rref_rational(M: Sequence[Sequence[int]]) -> tuple[List[List[Fraction]], List[int]]:
    A, m, n = require_integer_matrix(M)
    R: List[List[Fraction]] = [[Fraction(A[i][j]) for j in range(n)] for i in range(m)]
    pivots: List[int] = []
    row = 0
    for col in range(n):
        if row >= m:
            break
        piv = None
        for i in range(row, m):
            if R[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        R[row], R[piv] = R[piv], R[row]
        lead = R[row][col]
        R[row] = [x / lead for x in R[row]]
        for i in range(m):
            if i == row:
                continue
            f = R[i][col]
            if f == 0:
                continue
            R[i] = [R[i][j] - f * R[row][j] for j in range(n)]
        pivots.append(col)
        row += 1
    return R, pivots


def rational_nullspace_cleared(M: Sequence[Sequence[int]]) -> List[Vector]:
    """Finite-index (in general) lattice from ker_Q, denominators cleared.

    This is the method v2 forbids as a search space.
    """
    A, m, n = require_integer_matrix(M)
    R, pivots = _rref_rational(A)
    pivot_set = set(pivots)
    free = [j for j in range(n) if j not in pivot_set]
    basis: List[Vector] = []
    for f in free:
        qvec = [Fraction(0) for _ in range(n)]
        qvec[f] = Fraction(1)
        for r_i, pcol in enumerate(pivots):
            # R[r_i][pcol] = 1, so x_pcol = -sum_{j≠pcol} R[r_i][j] x_j
            qvec[pcol] = -R[r_i][f]
        den = 1
        for x in qvec:
            den = lcm(den, x.denominator)
        ivec = [int(x * den) for x in qvec]
        g = 0
        for v in ivec:
            g = gcd(g, v)
        if g > 1:
            ivec = [v // g for v in ivec]
        for v in ivec:
            if v != 0:
                if v < 0:
                    ivec = [-u for u in ivec]
                break
        if any(ivec):
            basis.append(ivec)
    basis.sort(key=tuple)
    return basis


def label() -> str:
    return "UNSATURATED_LATTICE_FROM_Q_NULLSPACE"
