"""Standard torus reachability for integer homomorphisms.

For M in Z^{m x n} the induced map

    T_M : T^n → T^m,    θ ↦ M θ

(with T^k = R^k / 2π Z^k) is ordinary compact-abelian-group algebra.
Pontryagin duality identifies the annihilator of im T_M with
ker_Z(M^T). Smith normal form is the computational certificate.

This is not a Gate-C theorem and is not claimed as original.
"""

from __future__ import annotations

import math
from typing import List, Sequence

from ns_attacks.integer_snf import (
    integer_rank,
    left_kernel_primitive,
    matmul,
    shape,
    smith_invariants,
    smith_normal_form,
    transpose,
)

TWOPI = 2.0 * math.pi


def cycle_rank(M: Sequence[Sequence[int]]) -> int:
    """r_cyc = m - rank M.

    TREE means r_cyc = 0. LOOP means r_cyc >= 1. The words TREE
    and LOOP are shorthand for this integer; they are not a
    picture of triangles.
    """
    m, _ = shape(M)
    return m - integer_rank(M)


def is_tree(M: Sequence[Sequence[int]]) -> bool:
    return cycle_rank(M) == 0


def torus_reachability(
    M: Sequence[Sequence[int]],
    b: Sequence[float],
    *,
    tol: float = 1e-10,
) -> dict:
    """b in im T_M  iff  c^T b ≡ 0 (mod 2π) for every c in ker_Z(M^T)."""
    m, n = shape(M)
    if len(b) != m:
        raise ValueError(f"b has length {len(b)}, expected m={m}")
    ker = left_kernel_primitive(M)
    conditions = []
    ok = True
    for c in ker:
        pairing = sum(float(c[i]) * float(b[i]) for i in range(m))
        reduced = pairing - TWOPI * round(pairing / TWOPI)
        hit = abs(reduced) <= tol
        ok = ok and hit
        conditions.append(
            {
                "c": list(c),
                "cTb": pairing,
                "cTb_mod_2pi": reduced,
                "satisfied": hit,
            }
        )
    r = integer_rank(M)
    return {
        "m": m,
        "n": n,
        "rank": r,
        "r_cyc": m - r,
        "tree": (m - r) == 0,
        "ker_Z_MT": ker,
        "smith_invariants": smith_invariants(M),
        "conditions": conditions,
        "reachable": ok,
        "statement": (
            "b ∈ im T_M  iff  c^T b ≡ 0 (mod 2π)  ∀ c ∈ ker_Z(M^T). "
            "Standard torus algebra (Pontryagin duality / Smith form). "
            "Not a Gate-C theorem."
        ),
    }


def assemble_from_phases(M: Sequence[Sequence[int]], theta: Sequence[float]) -> List[float]:
    """b = M θ, the exact image point used by NA-2B assembly tests."""
    m, n = shape(M)
    if len(theta) != n:
        raise ValueError(f"theta has length {len(theta)}, expected n={n}")
    b = []
    for i in range(m):
        s = 0.0
        for j in range(n):
            s += M[i][j] * float(theta[j])
        b.append(s)
    return b


def add_dependent_channel(
    M: Sequence[Sequence[int]],
    coeffs: Sequence[int],
) -> List[List[int]]:
    """Append the integer combination sum_i coeffs_i M_i as a new row.

    Rank is unchanged when coeffs is not zero and M already has full
    row rank equal to its current rank. Cycle rank then increases by 1.
    """
    m, n = shape(M)
    if len(coeffs) != m:
        raise ValueError("coeffs must have one entry per existing row")
    if all(c == 0 for c in coeffs):
        raise ValueError("zero combination does not add a channel")
    row = [0] * n
    for i in range(m):
        for j in range(n):
            row[j] += int(coeffs[i]) * int(M[i][j])
    if all(v == 0 for v in row):
        raise ValueError("combination produced the zero channel")
    return [list(r) for r in M] + [row]


def tree_to_loop_control(
    M_tree: Sequence[Sequence[int]],
    coeffs: Sequence[int],
) -> dict:
    """Algebraic TREE → LOOP positive control.

    Start from r_cyc = 0. Add one channel that is an integer
    combination of existing rows, so no new independent phase
    constraint is introduced (rank unchanged, n unchanged) and

        r_cyc : 0 ⟶ 1.

    Then ker_Z M^T has rank one; its primitive generator c is the
    unique compatibility condition.
    """
    if not is_tree(M_tree):
        raise ValueError("control requires a TREE input (r_cyc = 0)")
    M_loop = add_dependent_channel(M_tree, coeffs)
    r0 = cycle_rank(M_tree)
    r1 = cycle_rank(M_loop)
    ker = left_kernel_primitive(M_loop)
    if r1 != 1:
        raise ValueError(f"expected r_cyc: 0 → 1, got {r0} → {r1}")
    if len(ker) != 1:
        raise ValueError(f"expected unique primitive generator, got {ker}")
    c = ker[0]
    # Uniqueness up to sign: the generator is primitive of rank-1 kernel.
    return {
        "M_tree": [list(r) for r in M_tree],
        "M_loop": M_loop,
        "coeffs": [int(x) for x in coeffs],
        "r_cyc_before": r0,
        "r_cyc_after": r1,
        "transition": "0 → 1",
        "primitive_c": c,
        "acceptance": (
            "TREE→LOOP control accepted: r_cyc : 0 → 1, "
            "rank_Z ker M^T = 1, unique primitive compatibility vector c."
        ),
        "not_a_picture": True,
    }


def snf_certificate(M: Sequence[Sequence[int]]) -> dict:
    U, S, V = smith_normal_form(M)
    recon = matmul(matmul(U, M), V)
    return {
        "U": U,
        "S": S,
        "V": V,
        "invariants": smith_invariants(M),
        "reconstructs": recon == S,
        "novelty": False,
        "cite": "Smith normal form over Z; Pontryagin dual of T^n.",
    }


def apply_MT(M: Sequence[Sequence[int]], c: Sequence[int]) -> List[int]:
    """M^T c."""
    return [row[0] for row in matmul(transpose(M), [[int(x)] for x in c])]
