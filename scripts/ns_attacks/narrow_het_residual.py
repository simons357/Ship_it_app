#!/usr/bin/env python3
"""Narrow heterochiral residual: width crossover and S_Γ primitive.

Not DA-NS-2. NS is not solved.

r² = D_s/(Λ Y), κ = √Λ.
B^{prim} is the Waleffe cyclic incidence.
b is the channel target (ones for charge, A_γ for S_Γ).
No optimizer. No single-circle search.
"""

from __future__ import annotations

import argparse
import json
import math
from itertools import combinations
from typing import Dict, List, Sequence, Tuple

import sys
from pathlib import Path

import numpy as np

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ns_attacks.sag_two_triad_witness import (
    K,
    P,
    Q,
    R,
    S,
    L_family,
)

Mode = Tuple[int, int, int]
Signed = Tuple[Mode, int]


def nrm(k: Mode) -> float:
    return math.sqrt(k[0] * k[0] + k[1] * k[1] + k[2] * k[2])


def n2(k: Mode) -> int:
    return k[0] * k[0] + k[1] * k[1] + k[2] * k[2]


def add(a: Mode, b: Mode) -> Mode:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def neg(a: Mode) -> Mode:
    return (-a[0], -a[1], -a[2])


def cross2(a: Mode, b: Mode) -> Mode:
    return (
        a[1] * b[2] - a[2] * b[1],
        a[2] * b[0] - a[0] * b[2],
        a[0] * b[1] - a[1] * b[0],
    )


def collinear(a: Mode, b: Mode) -> bool:
    return cross2(a, b) == (0, 0, 0)


def lex(k: Mode) -> Mode:
    return k


def canon_signed(k: Mode, s: int) -> Signed:
    mk = neg(k)
    if k < mk:
        return (k, s)
    if mk < k:
        return (mk, -s)
    return (k, s)


def H_ijo(i: float, j: float, o: float) -> float:
    return i * i + j * j + o * o + i * j - o * (i + j)


def A_coeff(i: float, j: float, o: float) -> float:
    return (i + o) * (j + o) / (2.0 * o)


def R_of(i: float, j: float, o: float, Lambda: float) -> float:
    return A_coeff(i, j, o) * (H_ijo(i, j, o) - Lambda)


def vandermonde(x: float, y: float, z: float) -> float:
    return (x - y) * (y - z) * (z - x)


# ---------------------------------------------------------------------------
# Width / crossover (independent algebra checker)
# ---------------------------------------------------------------------------


def moments(eigs: Sequence[float], mass: Sequence[float]) -> dict:
    x = sum(a * m for a, m in zip(eigs, mass))
    y = sum(a * a * m for a, m in zip(eigs, mass))
    z = sum(a**3 * m for a, m in zip(eigs, mass))
    lam = y / x
    d_s = z - lam * y
    d_s_var = sum(a * (a - lam) ** 2 * m for a, m in zip(eigs, mass))
    return {"X": x, "Y": y, "Z": z, "Lambda": lam, "D_s": d_s, "D_s_var": d_s_var}


def relative_width(D_s: float, Lambda: float, Y: float) -> float:
    return math.sqrt(D_s / (Lambda * Y))


