#!/usr/bin/env python3
"""
DA done: is the written chain a finish?

The study is whether DA can write the chain, diagnose,
and name the leftover. Emitting the chain is not QED.
Theorem A is done for the Q1 PDE. Classical NS is not.
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


ROWS = [
    {
        "id": "A_this_pde",
        "name": "Track A, this PDE (eps>0, beta>=1/2)",
        "done": True,
        "verdict": "pass",
        "why": "Theorem A. Ladyzhenskaya / p-Laplacian. That close is real.",
    },
    {
        "id": "A_uniform",
        "name": "Track A, uniform H1 as eps->0",
        "done": False,
        "verdict": "open",
        "why": "A_uniform_H1 open. A7/A9 fail on the box. Not a no-go for all data.",
    },
    {
        "id": "B",
        "name": "Track B, classical NS (Navi / unaugmented)",
        "done": False,
        "verdict": "open",
        "why": "Chain written through (5). Line (6) does not sit. check B stays open.",
    },
    {
        "id": "emit",
        "name": "DA wrote the chains",
        "done": True,
        "verdict": "pass",
        "why": "That is the study. Write, diagnose, refuse glue. Emit is not the leftover.",
    },
    {
        "id": "A_is_B",
        "name": "Theorem A is classical NS",
        "done": False,
        "verdict": "fail",
        "why": "Different equation. Hearing A closed is the fake classical close.",
    },
]


CLAIMS = [
    rec(
        "E1",
        "study_is_the_write",
        "The study is whether DA can write the chain, diagnose, and name the leftover",
        "pass",
        "Fix category errors. Print HAVE / WRITE / THEN. That is the product.",
    ),
    rec(
        "E2",
        "a_this_pde_done",
        "The Q1-augmented chain at eps>0 is done",
        "pass",
        "Theorem A. That is the close already heard for this PDE.",
    ),
    rec(
        "E3",
        "emit_means_b_done",
        "The written Navier-Stokes chain means classical NS is done",
        "fail",
        "The chain is the argument. Line (6) is still a write. C3 already fail.",
    ),
    rec(
        "E4",
        "da_finishes_by_printing",
        "DA finishes classical leftover by emitting the chain",
        "fail",
        "An LLM may phrase a candidate. The checker scores it. check B stays open.",
    ),
    rec(
        "E5",
        "hearing_a_is_navi",
        "Hearing Theorem A closed means Navi Stokes is done",
        "fail",
        "That close is the Q1 PDE. Exporting it onto B is the refuse.",
    ),
    rec(
        "E6",
        "b_may_sit",
        "Classical line (6) may sit later",
        "open",
        "All-data integrable R, A1, A2, or a killing field. Then Gronwall / Beale / bootstrap.",
    ),
    rec(
        "E7",
        "finish_bad_closes",
        "Please finish bad closes leftover (6)",
        "fail",
        "Finish-bad prints the B chain. Line (6) still does not sit.",
    ),
]


def is_done_ask(ask: str) -> bool:
    """Is NS done / is that right / can DA finish."""
    from da_study import is_study_ask

    text = (ask or "").lower().strip()
    if not text:
        return False
    if is_study_ask(text):
        return False
    return bool(
        re.search(
            r"\bis (that |it |ns |navier |navi |navi(?:er)?.?stokes )?(done|finished|complete)\b|"
            r"\bis that right\b|"
            r"\bdid da\b|"
            r"\bcan da\b|"
            r"\blooks like.{0,24}done\b|"
            r"\b(ns|navier|navi|track b).{0,24}(done|finished|complete)\b|"
            r"\bda done\b|\bis it done\b",
            text,
        )
    )


def run(out: Path | None = None) -> dict:
    payload = {
        "meta": {
            "question": "is Navier-Stokes done? can DA finish it?",
            "writeup": "docs/DA-DONE.md",
            "study_is_the_write": True,
            "emit_is_not_qed": True,
            "a_this_pde_done": True,
            "a_uniform_not_done": True,
            "b_not_done": True,
            "a_is_not_b": True,
        },
        "rows": ROWS,
        "claims": CLAIMS,
        "counts": {
            "done": sum(1 for r in ROWS if r["done"]),
            "not_done": sum(1 for r in ROWS if not r["done"]),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "answer": (
            "Track A this PDE: done. Track A uniform H1: not done. "
            "Track B classical NS: not done. DA wrote the chains. That is the study, not X."
        ),
        "next_da_move": (
            "Classical leftover is still line (6). Classify one candidate. "
            "Do not cash Theorem A as Navi Stokes."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_done.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_done(out: Path | None = None) -> dict:
    payload = run(out=out)
    print("DONE?  (emit is not QED)")
    print(payload["answer"])
    print()
    for row in payload["rows"]:
        tag = "DONE" if row["done"] else row["verdict"].upper()
        print(f"  [{tag}] {row['name']}")
        print(f"         {row['why']}")
    print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return payload


def main() -> int:
    print_done()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
