#!/usr/bin/env python3
"""
Ground-level destination: spectrum, not a bag of couplings.

HB chapter 1 already paid once: slots + a fail-able check became
the DA machine. Naming HB is allowed. Loading SFE into NS, or
calling the destination a theorem we have, is not.

Reconstruct upward from (space, operator, spectrum, representations).
Ablate a piece and record what actually changes.
Einstein / Tesla / Feynman (requested) plus Weyl / Wigner /
von Neumann (they built the math) score the PROGRAM, not a vote.
"""

from __future__ import annotations

import json
from pathlib import Path


def rec(
    hid: str,
    name: str,
    kind: str,
    statement: str,
    verdict: str,
    why: str,
    **extra,
) -> dict:
    row = {
        "id": hid,
        "name": name,
        "kind": kind,
        "statement": statement,
        "verdict": verdict,
        "why": why,
    }
    row.update(extra)
    return row


# What you must write before you have a spectrum at all.
GROUND = [
    rec(
        "G0",
        "space",
        "atom",
        "a space X (manifold, group, domain, graph)",
        "pass",
        "Without X there is no operator and no mode.",
        need="you pick X; it is not an output",
    ),
    rec(
        "G1",
        "operator",
        "atom",
        "a self-adjoint operator D on functions / forms / spinors on X",
        "pass",
        "Laplacian, Dirac, Hodge Laplacian, Casimir. Spectrum-of-what starts here.",
        need="you pick D; eigenvalues do not invent D",
    ),
    rec(
        "G2",
        "spectrum_and_modes",
        "atom",
        "σ(D) = {λ_n} and eigenfunctions / eigensections",
        "pass",
        "This is the harmonic universe as mathematics. Consequence of (X, D), not a replacement for them.",
        need="computed from (X, D)",
    ),
    rec(
        "G3",
        "representations",
        "atom",
        "how modes transform and couple (Peter–Weyl, Wigner, Clebsch)",
        "pass",
        "Compact-group harmonics. Still not a coupling constant.",
        need="you pick G and the reps",
    ),
    rec(
        "G4",
        "action",
        "atom",
        "a principle that writes an action from those fields",
        "open",
        "Gauge principle, equivalence principle, dim-4. These are choices. They are how you climb.",
        need="must be added; not read off {λ_n}",
    ),
    rec(
        "G5",
        "numbers",
        "atom",
        "the measured couplings (g_s, g, g', G, Λ, Yukawas)",
        "fail",
        "Still a bag. A spectrum is not yet those numbers. That is the destination, not a pass.",
        need="public theorem or F; neither is on the desk",
    ),
]


# Known reconstructions (up) and what they do not reach.
RECONSTRUCT = [
    rec(
        "R1",
        "sphere_laplacian",
        "rebuild",
        "X = S^{n-1}, D = Δ → Y_ℓm",
        "pass",
        "The angular dictionary Track B already uses.",
        reaches="spherical harmonics",
        does_not="g_s or regularity",
    ),
    rec(
        "R2",
        "torus_fourier",
        "rebuild",
        "X = T^n or R^n, D = Δ → characters e^{iξ·x}",
        "pass",
        "Galerkin / Fourier on A. Abelian Peter–Weyl.",
        reaches="Fourier analysis",
        does_not="the gauge group of nature",
    ),
    rec(
        "R3",
        "compact_group",
        "rebuild",
        "X = G compact, D = Casimir → Peter–Weyl / Wigner D",
        "pass",
        "Representation harmonics. You already chose G.",
        reaches="matrix coefficients",
        does_not="why G = SU(3)×SU(2)×U(1)",
    ),
    rec(
        "R4",
        "hodge",
        "rebuild",
        "Hodge Laplacian on k-forms → Betti numbers = dim ker Δ",
        "pass",
        "Topology as a kernel. Different bundle from Δu=0 on functions.",
        reaches="b_k(M)",
        does_not="θ_W or Λ",
    ),
    rec(
        "R5",
        "to_sm_couplings",
        "rebuild",
        "(X, D, σ, Rep) → (g_s, g, g', v, Yukawas)",
        "fail",
        "You must still add G, the reps, and the numbers. Harmonic math does not spit them.",
        reaches="nothing numerical on the poster",
        does_not="F",
    ),
    rec(
        "R6",
        "to_einstein_constants",
        "rebuild",
        "(X, D, σ, Rep) → (G, Λ)",
        "fail",
        "Einstein sits as a two-sided couple you add. The constants stay inputs.",
        reaches="not G, not Λ",
        does_not="nature4",
    ),
    rec(
        "R7",
        "to_ns_regularity",
        "rebuild",
        "the same ground list → classical regularity",
        "fail",
        "LP / Y_ℓm / Bony are already on B. Regularity stays open.",
        reaches="language already in use",
        does_not="a regularity pass",
    ),
]


