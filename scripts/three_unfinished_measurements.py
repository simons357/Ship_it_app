#!/usr/bin/env python3
"""The three unfinished measurements — 25 September 2026.

1. Exercise the (16) positive-part term on a LOCKED field that has S>0.
   The Sept 20 initial datum that produced
   S(1) ≈ 0.001337845, 0.046918627, 0.072599898 is NOT in this tree.
   This is not a reproduction of those numbers.

2. Certified loop upper bound on the locked parallelogram only.
   L_N, M_N, U_N as a general sandwich stay undefined.
   Scale decay Γ_cyc(N) ≲ N^{-δ} stays OPEN. Not a defect of NS.

3. Q vs the η_DA skeleton. α_c and χ_κ are not defined here and
   are not invented. η_DA itself is therefore not evaluated.

Classical NS stays open. DA-NS-2 stays OPEN. (17) stays OPEN.
"""

from __future__ import annotations

import argparse
import json
import math
from typing import Dict, Iterable, List, Tuple

import numpy as np

Mode = Tuple[int, int, int]
CVec = Tuple[complex, complex, complex]
Field = Dict[Mode, np.ndarray]


def _add(a: Mode, b: Mode) -> Mode:
    return (a[0] + b[0], a[1] + b[1], a[2] + b[2])


def _sub(a: Mode, b: Mode) -> Mode:
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


def _lam(k: Mode) -> int:
    return k[0] * k[0] + k[1] * k[1] + k[2] * k[2]


def lattice(n2: int) -> List[Mode]:
    r = int(math.sqrt(n2)) + 1
    out = []
    for i in range(-r, r + 1):
        for j in range(-r, r + 1):
            for k in range(-r, r + 1):
                if i == 0 and j == 0 and k == 0:
                    continue
                if i * i + j * j + k * k <= n2:
                    out.append((i, j, k))
    return out


def odd_field(A: float) -> Field:
    """Locked real-odd Hermitian triad. X=52 A², Y=532 A², T=24 A³."""
    iA = 1j * A
    return {
        (2, 0, 0): np.array([0j, iA, 0j], dtype=complex),
        (-2, 0, 0): np.array([0j, -iA, 0j], dtype=complex),
        (0, 3, 0): np.array([0j, 0j, iA], dtype=complex),
        (0, -3, 0): np.array([0j, 0j, -iA], dtype=complex),
        (2, 3, 0): np.array([0j, 0j, iA], dtype=complex),
        (-2, -3, 0): np.array([0j, 0j, -iA], dtype=complex),
    }


def project_mode(k: Mode, v: np.ndarray) -> np.ndarray:
    lam = float(_lam(k))
    if lam <= 0:
        return np.zeros(3, dtype=complex)
    kv = k[0] * v[0] + k[1] * v[1] + k[2] * v[2]
    return v - (kv / lam) * np.array(k, dtype=complex)


def modal_tau(field: Field, scalene_only: bool = False, highpass_k: float = 0.0) -> Dict[Mode, float]:
    keys = [m for m in field if math.sqrt(_lam(m)) > highpass_k]
    keyset = set(keys)
    t = {m: 0.0 for m in keys}
    for p in keys:
        vp = field[p]
        lp = _lam(p)
        for q in keys:
            k = _add(p, q)
            if k not in keyset:
                continue
            lk = _lam(k)
            lq = _lam(q)
            if scalene_only and len({lp, lq, lk}) < 3:
                continue
            vq = field[q]
            vk = field[k]
            qvp = q[0] * vp[0] + q[1] * vp[1] + q[2] * vp[2]
            vq_vk = vq[0] * vk[0].conjugate() + vq[1] * vk[1].conjugate() + vq[2] * vk[2].conjugate()
            t[k] += float(np.imag(qvp * vq_vk))
    return t


def moments(field: Field, tau: Dict[Mode, float] | None = None) -> dict:
    if tau is None:
        tau = modal_tau(field)
    x = y = z = e = 0.0
    for k, v in field.items():
        ek = float(np.vdot(v, v).real)
        lam = float(_lam(k))
        e += ek
        x += lam * ek
        y += (lam**2) * ek
        z += (lam**3) * ek
    if x <= 0.0:
        return {"E": e, "X": 0.0, "Y": 0.0, "Z": 0.0, "Lambda": 0.0, "D_s": 0.0, "T": 0.0, "T_c": 0.0}
    lam_bar = y / x
    T = 0.0
    tc = 0.0
    for k, tk in tau.items():
        lam = float(_lam(k))
        T += lam * tk
        tc += lam * (lam - lam_bar) * tk
    return {
        "E": e,
        "X": x,
        "Y": y,
        "Z": z,
        "Lambda": lam_bar,
        "D_s": z - lam_bar * y,
        "T": T,
        "T_c": tc,
    }


def T_sc(field: Field, K: float) -> float:
    tau = modal_tau(field, scalene_only=True, highpass_k=K)
    return float(sum(float(_lam(k)) * tk for k, tk in tau.items()))


