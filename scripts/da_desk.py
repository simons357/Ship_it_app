#!/usr/bin/env python3
"""
The desk write-up, as a scored roster.

The operator's lead, in palatable form: DA draws from a
published corpus (the papers, not the person), sits it next
to two or three others, and any new sentence names a slot
and a killer. That is a corpus method. It is not a vote
and it does not write F.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_ground import ABLATE, GROUND, MINDS, RECONSTRUCT  # noqa: E402
from da_harmonic import VOCAB  # noqa: E402
from da_pipe import FORMS, NOW, PIPES  # noqa: E402
from da_team import TEAM  # noqa: E402


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


CORPUS_RULES = [
    rec(
        "K1",
        "draw_from_papers",
        "DA may draw from published work, including people who are gone",
        "pass",
        "The unit is the paper trail. Alive or not does not matter.",
    ),
    rec(
        "K2",
        "pair_two_or_three",
        "Sit one corpus next to two or three others and emit one sentence",
        "pass",
        "That is the lead. The sentence still has to be scored.",
    ),
    rec(
        "K3",
        "slot_and_killer",
        "The sentence names one slot and a check that could kill it",
        "pass",
        "Otherwise it is not a proposal.",
    ),
    rec(
        "K4",
        "pairing_writes_F",
        "The pairing writes a theory of everything / F",
        "fail",
        "A corpus method is not a producing-map.",
    ),
    rec(
        "K5",
        "pairing_closes_B",
        "The pairing closes classical regularity",
        "fail",
        "Leray + BKM + CKN are constraints. Domain B stays open.",
    ),
    rec(
        "K6",
        "pairing_unshelves",
        "The pairing unshelves SFE or retunes nodes.json",
        "fail",
        "Motive may come back. The close may not.",
    ),
    rec(
        "K7",
        "vote_replaces_check",
        "A vote of names replaces a check",
        "fail",
        "A program review types demands. It does not collapse the wave.",
    ),
]


PAIRS = [
    rec(
        "Y1",
        "einstein_weinberg_pdg",
        "Einstein + Weinberg + PDG → Einstein+T_SM",
        "open",
        "The couple already passes. The numbers stay inputs.",
        primary="Einstein (GR)",
        companions=["Weinberg", "PDG"],
        may_emit="two-sided couple",
        couple="pass",
        numbers="fail",
    ),
    rec(
        "Y2",
        "weyl_wigner_vN",
        "Weyl + Wigner + von Neumann → (X, D, σ, Rep)",
        "pass",
        "Ground language. Not the couplings.",
        primary="Weyl",
        companions=["Wigner", "von Neumann"],
        may_emit="vocabulary of the destination",
    ),
    rec(
        "Y3",
        "leray_bkm_ckn",
        "Leray + BKM + CKN → constraints on B",
        "open",
        "Energy, continuation, partial regularity. Not a regularity pass.",
        primary="Leray",
        companions=["Beale–Kato–Majda", "Caffarelli–Kohn–Nirenberg"],
        may_emit="constraints",
    ),
    rec(
        "Y4",
        "lvk_eht_ipta",
        "LVK + EHT + IPTA → black holes are seen",
        "pass",
        "Observation on U. Not 1/r^4 and not primes.",
        primary="LVK",
        companions=["EHT", "IPTA"],
        may_emit="strain and images exist",
    ),
    rec(
        "Y5",
        "lmfdb_nt_bridge",
        "LMFDB + math.NT + Bridge* → arithmetic only",
        "pass",
        "Stays on Q. No map onto (u·∇)u.",
        primary="LMFDB",
        companions=["math.NT", "Bridge*"],
        may_emit="Q hygiene",
    ),
    rec(
        "Y6",
        "hb_sfe_cosmo",
        "HB + SFE + Cosmo Superagent → F",
        "fail",
        "The refused pairing. Motive is not a producing-map.",
        primary="HB",
        companions=["SFE", "Cosmo Superagent"],
        may_emit="nothing legal on the desk",
    ),
    rec(
        "Y7",
        "primes_qnm_ns",
        "primes + QNMs + NS → one theorem",
        "fail",
        "Three slots. The word spectrum is not glue.",
        primary="LMFDB",
        companions=["EHT / LVK", "Track B"],
        may_emit="nothing glued",
    ),
]


def run(out: Path | None = None) -> dict:
    payload = {
        "meta": {
            "question": "write the whole desk down; type the corpus method",
            "writeup": "docs/DA-DESK.md",
            "dated": "2026-09-03",
            "corpus_means": "published papers, not the person",
            "not_a_unifier": True,
            "vote_cannot_close": True,
            "program_review": True,
            "does_not_retune_nodes": True,
            "anti_bullshit_device": True,
        },
        "slots": {
            "A": "Q1-augmented NS, eps>0; Theorem A for this PDE; not B",
            "B": "classical NS, keep 1/r^4; regularity open",
            "Q": "inverse-GCD only; full floor false",
            "U": "process / SM / score; not a unifier",
        },
        "purpose": {
            "statement": "DA is an anti-bullshit device",
            "as_process": "pass",
            "as_unifier": "fail",
            "kills": [
                "slogan with no killer",
                "fake pass",
                "unfalsifiable might be true",
                "glue across slots",
                "a vote or review that writes F",
            ],
            "allows": ["open", "fail", "a lead that becomes one scored sentence"],
        },
        "corpus_rules": CORPUS_RULES,
        "pairs": PAIRS,
        "dream_team": TEAM,
        "program_review": MINDS,
        "now_bench": NOW,
        "pipes": [{"name": p["name"], "slot": p["slot"], "asof": p.get("asof")} for p in PIPES],
        "forms": [f["name"] for f in FORMS],
        "ground": [g["name"] for g in GROUND],
        "reconstruct_pass": [r["name"] for r in RECONSTRUCT if r["verdict"] == "pass"],
        "reconstruct_fail": [r["name"] for r in RECONSTRUCT if r["verdict"] == "fail"],
        "ablate": [a["name"] for a in ABLATE],
        "vocab_n": len(VOCAB),
        "counts": {
            "dream_team": len(TEAM),
            "program_review": len(MINDS),
            "now_bench": len(NOW),
            "pipes": len(PIPES),
            "corpus_rules_pass": sum(1 for r in CORPUS_RULES if r["verdict"] == "pass"),
            "corpus_rules_fail": sum(1 for r in CORPUS_RULES if r["verdict"] == "fail"),
            "pairs_pass": sum(1 for r in PAIRS if r["verdict"] == "pass"),
            "pairs_fail": sum(1 for r in PAIRS if r["verdict"] == "fail"),
            "pairs_open": sum(1 for r in PAIRS if r["verdict"] == "open"),
        },
        "next_da_move": (
            "Use the write-up. Next B write is occupation time. B4c on packets, energy-class T on spread. "
            "Corpus pairings emit scored sentences, not F."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_desk.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA desk. Write-up: docs/DA-DESK.md")
    print("Name list: docs/DA-THINK-TANK.md")
    print("Working session: docs/DA-SESSION.md")
    print("DA is an anti-bullshit device. Process pass. Unifier fail.")
    print("Corpus = published papers. Pair 2–3. Score the sentence.")
    print("dream team:")
    for m in payload["dream_team"]:
        print(f"  [{m['slot']}] {m['name']}")
    print("program review:")
    for m in payload["program_review"]:
        print(f"  {m['name']}: {m['improve_program']}")
    print("now-bench:")
    for m in payload["now_bench"]:
        print(f"  [{m['slot']}] {m['name']}")
    print("corpus rules:")
    for r in payload["corpus_rules"]:
        print(f"  [{r['verdict']}] {r['id']}: {r['statement']}")
    print("pairs:")
    for r in payload["pairs"]:
        print(f"  [{r['verdict']}] {r['name']}: {r['statement']}")
    print("counts", payload["counts"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
