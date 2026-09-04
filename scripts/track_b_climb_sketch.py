#!/usr/bin/env python3
"""
Climb sketch: the B11c ODE, read against the NS window.

Classical NS. No Q1. No ε. Prescribed c=8 sits on a long
ODE (B11c). NS did not pick that c (B11d). This write asks
whether that sitting path is the working-box field.
The climb has not reached the viscous room on T=0.064.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_climb import integrate_climb
from track_b_climb_law import C_SAVE
from track_b_field_occ import DT, NU, STEPS, paths
from track_b_glue import model_xdot, step_x
from track_b_lemmas import rec

J0 = 2.0
X0 = 2.5
J_ROOM = 5.0
_CMP: dict | None = None


def window_climb(
    c: float = C_SAVE,
    x0: float = X0,
    j0: float = J0,
    nu: float = NU,
    dt: float = DT,
    steps: int = STEPS,
) -> dict:
    x = float(x0)
    j = float(j0)
    for _ in range(steps):
        x = max(step_x(x, True, int(round(j)), nu, dt), 0.0)
        j = j + c * dt
    t = steps * dt
    return {
        "c": c,
        "X0": float(x0),
        "XT": float(x),
        "dX": float(x - x0),
        "j0": float(j0),
        "jT": float(j),
        "dj": float(j - j0),
        "T": float(t),
        "Xdot0": float(model_xdot(x0, int(round(j0)), nu, True)),
        "reached_room": bool(j >= J_ROOM),
        "X_fell": bool(x < x0 - 1e-9),
    }


def comparison() -> dict:
    global _CMP
    if _CMP is None:
        ode = window_climb()
        long = integrate_climb(c=C_SAVE)
        ns = paths()
        pack = ns["packet"]
        t_room = (J_ROOM - J0) / C_SAVE
        _CMP = {
            "ode": ode,
            "long": {
                "X_final": long["X_final"],
                "X_max": long["X_max"],
                "j_final": long["j_final"],
                "blew": long["blew"],
                "T": long["T"],
            },
            "ns": {
                "X0": pack["X0"],
                "XT": pack["XT"],
                "dX": pack["XT"] - pack["X0"],
                "jbar0": pack["jbar0"],
                "jbarT": pack["jbarT"],
                "dj": pack["jbarT"] - pack["jbar0"],
                "c_mean": pack["c_mean"],
                "T": pack["steps"] * pack["dt"],
            },
            "t_room": t_room,
            "window_over_room": ode["T"] / max(t_room, 1e-30),
            "sign_match": (ode["dX"] > 0.0) == ((pack["XT"] - pack["X0"]) > 0.0),
        }
    return _CMP


def lemma_window_rates() -> dict:
    cmp = comparison()
    ok = (
        cmp["ode"]["T"] > 0.0
        and cmp["ns"]["T"] > 0.0
        and abs(cmp["ode"]["T"] - cmp["ns"]["T"]) < 1e-12
        and cmp["long"]["j_final"] >= J_ROOM
        and not cmp["long"]["blew"]
    )
    return rec(
        "B21_window_rates",
        "the c=8 climb ODE and the NS packet are both readable on the B18 window; B11c still sits on the long ODE",
        "pass" if ok else "fail",
        "Same T=0.064 as B18 / B19 / B20. Long ODE is B11c. Typed c is not written into the PDE.",
        T=cmp["ode"]["T"],
        ode_jT=cmp["ode"]["jT"],
        ode_XT=cmp["ode"]["XT"],
        ns_jbarT=cmp["ns"]["jbarT"],
        ns_XT=cmp["ns"]["XT"],
        long_j_final=cmp["long"]["j_final"],
        long_T=cmp["long"]["T"],
    )


def lemma_not_the_room() -> dict:
    cmp = comparison()
    in_room = cmp["ode"]["reached_room"] or cmp["ode"]["T"] >= cmp["t_room"]
    return rec(
        "B21a_not_the_room",
        "on the working-box window, prescribed c=8 has already reached the viscous room j* ≥ 5",
        "fail" if not in_room else "open",
        "j: 2 → 2.51. Time to j=5 at c=8 is 0.375. The window is 0.064. The sitting of B11c has not arrived.",
        jT=cmp["ode"]["jT"],
        j_room=J_ROOM,
        t_room=cmp["t_room"],
        T=cmp["ode"]["T"],
        window_over_room=cmp["window_over_room"],
    )


def lemma_not_the_sitting() -> dict:
    cmp = comparison()
    return rec(
        "B21b_not_the_sitting",
        "the B11c sitting path is the NS packet on this window",
        "fail" if not cmp["sign_match"] else "open",
        "Climb ODE X grows 2.5 → 2.67. NS X falls 2.5 → 1.43. B11c sits on T ≈ 0.81. This box is T=0.064.",
        dX_ode=cmp["ode"]["dX"],
        dX_ns=cmp["ns"]["dX"],
        sign_match=cmp["sign_match"],
        long_T=cmp["long"]["T"],
        long_X_max=cmp["long"]["X_max"],
    )


def lemma_delta_j_not_prescribed() -> dict:
    cmp = comparison()
    close = abs(cmp["ns"]["dj"] - cmp["ode"]["dj"]) < 0.25
    return rec(
        "B21c_delta_j_not_prescribed",
        "NS Δj_bar on the packet equals the prescribed climb c T",
        "fail" if not close else "open",
        "Prescribed Δj = 0.512. NS Δj_bar ≈ −0.015. The field went the other way.",
        dj_ode=cmp["ode"]["dj"],
        dj_ns=cmp["ns"]["dj"],
        c_mean_ns=cmp["ns"]["c_mean"],
        c_save=C_SAVE,
    )


def lemma_sketch_did_not_save() -> dict:
    cmp = comparison()
    sat = cmp["ode"]["X_fell"] and cmp["ode"]["reached_room"]
    return rec(
        "B21d_sketch_did_not_save",
        "on the working-box window the c=8 sketch already sits (X falling, j* in the viscous room)",
        "fail" if not sat else "open",
        "Model X still grows. t=0 Ẋ = +2.25, same fat cubic as frozen j*=2. Climbing has not owned the cubic yet.",
        dX_ode=cmp["ode"]["dX"],
        Xdot0=cmp["ode"]["Xdot0"],
        jT=cmp["ode"]["jT"],
    )


def lemma_sketch_not_close() -> dict:
    return rec(
        "B21e_sketch_not_X_a_priori",
        "matching the c=8 sketch to a longer / finer NS run closes a bound for classical X",
        "open",
        "The sketch is not this field. Finer/longer is B13e. Typing c=8 into the PDE is a retune. Not continuation.",
    )


def lemma_sketch_not_a_retune() -> dict:
    return rec(
        "B21f_not_a_pde_retune",
        "reading the c=8 ODE against the NS window, or writing c=8 into classical Navier–Stokes, is a retune of the PDE",
        "fail",
        "The PDE is untouched. c is a knob on the estimate. No Q1. No ε. Do not type B11c into the equation.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_window_rates(),
        lemma_not_the_room(),
        lemma_not_the_sitting(),
        lemma_delta_j_not_prescribed(),
        lemma_sketch_did_not_save(),
        lemma_sketch_not_close(),
        lemma_sketch_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "climb sketch; B11c ODE against the NS window",
            "tuning_the_pde": False,
            "tesla": (
                "exacting, not a jerk. The sitting of c=8 is a long ODE. "
                "This window is short. The field did not follow the rate."
            ),
            "domain_verdict": "open",
            "c_save": C_SAVE,
            "j_room": J_ROOM,
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget leftover is B15e. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_climb_sketch.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Climb sketch. B11c against the NS window.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