def integrand_S(field: Field, nu: float, K: float) -> dict:
    m = moments(field)
    tsc = T_sc(field, K)
    raw = tsc - nu * m["Y"] / 4.0
    pos = max(raw, 0.0)
    val = pos / m["X"] if m["X"] > 0.0 else 0.0
    return {
        "T_sc": tsc,
        "T": m["T"],
        "X": m["X"],
        "Y": m["Y"],
        "D_s": m["D_s"],
        "T_c": m["T_c"],
        "raw": raw,
        "positive_part": pos,
        "integrand": val,
        "S_positive": pos > 0.0,
    }


def convective(field: Field, modes: Iterable[Mode]) -> Dict[Mode, np.ndarray]:
    keyset = set(field)
    acc: Dict[Mode, np.ndarray] = {k: np.zeros(3, dtype=complex) for k in modes}
    for p, vp in field.items():
        for q, vq in field.items():
            k = _add(p, q)
            if k not in acc:
                continue
            qvp = q[0] * vp[0] + q[1] * vp[1] + q[2] * vp[2]
            acc[k] = acc[k] + qvp * vq
    out = {}
    for k, conv in acc.items():
        out[k] = project_mode(k, conv)
    return out


def rhs_modal(field: Field, modes: List[Mode], nu: float) -> Field:
    conv = convective(field, modes)
    deriv: Field = {}
    for k in modes:
        v = field.get(k, np.zeros(3, dtype=complex))
        deriv[k] = -nu * float(_lam(k)) * v - 1j * conv[k]
    return deriv


def axpy(field: Field, deriv: Field, dt: float, modes: List[Mode]) -> Field:
    out: Field = {}
    for k in modes:
        out[k] = field.get(k, np.zeros(3, dtype=complex)) + dt * deriv.get(k, np.zeros(3, dtype=complex))
        out[k] = project_mode(k, out[k])
    return {k: v for k, v in out.items() if np.linalg.norm(v) > 1e-16}


def rk4_modal(field: Field, dt: float, modes: List[Mode], nu: float) -> Field:
    k1 = rhs_modal(field, modes, nu)
    y2 = axpy(field, k1, 0.5 * dt, modes)
    k2 = rhs_modal(y2, modes, nu)
    y3 = axpy(field, k2, 0.5 * dt, modes)
    k3 = rhs_modal(y3, modes, nu)
    y4 = axpy(field, k3, dt, modes)
    k4 = rhs_modal(y4, modes, nu)
    out: Field = {}
    for k in modes:
        v = field.get(k, np.zeros(3, dtype=complex))
        v = v + (dt / 6.0) * (
            k1.get(k, 0) + 2 * k2.get(k, 0) + 2 * k3.get(k, 0) + k4.get(k, 0)
        )
        v = project_mode(k, v)
        if np.linalg.norm(v) > 1e-16:
            out[k] = v
    return out


def eta_skeleton(m: dict, nu: float) -> dict:
    """Pieces of (8) that are defined. α_c χ are not invented."""
    X = m["X"]
    Y = m["Y"]
    Ds = m["D_s"]
    Tc = m["T_c"]
    if X <= 0.0 or Y <= 0.0 or Ds <= 0.0:
        return {
            "defined": False,
            "Q_actual": None,
            "skeleton": None,
            "alpha_c_chi": "UNSTAMPED",
            "eta_DA": "NOT_EVALUATED",
        }
    lam = Y / X
    kappa = math.sqrt(lam)
    r = math.sqrt(Ds / Y) / kappa
    Q = max(Tc, 0.0) / (nu * Ds)
    skeleton = math.sqrt(X) / (nu * math.sqrt(kappa) * r)
    return {
        "defined": True,
        "kappa": kappa,
        "r": r,
        "X": X,
        "Y": Y,
        "D_s": Ds,
        "T_c": Tc,
        "T_c_plus": max(Tc, 0.0),
        "Q_actual": Q,
        "skeleton": skeleton,
        "note": (
            "skeleton = sqrt(X)/(nu sqrt(kappa) r) = eta_DA / (alpha_c chi). "
            "Q_actual uses [T_c]_+ not the unreproved local envelope (5). "
            "alpha_c chi UNSTAMPED, so eta_DA is not evaluated."
        ),
        "alpha_c_chi": "UNSTAMPED",
        "eta_DA": "NOT_EVALUATED",
        "local_envelope_5_reproved": False,
    }


