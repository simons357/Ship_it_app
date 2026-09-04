#!/usr/bin/env python3
"""
Climb law from the field: c the packet makes, not a c we type.

Instantaneous barycenter drift of enstrophy shells from the
vorticity RHS. Random CONC packets do not produce the saving
climb. Viscosity pulls j_bar down. A time-evolved cascade is
not shown. The PDE is not tuned.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from track_b_lemmas import (
    convect,
    curl,
    fft,
    ifft,
    mask_band,
    rec,
    three_shell_field,
)

# Saving rate on the B11 model. Fast prescribed climb sat at c = 8.
C_SAVE = 8.0


def hats_climb(uh, vh, wh, kx, ky, kz, k2, nu: float, jstar: int) -> dict:
    """Instantaneous c = d j_bar / dt from the vorticity RHS on given hats."""
    ox, oy, oz, oxh, oyh, ozh = curl(uh, vh, wh, kx, ky, kz)
    vol = (2.0 * math.pi) ** 3
    xtot = float(np.mean(ox * ox + oy * oy + oz * oz)) * vol
    u, v, w = ifft(uh), ifft(vh), ifft(wh)
    cu, cv, cw = convect(u, v, w, oxh, oyh, ozh, kx, ky, kz)
    su, sv, sw = convect(ox, oy, oz, uh, vh, wh, kx, ky, kz)
    visc_x, visc_y, visc_z = ifft(-k2 * oxh), ifft(-k2 * oyh), ifft(-k2 * ozh)
    rx = -cu + su + nu * visc_x
    ry = -cv + sv + nu * visc_y
    rz = -cw + sw + nu * visc_z
    rxh, ryh, rzh = fft(rx), fft(ry), fft(rz)
    js = list(range(max(jstar - 2, 1), jstar + 3))
    x_shell: dict[int, float] = {}
    dx_shell: dict[int, float] = {}
    for j in js:
        band = mask_band(k2, 2.0 ** (j - 1), 2.0**j)
        oxj, oyj, ozj = ifft(oxh * band), ifft(oyh * band), ifft(ozh * band)
        rxj, ryj, rzj = ifft(rxh * band), ifft(ryh * band), ifft(rzh * band)
        x_shell[j] = float(np.mean(oxj * oxj + oyj * oyj + ozj * ozj)) * vol
        dx_shell[j] = 2.0 * float(np.mean(oxj * rxj + oyj * ryj + ozj * rzj)) * vol
    tot = sum(x_shell.values())
    dtot = sum(dx_shell.values())
    jbar = sum(j * x_shell[j] for j in js) / max(tot, 1e-30)
    c = (sum(j * dx_shell[j] for j in js) / max(tot, 1e-30)) - jbar * (
        dtot / max(tot, 1e-30)
    )
    triad = sum(x_shell[j] for j in (jstar - 1, jstar, jstar + 1) if j in x_shell)
    return {
        "jstar": jstar,
        "jbar": float(jbar),
        "c": float(c),
        "sigma": float(triad / max(tot, 1e-30)),
        "X": float(xtot),
        "nu": nu,
    }


def packet_climb(
    n: int,
    jstar: int,
    seed: int,
    nu: float,
    x_target: float | None = 2.5,
) -> dict:
    rng = np.random.default_rng(seed)
    uh, vh, wh, kx, ky, kz, k2 = three_shell_field(n, jstar, rng)
    if x_target is not None:
        ox, oy, oz, *_ = curl(uh, vh, wh, kx, ky, kz)
        vol = (2.0 * math.pi) ** 3
        xtot = float(np.mean(ox * ox + oy * oy + oz * oz)) * vol
        scale = math.sqrt(x_target / max(xtot, 1e-30))
        uh, vh, wh = uh * scale, vh * scale, wh * scale
    out = hats_climb(uh, vh, wh, kx, ky, kz, k2, nu, jstar)
    out["seed"] = seed
    return out


def sample(n: int = 24, trials: int = 8, jstar: int = 3, nu: float = 0.1, seed0: int = 1):
    return [packet_climb(n, jstar, seed0 + k, nu) for k in range(trials)]


def lemma_barycenter() -> dict:
    rows = sample(nu=0.1)
    near = all(abs(r["jbar"] - r["jstar"]) <= 1.5 for r in rows)
    conc = all(r["sigma"] >= 0.5 for r in rows)
    ok = near and conc
    return rec(
        "B12_barycenter",
        "on a 3-shell packet, j_bar is within 1.5 of j* and σ ≥ 1/2",
        "pass" if ok else "fail",
        "A readable peak scale. Tesla’s first knob on the field: you can say where the mass sits.",
        samples=rows,
    )


def lemma_c_from_rhs() -> dict:
    visc = sample(nu=0.1)
    euler = sample(nu=0.0)
    finite = all(math.isfinite(r["c"]) for r in visc + euler)
    return rec(
        "B12a_c_from_rhs",
        "instantaneous c = d j_bar / dt is computable from the vorticity RHS",
        "pass" if finite else "fail",
        "The apparatus reads the field. It does not type c=8.",
        viscous=[r["c"] for r in visc],
        euler=[r["c"] for r in euler],
    )


def lemma_t0_not_saving() -> dict:
    visc = sample(nu=0.1)
    euler = sample(nu=0.0)
    any_save = any(r["c"] >= C_SAVE for r in visc + euler)
    return rec(
        "B12b_t0_not_saving",
        "random CONC packets at t=0 produce c ≥ 8 (the B11c saving rate)",
        "fail" if not any_save else "open",
        "None of the packets reach the saving climb. The field did not hand us c=8.",
        c_save=C_SAVE,
        viscous_max=max(r["c"] for r in visc),
        euler_max=max(r["c"] for r in euler),
    )


def lemma_visc_pulls_down() -> dict:
    visc = sample(nu=0.1)
    all_neg = all(r["c"] < 0.0 for r in visc)
    return rec(
        "B12c_visc_pulls_down",
        "viscosity on a CONC packet forces an upward climb",
        "fail" if all_neg else "open",
        "High shells damp faster. j_bar falls. Viscosity is not a ladder.",
        viscous=[r["c"] for r in visc],
    )


def lemma_evolved_cascade_open() -> dict:
    return rec(
        "B12d_evolved_not_saving",
        "a short NS evolution of a CONC packet produces a saving climb",
        "fail",
        "Broken out as B13. Short missed (B13a). Longer past room time missed (B22). DNS is not an a priori (B13f).",
    )


def lemma_law_not_a_priori() -> dict:
    return rec(
        "B12e_law_not_X_a_priori",
        "the instantaneous field drift is a closed climb law for classical X",
        "fail",
        "A t=0 reading is not a law. The path did not write one either (B13, B20, B22). Do not sit it as dj*/dt on NS.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_barycenter(),
        lemma_c_from_rhs(),
        lemma_t0_not_saving(),
        lemma_visc_pulls_down(),
        lemma_evolved_cascade_open(),
        lemma_law_not_a_priori(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "climb law from the field",
            "knob": "c the packet makes, read from the vorticity RHS",
            "tuning_the_pde": False,
            "tesla": "exacting, not a jerk. Ask the field. It did not give you c=8.",
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). Field occupation is not an a priori (B18e). Field-glue leftover is B19e. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_climb_law.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Climb law from the field. Knob is c the packet makes.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
