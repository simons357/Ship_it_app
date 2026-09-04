#!/usr/bin/env python3
"""
Enstrophy balance as an a priori: a decaying net is not a bound.

Classical NS. No Q1. No ε. No Biot–Savart slogan.
B16: Ẋ = 2P − 2D. B16a: visc owns this ensemble.
B16b: P_+ is not a net cubic. This write asks whether
that reading closes X. It does not.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_balance import (
    CANCEL_MAX,
    PD_MAX,
    lemma_enstrophy_identity,
    lemma_plus_not_a_cubic,
    lemma_visc_owns_net,
    packets,
)
from track_b_lemmas import rec


def lemma_net_readable() -> dict:
    ident = lemma_enstrophy_identity()
    visc = lemma_visc_owns_net()
    plus = lemma_plus_not_a_cubic()
    ok = (
        ident["verdict"] == "pass"
        and visc["verdict"] == "pass"
        and plus["verdict"] == "fail"
        and all(abs(r) < PD_MAX for r in visc["P_over_D"])
        and all(c < CANCEL_MAX for c in plus["cancel"])
        and all(xd < 0.0 for xd in visc["Xdot"])
    )
    return rec(
        "B27_net_readable",
        "enstrophy identity, visc-owned net, and cancelled P_+ are readable together",
        "pass" if ok else "fail",
        "The identity holds. |P|/D sits below 0.05. Plus and minus cancel. Typed c is not written into the PDE.",
        rel=ident["rel"],
        P_over_D=visc["P_over_D"],
        cancel=plus["cancel"],
        Xdot=visc["Xdot"],
    )


def lemma_visc_ensemble_not_a_priori() -> dict:
    rows = packets()
    return rec(
        "B27a_visc_ensemble_not_a_priori",
        "viscosity owning the net on these packets closes a bound for classical X",
        "fail",
        "Ẋ < 0 on a random-phase ensemble is a reading. Leray’s dissipation did the work here. That is not continuation.",
        P_over_D=[r["P_over_D"] for r in rows],
        Xdot=[r["Xdot"] for r in rows],
    )


def lemma_cancel_not_all_data() -> dict:
    rows = packets()
    return rec(
        "B27b_cancel_not_all_data",
        "random-phase cancellation of ∫ω·Sω is an a priori for every 3-CONC field",
        "fail",
        "B16d already missed. A coherent field can have P ≈ (ω·Sω)_+. Fluids did not promote a packet to a class.",
        cancel=[r["cancel"] for r in rows],
    )


def lemma_decay_not_continuation() -> dict:
    rows = packets()
    return rec(
        "B27c_decay_not_continuation",
        "a decaying L² packet is a continuation argument for classical X",
        "fail",
        "X falling here does not bound X on a live cubic. B23 already refused DNS-never-blew-up. So does a cancelled net.",
        Xdot=[r["Xdot"] for r in rows],
        X=[r["X"] for r in rows],
    )


def lemma_net_not_integral_max() -> dict:
    rows = packets()
    return rec(
        "B27d_net_not_integral_max",
        "the enstrophy identity is an integral bound on the max vorticity",
        "fail",
        "Ẋ = 2P − 2D is L². A fat-packet ratio ‖ω‖_∞/‖ω‖₂ ~ 0.2 is not ∫‖ω‖_∞. Do not improve the identity into the max.",
        bkm_gap=[r["bkm_gap"] for r in rows],
    )


def lemma_coherent_leftover() -> dict:
    return rec(
        "B27e_coherent_leftover",
        "the signed-strain blob closes X",
        "open",
        "The net is scored. The leftover close on a coherent CONC field is B17e. Not a bigger FFT. Do not spawn n=64.",
    )


def lemma_net_not_a_retune() -> dict:
    return rec(
        "B27f_not_a_pde_retune",
        "scoring the enstrophy balance as not an a priori is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. The net is a knob on the estimate: a cancellation you can miss. No Q1. No ε.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_net_readable(),
        lemma_visc_ensemble_not_a_priori(),
        lemma_cancel_not_all_data(),
        lemma_decay_not_continuation(),
        lemma_net_not_integral_max(),
        lemma_coherent_leftover(),
        lemma_net_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "enstrophy balance as an a priori",
            "tuning_the_pde": False,
            "tesla": (
                "exacting, not a jerk. Net production is a number. "
                "Viscosity owned this ensemble. That is not continuation."
            ),
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). "
            "Enstrophy balance is not an a priori (B16e). Coherent leftover is B17e. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_net.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Enstrophy balance as an a priori. A decaying net is not a bound.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