def crossover_audit() -> dict:
    """Reproduce r ∼ κ^{-1/2} from the definitions. Flag conventions."""
    eigs = [1.0, 2.0, 4.0, 9.0]
    mass = [0.20, 0.35, 0.30, 0.15]
    m = moments(eigs, mass)
    r = relative_width(m["D_s"], m["Lambda"], m["Y"])
    kappa = math.sqrt(m["Lambda"])
    ds_over_y = m["D_s"] / m["Y"]
    # One-shell-plus-spread family: λ = κ² (1 + ε ξ), mean-zero ξ in λ-weight.
    kappa0 = 4.0
    lam0 = kappa0**2
    epsilons = [0.05, 0.25, 0.80]
    family = []
    for eps in epsilons:
        # two-point mass at λ = λ0 (1±eps), equal X-weight ⇒ barycenter λ0.
        a1, a2 = lam0 * (1.0 - eps), lam0 * (1.0 + eps)
        # mass chosen so λ-weighted mean is λ0: a m  proportional to X-share.
        # take equal X-share: a1 m1 = a2 m2 = 1/2, wait X = Σ a m.
        m1 = 0.5 / a1
        m2 = 0.5 / a2
        mm = moments([a1, a2], [m1, m2])
        rr = relative_width(mm["D_s"], mm["Lambda"], mm["Y"])
        family.append(
            {
                "eps": eps,
                "Lambda": mm["Lambda"],
                "r": rr,
                "Ds_over_Y": mm["D_s"] / mm["Y"],
                "Lambda_r2": mm["Lambda"] * rr * rr,
                "kappa": math.sqrt(mm["Lambda"]),
                "kappa_inv_sqrt": mm["Lambda"] ** -0.25,
                "broad_by_r": rr >= mm["Lambda"] ** -0.25,
                "broad_by_visc": (mm["D_s"] / mm["Y"]) >= math.sqrt(mm["Lambda"]),
            }
        )

    # Linear expansion of R − 2κ³.
    kappa = 5.0
    lam = kappa**2
    R0 = R_of(kappa, kappa, kappa, lam)
    # unit-relative |k| perturbations of size r_rel = 0.01
    r_rel = 0.01
    samples = []
    for di, dj, do in ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (1.0, -0.5, -0.5), (1.0, 1.0, 1.0)):
        i = kappa * (1.0 + r_rel * di)
        j = kappa * (1.0 + r_rel * dj)
        o = kappa * (1.0 + r_rel * do)
        dR = R_of(i, j, o, lam) - 2.0 * kappa**3
        samples.append(
            {
                "dirs": [di, dj, do],
                "dR": dR,
                "dR_over_kappa3_r": dR / (kappa**3 * r_rel),
                "dR_over_kappa2_delta": dR / (kappa**2 * (kappa * r_rel)),
            }
        )

    # Homochiral Vandermonde scaling.
    vand = []
    for r_rel in (0.01, 0.02, 0.04):
        x, y, z = kappa * (1.0 + r_rel), kappa * (1.0 - 0.5 * r_rel), kappa * (1.0 - 0.5 * r_rel)
        # last two equal ⇒ vandermonde 0; use a 3-gap.
        x, y, z = kappa * (1.0 + r_rel), kappa * (1.0 - 0.4 * r_rel), kappa * (1.0 - 0.6 * r_rel)
        v = vandermonde(x, y, z)
        vand.append(
            {
                "r_rel": r_rel,
                "V": v,
                "V_over_kappa3_r3": v / (kappa**3 * r_rel**3),
            }
        )

    return {
        "definitions": {
            "r2": "D_s / (Λ Y)",
            "kappa": "sqrt(Λ)",
            "Ds_over_Y_identity": "Λ r²",
        },
        "sample_moments": {
            "r": r,
            "kappa": math.sqrt(m["Lambda"]),
            "Ds_over_Y": ds_over_y,
            "Lambda_r2": m["Lambda"] * r * r,
            "Ds_is_variance": abs(m["D_s"] - m["D_s_var"]) < 1e-12,
        },
        "two_point_family": family,
        "R_minus_2k3": {
            "R0": R0,
            "two_k3": 2.0 * 5.0**3,
            "samples": samples,
        },
        "vandermonde": vand,
        "conventions": {
            "r_dimensionless": True,
            "kappa_inv_sqrt_is_torus_unit": True,
            "r_is_sigma_lambda_over_Lambda": True,
            "r_approx_2_delta_over_kappa": True,
            "do_not_mix_with_Ds_over_Y": "D_s/Y = κ² r², not r",
            "do_not_mix_with_sigma_lambda_over_kappa": "σ_λ/κ = κ r",
            "crossover_equivalence_exact": "r ≳ κ^{-1/2} ⇔ D_s/Y ≳ κ",
            "box_rescaling_changes_the_number": True,
        },
    }


# ---------------------------------------------------------------------------
# Primitive test
# ---------------------------------------------------------------------------


def minority_output(legs: Sequence[Signed]) -> Tuple[Signed, List[Signed]]:
    plus = [leg for leg in legs if leg[1] > 0]
    minus = [leg for leg in legs if leg[1] < 0]
    if len(plus) == 1:
        return plus[0], minus
    if len(minus) == 1:
        return minus[0], plus
    raise ValueError("not a 2+1 heterochiral channel")


def channel_A(legs: Sequence[Signed]) -> float:
    o, pair = minority_output(legs)
    i, j = nrm(pair[0][0]), nrm(pair[1][0])
    return A_coeff(i, j, nrm(o[0]))


def waleffe_row(legs: Sequence[Signed], index: Dict[Signed, int], n_col: int) -> np.ndarray:
    row = np.zeros(n_col)
    ks = [leg[1] * nrm(leg[0]) for leg in legs]
    for t in range(3):
        col = index[canon_signed(*legs[t])]
        row[col] += ks[(t + 1) % 3] - ks[(t + 2) % 3]
    return row


