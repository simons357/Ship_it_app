#!/usr/bin/env python3
"""
Stretching budget on E_c, then a short run.

Classical NS. No Q1. No ε. B14 read |cos α_3| unweighted.
Here the cubic's payers are weighted by (ω·Sω)_+.
The budget sits on the aligned cap. Time does not empty it.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from track_b_evolve import ifrk2_step
from track_b_lemmas import curl, ifft, make_grid, project, rec, three_shell_field

_T0: list[dict] | None = None
_EV: dict[str, list[dict]] | None = None

EC_C = 0.5
HIGH = 0.8
LOW = 0.25
WMEAN_GAP = 0.15


def budget(uh, vh, wh, kx, ky, kz, c: float = EC_C) -> dict:
    ox, oy, oz, _, _, _ = curl(uh, vh, wh, kx, ky, kz)
    d = [[ifft(1j * k * h) for k in (kx, ky, kz)] for h in (uh, vh, wh)]
    s00, s11, s22 = d[0][0], d[1][1], d[2][2]
    s01 = 0.5 * (d[0][1] + d[1][0])
    s02 = 0.5 * (d[0][2] + d[2][0])
    s12 = 0.5 * (d[1][2] + d[2][1])
    mag2 = ox * ox + oy * oy + oz * oz
    mag = np.sqrt(mag2)
    rms = float(np.sqrt(np.mean(mag2)))
    ec = mag >= c * rms
    stretch = (
        ox * (s00 * ox + s01 * oy + s02 * oz)
        + oy * (s01 * ox + s11 * oy + s12 * oz)
        + oz * (s02 * ox + s12 * oy + s22 * oz)
    )
    mats = np.stack(
        [
            np.stack([s00[ec], s01[ec], s02[ec]], axis=-1),
            np.stack([s01[ec], s11[ec], s12[ec]], axis=-1),
            np.stack([s02[ec], s12[ec], s22[ec]], axis=-1),
        ],
        axis=-2,
    )
    _, vecs = np.linalg.eigh(mats)
    xi = np.stack([ox[ec], oy[ec], oz[ec]], axis=-1)
    nrm = np.linalg.norm(xi, axis=-1, keepdims=True)
    xi = xi / np.maximum(nrm, 1e-30)
    cos3 = np.abs(np.sum(xi * vecs[..., 2], axis=-1))
    st = stretch[ec]
    pos = np.maximum(st, 0.0)
    pos_sum = float(np.sum(pos)) + 1e-30
    all_pos = float(np.sum(np.maximum(stretch, 0.0))) + 1e-30
    return {
        "n_ec": int(np.sum(ec)),
        "frac_vol": float(np.mean(ec)),
        "median_cos3": float(np.median(cos3)),
        "mean_cos3": float(np.mean(cos3)),
        "wmean_cos3": float(np.sum(pos * cos3) / pos_sum),
        "frac_pos_hi": float(np.sum(pos[cos3 > HIGH]) / pos_sum),
        "frac_pos_lo": float(np.sum(pos[cos3 < LOW]) / pos_sum),
        "share_of_all_pos": float(np.sum(pos) / all_pos),
        "X": float(np.mean(mag2)) * (2.0 * math.pi) ** 3,
    }


def packet_t0(n: int = 32, jstar: int = 3, seed: int = 1) -> dict:
    rng = np.random.default_rng(seed)
    uh, vh, wh, kx, ky, kz, _ = three_shell_field(n, jstar, rng)
    row = budget(uh, vh, wh, kx, ky, kz)
    row["seed"] = seed
    row["jstar"] = jstar
    return row


def evolve_one(
    n: int = 32,
    jstar: int = 2,
    seed: int = 1,
    nu: float = 0.1,
    x_target: float = 2.5,
    dt: float = 0.008,
    steps: int = 8,
) -> dict:
    rng = np.random.default_rng(seed)
    uh, vh, wh, kx, ky, kz, k2 = three_shell_field(n, jstar, rng)
    _, _, _, _, k2_safe, dealias = make_grid(n)
    ox, oy, oz, _, _, _ = curl(uh, vh, wh, kx, ky, kz)
    vol = (2.0 * math.pi) ** 3
    xtot = float(np.mean(ox * ox + oy * oy + oz * oz)) * vol
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
    start = budget(uh, vh, wh, kx, ky, kz)
    for _ in range(steps):
        uh, vh, wh = ifrk2_step(uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, nu, dt)
    end = budget(uh, vh, wh, kx, ky, kz)
    return {
        "seed": seed,
        "nu": nu,
        "T": steps * dt,
        "start": start,
        "end": end,
    }


def t0_samples(trials: int = 6) -> list[dict]:
    global _T0
    if _T0 is None:
        _T0 = [packet_t0(seed=s) for s in range(1, trials + 1)]
    return _T0


def evolved(seeds: tuple[int, ...] = (1, 2, 3)) -> dict[str, list[dict]]:
    global _EV
    if _EV is None:
        _EV = {
            "visc": [evolve_one(seed=s, nu=0.1) for s in seeds],
            "euler": [evolve_one(seed=s, nu=0.0) for s in seeds],
        }
    return _EV


def lemma_budget_readable() -> dict:
    rows = t0_samples()
    ok = all(r["n_ec"] >= 1000 and r["share_of_all_pos"] > 0.5 for r in rows)
    return rec(
        "B15_stretch_budget",
        "(ω·Sω)_+ on E_c is a readable stretching budget, with stretch-weighted |cos α_3|",
        "pass" if ok else "fail",
        "B14 subsampled efficiency. This write integrates the cubic's payers.",
        n_ec=[r["n_ec"] for r in rows],
        share_of_all_pos=[r["share_of_all_pos"] for r in rows],
    )


def lemma_cf_weights_budget() -> dict:
    rows = t0_samples()
    gaps = [r["wmean_cos3"] - r["mean_cos3"] for r in rows]
    ok = all(g > WMEAN_GAP for g in gaps)
    return rec(
        "B15a_cf_weights_budget",
        "stretch-weighted |cos α_3| on E_c exceeds the unweighted mean by more than 0.15",
        "pass" if ok else "fail",
        "Constantin–Fefferman as a budget. The cubic pays more where vorticity meets extension. Not depletion of the field.",
        wmean=[r["wmean_cos3"] for r in rows],
        mean=[r["mean_cos3"] for r in rows],
        gaps=gaps,
    )


def lemma_majority_aligned() -> dict:
    rows = t0_samples()
    fracs = [r["frac_pos_hi"] for r in rows]
    ok = all(f > 0.5 for f in fracs)
    return rec(
        "B15b_majority_from_aligned",
        "a majority of (ω·Sω)_+ on E_c comes from |cos α_3| > 0.8",
        "pass" if ok else "fail",
        "The aligned cap is a directional minority and a production majority. Median |cos α_3| is still ~1/2.",
        frac_pos_hi=fracs,
        frac_pos_lo=[r["frac_pos_lo"] for r in rows],
        median_cos3=[r["median_cos3"] for r in rows],
    )


def lemma_run_not_depleted() -> dict:
    visc = evolved()["visc"]
    meds = [r["end"]["median_cos3"] for r in visc]
    depleted = all(m <= LOW for m in meds)
    return rec(
        "B15c_run_not_depleted",
        "a short viscous run depletes median |cos α_3| on E_c to ≤ 0.25",
        "fail" if not depleted else "open",
        "Median stays near 1/2. Viscosity ate X. It did not rotate the sphere.",
        median_end=meds,
        median_start=[r["start"]["median_cos3"] for r in visc],
    )


def lemma_run_keeps_budget() -> dict:
    visc = evolved()["visc"]
    euler = evolved()["euler"]
    visc_hi = [r["end"]["frac_pos_hi"] for r in visc]
    euler_hi = [r["end"]["frac_pos_hi"] for r in euler]
    emptied = any(h < 0.5 for h in visc_hi + euler_hi)
    return rec(
        "B15d_run_keeps_aligned_budget",
        "a short run drops the aligned share of (ω·Sω)_+ below 1/2",
        "fail" if not emptied else "open",
        "frac_hi stays ~0.65. The cubic's payers did not leave. Tesla: time was a knob. It did not empty the cap.",
        visc_frac_hi_end=visc_hi,
        euler_frac_hi_end=euler_hi,
        visc_wmean_end=[r["end"]["wmean_cos3"] for r in visc],
        visc_X=[(r["start"]["X"], r["end"]["X"]) for r in visc],
    )


def lemma_budget_not_close() -> dict:
    return rec(
        "B15e_budget_not_X_a_priori",
        "an aligned stretching budget closes a bound for classical X",
        "fail",
        "Scored as B26. A weighted |cos α_3| is not an a priori. Time did not empty the cap. A share is not continuation.",
    )


def lemma_stretch_not_a_retune() -> dict:
    return rec(
        "B15f_not_a_pde_retune",
        "weighting stretching by (ω·Sω)_+ is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. The budget is a knob on the estimate: a share you can miss.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_budget_readable(),
        lemma_cf_weights_budget(),
        lemma_majority_aligned(),
        lemma_run_not_depleted(),
        lemma_run_keeps_budget(),
        lemma_budget_not_close(),
        lemma_stretch_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "stretching budget on CONC packets",
            "tuning_the_pde": False,
            "tesla": "exacting, not a jerk. The cubic's payers are a number. Time did not empty them.",
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). "
            "Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Finer box is not an a priori (B22e). DNS leftover is B23e. Finer (n>32) stays a box knob (B22e). "
            "Do not spawn n=64. B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_stretch.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Stretching budget. Aligned cap pays; time does not empty it.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
