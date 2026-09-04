#!/usr/bin/env python3
"""
Field occupation: the B8 clock, read on a path.

Classical NS. No Q1. No ε. Typed σ already partitions T (B8).
Leray does not shorten CONC (B8b). This write samples σ along
short IF-RK2 trajectories. The clock never leaves CONC.
X sits, when it sits, by viscosity.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from track_b_balance import VOL, PD_MAX, production_dissipation
from track_b_coherent import blob_packet
from track_b_evolve import ifrk2_step, packet_stats, shell_masses
from track_b_lemmas import curl, make_grid, project, rec, three_shell_field
from track_b_occupation import occupation

N = 32
DT = 0.008
STEPS = 8
X_TARGET = 2.5
NU = 0.1
CONC_FRAC_MIN = 0.9
CLOCK_GAP = 1e-12

_PATHS: dict[str, dict] | None = None


def interval_occupation(sigma: np.ndarray, dt: float) -> dict:
    """Occupation on step intervals so T matches evolution time."""
    left = np.asarray(sigma[:-1], dtype=float) if len(sigma) > 1 else np.asarray(sigma)
    return occupation(left, dt)


def scaled_packet(n: int = N, jstar: int = 2, seed: int = 1, x_target: float = X_TARGET):
    rng = np.random.default_rng(seed)
    uh, vh, wh, kx, ky, kz, k2 = three_shell_field(n, jstar, rng)
    _, _, _, _, k2_safe, dealias = make_grid(n)
    ox, oy, oz, *_ = curl(uh, vh, wh, kx, ky, kz)
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
    return uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, jstar


def record_path(uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, nu, jstar0, dt=DT, steps=STEPS):
    uh, vh, wh = uh.copy(), vh.copy(), wh.copy()
    sigmas: list[float] = []
    xs: list[float] = []
    jbars: list[float] = []
    aboves: list[float] = []
    p_over_d: list[float] = []
    for i in range(steps + 1):
        ox, oy, oz, oxh, oyh, ozh = curl(uh, vh, wh, kx, ky, kz)
        st = packet_stats(shell_masses(oxh, oyh, ozh, k2, VOL), jstar0)
        pd = production_dissipation(uh, vh, wh, kx, ky, kz, nu)
        sigmas.append(st["sigma"])
        xs.append(st["X"])
        jbars.append(st["jbar"])
        aboves.append(st["above"])
        p_over_d.append(pd["P_over_D"] if nu > 0.0 else 0.0)
        if i < steps:
            uh, vh, wh = ifrk2_step(
                uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, nu, dt
            )
    sigma = np.array(sigmas)
    occ = interval_occupation(sigma, dt)
    live = int(sum(abs(p) >= PD_MAX for p in p_over_d))
    return {
        "nu": nu,
        "jstar0": jstar0,
        "dt": dt,
        "steps": steps,
        "sigma": [float(s) for s in sigma],
        "X": [float(x) for x in xs],
        "jbar": [float(j) for j in jbars],
        "jbar0": float(jbars[0]),
        "jbarT": float(jbars[-1]),
        "c_mean": float((jbars[-1] - jbars[0]) / max(steps * dt, 1e-30)),
        "c_inc": [
            float((jbars[i + 1] - jbars[i]) / max(dt, 1e-30))
            for i in range(len(jbars) - 1)
        ],
        "above0": float(aboves[0]),
        "aboveT": float(aboves[-1]),
        "P_over_D": [float(p) for p in p_over_d],
        "occ": occ,
        "tau_frac_conc": occ["tau_conc"] / max(occ["T"], 1e-30),
        "switches": occ["switches"],
        "clock_gap": abs(occ["tau_conc"] + occ["tau_spread"] - occ["T"]),
        "live_samples": live,
        "X0": float(xs[0]),
        "XT": float(xs[-1]),
        "X_fell": bool(xs[-1] < xs[0] - 1e-9),
        "sigma_min": float(np.min(sigma)),
    }


def paths() -> dict[str, dict]:
    global _PATHS
    if _PATHS is None:
        uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, jstar = scaled_packet()
        pack = record_path(uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, NU, jstar)
        blob = blob_packet()
        blob_path = record_path(
            blob["uh"],
            blob["vh"],
            blob["wh"],
            blob["kx"],
            blob["ky"],
            blob["kz"],
            blob["k2"],
            blob["k2_safe"],
            blob["dealias"],
            NU,
            3,
        )
        _PATHS = {"packet": pack, "blob": blob_path}
    return _PATHS


def lemma_field_clock() -> dict:
    rows = paths()
    ok = all(r["clock_gap"] < CLOCK_GAP for r in rows.values())
    return rec(
        "B18_field_clock",
        "τ_CONC + τ_SPREAD = T along short IF-RK2 paths of a packet and a signed-strain blob",
        "pass" if ok else "fail",
        "The B8 clock, read on a field. Same threshold σ=1/2. Switching still free.",
        clock_gap={"packet": rows["packet"]["clock_gap"], "blob": rows["blob"]["clock_gap"]},
        T={"packet": rows["packet"]["occ"]["T"], "blob": rows["blob"]["occ"]["T"]},
    )


def lemma_stays_conc() -> dict:
    rows = paths()
    ok = all(r["tau_frac_conc"] >= CONC_FRAC_MIN and r["sigma_min"] >= 0.5 for r in rows.values())
    return rec(
        "B18a_paths_stay_conc",
        "short viscous packet and blob paths occupy 3-CONC for the whole interval",
        "pass" if ok else "fail",
        "σ never drops through 1/2. The clock has one column on.",
        tau_frac={"packet": rows["packet"]["tau_frac_conc"], "blob": rows["blob"]["tau_frac_conc"]},
        sigma_min={"packet": rows["packet"]["sigma_min"], "blob": rows["blob"]["sigma_min"]},
        switches={"packet": rows["packet"]["switches"], "blob": rows["blob"]["switches"]},
    )


def lemma_clock_did_not_save() -> dict:
    rows = paths()
    flipped = any(r["switches"] > 0 for r in rows.values())
    return rec(
        "B18b_clock_did_not_save",
        "the clock left CONC, and that is why X sat on these paths",
        "fail" if not flipped else "open",
        "Zero switches. Packet X falls by viscosity. The blob too. The clock did not flip them into SPREAD.",
        switches={"packet": rows["packet"]["switches"], "blob": rows["blob"]["switches"]},
        X0={"packet": rows["packet"]["X0"], "blob": rows["blob"]["X0"]},
        XT={"packet": rows["packet"]["XT"], "blob": rows["blob"]["XT"]},
        X_fell={"packet": rows["packet"]["X_fell"], "blob": rows["blob"]["X_fell"]},
    )


def lemma_conc_not_short() -> dict:
    rows = paths()
    short = any(r["tau_frac_conc"] < CONC_FRAC_MIN for r in rows.values())
    return rec(
        "B18c_conc_not_short",
        "CONC occupation is short on these Navier–Stokes runs",
        "fail" if not short else "open",
        "τ_CONC = T. High-j* short (B8a) is a packet ODE. These fields did not occupy a short visit.",
        tau_frac={"packet": rows["packet"]["tau_frac_conc"], "blob": rows["blob"]["tau_frac_conc"]},
    )


def lemma_cubic_not_live_time() -> dict:
    rows = paths()
    live = any(r["live_samples"] > 0 for r in rows.values())
    return rec(
        "B18d_cubic_not_live_time",
        "the cubic is live (|P|/D ≥ 0.05) on a nonempty set of samples at the working box",
        "fail" if not live else "open",
        "Zero live samples. One-sided P on the blob is still a leftover versus D. Occupation of CONC is not occupation of a live cubic.",
        live_samples={"packet": rows["packet"]["live_samples"], "blob": rows["blob"]["live_samples"]},
        P_over_D={
            "packet": rows["packet"]["P_over_D"],
            "blob": rows["blob"]["P_over_D"],
        },
    )


def lemma_field_occ_not_close() -> dict:
    return rec(
        "B18e_field_occ_not_X_a_priori",
        "field occupation closes a bound for classical X",
        "fail",
        "Scored as B29. Occupation of CONC is not continuation. The clock did not leave. Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). Regularity leftover is open.",
    )


def lemma_field_occ_not_a_retune() -> dict:
    return rec(
        "B18f_not_a_pde_retune",
        "reading σ along an IF-RK2 path is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. Sampling the clock is a knob on the check. No Q1. No ε.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_field_clock(),
        lemma_stays_conc(),
        lemma_clock_did_not_save(),
        lemma_conc_not_short(),
        lemma_cubic_not_live_time(),
        lemma_field_occ_not_close(),
        lemma_field_occ_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "field occupation; B8 clock on a path",
            "tuning_the_pde": False,
            "tesla": (
                "exacting, not a jerk. Occupation is a number on a path. "
                "If the path never leaves CONC, the clock did not do the bound."
            ),
            "domain_verdict": "open",
            "n": N,
            "dt": DT,
            "steps": STEPS,
            "nu": NU,
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). Finer DNS is not an a priori (B23e). Regularity leftover is open. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_field_occ.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Field occupation. The clock, on a path.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
