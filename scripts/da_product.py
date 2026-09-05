#!/usr/bin/env python3
"""
DA product: capabilities for a possible license.

What it is. What a licensee can do. What they cannot
sell. This is a spec, not a contract.
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


CAN = [
    "Name a leftover and get a HAVE / WRITE / THEN chain",
    "Diagnose work already on the desk and name the legal write",
    "Translate English into a slot plus a math sentence",
    "Score a candidate pass / fail / open",
    "Refuse glue and fake last lines",
    "Print status of what sits versus what is open",
]

CANNOT = [
    "Finish an open WRITE by emitting it",
    "Close NS / RH / YM / BSD / Hodge / P vs NP by running DA",
    "Sell Theorem A as classical NS",
    "Sell Q as RH or BSD",
    "Sell SFE as Hodge or P vs NP",
    "Sell a hidden leftover close",
    "Sell prize packaging of an open leftover",
]


CLAIMS = [
    rec(
        "L1",
        "support_machine",
        "DA is a support / anti-bullshit process machine",
        "pass",
        "Ordinary AI proposes. Scripts score. Open and fail are allowed.",
    ),
    rec(
        "L2",
        "no_chops",
        "The operator does not need the chops",
        "pass",
        "Asking is the product. The chain is the assist.",
    ),
    rec(
        "L3",
        "sell_as_qed",
        "DA is a leftover closer you can sell as QED",
        "fail",
        "Emit is not QED. check B stays open. A license is not a close.",
    ),
    rec(
        "L4",
        "license_includes_mp_sits",
        "A license includes sitting MP leftovers",
        "fail",
        "Poincare sits in the literature. A this PDE sits. The rest stay WRITE.",
    ),
    rec(
        "L5",
        "this_is_a_contract",
        "This note is a legal license",
        "fail",
        "Capabilities spec. Not a contract. Not legal advice.",
    ),
]


def is_product_ask(ask: str) -> bool:
    """License / sell / under the hood / capabilities."""
    text = (ask or "").lower().strip()
    if not text:
        return False
    return bool(
        re.search(
            r"\blicense\b|\bsell(ing)? it\b|\bsell it\b|"
            r"under the hood|capabilities|"
            r"what (can|can't|cannot) (i|you|we) do with it|"
            r"\bda product\b|\bif i (choose to )?sell\b|"
            r"what i can do with it",
            text,
        )
    )


def run(out: Path | None = None) -> dict:
    payload = {
        "meta": {
            "question": "what is DA, what can a licensee do, what must they not sell",
            "writeup": "docs/DA-PRODUCT.md",
            "not_a_contract": True,
            "emit_is_not_qed": True,
            "sell_as_qed": False,
        },
        "is": (
            "Anti-bullshit process machine. Four slots (A, B, Q, U). "
            "AI proposes. Scripts score. Operator runs the command."
        ),
        "can": CAN,
        "cannot": CANNOT,
        "claims": CLAIMS,
        "counts": {
            "can": len(CAN),
            "cannot": len(CANNOT),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
        },
        "next_da_move": (
            "License the process: write, diagnose, refuse, score. "
            "Do not license a leftover close."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_product.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_product(out: Path | None = None) -> dict:
    payload = run(out=out)
    print("PRODUCT  (capabilities; not a contract)")
    print(payload["is"])
    print()
    print("CAN")
    for row in payload["can"]:
        print(f"  - {row}")
    print()
    print("CANNOT")
    for row in payload["cannot"]:
        print(f"  - {row}")
    print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return payload


def main() -> int:
    print_product()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
