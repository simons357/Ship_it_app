#!/usr/bin/env python3
"""
Break L_SM all the way down, then put it back together.

Five poster blocks are not fundamental. The atoms are spacetime,
a gauge group, representations, dim-4 operators, and input numbers.
Reassembly: those atoms (minus ghosts) are the SM. Attach Einstein
to get the two-sided couple. Still not F. A/B/Q untouched.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_sm import realized_equation  # noqa: E402


def node(name: str, piece: str, verdict: str, why: str, fingers: list | None = None) -> dict:
    rec = {"name": name, "piece": piece, "verdict": verdict, "why": why}
    if fingers:
        rec["fingers"] = fingers
    return rec


def principles() -> dict:
    return node(
        "principles",
        "what you must assume before writing a term",
        "open",
        "These are choices, not outputs of F.",
        [
            node("spacetime", "Minkowski η_μν, then g_μν if coupled to gravity", "pass", "needed to write ∂_μ and spinors"),
            node("gauge_principle", "replace ∂ by D = ∂ − igA on a principal bundle", "pass", "one idea, three groups"),
            node("representations", "fermions and Higgs sit in fixed G-reps", "pass", "the quantum numbers are inputs"),
            node("dim4", "operators of mass dimension ≤ 4 (renormalizable)", "pass", "this is why the SM is a finite list, not an infinite one"),
            node("three_copies", "repeat the fermion reps three times", "open", "copied in. Not derived from the group."),
        ],
    )


def groups() -> dict:
    return node(
        "gauge_group",
        "G = SU(3)_c × SU(2)_L × U(1)_Y",
        "pass",
        "Three factors. Not one group. That is why gauge3 can miss.",
        [
            node("SU3", "8 gluons, f^{abc}, g_s", "pass", "working Yang–Mills. g_s in."),
            node("SU2", "3 W's, ε^{abc}, g", "pass", "left-handed weak. g in."),
            node("U1", "1 hypercharge B_μ, g'", "pass", "g' in. Photon appears only after mixing."),
        ],
    )


def fields() -> dict:
    return node(
        "fields",
        "what the Lagrangian is a function of",
        "pass",
        "Connections + Higgs + fermions + ghosts.",
        [
            node("gluons", "A_μ^a, a=1..8", "pass", "block 1"),
            node("weak_bosons", "W_μ^i, i=1,2,3", "pass", "block 2 before rotation"),
            node("hypercharge", "B_μ", "pass", "mixes with W³"),
            node("higgs_doublet", "H = (φ⁺, (v+H+iφ⁰)/√2)", "pass", "4 real scalars; 3 eaten"),
            node("quarks", "Q_L, u_R, d_R × 3 gen × 3 color", "pass", "reps, not masses"),
            node("leptons", "L_L, e_R × 3 gen (ν_R absent on the poster)", "open", "minimal SM; data want neutrino mass"),
            node("ghosts", "Faddeev–Popov X, Y, …", "pass", "bookkeeping. Drop from the classical EOM."),
        ],
    )


def operators() -> dict:
    return node(
        "operators",
        "the actual terms, one kind each",
        "pass",
        "Most general dim-4 operators with those quantum numbers.",
        [
            node("F2", "−1/4 F_{μν} F^{μν} for each factor", "pass", "kinetic + YM self-interaction"),
            node("DH2", "|D_μ H|²", "pass", "Higgs kinetic; after VEV, W/Z masses"),
            node("VH", "μ²|H|² + λ|H|⁴", "pass", "potential. v and m_H from μ, λ — still inputs"),
            node("psiDpsi", "ψ̄ i D̸ ψ", "pass", "fermion kinetic + gauge vertices"),
            node("yukawa", "y ψ̄ H ψ + h.c.", "pass", "masses after VEV. y in, m out of yv, not out of topology"),
            node("theta_term", "θ F F̃", "open", "usually omitted; strong-CP leftover"),
            node("ghost_op", "ghost kinetic + mixing", "pass", "not a force"),
        ],
    )


def parameters() -> dict:
    return node(
        "parameters",
        "numbers the operators consume",
        "fail",
        "This list is the input side of F. Nothing here is produced by L_SM.",
        [
            node("g_s", "strong coupling", "fail", "consumed by F2_SU3"),
            node("g", "SU(2) coupling", "fail", "consumed by F2_SU2 and D"),
            node("g_prime", "U(1)_Y coupling", "fail", "consumed by F2_U1; θ_W = arctan(g'/g) after the fact"),
            node("v_or_mu", "Higgs scale", "fail", "input; 246 GeV is sat at"),
            node("lambda_h", "Higgs self-coupling", "fail", "input; m_H from λv²"),
            node("yukawas", "3×3 complex matrices", "fail", "independent inputs; Koide not among them"),
            node("CKM", "quark mixing after diagonalizing y_u, y_d", "fail", "derived from Yukawas, still not from topology"),
            node("theta_qcd", "strong CP angle", "open", "must-hit leftover if you mean nature"),
        ],
    )


def missing() -> dict:
    return node(
        "not_in_L_SM",
        "atoms you need for a universe model that are not on the poster",
        "fail",
        "Cannot satisfy nature4 from L_SM alone.",
        [
            node("G_N", "Newton / Planck", "fail", "not a field in L_SM"),
            node("Lambda", "cosmological constant", "fail", "not a term in L_SM"),
            node("metric", "g_μν as a dynamical field", "fail", "poster is written on η_μν"),
            node("nu_R_or_m", "neutrino masses", "open", "absent on the minimal poster"),
        ],
    )


def tree() -> dict:
    return node(
        "L_SM",
        "expanded Standard Model Lagrangian (the poster)",
        "open",
        "A sum. Five blocks were the printing. These are the parts.",
        [principles(), groups(), fields(), operators(), parameters(), missing()],
    )


def walk(n: dict, depth: int = 0) -> list[dict]:
    rows = [{"depth": depth, "name": n["name"], "verdict": n["verdict"], "piece": n["piece"]}]
    for ch in n.get("fingers") or []:
        rows.extend(walk(ch, depth + 1))
    return rows


def leaves(n: dict) -> list[dict]:
    kids = n.get("fingers") or []
    if not kids:
        return [n]
    out: list[dict] = []
    for ch in kids:
        out.extend(leaves(ch))
    return out


def reassembly() -> dict:
    """Put the atoms back. Unique SM, then the couple. Not F."""
    steps = [
        {
            "step": 1,
            "do": "Keep spacetime + gauge principle + G = SU(3)×SU(2)×U(1)",
            "get": "the covariant derivative and three field strengths",
            "verdict": "pass",
        },
        {
            "step": 2,
            "do": "Assign the observed fermion and Higgs representations",
            "get": "the allowed dim-4 operators are a finite list",
            "verdict": "pass",
        },
        {
            "step": 3,
            "do": "Write every dim-4 operator allowed by those quantum numbers",
            "get": "L_SM (up to the numerical values of the couplings)",
            "verdict": "pass",
            "why": "This is the uniqueness. The poster is that list, expanded in components.",
        },
        {
            "step": 4,
            "do": "Drop ghosts",
            "get": "same classical equations of motion",
            "verdict": "pass",
            "why": "Bookkeeping. Not a fifth force.",
        },
        {
            "step": 5,
            "do": "Insert the measured couplings / Yukawas / v",
            "get": "the working Standard Model, three forces, no gravity",
            "verdict": "pass",
            "why": "Dynamics pass. The numbers were pasted. Produce still fail.",
        },
        {
            "step": 6,
            "do": "Replace η by g and add S_EH + Λ",
            "get": "G_μν + Λ g_μν = 8π G T_μν[SM]",
            "verdict": "pass",
            "why": "The two-sided couple. Working. Not nature4.",
        },
        {
            "step": 7,
            "do": "Ask the rebuilt L to output g_s, θ_W, G, Λ",
            "get": "nothing. The numbers went in at step 5 and 6",
            "verdict": "fail",
        },
    ]
    eq = realized_equation()
    return {
        "unique_sm": (
            "The most general renormalizable Lagrangian with "
            "G = SU(3)×SU(2)×U(1), one Higgs doublet, and the SM fermion "
            "reps is L_SM, up to parameter values."
        ),
        "steps": steps,
        "put_back": eq,
        "still_not_F": True,
        "still_not_NS": True,
    }


def drop_tests() -> list[dict]:
    """What dies if you drop one atom. Isolation."""
    return [
        {"drop": "SU3", "still_SM": False, "why": "no QCD"},
        {"drop": "SU2", "still_SM": False, "why": "no weak"},
        {"drop": "U1", "still_SM": False, "why": "no hypercharge / no photon after mix"},
        {"drop": "higgs_doublet", "still_SM": False, "why": "no SSB, no W/Z masses, no Yukawa masses"},
        {"drop": "dim4", "still_SM": False, "why": "infinite operator tower; not the SM"},
        {"drop": "three_copies", "still_SM": False, "why": "one-generation toy, not the SM"},
        {"drop": "ghosts", "still_SM": True, "why": "classical SM EOM unchanged"},
        {"drop": "G_N", "still_SM": True, "why": "SM never had it; universe model loses gravity"},
    ]


def run(out: Path | None = None) -> dict:
    t = tree()
    leaf = leaves(t)
    rows = walk(t)
    rebuild = reassembly()
    drops = drop_tests()
    payload = {
        "meta": {
            "question": "break L_SM to atoms, then reassemble",
            "five_blocks_not_enough": True,
            "n_poster_blocks": 5,
            "n_leaves": len(leaf),
            "not_a_unifier": True,
            "does_not_touch_ABQ": True,
        },
        "tree": t,
        "leaves": [{"name": x["name"], "verdict": x["verdict"], "piece": x["piece"]} for x in leaf],
        "flat": rows,
        "reassembly": rebuild,
        "drop_one": drops,
        "counts": {
            "leaves": len(leaf),
            "pass": sum(1 for x in leaf if x["verdict"] == "pass"),
            "fail": sum(1 for x in leaf if x["verdict"] == "fail"),
            "open": sum(1 for x in leaf if x["verdict"] == "open"),
            "drop_still_sm": sum(1 for d in drops if d["still_SM"]),
        },
        "how_far": [
            f"five poster blocks opened into {len(leaf)} atoms",
            "principles / group / fields / operators / parameters / missing",
            "reassembly uniqueness: G + reps + dim-4 → L_SM (parameters still pasted)",
            "ghosts droppable; SU(3), SU(2), U(1), Higgs, dim-4, 3 families not",
            "put back with gravity: Einstein + T_SM (working couple)",
            "step 7 fail: rebuilt L still does not produce the couplings",
            "A/B/Q untouched",
        ],
        "next_da_move": (
            "Stop breaking L_SM. The atoms are on the table. "
            "A producing-map has to live outside this list. Fluids stay on B."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_sm_break.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def _print(n: dict, indent: int = 0) -> None:
    pad = "  " * indent
    print(f"{pad}[{n['verdict']}] {n['name']}: {n['piece']}")
    for ch in n.get("fingers") or []:
        _print(ch, indent + 1)


def main() -> int:
    payload = run()
    print("DA break L_SM, then put it back. Five blocks were not enough.")
    print(f"leaves={payload['meta']['n_leaves']}  counts={payload['counts']}")
    _print(payload["tree"])
    print("\nreassembly:")
    for s in payload["reassembly"]["steps"]:
        print(f"  {s['step']}. [{s['verdict']}] {s['do']} → {s['get']}")
    print("put back:", payload["reassembly"]["put_back"]["equation"])
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
