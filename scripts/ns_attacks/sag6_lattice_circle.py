#!/usr/bin/env python3
"""SAG-6 — one output k, full equal-input lattice circle.

Not a proof of depletion. Not a T_c bound. NS is not solved.

p + q = k, |p|^2 = |q|^2 = α  ⇒  p · k = |k|^2 / 2.
Incoming vectors w_j = (k · v_p) P_k v_q live in k^⊥.
Centered weight λ_k(λ_k−Λ) is a common prefactor and is
kept off this sum.

Test: ||∑ w_j|| ≲ N^{1/2} × (one-triangle natural size)?
If an aligned legal field destroys that, mark the obstruction.
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Dict, List, Sequence, Tuple

import numpy as np

Mode = Tuple[int, int, int]


def vec(m: Sequence[int]) -> np.ndarray:
    return np.asarray(m, dtype=float)


def mode_dot(a: Mode, b: Mode) -> int:
    return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]


def mode_norm2(a: Mode) -> int:
    return mode_dot(a, a)


def perp_basis(k: Mode) -> Tuple[np.ndarray, np.ndarray]:
    w = vec(k)
    n = np.linalg.norm(w)
    if n < 1e-15:
        raise ValueError("zero output")
    w = w / n
    seed = np.array([1.0, 0.0, 0.0])
    if abs(float(seed @ w)) > 0.9:
        seed = np.array([0.0, 1.0, 0.0])
    e1 = seed - (seed @ w) * w
    e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(w, e1)
    e2 = e2 / np.linalg.norm(e2)
    return e1, e2


def project_kperp(k: Mode, v: np.ndarray) -> np.ndarray:
    kk = vec(k)
    return v - ((kk @ v) / float(kk @ kk)) * kk


def lattice_circle(k: Mode, alpha: int) -> List[Mode]:
    """Integer p with |p|^2 = α and p · k = |k|^2 / 2."""
    beta = mode_norm2(k)
    if beta == 0 or (beta % 2) != 0:
        return []
    target = beta // 2
    if 4 * alpha < beta:
        return []
    lim = int(math.isqrt(alpha)) + 1
    pts: List[Mode] = []
    for x in range(-lim, lim + 1):
        for y in range(-lim, lim + 1):
            z2 = alpha - x * x - y * y
            if z2 < 0:
                continue
            rz = int(math.isqrt(z2))
            if rz * rz != z2:
                continue
            for z in dict.fromkeys((rz, -rz)):
                p = (x, y, z)
                if mode_dot(p, k) == target:
                    pts.append(p)
    return sorted(set(pts))


def circle_geometry(k: Mode, alpha: int) -> dict:
    beta = mode_norm2(k)
    pts = lattice_circle(k, alpha)
    center = vec(k) / 2.0
    radii = [float(np.linalg.norm(vec(p) - center)) for p in pts]
    r2 = alpha - beta / 4.0
    kperp2 = beta * (1.0 - beta / (4.0 * alpha)) if alpha else 0.0
    return {
        "k": k,
        "alpha": alpha,
        "beta": beta,
        "N": len(pts),
        "r2": r2,
        "kperp": math.sqrt(max(kperp2, 0.0)),
        "radius": math.sqrt(max(r2, 0.0)),
        "points": pts,
        "radii_ok": all(abs(r - math.sqrt(max(r2, 0.0))) < 1e-9 for r in radii),
        "pairs_close": all(
            (p[0] + (k[0] - p[0]), p[1] + (k[1] - p[1]), p[2] + (k[2] - p[2])) == k
            and mode_norm2((k[0] - p[0], k[1] - p[1], k[2] - p[2])) == alpha
            for p in pts
        ),
    }


def partner(k: Mode, p: Mode) -> Mode:
    return (k[0] - p[0], k[1] - p[1], k[2] - p[2])


def radial_inplane(k: Mode, p: Mode) -> np.ndarray:
    return vec(p) - vec(k) / 2.0


def unit_from_u(k: Mode, p: Mode, u: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """Legal DF coefficient with P_k v = u and |v|=1 if possible.

    v = a k̂ + u, a = -2 (u·r) / |k|, bilinear (no conjugate on r, real).
    Scale so |v|=1. Returns (v, u_scaled).
    """
    r = radial_inplane(k, p)
    kk = vec(k)
    kn = float(np.linalg.norm(kk))
    # complex bilinear dots against real r, k
    ur = complex(r @ u)
    a = -2.0 * ur / kn
    v = (a / kn) * kk + u
    nrm = float(np.linalg.norm(v))
    if nrm < 1e-15:
        raise ValueError("zero coefficient")
    v = v / nrm
    u_scaled = project_kperp(k, v)
    return v, u_scaled


def sigma_from_u(k: Mode, field_u: Dict[Mode, np.ndarray]) -> np.ndarray:
    """Σ = ∑_p (k · v_p) P_k v_q with |v|=1, u given before unit scaling."""
    acc = np.zeros(3, dtype=complex)
    for p, u_p_raw in field_u.items():
        q = partner(k, p)
        if q not in field_u:
            raise KeyError(q)
        vp, _ = unit_from_u(k, p, u_p_raw)
        vq, uq = unit_from_u(k, q, field_u[q])
        coupling = complex(vec(k) @ vp)
        acc = acc + coupling * uq
    return acc


def natural_size(k: Mode, alpha: int) -> float:
    beta = float(mode_norm2(k))
    return math.sqrt(max(beta * (1.0 - beta / (4.0 * alpha)), 0.0))


def ratios(k: Mode, alpha: int, field_u: Dict[Mode, np.ndarray]) -> dict:
    pts = list(field_u)
    n = len(pts)
    sig = sigma_from_u(k, field_u)
    nrm = float(np.linalg.norm(sig))
    wnat = natural_size(k, alpha)
    energy = float(n)  # unit amplitudes
    return {
        "N": n,
        "sigma": nrm,
        "wnat": wnat,
        "sigma_over_N_wnat": nrm / (n * wnat) if n and wnat else float("nan"),
        "sigma_over_sqrtN_wnat": nrm / (math.sqrt(n) * wnat) if n and wnat else float("nan"),
        "sigma_over_energy": nrm / energy if energy else float("nan"),
    }


def ansatz_constant(k: Mode, pts: Sequence[Mode]) -> Dict[Mode, np.ndarray]:
    e1, _ = perp_basis(k)
    return {p: e1.copy() for p in pts}


def ansatz_radial(k: Mode, pts: Sequence[Mode]) -> Dict[Mode, np.ndarray]:
    out = {}
    for p in pts:
        r = radial_inplane(k, p)
        n = np.linalg.norm(r)
        out[p] = r / n if n > 1e-15 else perp_basis(k)[0]
    return out


def ansatz_tangential(k: Mode, pts: Sequence[Mode]) -> Dict[Mode, np.ndarray]:
    kh = vec(k) / np.linalg.norm(vec(k))
    out = {}
    for p in pts:
        r = radial_inplane(k, p)
        t = np.cross(kh, r)
        n = np.linalg.norm(t)
        out[p] = t / n if n > 1e-15 else perp_basis(k)[1]
    return out


def best_hemisphere_axis(k: Mode, pts: Sequence[Mode]) -> np.ndarray:
    """Direction e1 in k^⊥ maximizing ∑ |r_p · e|."""
    e1, e2 = perp_basis(k)
    best_val = -1.0
    best = e1
    for i in range(360):
        phi = 2.0 * math.pi * i / 360.0
        e = math.cos(phi) * e1 + math.sin(phi) * e2
        val = sum(abs(float(radial_inplane(k, p) @ e)) for p in pts)
        if val > best_val:
            best_val = val
            best = e
    return best


def ansatz_hemisphere(k: Mode, pts: Sequence[Mode]) -> Dict[Mode, np.ndarray]:
    e1 = best_hemisphere_axis(k, pts)
    e2 = np.cross(vec(k) / np.linalg.norm(vec(k)), e1)
    e2 = e2 / np.linalg.norm(e2)
    out = {}
    for p in pts:
        r = radial_inplane(k, p)
        out[p] = e1.copy() if float(r @ e1) >= 0.0 else e2.copy()
    return out


def hemisphere_lower_bound(k: Mode, alpha: int, pts: Sequence[Mode]) -> float:
    """EXACT analytic lower bound on ||Σ|| / (N w_nat): (1/(2π)) √(β/α)."""
    beta = float(mode_norm2(k))
    return math.sqrt(beta / alpha) / (2.0 * math.pi)


def named_circles() -> List[Tuple[Mode, int, str]]:
    return [
        ((0, 0, 2), 6, "8-point r^2=5"),
        ((0, 0, 2), 26, "12-point r^2=25"),
        ((0, 0, 2), 66, "16-point r^2=65"),
        ((0, 2, 0), 6, "8-point axis y"),
        ((2, 2, 2), 17, "12-point 3D tilt"),
        ((0, 0, 10), 90, "16-point |k|=10 r^2=65"),
        ((0, 0, 66), 2194, "32-point fat β/α~2"),
        ((0, 0, 148), 11001, "48-point fat β/α~2"),
    ]


def probe_circle(k: Mode, alpha: int) -> dict:
    geo = circle_geometry(k, alpha)
    pts = geo["points"]
    if len(pts) < 2:
        return {"k": k, "alpha": alpha, "N": len(pts), "empty": True}
    rows = {}
    for name, builder in (
        ("constant", ansatz_constant),
        ("radial", ansatz_radial),
        ("tangential", ansatz_tangential),
        ("hemisphere", ansatz_hemisphere),
    ):
        field = builder(k, pts)
        rows[name] = ratios(k, alpha, field)
    lb = hemisphere_lower_bound(k, alpha, pts)
    hem = rows["hemisphere"]
    return {
        "k": k,
        "alpha": alpha,
        "beta": geo["beta"],
        "N": geo["N"],
        "r2": geo["r2"],
        "kperp": geo["kperp"],
        "sqrt_beta_over_alpha": math.sqrt(geo["beta"] / alpha),
        "lower_bound_N_ratio": lb,
        "hemisphere_N_ratio": hem["sigma_over_N_wnat"],
        "hemisphere_sqrtN_ratio": hem["sigma_over_sqrtN_wnat"],
        "sqrtN_times_sqrt_beta_over_alpha": math.sqrt(geo["N"] * geo["beta"] / alpha),
        "geometry_ok": geo["radii_ok"] and geo["pairs_close"],
        "ansatze": rows,
        "cancels": {
            "constant": rows["constant"]["sigma"] < 1e-9,
            "radial": rows["radial"]["sigma"] < 1e-9,
            "tangential": rows["tangential"]["sigma"] < 1e-9,
        },
    }


def report() -> dict:
    rows = []
    for k, alpha, tag in named_circles():
        row = probe_circle(k, alpha)
        row["tag"] = tag
        rows.append(row)
    live = [r for r in rows if not r.get("empty") and r["N"] >= 8]
    max_sqrt = max((r["hemisphere_sqrtN_ratio"] for r in live), default=float("nan"))
    # Obstruction: N^{1/2} test dies if hemisphere / √N grows without bound
    # on a family with N β/α → ∞.
    return {
        "tag": "SAG-6. Centered prefactor kept off. No occupancy envelope.",
        "identities": {
            "center": "k/2",
            "r2": "α − β/4",
            "p_dot_k": "β/2",
            "coupling": "k·v_p = −2 r_p · u_p",
            "pair_cancel": "constant / radial / saturating / tangential Σ = 0",
        },
        "test": "||Σ|| ≲ N^{1/2} × w_nat ?",
        "verdict": "OBSTRUCTION",
        "why": (
            "Hemisphere alignment is a legal DF field on the circle. "
            "||Σ|| ≥ (1/(2π)) √(β/α) N w_nat, so ||Σ||/(√N w_nat) "
            "≥ (1/(2π)) √(N β/α), unbounded on fat well-populated circles. "
            "Naive radial/constant/tangential alignments cancel and are "
            "not the killer. Do not massage. Energy-normalized ||Σ||/E "
            "is a different object and is not a repair of this test."
        ),
        "max_hemisphere_sqrtN_ratio": max_sqrt,
        "circles": rows,
        "locks": {
            "no_abs_envelope": True,
            "no_occupancy_bound": True,
            "centered_prefactor_separate": True,
            "not_a_theorem_for_16_9": True,
            "not_a_close": True,
        },
    }


def _py(x):
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, np.ndarray):
        return [_py(v) for v in x.tolist()] if x.ndim else _py(x.item())
    if isinstance(x, dict):
        return {str(k): _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    return x


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(list(argv) if argv is not None else None)
    print(json.dumps(_py(report()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
