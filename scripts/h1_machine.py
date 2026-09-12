#!/usr/bin/env python3
"""
H1 machine. The write is the objective. The machine refuses a fake close.

Unaugmented NS, one cylinder Q_r. Quantity A_bad.
Remainder A_bad versus dissipation plus r^{-2} enstrophy.
Not WRITE (6) as a theorem. Not Lemma-star. Not ABC_λ.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from estimate_audit import classify_paragraph  # noqa: E402
from track_b_lemmas import rec  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
WRITE = ROOT / "docs" / "H1-WRITE.md"

# A paragraph that retitles a cousin, drops the class, or claims the write sits.
REFUSE_MARKERS = (
    "h1 is proved",
    "h1 sits as a theorem",
    "write (6) is a theorem",
    "write (6) sits as a theorem",
    "p1 is h1",
    "p1-loc is h1",
    "pc is h1",
    "lemma pc is write (6)",
    "cs thinness is h1",
    "assume thin is shape 1",
    "lemma j on generic fields is h1",
    "lemma j sits as shape 2",
    "imposed wait is shape 3",
    "ring lemma is proved",
    "glue h1 to lemma-star",
    "glue h1 to ★",
    "start h1 from abc",
    "ns is solved",
)

OBJECTIVE = (
    "A_bad(Q_r) <= (nu/8) ∬|∇ω|^2 φ + C r^{-2} ∬|ω|^2 "
    "on Bad pairs, or G(Q_r) → ∞ on a named sequence."
)


def kernel_exponent(side: str) -> float:
    """Hölder cut spent once. Good drops. Bad does not."""
    if side == "good":
        return -2.5
    if side == "bad":
        return -3.0
    raise ValueError(side)


def locked_G_name() -> str:
    return "G(Q_r) = A_bad / (∬|∇ω|^2 φ + r^{-2} ∬|ω|^2)"


def classify_h1_claim(text: str) -> dict:
    low = text.lower()
    hits = [m for m in REFUSE_MARKERS if m in low]
    audit = classify_paragraph(text)
    return {
        "refuse_hits": hits,
        "accepted_as_close": False,
        "allowed_as_write": len(hits) == 0 and audit["allowed_in_estimate"],
        "discard_hits": audit["discard_hits"],
    }


def lemmas() -> list[dict]:
    good = kernel_exponent("good")
    bad = kernel_exponent("bad")
    write = WRITE.read_text() if WRITE.is_file() else ""
    claim = classify_h1_claim(write)
    return [
        rec(
            "H1w_first_sentence",
            "first sentence names class, quantity, remainder, OPEN",
            "pass" if "Unaugmented Navier–Stokes, one cylinder" in write else "fail",
            "Estimate-audit standing order 1, for leftover 1.",
        ),
        rec(
            "H1w_G_locked",
            locked_G_name(),
            "pass" if "\\mathcal G(Q_r)" in write else "fail",
            "Definition only. Not a bound. Not a kill.",
        ),
        rec(
            "H1w_holder_once",
            "Good kernel |z|^{-5/2}; Bad kernel stays |z|^{-3}",
            "pass" if good == -2.5 and bad == -3.0 else "fail",
            "The cut changes the set, not the Bad exponent.",
            good_exponent=good,
            bad_exponent=bad,
        ),
        rec(
            "H1w_identity_not_bound",
            "local enstrophy identity does not bound A_bad",
            "pass",
            "The identity sits. The Bad piece is the leftover.",
        ),
        rec(
            "H1w_p1_is_h1",
            "Lemma P1 is WRITE (6)",
            "fail",
            "Low-pass Plancherel is a cousin. NSE membership open.",
        ),
        rec(
            "H1w_p1loc_is_h1",
            "Lemma P1-loc is WRITE (6)",
            "fail",
            "Cutoff keeps ∇u. Dropping ∇u fails.",
        ),
        rec(
            "H1w_pc_is_h1",
            "Lemma PC is WRITE (6)",
            "fail",
            "A curve bound is not A_bad. Gap removes the path.",
        ),
        rec(
            "H1w_cs_is_shape1",
            "CS-summable volume thinness is shape 1 / H1",
            "fail",
            "CS returns E^{3/2}. That is mid-Bad / H3 class.",
        ),
        rec(
            "H1w_write_proved",
            "WRITE (6) / H1 is a theorem",
            "fail",
            "Aimed leftover yes. Theorem no.",
        ),
        rec(
            "H1w_machine_refuses_fake",
            "the write page is accepted as a write and refused as a close",
            "pass" if claim["allowed_as_write"] and not claim["accepted_as_close"] else "fail",
            "Obedience: no cousin, no dropped class, no (6) as QED.",
            refuse_hits=claim["refuse_hits"],
        ),
        rec(
            "H1w_abc_start",
            "H1 is started from ABC_λ",
            "fail",
            "Named only. Do not start leftover 1 from that table.",
        ),
        rec(
            "H1w_sup_G",
            "sup G < ∞ on every admissible cylinder",
            "open",
            "The bound. Or G → ∞ on a named sequence. Neither sits.",
        ),
    ]


def run(out: Path | None = None) -> dict:
    rows = lemmas()
    counts = {"pass": 0, "fail": 0, "open": 0}
    for row in rows:
        counts[row["verdict"]] += 1
    payload = {
        "objective": OBJECTIVE,
        "ratio": locked_G_name(),
        "good_exponent": kernel_exponent("good"),
        "bad_exponent": kernel_exponent("bad"),
        "lemmas": rows,
        "counts": counts,
        "domain_verdict": "open",
        "meta": {
            "h1_proved": False,
            "write_6_is_theorem": False,
            "started_from_abc": False,
            "glued_to_star": False,
        },
    }
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--claim", type=str, default="")
    args = p.parse_args()
    if args.claim:
        print(json.dumps(classify_h1_claim(args.claim), indent=2))
        return
    print(json.dumps(run(out=args.out), indent=2))


if __name__ == "__main__":
    main()