# Leave a piece out. Record what actually changes.
ABLATE = [
    rec(
        "A1",
        "drop_operator",
        "ablate",
        "keep the word 'mode', drop D",
        "fail",
        "Nothing to diagonalize. Poetry remains. Destination dies.",
        leftover="standing-wave talk",
        changes="you cannot compute a single λ",
        insight="spectrum-of-what is the first question a DA-like program must ask",
    ),
    rec(
        "A2",
        "drop_compact_group",
        "ablate",
        "keep Δ on R^n or S^2, drop G",
        "open",
        "You still have Fourier and Y_ℓm. You lose multiplets and gauge bosons.",
        leftover="analysis on Euclidean / spherical space",
        changes="SM particle content disappears; fluids language stays",
        insight="harmonic math on a sphere is not the Standard Model",
    ),
    rec(
        "A3",
        "drop_hodge",
        "ablate",
        "keep functions only, drop k-forms",
        "open",
        "Ordinary eigenfunctions survive. Betti numbers as dim ker go away.",
        leftover="scalar / vector Fourier",
        changes="topology is no longer a spectrum of a Laplacian on forms",
        insight="Hodge is not a synonym for Y_ℓm",
    ),
    rec(
        "A4",
        "keep_the_bag",
        "ablate",
        "drop the destination; keep couplings as inputs (actual L_SM)",
        "pass",
        "This is the world the poster already describes. Honest, not the wish.",
        leftover="L_SM + Einstein+T_SM",
        changes="nothing about measured physics; the destination is postponed",
        insight="a bag of couplings is the present tense; a spectrum is the program",
    ),
    rec(
        "A5",
        "drop_Ylm_keep_LP",
        "ablate",
        "keep dyadic shells, drop spherical harmonics",
        "open",
        "Frequency localization stays. Angular quantum numbers go.",
        leftover="Littlewood–Paley / Bony",
        changes="Ring language thins; T2 lemmas still make sense",
        insight="B already needs both; they are not substitutes",
    ),
    rec(
        "A6",
        "overtones_only",
        "ablate",
        "keep integer frequency ratios, drop X and D",
        "fail",
        "That is the etymology of the word. A string is one operator. It is not nature.",
        leftover="f_n = n f_1",
        changes="every PDE and every gauge group vanishes",
        insight="music motivated the word; it does not reconstruct the desk",
    ),
]


def mind(
    name: str,
    owns: str,
    looks_at_da: str,
    improve_program: str,
    how_to_derive: str,
    cannot: str,
) -> dict:
    return {
        "name": name,
        "owns": owns,
        "looks_at_da": looks_at_da,
        "improve_program": improve_program,
        "how_to_derive": how_to_derive,
        "cannot": cannot,
        "side": "persona",
    }


