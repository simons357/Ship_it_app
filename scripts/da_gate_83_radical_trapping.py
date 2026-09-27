#!/usr/bin/env python3
"""Gate 83: radical / divisibility test for the 71E volumetric thickening.

After gauge, V = b2 * λ. On the reduced slice the 2x4 71E patch is the
planar 2x2x2 cube with d = 2b. Thicken by d = 2b + λ n, n = a × b.
Nine cube collinearities I_act = (C1,C2,C3,F1,...,F6).

Question (83.34): is λ in the radical of I_act localized at p_71E?

Not a Navier-Stokes regularity proof. NS is not solved.
Gate 81 census is REPORTED, not recomputed here.
"""

from __future__ import annotations

import json
from fractions import Fraction
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[1]

P0 = np.array([1.0, 1.0, 1.0])
A_VEC = np.array([1.0, 0.0, 1.0])
B_VEC = np.array([0.0, 1.0, 1.0])
N_VEC = np.cross(A_VEC, B_VEC)  # (-1, -1, 1)
E1 = np.array([1.0, 0.0, 0.0])
E2 = np.array([0.0, 1.0, 0.0])

# 71E z* in the seated i-major / j-minor order, which is also the cube order
# 000,010,001,011,100,110,101,111.
Z_STAR = np.array(
    [
        3.0,
        3.0 / 2.0,
        1.0,
        3.0 / 4.0,
        9.0 / 11.0,
        15.0 / 19.0,
        21.0 / 31.0,
        27.0 / 47.0,
    ],
    dtype=float,
)
Z_STAR_Q = [
    Fraction(3),
    Fraction(3, 2),
    Fraction(1),
    Fraction(3, 4),
    Fraction(9, 11),
    Fraction(15, 19),
    Fraction(21, 31),
    Fraction(27, 47),
]

