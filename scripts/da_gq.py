#!/usr/bin/env python3
"""
Start at gravity + quantum. What is actually coupled?

Each pair is scored separately. Not a unifier. Not Quantum Lens.
Does not glue to Track A/B or to gauge3.
"""

from __future__ import annotations

import json
from pathlib import Path


def pair(
    name: str,
    left: str,
    right: str,
    coupling: str,
    status: str,
    verdict: str,
    note: str,
) -> dict:
    return {
        "name": name,
        "left": left,
        "right": right,
        "coupling": coupling,
        "status": status,
        "verdict": verdict,
        "note": note,
    }


PAIRS = [
    pair(
        "Einstein",
        "G_μν (curvature)",
        "T_μν (stress-energy)",
        "8π G",
        "working classical + QFT source",
        "pass",
        "Universal. Everything with energy sources curvature the same way. One constant, G.",
    ),
    pair(
        "equivalence",
        "g_μν (metric)",
        "every matter worldline / kinetic term",
        "minimal coupling (√−g, g^μν)",
        "working; tested",
        "pass",
        "The same metric enters every species. That is why gravity is not a fourth SM gauge click.",
    ),
    pair(
        "Lambda",
        "Λ g_μν",
        "g_μν",
        "Λ (or ρ_Λ = Λ/8πG)",
        "working as a term; origin open",
        "open",
        "Observed. Sits on the left of Einstein. Not derived from the SM vacuum.",
    ),
    pair(
        "QFT_on_curved",
        "quantum fields ψ, A",
        "classical g_μν",
        "D_μ[g], √−g",
        "working semiclassical",
        "pass",
        "Hawking, inflation perturbations, etc. Fields are quantum. Geometry is not.",
    ),
    pair(
        "vacuum_to_gravity",
        "⟨0|T_μν|0⟩ ~ k_UV⁴",
        "G_μν via 8πG",
        "same G",
        "the leftover",
        "fail",
        "This coupling is why ρ_Λ is a problem. Naive QFT vacuum overshoots the observed Λ by a huge factor. Not a pass.",
    ),
    pair(
        "hierarchy",
        "M_Pl = 1/√G",
        "v (electroweak)",
        "G v² ~ 10⁻³²",
        "the other leftover",
        "open",
        "Gravity is weak at v because M_Pl is huge. A fact. Not a derivation.",
    ),
    pair(
        "graviton_to_SM",
        "quantized h_μν",
        "SM fields",
        "κ = √(8πG)",
        "not established as a complete theory",
        "open",
        "Effective EFT exists (soft gravitons). A finite UV theory that outputs G and Λ is not on the desk.",
    ),
    pair(
        "gauge3_to_G",
        "α_em, α_s, α_w",
        "G_N",
        "no working F",
        "not coupled in any screened program",
        "fail",
        "The screen: MSSM-class can meet the three gauges. None of them output G from that same map.",
    ),
]


def run(out: Path | None = None) -> dict:
    working = [p["name"] for p in PAIRS if p["verdict"] == "pass"]
    leftovers = ["vacuum_to_gravity", "hierarchy"]
    payload = {
        "meta": {
            "start": "gravity + quantum",
            "question": "what is coupled?",
            "not_a_unifier": True,
            "not_quantum_lens": True,
            "do_not_glue_to_gauge3": True,
        },
        "what_is_coupled": (
            "One universal pair: metric ↔ stress-energy, strength G. "
            "Quantum fields couple to a classical metric. "
            "Their vacuum couples through the same G and overshoots Λ. "
            "That is the start. The three SM gauges are a different coupling."
        ),
        "pairs": PAIRS,
        "working": working,
        "leftovers": leftovers,
        "why_the_score_cared": (
            "lock-R, Born, and Shapley all put mass on log(ρ_Λ^{1/4}/v) and "
            "log(M_Pl/v) because those are the two leftovers of this one coupling."
        ),
        "how_far": [
            "named the actual couple: (g_μν, T_μν) with strength G",
            "ran each pair separately",
            "working: Einstein, equivalence, QFT-on-curved",
            "leftovers: vacuum→gravity (fail as a prediction), hierarchy (open as a fact)",
            "graviton↔SM is EFT-open, not a UV F",
            "gauge3 is not coupled to G in any screened program",
            "start here; do not glue a GUT meet onto this pair",
        ],
        "next_da_move": (
            "Stay on this pair. A nature4 pass needs G and Λ as outputs of one F. "
            "That F is not on the desk."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_gq.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA gravity + quantum. What is coupled? Each pair separate.")
    print(payload["what_is_coupled"])
    print(f"{'pair':<22} {'verdict':<6} coupling")
    for p in payload["pairs"]:
        print(f"{p['name']:<22} {p['verdict']:<6} {p['coupling']}")
    print("working:", payload["working"])
    print("leftovers:", payload["leftovers"])
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
