#!/usr/bin/env python3
"""
Wind the Standard Model backwards and forwards.

The poster was not born in one piece. Each ancestor is a theory
with a limit that recovers it from L_SM, or a construction that
builds the next layer. Forwards = history + assembly.
Backwards = drop a piece or take a limit. Not F. Not NS.
"""

from __future__ import annotations

import json
from pathlib import Path


def rec(
    name: str,
    year: str,
    theory: str,
    back_from_sm: str,
    back_verdict: str,
    fwd_to_next: str,
    why: str,
) -> dict:
    return {
        "name": name,
        "year": year,
        "theory": theory,
        "back_from_sm": back_from_sm,
        "back_verdict": back_verdict,
        "fwd_to_next": fwd_to_next,
        "why": why,
    }


# Oldest first. back_verdict = can you recover this from L_SM by a named limit?
LINEAGE = [
    rec(
        "Maxwell",
        "1864",
        "classical U(1) field, F_μν, no ħ, no charges as spinors",
        "QED tree / ħ → 0, keep A_μ = photon after Weinberg rotation",
        "pass",
        "add charges and ħ → Dirac + Maxwell → QED",
        "The photon kinetic term in L2/L3 is Maxwell once fermions and loops are stripped.",
    ),
    rec(
        "Dirac",
        "1928",
        "relativistic spin-1/2, (iγ∂ − m)ψ = 0",
        "keep one charged fermion, turn off all non-U(1) gauge fields, replace yv by m",
        "pass",
        "couple to A_μ → QED",
        "Block 3 kinetic + block 4 mass term, one flavor, no W/Z/g.",
    ),
    rec(
        "Fermi_4fermion",
        "1933",
        "G_F (ψ̄γμψ)(ψ̄γ^μψ), no W boson",
        "E ≪ M_W: integrate out W, G_F = g² / (4√2 M_W²)",
        "pass",
        "promote contact term to SU(2) gauge boson → GWS",
        "A real low-energy limit of L2+L3. Not a UV theory.",
    ),
    rec(
        "QED",
        "1948",
        "U(1)_EM, e, electron + photon, renormalizable",
        "after SSB: e = g sin θ_W, keep A_μ, drop W, Z, gluons, Higgs fluctuations",
        "pass",
        "nonabelian copy of the same idea → Yang–Mills",
        "QED sits inside SM as the unbroken U(1)_EM. e is composed, not primitive.",
    ),
    rec(
        "Yang_Mills",
        "1954",
        "nonabelian F = dA + A∧A, cubic/quartic gluon or W self-coupling",
        "drop fermions and Higgs; keep one simple factor (SU(3) or SU(2))",
        "pass",
        "add SSB + mixing → GWS; add color + quarks → QCD",
        "Block 1 is SU(3) YM. Block 2 contains SU(2) YM before the VEV.",
    ),
    rec(
        "GWS_electroweak",
        "1967",
        "SU(2)_L × U(1)_Y + Higgs, Weinberg rotation, W/Z masses",
        "turn off g_s; drop QCD sector",
        "pass",
        "add SU(3)_c + quarks → SM (modulo generations / QCD)",
        "Blocks 2–4. θ_W and v still inputs.",
    ),
    rec(
        "QCD",
        "1973",
        "SU(3)_c, quarks, asymptotic freedom",
        "turn off g, g'; keep colored quarks + gluons",
        "pass",
        "add GWS → SM",
        "Block 1 + the color part of block 3. UV-free, IR-confining.",
    ),
    rec(
        "KM_three_gen",
        "1973",
        "third family, CKM phase, CP in the charged current",
        "keep three copies of the fermion reps and the Yukawa matrices",
        "pass",
        "already inside the poster SM",
        "Three copies are an input. Running backwards to one generation is a toy, not the SM.",
    ),
    rec(
        "SM_poster",
        "1970s–2012",
        "L_SM as assembled: QCD + GWS + 3 families + Higgs (found 2012)",
        "identity",
        "pass",
        "add S_EH + Λ → Einstein + T_SM (not a term in L_SM)",
        "The poster. Consumes the couplings. Does not produce them.",
    ),
    rec(
        "Einstein_plus_T",
        "1915 + SM",
        "G_μν + Λ g_μν = 8π G T_μν[SM]",
        "cannot. G and Λ are not in L_SM",
        "fail",
        "this is the universe couple, not a prior layer of the poster",
        "Forwards from SM you must ADD gravity. Backwards from the couple you can drop EH and recover L_SM on η.",
    ),
]


