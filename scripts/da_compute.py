#!/usr/bin/env python3
"""
Computing techniques the desk can borrow or already runs.

A library is a tool. It sits on one slot and needs a killer.
It does not write F, close B, or unshelve HB.
"""

from __future__ import annotations

import json
from pathlib import Path


def rec(
    hid: str,
    name: str,
    slot: str,
    status: str,
    verdict: str,
    why: str,
    **extra,
) -> dict:
    row = {
        "id": hid,
        "name": name,
        "slot": slot,
        "status": status,
        "verdict": verdict,
        "why": why,
    }
    row.update(extra)
    return row


# status: wired | borrow | refuse
# verdict: pass = legal to use for that job; fail = would be glue / fake close
TECH = [
    rec(
        "T1",
        "numpy_fft_galerkin",
        "A",
        "wired",
        "pass",
        "scripts/augmented_ns_verify.py: Fourier on T^3, 2/3 dealias, Leray project, energy residual.",
        does="consistency of the Q1 energy law",
        cannot="prove Theorem A, or speak B",
    ),
    rec(
        "T2",
        "numpy_eigh_gcd",
        "Q",
        "wired",
        "pass",
        "scripts/spectral_floor_explore.py: Rayleigh / eigenvalues of Q, Qtilde, H.",
        does="kill the full-floor slogan; keep Bridge* / Theorem P / H_N≥-1",
        cannot="map onto (u·∇)u",
    ),
    rec(
        "T3",
        "numpy_b_identities",
        "B",
        "wired",
        "pass",
        "scripts/track_b_lemmas.py: FFT probes of B1 and related identities.",
        does="fail an identity if it is false on a named field",
        cannot="close regularity",
    ),
    rec(
        "T4",
        "arxiv_atom",
        "U",
        "wired",
        "pass",
        "scripts/da_pipe.py: optional live sample from export.arxiv.org.",
        does="refresh the now-bench titles",
        cannot="ingest all of science; collapse the wave",
    ),
    rec(
        "T5",
        "unittest_checker",
        "meta",
        "wired",
        "pass",
        "The anti-bullshit device. Every command has a fail-able test.",
        does="kill a fake pass",
        cannot="replace a missing estimate",
    ),
    rec(
        "T6",
        "scipy_or_pyfftw",
        "A",
        "borrow",
        "pass",
        "Same Galerkin, faster FFT. Drop-in for T1.",
        does="larger n on the energy residual",
        cannot="ε→0 or Track B",
    ),
    rec(
        "T7",
        "dedalus_spectral",
        "A",
        "borrow",
        "pass",
        "Public spectral PDE toolkit (Fourier / Chebyshev). Energy checks on A, probes on B.",
        does="named residual of a named PDE",
        cannot="a no-blowup run is not a regularity pass",
    ),
    rec(
        "T8",
        "sympy_identities",
        "B",
        "borrow",
        "pass",
        "Computer algebra for B1 / B5 / tube Hardy algebra. Also SM index contractions on U.",
        does="expand an identity and see if it is 0",
        cannot="absorb I_tube for all data",
    ),
    rec(
        "T9",
        "lp_bony_fft",
        "B",
        "borrow",
        "pass",
        "Dyadic projectors and Bony T/R from the same FFT already on the desk.",
        does="numerical probe of T2 / occupation; a field where B4b wall wins",
        cannot="close domain B",
    ),
    rec(
        "T10",
        "lmfdb_pari_sage",
        "Q",
        "borrow",
        "pass",
        "LMFDB API, Sage/Pari, flint. L-functions, characters, gcd tables.",
        does="kill a false arithmetic claim",
        cannot="QNMs or NS",
    ),
    rec(
        "T11",
        "gwosc_pdg_desi",
        "U",
        "borrow",
        "pass",
        "GWOSC strain/catalogs, PDG listings, DESI public BAO tables.",
        does="refresh consumed numbers and tensions",
        cannot="write F; enter the tube",
    ),
    rec(
        "T12",
        "jax_autodiff_energy",
        "A",
        "borrow",
        "pass",
        "Differentiate a discrete energy and check the residual matches the code.",
        does="catch an algebra bug in the Galerkin step",
        cannot="Theorem A by autodiff",
    ),
    rec(
        "T13",
        "dns_never_blew_up",
        "B",
        "refuse",
        "fail",
        "A long smooth run is not a closed estimate for X.",
        does="nothing legal on domain B",
        cannot="regularity",
    ),
    rec(
        "T14",
        "qnm_solver_into_b_or_q",
        "U",
        "refuse",
        "fail",
        "Kerr QNM codes sit next to EHT/LVK as observation language. Not 1/r^4, not H_N.",
        does="optional U catalog only",
        cannot="retune nodes.json; glue to primes",
    ),
    rec(
        "T15",
        "cosmo_private_core",
        "U",
        "refuse",
        "fail",
        "The app equation is not public. No SDK to wire.",
        does="nothing",
        cannot="produce the couplings",
    ),
    rec(
        "T16",
        "llm_proves_the_theorem",
        "meta",
        "refuse",
        "fail",
        "The generator may propose. The checker scores. A model is not a close.",
        does="emit a sentence for classify / check",
        cannot="collapse the wave",
    ),
]


def claims() -> list[dict]:
    return [
        {
            "id": "C1",
            "statement": "The desk already has FFT-Galerkin, eigh-GCD, B-identity probes, arXiv sample, unittest",
            "verdict": "pass",
            "why": "T1–T5 are wired and slot-typed.",
        },
        {
            "id": "C2",
            "statement": "scipy/Dedalus/sympy/LMFDB/GWOSC/PDG/DESI may be borrowed on their slot",
            "verdict": "pass",
            "why": "Each names a job and a cannot.",
        },
        {
            "id": "C3",
            "statement": "Wiring a library closes Track B or writes F",
            "verdict": "fail",
            "why": "A tool is not an estimate and not a producing-map.",
        },
        {
            "id": "C4",
            "statement": "DNS, QNM→B/Q, Cosmo core, or LLM-as-proof may be wired as closes",
            "verdict": "fail",
            "why": "T13–T16 are refuse.",
        },
    ]


def run(out: Path | None = None) -> dict:
    scored = claims()
    payload = {
        "meta": {
            "question": "what computing techniques can we borrow or wire in?",
            "writeup": "docs/DA-COMPUTE.md",
            "not_a_unifier": True,
            "anti_bullshit_device": True,
            "does_not_close_B": True,
        },
        "tech": TECH,
        "claims": scored,
        "already": [t["name"] for t in TECH if t["status"] == "wired"],
        "borrow": [t["name"] for t in TECH if t["status"] == "borrow"],
        "refuse": [t["name"] for t in TECH if t["status"] == "refuse"],
        "counts": {
            "wired": sum(1 for t in TECH if t["status"] == "wired"),
            "borrow": sum(1 for t in TECH if t["status"] == "borrow"),
            "refuse": sum(1 for t in TECH if t["status"] == "refuse"),
        },
        "next_da_move": (
            "If you wire one, start with sympy on B1/B5 or LP/Bony FFT probes for B4b. "
            "A residual is a check. It is not I_tube."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_compute.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA compute. A library sits on one slot. It is not a theorem.")
    print(f"{'id':<4} {'status':<7} {'slot':<5} {'name'}")
    for t in payload["tech"]:
        print(f"{t['id']:<4} {t['status']:<7} {t['slot']:<5} {t['name']}")
    print("claims:")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    print("next:", payload["next_da_move"])
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
