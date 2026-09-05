#!/usr/bin/env python3
"""
DA study: the questions were pointed at DA.

Can DA write the chain, diagnose, and refuse glue?
Yes. Can DA finish every leftover by emitting it?
No. That split is the study, not a solver pass.
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


ASKS = [
    {
        "id": "B_write",
        "ask": "Track B please write",
        "can_write": True,
        "can_finish": False,
        "why": "Chain through (5) emitted. Line (6) does not sit. check B stays open.",
    },
    {
        "id": "A_write",
        "ask": "Track A write",
        "can_write": True,
        "can_finish": True,
        "why": "Theorem A for this PDE already sits. Uniform H1 as eps->0 is a different write and is not finished.",
    },
    {
        "id": "RH_write",
        "ask": "use my best paper and write RH",
        "can_write": True,
        "can_finish": False,
        "why": "(1)-(5) have. (6) does not sit. The paper is Q, not the line.",
    },
    {
        "id": "NS_done",
        "ask": "is that right for Navi Stokes",
        "can_write": True,
        "can_finish": False,
        "why": "DA can split A vs B. Classical leftover is not done. Hearing A closed is the refuse.",
    },
    {
        "id": "Q_paper",
        "ask": "look at my best gcd paper / electoral floor",
        "can_write": True,
        "can_finish": True,
        "why": "Sitting floors found (Bridge*, Theorem P, H_N>=-1). Retracted Q>-1/2 correctly refused.",
    },
    {
        "id": "Q6_floor",
        "ask": "Q6. Spectral floor",
        "can_write": True,
        "can_finish": True,
        "why": "H-floor sits. Sharp H_N>=-1/4 is the remaining write and is not finished.",
    },
    {
        "id": "Q7",
        "ask": "where does Q7 fit",
        "can_write": True,
        "can_finish": False,
        "why": "Not seated. DA did not invent a paper. That refuse is the correct do.",
    },
]


CLAIMS = [
    rec(
        "S1",
        "questions_are_the_exam",
        "These questions are pointed at DA to see if it can do the job",
        "pass",
        "Write, diagnose, refuse glue, name the leftover. That is the study.",
    ),
    rec(
        "S2",
        "da_can_write",
        "DA can emit a have / write / follows chain when named",
        "pass",
        "B, A, RH, Q6 floor. Asking is the product.",
    ),
    rec(
        "S3",
        "da_can_refuse",
        "DA can refuse A=>B, Q=>RH, Q6=>SND, and a minted Q7",
        "pass",
        "The refuse is a scored fail, not a shrug.",
    ),
    rec(
        "S4",
        "da_finishes_by_emit",
        "DA finishes every leftover by printing the chain",
        "fail",
        "Emit is not QED. B (6), RH (6), A uniform H1, H_N>=-1/4 stay writes.",
    ),
    rec(
        "S5",
        "da_is_a_solver",
        "If DA can do the study job then classical NS is done",
        "fail",
        "Support is not X. Theorem A is a different equation.",
    ),
    rec(
        "S6",
        "open_writes_later",
        "An open WRITE line may sit later",
        "open",
        "Classify one candidate. DA may phrase. The checker scores it.",
    ),
    rec(
        "S7",
        "da_finished_just_now",
        "DA finished those proofs just now",
        "fail",
        "Sitting theorems already sat. Open WRITE lines still open. An emit is a reprint.",
    ),
    rec(
        "S8",
        "agent_phrased",
        "The session writes were the agent operating DA",
        "pass",
        "DA is scripts plus scored docs. The agent phrases. DA reprints. Neither is a second author of (6).",
    ),
]


def is_study_ask(ask: str) -> bool:
    """The questions were pointed at DA: can it do the job."""
    text = (ask or "").lower().strip()
    if not text:
        return False
    return bool(
        re.search(
            r"\bcan da do\b|\bcan (he|it) do it\b|"
            r"\bdirected at da\b|\bsee if (he|da|it) can\b|"
            r"\bthese questions\b|\bda study\b|"
            r"\bthe (point of the )?study\b|"
            r"\bif (he|da) can do\b|"
            r"\bdid da (finish|write|do|prove)\b|"
            r"\bwas it you\b|\bwas that you\b|"
            r"\byou or da\b|\bda or you\b",
            text,
        )
    )


def run(out: Path | None = None) -> dict:
    payload = {
        "meta": {
            "question": "can DA do the job the questions asked",
            "writeup": "docs/DA-STUDY.md",
            "questions_are_the_exam": True,
            "emit_is_not_qed": True,
            "da_is_not_a_solver": True,
            "da_did_not_finish_just_now": True,
            "agent_phrased": True,
        },
        "asks": ASKS,
        "claims": CLAIMS,
        "answer": (
            "DA can write the chain, diagnose, and refuse glue. "
            "DA cannot finish an open WRITE by emitting it. "
            "This session: the agent phrased; DA reprinted. "
            "Neither finished leftover (6) just now."
        ),
        "counts": {
            "asks": len(ASKS),
            "can_write": sum(1 for a in ASKS if a["can_write"]),
            "can_finish": sum(1 for a in ASKS if a["can_finish"]),
            "cannot_finish": sum(1 for a in ASKS if not a["can_finish"]),
            "pass": sum(1 for c in CLAIMS if c["verdict"] == "pass"),
            "fail": sum(1 for c in CLAIMS if c["verdict"] == "fail"),
            "open": sum(1 for c in CLAIMS if c["verdict"] == "open"),
        },
        "next_da_move": (
            "Pick one open WRITE: B (6), RH (6), A uniform H1, or H_N>=-1/4. "
            "Classify it. Do not cash a written chain as the close."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_study.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def print_study(out: Path | None = None) -> dict:
    payload = run(out=out)
    print("STUDY  (questions pointed at DA)")
    print(payload["answer"])
    print()
    print("WHO")
    print("  DA = scripts + scored docs. It reprints a typed chain.")
    print("  The agent phrases the emit and wires the ask.")
    print("  Sitting theorems sat before this session.")
    print("  Open WRITE lines were not closed just now.")
    print()
    print("ASKS")
    for a in payload["asks"]:
        write = "WROTE" if a["can_write"] else "NO"
        fin = "FINISH" if a["can_finish"] else "NOT FINISHED"
        print(f"  [{write} / {fin}] {a['ask']}")
        print(f"         {a['why']}")
    print()
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return payload


def main() -> int:
    print_study()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
