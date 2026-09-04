#!/usr/bin/env python3
"""
Typed harmonic vocabulary from mathematics.

The English word is not one object. DA can name the distinct
objects, type them, and map each live desk use. That is a
catalog. It is not a finished field and not a unifier.
"""

from __future__ import annotations

import json
from pathlib import Path


def rec(
    hid: str,
    name: str,
    family: str,
    obj: str,
    equation: str,
    slot: str,
    on_desk: bool,
    real_math: bool,
    why: str,
) -> dict:
    return {
        "id": hid,
        "name": name,
        "family": family,
        "object": obj,
        "equation": equation,
        "slot": slot,
        "on_desk": on_desk,
        "real_math": real_math,
        "why": why,
    }


# Distinct objects that share the English word. Not one thing.
VOCAB = [
    rec(
        "H1",
        "harmonic_function",
        "kernel",
        "u with Δu = 0",
        "Δu = 0",
        "none",
        False,
        True,
        "Laplace kernel. The oldest mathematical sense of the word.",
    ),
    rec(
        "H2",
        "harmonic_polynomial",
        "kernel",
        "homogeneous polynomial in ker Δ",
        "ΔP = 0, P homogeneous",
        "none",
        False,
        True,
        "Polynomial kernel. Restricts to spherical harmonics.",
    ),
    rec(
        "H3",
        "spherical_harmonic",
        "spectral",
        "Y_ℓm on S^{n-1}; Laplace–Beltrami eigenfunction",
        "Δ_{S^{n-1}} Y = −ℓ(ℓ+n-2) Y",
        "B",
        True,
        True,
        "Angular modes. Already the language of Ring / angular decomposition on B.",
    ),
    rec(
        "H4",
        "helmholtz_leray",
        "kernel",
        "u = ∇φ + curl A, or P = I − ∇Δ^{-1}div",
        "div u = 0 after Leray",
        "A",
        True,
        True,
        "On A and on every NS write. Projector, not a universe law.",
    ),
    rec(
        "H5",
        "laplacian_eigenfunction",
        "spectral",
        "Δφ = λφ on a manifold or domain",
        "Δφ = λφ",
        "none",
        False,
        True,
        "Spectral geometry. Spherical harmonics are the S^{n-1} case.",
    ),
    rec(
        "H6",
        "spherical_bessel",
        "spectral",
        "radial Helmholtz / Fourier–Bessel",
        "r²R'' + 2rR' + (k²r² − ℓ(ℓ+1))R = 0",
        "none",
        False,
        True,
        "Radial partner of Y_ℓm. Not loaded into ω·Sω.",
    ),
    rec(
        "H7",
        "fourier_character",
        "group",
        "characters of R^n or T^n",
        "e^{iξ·x}",
        "A",
        True,
        True,
        "Galerkin / Fourier on A. The abelian case of Peter–Weyl.",
    ),
    rec(
        "H8",
        "peter_weyl",
        "group",
        "matrix coefficients of a compact group",
        "L²(G) = ⊕_π (dim π) H_π",
        "none",
        False,
        True,
        "Nonabelian Fourier. Wigner D-matrices are the SU(2) case.",
    ),
    rec(
        "H9",
        "wigner_d",
        "group",
        "SU(2) / SO(3) matrix coefficients",
        "D^j_{m'm}(α,β,γ)",
        "none",
        False,
        True,
        "Rotation harmonics. Not a Cosmo knob and not F.",
    ),
    rec(
        "H10",
        "spherical_function",
        "group",
        "zonal / Gelfand spherical functions on G/K",
        "bi-K-invariant eigenfunctions of the algebra",
        "none",
        False,
        True,
        "Symmetric-space harmonics. A different catalog from Y_ℓm on S².",
    ),
    rec(
        "H11",
        "dirichlet_character",
        "group",
        "characters of (Z/NZ)*",
        "χ: (Z/NZ)* → C*",
        "Q",
        True,
        True,
        "Arithmetic harmonics. Sit near Track Q. Not a map onto (u·∇)u.",
    ),
    rec(
        "H12",
        "automorphic_maass",
        "group",
        "Maass forms / automorphic forms",
        "Δf = λf on Γ\\H, plus growth",
        "none",
        False,
        True,
        "Number-theory harmonics. Proof that the field kept growing after Fourier.",
    ),
    rec(
        "H13",
        "littlewood_paley",
        "analysis",
        "dyadic frequency shells Δ_j",
        "u = Σ_j Δ_j u",
        "B",
        True,
        True,
        "Already on Track B. A tool, not a regularity pass.",
    ),
    rec(
        "H14",
        "bony_paraproduct",
        "analysis",
        "low-high / high-low / high-high split of uv",
        "uv = T_u v + T_v u + R(u,v)",
        "B",
        True,
        True,
        "Already on Track B (T2). Energy-class low T is the live write, not a close.",
    ),
    rec(
        "H15",
        "calderon_zygmund",
        "analysis",
        "singular integral operators",
        "T f = p.v. K * f, K Calderón–Zygmund",
        "B",
        True,
        True,
        "The kernel class behind Riesz and much of NS harmonic analysis.",
    ),
    rec(
        "H16",
        "riesz_transform",
        "analysis",
        "R_j = ∂_j (−Δ)^{-1/2}",
        "u = −R ⊗ R · (something for Helmholtz)",
        "A",
        True,
        True,
        "Makes Helmholtz bounded on L^p, 1<p<∞. Not a Φ cancel.",
    ),
    rec(
        "H17",
        "hardy_space",
        "analysis",
        "H^p, maximal or conjugate-function definition",
        "sup_{t>0} |P_t * f| ∈ L^p",
        "none",
        False,
        True,
        "A different Hardy from the tube inequality on B. Do not glue the names.",
    ),
    rec(
        "H18",
        "tube_hardy",
        "analysis",
        "Hardy inequality on a vortex tube",
        "∫ |Γ|²/r² ≲ ∫ |∇Γ|² plus a wall",
        "B",
        True,
        True,
        "B4 pass. All-data I_tube fail (B4b). Packet class pass (B4c). Not H^p.",
    ),
    rec(
        "H19",
        "bmo_maximal",
        "analysis",
        "BMO and Hardy–Littlewood maximal function",
        "M f(x) = sup_B ⨍_B |f|",
        "none",
        False,
        True,
        "Standard harmonic analysis. Not loaded into Cosmo A,f,φ,δ.",
    ),
    rec(
        "H20",
        "besov_triebel",
        "analysis",
        "Besov / Triebel–Lizorkin scales",
        "B^s_{p,q}, F^s_{p,q}",
        "B",
        True,
        True,
        "LP cousins. Useful language for Bony estimates. Not a close.",
    ),
    rec(
        "H21",
        "hodge_form",
        "kernel",
        "harmonic differential forms",
        "Δα = 0, or dα = δα = 0",
        "none",
        False,
        True,
        "Hodge theory. Same word as Δu=0, different bundle. Not Y_ℓm.",
    ),
    rec(
        "H22",
        "quantum_oscillator",
        "spectral",
        "H = p²/2m + (1/2)mω²x²",
        "H ψ_n = ħω(n+1/2) ψ_n",
        "none",
        False,
        True,
        "A real Hamiltonian. Not SFE and not a producing-map.",
    ),
    rec(
        "H23",
        "string_overtone",
        "etymology",
        "integer frequency ratios of a vibrating string",
        "f_n = n f_1",
        "none",
        False,
        True,
        "Where the English word comes from. Motive, not a PDE theorem.",
    ),
    rec(
        "H24",
        "kolmogorov_spectrum",
        "false_friend",
        "E(k) ∼ k^{-5/3} inertial range",
        "not Δu = 0",
        "none",
        False,
        True,
        "Turbulence spectrum. Real fluid fact. Not harmonic analysis in the H1–H21 sense.",
    ),
    rec(
        "H25",
        "cosmo_oscillator_knobs",
        "false_friend",
        "Cosmo A, f, φ, δ labeled 'harmonic'",
        "score knobs, not Δu = 0",
        "U",
        True,
        False,
        "The reconstructed 4×4 used this word for oscillator knobs. Not Y_ℓm, not LP.",
    ),
    rec(
        "H26",
        "hb_nodes",
        "false_friend",
        "Harmonic Blueprint nodes.json",
        "shelved experiment, H0 not rejected",
        "none",
        False,
        False,
        "Shelved. Do not retune. Poetry as motive is allowed. Unifier is not.",
    ),
    rec(
        "H27",
        "sfe_F",
        "false_friend",
        "Simons Field Equation / oscillator F",
        "a different PDE",
        "none",
        False,
        False,
        "Shelved. Not NS, not Q_1, not Hodge, not LP.",
    ),
]