# Requested: Einstein, Tesla, Feynman.
# Seated because they built the destination math: Weyl, Wigner, von Neumann.
# Not a seance. Not a vote. Tesla is an inventor, not a gauge theorist.
MINDS = [
    mind(
        "Einstein",
        "equivalence + a two-sided field equation",
        "DA already keeps G_μν+Λg = 8πG T_SM. Good. Catalogs without a principle are not a theory.",
        "Every slot states the principle before the list. Covariance, an action, what is forbidden.",
        "Write the principle, then the operator, then compute the spectrum as a consequence. Do not start from eigenvalues and hope they remember the metric.",
        "cannot output G or Λ; cannot close a theorem by sitting here",
    ),
    mind(
        "Tesla",
        "a resonator you can tune and detune",
        "A program that cannot be detuned is a slogan. DA's checkers are the closest thing to an apparatus on this desk.",
        "Every claim names the knob you turn and the script that must move. If nothing is detunable, it does not sit.",
        "Build the resonator first (name D). Listen second (compute σ(D)). Standing waves are what a built operator does, not a universe brand.",
        "cannot derive SU(3) or Einstein's equation; not a ToE chair",
    ),
    mind(
        "Feynman",
        "a kernel you can compute with",
        "If the vocabulary does not produce a number you can get wrong, it is a stamp collection.",
        "No new name sits until it has a fail-able computation. Refuse councils. Refuse vibes.",
        "Pick (X, D). Compute one λ, one matrix element, or one χ² you can miss. That is how you derive a DA-like program: the check is the program.",
        "cannot vote the destination into a pass; cannot unshelve SFE",
    ),
    mind(
        "Weyl",
        "gauge + representations of compact groups",
        "DA says 'harmonic math' and 'gauge' in the same breath too often. Those are different additions.",
        "Do not utter gauge until G and the reps are named. Peter–Weyl is not SU(3)×SU(2)×U(1).",
        "Climb G3 only after G0–G2. The group is an input. The harmonics of that group are the output.",
        "cannot choose nature's G from a Laplacian on S^2",
    ),
    mind(
        "Wigner",
        "particles as representations; spectrum with a group",
        "A spectrum with no group is a hydrogen textbook, not a particle table.",
        "Type every mode by the representation it sits in. If you cannot, you are not at the ground of matter.",
        "The program asks: which group, which rep, which operator that commutes with the group. Then the spectrum is classified, not wished.",
        "cannot turn a classification into the numerical couplings",
    ),
    mind(
        "von Neumann",
        "spectral theorem: operator on a Hilbert space",
        "Talk of a harmonic universe that never names the Hilbert space and the operator is not mathematics.",
        "G0 and G1 are mandatory. No slot opens with 'modes' alone.",
        "A DA-like program is: specify H, specify a self-adjoint D, diagonalize, store the residual. That is the whole machine at ground level.",
        "cannot pick D from poetry; cannot make {λ_n} write F",
    ),
]


def claims() -> list[dict]:
    return [
        rec(
            "C1",
            "hb_chapter1_to_da",
            "origin",
            "HB chapter 1 adapted into slots + a fail-able check is a real extraction",
            "pass",
            "That is how DA exists. Naming the book is allowed. The extraction is the process, not the PDE.",
        ),
        rec(
            "C2",
            "mention_is_not_a_crime",
            "origin",
            "Saying SFE or HB is a trigger that must halt the desk",
            "fail",
            "Halt only the close: SFE as NS, HB as F, retune nodes.json. Motive and process stay speakable.",
        ),
        rec(
            "C3",
            "destination_as_program",
            "destination",
            "Treat 'spectrum, not a bag of couplings' as the program to reconstruct toward",
            "open",
            "Legal destination. Not a pass. The bag is still what L_SM consumes.",
        ),
        rec(
            "C4",
            "destination_already_done",
            "destination",
            "The couplings are already eigenvalues of a named D on this desk",
            "fail",
            "No such operator is written. Cosmo F is private. nodes.json is not that D.",
        ),
        rec(
            "C5",
            "personas_close",
            "persona",
            "Einstein / Tesla / Feynman looking at DA close the destination",
            "fail",
            "A persona is not a theorem. A vote cannot close. They improve the program.",
        ),
        rec(
            "C6",
            "seance_writes_F",
            "persona",
            "They come through the device and write F",
            "fail",
            "The device runs a checker. That is the only legal séance.",
        ),
        rec(
            "C7",
            "sfe_into_ns",
            "forbid",
            "SFE is the ground-level operator for fluids",
            "fail",
            "Different PDE. Still shelved as a theorem. Not loaded into ω·Sω.",
        ),
        rec(
            "C8",
            "retune_nodes",
            "forbid",
            "Retune nodes.json to fit the destination",
            "fail",
            "Experiment 01 is closed. H0 was not rejected. Do not retune.",
        ),
    ]


