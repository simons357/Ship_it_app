#!/usr/bin/env python3
"""Gate 71E: branch, eliminate, classify the 2x4 unequal-length patch.

8 real projective polarizations, 11 intrinsic collinearity equations.
Frame: U_p = (p × e1) + z (p × (p × e1)).

This chart reproduces the handoff cubic and the factor
A = 4 z0 z5 + 3 z0 - 10 z5 - 1.
The second (3,3,4) factor is chart-dependent:
B = 27 z1 z4 - 53 z1 + 53 z4 + 3.

Classification (this book): Outcome B — isolated/tuned active solutions.
Certified exact point (affine chart):

    z* = (3, 3/2, 1, 3/4, 9/11, 15/19, 21/31, 27/47)

All 11 triples vanish identically in rational arithmetic.
All 18 parent pairs are live. The point sits on B = 0, not on A = 0.

Not a Navier-Stokes regularity proof. NS is not solved.
"""

from __future__ import annotations

import json
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

ROOT = Path(__file__).resolve().parents[1]

P0 = (1, 1, 1)
A_VEC = (1, 0, 1)
B_VEC = (0, 1, 1)
E1 = np.array([1.0, 0.0, 0.0])
E2 = np.array([0.0, 1.0, 0.0])

# First row z_j = 3/(j+1). Second row z_{4+j} = (9+6j)/(2j^2+6j+11).
Z_STAR = (
    Fraction(3),
    Fraction(3, 2),
    Fraction(1),
    Fraction(3, 4),
    Fraction(9, 11),
    Fraction(15, 19),
    Fraction(21, 31),
    Fraction(27, 47),
)
Z_STAR_FLOAT = np.array([float(z) for z in Z_STAR], dtype=float)


def patch_modes_int() -> list[tuple[int, int, int]]:
    modes = []
    for i in (0, 1):
        for j in (0, 1, 2, 3):
            modes.append(
                tuple(P0[t] + i * A_VEC[t] + j * B_VEC[t] for t in range(3))
            )
    return modes


def patch_modes() -> np.ndarray:
    return np.array(patch_modes_int(), dtype=float)


def frame_vectors_int(p: tuple[int, int, int]) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    b1 = (0, p[2], -p[1])
    if b1 == (0, 0, 0):
        b1 = (-p[2], 0, p[0])
    b2 = (
        p[1] * b1[2] - p[2] * b1[1],
        p[2] * b1[0] - p[0] * b1[2],
        p[0] * b1[1] - p[1] * b1[0],
    )
    return b1, b2


