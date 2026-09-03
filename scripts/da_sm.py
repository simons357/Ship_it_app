#!/usr/bin/env python3
"""
DA on the Standard Model Lagrangian.

Start over from the equation, not the Cosmo 16. The poster is a sum
of terms that CONSUMES (g_s, g, g', v, Yukawas, …). It does not
produce them. The two-sided equation that actually couples this
matter to gravity is Einstein + T_SM. That couple already passed
as a working pair (gq). It is not nature4.
"""

from __future__ import annotations

import json
from pathlib import Path


def rec(name: str, kind: str, verdict: str, why: str, **extra) -> dict:
    row = {"name": name, "kind": kind, "verdict": verdict, "why": why}
    row.update(extra)
    return row


# Five blocks on the usual expanded SM Lagrangian poster.
BLOCKS = [
    rec(
        "L1_qcd_yang_mills",
        "gauge",
        "pass",
        "SU(3)_c field strength + gluon self-interaction. This is a working Yang–Mills piece. g_s is an input.",
        consumes=["g_s"],
        produces=[],
    ),
    rec(
        "L2_electroweak_higgs",
        "gauge",
        "pass",
        "SU(2)_L × U(1)_Y + Higgs. After SSB, W/Z masses and the Weinberg rotation. g, g', v, λ are inputs.",
        consumes=["g", "g_prime", "v", "lambda_h"],
        produces=[],
    ),
    rec(
        "L3_fermion_gauge",
        "gauge",
        "pass",
        "Quarks and leptons couple to W, Z, A. Three generations and CKM are copied in, not derived.",
        consumes=["CKM", "three_generations"],
        produces=[],
    ),
    rec(
        "L4_yukawa",
        "gauge",
        "pass",
        "Higgs–fermion couplings write masses as m = y v / √2. The y's are inputs. Koide is not in this term.",
        consumes=["yukawas"],
        produces=[],
    ),
    rec(
        "L5_ghosts",
        "gauge_fix",
        "pass",
        "Faddeev–Popov ghosts. Bookkeeping for the path integral. Not a physical force.",
        consumes=["gauge_fix"],
        produces=[],
    ),
]


# Only isomorphisms / equivalences that are actually theorems.
ISOS = [
    rec(
        "SU2_iso_Spin3",
        "iso",
        "pass",
        "SU(2) ≅ Spin(3) ≅ Sp(1) as Lie groups. Does not output a coupling.",
    ),
    rec(
        "U1_iso_SO2",
        "iso",
        "pass",
        "U(1) ≅ SO(2) ≅ S¹. Does not output α.",
    ),
    rec(
        "weinberg_rotation",
        "iso",
        "pass",
        "(Z, A)^T = R(θ_W) (W³, B)^T. A real SO(2) on field space. θ_W is an input, not an output.",
    ),
    rec(
        "goldstone_eaten",
        "iso",
        "pass",
        "Three Goldstones ≅ longitudinal W±, Z (equivalence theorem). Degrees of freedom, not a number.",
    ),
    rec(
        "U3xU2xU1_is_cosmo_16",
        "iso",
        "fail",
        "Generator-count ≠ Cosmo 16 ≠ nature leftovers. A dimension count is P1, not F.",
    ),
    rec(
        "gluon_cubic_is_NS",
        "iso",
        "fail",
        "f^{abc} A A ∂A looks like convection. Different PDE, different manifold, no map onto ω·Sω.",
    ),
    rec(
        "yukawa_is_koide",
        "iso",
        "fail",
        "Yukawas are independent inputs. Koide is a 1981 mass-ratio, not a term in L4.",
    ),
    rec(
        "harmonic_phenotype",
        "iso",
        "fail",
        "Calling L a harmonic phenotype does not write F and does not move Track B.",
    ),
]


MISSING = [
    rec("gravity_G", "missing", "fail", "G_N is not a field in this Lagrangian."),
    rec("cosmological_constant", "missing", "fail", "Λ is not a term in this Lagrangian."),
    rec("neutrino_masses", "missing", "open", "Minimal poster SM has none. Data need them or a bound."),
    rec("theta_qcd", "missing", "open", "Usually omitted on the poster. Strong-CP leftover."),
]


def consumes() -> list[str]:
    names: list[str] = []
    for b in BLOCKS:
        names.extend(b.get("consumes") or [])
    return names


def realized_equation() -> dict:
    """The two-sided equation. Not F. The working couple."""
    return {
        "name": "Einstein_plus_T_SM",
        "equation": "G_μν + Λ g_μν = 8π G T_μν[SM]",
        "action": "S = S_EH[g] + ∫ √−g L_SM(g, ψ, A, H)",
        "left": "geometry (Einstein + Λ)",
        "right": "stress-energy built from this Lagrangian",
        "both_sides": True,
        "uses_the_poster": True,
        "produces_couplings": False,
        "gauge3": "fail",
        "nature4": "fail",
        "working_couple": "pass",
        "why": (
            "This is the equation with an equals sign that actually uses L_SM. "
            "T_μν is the Hilbert / Noether stress from blocks 1–4. "
            "The couple works (equivalence). It does not output g_s, θ_W, G, or Λ."
        ),
    }


def run(out: Path | None = None) -> dict:
    eq = realized_equation()
    payload = {
        "meta": {
            "object": "Standard Model Lagrangian (expanded poster form)",
            "forget_cosmo_16": True,
            "slot": "U",
            "not_a_unifier": True,
            "does_not_touch_ABQ": True,
            "L_consumes_couplings": True,
        },
        "blocks": BLOCKS,
        "isomorphisms": ISOS,
        "missing": MISSING,
        "consumes": consumes(),
        "produces": [],
        "realized_equation": eq,
        "gauge3": "fail",
        "nature4": "fail",
        "collapsed": False,
        "how_far": [
            "started over from L_SM, not the Cosmo 16",
            "five blocks are a working QFT (pass as dynamics, not as F)",
            "real isos: SU(2)≅Spin(3), U(1)≅SO(2), Weinberg rotation, Goldstones eaten",
            "fake isos failed: generator-count=16, gluon cubic=NS, Yukawa=Koide, harmonic phenotype",
            "L consumes g_s, g, g', v, λ, Yukawas, CKM; produces none of them",
            "G and Λ are not in the poster (fail as nature4 leftovers)",
            "realized two-sided equation is G_μν+Λg_μν=8πG T_μν[SM]",
            "that couple already passed as working (gq); it is not a producing-map",
            "Track A/B/Q untouched",
        ],
        "next_da_move": (
            "Keep the Einstein+T_SM couple. Do not hunt F inside L_SM — the "
            "couplings already went in. Nature4 still needs G and Λ as outputs "
            "of some other map. Fluids stay on Track B."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_sm.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA on the SM Lagrangian. Started over. Cosmo 16 not used.")
    print("L consumes:", ", ".join(payload["consumes"]))
    print("L produces: (nothing)")
    print("realized:", payload["realized_equation"]["equation"])
    print("working couple:", payload["realized_equation"]["working_couple"])
    print("gauge3:", payload["gauge3"], "nature4:", payload["nature4"])
    print("\nblocks:")
    for b in payload["blocks"]:
        print(f"  [{b['verdict']}] {b['name']}: {b['why']}")
    print("\nisos:")
    for r in payload["isomorphisms"]:
        print(f"  [{r['verdict']}] {r['name']}: {r['why']}")
    print("\nmissing:")
    for r in payload["missing"]:
        print(f"  [{r['verdict']}] {r['name']}: {r['why']}")
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
