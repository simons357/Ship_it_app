#!/usr/bin/env python3
"""
How a program can say: unification is possible, there are X candidates,
and each is gauge / harmonic / topological / … — without having F.

Official Cosmo 16 names are in scripts/da_cosmo.py. The core equation
is still private. This file lists the only legal reasons a program can
say “possible” and emit a finite X, plus a reconstructed enumerator.
"""

from __future__ import annotations

import json
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_fingers import CANDIDATE_META, SIXTEEN, TOE_CATEGORIES  # noqa: E402


LINE = "how did a typed catalog plus a count become 'possible' and 'X candidates'?"
K_FORCES = 4
K_NATURE = 6

# The hand is not capped at five. Cosmos 3-D typed "other dimensional
# objects" too. These extra types are open slots, not a claim that the
# app used these names.
OPEN_TYPES = TOE_CATEGORIES + (
    "p_form",
    "moduli",
    "characteristic_class",
    "spinor",
    "other_dimensional",
)


def legal_reasons_possible() -> list[dict]:
    return [
        {
            "id": "P1",
            "reason": "dimension count",
            "statement": "n knobs > k targets ⇒ a generic continuous F hits",
            "needs_names": False,
            "needs_F": False,
            "verdict": "open",
            "why": (
                "This is the only reason a program can say 'possible' before "
                "the names exist. 16 > 4 and 15 > 6. It is a clue, not a pass."
            ),
        },
        {
            "id": "P2",
            "reason": "topological existence (degree / transversality)",
            "statement": "an existence proof without writing F",
            "needs_names": True,
            "needs_F": False,
            "verdict": "open",
            "why": (
                "Possible in principle once the domain and codomain are typed. "
                "No such proof is in this repo. Cosmos saying 'possible' may "
                "have meant P1, not P2."
            ),
        },
        {
            "id": "P3",
            "reason": "explicit F with χ²_ext ≤ ε²",
            "statement": "construction",
            "needs_names": True,
            "needs_F": True,
            "verdict": "fail",
            "why": "No producing-map is in the repo. Affine holdout failed.",
        },
        {
            "id": "P4",
            "reason": "slogan",
            "statement": "the app said so",
            "needs_names": False,
            "needs_F": False,
            "verdict": "fail",
            "why": "A sentence is not a check. DA does not accept this as a pass.",
        },
    ]


def legal_reasons_x() -> list[dict]:
    return [
        {
            "id": "X1",
            "reason": "count typed objects in a catalog",
            "verdict": "open",
            "why": (
                "Classifier: object → {gauge, harmonic, topological, …}. "
                "Keep those whose type is allowed in domain(F) or as a "
                "must-hit leftover. X = |survivors|. This does not need F. "
                "It needs a catalog and a type map. Cosmos 3-D already typed "
                "harmonic / gauge / topological for dimensional objects. "
                "That is enough to emit a finite X."
            ),
        },
        {
            "id": "X2",
            "reason": "dimension of a moduli / leftover space",
            "verdict": "open",
            "why": (
                "X is not a head-count of widgets but dim of the space of "
                "allowed inputs. Still a number. Still not F."
            ),
        },
        {
            "id": "X3",
            "reason": "count slots on a screen",
            "verdict": "open",
            "why": (
                "Official Topology vs Gauge table is now in the repo: X=16 named "
                "slots. That closes the missing-names block. It does not close P3."
            ),
        },
        {
            "id": "X4",
            "reason": "invented a round number",
            "verdict": "fail",
            "why": "Not a reason. DA does not use this.",
        },
    ]


def enumerate_candidates() -> dict:
    """Reconstructed enumerator: type each of the 16, keep unifier-eligible ones."""
    allowed_in_domain = {
        "gauge",
        "gravity_gauge",
        "topological",
        "harmonic",
        "teleological",
    }
    must_hit = {"gauge", "gravity_gauge"}
    rows = []
    for name in SIXTEEN:
        cat, fate, note = CANDIDATE_META[name]
        eligible = cat in allowed_in_domain and fate != "output"
        rows.append(
            {
                "name": name,
                "type": cat,
                "fate": fate,
                "eligible_as_candidate": eligible,
                "must_hit_nature": cat in must_hit and fate.startswith("must_hit"),
                "note": note,
            }
        )
    eligible = [r for r in rows if r["eligible_as_candidate"]]
    must = [r for r in rows if r["must_hit_nature"]]
    x = len(eligible)
    return {
        "catalog_source": "reconstructed 16; official Cosmo 16 is a different catalog",
        "open_types_not_capped_at_five": list(OPEN_TYPES),
        "rows": rows,
        "X_eligible": x,
        "X_must_hit_nature": len(must),
        "k_forces": K_FORCES,
        "k_nature": K_NATURE,
        "possible_by_count": x > K_NATURE,
        "able_means": (
            "type-correct and enough of them (X > k). "
            "Not 'F hits the data'. The app can know they are candidates "
            "without knowing they succeed."
        ),
        "how_it_could_know": [
            "Type every dimensional object it already knew (harmonic / gauge / topological / …).",
            "Keep those whose type is allowed as an input or as a leftover F must hit.",
            "X = that count (or the dimension of their span).",
            "Say 'possible' because X > k (P1), not because F was built (P3).",
        ],
    }


def type_filters() -> list[dict]:
    """What happens to X if a type is dropped. The hand can lose a finger."""
    enum = enumerate_candidates()
    out = []
    for dropped in TOE_CATEGORIES:
        kept = [r for r in enum["rows"] if r["eligible_as_candidate"] and r["type"] != dropped]
        out.append(
            {
                "drop_type": dropped,
                "X": len(kept),
                "still_possible": len(kept) > K_NATURE,
                "names": [r["name"] for r in kept],
            }
        )
    return out


def run(out: Path | None = None) -> dict:
    enum = enumerate_candidates()
    payload = {
        "meta": {
            "question": LINE,
            "cosmos_internals_found": False,
            "cosmos_app_list_found": True,
            "not_a_unifier": True,
            "hand_not_capped_at_five": True,
        },
        "possible": legal_reasons_possible(),
        "how_X": legal_reasons_x(),
        "enumerator": enum,
        "drop_one_type": type_filters(),
        "how_far": [
            "Cosmo 16 names are in; core equation is still not in the repo",
            "P1 (n > k) is the only 'possible' that works before names exist",
            "X comes from a type-classifier on a catalog, not from F",
            f"on this reconstructed 16: X_eligible={enum['X_eligible']}, possible_by_count={enum['possible_by_count']}",
            "dropping any one type still leaves X > 6, so 'possible' is robust to a missing finger",
            "candidate ≠ success; 'able' here means type-correct and numerous enough",
            "official Cosmo 16/16 is not P3; produce still fails on that catalog",
        ],
        "next_da_move": (
            "P3 still needs a public F. Official Cosmo names do not write that map. "
            "Do not treat the count or the UI 16/16 as F."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_how.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA how-it-knew. Cosmo names in; core equation still private.")
    print("Possible: only P1 (n > k) works before names. P3 (explicit F) fails here.")
    enum = payload["enumerator"]
    print(f"X_eligible={enum['X_eligible']}  X_must_hit={enum['X_must_hit_nature']}  "
          f"k_nature={enum['k_nature']}  possible_by_count={enum['possible_by_count']}")
    print("able means:", enum["able_means"])
    print("how it could know:")
    for step in enum["how_it_could_know"]:
        print(" -", step)
    print("drop one type:")
    for row in payload["drop_one_type"]:
        print(f"  drop {row['drop_type']:<16} X={row['X']} possible={row['still_possible']}")
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
