#!/usr/bin/env python3
"""
DA Q: the inverse-GCD paper, the floors, Q6, Q7.

The best GCD paper on this desk is August inverse-GCD
(Zenodo 22045478), also called Q6 hygiene. Live floors
are Bridge*, Theorem P, H_N >= -1. Full Q > -1/2 is
false. Q is not RH, not SND, not Track B.
Q7 is not seated.

Gold box = Goldbach. The T-name that sits is Theorem P.
Goldbach-shaped nonzero v_k has R >= -2/9 (odd-prime corollary).
That is not Goldbach's conjecture. (3,5) sharpness stays open.
The other far leftover is H_N >= -1/4.
GNC stays withdrawn.
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


FLOOR_LINES = [
    {
        "n": 1,
        "status": "have",
        "text": (
            "Three matrices. Q_N = 1/gcd(i,j). "
            "Q-tilde_N(i,j) = 1/(gcd(i,j) sqrt(i j)). "
            "H_N = D^{-1/2} Q-tilde D^{-1/2}, D = diag(Q-tilde 1). "
            "Do not mix them."
        ),
    },
    {
        "n": 2,
        "status": "have",
        "text": (
            "Full Q floor is false. lambda_min(Q_10) ~ -1.90. "
            "lambda_min(Q-tilde_20) ~ -0.505. Composites kill Q-tilde."
        ),
    },
    {
        "n": 3,
        "status": "have",
        "text": (
            "Bridge*. On Q-tilde, v = e_p - e_q: "
            "R(v) = (1/2)(1/p^2 + 1/q^2) - 1/sqrt(p q) > -1/2 "
            "because p q >= 6. Two-line identity. Not lambda_min."
        ),
    },
    {
        "n": 4,
        "status": "have",
        "text": (
            "Theorem P. Prime block A = u u^T + D with "
            "u_p = p^{-1/2}, D_pp = 1/p^2 - 1/p. "
            "uu^T >= 0 and min D = -1/4 at p=2. "
            "Hence lambda_min(Q-tilde |_P) >= -1/4."
        ),
    },
    {
        "n": 5,
        "status": "have",
        "text": (
            "Theorem H-floor. w^T Q-tilde w + w^T D w "
            "= (1/2) sum Q-tilde_ij (w_i + w_j)^2 >= 0. "
            "So w^T Q-tilde w >= - w^T D w, i.e. lambda_min(H_N) >= -1 "
            "for every N. This is the unrestricted spectral floor that sits."
        ),
    },
    {
        "n": 6,
        "status": "write",
        "text": (
            "WRITE. lambda_min(H_N) >= -1/4 for all N. "
            "Numeric through N=200 (worst H_4 ~ -0.225). "
            "The pairing that proves -1 does not prove -1/4. "
            "Do not revive -3/14."
        ),
    },
    {
        "n": 7,
        "status": "follows",
        "text": (
            "If (6) sits, the full-index floor is sharp at -1/4. "
            "Still not RH. Still not SND. Still not Track B."
        ),
    },
    {
        "n": 8,
        "status": "open",
        "text": (
            "Spectral-limit leftover. lambda_min(Q-tilde_N)/log N "
            "sits near -0.16. Compatible with a finite limit. "
            "That is the old Route C shape. It is not a floor at -1/2. "
            "Gap 1 complete is stale."
        ),
    },
]


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
        {
            "id": "Goldbach-shaped",
            "what": "nonzero v_k has R >= -2/9 on Q-tilde",
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
        {
            "id": "GNC",
            "what": "GNC is a live Goldbach detector",
            "verdict": "fail",
            "why": "vanishes on an actual pair. Shelved. Not Theorem P.",
        },
        {
            "id": "Goldbach_conjecture",
            "what": "this matrix write is Goldbach's conjecture",
            "verdict": "fail",
            "why": "v_k=0 if there is no pair. No Rayleigh. Different object.",
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
            "id": "Goldbach_sharp",
            "what": "multi-rep never undercuts (3,5)",
            "verdict": "open",
            "why": (
                "Numeric through N=200 stays ~ -0.183. "
                "Odd-prime D gives -2/9, not the pair."
            ),
        },
    ],
}


# Voice: gold box = Goldbach. T-name = Theorem P. Not T2 / Titchmarsh / T3.
PAIR = {
    "gold_box": "Goldbach",
    "t_name": "Theorem P",
    "sits": (
        "Theorem P. Prime-supported Q-tilde |_P >= -1/4. "
        "Rank-one split A = uu^T + D. This is the T-name that sits."
    ),
    "follows": (
        "Goldbach-shaped. Nonzero v_k lives on odd primes "
        "(2+(k-2) is even; only k=4 is (2,2), and that cancels). "
        "Hence R >= -2/9 > -1/2. Corollary of Theorem P. "
        "Not Goldbach's conjecture."
    ),
    "leftover": (
        "Never undercuts (3,5) ~ -0.183. Numeric through N=200. "
        "The other far leftover is H_N >= -1/4."
    ),
    "withdrawn": (
        "GNC. Goldbach detector / prime-indicator difference. "
        "v_k vanishes on an actual Goldbach pair. Shelved. Not RH."
    ),
    "not_these": (
        "Not the integer conjecture. Not T2 (fluids). "
        "Not Titchmarsh. Not T3 / triple lock. Not Tao."
    ),
}


GOLDBACH_LINES = [
    {
        "n": 1,
        "status": "have",
        "text": (
            "Theorem P. Any prime-supported v has R >= -1/4 "
            "because A = uu^T + D and min D = -1/4 at p=2."
        ),
    },
    {
        "n": 2,
        "status": "have",
        "text": (
            "v_k = sum_{p+q=k}(e_p-e_q) is prime-supported. "
            "Already R >= -1/4 when v_k != 0."
        ),
    },
    {
        "n": 3,
        "status": "have",
        "text": (
            "No 2. 2+(k-2)=k forces k-2 even. Only even prime "
            "is 2, so k=4 and (2,2) cancels. Nonzero v_k has v_k(2)=0."
        ),
    },
    {
        "n": 4,
        "status": "have",
        "text": (
            "Odd-prime D. min_{p>=3}(1/p^2-1/p) = 1/9-1/3 = -2/9. "
            "Hence R(v_k) >= -2/9 > -1/2."
        ),
    },
    {
        "n": 5,
        "status": "follows",
        "text": (
            "The matrix leftover 'multi-rep stays above -1/2' sits. "
            "This is not every even integer as p+q."
        ),
    },
    {
        "n": 6,
        "status": "open",
        "text": (
            "Never undercuts (3,5) ~ -0.183. Numeric through N=200. "
            "Odd-prime D does not prove the pair."
        ),
    },
]


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
    {
        "id": "Theorem_P",
        "name": "Theorem P",
        "is": "the T-name that sits. Prime-supported Q-tilde >= -1/4. Rank-one split.",
        "is_not": "RH, SND, Goldbach's conjecture, T2, or GNC.",
    },
    {
        "id": "Goldbach",
        "name": "Goldbach (gold box)",
        "is": (
            "Goldbach-shaped multi-rep. Nonzero v_k has R >= -2/9 "
            "by Theorem P on odd primes."
        ),
        "is_not": (
            "Goldbach's conjecture. Not (3,5) sharpness. Not RH."
        ),
    },
    {
        "id": "GNC",
        "name": "GNC",
        "is": "withdrawn. Detector vanishes on an actual Goldbach pair.",
        "is_not": "the live Goldbach floor. That floor is the odd-prime corollary.",
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
    rec(
        "Q10",
        "t_name_is_theorem_p",
        "The T-name we got to a close is Theorem P",
        "pass",
        "Prime block Q-tilde >= -1/4. Rank-one split. Already scored.",
    ),
    rec(
        "Q11",
        "goldbach_shaped_floor",
        "Goldbach-shaped nonzero v_k has R >= -2/9 on Q-tilde",
        "pass",
        "2 is absent. Odd-prime D min is -2/9. Corollary of Theorem P.",
    ),
    rec(
        "Q12",
        "gnc_is_live",
        "GNC is the live Goldbach object",
        "fail",
        "Withdrawn. The sitting Goldbach object is the odd-prime corollary.",
    ),
    rec(
        "Q13",
        "goldbach_sharp_35",
        "Multi-rep never undercuts the pair (3,5)",
        "open",
        "Numeric through N=200. -2/9 is not -0.183.",
    ),
    rec(
        "Q14",
        "goldbach_conjecture",
        "This write is Goldbach's conjecture",
        "fail",
        "A Rayleigh on Q-tilde is not every even integer as p+q.",
    ),
]


def is_q_ask(ask: str) -> bool:
    """Look at the GCD paper / Q6 / Q7 / Goldbach / Theorem P."""
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
            r"\bwhere does q7\b|\bwhat about q6\b|"
            r"\bgoldbach\b|\bgold box\b|\bgnc\b|"
            r"\bmulti.?rep\b|\bgoldbach.?shaped\b",
            text,
        )
    )


def run(out: Path | None = None) -> dict:
    payload = {
        "meta": {
            "question": "look at the GCD paper; electoral floor; Q6; Q7",
            "writeup": "docs/DA-Q.md",
            "paper": "docs/SPECTRAL-FLOOR-EXPLORATION.md",
            "goldbach": "docs/GOLDBACH-CHAIN.md",
            "q_is_not_rh": True,
            "q_is_not_b": True,
            "q7_not_seated": True,
            "full_floor_false": True,
            "goldbach_shaped_sits": True,
            "goldbach_conjecture_false": True,
        },
        "paper": PAPER,
        "lines": FLOOR_LINES,
        "goldbach_lines": GOLDBACH_LINES,
        "names": NAMES,
        "claims": CLAIMS,
        "pair": PAIR,
        "answer": (
            "Best GCD paper is Q6 hygiene (22045478). "
            "Sitting floors: Bridge*, Theorem P, H_N>=-1, "
            "Goldbach-shaped R>=-2/9. "
            "Gold box = Goldbach. The T-name that sits is Theorem P. "
            "The matrix leftover is a corollary: nonzero v_k has no 2, "
            "so R>=-2/9. Not Goldbach's conjecture. "
            "(3,5) sharpness open. "
            "The other far leftover is H_N>=-1/4. "
            "GNC stays withdrawn. "
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
            "Keep Theorem P and the Goldbach-shaped corollary. "
            "Write H_N>=-1/4 if you want the next floor sentence. "
            "Do not claim the integer conjecture. Do not unshelve GNC. "
            "Do not mint Q7. Do not glue to RH or B."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_q.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_q(out: Path | None = None) -> dict:
    payload = run(out=out)
    print("Q6  SPECTRAL FLOOR")
    print("  August inverse-GCD (Zenodo 22045478). Slot Q. Not RH. Not B.")
    print()
    print("THEOREM (sits)")
    print("  lambda_min(H_N) >= -1 for every N. Prime block Q-tilde >= -1/4.")
    print()
    print("GOLDBACH / THEOREM P")
    print(f"  Gold box = {PAIR['gold_box']}. The T-name that sits is {PAIR['t_name']}.")
    print(f"  [HAVE] {PAIR['sits']}")
    print(f"  [HAVE] {PAIR['follows']}")
    print(f"  [OPEN] {PAIR['leftover']}")
    print(f"  [FAIL] {PAIR['withdrawn']}")
    print(f"  {PAIR['not_these']}")
    print()
    print("GOLDBACH CHAIN")
    for L in GOLDBACH_LINES:
        tag = {
            "have": "HAVE",
            "write": "WRITE",
            "follows": "THEN",
            "open": "OPEN",
        }[L["status"]]
        print(f"  ({L['n']}) [{tag}] {L['text']}")
    print()
    print("PROOF CHAIN  (ground floor up)")
    for L in FLOOR_LINES:
        tag = {
            "have": "HAVE",
            "write": "WRITE",
            "follows": "THEN",
            "open": "OPEN",
        }[L["status"]]
        print(f"  ({L['n']}) [{tag}] {L['text']}")
    print()
    print("If (6) sits, the full-index floor is sharp. Emit is not that close.")
    print("Do not glue Q6 onto SND, RH, or Navi Stokes.")
    print()
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
