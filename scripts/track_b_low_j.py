#!/usr/bin/env python3
"""
Low-j* CONC: energy ceiling, not a retune of the PDE.

Classical NS is not being tuned. Q1 stays off. ε stays off.
The B9b model forgot X ≤ K^2 E at frozen packet support.
That trajectory is not NS-legal. Climbing j* is the remaining room.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

from track_b_lemmas import rec, three_shell_field, ifft, curl


def packet_energy_enstrophy(n: int, jstar: int, rng: np.random.Generator) -> dict:
    uh, vh, wh, kx, ky, kz, k2 = three_shell_field(n, jstar, rng)
    u, v, w = ifft(uh), ifft(vh), ifft(wh)
    ox, oy, oz, _, _, _ = curl(uh, vh, wh, kx, ky, kz)
    vol = (2.0 * math.pi) ** 3
    energy = float(np.mean(u * u + v * v + w * w)) * vol
    enstrophy = float(np.mean(ox * ox + oy * oy + oz * oz)) * vol
    kabs = np.sqrt(np.maximum(k2, 0.0))
    support = (np.abs(uh) + np.abs(vh) + np.abs(wh)) > 0
    k_max = float(np.max(kabs[support])) if np.any(support) else 0.0
    ratio = enstrophy / max(energy * max(k_max**2, 1e-30), 1e-30)
    return {
        "E": energy,
        "X": enstrophy,
        "k_max": k_max,
        "ceiling": energy * k_max**2,
        "X_over_ceiling": ratio,
        "jstar": jstar,
    }


def lemma_energy_ceiling(n: int = 32, seed: int = 11) -> dict:
    rng = np.random.default_rng(seed)
    rows = []
    worst = 0.0
    for jstar in (2, 3, 4):
        st = packet_energy_enstrophy(n, jstar, rng)
        rows.append(st)
        worst = max(worst, st["X_over_ceiling"])
    ok = worst <= 1.0 + 1e-9
    return rec(
        "B10_energy_ceiling",
        "packet support |k|≤K ⇒ X ≤ K² E (frozen j* has an energy ceiling)",
        "pass" if ok else "fail",
        "Leray’s energy, Bernstein’s support. Not a retune of the PDE. Tesla: the model forgot a knob.",
        samples=rows,
        worst_X_over_ceiling=worst,
        n=n,
    )


def lemma_frozen_blow_not_ns() -> dict:
    """B9b lets X run away at frozen j*=2. NS cannot: X ≤ K² E."""
    from track_b_glue import low_j_can_blow

    blow = low_j_can_blow()
    jstar = 2
    k = 2.0 ** (jstar + 1)
    # Near-saturated packet: E0 = X0 / K². Ceiling sits on the initial datum.
    x0 = 2.5
    e_sat = x0 / (k**2)
    ceiling_sat = (k**2) * e_sat
    model_unbounded = bool(blow["blew"])
    past_sat = float(blow["X_max"]) > ceiling_sat + 1e-9
    illegal = model_unbounded and past_sat
    return rec(
        "B10a_frozen_blow_not_ns",
        "the B9b X→∞ trajectory at frozen j* is an NS-legal path",
        "fail" if illegal else "open",
        "Frozen support caps X by K² E. A near-saturated packet has no room to run to 40. The model forgot E.",
        blow=blow,
        E_sat=e_sat,
        K=k,
        ceiling_sat=ceiling_sat,
    )


def lemma_ceiling_not_climbing() -> dict:
    e0 = 1.0
    ceilings = {j: float((2.0 ** (j + 1)) ** 2 * e0) for j in (2, 3, 4, 5, 6)}
    rises = ceilings[6] > 10.0 * ceilings[2]
    return rec(
        "B10b_ceiling_not_climbing",
        "the energy ceiling bounds X even if j* climbs",
        "fail" if rises else "open",
        "K grows with j*. The cap rises. Frozen-j* hygiene is not a climbing-packet bound.",
        ceilings=ceilings,
        E0=e0,
    )


def lemma_climbing_open() -> dict:
    return rec(
        "B10c_climbing_not_close",
        "CONC with climbing j* is a closed estimate for X",
        "fail",
        "Broken out as B11. NS did not force a saving c (B11d). The sketch is not an a priori (B11e). DNS is not an a priori (B13f).",
    )


def lemma_not_a_retune() -> dict:
    return rec(
        "B10d_not_a_pde_retune",
        "the energy ceiling is a retune of classical Navier–Stokes (Q1, ε, Φ-cancel)",
        "fail",
        "The PDE is untouched. No Q1. No ε. Keep 1/r^4. The knob is on the estimate, not the equation.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_energy_ceiling(),
        lemma_frozen_blow_not_ns(),
        lemma_ceiling_not_climbing(),
        lemma_climbing_open(),
        lemma_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "low-j CONC energy ceiling",
            "tuning_the_pde": False,
            "tesla": "exacting, not a jerk. Detune the apparatus. Do not retune the machine.",
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "Packet geometry is not an a priori (B14d). Stretching budget is not an a priori (B15e). Enstrophy balance is not an a priori (B16e). Coherent blob is not an a priori (B17e). Field-occupation leftover is B18e. "
            "Finer (n>32) stays a box knob (B22e). Do not spawn n=64. "
            "B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_low_j.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Low-j CONC. Energy ceiling. PDE not tuned.")
    print("Tesla:", payload["meta"]["tesla"])
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