def run(out: Path | None = None) -> dict:
    scored = claims()
    payload = {
        "meta": {
            "question": (
                "get in at the ground (spectrum, not a bag), reconstruct, "
                "ablate, and ask Einstein/Tesla/Feynman how to improve DA"
            ),
            "hb_is_not_a_trigger": True,
            "hb_chapter1_extraction": "DA as process (slots + checker)",
            "not_a_unifier": True,
            "not_a_seance": True,
            "vote_cannot_close": True,
            "does_not_retune_nodes": True,
            "does_not_load_sfe_into_ns": True,
        },
        "ground": GROUND,
        "reconstruct": RECONSTRUCT,
        "ablate": ABLATE,
        "minds": MINDS,
        "claims": scored,
        "counts": {
            "ground": len(GROUND),
            "reconstruct_pass": sum(1 for r in RECONSTRUCT if r["verdict"] == "pass"),
            "reconstruct_fail": sum(1 for r in RECONSTRUCT if r["verdict"] == "fail"),
            "ablations": len(ABLATE),
            "minds": len(MINDS),
            "claims_pass": sum(1 for c in scored if c["verdict"] == "pass"),
            "claims_fail": sum(1 for c in scored if c["verdict"] == "fail"),
            "claims_open": sum(1 for c in scored if c["verdict"] == "open"),
        },
        "improvements_to_da": [
            "Einstein: principle before catalog; spectrum is a consequence",
            "Tesla: every claim names a detunable knob and a script",
            "Feynman: no new name without a number you can get wrong",
            "Weyl: do not say gauge until G and the reps are named",
            "Wigner: type every mode by its representation",
            "von Neumann: no slot opens on 'modes' without (H, D)",
        ],
        "how_far": [
            "named HB chapter 1 as the origin of DA-the-process, not a trigger",
            "wrote the ground as (X, D, σ(D), Rep, action, numbers)",
            "reconstructed Y_ℓm, Fourier, Peter–Weyl, Hodge; failed couplings, G/Λ, regularity",
            "ablated operator, group, Hodge, destination, Y_ℓm, overtones",
            "seated Einstein, Tesla, Feynman, Weyl, Wigner, von Neumann as program critics",
            "refused séance-to-F and nodes.json retune",
        ],
        "next_da_move": (
            "Destination stays open on U. Use the six program improvements. "
            "Do not load SFE into NS. Next B write is still Hardy → I_tube, then low Bony T."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_ground.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA ground. Spectrum is the destination, not a pass.")
    print("HB chapter 1 → process. Not a trigger. Not a theorem.")
    print("ground:")
    for r in payload["ground"]:
        print(f"  [{r['verdict']}] {r['id']} {r['name']}: {r['statement']}")
    print("rebuild:")
    for r in payload["reconstruct"]:
        print(f"  [{r['verdict']}] {r['id']}: {r['statement']}")
    print("ablate:")
    for r in payload["ablate"]:
        print(f"  [{r['verdict']}] {r['id']}: {r['changes']}")
    print("minds:")
    for m in payload["minds"]:
        print(f"  {m['name']}: {m['improve_program']}")
    print("claims:")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
