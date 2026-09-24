#!/usr/bin/env python3
"""SAG-5 — smallest Fourier-hypergraph compatibility ratios.

Not a proof. Not an occupancy bound. Not a T_c estimate.
NS is not solved.

5A is the rank of L_p : p^perp_C -> C^{d(p)}.
5B is joint signed Im[(k·v_p)(v_q · conj(v_k))] with shared coefficients.

Frozen |v_j|=1. First pass uses G_triangle = 1.
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Dict, Iterable, List, Sequence, Tuple

import numpy as np

Mode = Tuple[int, int, int]
Triangle = Tuple[Mode, Mode, Mode]


def as_mode(v: Sequence[int]) -> Mode:
    return (int(v[0]), int(v[1]), int(v[2]))


def vec(m: Mode) -> np.ndarray:
    return np.asarray(m, dtype=float)


def perp_project(k: Mode, p: Mode) -> np.ndarray:
    kk = vec(k)
    pp = vec(p)
    n2 = float(pp @ pp)
    if n2 < 1e-15:
        raise ValueError("zero mode")
    return kk - ((kk @ pp) / n2) * pp


def one_triangle_max(tri: Triangle) -> float:
    p, q, k = tri
    if (p[0] + q[0], p[1] + q[1], p[2] + q[2]) != k:
        raise ValueError(f"triangle does not close: {tri}")
    return float(np.linalg.norm(perp_project(k, p)))


def perp_basis(m: Mode) -> Tuple[np.ndarray, np.ndarray]:
    w = vec(m)
    n = np.linalg.norm(w)
    if n < 1e-15:
        raise ValueError("zero mode")
    w = w / n
    seed = np.array([1.0, 0.0, 0.0])
    if abs(float(seed @ w)) > 0.9:
        seed = np.array([0.0, 1.0, 0.0])
    e1 = seed - (seed @ w) * w
    e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(w, e1)
    e2 = e2 / np.linalg.norm(e2)
    return e1, e2


def unit_perp(m: Mode, alpha: float, psi: float, chi: float) -> np.ndarray:
    e1, e2 = perp_basis(m)
    a = math.cos(alpha) * np.exp(1j * psi)
    b = math.sin(alpha) * np.exp(1j * chi)
    return a * e1 + b * e2


def coupling_map_rank(p: Mode, ks: Sequence[Mode], tol: float = 1e-12) -> int:
    e1, e2 = perp_basis(p)
    cols = np.stack([e1, e2], axis=1)
    rows = []
    for k in ks:
        rows.append(vec(k) @ cols)
    A = np.asarray(rows, dtype=float)
    return int(np.linalg.matrix_rank(A, tol=tol))


def signed_s(tri: Triangle, field: Dict[Mode, np.ndarray]) -> float:
    p, q, k = tri
    vp, vq, vk = field[p], field[q], field[k]
    prod = (vec(k) @ vp) * np.vdot(vk, vq)
    return float(np.imag(prod))


def _angles_to_field(
    modes: Sequence[Mode], params: np.ndarray
) -> Dict[Mode, np.ndarray]:
    field = {}
    for i, m in enumerate(modes):
        alpha, psi, chi = params[3 * i : 3 * i + 3]
        field[m] = unit_perp(m, float(alpha), float(psi), float(chi))
    return field


def joint_abs_sum(
    triangles: Sequence[Triangle],
    field: Dict[Mode, np.ndarray],
    weights: Sequence[float] | None = None,
) -> float:
    if weights is None:
        weights = [1.0] * len(triangles)
    total = 0.0
    for tri, g in zip(triangles, weights):
        total += float(g) * signed_s(tri, field)
    return abs(total)


def independent_denom(
    triangles: Sequence[Triangle], weights: Sequence[float] | None = None
) -> float:
    if weights is None:
        weights = [1.0] * len(triangles)
    return float(sum(abs(g) * one_triangle_max(tri) for tri, g in zip(triangles, weights)))


def _grid_unit_perp(m: Mode, n: int) -> Iterable[np.ndarray]:
    e1, e2 = perp_basis(m)
    # Exact axes and equal-weight combinations sit on the optimum
    # for the named orthogonal pairs. Include them so the reduced
    # maximizer is not a grid-approximation of a known ratio.
    for a, b in (
        (1.0, 0.0),
        (0.0, 1.0),
        (1.0 / math.sqrt(2.0), 1.0 / math.sqrt(2.0)),
        (1.0 / math.sqrt(2.0), -1.0 / math.sqrt(2.0)),
        (1.0 / math.sqrt(2.0), 1j / math.sqrt(2.0)),
    ):
        yield a * e1 + b * e2
    for i in range(n):
        alpha = (i + 0.5) * (0.5 * math.pi) / n
        for j in range(n):
            psi = 2.0 * math.pi * j / n
            for k_i in range(n):
                chi = 2.0 * math.pi * k_i / n
                yield unit_perp(m, alpha, psi, chi)


def shared_input_joint(triangles: Sequence[Triangle], n_grid: int = 24) -> float:
    """Free partners: joint max is max_{|v_p|=1} Σ |k_j · v_p|."""
    p = triangles[0][0]
    if any(tri[0] != p for tri in triangles):
        raise ValueError("shared_input_joint expects a common input")
    best = 0.0
    for v in _grid_unit_perp(p, n_grid):
        total = 0.0
        for _, _, k in triangles:
            total += abs(complex(vec(k) @ v))
        if total > best:
            best = total
    return float(best)


def shared_output_joint(triangles: Sequence[Triangle], n_grid: int = 24) -> float:
    """Independent inputs: joint max is Σ |P_{p^⊥}k| |v_k · n̂_q|."""
    k = triangles[0][2]
    if any(tri[2] != k for tri in triangles):
        raise ValueError("shared_output_joint expects a common output")
    prefs = []
    weights = []
    for p, q, kk in triangles:
        nvec = np.cross(vec(q), vec(kk))
        norm = np.linalg.norm(nvec)
        if norm < 1e-15:
            raise ValueError("degenerate triangle")
        prefs.append(nvec / norm)
        weights.append(one_triangle_max((p, q, kk)))
    best = 0.0
    for vk in _grid_unit_perp(k, n_grid):
        total = 0.0
        for nvec, w in zip(prefs, weights):
            total += w * abs(complex(np.vdot(nvec, vk)))
        if total > best:
            best = total
    return float(best)


def role_conflict_joint(tri_in: Triangle, tri_out: Triangle, n_grid: int = 28) -> float:
    """v_p is input of tri_in and output of tri_out."""
    p, q, k = tri_in
    r, s, p2 = tri_out
    if p != p2:
        raise ValueError("role_conflict_joint: output of tri_out must be input of tri_in")
    # S2 ≤ |P_r⊥ p| |P_{s^⊥} v_p| after aligning v_r, v_s given v_p.
    pr = float(np.linalg.norm(perp_project(p, r)))
    best = 0.0
    for vp in _grid_unit_perp(p, n_grid):
        s1 = abs(complex(vec(k) @ vp))
        s2 = pr * math.sqrt(max(0.0, 1.0 - abs(complex(vec(s) @ vp / np.linalg.norm(vec(s)))) ** 2))
        total = s1 + s2
        if total > best:
            best = total
    return float(best)


def optimize_rho(
    triangles: Sequence[Triangle],
    rng: np.random.Generator,
    n_starts: int = 80,
    n_refine: int = 40,
    step: float = 0.35,
    weights: Sequence[float] | None = None,
    n_grid: int = 24,
) -> Dict[str, float]:
    """Reduced maximizer when the share is named; generic search otherwise."""
    denom = independent_denom(triangles, weights)
    inputs = {tri[0] for tri in triangles}
    outputs = {tri[2] for tri in triangles}
    if weights is None and len(inputs) == 1 and len(triangles) >= 2:
        joint = shared_input_joint(triangles, n_grid=n_grid)
        kind = "shared-input reduced"
    elif weights is None and len(outputs) == 1 and len(triangles) >= 2:
        joint = shared_output_joint(triangles, n_grid=n_grid)
        kind = "shared-output reduced"
    elif (
        weights is None
        and len(triangles) == 2
        and triangles[1][2] == triangles[0][0]
    ):
        joint = role_conflict_joint(triangles[0], triangles[1], n_grid=max(n_grid, 28))
        kind = "role-conflict reduced"
    else:
        modes: List[Mode] = []
        seen = set()
        for p, q, k in triangles:
            for m in (p, q, k):
                if m not in seen:
                    seen.add(m)
                    modes.append(m)
        dim = 3 * len(modes)

        def score(params: np.ndarray) -> float:
            return joint_abs_sum(triangles, _angles_to_field(modes, params), weights)

        best_val = -1.0
        best_params = np.zeros(dim)
        for _ in range(n_starts):
            params = np.empty(dim)
            for i in range(len(modes)):
                params[3 * i] = rng.uniform(0.0, 0.5 * math.pi)
                params[3 * i + 1] = rng.uniform(0.0, 2.0 * math.pi)
                params[3 * i + 2] = rng.uniform(0.0, 2.0 * math.pi)
            val = score(params)
            if val > best_val:
                best_val = val
                best_params = params
        params = best_params.copy()
        for scale in (step, step * 0.4, step * 0.15):
            for _ in range(n_refine):
                trial = params.copy()
                trial += rng.normal(scale=scale, size=dim)
                for i in range(len(modes)):
                    trial[3 * i] = float(np.clip(trial[3 * i], 0.0, 0.5 * math.pi))
                val = score(trial)
                if val > best_val:
                    best_val = val
                    params = trial
        joint = float(best_val)
        kind = "generic search"
    return {
        "joint": float(joint),
        "denom": float(denom),
        "rho": float(joint / denom) if denom > 0 else float("nan"),
        "kind": kind,
    }


# --- named hypergraphs ---

H2_IN: List[Triangle] = [
    ((2, 0, 0), (0, 2, 0), (2, 2, 0)),
    ((2, 0, 0), (0, 0, 2), (2, 0, 2)),
]
H2_OUT: List[Triangle] = [
    ((2, 0, 0), (-2, 0, 2), (0, 0, 2)),
    ((0, 2, 0), (0, -2, 2), (0, 0, 2)),
]
H2_ROLE: List[Triangle] = [
    ((2, 0, 0), (0, 0, 2), (2, 0, 2)),
    ((1, 1, 1), (1, -1, -1), (2, 0, 0)),
]
H3_IN: List[Triangle] = [
    ((2, 0, 0), (0, 2, 0), (2, 2, 0)),
    ((2, 0, 0), (0, 0, 2), (2, 0, 2)),
    ((2, 0, 0), (0, 2, 2), (2, 2, 2)),
]


def rho2_two_vector(w1: float, w2: float, cos_phi: float) -> float:
    """Stamped finite SAG-5 formula. Constant depletion, not N^{-δ}."""
    return math.sqrt(w1 * w1 + w2 * w2 + 2.0 * w1 * w2 * abs(cos_phi)) / (w1 + w2)


def rho2_in_exact() -> float:
    return rho2_two_vector(1.0, 1.0, 0.0)


def rho2_out_exact() -> float:
    return 1.0 / math.sqrt(2.0)


def rho3_in_exact() -> float:
    return 2.0 * (math.sqrt(2.0) - 1.0)


def report(rng: np.random.Generator, n_starts: int = 400) -> dict:
    h2_in_opt = optimize_rho(H2_IN, rng, n_starts=n_starts)
    h2_out_opt = optimize_rho(H2_OUT, rng, n_starts=n_starts)
    h2_role_opt = optimize_rho(H2_ROLE, rng, n_starts=max(n_starts, 800))
    h3_in_opt = optimize_rho(H3_IN, rng, n_starts=n_starts)
    return {
        "tag": "NUMERICAL optimizer vs EXACT named ratios. Not C0. Not 16/9.",
        "sag5a": {
            "rank_H2_in": coupling_map_rank((2, 0, 0), [(2, 2, 0), (2, 0, 2)]),
            "rank_H3_in": coupling_map_rank(
                (2, 0, 0), [(2, 2, 0), (2, 0, 2), (2, 2, 2)]
            ),
            "rank_bound": 2,
        },
        "H2_in": {
            "kind": "shared-input polarization budget; 5A rank = 2 (no coupling obstruction)",
            "rho_exact": rho2_in_exact(),
            "rho_opt": h2_in_opt["rho"],
            "joint_opt": h2_in_opt["joint"],
            "denom": h2_in_opt["denom"],
        },
        "H2_out": {
            "kind": "shared-output identification; smallest 5B",
            "rho_exact": rho2_out_exact(),
            "rho_opt": h2_out_opt["rho"],
            "joint_opt": h2_out_opt["joint"],
            "denom": h2_out_opt["denom"],
        },
        "H2_role": {
            "kind": "input-of-one / output-of-the-other; 5B role conflict",
            "rho_opt": h2_role_opt["rho"],
            "joint_opt": h2_role_opt["joint"],
            "denom": h2_role_opt["denom"],
        },
        "H3_in": {
            "kind": "three shared-input; rank 2 < 3; G=1 budget still in im L_p",
            "rho_exact": rho3_in_exact(),
            "rho_opt": h3_in_opt["rho"],
            "joint_opt": h3_in_opt["joint"],
            "denom": h3_in_opt["denom"],
        },
        "locks": {
            "no_abs_envelope": True,
            "no_occupancy_bound": True,
            "not_a_theorem": True,
        },
    }


def _py(x):
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, dict):
        return {k: _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    return x


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--starts", type=int, default=400)
    args = parser.parse_args(list(argv) if argv is not None else None)
    rng = np.random.Generator(np.random.PCG64(args.seed))
    print(json.dumps(_py(report(rng, n_starts=args.starts)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
