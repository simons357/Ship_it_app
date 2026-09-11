#!/usr/bin/env python3
"""
Estimate audit filter. Axisymmetric shell estimate.

KEEP may enter. DISCARD does not enter the identity,
the Young step, or the claim. PARK is another stack.
Not a proof. NS is not solved.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from track_b_lemmas import rec  # noqa: E402

DISCARD_MARKERS = (
    "coherence viscosity",
    "gcd spectral attractor",
    "e8 cathedral",
    "prime-harmonic lock",
    "borromean coherence",
    "gematria",
    "lightning flash",
    "clay is solved",
    "unconditional 3-d regularity",
    "unconditional 3d regularity",
    "coherence-floor",
    "prime gates",
    "titanh",
    "harborsafe",
)

# Constitutive Q-stack / SFE as NS. Naming as "other PDE" is allowed.
DISCARD_AS_NS = (
    "q1 as clay",
    "q6 as clay",
    "sfe closes ns",
    "sfe as ns",
)


def classify_paragraph(text: str) -> dict:
    """Flag discard markers. A hit means the paragraph is out of this estimate."""
    low = text.lower()
    hits = [m for m in DISCARD_MARKERS if m in low]
    hits += [m for m in DISCARD_AS_NS if m in low]
    return {
        "discard_hits": hits,
        "allowed_in_estimate": len(hits) == 0,
    }


def lemmas() -> list[dict]:
    return [
        rec(
            "EAud_filter_seated",
            "KEEP / DISCARD / PARK is the writing rule for the next estimate",
            "pass",
            "Axisymmetric shell estimate. Not unrestricted 3-D. Not ★. Not H1.",
        ),
        rec(
            "EAud_class_named",
            "class is axisymmetric with swirl, remainder T_{j←j}",
            "pass",
            "First sentence names class, quantity, remainder, brackets.",
        ),
        rec(
            "EAud_lambda_bookkeeping",
            "Lambda' = 2(Tc-ν Ds)/X is bookkeeping",
            "pass",
            "Already on disk as an identity check. Not the claim LHS.",
        ),
        rec(
            "EAud_remainder_named",
            "the only remainder in Audit Door 1 is T_{j←j}",
            "pass",
            "Named hole. Not Attack-6 Door 1 (pre-Young C), which is off.",
        ),
        rec(
            "EAud_tau_seated",
            "closed-triad rewrite τ is a theorem on this branch",
            "fail",
            "Allowed to enter. Not seated.",
        ),
        rec(
            "EAud_omega_star_seated",
            "shift by lattice constant ω_* is a theorem on this branch",
            "fail",
            "Allowed to enter. Not seated. Do not shift by Λ.",
        ),
        rec(
            "EAud_door1_closed",
            "Audit Door 1 shell budget is closed",
            "fail",
            "Remainder T_{j←j} is open.",
        ),
        rec(
            "EAud_door3_closed",
            "Door 3 alignment α is a bound",
            "fail",
            "Criterion to test. Separate from occupancy. Not CFM imported.",
        ),
        rec(
            "EAud_discard_in_claim",
            "discard list may enter the claim sentence",
            "fail",
            "SFE, Q-stack as NS, large [SND], gematria, Clay-is-solved: out.",
        ),
        rec(
            "EAud_ns_solved",
            "axisymmetric shell filter solves NS",
            "fail",
            "Class and measured ρ_j stay in the sentence. NS not solved.",
        ),
    ]


def run(out: Path | None = None) -> dict:
    rows = lemmas()
    counts = {"pass": 0, "fail": 0, "open": 0}
    for item in rows:
        counts[item["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "axisymmetric shell estimate audit",
            "class": "axisymmetric with swirl",
            "remainder": "T_{j<-j}",
            "tuning_the_pde": False,
            "lemma_star_open": True,
            "h1_started": False,
            "estimate_open": True,
            "kill": False,
        },
        "lemmas": rows,
        "counts": counts,
        "domain_verdict": "open",
        "discard_self_check": classify_paragraph(
            "Axisymmetric-with-swirl NS; shell Z_j; remainder T_{j<-j}; no extra field."
        ),
    }
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--check", type=str, default=None, help="classify one paragraph")
    args = p.parse_args()
    if args.check is not None:
        print(json.dumps(classify_paragraph(args.check), indent=2))
        return
    print(json.dumps(run(out=args.out), indent=2))


if __name__ == "__main__":
    main()
