#!/usr/bin/env python3
"""
Residual tool: name the holes in R.

Classical NS. No Q1. No ε. No n=64.
The missing piece is an integrable R in
  dX/dt + ν‖∇ω‖₂² ≤ εν‖∇ω‖₂² + C_ε X R(t).
This apparatus splits the stretching leftover into
three holes on the working box and reads them.
Reading is not a bound.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_balance import packets
from track_b_lemmas import rec
from track_b_stretch import t0_samples


def holes() -> dict:
    stretch = t0_samples()
    bal = packets()
    hole1 = [r["frac_pos_hi"] for r in stretch]
    hole2 = [1.0 - r["frac_pos_hi"] for r in stretch]
    hole3 = [1.0 - r["share_of_all_pos"] for r in stretch]
    wmean = [r["wmean_cos3"] for r in stretch]
    mean = [r["mean_cos3"] for r in stretch]
    pd = [abs(r["P_over_D"]) for r in bal]
    xdot = [r["Xdot"] for r in bal]
    return {
        "n": 32,
        "hole1_aligned": hole1,
        "hole2_unaligned": hole2,
        "hole3_off_Ec": hole3,
        "wmean_cos3": wmean,
        "mean_cos3": mean,
        "P_over_D": pd,
        "Xdot": xdot,
        "hole1_mean": sum(hole1) / len(hole1),
        "hole2_mean": sum(hole2) / len(hole2),
        "hole3_mean": sum(hole3) / len(hole3),
        "pd_max": max(pd),
        "xdot_max": max(xdot),
    }


def lemma_residual_readable() -> dict:
    h = holes()
    parts = [a + b for a, b in zip(h["hole1_aligned"], h["hole2_unaligned"])]
    ok = (
        h["n"] == 32
        and all(abs(p - 1.0) < 1e-12 for p in parts)
        and h["hole1_mean"] > 0.5
        and all(w > m for w, m in zip(h["wmean_cos3"], h["mean_cos3"]))
        and h["pd_max"] < 0.05
        and h["xdot_max"] < 0.0
    )
    return rec(
        "B37_residual_readable",
        "three holes of R are readable on the n=32 caches: aligned P+, unaligned P+, off-E_c leftover",
        "pass" if ok else "fail",
        "Same caches as B15 / B16. No new FFT. No n=64. Named holes are not an integrable R.",
        n=h["n"],
        hole1_mean=h["hole1_mean"],
        hole2_mean=h["hole2_mean"],
        hole3_mean=h["hole3_mean"],
        pd_max=h["pd_max"],
        xdot_max=h["xdot_max"],
    )


def lemma_residual_not_a_priori() -> dict:
    return rec(
        "B37a_residual_not_a_priori",
        "naming the holes of R is a closed estimate for classical X",
        "fail",
        "A synthetic split is an apparatus. R is still the unknown. Sit down on leftover knobs.",
    )


def lemma_residual_not_continuation() -> dict:
    return rec(
        "B37b_residual_not_continuation",
        "readable holes make R integrable and therefore continue X",
        "fail",
        "Readability is not integrability. Hole 2 is the live cubic. Hole 1 is still an if. Hole 3 is not all-data Hardy.",
    )


def lemma_residual_not_ns() -> dict:
    return rec(
        "B37c_residual_not_ns",
        "the synthetic R is an NS a priori",
        "fail",
        "A skeleton with blanks is not sitting the packet. Do not promote a reconstruction to a type.",
    )


def lemma_residual_not_integral_max() -> dict:
    return rec(
        "B37d_residual_not_integral_max",
        "the residual tool is an integral bound on the max vorticity",
        "fail",
        "Named holes are not ∫‖ω‖_∞. Beale still asks for the max.",
    )


def lemma_residual_not_regularity() -> dict:
    return rec(
        "B37e_residual_not_regularity",
        "the residual tool decides classical regularity",
        "fail",
        "No. Domain B stays open. The leftover is still a closed estimate for X. Do not spawn n=64.",
    )


def lemma_residual_not_a_retune() -> dict:
    return rec(
        "B37f_not_a_pde_retune",
        "naming the holes of R is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. The tool is a knob on the check. No Q1. No ε. Do not type c=8. Do not spawn n=64.",
    )


def run(out: Path | None = None) -> dict:
    lemmas = [
        lemma_residual_readable(),
        lemma_residual_not_a_priori(),
        lemma_residual_not_continuation(),
        lemma_residual_not_ns(),
        lemma_residual_not_integral_max(),
        lemma_residual_not_regularity(),
        lemma_residual_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "residual tool: holes of R",
            "tuning_the_pde": False,
            "spawned_n64": False,
            "tesla": (
                "exacting, not a jerk. Name the holes. "
                "A script that must move. Reading is not a bound."
            ),
            "domain_verdict": "open",
        },
        "lemmas": lemmas,
        "counts": counts,
        "next_da_move": (
            "The residual tool names the holes in R. It is not an a priori. "
            "Hole 1 is the CF if. Hole 2 is the live cubic. Hole 3 is leftover weight. "
            "Regularity leftover is not an a priori (B35e). Regularity stays open. "
            "Do not spawn n=64. B4c stands. Do not cancel to Φ."
        ),
    }
    dest = Path(out) if out is not None else Path("results/track_b_residual.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Track B residual. Holes named. Not a bound.")
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("counts", payload["counts"])
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
