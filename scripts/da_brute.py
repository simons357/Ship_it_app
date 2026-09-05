#!/usr/bin/env python3
"""
DA brute: why a supercomputer / quantum device cannot
try every permutation and write the leftover.

A machine can exhaust a finite list. The missing write
is all-data (or every zero). Combining known fails is glue.
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
    **extra,
) -> dict:
    row = {
        "id": hid,
        "name": name,
        "statement": statement,
        "verdict": verdict,
        "why": why,
    }
    row.update(extra)
    return row


FINITE = [
    "the n=32 box (and any larger n you can buy)",
    "published attempts already seated (living walls + Q scan)",
    "Q_N / H_N through a finite N (scanned to 200)",
    "eps in a finite list (0.2, 0.05, 0)",
    "a finite tuple of knobs",
]

NOT_FINITE = [
    "all smooth initial data",
    "all time (int_0^T R < infinity for arbitrary T)",
    "every non-trivial zero of zeta",
    "uniform H1 as eps->0, not at three values",
    "the classical PDE with no extra term (not a retune)",
]

VISUAL = """
  A MACHINE CAN EXHAUST                    THE WRITE IS
  ---------------------                    ------------
  finite n box                             all smooth data
  papers already seated                    one all-data integral
  Q_N through N=200                        every zero of zeta
  eps in {0.2, 0.05, 0}                    uniform as eps -> 0
  knob tuples                              the same PDE (no retune)

            finite list  --------------X------------>  all-data write
                         try-every does not cross

  QUANTUM DEVICE
    superposition of guesses  !=  a theorem
    Grover searches a list    !=  int_0^T R < infinity
    Shor factors integers     !=  Re rho = 1/2 for every rho
"""


CLAIMS = [
    rec(
        "K1",
        "finite_list_legal",
        "A machine may exhaust a finite list on one slot (box, N, seated papers)",
        "pass",
        "That is already what tracka / trackb / spectral_floor / living walls do.",
    ),
    rec(
        "K2",
        "try_every_writes",
        "Trying every known attempt and every combination writes the leftover",
        "fail",
        "The leftover is all-data. A list of fails is a library. Glue of fails is not a pass.",
    ),
    rec(
        "K3",
        "quantum_instantly",
        "A quantum computer tries every nuance instantly and emits the estimate",
        "fail",
        "Grover searches a list you already have. Shor factors. Neither writes an a priori.",
    ),
    rec(
        "K4",
        "permute_knobs",
        "Every permutation of knobs is the next write",
        "fail",
        "A knob is on the check, not the PDE. Retune of nodes.json is refused on B.",
    ),
    rec(
        "K5",
        "combine_papers",
        "Sit every paper at once and vote the missing line",
        "fail",
        "already scored: a council is not a close. Combining A and Q is glue.",
    ),
    rec(
        "K6",
        "bigger_n",
        "A supercomputer at n=64 or a never-blowup run is regularity",
        "fail",
        "B22e / T13. A box is not all data. Do not spawn n=64 as a close.",
    ),
    rec(
        "K7",
        "desk_already_tried_the_list",
        "The finite lists that sit on this desk were already tried and scored",
        "pass",
        "A lemmas, B through B41, Q through N=200, living walls L55-L76. That is the permutation you already have.",
    ),
    rec(
        "K8",
        "write_may_sit",
        "A new all-data write may sit later; it will not arrive as a sweep",
        "open",
        "One estimate: integrable R, uniform H1, or every zero on the line. Not a combination search.",
    ),
]


def is_brute_ask(ask: str) -> bool:
    text = (ask or "").lower().strip()
    if not text:
        return False
    return bool(
        re.search(
            r"\btry every\b|\bevery (combination|permutation|nuance|attempt)\b|"
            r"\bquantum comput|\bsupercomput|\bbrute\b|"
            r"\ball the combinations\b|\binstantly\b|"
            r"\bda brute\b|\btry them all\b",
            text,
        )
    )


def run(out: Path | None = None) -> dict:
    payload = {
        "meta": {
            "question": "why not try every permutation on a supercomputer / quantum device",
            "writeup": "docs/DA-BRUTE.md",
            "finite_list_is_legal": True,
            "try_every_is_not_a_write": True,
            "quantum_is_not_the_estimate": True,
        },
        "finite": FINITE,
        "not_finite": NOT_FINITE,
        "visual": VISUAL,
        "claims": CLAIMS,
        "counts": {
            "finite": len(FINITE),
            "not_finite": len(NOT_FINITE),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "next_da_move": (
            "Keep using the machine on a finite list (classify, check, attempt). "
            "Do not stand up a quantum device to permute knobs. "
            "The next write is still one all-data estimate."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_brute.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_brute(out: Path | None = None) -> dict:
    payload = run(out=out)
    print("BRUTE  (finite list vs the write)")
    print(payload["visual"])
    print("CAN TRY")
    for line in payload["finite"]:
        print(f"  - {line}")
    print("CANNOT HIT BY TRYING ALL")
    for line in payload["not_finite"]:
        print(f"  - {line}")
    print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return payload


def main() -> int:
    print_brute()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
