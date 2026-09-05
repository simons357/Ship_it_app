#!/usr/bin/env python3
"""
DA Q: the inverse-GCD paper, the floors, Q6, Q7.

The best GCD paper on this desk is August inverse-GCD
(Zenodo 22045478), also called Q6 hygiene. Live floors
are Bridge*, Theorem P, H_N >= -1. Full Q > -1/2 is
false. Q is not RH, not SND, not Track B.
Q7 is not seated.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def rec(
    hid: str,
    name: str,
    statement: str,
    verdict: str,
    why: str,
) -> dict:
    return {
        "id": hid,
        "name": name,
        "statement": statement,
        "verdict": verdict,
        "why": why,
    }


PAPER = {
    "name": "August inverse-GCD (Zenodo 22045478) — Q6 hygiene",
    "also": "spectral-floor retraction, docs/SPECTRAL-FLOOR-EXPLORATION.md",
    "slot": "Q",
    "sits": [
        {
            "id": "Bridge*",
            "what": "R(e_p - e_q) > -1/2 on Q-tilde",
            "verdict": "pass",
        },
        {
            "id": "Theorem P",
            "what": "prime-supported Q-tilde >= -1/4",
            "verdict": "pass",
        },
        {
            "id": "H-floor",
            "what": "lambda_min(H_N) >= -1 (pairing)",
            "verdict": "pass",
        },
        {
            "id": "orthant",
            "what": "v >= 0 => v^T Q-tilde v >= 0",
            "verdict": "pass",
        },
    ],
    "false": [
        {
            "id": "full_Q",
            "what": "lambda_min(Q_N) > -1/2",
            "verdict": "fail",
            "why": "Q_10 ~ -1.90",
        },
        {
            "id": "H_314",
            "what": "lambda_min(H_N) >= -3/14",
            "verdict": "fail",
            "why": "H_4 ~ -0.225",
        },
        {
            "id": "Q_is_RH",
            "what": "Theorem P / H_N is RH",
            "verdict": "fail",
            "why": "a GCD matrix is not a zero",
        },
        {
            "id": "Q_is_SND",
            "what": "Q6 with gamma>3/2 enforces SND",
            "verdict": "fail",
            "why": "May T3 glue. Withdrawn.",
        },
    ],
    "open": [
        {
            "id": "H_sharp",
            "what": "lambda_min(H_N) >= -1/4",
            "verdict": "open",
            "why": "numeric through N=200; pairing does not prove it",
        },
        {
            "id": "spectral_limit",
            "what": "lambda_min(Q-tilde_N) / log N has a finite limit",
            "verdict": "open",
            "why": "values sit near -0.16. Not a floor at -1/2. Old Route C shape.",
        },
        {
            "id": "multirep",
            "what": "multi-rep Bridge* stays above -1/2",
            "verdict": "open",
            "why": "numeric through N=200 is not a proof",
        },
    ],
}


NAMES = [
    {
        "id": "Q6_paper",
        "name": "Q6",
        "is": "the August inverse-GCD note (22045478). Hygiene. Bridge* and the floor withdrawal.",
        "is_not": "Montgomery-Dyson pair correlation, Route C Gap 1 complete, or SND.",
    },
    {
        "id": "Q6_old",
        "name": "Q6 (old slogan)",
        "is": "lambda_min / log N, operator-to-Mertens, mixed Q vs Q-tilde vs H. Still open as arithmetic.",
        "is_not": "Gap 1 complete. That log is stale.",
    },
    {
        "id": "Q7",
        "name": "Q7",
        "is": "not seated on this desk. No file, no theorem id.",
        "is_not": "a hidden close of RH, SND, or Track B. Do not invent the paper.",
    },
]


CLAIMS = [
    rec(
        "Q1",
        "paper_is_q6",
        "The best GCD paper on this desk is Q6 hygiene (22045478)",
        "pass",
        "August inverse-GCD plus the spectral-floor retraction.",
    ),
    rec(
        "Q2",
        "da_finds_sitting_floors",
        "DA can find the floors that sit: Bridge*, Theorem P, H_N>=-1",
        "pass",
        "Those are scored. The pairing and the prime-block split are theorems.",
    ),
    rec(
        "Q3",
        "da_finds_retracted_floor",
        "DA can find the retracted full Q floor lambda_min(Q)>-1/2",
        "fail",
        "That floor is false. Finding it would be reviving a counterexample.",
    ),
    rec(
        "Q4",
        "electoral_is_spectral",
        "The electoral / actual / spectral floor is one Q object",
        "pass",
        "Live: H_N>=-1 and Theorem P. Sharp H_N>=-1/4 is the remaining floor write.",
    ),
    rec(
        "Q5",
        "q6_is_snd",
        "Q6 with gamma>3/2 enforces SND",
        "fail",
        "Withdrawn glue. Q is a matrix. SND is fluids.",
    ),
    rec(
        "Q6c",
        "gap1_complete",
        "Route C Gap 1 is complete",
        "fail",
        "Stale against the Aug 2026 Q6 audit. Spectral-limit still open.",
    ),
    rec(
        "Q7c",
        "q7_seated",
        "Q7 is already a named theorem on this desk",
        "fail",
        "Not in the tree. Do not mint Q7 to look finished.",
    ),
    rec(
        "Q8",
        "q_is_rh_or_b",
        "The GCD paper closes RH or classical NS",
        "fail",
        "Q is inverse-GCD. Different object.",
    ),
    rec(
        "Q9",
        "sharp_later",
        "H_N>=-1/4 or the spectral-limit may sit later",
        "open",
        "Those are the named Q writes. They are not Q7 until a paper is typed.",
    ),
]


def is_q_ask(ask: str) -> bool:
    """Look at the GCD paper / Q6 / Q7 / spectral floor."""
    text = (ask or "").lower().strip()
    if not text:
        return False
    if re.search(r"\bwrite rh\b|\brh proof\b|\briemann\b", text):
        return False
    if re.search(
        r"\bis that right\b|\bis (ns |navier |navi )?done\b|\bcan da finish\b",
        text,
    ):
        return False
    return bool(
        re.search(
            r"\bgcd\b|\binverse.?gcd\b|\bq6\b|\bq7\b|"
            r"\belectoral floor\b|\bspectral floor\b|\bactual floor\b|"
            r"\bbest gcd\b|\bgcd paper\b|\btheorem p\b|"
            r"\bwhere does q7\b|\bwhat about q6\b",
            text,
        )
    )


def run(out: Path | None = None) -> dict:
    payload = {
        "meta": {
            "question": "look at the GCD paper; electoral floor; Q6; Q7",
            "writeup": "docs/DA-Q.md",
            "paper": "docs/SPECTRAL-FLOOR-EXPLORATION.md",
            "q_is_not_rh": True,
            "q_is_not_b": True,
            "q7_not_seated": True,
            "full_floor_false": True,
        },
        "paper": PAPER,
        "names": NAMES,
        "claims": CLAIMS,
        "answer": (
            "Best GCD paper is Q6 hygiene (22045478). "
            "Sitting floors: Bridge*, Theorem P, H_N>=-1. "
            "Retracted floor cannot be found (false). "
            "Sharp H_N>=-1/4 open. "
            "Q6 is that paper, not SND. "
            "Q7 is not seated."
        ),
        "counts": {
            "sits": sum(1 for r in PAPER["sits"] if r["verdict"] == "pass"),
            "false": sum(1 for r in PAPER["false"] if r["verdict"] == "fail"),
            "open": len(PAPER["open"]),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "claim_open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "next_da_move": (
            "Keep the sitting Q floors. Write H_N>=-1/4 or the spectral-limit "
            "if you want the next Q sentence. Do not mint Q7. Do not glue to RH or B."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_q.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_q(out: Path | None = None) -> dict:
    payload = run(out=out)
    print("Q  (inverse-GCD paper; floors; Q6; Q7)")
    print(payload["answer"])
    print()
    print(f"PAPER  slot {PAPER['slot']}")
    print(f"  {PAPER['name']}")
    print(f"  {PAPER['also']}")
    print("  sits:")
    for row in PAPER["sits"]:
        print(f"    [HAVE] {row['id']}: {row['what']}")
    print("  withdrawn:")
    for row in PAPER["false"]:
        print(f"    [FAIL] {row['id']}: {row['what']}  ({row['why']})")
    print("  remaining Q writes:")
    for row in PAPER["open"]:
        print(f"    [OPEN] {row['id']}: {row['what']}  ({row['why']})")
    print()
    print("NAMES")
    for row in NAMES:
        print(f"  {row['name']}")
        print(f"    is: {row['is']}")
        print(f"    is not: {row['is_not']}")
    print()
    print("ELECTORAL / SPECTRAL FLOOR")
    print("  DA can find the floors that sit (H_N>=-1, Theorem P, Bridge*).")
    print("  DA cannot find lambda_min(Q)>-1/2. That statement is false.")
    print("  The remaining floor write is H_N>=-1/4.")
    print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return payload


def main() -> int:
    print_q()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