def solve_primitive(B: np.ndarray, b: np.ndarray, tol: float = 1e-10) -> dict:
    if B.size == 0:
        return {"empty": True}
    # Thin SVD only. Full U is n_ch × n_ch and is not needed:
    # c^T b = 0 for all c ∈ ker(B^T)  ⇔  b ∈ range(B)  ⇔  residual = 0.
    # The least-squares residual vector is itself a left-null witness.
    S = np.linalg.svd(B, compute_uv=False)
    smax = float(S[0]) if S.size else 1.0
    cutoff = tol * max(smax, 1.0)
    rank = int(np.sum(S > cutoff))
    n_ch, n_mo = int(B.shape[0]), int(B.shape[1])
    n_left_null = n_ch - rank
    w, *_ = np.linalg.lstsq(B, b, rcond=tol)
    resid_vec = B @ w - b
    resid = float(np.linalg.norm(resid_vec))
    bn = float(np.linalg.norm(b))
    compatible = resid <= cutoff * max(bn, 1.0)
    # Residual holonomy: r = b − Bw ∈ ker(B^T), r^T b = ||r||² when Bw ⟂ ker.
    holonomy_rel = (resid / bn) if bn else 0.0
    smin = float(S[rank - 1]) if rank else 0.0
    cond = (smax / smin) if smin > 0 else math.inf
    holonomy = []
    if n_ch <= 64 and n_left_null:
        U, _, _ = np.linalg.svd(B, full_matrices=True)
        left_null = U[:, rank:]
        for j in range(min(8, left_null.shape[1])):
            c = left_null[:, j]
            holonomy.append(
                {
                    "cTb": float(c @ b),
                    "rel": float(abs(c @ b) / (np.linalg.norm(c) * bn)) if bn else 0.0,
                }
            )
    return {
        "n_channels": n_ch,
        "n_modes": n_mo,
        "rank": rank,
        "n_left_null": n_left_null,
        "singular_max": smax,
        "singular_min_pos": smin,
        "cond": cond,
        "compatible": bool(compatible),
        "residual": resid,
        "min_norm_w": float(np.linalg.norm(w)),
        "min_norm_w_over_b": float(np.linalg.norm(w) / bn) if bn else 0.0,
        "worst_holonomy_rel": float(holonomy_rel),
        "holonomy": holonomy,
    }


def assemble(channels: List[List[Signed]]) -> Tuple[np.ndarray, Dict[str, np.ndarray], List[Signed]]:
    nodes: List[Signed] = []
    seen = set()
    for ch in channels:
        for leg in ch:
            c = canon_signed(*leg)
            if c not in seen:
                seen.add(c)
                nodes.append(c)
    index = {m: i for i, m in enumerate(nodes)}
    n_col = len(nodes)
    rows = [waleffe_row(ch, index, n_col) for ch in channels]
    B = np.vstack(rows) if rows else np.zeros((0, 0))
    A = np.array([channel_A(ch) for ch in channels], dtype=float)
    ones = np.ones(len(channels), dtype=float)
    return B, {"A": A, "ones": ones, "A_minus_mean": A - np.mean(A) if len(A) else A}, nodes


def restrict_isotropic(B: np.ndarray, nodes: List[Signed]) -> Tuple[np.ndarray, int]:
    """w = w(|k|, s): translation-invariant isotropic multiplier."""
    keys = []
    key_of = []
    lookup = {}
    for k, s in nodes:
        key = (n2(k), s)
        if key not in lookup:
            lookup[key] = len(keys)
            keys.append(key)
        key_of.append(lookup[key])
    n = len(keys)
    R = np.zeros((B.shape[1], n))
    for i, j in enumerate(key_of):
        R[i, j] = 1.0
    return B @ R, n


def two_triad_channels() -> List[List[Signed]]:
    return [
        [(K, 1), (P, 1), (Q, -1)],
        [(K, 1), (R, -1), (S, 1)],
    ]


def L_channels(L: int) -> List[List[Signed]]:
    row = L_family(L)
    return [
        [(row["k"], 1), (row["p"], 1), (row["q"], -1)],
        [(row["k"], 1), (row["r"], -1), (row["s"], 1)],
    ]


def lattice_modes(max_n2: int) -> List[Mode]:
    lim = int(math.sqrt(max_n2)) + 1
    out = []
    for x in range(-lim, lim + 1):
        for y in range(-lim, lim + 1):
            for z in range(-lim, lim + 1):
                k = (x, y, z)
                if k == (0, 0, 0):
                    continue
                if n2(k) <= max_n2:
                    out.append(k)
    return out


def geometric_triads(modes: List[Mode]) -> List[Tuple[Mode, Mode, Mode]]:
    Sset = set(modes)
    seen = set()
    triads = []
    for k, p in combinations(modes, 2):
        q = neg(add(k, p))
        if q not in Sset or q == (0, 0, 0):
            continue
        if q == k or q == p or q == neg(k) or q == neg(p) or k == neg(p):
            continue
        if collinear(k, p):
            continue
        geo = tuple(sorted((k, p, q)))
        conj = tuple(sorted((neg(k), neg(p), neg(q))))
        key = min(geo, conj)
        if key in seen:
            continue
        seen.add(key)
        triads.append(geo)
    return triads


