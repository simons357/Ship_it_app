#!/usr/bin/env python3
"""
Residual tool: name the holes in R.

Classical NS. No Q1. No ε. No n=64.
The missing piece is an integrable R in
  dX/dt + ν‖∇ω‖₂² ≤ εν‖∇ω‖₂² + C_ε X R(t).
This apparatus splits the stretching leftover into
three holes on the working box and reads them.
Miller λ2+ is a different cut from hole 2, from the
same eigh. Reading is not a bound.
"""

from __future__ import annotations

import json
from pathlib import Path

from track_b_balance import packets
from track_b_lemmas import rec
from track_b_stretch import t0_samples

ROOT = Path(__file__).resolve().parents[1]
STRETCH_CACHE = ROOT / "results" / "track_b_stretch.json"
MILLER_GAP = 0.10


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


def miller_cut() -> dict:
    rows = t0_samples()
    hole2 = [1.0 - r["frac_pos_hi"] for r in rows]
    share_l2p = [r["share_l2p"] for r in rows]
    share_e2 = [r["share_e2_hi"] for r in rows]
    share_both = [r["share_h2_and_l2p"] for r in rows]
    gaps = [abs(a - b) for a, b in zip(hole2, share_l2p)]
    return {
        "n": 32,
        "hole2": hole2,
        "share_l2p": share_l2p,
        "share_e2_hi": share_e2,
        "share_h2_and_l2p": share_both,
        "gap_h2_l2p": gaps,
        "hole2_mean": sum(hole2) / len(hole2),
        "l2p_mean": sum(share_l2p) / len(share_l2p),
        "e2_mean": sum(share_e2) / len(share_e2),
        "both_mean": sum(share_both) / len(share_both),
        "gap_mean": sum(gaps) / len(gaps),
    }


def hole_times() -> dict:
    data = json.loads(STRETCH_CACHE.read_text())
    by = {row["name"]: row for row in data["lemmas"]}
    ends = list(by["B15d_run_keeps_aligned_budget"]["visc_frac_hi_end"])
    xs = list(by["B15d_run_keeps_aligned_budget"]["visc_X"])
    return {
        "hole1_end": ends,
        "x_start": [pair[0] for pair in xs],
        "x_end": [pair[1] for pair in xs],
        "hole1_end_min": min(ends),
        "x_dropped": all(b < a for a, b in xs),
    }


def lemma_residual_not_a_retune() -> dict:
    return rec(
        "B37f_not_a_pde_retune",
        "naming the holes of R is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. The tool is a knob on the check. No Q1. No ε. Do not type c=8. Do not spawn n=64.",
    )


def lemma_miller_readable() -> dict:
    m = miller_cut()
    t = hole_times()
    ok = (
        m["n"] == 32
        and m["gap_mean"] > MILLER_GAP
        and m["e2_mean"] < m["hole2_mean"] - 0.10
        and t["hole1_end_min"] > 0.5
        and t["x_dropped"]
    )
    return rec(
        "B38_miller_readable",
        "Miller λ2+ is a different cut from hole 2; hole 1(t) on the B15 cache stays a majority while visc eats X",
        "pass" if ok else "fail",
        "Same eigh as B15. No new FFT. No n=64. A different cut is not an integrable R.",
        n=m["n"],
        hole2_mean=m["hole2_mean"],
        l2p_mean=m["l2p_mean"],
        e2_mean=m["e2_mean"],
        both_mean=m["both_mean"],
        gap_mean=m["gap_mean"],
        hole1_end_min=t["hole1_end_min"],
    )


def lemma_miller_not_a_priori() -> dict:
    return rec(
        "B38a_miller_not_a_priori",
        "the Miller cut is a closed estimate for classical X",
        "fail",
        "λ2+ is a different name for part of the cubic. Miller's identity is not an a priori. A strain model with the same identity blows.",
    )


def lemma_miller_not_continuation() -> dict:
    return rec(
        "B38b_miller_not_continuation",
        "a different cut plus hole 1(t) makes R integrable and therefore continues X",
        "fail",
        "A gap of 0.15 on this ensemble is not ∫‖λ2+‖_q < ∞. Hole 1(t) staying a majority is B15d in hole language.",
    )


def lemma_miller_not_ns() -> dict:
    return rec(
        "B38c_miller_not_ns",
        "reading λ2+ on the working box is an NS a priori",
        "fail",
        "Keeping the middle eigenvalue of an already-computed eigh is a knob on the check. Sit down.",
    )


def lemma_miller_not_integral_max() -> dict:
    return rec(
        "B38d_miller_not_integral_max",
        "the Miller cut is an integral bound on the max vorticity",
        "fail",
        "λ2+ is not ∫‖ω‖_∞. Beale still asks for the max.",
    )


def lemma_miller_not_regularity() -> dict:
    return rec(
        "B38e_miller_not_regularity",
        "the Miller cut decides classical regularity",
        "fail",
        "No. Domain B stays open. Do not spawn n=64.",
    )


def lemma_miller_not_a_retune() -> dict:
    return rec(
        "B38f_not_a_pde_retune",
        "reading λ2+ is a retune of classical Navier–Stokes",
        "fail",
        "The PDE is untouched. No Q1. No ε. Do not type c=8. Do not spawn n=64.",
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
        lemma_miller_readable(),
        lemma_miller_not_a_priori(),
        lemma_miller_not_continuation(),
        lemma_miller_not_ns(),
        lemma_miller_not_integral_max(),
        lemma_miller_not_regularity(),
        lemma_miller_not_a_retune(),
    ]
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in lemmas:
        counts[row["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "residual tool: holes of R, then the Miller cut",
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
            "The residual tool names the holes in R. Miller λ2+ is a different cut from hole 2. "
            "Neither is an a priori. Hole 1 is the CF if. Hole 2 is the live cubic. "
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
    print("Track B residual. Holes named. Miller cut is different. Not a bound.")
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("counts", payload["counts"])
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
