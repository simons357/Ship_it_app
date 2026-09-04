#!/usr/bin/env python3
"""
Short evolution of a CONC packet. We do not stop at t=0.

Classical NS, no Q1, no ε. Integrating-factor RK2 on T^3.
Resolved shells do not produce the saving climb. A finer /
longer cascade is another check, not a close.
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
    make_grid,
    mask_band,
    project,
    rec,
    three_shell_field,
)

C_SAVE = 8.0
_RUNS: dict[str, dict] | None = None


def shell_masses(oxh, oyh, ozh, k2, vol, jlo: int = 1, jhi: int = 5) -> dict[int, float]:
    out = {}
    for j in range(jlo, jhi + 1):
        band = mask_band(k2, 2.0 ** (j - 1), 2.0**j)
        oxj, oyj, ozj = ifft(oxh * band), ifft(oyh * band), ifft(ozh * band)
        out[j] = float(np.mean(oxj * oxj + oyj * oyj + ozj * ozj)) * vol
    return out


def packet_stats(masses: dict[int, float], jstar0: int) -> dict:
    tot = sum(masses.values()) or 1e-30
    js = list(masses)
    jbar = sum(j * masses[j] for j in js) / tot
    jnow = max(js, key=lambda j: masses[j])
    lo, hi = max(jnow - 1, min(js)), min(jnow + 1, max(js))
    sigma = sum(masses[j] for j in range(lo, hi + 1)) / tot
    above = sum(masses[j] for j in js if j > jstar0 + 1) / tot
    return {
        "jbar": float(jbar),
        "jstar": int(jnow),
        "sigma": float(sigma),
        "above": float(above),
        "X": float(tot),
    }


def ifrk2_step(uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, nu, dt):
    u, v, w = ifft(uh), ifft(vh), ifft(wh)
    cu, cv, cw = convect(u, v, w, uh, vh, wh, kx, ky, kz)
    cuh, cvh, cwh = project(
        fft(cu) * dealias, fft(cv) * dealias, fft(cw) * dealias, kx, ky, kz, k2_safe
    )
    decay = np.exp(-nu * k2 * dt)
    uh1, vh1, wh1 = project(
        (uh - dt * cuh) * decay,
        (vh - dt * cvh) * decay,
        (wh - dt * cwh) * decay,
        kx,
        ky,
        kz,
        k2_safe,
    )
    u1, v1, w1 = ifft(uh1), ifft(vh1), ifft(wh1)
    cu1, cv1, cw1 = convect(u1, v1, w1, uh1, vh1, wh1, kx, ky, kz)
    c1uh, c1vh, c1wh = project(
        fft(cu1) * dealias, fft(cv1) * dealias, fft(cw1) * dealias, kx, ky, kz, k2_safe
    )
    return project(
        (uh - 0.5 * dt * (cuh + c1uh)) * decay,
        (vh - 0.5 * dt * (cvh + c1vh)) * decay,
        (wh - 0.5 * dt * (cwh + c1wh)) * decay,
        kx,
        ky,
        kz,
        k2_safe,
    )


def evolve_packet(
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
    ox, oy, oz, oxh, oyh, ozh = curl(uh, vh, wh, kx, ky, kz)
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
    ox, oy, oz, oxh, oyh, ozh = curl(uh, vh, wh, kx, ky, kz)
    start = packet_stats(shell_masses(oxh, oyh, ozh, k2, vol), jstar)
    for _ in range(steps):
        uh, vh, wh = ifrk2_step(uh, vh, wh, kx, ky, kz, k2, k2_safe, dealias, nu, dt)
    ox, oy, oz, oxh, oyh, ozh = curl(uh, vh, wh, kx, ky, kz)
    end = packet_stats(shell_masses(oxh, oyh, ozh, k2, vol), jstar)
    t = steps * dt
    c_mean = (end["jbar"] - start["jbar"]) / max(t, 1e-30)
    return {
        "n": n,
        "jstar0": jstar,
        "nu": nu,
        "T": t,
        "steps": steps,
        "start": start,
        "end": end,
        "c_mean": float(c_mean),
        "X_grew": bool(end["X"] > start["X"] + 1e-9),
        "finite": bool(math.isfinite(end["X"]) and end["X"] > 0.0),
    }


def runs() -> dict[str, dict]:
    global _RUNS
    if _RUNS is None:
        _RUNS = {
            "visc": evolve_packet(nu=0.1),
            "euler": evolve_packet(nu=0.0),
        }
    return _RUNS


def lemma_run_completes() -> dict:
    visc, euler = runs()["visc"], runs()["euler"]
    ok = visc["finite"] and euler["finite"] and (not visc["X_grew"])
    return rec(
        "B13_short_run",
        "a short classical IF-RK2 step of a CONC packet stays finite; viscous X does not grow",
        "pass" if ok else "fail",
        "We did not stop at t=0. The field ran. Tesla: that is the next knob.",
        visc=visc,
        euler=euler,
    )


def lemma_no_saving_climb() -> dict:
    visc, euler = runs()["visc"], runs()["euler"]
    any_save = visc["c_mean"] >= C_SAVE or euler["c_mean"] >= C_SAVE
    return rec(
        "B13a_no_saving_climb",
        "a short evolution produces mean c ≥ 8 on a CONC packet",
        "fail" if not any_save else "open",
        "Viscous c_mean is negative. Euler is ~0. Letting it run did not hand us B11c.",
        c_save=C_SAVE,
        visc_c=visc["c_mean"],
        euler_c=euler["c_mean"],
    )


def lemma_no_high_fill() -> dict:
    visc, euler = runs()["visc"], runs()["euler"]
    filled = visc["end"]["above"] > 1e-3 or euler["end"]["above"] > 1e-3
    return rec(
        "B13b_no_high_fill",
        "a short run fills resolved shells above the original triad",
        "fail" if not filled else "open",
        "Resolved mass above j*+1 stays ~0. n=32 dealias cannot host a fat j=4. Still a reading.",
        visc_above=visc["end"]["above"],
        euler_above=euler["end"]["above"],
    )


def lemma_stays_conc() -> dict:
    visc = runs()["visc"]
    ok = visc["end"]["sigma"] >= 0.5
    return rec(
        "B13c_stays_conc",
        "the short viscous run stays 3-CONC",
        "pass" if ok else "fail",
        "The clock did not sneak into SPREAD. They stayed concentrated and still did not climb.",
        sigma_end=visc["end"]["sigma"],
    )


def lemma_visc_still_down() -> dict:
    visc = runs()["visc"]
    down = visc["end"]["jbar"] < visc["start"]["jbar"]
    return rec(
        "B13d_visc_still_down",
        "a short viscous evolution is a ladder for j_bar",
        "fail" if down else "open",
        "Along the trajectory, j_bar falls. Same direction as the t=0 RHS.",
        jbar0=visc["start"]["jbar"],
        jbarT=visc["end"]["jbar"],
    )


def lemma_finer_open() -> dict:
    return rec(
        "B13e_longer_not_saving",
        "a finer / longer run produces a saving climb",
        "fail",
        "Longer n=32 past the B11c room time does not produce c=8 (B22). Finer (n>32) is a box knob (B22e), not a close. Do not spawn n=64.",
    )


def lemma_evolve_not_a_priori() -> dict:
    return rec(
        "B13f_evolve_not_X_a_priori",
        "a packet DNS run is a closed a priori bound for classical X",
        "fail",
        "Short missed (B13a). Longer past room time missed (B22). A decaying n=32 packet is a check, not continuation (B23).",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_run_completes(),
        lemma_no_saving_climb(),
        lemma_no_high_fill(),
        lemma_stays_conc(),
        lemma_visc_still_down(),
        lemma_finer_open(),
        lemma_evolve_not_a_priori(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "short CONC evolution",
            "tuning_the_pde": False,
            "stopped_at_t0": False,
            "tesla": "exacting, not a jerk. Let the field run. It still did not give you c=8.",
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). Enstrophy-balance leftover is B16e. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_evolve.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Short CONC evolution. We did not stop at t=0.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
