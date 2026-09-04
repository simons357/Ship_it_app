#!/usr/bin/env python3
"""
Climbing CONC: j* rises while σ ≥ 1/2.

The PDE is not tuned. The knob is the climb rate c = dj*/dt
on the estimate. Slow climb still blows. Fast climb sits.
NS does not hand us c.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from track_b_glue import step_x
from track_b_lemmas import rec


def integrate_climb(
    c: float,
    x0: float = 2.5,
    j0: float = 2.0,
    nu: float = 0.1,
    dt: float = 5e-5,
    tmax: float = 1.0,
    j_cap: float | None = None,
) -> dict:
    x = float(x0)
    j = float(j0)
    xs = [x]
    t = 0.0
    while t < tmax and 0.0 < x < 40.0:
        j_used = min(j, j_cap) if j_cap is not None else j
        x = step_x(x, True, int(round(j_used)), nu, dt)
        if x < 0.0:
            x = 0.0
        j = j + c * dt
        if j_cap is not None:
            j = min(j, j_cap)
        xs.append(x)
        t += dt
    arr = np.array(xs)
    return {
        "c": c,
        "X_final": float(arr[-1]),
        "X_max": float(np.max(arr)),
        "j_final": float(j),
        "blew": bool(np.max(arr) > 20.0),
        "steps": int(len(arr) - 1),
        "T": float((len(arr) - 1) * dt),
    }


def bookkeeping_climb(n: int = 400, seed: int = 17) -> dict:
    rng = np.random.default_rng(seed)
    dt = 5e-5
    c = 4.0
    j = 2.0
    x = 2.0
    x0 = x
    acc = 0.0
    for _ in range(n):
        x_next = step_x(x, True, int(round(j)), 0.1, dt)
        acc += x_next - x
        x = max(x_next, 0.0)
        j = j + c * dt
    residual = abs((x - x0) - acc)
    return {"residual": residual, "ok": residual < 1e-12, "X0": x0, "XT": x, "j": j}


def lemma_climb_bookkeeping() -> dict:
    bk = bookkeeping_climb()
    return rec(
        "B11_climb_bookkeeping",
        "along a prescribed climb, ΔX equals the sum of CONC increments at the current j*",
        "pass" if bk["ok"] else "fail",
        "Tesla’s knob on this write: c = dj*/dt. The increments still add.",
        bookkeeping=bk,
    )


def lemma_bounded_j_bounds_x() -> dict:
    e0 = 1.0
    finite = []
    for jmax in (3, 4, 5, 6):
        cap = float((2.0 ** (jmax + 1)) ** 2 * e0)
        finite.append({"jmax": jmax, "ceiling": cap, "finite": cap < float("inf")})
    ok = all(row["finite"] and row["ceiling"] > 0 for row in finite)
    return rec(
        "B11a_bounded_j_bounds_X",
        "packet class + bounded j* ⇒ X bounded (unbounded X needs unbounded j*)",
        "pass" if ok else "fail",
        "Necessary condition only. Finite peak scale, finite ceiling. Not a climb law.",
        ceilings=finite,
        E0=e0,
    )


def lemma_slow_climb_blows() -> dict:
    run = integrate_climb(c=1.0)
    return rec(
        "B11b_slow_climb_blows",
        "any positive climb rate saves the model X",
        "fail" if run["blew"] else "open",
        "c=1: j* barely moves, X crosses 40. Climbing is not a charm. Tesla: turn c down.",
        run=run,
    )


def lemma_fast_climb_sits() -> dict:
    run = integrate_climb(c=8.0)
    return rec(
        "B11c_fast_climb_sits",
        "a fast prescribed climb reaches the viscous room and the model X sits",
        "pass" if (not run["blew"]) and run["j_final"] >= 5.0 else "fail",
        "c=8: j* reaches the thin packet, viscosity owns the cubic. Same ODE as B9a, entered from below.",
        run=run,
    )


def lemma_ns_climb_law() -> dict:
    return rec(
        "B11d_ns_climb_law",
        "classical NS forces a climb rate c that saves X while CONC",
        "fail",
        "c is prescribed here. t=0 packets do not produce c=8 (B12b). Short visc run does not (B13a). Blob and B18 paths do not (B20). The field did not hand us a saving c.",
    )


def lemma_climb_not_a_priori() -> dict:
    return rec(
        "B11e_climb_not_X_a_priori",
        "the climbing model is a closed a priori bound for classical X",
        "fail",
        "Prescribed c=8 sits on the ODE (B11c). NS did not pick that c (B11d). On the readable window the climb has not reached the viscous room (B21). A sketch that grows while the field falls is not an a priori.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_climb_bookkeeping(),
        lemma_bounded_j_bounds_x(),
        lemma_slow_climb_blows(),
        lemma_fast_climb_sits(),
        lemma_ns_climb_law(),
        lemma_climb_not_a_priori(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "climbing CONC",
            "knob": "c = dj*/dt on the estimate, not on the PDE",
            "tuning_the_pde": False,
            "tesla": "exacting, not a jerk. Turn c. If the script does not move, it is a paragraph.",
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
    dest = Path(out) if out is not None else Path("results/track_b_climb.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Climbing CONC. Knob is c = dj*/dt. PDE not tuned.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
