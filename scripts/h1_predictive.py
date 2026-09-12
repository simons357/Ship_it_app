#!/usr/bin/env python3
"""H1 shape 3 — predictive CF pair tracker.

Not a theorem. H1 is not proved. NS is not solved.
Do not start from ABC_λ. Do not glue to Lemma★.
Do not cash an imposed waiting time.

The Constantin–Fefferman direction law
    D_t ξ = Sξ − (ξ·Sξ)ξ
is predictive: given two high-vorticity blobs, it
forecasts whether a Bad pair stays Bad on the
waiting scale τ = ρ²/ν.

Shape 3 claims NSE forbids persistent sheets and
gaps on that scale. This file tests the reduced
ODE (Rosenhead Biot–Savart + viscous core), not NSE.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np

# Conventional cut so fold, sheet, and a 6ρ gap all start Bad.
# Not the CF paper constant. Report holder, not just the boolean.
C_STAR = 0.35


def _py(x):
    if isinstance(x, (np.floating, np.integer)):
        return x.item()
    if isinstance(x, np.bool_):
        return bool(x)
    if isinstance(x, dict):
        return {k: _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    return x


def _unit(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v))
    if n < 1e-30:
        return np.zeros(3)
    return v / n


def holder(xi1: np.ndarray, xi2: np.ndarray, sep: float, rho: float) -> float:
    """Dimensionless CF ratio |sin φ| / sqrt(sep/ρ)."""
    cross = float(np.linalg.norm(np.cross(xi1, xi2)))
    return cross / math.sqrt(max(sep / max(rho, 1e-30), 1e-30))


def is_bad(h: float, c_star: float = C_STAR) -> bool:
    return h > c_star


def ros_u_S(r: np.ndarray, gamma: np.ndarray, eps2: float) -> Tuple[np.ndarray, np.ndarray]:
    """Rosenhead velocity and strain at offset r from a blob γ = Γ ξ."""
    r2 = float(np.dot(r, r))
    R2 = r2 + eps2
    if R2 < 1e-30:
        return np.zeros(3), np.zeros((3, 3))
    c = 1.0 / (4.0 * math.pi)
    R3 = R2 ** 1.5
    R5 = R2 ** 2.5
    u = c * np.cross(gamma, r) / R3
    # ∂_k u_i = c [ ε_{ijn} γ_j δ_{nk} / R3 − 3 (γ × r)_i r_k / R5 ]
    S = np.zeros((3, 3))
    gx = np.cross(gamma, r)
    for k in range(3):
        ek = np.zeros(3)
        ek[k] = 1.0
        du = c * (np.cross(gamma, ek) / R3 - 3.0 * gx * r[k] / R5)
        S[:, k] += 0.5 * du
        S[k, :] += 0.5 * du
    # Make symmetric part exact (numerical)
    S = 0.5 * (S + S.T)
    return u, S


def rhs(state: np.ndarray, nu: float) -> np.ndarray:
    """state = (x1, x2, xi1, xi2, G1, G2, rho)."""
    x1, x2 = state[0:3], state[3:6]
    xi1, xi2 = _unit(state[6:9]), _unit(state[9:12])
    G1, G2, rho = float(state[12]), float(state[13]), float(max(state[14], 1e-12))
    eps2 = rho * rho
    u21, S21 = ros_u_S(x1 - x2, G2 * xi2, eps2)  # field of 2 at 1
    u12, S12 = ros_u_S(x2 - x1, G1 * xi1, eps2)  # field of 1 at 2
    # Self-strain of a symmetric blob is 0 in this model.
    stretch1 = float(xi1 @ S21 @ xi1)
    stretch2 = float(xi2 @ S12 @ xi2)
    dxi1 = S21 @ xi1 - stretch1 * xi1
    dxi2 = S12 @ xi2 - stretch2 * xi2
    dG1 = stretch1 * G1 - nu * G1 / eps2
    dG2 = stretch2 * G2 - nu * G2 / eps2
    drho = nu / rho  # ρ²' = 2ν ⇒ ρ' = ν/ρ
    out = np.zeros(15)
    out[0:3] = u21
    out[3:6] = u12
    out[6:9] = dxi1
    out[9:12] = dxi2
    out[12] = dG1
    out[13] = dG2
    out[14] = drho
    return out


def rk4_step(state: np.ndarray, dt: float, nu: float) -> np.ndarray:
    k1 = rhs(state, nu)
    k2 = rhs(state + 0.5 * dt * k1, nu)
    k3 = rhs(state + 0.5 * dt * k2, nu)
    k4 = rhs(state + dt * k3, nu)
    nxt = state + (dt / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    nxt[6:9] = _unit(nxt[6:9])
    nxt[9:12] = _unit(nxt[9:12])
    nxt[14] = max(float(nxt[14]), 1e-12)
    return nxt


def pack(x1, x2, xi1, xi2, G1, G2, rho) -> np.ndarray:
    s = np.zeros(15)
    s[0:3] = x1
    s[3:6] = x2
    s[6:9] = _unit(np.asarray(xi1, dtype=float))
    s[9:12] = _unit(np.asarray(xi2, dtype=float))
    s[12] = G1
    s[13] = G2
    s[14] = rho
    return s


def snapshot(state: np.ndarray, t: float, rho0: float, G0: float) -> Dict:
    x1, x2 = state[0:3], state[3:6]
    xi1, xi2 = _unit(state[6:9]), _unit(state[9:12])
    sep = float(np.linalg.norm(x1 - x2))
    rho = float(state[14])
    h = holder(xi1, xi2, sep, rho0)
    return {
        "t": t,
        "sep": sep,
        "rho": rho,
        "G1": float(state[12]),
        "G2": float(state[13]),
        "amp_frac": 0.5 * (abs(state[12]) + abs(state[13])) / max(abs(G0), 1e-30),
        "sin_phi": float(np.linalg.norm(np.cross(xi1, xi2))),
        "holder": h,
        "bad": bool(is_bad(h)),
        "xi1": xi1.tolist(),
        "xi2": xi2.tolist(),
    }


def integrate(
    picture: str,
    x1,
    x2,
    xi1,
    xi2,
    G0: float,
    rho0: float,
    nu: float,
    n_steps: int = 400,
) -> Dict:
    waiting = (rho0 * rho0) / max(nu, 1e-30)
    t_max = 4.0 * waiting
    dt = t_max / n_steps
    state = pack(x1, x2, xi1, xi2, G0, G0, rho0)
    rows = [snapshot(state, 0.0, rho0, G0)]
    t_leave = None
    leave_how = None
    h0 = rows[0]["holder"]
    t_half = None
    for i in range(n_steps):
        state = rk4_step(state, dt, nu)
        t = (i + 1) * dt
        rec = snapshot(state, t, rho0, G0)
        rows.append(rec)
        if t_half is None and rec["holder"] <= 0.5 * h0:
            t_half = t
        if t_leave is None and rows[0]["bad"] and not rec["bad"]:
            t_leave = t
            if rec["amp_frac"] < 0.25 and rec["holder"] > 0.5 * h0:
                leave_how = "amp"
            elif rec["holder"] <= C_STAR:
                leave_how = "align"
            else:
                leave_how = "mixed"
        # keep integrating for the curve
    last = rows[-1]
    persisted = bool(rows[0]["bad"] and last["bad"])
    return {
        "picture": picture,
        "rho0": rho0,
        "nu": nu,
        "G0": G0,
        "waiting": waiting,
        "t_max": t_max,
        "holder0": h0,
        "holder_end": last["holder"],
        "sin_phi0": rows[0]["sin_phi"],
        "sin_phi_end": last["sin_phi"],
        "sep0": rows[0]["sep"],
        "sep_end": last["sep"],
        "amp_end": last["amp_frac"],
        "started_bad": bool(rows[0]["bad"]),
        "ended_bad": bool(last["bad"]),
        "persisted_through_4waiting": persisted,
        "t_leave": t_leave,
        "t_leave_over_waiting": (t_leave / waiting) if t_leave else None,
        "leave_how": leave_how,
        "t_half": t_half,
        "t_half_over_waiting": (t_half / waiting) if t_half else None,
        "holder_rel_change": (last["holder"] - h0) / max(h0, 1e-30),
        "xi_unit_err": max(
            abs(float(np.linalg.norm(state[6:9])) - 1.0),
            abs(float(np.linalg.norm(state[9:12])) - 1.0),
        ),
        "curve": rows[:: max(1, n_steps // 40)],
    }


def pictures(rho0: float = 0.25, G0: float = 1.0, nu: float = 0.02) -> Dict[str, Dict]:
    """Fold / sheet / gap. Not ABC. Not an imposed Burgers strain."""
    z = np.array([0.0, 0.0, 1.0])
    y = np.array([0.0, 1.0, 0.0])
    xhat = np.array([1.0, 0.0, 0.0])
    # Fold: close, 90°, same core scale — large |∇ξ|.
    fold = integrate(
        "fold",
        -0.5 * rho0 * xhat,
        0.5 * rho0 * xhat,
        z,
        y,
        G0,
        rho0,
        nu,
    )
    # Sheet: side-by-side in a plane, 90°, sep = 2ρ — direction jump.
    sheet = integrate(
        "sheet",
        -1.0 * rho0 * xhat,
        1.0 * rho0 * xhat,
        z,
        y,
        G0,
        rho0,
        nu,
    )
    # Gap: distant blobs, 90°. The alternative shape 3 must forbid.
    gap = integrate(
        "gap",
        -3.0 * rho0 * xhat,
        3.0 * rho0 * xhat,
        z,
        y,
        G0,
        rho0,
        nu,
    )
    return {"fold": fold, "sheet": sheet, "gap": gap}


def score(pics: Dict[str, Dict]) -> List[Dict]:
    fold, sheet, gap = pics["fold"], pics["sheet"], pics["gap"]
    unit_ok = all(p["xi_unit_err"] < 1e-8 for p in pics.values())
    # Shape 3: gaps/sheets cannot stay Bad on waiting. This ODE is not NSE.
    gap_persists = gap["persisted_through_4waiting"]
    sheet_persists = sheet["persisted_through_4waiting"]
    return [
        {
            "name": "H1p_xi_unit",
            "claim": "predictive ODE keeps |ξ|=1",
            "verdict": "pass" if unit_ok else "fail",
            "note": "Projection Sξ−(ξ·Sξ)ξ. Identity, not H1.",
        },
        {
            "name": "H1p_not_abc",
            "claim": "probe starts from fold/sheet/gap, not ABC_λ",
            "verdict": "pass",
            "note": "ABC snapshots already scored on the tube door. Do not start H1 from that screenshot.",
        },
        {
            "name": "H1p_waiting_derived",
            "claim": "waiting τ=ρ²/ν is the viscous scale, not an imposed strain lock",
            "verdict": "pass",
            "note": "Burgers locked τ=4 to γ. Here τ is the core diffusion time. Still not a derived NSE persistence time.",
        },
        {
            "name": "H1p_gap_forbidden",
            "claim": "predictive ODE forbids a persistent Bad gap on 4τ",
            "verdict": "fail" if gap_persists or not gap["started_bad"] else "pass",
            "note": (
                "Shape 3 needs NSE to kill gaps. This reduced ODE "
                f"{'kept the gap Bad' if gap_persists else 'cleared the gap'} "
                f"(holder {gap['holder0']:.3f}→{gap['holder_end']:.3f}, "
                f"amp_end={gap['amp_end']:.3f}). Not a theorem."
            ),
            "t_half_over_waiting": gap["t_half_over_waiting"],
            "persisted": gap_persists,
        },
        {
            "name": "H1p_sheet_forbidden",
            "claim": "predictive ODE forbids a persistent Bad sheet on 4τ",
            "verdict": "fail" if sheet_persists or not sheet["started_bad"] else "pass",
            "note": (
                f"holder {sheet['holder0']:.3f}→{sheet['holder_end']:.3f}. "
                "Not a theorem."
            ),
            "persisted": sheet_persists,
        },
        {
            "name": "H1p_shape3",
            "claim": "shape 3 sits (NSE forbids sheets/gaps on r²/ν)",
            "verdict": "fail",
            "note": (
                "The CF ODE is predictive and sits as an ODE. "
                "It is not NSE, and it does not prove sheets/gaps cannot persist. "
                "Shape 3 remains a miss. H1 is not proved."
            ),
        },
        {
            "name": "H1p_not_a_close",
            "claim": "this file closes H1 / WRITE (6)",
            "verdict": "fail",
            "note": "Predictive tracker is a test of shape 3, not the leftover bound. Do not emit H1.",
        },
        {
            "name": "H1p_not_star",
            "claim": "glue this to Lemma★",
            "verdict": "fail",
            "note": "Different integral. Do not merge.",
        },
    ]


def run(rho0: float = 0.25, G0: float = 1.0, nu: float = 0.02) -> Dict:
    pics = pictures(rho0=rho0, G0=G0, nu=nu)
    rows = score(pics)
    by = {r["name"]: r for r in rows}
    return {
        "write": "H1 shape 3 predictive",
        "h1_proved": False,
        "shape3_sits": False,
        "ns_solved": False,
        "started_from_abc": False,
        "glued_to_star": False,
        "rho0": rho0,
        "G0": G0,
        "nu": nu,
        "C_star": C_STAR,
        "pictures": {k: {kk: vv for kk, vv in p.items() if kk != "curve"} for k, p in pics.items()},
        "curves": {k: p["curve"] for k, p in pics.items()},
        "lemmas": rows,
        "verdict": (
            "SHAPE3_NOT_SEATED_H1_OPEN"
            if by["H1p_shape3"]["verdict"] == "fail"
            else "CHECK"
        ),
        "note": (
            "Predictive CF pair tracker on fold/sheet/gap. "
            "Not ABC_λ. Not a close of WRITE (6). NS not solved."
        ),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", type=str, default="")
    ap.add_argument("--rho", type=float, default=0.25)
    ap.add_argument("--G0", type=float, default=1.0)
    ap.add_argument("--nu", type=float, default=0.02)
    args = ap.parse_args()
    print("H1 predictive — shape 3. Not a theorem. NS not solved.", flush=True)
    summary = run(rho0=args.rho, G0=args.G0, nu=args.nu)
    slim = {k: v for k, v in summary.items() if k != "curves"}
    print(json.dumps(_py(slim), indent=2), flush=True)
    if args.out:
        Path(args.out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.out).write_text(json.dumps(_py(summary), indent=2))
        print(f"wrote {args.out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