def claim(cid: str, statement: str, verdict: str, why: str) -> dict:
    return {"id": cid, "statement": statement, "verdict": verdict, "why": why}


def claims() -> list[dict]:
    return [
        claim(
            "C1",
            "DA can type the distinct mathematical objects that share the word",
            "pass",
            "The catalog is finite, named, and fail-able. That is a vocabulary.",
        ),
        claim(
            "C2",
            "The catalog covers every live desk use of the word",
            "pass",
            "A: Fourier, Helmholtz, Riesz. B: Y_ℓm, LP, Bony, CZ, tube Hardy. "
            "Q: Dirichlet characters. U: Cosmo knobs typed as false friends.",
        ),
        claim(
            "C3",
            "Those objects are one mathematical object",
            "fail",
            "Δu=0, Y_ℓm, LP shells, Hodge forms, characters, and H^p are not the same.",
        ),
        claim(
            "C4",
            "The list is a complete vocabulary of mathematics",
            "fail",
            "Harmonic analysis is an open field. Maass forms arrived late. More will.",
        ),
        claim(
            "C5",
            "The vocabulary writes a producing-map F to the couplings",
            "fail",
            "Naming operators does not output (g_s, g, g', G, Λ).",
        ),
        claim(
            "C6",
            "The vocabulary is the Harmonic Blueprint / SFE",
            "fail",
            "HB and SFE stay shelved. They are not the catalog and not a unifier.",
        ),
        claim(
            "C7",
            "The vocabulary implies classical NS regularity",
            "fail",
            "LP and Bony are already on B. Regularity stays open.",
        ),
        claim(
            "C8",
            "Cosmo A,f,φ,δ are spherical harmonics",
            "fail",
            "Those are score knobs. Y_ℓm is H3. Do not glue the label.",
        ),
        claim(
            "C9",
            "Musical overtones are the same object as Δu=0",
            "fail",
            "Etymology is real. Identity of objects is false. A string mode can be "
            "expanded in eigenfunctions; that does not make every 'harmonic' a tone.",
        ),
        claim(
            "C10",
            "Hodge forms, LP shells, and Hardy H^p are the same Hardy as the tube",
            "fail",
            "Four different objects. Tube Hardy is an inequality on Γ. H^p is a function space.",
        ),
        claim(
            "C11",
            "Track Q characters map onto (u·∇)u",
            "fail",
            "Arithmetic only. Inverse-GCD stays on Q.",
        ),
    ]


