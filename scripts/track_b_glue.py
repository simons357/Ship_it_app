#!/usr/bin/env python3
"""
Glue: B4c on CONC, energy-class T on SPREAD, against the B8 clock.

A two-regime enstrophy ODE. High-j* CONC holds. Low-j* CONC
can still blow. The bookkeeping is not a bound for X.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from track_b_lemmas import rec


def step_x(x: float, conc: bool, jstar: int, nu: float, dt: float) -> float:
    """
    CONC (B4c):  Ẋ = α_c(j*) X³ − ν 2^{2j*} X
    SPREAD (T):  Ẋ = α_s X² − ν λ X
    α_c shrinks with j* (packet leftover). α_s is energy-class, no extra scale.
    """
    if conc:
        alpha = 0.4 * (0.5 ** max(jstar - 2, 0))
        gamma = nu * (2.0 ** (2 * jstar))
        return x + dt * (alpha * x**3 - gamma * x)
    alpha_s = 0.8
    lam = 1.5
    return x + dt * (alpha_s * x**2 - nu * lam * x)


def integrate(conc: np.ndarray, jstar: int, nu: float = 0.1, x0: float = 1.15, dt: float = 2e-4):
    x = float(x0)
    xs = [x]
    for c in conc:
        x = step_x(x, bool(c), jstar, nu, dt)
        if x < 0.0:
            x = 0.0
        xs.append(x)
        if x > 40.0:
            break
    arr = np.array(xs)
    return {
        "X_final": float(arr[-1]),
        "X_max": float(np.max(arr)),
        "blew": bool(np.max(arr) > 20.0),
        "steps": int(len(arr) - 1),
        "T": float((len(arr) - 1) * dt),
        "tau_conc": float(np.sum(conc[: len(arr) - 1]) * dt),
    }


def bookkeeping_identity(n: int = 400, seed: int = 13) -> dict:
    """Discrete telescope: ΔX equals the sum of the two regime increments."""
    rng = np.random.default_rng(seed)
    dt = 2e-4
    conc = rng.random(n) > 0.45
    jstar = 4
    nu = 0.1
    x = 1.15
    acc_c = 0.0
    acc_s = 0.0
    x0 = x
    for c in conc:
        x_next = step_x(x, bool(c), jstar, nu, dt)
        inc = x_next - x
        if c:
            acc_c += inc
        else:
            acc_s += inc
        x = max(x_next, 0.0)
    residual = abs((x - x0) - (acc_c + acc_s))
    return {"residual": residual, "ok": residual < 1e-12, "X0": x0, "XT": x}


def high_j_holds() -> dict:
    n = 8000
    conc = np.ones(n, dtype=bool)
    run = integrate(conc, jstar=5)
    return {**run, "ok": (not run["blew"]) and run["X_final"] < 2.0}


def low_j_can_blow() -> dict:
    n = 20000
    conc = np.ones(n, dtype=bool)
    run = integrate(conc, jstar=2, x0=2.5, dt=5e-5)
    return {**run, "ok_as_kill": run["blew"]}


def switching_high_j() -> dict:
    n = 12000
    conc = np.resize(np.array([True] * 80 + [False] * 80), n)
    run = integrate(conc, jstar=5)
    return {**run, "ok": not run["blew"]}


def lemma_bookkeeping() -> dict:
    bk = bookkeeping_identity()
    return rec(
        "B9_glue_bookkeeping",
        "ΔX = increment_CONC + increment_SPREAD against the B8 clock",
        "pass" if bk["ok"] else "fail",
        "Tesla’s first knob: the two columns add. That is the apparatus, not a bound.",
        bookkeeping=bk,
    )


def lemma_high_j_glue() -> dict:
    run = high_j_holds()
    return rec(
        "B9a_glue_high_jstar",
        "B4c-scale CONC (high j*) plus the clock keeps the model X bounded",
        "pass" if run["ok"] else "fail",
        "Same weight, both sides, at the thin packet. Olga’s instinct, Tesla’s knob.",
        run=run,
    )


def lemma_low_j_blows() -> dict:
    run = low_j_can_blow()
    return rec(
        "B9b_glue_low_jstar_blows",
        "the glued ODE bounds X for low-j* CONC as well",
        "fail" if run["ok_as_kill"] else "open",
        "Fat slow CONC. The leftover cubic still wins. The glue is not all-data.",
        run=run,
    )


def lemma_switching() -> dict:
    run = switching_high_j()
    return rec(
        "B9c_glue_switching",
        "switching high-j* CONC with SPREAD keeps the model X bounded",
        "pass" if run["ok"] else "fail",
        "The clock can flip. High packets plus energy-class T do not blow this ODE.",
        run=run,
    )


def lemma_glue_not_regularity() -> dict:
    return rec(
        "B9d_glue_not_X_a_priori",
        "the glued model is a closed a priori bound for classical X",
        "open",
        "A two-regime ODE is a sketch of the estimate. It is not the estimate on NS.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_bookkeeping(),
        lemma_high_j_glue(),
        lemma_low_j_blows(),
        lemma_switching(),
        lemma_glue_not_regularity(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "glue to X",
            "tesla": "exacting, not a jerk. He will not sit a paragraph.",
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Stay with high-j* CONC + energy-class T. "
            "Low-j* CONC is the remaining cubic. That is the live room."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_glue.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Glue to X. Two columns against the clock.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
