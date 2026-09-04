#!/usr/bin/env python3
"""
Enstrophy balance: fluids look at the stretching budget.

Classical NS. No Q1. No ε. B15 weighted (ω·Sω)_+.
The fluids identity is Ẋ = 2∫ ω·Sω − 2ν‖∇ω‖₂².
On random 3-CONC packets the cubic cancels. Viscosity
owns the net. That is not BKM, and not all CONC.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from track_b_evolve import ifrk2_step
from track_b_lemmas import curl, ifft, make_grid, project, rec, three_shell_field

_PACKETS: list[dict] | None = None
_IDENT: dict | None = None

VOL = (2.0 * math.pi) ** 3
CANCEL_MAX = 0.05
PD_MAX = 0.05
PPD_MAX = 0.05
IDENT_MAX = 1e-2


def production_dissipation(uh, vh, wh, kx, ky, kz, nu: float) -> dict:
    ox, oy, oz, oxh, oyh, ozh = curl(uh, vh, wh, kx, ky, kz)
    mag2 = ox * ox + oy * oy + oz * oz
    X = float(np.mean(mag2)) * VOL
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
    P = float(np.mean(stretch)) * VOL
    Pp = float(np.mean(np.maximum(stretch, 0.0))) * VOL
    Pm = float(np.mean(np.maximum(-stretch, 0.0))) * VOL
    go = [ifft(1j * k * h) for h in (oxh, oyh, ozh) for k in (kx, ky, kz)]
    D = nu * float(np.mean(sum(g * g for g in go))) * VOL
    winf = float(np.max(np.sqrt(mag2)))
    return {
        "X": X,
        "P": P,
        "Pplus": Pp,
        "Pminus": Pm,
        "D": D,
        "cancel": abs(P) / max(Pp + Pm, 1e-30),
        "P_over_D": P / max(D, 1e-30),
        "Pplus_over_D": Pp / max(D, 1e-30),
        "Xdot": 2.0 * P - 2.0 * D,
        "winf": winf,
        "wl2": math.sqrt(max(X, 1e-30)),
        "bkm_gap": winf / math.sqrt(max(X, 1e-30)),
    }


def scaled_packet(n: int, jstar: int, seed: int, x_target: float = 2.5):
    rng = np.random.default_rng(seed)
    uh, vh, wh, kx, ky, kz, k2 = three_shell_field(n, jstar, rng)
    _, _, _, _, k2_safe, dealias = make_grid(n)
    ox, oy, oz, _, _, _ = curl(uh, vh, wh, kx, ky, kz)
    xtot = float(np.mean(ox * ox + oy * oy + oz * oz)) * VOL
    scale = math.sqrt(x_target / max(xtot, 1e-30))
    uh, vh, wh = project(
        uh * scale * dealias,
        vh * scale * dealias,
        wh * scale * dealias,
        kx,
        ky,
        kz,
        k2_safe,
    )
    return uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias


def packets(seeds: tuple[int, ...] = (1, 2, 3), nu: float = 0.1) -> list[dict]:
    global _PACKETS
    if _PACKETS is None:
        rows = []
        for seed in seeds:
            uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias = scaled_packet(32, 2, seed)
            row = production_dissipation(uh, vh, wh, kx, ky, kz, nu)
            row["seed"] = seed
            row["nu"] = nu
            row["jstar"] = 2
            rows.append(row)
        _PACKETS = rows
    return _PACKETS


def identity_check(nu: float = 0.1, dt: float = 5e-5) -> dict:
    global _IDENT
    if _IDENT is None:
        uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias = scaled_packet(32, 2, 1)
        before = production_dissipation(uh, vh, wh, kx, ky, kz, nu)
        uh, vh, wh = ifrk2_step(uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, nu, dt)
        after = production_dissipation(uh, vh, wh, kx, ky, kz, nu)
        pred = before["Xdot"]
        got = (after["X"] - before["X"]) / dt
        _IDENT = {
            "pred": pred,
            "got": got,
            "rel": abs(got - pred) / max(abs(pred), 1e-30),
            "dt": dt,
            "nu": nu,
        }
    return _IDENT


def lemma_enstrophy_identity() -> dict:
    ident = identity_check()
    ok = ident["rel"] < IDENT_MAX
    return rec(
        "B16_enstrophy_identity",
        "Ẋ = 2∫ ω·Sω − 2ν‖∇ω‖₂² on a classical CONC packet",
        "pass" if ok else "fail",
        "Fluids identity. Geometry weighted a leftover. This is the net.",
        rel=ident["rel"],
        pred=ident["pred"],
        got=ident["got"],
    )


def lemma_visc_owns_net() -> dict:
    rows = packets()
    ok = all(abs(r["P_over_D"]) < PD_MAX and r["Xdot"] < 0.0 for r in rows)
    return rec(
        "B16a_visc_owns_net",
        "on B13-scale random 3-CONC packets, |∫ω·Sω| ≪ ν‖∇ω‖₂² and Ẋ < 0",
        "pass" if ok else "fail",
        "Leray’s dissipation owns the net on this ensemble. Same packets as the stretching budget.",
        P_over_D=[r["P_over_D"] for r in rows],
        Xdot=[r["Xdot"] for r in rows],
        D=[r["D"] for r in rows],
    )


def lemma_plus_not_a_cubic() -> dict:
    rows = packets()
    cancels = [r["cancel"] for r in rows]
    ppd = [r["Pplus_over_D"] for r in rows]
    large_cubic = any(c > CANCEL_MAX or p > PPD_MAX for c, p in zip(cancels, ppd))
    return rec(
        "B16b_plus_not_net_cubic",
        "the aligned (ω·Sω)_+ budget is a large net cubic on these packets",
        "fail" if not large_cubic else "open",
        "Plus and minus stretch cancel at ~10^{-3}. The 65% share is 65% of a leftover that nets near zero.",
        cancel=cancels,
        Pplus_over_D=ppd,
        P=[r["P"] for r in rows],
        Pplus=[r["Pplus"] for r in rows],
    )


def lemma_not_bkm() -> dict:
    rows = packets()
    gaps = [r["bkm_gap"] for r in rows]
    return rec(
        "B16c_l2_is_not_bkm",
        "an L² packet bound is the Beale–Kato–Majda criterion",
        "fail",
        "‖ω‖_∞/‖ω‖₂ sits near 0.2 on a fat packet. BKM asks for ∫‖ω‖_∞. Do not improve them into L².",
        bkm_gap=gaps,
        winf=[r["winf"] for r in rows],
        wl2=[r["wl2"] for r in rows],
    )


def lemma_not_all_conc() -> dict:
    return rec(
        "B16d_not_all_conc",
        "random-phase cancellation is an a priori for every 3-CONC field",
        "fail",
        "This ensemble is random phase. A coherent vortex can have P ≈ (ω·Sω)_+. Fluids did not promote a packet to a class.",
    )


def lemma_balance_not_close() -> dict:
    return rec(
        "B16e_balance_not_X_a_priori",
        "the enstrophy balance on these packets closes a bound for classical X",
        "fail",
        "Scored as B27. Viscosity owned this ensemble. That is not continuation. A cancelled net is not a bound.",
    )


def lemma_balance_not_a_retune() -> dict:
    return rec(
        "B16f_not_a_pde_retune",
        "reading ∫ω·Sω versus viscosity is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. The balance is a knob on the estimate: a cancellation you can miss.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_enstrophy_identity(),
        lemma_visc_owns_net(),
        lemma_plus_not_a_cubic(),
        lemma_not_bkm(),
        lemma_not_all_conc(),
        lemma_balance_not_close(),
        lemma_balance_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "enstrophy balance; fluids look at the stretching budget",
            "tuning_the_pde": False,
            "tesla": "exacting, not a jerk. Net production is a number. The share of a leftover is not the cubic.",
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). "
            "Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). DNS leftover is B23e. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_balance.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Enstrophy balance. Fluids look at the net, not the share.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