def evolve_S(field0: Field, nu: float, K: float, n2: int, T: float, dt: float) -> dict:
    modes = lattice(n2)
    field = {k: project_mode(k, v.copy()) for k, v in field0.items() if _lam(k) <= n2}
    steps = max(1, int(round(T / dt)))
    dt = T / steps
    rows = []
    integ = 0.0
    t = 0.0
    snap = integrand_S(field, nu, K)
    rows.append({"t": 0.0, **{k: snap[k] for k in ("T_sc", "X", "Y", "raw", "positive_part", "integrand", "S_positive", "T_c", "D_s")}})
    eta_rows = [{"t": 0.0, **eta_skeleton({**moments(field), "T_c": snap["T_c"], "D_s": snap["D_s"]}, nu)}]
    ever_positive = bool(snap["S_positive"])
    for _ in range(steps):
        field = rk4_modal(field, dt, modes, nu)
        t += dt
        snap = integrand_S(field, nu, K)
        rows.append({"t": t, **{k: snap[k] for k in ("T_sc", "X", "Y", "raw", "positive_part", "integrand", "S_positive", "T_c", "D_s")}})
        eta_rows.append({"t": t, **eta_skeleton({**moments(field), "T_c": snap["T_c"], "D_s": snap["D_s"]}, nu)})
        integ += snap["integrand"] * dt
        ever_positive = ever_positive or bool(snap["S_positive"])
    return {
        "nu": nu,
        "K": K,
        "N2": n2,
        "T": T,
        "dt": dt,
        "S": integ,
        "ever_positive_part": ever_positive,
        "n_rows": len(rows),
        "rows": rows,
        "eta_rows": eta_rows,
        "final": rows[-1],
        "ns_solved": False,
        "is_sept20_datum": False,
    }


def loop_certified_upper() -> dict:
    from ns_attacks.loop_gauge import parallelogram_report

    rep = parallelogram_report()
    cert = rep["certified"]
    return {
        "family": "locked_parallelogram_4cycle",
        "Omega": 2.0 * math.pi / 3.0,
        "tree": cert["tree"],
        "certified_max": cert["loop"],
        "Gamma_cyc": cert["Gamma_cyc"],
        "method": cert["method"],
        "is_general_L_N_M_N_U_N": False,
        "scale_decay_prize": "OPEN",
        "is_ns_defect": False,
        "reading": (
            "Certified global max against the Γ=1 tree baseline on this "
            "one family. That is an upper bound for this cosine problem. "
            "It is not L_N≤M_N≤U_N in general, not Γ_cyc(N)≲N^{-δ}, "
            "and not a defect of NS."
        ),
    }


def t0_odd_check(A: float = 24.0, nu: float = 1.5) -> dict:
    field = odd_field(A)
    s = integrand_S(field, nu, K=1.0)
    expected_T = 24.0 * A**3
    expected_X = 52.0 * A**2
    expected_Y = 532.0 * A**2
    expected_raw = expected_T - nu * expected_Y / 4.0
    return {
        "T_sc": s["T_sc"],
        "T_expected": expected_T,
        "X": s["X"],
        "X_expected": expected_X,
        "Y": s["Y"],
        "Y_expected": expected_Y,
        "raw": s["raw"],
        "raw_expected": expected_raw,
        "S_positive": s["S_positive"],
        "locks": {
            "T_match": abs(s["T_sc"] - expected_T) < 1e-8,
            "X_match": abs(s["X"] - expected_X) < 1e-8,
            "Y_match": abs(s["Y"] - expected_Y) < 1e-8,
            "positive_part_live": expected_raw > 0.0 and s["S_positive"],
        },
    }


def run_all(dt: float = 0.002, T: float = 1.0) -> dict:
    t0 = t0_odd_check()
    # A=24 is stiff. The positive-part term is already live at t=0.
    # Evolve a milder A=9 that still has S>0 (A>8.3125 at ν=3/2).
    ev20 = evolve_S(odd_field(9.0), nu=1.5, K=1.0, n2=20, T=T, dt=dt)
    loop = loop_certified_upper()
    return {
        "ns_solved": False,
        "da_ns_2": "OPEN",
        "missing_17": "OPEN",
        "sept20_IC": "MISSING",
        "sept20_S1_reported_not_reproduced": [0.001337845, 0.046918627, 0.072599898],
        "sixteen_positive_part": {
            "t0_odd_A24_nu32": t0,
            "evolved_odd_A9_N2_20": {
                "S": ev20["S"],
                "ever_positive_part": ev20["ever_positive_part"],
                "n_rows": ev20["n_rows"],
                "first": ev20["rows"][0],
                "last": ev20["final"],
                "is_sept20_datum": False,
                "field": "locked odd Hermitian triad A=9",
            },
        },
        "loop_certified_upper": loop,
        "eta_DA": {
            "alpha_c_chi": "UNSTAMPED",
            "eta_DA": "NOT_EVALUATED",
            "first": ev20["eta_rows"][0],
            "last": ev20["eta_rows"][-1],
        },
        "evolution": ev20,
    }


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--dt", type=float, default=0.002)
    p.add_argument("--T", type=float, default=1.0)
    p.add_argument("--out", default="results/three_unfinished_measurements.json")
    args = p.parse_args()
    payload = run_all(dt=args.dt, T=args.T)
    # Drop the full row list from the written payload if huge; keep compact.
    compact = dict(payload)
    compact["evolution"] = {
        k: payload["evolution"][k]
        for k in ("nu", "K", "N2", "T", "dt", "S", "ever_positive_part", "n_rows", "final", "is_sept20_datum")
    }
    compact["evolution"]["first"] = payload["evolution"]["rows"][0]
    compact["evolution"]["eta_first"] = payload["evolution"]["eta_rows"][0]
    compact["evolution"]["eta_last"] = payload["evolution"]["eta_rows"][-1]
    text = json.dumps(compact, indent=2)
    with open(args.out, "w", encoding="utf-8") as fh:
        fh.write(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