def desk_map() -> dict[str, list[str]]:
    out: dict[str, list[str]] = {"A": [], "B": [], "Q": [], "U": [], "none": []}
    for row in VOCAB:
        out[row["slot"]].append(row["name"])
    return out


def run(out: Path | None = None) -> dict:
    scored = claims()
    families = sorted({r["family"] for r in VOCAB})
    real = [r for r in VOCAB if r["real_math"]]
    friends = [r for r in VOCAB if r["family"] == "false_friend"]
    on_desk = [r for r in VOCAB if r["on_desk"]]
    payload = {
        "meta": {
            "question": "can DA make a complete harmonic vocabulary out of mathematics?",
            "answer": (
                "A typed catalog: yes. Desk coverage: yes. "
                "One object, a finished field, or a unifier: no."
            ),
            "not_a_unifier": True,
            "does_not_touch_ABQ_math": True,
            "does_not_retune_nodes": True,
        },
        "vocab": VOCAB,
        "claims": scored,
        "desk": desk_map(),
        "families": families,
        "counts": {
            "entries": len(VOCAB),
            "families": len(families),
            "real_math": len(real),
            "false_friends": len(friends),
            "on_desk": len(on_desk),
            "claims_pass": sum(1 for c in scored if c["verdict"] == "pass"),
            "claims_fail": sum(1 for c in scored if c["verdict"] == "fail"),
        },
        "how_far": [
            "named the distinct objects that share the English word",
            "typed kernel / spectral / group / analysis / etymology / false friend",
            "mapped every live desk use (A Fourier+Helmholtz, B LP/Bony/Y_lm/tube Hardy, Q characters, U Cosmo knobs)",
            "refused one-object, finished-field, F, HB, and regularity closes",
            "did not retune nodes.json",
        ],
        "next_da_move": (
            "Use the names on the slot they already sit on. "
            "Do not load the catalog into F or into ω·Sω. "
            "Next B write is still Hardy → I_tube, then low Bony T."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_harmonic.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA harmonic vocabulary. Typed catalog, not a unifier.")
    print(payload["meta"]["answer"])
    print(f"{'id':<4} {'name':<24} {'family':<14} slot  math")
    for r in payload["vocab"]:
        print(
            f"{r['id']:<4} {r['name']:<24} {r['family']:<14} "
            f"{r['slot']:<5} {'yes' if r['real_math'] else 'no'}"
        )
    print("claims:")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("desk", payload["desk"])
    print("counts", payload["counts"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