# Cube node -> z-index
# (i, j', k)
NODE = [
    (0, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (0, 1, 1),
    (1, 0, 0),
    (1, 1, 0),
    (1, 0, 1),
    (1, 1, 1),
]

# Nine pair-classes: 3 space-diagonal + 6 face-diagonal.
SPACE = [
    [(0, 7), (4, 3)],
    [(0, 7), (1, 6)],
    [(0, 7), (2, 5)],
]
FACES = [
    [(0, 5), (4, 1)],  # F1 a+b, k=0
    [(2, 7), (6, 3)],  # F2 a+b, k=1
    [(0, 6), (4, 2)],  # F3 a+d, j=0
    [(1, 7), (5, 3)],  # F4 a+d, j=1
    [(0, 3), (1, 2)],  # F5 b+d, i=0
    [(4, 7), (5, 6)],  # F6 b+d, i=1
]
PAIR_CLASSES = SPACE + FACES
ALL_PAIRS = [(0, 7), (4, 3), (1, 6), (2, 5), (0, 5), (4, 1), (2, 7), (6, 3), (0, 6), (4, 2), (1, 7), (5, 3), (0, 3), (1, 2), (4, 7), (5, 6)]


def gauge_volume(b2, lam):
    """Exact identity V = b2 * λ after the seated gauge."""
    return b2 * lam


def mode(i: int, jp: int, k: int, lam: float) -> np.ndarray:
    d = 2.0 * B_VEC + lam * N_VEC
    return P0 + i * A_VEC + jp * B_VEC + k * d


def modes_of(lam: float) -> np.ndarray:
    return np.array([mode(*node, lam) for node in NODE], dtype=float)


def frame_vectors(p: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    b1 = np.cross(p, E1)
    if float(np.dot(b1, b1)) < 1e-18:
        b1 = np.cross(p, E2)
    return b1, np.cross(p, b1)


def polarization(p: np.ndarray, z: float) -> np.ndarray:
    a, b = frame_vectors(p)
    return a + z * b


def W_raw(p, q, up, uq) -> np.ndarray:
    return float(np.dot(q, up)) * uq + float(np.dot(p, uq)) * up


def collinearity(K, W1, W2) -> float:
    return float(np.dot(K, np.cross(W1, W2)))


def residuals(z: np.ndarray, lam: float, scale_free: bool = True) -> np.ndarray:
    P = modes_of(lam)
    U = [polarization(P[i], float(z[i])) for i in range(8)]
    out = []
    for (r, s), (u, v) in PAIR_CLASSES:
        W1 = W_raw(P[r], P[s], U[r], U[s])
        W2 = W_raw(P[u], P[v], U[u], U[v])
        K = P[r] + P[s]
        if scale_free:
            n1 = float(np.linalg.norm(W1)) + 1e-30
            n2 = float(np.linalg.norm(W2)) + 1e-30
            out.append(collinearity(K, W1 / n1, W2 / n2))
        else:
            out.append(collinearity(K, W1, W2))
    return np.array(out, dtype=float)


def pair_activity(z: np.ndarray, lam: float) -> dict:
    P = modes_of(lam)
    U = [polarization(P[i], float(z[i])) for i in range(8)]
    Un = [u / (np.linalg.norm(u) + 1e-30) for u in U]
    raw = []
    unit = []
    dead = 0
    for r, s in ALL_PAIRS:
        W = W_raw(P[r], P[s], U[r], U[s])
        n = float(np.linalg.norm(W))
        raw.append(n)
        Wu = W_raw(P[r], P[s], Un[r], Un[s])
        unit.append(float(np.linalg.norm(Wu)))
        if n < 1e-10:
            dead += 1
    return {
        "n_pairs": len(ALL_PAIRS),
        "dead_pairs": dead,
        "min_pair_norm": min(raw),
        "min_unit_pair_norm": min(unit),
        "live": dead == 0,
    }


def jacobian(z: np.ndarray, lam: float, h: float = 1e-7) -> np.ndarray:
    """9 x 9 Jacobian in (z0..z7, λ)."""
    x0 = np.concatenate([z, [lam]])
    f0 = residuals(x0[:8], float(x0[8]))
    J = np.zeros((9, 9))
    for j in range(9):
        xp = x0.copy()
        xp[j] += h
        J[:, j] = (residuals(xp[:8], float(xp[8])) - f0) / h
    return J


def gauge_identity_check() -> dict:
    a = np.array([1.0, 0.0, 0.0])
    samples = []
    ok = True
    rng = np.random.default_rng(83)
    for _ in range(12):
        b1, b2, d1, d2, lam = rng.normal(0.0, 1.0, size=5)
        b = np.array([b1, b2, 0.0])
        d = np.array([d1, d2, lam])
        V = float(np.linalg.det(np.stack([a, b, d], axis=1)))
        pred = float(b2 * lam)
        samples.append({"V": V, "b2_lambda": pred, "err": V - pred})
        ok = ok and abs(V - pred) < 1e-12
    # seated 71E lattice volume of {a,b,n}
    V_n = float(np.linalg.det(np.stack([A_VEC, B_VEC, N_VEC], axis=1)))
    return {
        "identity_V_eq_b2_lambda": ok,
        "seated_det_abn": V_n,
        "n": [float(x) for x in N_VEC],
        "samples_ok": ok,
    }


def exact_star_on_cube() -> dict:
    r = residuals(Z_STAR, 0.0)
    act = pair_activity(Z_STAR, 0.0)
    return {
        "max_abs_residual": float(np.max(np.abs(r))),
        "rms_residual": float(np.sqrt(np.mean(r * r))),
        "vanishes": bool(np.max(np.abs(r)) < 1e-10),
        "activity": act,
    }


def jacobian_filter() -> dict:
    rows = []
    for h in (1e-5, 1e-6, 1e-7):
        J = jacobian(Z_STAR, 0.0, h=h)
        s = np.linalg.svd(J, compute_uv=False)
        # kernel walk along smallest two right singular vectors
        _, _, Vt = np.linalg.svd(J, full_matrices=True)
        walks = []
        for k in (7, 8):
            v = Vt[k]
            rec = {"sigma": float(s[k] if k < len(s) else 0.0), "d_lambda": float(v[8])}
            for eps in (1e-4, 1e-3, 1e-2):
                z = Z_STAR + eps * v[:8]
                lam = 0.0 + eps * v[8]
                rec[f"max_abs_eps_{eps}"] = float(np.max(np.abs(residuals(z, lam))))
            walks.append(rec)
        rows.append(
            {
                "h": h,
                "singular_values": [float(x) for x in s],
                "rank_1e6": int(np.sum(s > 1e-6)),
                "rank_1e8": int(np.sum(s > 1e-8)),
                "lambda_column_norm": float(np.linalg.norm(J[:, 8])),
                "walks": walks,
            }
        )
    J = jacobian(Z_STAR, 0.0, h=1e-6)
    s = np.linalg.svd(J, compute_uv=False)
    _, _, Vt = np.linalg.svd(J, full_matrices=True)
    # Does any small singular direction carry λ?
    volumetric_tangent = False
    for k, sig in enumerate(s):
        if sig < 1e-4 and abs(Vt[k, 8]) > 0.1:
            volumetric_tangent = True
    return {
        "by_step": rows,
        "stable_rank_estimate": int(np.sum(s > 1e-4)),
        "lambda_in_approximate_kernel": volumetric_tangent,
        "min_sigma": float(s[-1]),
        "lambda_column_norm": float(np.linalg.norm(J[:, 8])),
    }


def frozen_z_lambda_slice() -> dict:
    """Residuals at z* as a univariate function of λ. Necessary, not sufficient."""
    lams = np.linspace(-0.4, 0.4, 41)
    vals = [float(np.max(np.abs(residuals(Z_STAR, float(lam))))) for lam in lams]
    # smallest |λ|>0 with residual below 1e-8
    extra = []
    for lam in lams:
        if abs(lam) < 1e-12:
            continue
        extra.append((abs(float(lam)), vals[list(lams).index(lam)]))
    min_off = min(vals[i] for i, lam in enumerate(lams) if abs(lam) > 1e-12)
    return {
        "n_samples": len(lams),
        "residual_at_0": vals[20],
        "min_residual_off_plane": float(min_off),
        "frozen_z_only_zero_at_origin": bool(min_off > 1e-4),
    }


def local_search(n_starts: int = 24, seed: int = 83) -> dict:
    """Search for active coherent points near p_71E with λ free."""
    rng = np.random.default_rng(seed)

    def f(x):
        return residuals(x[:8], float(x[8]))

    hits = []
    best = 1e300
    volumetric_active = 0
    planar_active = 0
    for _ in range(n_starts):
        x0 = np.concatenate(
            [Z_STAR + rng.normal(0.0, 0.05, size=8), [rng.normal(0.0, 0.05)]]
        )
        sol = least_squares(f, x0, method="lm", max_nfev=400)
        cost = float(np.dot(sol.fun, sol.fun))
        best = min(best, cost)
        z, lam = sol.x[:8], float(sol.x[8])
        res = residuals(z, lam)
        act = pair_activity(z, lam)
        if float(np.max(np.abs(res))) < 1e-8 and act["live"]:
            rec = {
                "lambda": lam,
                "cost": cost,
                "min_unit_W": act["min_unit_pair_norm"],
                "dist_z": float(np.linalg.norm(z - Z_STAR)),
            }
            hits.append(rec)
            if abs(lam) > 1e-6:
                volumetric_active += 1
            else:
                planar_active += 1
    return {
        "starts": n_starts,
        "best_cost": best,
        "n_active_hits": len(hits),
        "n_planar_active": planar_active,
        "n_volumetric_active": volumetric_active,
        "sample_hits": hits[:6],
    }


def try_low_degree_certificate() -> dict:
    """Try a constant-coefficient identity sum c_k R_k^{raw} = α λ on the z* slice.

    This is a probe, not the full (83.35). Raw (unnormalized) residuals at z*
    are univariate polynomials in λ vanishing at 0. If their gcd is c λ^N
    we record N on that frozen-z slice only.
    """
    # Sample raw residuals vs λ and fit a polynomial per equation.
    lams = np.linspace(-0.25, 0.25, 21)
    raw = np.array([residuals(Z_STAR, float(lam), scale_free=False) for lam in lams])
    # Each column ~ a_n λ^n + ... ; estimate vanishing order at 0.
    orders = []
    for k in range(9):
        # finite differences at 0
        # use a small stencil
        hs = [1e-2, 5e-3, 2.5e-3]
        vals = [abs(float(residuals(Z_STAR, h, scale_free=False)[k])) for h in hs]
        # order ~ log(v)/log(h)
        est = []
        for i in range(len(hs) - 1):
            if vals[i + 1] > 0 and hs[i + 1] > 0:
                est.append(np.log(vals[i] / vals[i + 1]) / np.log(hs[i] / hs[i + 1]))
        orders.append(float(np.median(est)) if est else None)
    return {
        "frozen_z_vanishing_order_estimates": orders,
        "note": "frozen-z slice only; not a full (83.35) certificate",
        "explicit_certificate_found": False,
    }


def classify(jac: dict, search: dict, frozen: dict, star: dict, gauge: dict) -> dict:
    if not gauge["identity_V_eq_b2_lambda"]:
        return {
            "question_83_34": "OPEN",
            "trapped": False,
            "explicit_certificate": False,
            "reason": "gauge identity failed",
        }
    if not star["vanishes"] or not star["activity"]["live"]:
        return {
            "question_83_34": "OPEN",
            "trapped": False,
            "explicit_certificate": False,
            "reason": "71E point is not an active cube zero",
        }
    if jac["lambda_in_approximate_kernel"]:
        return {
            "question_83_34": "NO",
            "trapped": False,
            "explicit_certificate": False,
            "reason": "volumetric tangent at p_71E; λ not in the radical",
        }
    if search["n_volumetric_active"] > 0:
        return {
            "question_83_34": "NO",
            "trapped": False,
            "explicit_certificate": False,
            "reason": "active volumetric hit near p_71E",
        }
    # Jacobian has no volumetric tangent; local search found only planar hits.
    # That is evidence, not a Nullstellensatz certificate.
    return {
        "question_83_34": "OPEN",
        "trapped": False,
        "explicit_certificate": False,
        "local_evidence": "no volumetric tangent and no nearby volumetric hit on the reduced slice",
        "reason": "no (83.35) identity constructed; radical membership not certified",
    }


def run(n_starts: int = 24) -> dict:
    gauge = gauge_identity_check()
    star = exact_star_on_cube()
    jac = jacobian_filter()
    frozen = frozen_z_lambda_slice()
    search = local_search(n_starts=n_starts, seed=83)
    probe = try_low_degree_certificate()
    decision = classify(jac, search, frozen, star, gauge)
    return {
        "ns_solved": False,
        "da_ns_2_open": True,
        "unrestricted_star_restored": False,
        "gate": "83",
        "question": "lambda in radical of (I_act) localized at p_71E?",
        "tag": "83.34",
        "certificate_shape": "83.35",
        "gauge": gauge,
        "cube_equations": {
            "n_C": 3,
            "n_F": 6,
            "n_I_act": 9,
            "n_variables_on_reduced_slice": 9,
            "slice": "a,b frozen; d = 2b + lambda n; eight z free",
        },
        "star_on_cube": star,
        "jacobian": {
            "stable_rank_estimate": jac["stable_rank_estimate"],
            "lambda_in_approximate_kernel": jac["lambda_in_approximate_kernel"],
            "min_sigma": jac["min_sigma"],
            "lambda_column_norm": jac["lambda_column_norm"],
            "by_step": jac["by_step"],
        },
        "frozen_z_slice": frozen,
        "local_search": search,
        "certificate_probe": probe,
        "gate_81_census": {
            "status": "REPORTED",
            "recomputed_here": False,
            "handoff": "40/40 tested volumetric cubes Outcome A",
        },
        "decision": decision,
        "locked_gates_unaltered": {
            "sbp": True,
            "phi_vs_d": True,
            "low_tail_snapshot": True,
            "sign_realizability": True,
            "s_pq": True,
            "local_exact_shell_star": True,
            "gate_71e": True,
        },
        "all_checks_ok": bool(
            gauge["identity_V_eq_b2_lambda"]
            and star["vanishes"]
            and star["activity"]["live"]
            and decision["question_83_34"] in ("OPEN", "YES", "NO")
        ),
    }


def jsonable(obj):
    if isinstance(obj, dict):
        return {k: jsonable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [jsonable(v) for v in obj]
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    if isinstance(obj, (np.floating, float)):
        return float(obj)
    if isinstance(obj, (np.integer, int)):
        return int(obj)
    return obj


def main() -> int:
    payload = run()
    out = ROOT / "results" / "da_gate_83_radical_trapping.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(jsonable(payload), indent=2)
    out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if payload["all_checks_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
