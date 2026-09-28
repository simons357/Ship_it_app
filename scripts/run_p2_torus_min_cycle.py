#!/usr/bin/env python3
"""Emit the MIN-CYCLE / P2 torus certificate. Not a close."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_attacks.min_cycle import CANONICAL_TREE, PARALLELOGRAM_M, min_cycle_acceptance
from ns_attacks.torus_p2 import snf_certificate


def main() -> None:
    acc = min_cycle_acceptance()
    payload = {
        "gate": "P2 / MIN-CYCLE",
        "torus_lemma": "standard/proved",
        "finite_p2_compatibility": "exact integer algebra",
        "one_cycle_loss_law": "complete (exact branch-enumerated + quadratic + quartic)",
        "min_cycle": "canonical-input gated",
        "scale_rate_defect": "OPEN",
        "acceptance": acc,
        "snf_tree": snf_certificate(CANONICAL_TREE),
        "snf_parallelogram": snf_certificate(PARALLELOGRAM_M),
        "ns_solved": False,
    }
    out = ROOT / "results" / "p2_torus_min_cycle.json"
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(
        json.dumps(
            {
                "wrote": str(out),
                "accepted": acc["accepted_on_this_gate"],
                "scale_rate": "OPEN",
            }
        )
    )


if __name__ == "__main__":
    main()