# Named limit maps that have to hold both ways (construction ↔ reduction).
LIMITS = [
    {
        "name": "SM_to_QED",
        "map": "SSB then e = g s_W, keep A_μ, drop W/Z/g/H fluc",
        "forward": "QED ⊂ SM",
        "backward": "SM ⊃ QED",
        "verdict": "pass",
    },
    {
        "name": "SM_to_Fermi",
        "map": "E ≪ M_W, integrate out W",
        "forward": "Fermi is the IR of GWS",
        "backward": "GWS UV-completes Fermi",
        "verdict": "pass",
    },
    {
        "name": "SM_to_Maxwell",
        "map": "QED then ħ → 0 / classical field",
        "forward": "Maxwell ⊂ QED ⊂ SM",
        "backward": "SM ⊃ Maxwell",
        "verdict": "pass",
    },
    {
        "name": "SM_to_YM",
        "map": "drop matter and VEV, keep one factor",
        "forward": "YM ⊂ SM",
        "backward": "SM ⊃ YM",
        "verdict": "pass",
    },
    {
        "name": "SM_to_one_group",
        "map": "run couplings backward (UV) until they meet",
        "forward": "would be a GUT",
        "backward": "SM running misses (gauge3 fail)",
        "verdict": "fail",
    },
    {
        "name": "SM_to_Einstein",
        "map": "derive G, Λ from L_SM",
        "forward": "must add S_EH by hand",
        "backward": "L_SM has no metric dynamics",
        "verdict": "fail",
    },
    {
        "name": "SM_to_NS",
        "map": "gluon cubic or continuum limit → Navier–Stokes",
        "forward": "glue",
        "backward": "glue",
        "verdict": "fail",
    },
]


def run(out: Path | None = None) -> dict:
    back_ok = [r for r in LINEAGE if r["back_verdict"] == "pass"]
    back_fail = [r for r in LINEAGE if r["back_verdict"] == "fail"]
    lim_pass = [r for r in LIMITS if r["verdict"] == "pass"]
    lim_fail = [r for r in LIMITS if r["verdict"] == "fail"]
    payload = {
        "meta": {
            "question": "does L_SM run backwards as well as forwards?",
            "not_a_unifier": True,
            "does_not_touch_ABQ": True,
            "both_directions": True,
        },
        "forwards": LINEAGE,
        "limits": LIMITS,
        "counts": {
            "ancestors": len(LINEAGE),
            "recoverable_from_SM": len(back_ok),
            "not_recoverable": len(back_fail),
            "limits_pass": len(lim_pass),
            "limits_fail": len(lim_fail),
        },
        "dots": (
            "Maxwell → Dirac → QED → Fermi sits beside → YM → GWS + QCD + KM → SM. "
            "Einstein+T is added, not recovered. A one-group UV is not recovered."
        ),
        "how_far": [
            "wound the poster back through Maxwell, Dirac, Fermi, QED, YM, GWS, QCD, KM",
            "four limits pass both ways: QED, Fermi, Maxwell, YM",
            "UV meet of the three couplings fails (already gauge3)",
            "Einstein+T does not sit inside L_SM; you add it",
            "NS is not on this line",
            "running backwards recovers prior theories, not the values of the couplings",
        ],
        "next_da_move": (
            "The SM runs backwards to its ancestors by named limits. "
            "It does not run backwards to F. Fluids stay on B."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_sm_lineage.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA lineage. SM runs backwards by limits, forwards by assembly.")
    print(payload["dots"])
    print(f"{'name':<22} {'year':<10} back  theory")
    for r in payload["forwards"]:
        print(f"{r['name']:<22} {r['year']:<10} {r['back_verdict']:<5} {r['theory'][:60]}")
    print("limits:")
    for r in payload["limits"]:
        print(f"  [{r['verdict']}] {r['name']}: {r['map']}")
    print("counts", payload["counts"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
