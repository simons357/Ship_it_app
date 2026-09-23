"""Short-time interval of N and T_c. Not a close.

Exact Stokes path: u(t)=e^{-ν A t} u_0. Closed form.
Galerkin NSE: integrating-factor RK2 for u_t=-B(u,u)-ν A u
on a sparse Fourier dictionary with an ℓ^∞ cutoff.

A positive-time interval is not a snapshot and not a
t=0 Taylor coefficient. It is still not L^1_loc of a
useful K, and not a named death of G4.

Do not overwrite stokes_moments.py.
Do not restore ★.
Do not seat B★.
Do not start leftover 1.
Do not treat a Galerkin path as a singular NSE solution.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "ns_attacks"))

from stokes_moments import (  # noqa: E402
    enforce_reality,
    k_norm2,
    nonlinear_B,
    probe,
    scale_field,
)
from bstar_attack import separated_triad  # noqa: E402
from fourier_triangle import isosceles_hh_l  # noqa: E402
from ns_lemma_star_core import Field  # noqa: E402
from pathwise import jets  # noqa: E402
from verify_pr24_closure_review import growing_layer_field  # noqa: E402

OUT = ROOT / "results" / "interval.json"
ZERO = np.zeros(3, dtype=np.complex128)


def field_to_stokes_dict(field: Field) -> dict:
    return {k: v.copy() for k, v in field.modes.items()}


def k_linf(k: tuple[int, int, int]) -> int:
    return max(abs(int(k[0])), abs(int(k[1])), abs(int(k[2])))


def cutoff(field: dict, kmax: int, floor: float = 1e-16) -> dict:
    out = {}
    for k, v in field.items():
        if k == (0, 0, 0) or k_linf(k) > kmax:
            continue
        if float(np.vdot(v, v).real) < max(floor, 1e-14):
            continue
        out[k] = v
    return enforce_reality(out)


def stokes_flow(field: dict, nu: float, t: float) -> dict:
    """Exact u(t)=e^{-ν A t} u_0."""
    field = enforce_reality(field)
    if t == 0.0:
        return field
    return {
        k: (math.exp(-nu * k_norm2(k) * t) * v) for k, v in field.items()
    }


def ratios(pr, nu: float = 1.0, theta: float = 0.5) -> dict:
    tc = float(pr.Tc)
    n = float(pr.N)
    m = float(pr.M)
    x = float(pr.X)
    y = float(pr.Y)
    e = float(pr.E)
    ds = float(pr.Ds)
    lam = float(pr.Lambda)
    mn_den = abs(m) + abs(lam) * abs(n)
    k_half = max(tc - theta * nu * ds, 0.0) / x if x > 0 else float("nan")
    return {
        "E": e,
        "X": x,
        "Y": y,
        "Lambda": lam,
        "Ds": ds,
        "N": n,
        "M": m,
        "Tc": tc,
        "n_modes": None,
        "R_mn": (abs(tc) / mn_den) if mn_den > 1e-14 else float("nan"),
        "R_E": (abs(tc) / (math.sqrt(e) * x)) if e > 0 and x > 0 else float("nan"),
        "R_Y": (abs(tc) / (math.sqrt(e) * y)) if e > 0 and y > 0 else float("nan"),
        "K_half": k_half,
        "K_over_sqrtE": (k_half / math.sqrt(e)) if e > 0 else float("nan"),
        "Tc_minus_nu_Ds": tc - nu * ds,
    }


def snapshot(field: dict, label: str, nu: float = 1.0) -> dict:
    field = enforce_reality(field)
    pr = probe(field, label=label)
    row = ratios(pr, nu=nu)
    row["label"] = label
    row["n_modes"] = len(field)
    return row


def sample_times(t_end: float, n_samples: int) -> list[float]:
    return [t_end * i / (n_samples - 1) for i in range(n_samples)]


def stokes_path(field: dict, label: str, nu: float, t_end: float, n_samples: int = 6) -> dict:
    field = enforce_reality(field)
    times = sample_times(t_end, n_samples)
    rows = []
    for t in times:
        row = snapshot(stokes_flow(field, nu, t), f"{label}:t={t:.4g}", nu=nu)
        row["t"] = t
        rows.append(row)
    n0 = rows[0]["N"]
    tc0 = rows[0]["Tc"]
    n_abs = [abs(r["N"]) for r in rows]
    return {
        "label": label,
        "nu": nu,
        "t_end": t_end,
        "rows": rows,
        "N0_is_zero": abs(n0) < 1e-8,
        "N_leaves_zero": n_abs[-1] > 1e-6 * max(1.0, abs(tc0)),
        "N_stays_small": n_abs[-1] < 1e-4 * max(1.0, abs(tc0), n_abs[0] + 1.0),
        "Tc_end_over_Tc0": (rows[-1]["Tc"] / tc0) if abs(tc0) > 1e-14 else float("nan"),
        "R_E0": rows[0]["R_E"],
        "R_E_end": rows[-1]["R_E"],
        "R_mn0": rows[0]["R_mn"],
        "R_mn_min": min(r["R_mn"] for r in rows),
        "K_half0": rows[0]["K_half"],
        "K_half_end": rows[-1]["K_half"],
    }


def ifrk2_step(field: dict, nu: float, dt: float, kmax: int) -> dict:
    """IF-RK2 matching track_b_evolve: decay multiplies the whole increment."""
    field = enforce_reality(field)
    Buu = nonlinear_B(field)
    u1 = {}
    keys = set(field) | set(Buu)
    for k in keys:
        dec = math.exp(-nu * k_norm2(k) * dt)
        u1[k] = dec * (field.get(k, ZERO) - dt * Buu.get(k, ZERO))
    u1 = cutoff(u1, kmax)
    Buu1 = nonlinear_B(u1)
    unew = {}
    keys = set(field) | set(Buu) | set(u1) | set(Buu1)
    for k in keys:
        dec = math.exp(-nu * k_norm2(k) * dt)
        bk = Buu.get(k, ZERO)
        b1 = Buu1.get(k, ZERO)
        unew[k] = dec * (field.get(k, ZERO) - 0.5 * dt * (bk + b1))
    return cutoff(unew, kmax)


def nse_path(
    field: dict,
    label: str,
    nu: float,
    t_end: float,
    dt: float,
    kmax: int,
    record_every: int = 1,
) -> dict:
    field = enforce_reality(field)
    jet0 = jets(field, label, nu=nu)
    steps = max(1, int(round(t_end / dt)))
    dt = t_end / steps
    rows = []
    x_int = 0.0
    u = field
    pr_prev = snapshot(u, f"{label}:t=0", nu=nu)
    pr_prev["t"] = 0.0
    rows.append(pr_prev)
    t = 0.0
    for i in range(steps):
        u = ifrk2_step(u, nu, dt, kmax)
        t = (i + 1) * dt
        pr = snapshot(u, f"{label}:t={t:.4g}", nu=nu)
        pr["t"] = t
        x_int += 0.5 * (pr_prev["X"] + pr["X"]) * dt
        if (i + 1) % record_every == 0 or i + 1 == steps:
            rows.append(pr)
        pr_prev = pr
    e0 = rows[0]["E"]
    e_end = rows[-1]["E"]
    energy_rhs = e0 - 2.0 * nu * x_int
    energy_rel = abs(e_end - energy_rhs) / max(1.0, e0)
    n0 = rows[0]["N"]
    tc0 = rows[0]["Tc"]
    return {
        "label": label,
        "nu": nu,
        "t_end": t_end,
        "dt": dt,
        "steps": steps,
        "kmax": kmax,
        "n_modes0": rows[0]["n_modes"],
        "n_modes_end": rows[-1]["n_modes"],
        "rows": rows,
        "energy_rel": energy_rel,
        "energy_lock": energy_rel < 5e-3,
        "N0_is_zero": abs(n0) < 1e-8,
        "N_end": rows[-1]["N"],
        "N_leaves_zero": abs(rows[-1]["N"]) > 1e-6 * max(1.0, abs(tc0)),
        "N_becomes_negative": rows[-1]["N"] < -1e-8 * max(1.0, abs(tc0)),
        "Tc0": tc0,
        "Tc_end": rows[-1]["Tc"],
        "Tc_grows": rows[-1]["Tc"] > tc0,
        "Tc_end_over_Tc0": (rows[-1]["Tc"] / tc0) if abs(tc0) > 1e-14 else float("nan"),
        "R_E0": rows[0]["R_E"],
        "R_E_end": rows[-1]["R_E"],
        "R_E_stays_large": rows[-1]["R_E"] > 0.5 * rows[0]["R_E"],
        "R_mn0": rows[0]["R_mn"],
        "R_mn_min": min(r["R_mn"] for r in rows),
        "R_mn_stays_high": min(r["R_mn"] for r in rows) > 0.7,
        "K_half0": rows[0]["K_half"],
        "K_half_end": rows[-1]["K_half"],
        "K_over_sqrtE0": rows[0]["K_over_sqrtE"],
        "K_over_sqrtE_end": rows[-1]["K_over_sqrtE"],
        "jet_N_dot": jet0["N_dot"],
        "jet_Tc_dot": jet0["Tc_dot"],
    }


def jet_step_lock(field: dict, nu: float = 1.0, dt: float = 1e-5, kmax: int = 8) -> dict:
    """One tiny NSE step versus the t=0 Gateaux."""
    field = enforce_reality(field)
    jet0 = jets(field, "lock", nu=nu)
    pr0 = snapshot(field, "lock0", nu=nu)
    u1 = ifrk2_step(field, nu, dt, kmax)
    pr1 = snapshot(u1, "lock1", nu=nu)
    n_fd = (pr1["N"] - pr0["N"]) / dt
    tc_fd = (pr1["Tc"] - pr0["Tc"]) / dt
    n_ok = abs(n_fd - jet0["N_dot"]) < 2e-2 * max(1.0, abs(jet0["N_dot"]), abs(n_fd))
    tc_ok = abs(tc_fd - jet0["Tc_dot"]) < 2e-2 * max(1.0, abs(jet0["Tc_dot"]), abs(tc_fd))
    return {
        "N_fd": n_fd,
        "N_jet": jet0["N_dot"],
        "Tc_fd": tc_fd,
        "Tc_jet": jet0["Tc_dot"],
        "N_ok": bool(n_ok),
        "Tc_ok": bool(tc_ok),
        "ok": bool(n_ok and tc_ok),
    }


def amplitude_stokes() -> dict:
    base = field_to_stokes_dict(isosceles_hh_l())
    rows = []
    for a in (0.25, 1.0, 4.0):
        path = stokes_path(scale_field(base, a), f"amp{a}", nu=1.0, t_end=0.02, n_samples=4)
        rows.append(
            {
                "amp": a,
                "R_E0": path["R_E0"],
                "R_E_end": path["R_E_end"],
                "R_mn0": path["R_mn0"],
                "N0_is_zero": path["N0_is_zero"],
            }
        )
    r0 = [r["R_E0"] for r in rows]
    return {
        "rows": rows,
        "R_E0_flat": max(r0) / min(r0) < 1.02,
    }


def record() -> dict:
    v1 = growing_layer_field(1)
    v4 = growing_layer_field(4)
    tri = field_to_stokes_dict(isosceles_hh_l())
    sep1 = separated_triad(1)

    lock = jet_step_lock(v1, nu=1.0, dt=1e-5, kmax=8)
    amp = amplitude_stokes()

    stokes = [
        stokes_path(v1, "vn1", nu=1.0, t_end=0.05, n_samples=6),
        stokes_path(v4, "vn4", nu=1.0, t_end=0.01, n_samples=5),
        stokes_path(growing_layer_field(8), "vn8", nu=1.0, t_end=0.004, n_samples=4),
        stokes_path(tri, "tri", nu=1.0, t_end=0.05, n_samples=4),
    ]
    vn_stokes = [p for p in stokes if p["label"].startswith("vn")]

    nse = [
        nse_path(v1, "vn1", nu=1.0, t_end=0.02, dt=0.004, kmax=6, record_every=2),
        nse_path(scale_field(v1, 4.0), "vn1a4", nu=1.0, t_end=0.006, dt=0.001, kmax=6, record_every=2),
        nse_path(tri, "tri", nu=1.0, t_end=0.02, dt=0.004, kmax=6, record_every=2),
        nse_path(sep1, "sep1", nu=1.0, t_end=0.016, dt=0.004, kmax=6, record_every=2),
        nse_path(v1, "vn1_euler", nu=0.0, t_end=0.006, dt=0.001, kmax=6, record_every=2),
    ]
    vn_nse = [p for p in nse if p["label"] in ("vn1", "vn1a4")]
    vn1 = next(p for p in nse if p["label"] == "vn1")
    vn1a4 = next(p for p in nse if p["label"] == "vn1a4")
    vn1_eu = next(p for p in nse if p["label"] == "vn1_euler")

    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "bstar_not_seated": True,
        "not_a_singular_solution": True,
        "identities": {
            "stokes_path": "u(t)=e^{-ν A t} u_0, exact",
            "energy": "E' = -2ν X  (Galerkin)",
            "Lambda_prime": "Λ' = 2/X (T_c − ν D_s)",
        },
        "jet_lock": lock,
        "amplitude": amp,
        "stokes": [
            {
                "label": p["label"],
                "t_end": p["t_end"],
                "N0_is_zero": p["N0_is_zero"],
                "N_leaves_zero": p["N_leaves_zero"],
                "N_stays_small": p["N_stays_small"],
                "Tc_end_over_Tc0": p["Tc_end_over_Tc0"],
                "R_E0": p["R_E0"],
                "R_E_end": p["R_E_end"],
                "R_mn0": p["R_mn0"],
                "R_mn_min": p["R_mn_min"],
                "K_half0": p["K_half0"],
                "K_half_end": p["K_half_end"],
                "N_end": p["rows"][-1]["N"],
                "Tc0": p["rows"][0]["Tc"],
                "Tc_end": p["rows"][-1]["Tc"],
            }
            for p in stokes
        ],
        "nse": [
            {
                "label": p["label"],
                "nu": p["nu"],
                "t_end": p["t_end"],
                "energy_lock": p["energy_lock"],
                "energy_rel": p["energy_rel"],
                "N0_is_zero": p["N0_is_zero"],
                "N_end": p["N_end"],
                "N_leaves_zero": p["N_leaves_zero"],
                "N_becomes_negative": p["N_becomes_negative"],
                "Tc0": p["Tc0"],
                "Tc_end": p["Tc_end"],
                "Tc_grows": p["Tc_grows"],
                "Tc_end_over_Tc0": p["Tc_end_over_Tc0"],
                "R_E0": p["R_E0"],
                "R_E_end": p["R_E_end"],
                "R_E_stays_large": p["R_E_stays_large"],
                "R_mn0": p["R_mn0"],
                "R_mn_min": p["R_mn_min"],
                "R_mn_stays_high": p["R_mn_stays_high"],
                "K_half0": p["K_half0"],
                "K_half_end": p["K_half_end"],
                "K_over_sqrtE0": p["K_over_sqrtE0"],
                "K_over_sqrtE_end": p["K_over_sqrtE_end"],
                "n_modes0": p["n_modes0"],
                "n_modes_end": p["n_modes_end"],
            }
            for p in nse
        ],
        "stokes_vn_N0_zero": all(p["N0_is_zero"] for p in vn_stokes),
        "stokes_vn_N_stays_small": all(p["N_stays_small"] for p in vn_stokes),
        "stokes_vn_R_mn_stays_one": all(p["R_mn_min"] > 0.99 for p in vn_stokes),
        "nse_energy_lock": all(p["energy_lock"] for p in nse if p["nu"] > 0),
        "nse_vn_N_leaves_zero": all(p["N_leaves_zero"] for p in vn_nse),
        "nse_vn_N_negative": all(p["N_becomes_negative"] for p in vn_nse),
        "nse_vn_Tc_grows": all(p["Tc_grows"] for p in vn_nse),
        "nse_vn_R_E_stays_large": all(p["R_E_stays_large"] for p in vn_nse),
        "nse_vn_R_mn_stays_high": all(p["R_mn_stays_high"] for p in vn_nse),
        "nse_vn_R_mn_stays_one": all(p["R_mn_min"] > 0.99 for p in vn_nse),
        "nse_euler_N_negative": vn1_eu["N_becomes_negative"],
        "nse_euler_Tc_grows": vn1_eu["Tc_grows"],
        "amp_large_K_not_killed_by_viscosity": vn1a4["K_half_end"] > 0.5 * vn1a4["K_half0"],
        "vn1_Tc_end_over_Tc0": vn1["Tc_end_over_Tc0"],
        "vn1_N_end": vn1["N_end"],
        "vn1a4_K_half0": vn1a4["K_half0"],
        "vn1a4_K_half_end": vn1a4["K_half_end"],
        "sits_as_useful_K": False,
        "sits_as_g4_death": False,
        "g4_stays_open": True,
        "jet_lock_ok": bool(lock["ok"]),
        "R_E0_amp_flat": bool(amp["R_E0_flat"]),
    }
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
