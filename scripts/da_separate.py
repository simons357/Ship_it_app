#!/usr/bin/env python3
"""
Run each candidate alone. No bundles. No glue.

Three decks, one object at a time:
  GQ   — gravity–quantum pairs
  PUB  — published unification claims (gauge3 and nature4 not glued)
  SIX  — reconstructed 16, singleton lock-R only
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_fingers import CANDIDATE_META, SIXTEEN  # noqa: E402
from da_gq import PAIRS  # noqa: E402
from da_screen import CLAIMS  # noqa: E402
from unifier_combo import INPUTS, lock_score, r_batch, sample_matrix  # noqa: E402


def run(n: int = 200, seed: int = 1, out: Path | None = None) -> dict:
    rng = np.random.default_rng(seed)
    base = sample_matrix(n, rng)
    baseline = float(np.mean(r_batch(base)))

    gq = []
    for p in PAIRS:
        gq.append(
            {
                "deck": "GQ",
                "alone": True,
                "name": p["name"],
                "object": f"{p['left']}  ↔  {p['right']}",
                "coupling": p["coupling"],
                "verdict": p["verdict"],
                "why": p["note"],
            }
        )

    pub = []
    for c in CLAIMS:
        pub.append(
            {
                "deck": "PUB",
                "alone": True,
                "name": c["name"],
                "kind": c["kind"],
                "gauge3_alone": c["gauge3_verdict"],
                "nature4_alone": c["nature4_verdict"],
                "glued": False,
                "why": c["note"],
            }
        )

    six = []
    for i, name in enumerate(SIXTEEN, start=1):
        cat, fate, note = CANDIDATE_META[name]
        rec = {
            "deck": "SIX",
            "alone": True,
            "id": i,
            "name": name,
            "kind": cat,
            "fate": fate,
            "why": note,
        }
        if name == "R":
            rec["verdict"] = "fail"
            rec["delta_lock_R"] = None
            rec["why"] = "output; circular as a candidate. Run alone: still not a theory."
        elif name not in INPUTS:
            rec["verdict"] = "open"
            rec["delta_lock_R"] = 0.0
        else:
            delta = lock_score(base, (name,)) - baseline
            rec["delta_lock_R"] = delta
            if fate.startswith("must_hit") and delta <= 0.02:
                rec["verdict"] = "open"
                rec["why"] = (
                    f"alone: must-hit as nature, decorative on the score (Δ={delta:+.3f})"
                )
            elif delta > 0.02:
                rec["verdict"] = "open"
                rec["why"] = f"alone: moves R (Δ={delta:+.3f}); does not write F"
            else:
                rec["verdict"] = "fail"
                rec["why"] = f"alone: does not move R (Δ={delta:+.3f}); not a force"
        six.append(rec)

    payload = {
        "meta": {
            "method": "one object, one verdict, no bundle",
            "not_a_unifier": True,
            "n": n,
            "seed": seed,
            "baseline_R": baseline,
        },
        "GQ": gq,
        "PUB": pub,
        "SIX": six,
        "counts": {
            "GQ": len(gq),
            "PUB": len(pub),
            "SIX": len(six),
        },
        "how_far": [
            f"GQ {len(gq)} pairs, each alone",
            f"PUB {len(pub)} claims, gauge3 and nature4 not glued",
            f"SIX {len(six)} slots, singleton lock-R only",
            "isolation did not promote anyone to a unifier",
            "Einstein/equivalence/QFT-on-curved still pass alone",
            "vacuum→gravity still fails alone",
            "MSSM-class still open as gauge3 alone and fail as nature4 alone",
        ],
        "next_da_move": "Stay on the GQ leftovers. Do not re-bundle into a 16-slogan.",
    }
    dest = Path(out) if out is not None else Path("results/da_separate.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA separate. One object, one verdict. No bundles.")
    print("\n--- GQ (gravity + quantum), each pair alone ---")
    for r in payload["GQ"]:
        print(f"  [{r['verdict']}] {r['name']}: {r['coupling']}")
        print(f"           {r['object']}")
    print("\n--- PUB (published claims), each program alone ---")
    for r in payload["PUB"]:
        print(f"  gauge3={r['gauge3_alone']:<5} nature4={r['nature4_alone']:<5}  {r['name']}")
    print("\n--- SIX (reconstructed 16), each slot alone ---")
    for r in payload["SIX"]:
        d = "" if r.get("delta_lock_R") is None else f" Δ={r['delta_lock_R']:+.3f}"
        print(f"  {r['id']:2d} [{r['verdict']}] {r['name']:<16} {r['fate']:<22}{d}")
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