def het_channels_from_triads(triads) -> List[List[Signed]]:
    channels = []
    signs = [(1, 1, -1), (1, -1, 1), (-1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)]
    seen = set()
    for a, b, c in triads:
        for sa, sb, sc in signs:
            if sa == sb == sc:
                continue
            legs = [(a, sa), (b, sb), (c, sc)]
            can = tuple(sorted((canon_signed(*leg) for leg in legs)))
            if can in seen:
                continue
            seen.add(can)
            channels.append(legs)
    return channels


def spanning_tree_channels(channels: List[List[Signed]]) -> List[List[Signed]]:
    """Kruskal on the mode graph: a channel is an edge-triple; keep a forest."""
    parent: Dict[Signed, Signed] = {}

    def find(x: Signed) -> Signed:
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: Signed, b: Signed) -> bool:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[rb] = ra
        return True

    tree = []
    for ch in channels:
        nodes = [canon_signed(*leg) for leg in ch]
        # A 3-node channel creates a loop unless it links 3 distinct components
        # or 2 components (connects a new node pair without closing).
        roots = {find(n) for n in nodes}
        if len(roots) <= 1:
            continue
        # Connect all three; if they were 2 components this adds a path, still a tree.
        union(nodes[0], nodes[1])
        union(nodes[0], nodes[2])
        tree.append(ch)
    return tree


def evaluate_network(name: str, channels: List[List[Signed]]) -> dict:
    B, targets, nodes = assemble(channels)
    out = {
        "name": name,
        "n_channels": len(channels),
        "n_modes": len(nodes),
    }
    for key, b in targets.items():
        out[key] = solve_primitive(B, b)
    B_iso, n_iso = restrict_isotropic(B, nodes)
    out["isotropic_n_weights"] = n_iso
    out["isotropic_A"] = solve_primitive(B_iso, targets["A"])
    out["isotropic_ones"] = solve_primitive(B_iso, targets["ones"])
    # Shared primitive? ones and A in the same 1-D ray inside range(B).
    # Ask whether A − α ones is solvable for some α, i.e. proj.
    if B.size:
        # residual of projecting A onto span{ones} in the least-squares B-sense
        # is not the right test. Test: is A in range(B)+span? Already have A and ones
        # separately. Shared *one* w for both iff A is a scalar multiple of ones
        # in the quotient R^{n} / (range(B))^⊥... 
        # They share a primitive iff there is w with B w = ones and B w = A,
        # hence A = ones, or more weakly a pair (α,β)≠0 with B w = α ones + β A
        # always true if either is in range. "Share" = one H_w produces both
        # functionals, i.e. A ∥ ones (channel-constant A).
        A = targets["A"]
        out["A_is_constant"] = bool(np.allclose(A, A[0])) if len(A) else True
        out["share_same_w_for_both_targets"] = bool(
            out["A"]["compatible"]
            and out["ones"]["compatible"]
            and np.allclose(A, A[0])
        )
        # Weaker: both lie in range(B), so each has a (possibly different) primitive.
        out["both_in_range"] = bool(out["A"]["compatible"] and out["ones"]["compatible"])
    return out


def report() -> dict:
    width = crossover_audit()
    nets = []
    nets.append(evaluate_network("two_triad_tree", two_triad_channels()))
    for L in (2, 7, 16, 55):
        nets.append(evaluate_network(f"L_family_tree_{L}", L_channels(L)))

    lat10 = het_channels_from_triads(geometric_triads(lattice_modes(10)))
    nets.append(evaluate_network("lattice_het_n2le10", lat10))
    tree10 = spanning_tree_channels(lat10)
    nets.append(evaluate_network("lattice_het_n2le10_tree", tree10))

    lat14 = het_channels_from_triads(geometric_triads(lattice_modes(14)))
    nets.append(evaluate_network("lattice_het_n2le14", lat14))
    tree14 = spanning_tree_channels(lat14)
    nets.append(evaluate_network("lattice_het_n2le14_tree", tree14))

    return {
        "crossover": width,
        "networks": nets,
        "locks": {
            "not_a_close": True,
            "not_DA_NS_2": True,
            "no_optimizer": True,
            "no_circle_search": True,
        },
    }


def _py(x):
    if isinstance(x, dict):
        return {str(k): _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, float) and (math.isnan(x) or math.isinf(x)):
        return None
    return x


def main(argv=None) -> int:
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    print(json.dumps(_py(report()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
