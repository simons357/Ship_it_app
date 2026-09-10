#!/usr/bin/env python3
"""
H1 on one cylinder: J and thinness on explicit tubes.

Classical NS. No Q1. No K(t). No GCD matrix.
Not a regularity proof. One tube is not a uniform constant.
The Ring Lemma direction bound is not assumed.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np

from track_b_lemmas import curl, fft, ifft, make_grid, rec


VOL_T3 = (2.0 * math.pi) ** 3
EC_FRAC = 0.35


def _integrate(field: np.ndarray, dx: float) -> float:
    return float(np.sum(field)) * dx**3


def _mag(ax, ay, az) -> np.ndarray:
    return np.sqrt(ax * ax + ay * ay + az * az)


def _xi(ox, oy, oz, eps: float = 1e-14):
    mag = _mag(ox, oy, oz)
    safe = np.maximum(mag, eps)
    return ox / safe, oy / safe, oz / safe, mag


def _jac_frob2_spectral(sx, sy, sz, kx, ky, kz) -> np.ndarray:
    acc = np.zeros_like(sx)
    for comp in (sx, sy, sz):
        ch = fft(comp)
        acc = acc + ifft(1j * kx * ch) ** 2
        acc = acc + ifft(1j * ky * ch) ** 2
        acc = acc + ifft(1j * kz * ch) ** 2
    return acc


def _jac_frob2_fd(sx, sy, sz, dx: float) -> np.ndarray:
    acc = np.zeros_like(sx)
    for comp in (sx, sy, sz):
        gx, gy, gz = np.gradient(comp, dx, dx, dx, edge_order=1)
        acc = acc + gx * gx + gy * gy + gz * gz
    return acc


def _strain_stretch_spectral(uh, vh, wh, kx, ky, kz, ox, oy, oz):
    d = [[ifft(1j * k * h) for k in (kx, ky, kz)] for h in (uh, vh, wh)]
    s00, s11, s22 = d[0][0], d[1][1], d[2][2]
    s01 = 0.5 * (d[0][1] + d[1][0])
    s02 = 0.5 * (d[0][2] + d[2][0])
    s12 = 0.5 * (d[1][2] + d[2][1])
    stretch = (
        ox * (s00 * ox + s01 * oy + s02 * oz)
        + oy * (s01 * ox + s11 * oy + s12 * oz)
        + oz * (s02 * ox + s12 * oy + s22 * oz)
    )
    return stretch


def _strain_stretch_fd(u, v, w, ox, oy, oz, dx: float):
    uu = np.gradient(u, dx, dx, dx, edge_order=1)
    vv = np.gradient(v, dx, dx, dx, edge_order=1)
    ww = np.gradient(w, dx, dx, dx, edge_order=1)
    s00, s11, s22 = uu[0], vv[1], ww[2]
    s01 = 0.5 * (uu[1] + vv[0])
    s02 = 0.5 * (uu[2] + ww[0])
    s12 = 0.5 * (vv[2] + ww[1])
    stretch = (
        ox * (s00 * ox + s01 * oy + s02 * oz)
        + oy * (s01 * ox + s11 * oy + s12 * oz)
        + oz * (s02 * ox + s12 * oy + s22 * oz)
    )
    return stretch


def _ec_mask(mag: np.ndarray, frac: float = EC_FRAC) -> np.ndarray:
    peak = float(np.max(mag))
    return mag >= frac * peak


def _sample(
    name: str,
    *,
    amp: float,
    ox,
    oy,
    oz,
    u,
    v,
    w,
    stretch,
    jac2,
    dx: float,
    rho: float,
    length: float,
    tube_mask: np.ndarray | None,
    note: str,
) -> dict:
    mag = _mag(ox, oy, oz)
    ec = _ec_mask(mag)
    if tube_mask is None:
        tube_mask = ec
    j_ec = _integrate(jac2 * mag * ec, dx)
    x_ec = _integrate((mag * mag) * ec, dx)
    x_full = _integrate(mag * mag, dx)
    x_tube = _integrate((mag * mag) * tube_mask, dx)
    e_full = _integrate(u * u + v * v + w * w, dx)
    e_tube = _integrate((u * u + v * v + w * w) * tube_mask, dx)
    mag2 = np.maximum(mag * mag, 1e-30)
    rate = stretch / mag2
    rate_pos = np.maximum(rate, 0.0)
    if np.any(ec):
        stretch_inf = float(np.max(rate_pos[ec]))
        stretch_mean = float(np.mean(rate[ec]))
    else:
        stretch_inf = 0.0
        stretch_mean = 0.0
    lhs = rho * rho * x_tube
    lhs_full = rho * rho * x_full
    return {
        "name": name,
        "amp": float(amp),
        "rho": float(rho),
        "L": float(length),
        "J_ec": j_ec,
        "X_ec": x_ec,
        "X_full": x_full,
        "X_tube": x_tube,
        "E_full": e_full,
        "E_tube": e_tube,
        "thinness_lhs": lhs,
        "thinness_lhs_full": lhs_full,
        "thinness_ratio_tube": lhs / max(e_tube, 1e-30),
        "thinness_ratio_full": lhs_full / max(e_full, 1e-30),
        "J_over_X": j_ec / max(x_full, 1e-30),
        "stretch_inf_plus": stretch_inf,
        "stretch_mean": stretch_mean,
        "n_ec": int(np.sum(ec)),
        "frac_ec": float(np.mean(ec)),
        "note": note,
    }


def abc_field(n: int, amp: float):
    x = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    u = amp * (np.sin(Z) + np.cos(Y))
    v = amp * (np.sin(X) + np.cos(Z))
    w = amp * (np.sin(Y) + np.cos(X))
    return u, v, w


def score_abc(n: int, amp: float) -> dict:
    u, v, w = abc_field(n, amp)
    kx, ky, kz, _k2, k2_safe, _dealias = make_grid(n)
    uh, vh, wh = fft(u), fft(v), fft(w)
    ox, oy, oz, _, _, _ = curl(uh, vh, wh, kx, ky, kz)
    sx, sy, sz, mag = _xi(ox, oy, oz)
    jac2 = _jac_frob2_spectral(sx, sy, sz, kx, ky, kz)
    stretch = _strain_stretch_spectral(uh, vh, wh, kx, ky, kz, ox, oy, oz)
    dx = 2.0 * math.pi / n
    beltrami = _integrate((ox - u) ** 2 + (oy - v) ** 2 + (oz - w) ** 2, dx)
    row = _sample(
        "abc",
        amp=amp,
        ox=ox,
        oy=oy,
        oz=oz,
        u=u,
        v=v,
        w=w,
        stretch=stretch,
        jac2=jac2,
        dx=dx,
        rho=math.pi,
        length=2.0 * math.pi,
        tube_mask=None,
        note="ABC is not a thin tube. J/stretch vs amplitude only.",
    )
    row["beltrami_l2"] = beltrami
    row["k2_safe0"] = float(k2_safe[0, 0, 0])
    return row


def burgers_field(n: int, circulation: float, gamma: float, nu: float, box: float):
    xs = np.linspace(-box, box, n, endpoint=False)
    dx = 2.0 * box / n
    X, Y, Z = np.meshgrid(xs, xs, xs, indexing="ij")
    r2 = X * X + Y * Y
    delta = nu / gamma
    core = 1.0 - np.exp(-r2 / (4.0 * delta))
    circ = circulation / (2.0 * math.pi)
    inv = np.where(r2 < 1e-14, circ / (4.0 * delta), circ * core / np.maximum(r2, 1e-30))
    u_swirl_x = -Y * inv
    u_swirl_y = X * inv
    u = -(gamma / 2.0) * X + u_swirl_x
    v = -(gamma / 2.0) * Y + u_swirl_y
    w = gamma * Z
    oz = (circulation * gamma / (4.0 * math.pi * nu)) * np.exp(-r2 * gamma / (4.0 * nu))
    ox = np.zeros_like(oz)
    oy = np.zeros_like(oz)
    rho = 2.0 * math.sqrt(nu / gamma)
    return u, v, w, ox, oy, oz, u_swirl_x, u_swirl_y, dx, rho


def score_burgers(
    n: int,
    circulation: float,
    gamma: float = 1.0,
    nu: float = 0.1,
    box: float = 4.0,
) -> dict:
    u, v, w, ox, oy, oz, usx, usy, dx, rho = burgers_field(
        n, circulation, gamma, nu, box
    )
    sx, sy, sz, mag = _xi(ox, oy, oz)
    jac2 = _jac_frob2_fd(sx, sy, sz, dx)
    stretch = _strain_stretch_fd(u, v, w, ox, oy, oz, dx)
    r2 = None
    xs = np.linspace(-box, box, n, endpoint=False)
    X, Y, _Z = np.meshgrid(xs, xs, xs, indexing="ij")
    r2 = X * X + Y * Y
    core = r2 <= (2.0 * rho) ** 2
    e_swirl = _integrate(usx * usx + usy * usy, dx)
    e_swirl_core = _integrate((usx * usx + usy * usy) * core, dx)
    row = _sample(
        "burgers",
        amp=circulation,
        ox=ox,
        oy=oy,
        oz=oz,
        u=usx,
        v=usy,
        w=np.zeros_like(w),
        stretch=stretch,
        jac2=jac2,
        dx=dx,
        rho=rho,
        length=2.0 * box,
        tube_mask=core,
        note="Strain is imposed. Energy is swirl only. Do not cash as H1.",
    )
    row["gamma"] = gamma
    row["nu"] = nu
    row["waiting_rho2_over_nu"] = (rho * rho) / nu
    row["E_swirl"] = e_swirl
    row["E_swirl_core"] = e_swirl_core
    row["thinness_ratio_swirl"] = row["thinness_lhs"] / max(e_swirl, 1e-30)
    row["thinness_ratio_swirl_core"] = row["thinness_lhs"] / max(e_swirl_core, 1e-30)
    return row


def gaussian_pair(n: int, amp: float, rho: float, sep: float = 2.0):
    x = np.linspace(0.0, 2.0 * math.pi, n, endpoint=False)
    X, Y, Z = np.meshgrid(x, x, x, indexing="ij")
    y1 = math.pi - 0.5 * sep
    y2 = math.pi + 0.5 * sep
    r2p = (X - math.pi) ** 2 + (Y - y1) ** 2
    r2m = (X - math.pi) ** 2 + (Y - y2) ** 2
    oz = amp * (np.exp(-r2p / rho**2) - np.exp(-r2m / rho**2))
    ox = np.zeros_like(oz)
    oy = np.zeros_like(oz)
    kx, ky, kz, k2, k2_safe, _ = make_grid(n)
    oxh, oyh, ozh = fft(ox), fft(oy), fft(oz)
    # u = curl(−Δ^{-1} ω)
    uh = 1j * ky * (ozh / k2_safe) - 1j * kz * (oyh / k2_safe)
    vh = 1j * kz * (oxh / k2_safe) - 1j * kx * (ozh / k2_safe)
    wh = 1j * kx * (oyh / k2_safe) - 1j * ky * (oxh / k2_safe)
    uh[0, 0, 0] = 0.0
    vh[0, 0, 0] = 0.0
    wh[0, 0, 0] = 0.0
    u, v, w = ifft(uh), ifft(vh), ifft(wh)
    core = r2p <= (2.0 * rho) ** 2
    return u, v, w, ox, oy, oz, uh, vh, wh, kx, ky, kz, core


def score_gaussian(n: int, amp: float, rho: float, sep: float = 2.0) -> dict:
    u, v, w, ox, oy, oz, uh, vh, wh, kx, ky, kz, core = gaussian_pair(
        n, amp, rho, sep
    )
    sx, sy, sz, mag = _xi(ox, oy, oz)
    jac2 = _jac_frob2_spectral(sx, sy, sz, kx, ky, kz)
    stretch = _strain_stretch_spectral(uh, vh, wh, kx, ky, kz, ox, oy, oz)
    dx = 2.0 * math.pi / n
    circ = amp * math.pi * rho * rho
    row = _sample(
        "gaussian_pair",
        amp=amp,
        ox=ox,
        oy=oy,
        oz=oz,
        u=u,
        v=v,
        w=w,
        stretch=stretch,
        jac2=jac2,
        dx=dx,
        rho=rho,
        length=2.0 * math.pi,
        tube_mask=core,
        note="Self-induced pair. Mean ω = 0. Stretching is not imposed strain.",
    )
    row["circulation"] = circ
    row["sep"] = sep
    return row


def sweep(n: int = 48, quick: bool = False) -> dict:
    amps = (1.0, 2.0, 4.0) if quick else (0.5, 1.0, 2.0, 4.0, 8.0)
    rhos = (0.35, 0.50) if quick else (0.28, 0.35, 0.45, 0.60)
    abc = [score_abc(n, a) for a in amps]
    burgers = [score_burgers(n, a) for a in amps]
    # Fixed circulation, thinner cores.
    gauss_amp = []
    for a in amps:
        gauss_amp.append(score_gaussian(n, a, 0.40))
    gauss_rho = []
    gamma0 = 1.0
    for rho in rhos:
        amp = gamma0 / (math.pi * rho * rho)
        gauss_rho.append(score_gaussian(n, amp, rho))
    return {
        "meta": {
            "slot": "B",
            "write": "H1 one cylinder: J and thinness",
            "tuning_the_pde": False,
            "ring_lemma_proved": False,
            "h1_proved": False,
            "n": n,
            "quick": quick,
            "tesla": "estimates, not names. One tube is not C0.",
        },
        "abc": abc,
        "burgers": burgers,
        "gaussian_amp": gauss_amp,
        "gaussian_rho": gauss_rho,
    }


def _scale_report(rows: list[dict], key: str) -> dict:
    a0 = rows[0]["amp"]
    v0 = rows[0][key]
    out = []
    for r in rows:
        pred = v0 * (r["amp"] / a0) if a0 else 0.0
        out.append(
            {
                "amp": r["amp"],
                key: r[key],
                "over_amp": r[key] / max(r["amp"], 1e-30),
                "linear_rel": abs(r[key] - pred) / max(abs(pred), 1e-30),
            }
        )
    return {"key": key, "rows": out}


def lemmas(payload: dict) -> list[dict]:
    abc = payload["abc"]
    burg = payload["burgers"]
    g_amp = payload["gaussian_amp"]
    g_rho = payload["gaussian_rho"]

    j_scale = _scale_report(abc, "J_ec")
    st_scale = _scale_report(abc, "stretch_inf_plus")
    j_lin = max(r["linear_rel"] for r in j_scale["rows"])
    st_lin = max(r["linear_rel"] for r in st_scale["rows"])
    j_over_x = [r["J_over_X"] for r in abc]

    rows = [
        rec(
            "H1t_abc_j_tracks_amp",
            "ABC: J_ec tracks amplitude, not enstrophy",
            "pass" if j_lin < 0.15 else "fail",
            "ξ of ABC does not change with amp. J ~ ∫|ω| ~ A. Not a uniform constant.",
            linear_rel=j_lin,
            J_over_amp=[r["over_amp"] for r in j_scale["rows"]],
            J_over_X=j_over_x,
        ),
        rec(
            "H1t_abc_stretch_tracks_amp",
            "ABC: ‖(ξ·∇u·ξ)_+‖_∞ is independent of amplitude",
            "fail",
            "BKM-on-cylinder fails on ABC: stretch rate grows like A. Kill of this packaging on this field, not of NS.",
            linear_rel=st_lin,
            stretch_over_amp=[r["over_amp"] for r in st_scale["rows"]],
            stretch_inf=[r["stretch_inf_plus"] for r in abc],
        ),
        rec(
            "H1t_abc_j_not_enstrophy",
            "ABC: J blows like enstrophy as amplitude grows",
            "fail",
            "J/X falls like 1/A. Folds stay O(1) in ξ; weight is |ω|. Not the H1 kill (that kill is the stretch rate).",
            J_over_X=j_over_x,
        ),
        rec(
            "H1t_burgers_aligned",
            "Burgers: J on E_c is tiny and stretch_+ is the imposed strain",
            "pass"
            if all(r["J_ec"] < 1e-6 * max(r["X_full"], 1.0) for r in burg)
            and all(abs(r["stretch_inf_plus"] - r["gamma"]) < 0.15 * r["gamma"] for r in burg)
            else "fail",
            "ξ = ê_z exactly. Stretching is γ, not Biot–Savart of the tube. Do not cash as H1.",
            J_ec=[r["J_ec"] for r in burg],
            stretch_inf=[r["stretch_inf_plus"] for r in burg],
            gamma=[r["gamma"] for r in burg],
        ),
        rec(
            "H1t_burgers_not_h1",
            "Burgers closes H1 as an a priori",
            "fail",
            "Imposed strain and a locked viscous radius. Waiting is built in. One exact tube is not C(ρ,L).",
        ),
        rec(
            "H1t_gaussian_thinness",
            "straight pair: ρ²∫|ω|² ≲ energy captured by the positive core, from Biot–Savart",
            "pass"
            if all(0.05 < r["thinness_ratio_tube"] < 80.0 for r in g_rho)
            else "fail",
            "A number on this pair. Not a picture. Not H1. Self-stretch is not the close.",
            ratios=[r["thinness_ratio_tube"] for r in g_rho],
            rhos=[r["rho"] for r in g_rho],
        ),
        rec(
            "H1t_gaussian_self_stretch",
            "straight pair: ‖(ξ·∇u·ξ)_+‖_∞ stays small versus ABC of the same |ω|",
            "pass"
            if max(r["stretch_inf_plus"] for r in g_amp) < 0.25 * max(r["stretch_inf_plus"] for r in abc)
            else "fail",
            "A straight tube has no axial strain from its own Biot–Savart. Thinness without stretching is not H1.",
            stretch_inf=[r["stretch_inf_plus"] for r in g_amp],
        ),
        rec(
            "H1t_not_a_close",
            "these tubes close H1 / BKM on one cylinder",
            "fail",
            "ABC stretch grows with amplitude. Burgers strain is imposed. A straight pair does not stretch. Ring Lemma unrepaired. NS not solved.",
        ),
        rec(
            "H1t_not_gcd",
            "H1 on a cylinder is the GCD matrix H_M[a]",
            "fail",
            "Different letters. Do not glue.",
        ),
        rec(
            "H1t_ring_not_proved",
            "ledger Ring Lemma ‖∇ξ‖_∞ ≤ C 2^{j*} is proved",
            "fail",
            "REPAIR. The claim assumes the direction bound it wants. H1 is that claim restricted to one cylinder. Constants must be checked.",
        ),
    ]
    return rows


def run(n: int = 48, quick: bool = False, out: Path | None = None) -> dict:
    payload = sweep(n=n, quick=quick)
    rows = lemmas(payload)
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in rows:
        counts[row["verdict"]] += 1
    payload["lemmas"] = rows
    payload["counts"] = counts
    payload["domain_verdict"] = "open"
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--n", type=int, default=48)
    p.add_argument("--quick", action="store_true")
    p.add_argument("--out", type=Path, default=None)
    args = p.parse_args()
    payload = run(n=args.n, quick=args.quick, out=args.out)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