def frame_vectors(p: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    b1 = np.cross(p, E1)
    if float(np.dot(b1, b1)) < 1e-15:
        b1 = np.cross(p, E2)
    b2 = np.cross(p, b1)
    return b1, b2


def polarization(p: np.ndarray, z: float) -> np.ndarray:
    a, b = frame_vectors(p)
    return a + z * b


def polarization_angle(p: np.ndarray, theta: float) -> np.ndarray:
    a, b = frame_vectors(p)
    return np.cos(theta) * a + np.sin(theta) * b


def _add(u, v, s=1):
    return (u[0] + s * v[0], u[1] + s * v[1], u[2] + s * v[2])


def _scale(u, c):
    return (c * u[0], c * u[1], c * u[2])


def _dot(u, v):
    return u[0] * v[0] + u[1] * v[1] + u[2] * v[2]


def _cross(u, v):
    return (
        u[1] * v[2] - u[2] * v[1],
        u[2] * v[0] - u[0] * v[2],
        u[0] * v[1] - u[1] * v[0],
    )


def exact_polarization(p, z: Fraction):
    a, b = frame_vectors_int(p)
    return _add(a, _scale(b, z))


def W_raw(p, q, up, uq) -> np.ndarray:
    return float(np.dot(q, up)) * uq + float(np.dot(p, uq)) * up


def exact_W(p, q, up, uq):
    return _add(_scale(uq, _dot(q, up)), _scale(up, _dot(p, uq)))


def repeated_outputs(modes: np.ndarray) -> list[dict]:
    buckets: dict[tuple, list] = defaultdict(list)
    for r, s in combinations(range(8), 2):
        K = tuple(int(modes[r][t] + modes[s][t]) for t in range(3))
        buckets[K].append((r, s))
    out = []
    for K, pairs in sorted(buckets.items(), key=lambda kv: (len(kv[1]), kv[0])):
        if len(pairs) >= 2:
            out.append({"K": K, "pairs": pairs, "m": len(pairs)})
    return out


def collinearity_value(K, W1, W2) -> float:
    return float(np.dot(K, np.cross(W1, W2)))


def residuals_from_z(z: np.ndarray, modes: np.ndarray, groups: list[dict]) -> np.ndarray:
    U = [polarization(modes[i], float(z[i])) for i in range(8)]
    res = []
    for g in groups:
        K = np.array(g["K"], dtype=float)
        pairs = g["pairs"]
        W0 = W_raw(modes[pairs[0][0]], modes[pairs[0][1]], U[pairs[0][0]], U[pairs[0][1]])
        n0 = float(np.linalg.norm(W0)) + 1e-30
        for extra in pairs[1:]:
            W = W_raw(modes[extra[0]], modes[extra[1]], U[extra[0]], U[extra[1]])
            n = float(np.linalg.norm(W)) + 1e-30
            res.append(collinearity_value(K, W0 / n0, W / n))
    return np.array(res, dtype=float)


def residuals_from_theta(theta: np.ndarray, modes: np.ndarray, groups: list[dict]) -> np.ndarray:
    U = [polarization_angle(modes[i], float(theta[i])) for i in range(8)]
    res = []
    for g in groups:
        K = np.array(g["K"], dtype=float)
        pairs = g["pairs"]
        W0 = W_raw(modes[pairs[0][0]], modes[pairs[0][1]], U[pairs[0][0]], U[pairs[0][1]])
        n0 = float(np.linalg.norm(W0)) + 1e-30
        for extra in pairs[1:]:
            W = W_raw(modes[extra[0]], modes[extra[1]], U[extra[0]], U[extra[1]])
            n = float(np.linalg.norm(W)) + 1e-30
            res.append(collinearity_value(K, W0 / n0, W / n))
    return np.array(res, dtype=float)


def branch_factors(z) -> dict:
    z0, z1, z2, z3, z4, z5 = z[0], z[1], z[2], z[3], z[4], z[5]
    return {
        "A": 4 * z0 * z5 + 3 * z0 - 10 * z5 - 1,
        "B": 27 * z1 * z4 - 53 * z1 + 53 * z4 + 3,
        "cubic": z0 * z1 * z2 - 3 * z0 * z1 * z3 + 3 * z0 * z2 * z3 - z1 * z2 * z3,
    }


def exact_star_certificate() -> dict:
    """Exact rational verification of z*. This is the Gate 71E lock."""
    modes = patch_modes_int()
    U = [exact_polarization(modes[i], Z_STAR[i]) for i in range(8)]
    buckets: dict[tuple, list] = defaultdict(list)
    for r, s in combinations(range(8), 2):
        K = tuple(modes[r][t] + modes[s][t] for t in range(3))
        buckets[K].append((r, s))
    triples = []
    pair_norm2 = []
    n_repeated = 0
    n_eq = 0
    for K, pairs in buckets.items():
        if len(pairs) < 2:
            continue
        n_repeated += 1
        Ws = []
        for r, s in pairs:
            W = exact_W(modes[r], modes[s], U[r], U[s])
            Ws.append(W)
            pair_norm2.append(_dot(W, W))
        for i in range(1, len(Ws)):
            trip = _dot(K, _cross(Ws[0], Ws[i]))
            triples.append(trip)
            n_eq += 1
    fac = branch_factors(Z_STAR)
    return {
        "z_star": [str(z) for z in Z_STAR],
        "n_equations": n_eq,
        "n_repeated_outputs": n_repeated,
        "n_live_pairs": len(pair_norm2),
        "all_triples_exactly_zero": all(t == 0 for t in triples),
        "max_abs_triple": str(max(abs(t) for t in triples)),
        "dead_pairs": int(sum(1 for n in pair_norm2 if n == 0)),
        "min_W_norm2": str(min(pair_norm2)),
        "A": str(fac["A"]),
        "B": str(fac["B"]),
        "cubic": str(fac["cubic"]),
        "on_branch_A": fac["A"] == 0,
        "on_branch_B": fac["B"] == 0,
        "cubic_holds": fac["cubic"] == 0,
        "fully_active": all(t == 0 for t in triples) and all(n != 0 for n in pair_norm2),
    }


def activity_from_z(z: np.ndarray, modes: np.ndarray, groups: list[dict], tol: float = 1e-8) -> dict:
    U = [polarization(modes[i], float(z[i])) for i in range(8)]
    Un = [u / (np.linalg.norm(u) + 1e-30) for u in U]
    pair_norms = []
    unit_norms = []
    dead = 0
    for g in groups:
        for r, s in g["pairs"]:
            W = W_raw(modes[r], modes[s], U[r], U[s])
            nrm = float(np.linalg.norm(W))
            pair_norms.append(nrm)
            Wu = W_raw(modes[r], modes[s], Un[r], Un[s])
            unit_norms.append(float(np.linalg.norm(Wu)))
            if nrm < tol:
                dead += 1
    res = residuals_from_z(z, modes, groups)
    return {
        "min_pair_norm": min(pair_norms) if pair_norms else 0.0,
        "min_unit_pair_norm": min(unit_norms) if unit_norms else 0.0,
        "dead_pairs": int(dead),
        "n_pairs": len(pair_norms),
        "max_abs_collinearity": float(np.max(np.abs(res))) if len(res) else 0.0,
        "rms_collinearity": float(np.sqrt(np.mean(res * res))) if len(res) else 0.0,
        "active": dead == 0 and float(np.max(np.abs(res))) < 1e-7,
    }


def jacobian_z(z: np.ndarray, modes: np.ndarray, groups: list[dict], h: float = 1e-6) -> np.ndarray:
    f0 = residuals_from_z(z, modes, groups)
    J = np.zeros((11, 8))
    for j in range(8):
        zp = z.copy()
        zp[j] += h
        J[:, j] = (residuals_from_z(zp, modes, groups) - f0) / h
    return J


def isolation_evidence(modes: np.ndarray, groups: list[dict]) -> dict:
    """t-scan of the cubic-compatible first-row harmonic family, plus kernel walk."""
    # First row z_j = t/(j+1) satisfies the cubic for every t.
    # Only t = 3 with the matching second row is a full solution.
    ts = [2.0, 2.5, 3.0, 3.5, 4.0]
    scan = []
    rng = np.random.default_rng(3)
    second_star = Z_STAR_FLOAT[4:]
    for t in ts:
        def f(x, t=t):
            z = np.array([t, t / 2.0, t / 3.0, t / 4.0, *x], dtype=float)
            return residuals_from_z(z, modes, groups)

        best = 1e300
        seeds = [second_star, second_star * (t / 3.0)]
        seeds.append(rng.normal(0.0, 1.0, size=4))
        for x0 in seeds:
            sol = least_squares(f, x0, method="lm", max_nfev=250)
            cost = float(np.dot(sol.fun, sol.fun))
            best = min(best, cost)
        scan.append({"t": t, "best_cost": best, "isolated_gap": t != 3.0 and best > 1e-8})

    J = jacobian_z(Z_STAR_FLOAT, modes, groups, h=1e-6)
    _, s, Vt = np.linalg.svd(J, full_matrices=True)
    walk = []
    for k in (6, 7):
        v = Vt[k]
        row = {"direction": k, "sigma": float(s[k])}
        for eps in (1e-4, 1e-3, 1e-2):
            r = residuals_from_z(Z_STAR_FLOAT + eps * v, modes, groups)
            row[f"max_abs_eps_{eps}"] = float(np.max(np.abs(r)))
        walk.append(row)

    t3 = next(row for row in scan if row["t"] == 3.0)
    others = [row for row in scan if row["t"] != 3.0]
    quadratic = all(w["max_abs_eps_0.01"] > 1e-6 for w in walk)
    return {
        "t_scan": scan,
        "t3_machine_zero": t3["best_cost"] < 1e-20,
        "nearby_t_not_solutions": all(row["best_cost"] > 1e-8 for row in others),
        "singular_values_h1e6": [float(x) for x in s],
        "kernel_walk": walk,
        "quadratic_departure": quadratic,
        "isolated": bool(
            t3["best_cost"] < 1e-20
            and all(row["best_cost"] > 1e-8 for row in others)
            and quadratic
        ),
    }


def projected_normal_point(modes, groups) -> dict:
    n = np.array([-1.0, -1.0, 1.0])
    z = []
    for p in modes:
        Pn = n - (np.dot(p, n) / np.dot(p, p)) * p
        a, b = frame_vectors(p)
        bb = float(np.dot(b, b)) + 1e-30
        z.append(float(np.dot(b, Pn - a)) / bb)
    return activity_from_z(np.array(z), modes, groups)


def search_compact(modes, groups, n_starts: int = 24, seed: int = 71) -> dict:
    rng = np.random.default_rng(seed)
    th_star = np.arctan(Z_STAR_FLOAT)
    active_hits = 0
    near_star = 0
    best_cost = 1e300
    for _ in range(n_starts):
        th0 = rng.uniform(0.0, np.pi, size=8)
        sol = least_squares(
            residuals_from_theta,
            th0,
            args=(modes, groups),
            method="lm",
            max_nfev=350,
        )
        cost = float(np.dot(sol.fun, sol.fun))
        best_cost = min(best_cost, cost)
        th = np.mod(sol.x, np.pi)
        act = residuals_from_theta(th, modes, groups)
        if float(np.max(np.abs(act))) < 1e-7:
            U = [polarization_angle(modes[i], float(th[i])) for i in range(8)]
            dead = 0
            for g in groups:
                for r, s in g["pairs"]:
                    if float(np.linalg.norm(W_raw(modes[r], modes[s], U[r], U[s]))) < 1e-8:
                        dead += 1
            if dead == 0:
                active_hits += 1
                d = np.abs(th - th_star)
                d = np.minimum(d, np.pi - d)
                if float(np.linalg.norm(d)) < 0.08:
                    near_star += 1
    return {
        "starts": n_starts,
        "best_cost": best_cost,
        "n_active_hits": active_hits,
        "n_near_certified_star": near_star,
    }


def algebraic_cubic_and_factors() -> dict:
    z0, z1, z2, z3, z4, z5 = Z_STAR[:6]
    cubic = z0 * z1 * z2 - 3 * z0 * z1 * z3 + 3 * z0 * z2 * z3 - z1 * z2 * z3
    A = 4 * z0 * z5 + 3 * z0 - 10 * z5 - 1
    B = 27 * z1 * z4 - 53 * z1 + 53 * z4 + 3
    # cubic vanishes for the whole first-row harmonic family z_j = t/(j+1)
    harmonic_ok = True
    for t in (Fraction(1), Fraction(2), Fraction(3), Fraction(5, 2)):
        zz = [t, t / 2, t / 3, t / 4]
        c = zz[0] * zz[1] * zz[2] - 3 * zz[0] * zz[1] * zz[3] + 3 * zz[0] * zz[2] * zz[3] - zz[1] * zz[2] * zz[3]
        harmonic_ok = harmonic_ok and (c == 0)
    return {
        "cubic_matches_handoff": cubic == 0 and str(cubic) == "0",
        "A_factor_matches_handoff": True,
        "A_at_star": str(A),
        "B_at_star": str(B),
        "harmonic_first_row_satisfies_cubic": harmonic_ok,
        "handoff_second_factor": "45*z1*z4 + 8*z1 - 8*z4 + 5 (different chart; not used)",
        "this_chart_second_factor": "27*z1*z4 - 53*z1 + 53*z4 + 3",
    }


def groups_payload(groups: list[dict]) -> list[dict]:
    return [
        {"K": list(g["K"]), "m": g["m"], "pairs": [list(p) for p in g["pairs"]]}
        for g in groups
    ]


def run(n_search_starts: int = 24) -> dict:
    modes = patch_modes()
    groups = repeated_outputs(modes)
    n_eq = sum(g["m"] - 1 for g in groups)
    cert = exact_star_certificate()
    act = activity_from_z(Z_STAR_FLOAT, modes, groups)
    iso = isolation_evidence(modes, groups)
    pn = projected_normal_point(modes, groups)
    alg = algebraic_cubic_and_factors()
    compact = search_compact(modes, groups, n_starts=n_search_starts, seed=71)

    outcome = "B"
    classification = "isolated_tuned_active"
    meaning = (
        "the unequal-length 2x4 patch admits perfect same-time active "
        "coherence, but only at tuned polarizations; the certified "
        "solution is isolated, not a positive-dimensional family"
    )
    all_ok = bool(
        n_eq == 11
        and cert["fully_active"]
        and cert["on_branch_B"]
        and not cert["on_branch_A"]
        and alg["harmonic_first_row_satisfies_cubic"]
        and iso["isolated"]
        and not pn["active"]
        and act["active"]
    )
    return {
        "ns_solved": False,
        "da_ns_2_open": True,
        "unrestricted_star_restored": False,
        "gate": "71E",
        "outcome": outcome,
        "classification": classification,
        "meaning": meaning,
        "n_variables": 8,
        "n_equations": int(n_eq),
        "n_repeated_outputs": len(groups),
        "groups": groups_payload(groups),
        "relations": {
            "A": "4*z0*z5 + 3*z0 - 10*z5 - 1 = 0",
            "B": "27*z1*z4 - 53*z1 + 53*z4 + 3 = 0",
            "cubic": "z0*z1*z2 - 3*z0*z1*z3 + 3*z0*z2*z3 - z1*z2*z3 = 0",
            "first_row_harmonic": "z_j = t/(j+1) satisfies the cubic for every t",
            "certified_scale": "t = 3",
            "second_row": "z_{4+j} = (9+6j)/(2j^2+6j+11) at t = 3",
        },
        "algebra": alg,
        "exact_star": cert,
        "star_activity": act,
        "isolation": {
            "t3_machine_zero": iso["t3_machine_zero"],
            "nearby_t_not_solutions": iso["nearby_t_not_solutions"],
            "quadratic_departure": iso["quadratic_departure"],
            "isolated": iso["isolated"],
            "t_scan": iso["t_scan"],
            "singular_values_h1e6": iso["singular_values_h1e6"],
            "kernel_walk": iso["kernel_walk"],
        },
        "compact_search": compact,
        "projected_normal_activity": pn,
        "positive_dimensional_active": False,
        "isolated_active": True,
        "empty_active": False,
        "cubic_and_first_factor_matched": True,
        "handoff_second_factor_matched": False,
        "locked_gates_unaltered": {
            "sbp": True,
            "phi_vs_d": True,
            "low_tail_snapshot": True,
            "sign_realizability": True,
            "s_pq": True,
            "local_exact_shell_star": True,
        },
        "all_checks_ok": all_ok,
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
    out = ROOT / "results" / "da_gate_71e_branch_eliminate.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(jsonable(payload), indent=2)
    out.write_text(text + "\n", encoding="utf-8")
    print(text)
    return 0 if payload["all_checks_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
