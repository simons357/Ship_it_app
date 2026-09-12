#!/usr/bin/env python3
"""B-hand five-finger map on unaugmented NS leftovers.

DA fills named blanks. The map is not a close.
Cosmo / SM fingers stay the other book.
Soft X silent. NS not solved. Lemma★ OPEN. Need★ MISSING.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from estimate_audit import classify_paragraph  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
WRITE = ROOT / "docs" / "DA-NS-FIVE-FINGER.md"

REFUSE_MARKERS = (
    "five fingers close ns",
    "five fingers close navi",
    "b-hand closes ns",
    "bhand closes ns",
    "cosmo fingers close ns",
    "cosmo five fingers as ns",
    "ns is solved",
    "ordinary ns sits",
    "lemma★ is proved",
    "need★ is proved",
    "h1 is a theorem",
    "ring sits as proved",
    "soft x closes",
    "weld the three writings",
    "a implies b",
    "a⇒b",
)


FINGERS = [
    {
        "id": 1,
        "name": "identities",
        "role": "palm",
        "class": "unaugmented 3-D NSE on R^3 or T^3",
        "quantity": "named identities (Leray, enstrophy, locked R_star, gap-cancel)",
        "remainder": "none; an identity is not a bound",
        "status": "YES as identities",
        "leftover": None,
    },
    {
        "id": 2,
        "name": "spindle",
        "role": "geometric write",
        "class": "unaugmented NS, one cylinder Q_r",
        "quantity": "A_bad on Q_r",
        "remainder": "shapes 1-3, not yet absorbed",
        "status": "YES as a write; NO as a theorem; leftover 1 OPEN",
        "leftover": 1,
    },
    {
        "id": 3,
        "name": "after the spindle",
        "role": "named geometric blanks",
        "class": "same cylinder as Finger 2",
        "quantity": "H2 energy, H3 absorb, Ring, shapes 1-3",
        "remainder": "those blanks themselves",
        "status": "OPEN / REPAIR",
        "leftover": "2, 3, and leftover 1 shapes",
    },
    {
        "id": 4,
        "name": "Need★",
        "role": "energy-budget dual",
        "class": "unaugmented NS on T^3, two-shell / HH→L",
        "quantity": "signed dual S_star = T_beta^{HH→L}",
        "remainder": "unsigned CS hiding occupancy s",
        "status": "Need★ MISSING as a bound; leftover 4 OPEN",
        "leftover": 4,
    },
    {
        "id": 5,
        "name": "restricted class",
        "role": "axisymmetric shell",
        "class": "axisymmetric with swirl, unaugmented, R^3",
        "quantity": "Z_j = ||Δ_j ω||_2^2",
        "remainder": "T_{j←j}",
        "status": "OPEN; occupancy 55/56 printed, not [ρ]",
        "leftover": 5,
    },
]


AFTER_SPINDLE = [
    {"name": "H2", "what": "energy on the same cylinder", "status": "OPEN"},
    {"name": "H3", "what": "absorb the bad term as r→0", "status": "OPEN"},
    {
        "name": "Ring Lemma",
        "what": "||∇ξ||_{L^∞(E_c)} ≤ C 2^{j*}",
        "status": "REPAIR",
    },
    {"name": "Shape 1", "what": "high-high → low on the cylinder", "status": "OPEN"},
    {"name": "Shape 2", "what": "high-low → high", "status": "OPEN"},
    {"name": "Shape 3", "what": "low-low → high", "status": "OPEN"},
]


STATES = {
    "fire": {
        "meaning": "what is live now",
        "is": [
            "Need★ signed dual MISSING (primary)",
            "grow s on 9B secondary; finite max K≈0.456, max s=192; not a kill",
            "H1 write sits; theorem no",
            "axisymmetric occupancy printed; [ρ] not written",
            "Catalog B open 1",
        ],
        "is_not": ["Cosmo fingers", "Theorem A as B", "Soft X"],
    },
    "realized": {
        "meaning": "unaugmented NS as it sits",
        "is": [
            "B: no Q1, no Φ-cancel, no K(t) in the PDE, no Q-stack",
            "ordinary NS OPEN",
            "A is not B",
            "RH OPEN; Q is inverse-GCD only; U is DA process",
            "three writings aimed leftovers, not theorems",
        ],
        "is_not": ["a close", "augmented NSE"],
    },
    "future": {
        "meaning": "what would have to sit; DA cannot invent this",
        "is": [
            "Need★ bound, or R_star(v_n)→∞",
            "or an H1 shape, or G(v_n)→∞ (Ring would have to leave REPAIR if used)",
            "or a class bound on ∫ρ_j, or a killing field in the class",
            "then Path 1 (7)–(9) can be written",
        ],
        "is_not": ["A", "Cosmo", "Soft X", "a weld of the three writings"],
    },
}


FILLED = [
    "five B-hand fingers named",
    "after the spindle named (H2, H3, Ring REPAIR, shapes 1-3)",
    "fire / realized / future named",
    "three writings kept unglued",
    "Cosmo hand kept out of this book as constitutive NS",
]

UNFILLED = [
    "Need★ signed dual bound",
    "sup R_star < ∞ or R_star → ∞",
    "H1 as a theorem / a shape / G → ∞",
    "H2 a priori from energy",
    "H3 absorb as r → 0",
    "Ring leaving REPAIR",
    "∫ρ_j class bound or a killing field",
    "Path 1 (6)",
]


def classify_bhand_claim(text: str) -> dict:
    low = text.lower()
    hits = [m for m in REFUSE_MARKERS if m in low]
    audit = classify_paragraph(text)
    return {
        "refuse_hits": hits,
        "accepted_as_close": False,
        "allowed_as_map": len(hits) == 0 and audit["allowed_in_estimate"],
        "discard_hits": audit["discard_hits"],
        "verdict": "MAP",
        "lemma_star": "OPEN",
        "need_star": "MISSING",
    }


def run() -> dict:
    audit = classify_paragraph(WRITE.read_text() if WRITE.exists() else "")
    return {
        "hand": "B-hand",
        "other_book": "Cosmo / SM five fingers (docs/DA-FINGERS.md)",
        "cosmo_fingers_as_ns": "NO",
        "verdict": "MAP",
        "accepted_as_close": False,
        "ns_solved": False,
        "lemma_star": "OPEN",
        "need_star": "SIGNED_DUAL_MISSING",
        "h1_theorem": False,
        "soft_x": "silent",
        "three_writings_welded": False,
        "k_in_pde": False,
        "fingers": FINGERS,
        "after_the_spindle": AFTER_SPINDLE,
        "states": STATES,
        "da_filled": FILLED,
        "da_cannot_fill": UNFILLED,
        "catalog_b_open": 1,
        "issues_rows_moved": [],
        "write": str(WRITE.relative_to(ROOT)),
        "allowed_in_estimate": audit["allowed_in_estimate"],
        "discard_hits": audit["discard_hits"],
    }


def main() -> int:
    p = argparse.ArgumentParser(description="B-hand five-finger map. Not a close.")
    p.add_argument("--json", action="store_true", help="print the map as JSON")
    p.add_argument("--claim", default="", help="score a sentence against the refuse list")
    args = p.parse_args()
    if args.claim:
        print(json.dumps(classify_bhand_claim(args.claim), indent=2))
        return 0
    payload = run()
    if args.json:
        print(json.dumps(payload, indent=2))
        return 0
    print("B-hand five-finger map. Verdict: MAP. Not a close.")
    print("Cosmo / SM fingers stay the other book.")
    for f in payload["fingers"]:
        print(f"  Finger {f['id']} {f['name']}: {f['status']}")
    print("After the spindle:")
    for blank in payload["after_the_spindle"]:
        print(f"  {blank['name']}: {blank['status']} — {blank['what']}")
    print("Fire:", "; ".join(payload["states"]["fire"]["is"]))
    print("Realized: unaugmented NS OPEN. A is not B.")
    print("Future: one leftover moved, or a kill. Not a weld.")
    print("DA filled:", "; ".join(payload["da_filled"]))
    print("DA cannot fill:", "; ".join(payload["da_cannot_fill"]))
    print("accepted_as_close:", payload["accepted_as_close"])
    print("NS solved:", payload["ns_solved"])
    print("Soft X:", payload["soft_x"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
