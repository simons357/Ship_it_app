#!/usr/bin/env python3
"""
Official CosmoEvolution 3D sixteen, isolated.

Source: https://cosmoevolution3d.base44.app  (live Topology vs Gauge table)
Ingested 2026-09-03. Core DA equation is still private / trade secret.

This is not the reconstructed 4×4 (that 16th was R). Do not glue
the two catalogs. Do not treat the app's 16/16 UI claim as a pass.
"""

from __future__ import annotations

import json
from pathlib import Path


SOURCE = {
    "url": "https://cosmoevolution3d.base44.app",
    "table": "Topology vs Gauge (home)",
    "key_findings": "https://cosmoevolution3d.base44.app/key-findings",
    "ingested": "2026-09-03",
    "host_typo": "bass44 → base44",
    "core_equation_public": False,
    "research_disclaimer": (
        "App: research and educational only; not established physics. "
        "Core DA equation is private / trade secret."
    ),
}

# Same five questions as the reconstructed fate hand.
FATE_KEYS = ("kind", "nature", "score", "produce", "next_piece")


def slot(
    cid: int,
    name: str,
    measured: str,
    app_claim: str,
    app_match: str,
    kind: str,
    nature: str,
    nature_verdict: str,
    score: str,
    score_verdict: str,
    produce: str,
    produce_verdict: str,
    next_piece: str,
    next_verdict: str,
    cluster: str,
    predates_da: bool,
    sits_at_measured: bool,
) -> dict:
    return {
        "id": cid,
        "name": name,
        "measured": measured,
        "app_claim": app_claim,
        "app_match": app_match,
        "cluster": cluster,
        "predates_da": predates_da,
        "sits_at_measured": sits_at_measured,
        "public_F": False,
        "hand": [
            {"name": "kind", "verdict": "open", "why": kind},
            {"name": "nature", "verdict": nature_verdict, "why": nature},
            {"name": "score", "verdict": score_verdict, "why": score},
            {"name": "produce", "verdict": produce_verdict, "why": produce},
            {"name": "next_piece", "verdict": next_verdict, "why": next_piece},
        ],
    }


# Official table. App labels: exact / good / approx / predicted.
# produce fails for everyone: F is not public.
COSMO_SIXTEEN = [
    slot(
        1,
        "Koide ratio (charged leptons)",
        "0.666661(7)",
        "exactly 2/3",
        "exact",
        "empirical mass-ratio (Koide 1981)",
        "lepton-mass pattern, not a force leftover",
        "fail",
        "not in the reconstructed lock-R vector",
        "fail",
        "formula predates DA; app papers say the spectral-zeta derivation has not been completed",
        "fail",
        "keep as a data fact; do not count tau and mμ/me as two extra hits",
        "open",
        "koide",
        True,
        False,
    ),
    slot(
        2,
        "tau mass",
        "1776.86 MeV",
        "Koide from e, μ → 1776.97 MeV",
        "exact 0.006%",
        "same Koide relation, written as m_τ",
        "same cluster as #1, not a new leftover",
        "fail",
        "not an independent score input",
        "fail",
        "output of the 1981 formula given e and μ, not of a public DA map",
        "fail",
        "collapse into the Koide cluster; one relation, not three predictions",
        "open",
        "koide",
        True,
        False,
    ),
    slot(
        3,
        "fermion generations",
        "3",
        "topological invariant",
        "exact",
        "counting fact of the SM",
        "family count, not a coupling",
        "fail",
        "not in lock-R",
        "fail",
        "'topological invariant' is a slogan until a public F outputs 3",
        "fail",
        "counting facts are real; they are not a producing-map",
        "open",
        "count",
        False,
        True,
    ),
    slot(
        4,
        "charge quantization |e|=|p|",
        "1 ± 10^{-21}",
        "winding conservation",
        "exact",
        "empirical / already in SM (Dirac quantization, U(1) embeddings)",
        "already-known constraint, not a new leftover",
        "fail",
        "not in lock-R",
        "fail",
        "winding slogan; no public F that produces |e|=|p| from a named topology",
        "fail",
        "treat as a known constraint, not a DA derivation",
        "open",
        "charge",
        True,
        True,
    ),
    slot(
        5,
        "α^{-1}",
        "137.035999…",
        "U(1) eigenvalue ≈137",
        "good 0.03%",
        "EM coupling (must-hit observable)",
        "yes — drop it and you are not unifying the forces",
        "open",
        "in the reconstructed 16 as log_alpha_em; decorative on lock-R",
        "fail",
        "sitting at the measured 137 is not a prediction",
        "fail",
        "still must-hit for nature4; needs a public F, not an eigenvalue slogan",
        "open",
        "alpha",
        False,
        True,
    ),
    slot(
        6,
        "sin²θ_W",
        "0.23122",
        "3/8 at unification → 0.231",
        "good",
        "weak mixing (must-hit)",
        "yes — a four-force unifier has to hit it",
        "open",
        "in the reconstructed 16 as sin2_theta_w; decorative on lock-R",
        "fail",
        "3/8 → 0.231 is standard GUT running, not a public topological F. "
        "App manifold sweep: 0/10 geometries match cos θ_W ≈ 0.878",
        "fail",
        "this is the gauge3 / GUT number; already screened. Manifold test already failed in-app",
        "fail",
        "weinberg",
        True,
        True,
    ),
    slot(
        7,
        "m_μ / m_e",
        "206.768",
        "recursive Koide",
        "good",
        "same Koide cluster as #1 and #2",
        "not an independent leftover",
        "fail",
        "not an independent score input",
        "fail",
        "recursive rewrite of the 1981 formula",
        "fail",
        "do not triple-count Koide",
        "open",
        "koide",
        True,
        False,
    ),
    slot(
        8,
        "Higgs VEV v",
        "246.22 GeV",
        "domain ground-state ≈246",
        "good ~1%",
        "electroweak scale",
        "yes — it is the scale the leftovers are measured against",
        "open",
        "enters lock-R as the denominator of hierarchy / vacuum / QCD ratios",
        "open",
        "'≈246' sits at the measured value; no public F",
        "fail",
        "keep as the scale leftover, not as a DA eigenvalue",
        "open",
        "vev",
        False,
        True,
    ),
    slot(
        9,
        "Higgs mass",
        "125.10 GeV",
        "first excitation ≈125",
        "good ~1%",
        "SM scalar mass",
        "SM parameter, not a force coupling",
        "fail",
        "not in lock-R",
        "fail",
        "'≈125' sits at the measured value",
        "fail",
        "related to v; still not G_N or Λ",
        "open",
        "higgs_mass",
        False,
        True,
    ),
    slot(
        10,
        "CKM θ_12",
        "13.04°",
        "interface winding ≈13°",
        "approx ~3%",
        "flavor mixing angle",
        "flavor, not a force leftover",
        "fail",
        "not in the reconstructed lock-R vector",
        "fail",
        "'≈13°' sits at the measured value",
        "fail",
        "flavor is a different book from nature4",
        "open",
        "flavor",
        False,
        True,
    ),
    slot(
        11,
        "α_s(M_Z)",
        "0.1181",
        "SU(3) spectral flow ≈0.118",
        "approx",
        "strong coupling (must-hit)",
        "yes",
        "open",
        "in the reconstructed 16 as log_alpha_s; decorative on lock-R",
        "fail",
        "sitting at 0.118 is not a prediction",
        "fail",
        "still must-hit for nature4",
        "open",
        "alpha_s",
        False,
        True,
    ),
    slot(
        12,
        "m_p / m_e",
        "1836.15",
        "baryon eigenvalue ≈1836",
        "approx",
        "baryon / lepton mass ratio",
        "not a force leftover",
        "fail",
        "not in lock-R",
        "fail",
        "sitting at 1836 is not a prediction",
        "fail",
        "hadron mass is a different book",
        "open",
        "hadron",
        False,
        True,
    ),
    slot(
        13,
        "Λ (cosmological constant)",
        "1.1×10^{-52} m^{-2}",
        "domain web tension (order of magnitude)",
        "order of magnitude",
        "vacuum leftover (must-hit)",
        "yes — drop Λ and you are not talking about nature",
        "open",
        "in the reconstructed 16 as log_cc_ratio; default lock-R mover",
        "open",
        "order-of-magnitude / 'derivable' is not χ²_ext ≤ ε² from a public F",
        "fail",
        "this is the GQ leftover the score already hit; still no F",
        "open",
        "vacuum",
        False,
        False,
    ),
    slot(
        14,
        "Newton G",
        "6.674×10^{-11}",
        "Planck spectral gap (order of magnitude)",
        "order of magnitude",
        "gravity leftover (must-hit)",
        "yes",
        "open",
        "in the reconstructed 16 as log_hierarchy; default lock-R mover",
        "open",
        "order-of-magnitude is not a public F",
        "fail",
        "same GQ leftover as Planck; do not also count ℓ_P as a second hit",
        "open",
        "planck",
        False,
        False,
    ),
    slot(
        15,
        "Planck length ℓ_P",
        "1.616×10^{-35} m",
        "domain foam cell (order of magnitude)",
        "order of magnitude",
        "definitional rewrite of G: ℓ_P = sqrt(ħG/c³)",
        "same leftover as #14, not a new one",
        "fail",
        "same hierarchy piece as G",
        "fail",
        "not independent of G",
        "fail",
        "collapse G and ℓ_P into one Planck leftover",
        "open",
        "planck",
        False,
        False,
    ),
    slot(
        16,
        "Σ m_ν",
        "< 0.12 eV (bound)",
        "≈ 0.06 eV",
        "predicted, untested",
        "the only forward number on the table",
        "neutrino masses, not a force leftover",
        "fail",
        "not in lock-R",
        "fail",
        "F is private, so 0.06 eV cannot be checked as a derivation. Open as a number to kill",
        "fail",
        "wait for cosmology / 0νββ; still not nature4",
        "open",
        "neutrino",
        False,
        False,
    ),
]


APP_LEVEL = [
    {
        "name": "DA_predicts_16_of_16",
        "app_says": "gauge 0/16, DA 16/16 (4 exact, 5 good, 6 approx, 1 predicted)",
        "verdict": "fail",
        "why": (
            "Core equation is private. Several slots sit at the measured value. "
            "Koide is counted three times. G and ℓ_P are one leftover. "
            "Weinberg 3/8 is standard GUT running. Manifold sweep already failed."
        ),
    },
    {
        "name": "public_producing_map_F",
        "app_says": "core DA equation is private / trade secret",
        "verdict": "fail",
        "why": "P3 requires a public F and χ²_ext ≤ ε². A hidden equation is not a check.",
    },
    {
        "name": "manifold_lambda_ratio_is_cos_theta_W",
        "app_says": "10 standard geometries, 0 match cos θ_W ≈ 0.878; highest Bolza 0.717",
        "verdict": "fail",
        "why": (
            "The app already recorded this as a DA prediction fail for every "
            "known exact-spectrum topology. A tuned torus aspect ratio is a fit, "
            "not a prediction (tuning trap)."
        ),
    },
    {
        "name": "gauge_couplings_should_not_meet",
        "app_says": "SM miss + no superpartners ⇒ topological unification",
        "verdict": "fail",
        "why": (
            "Non-convergence is only gauge3. Our screen already has SM fail and "
            "MSSM-class open as gauge3, fail as nature4. A miss is not a topology."
        ),
    },
    {
        "name": "scenario_B_strengthening",
        "app_says": "unification is topological, not gauge",
        "verdict": "fail",
        "why": "Slogan. Collapse still requires a public F. Waveform has not collapsed.",
    },
]


SPLIT_55 = {
    "source": "https://cosmoevolution3d.base44.app/key-findings  (finding 03)",
    "n": 55,
    "gauge": 1,
    "harmonic": 19,
    "anomaly_to_H": 2,
    "unresolved": 26,
    "both": 7,
    "names_extracted": False,
    "note": (
        "Counts only. Full 55 names were not extracted from the minified bundle. "
        "Do not invent the missing names. The official 16 is the named table."
    ),
}


OVERLAP = {
    "in_both_catalogs": [
        "α (EM)",
        "sin²θ_W",
        "α_s",
        "v (as scale in hierarchy / vacuum)",
        "G / Planck",
        "Λ",
        "CKM θ_12 (Cosmo named; reconstructed 16 did not carry it as a lock-R input)",
    ],
    "cosmo_only": [
        "Koide cluster (K, m_τ, m_μ/m_e)",
        "generations = 3",
        "charge quantization",
        "Higgs mass",
        "m_p/m_e",
        "ℓ_P (duplicate of G)",
        "Σ m_ν",
    ],
    "reconstruction_only": [
        "θ_QCD",
        "S_c, δ, A, f, φ, κ, |∇C|",
        "R (output; Cosmo 16th is Σ m_ν, not R)",
    ],
    "do_not_glue": True,
}


def unique_clusters(rows: list[dict]) -> dict:
    groups: dict[str, list[str]] = {}
    for r in rows:
        groups.setdefault(r["cluster"], []).append(r["name"])
    return {
        "n_slots": len(rows),
        "n_clusters": len(groups),
        "groups": groups,
        "note": (
            "16 UI slots collapse to 13 clusters once Koide is one relation "
            "and G ≡ ℓ_P. α, sin²θ_W, and α_s stay three leftovers. "
            "v and m_H stay two objects. Still no public F."
        ),
    }


def produce_all_fail(rows: list[dict]) -> bool:
    return all(
        next(h["verdict"] for h in r["hand"] if h["name"] == "produce") == "fail"
        for r in rows
    )


def nature4() -> dict:
    return {
        "level": "nature4",
        "verdict": "fail",
        "why": (
            "No public F hits (g_s, g_w, g_em, G_N) with Λ in the sum. "
            "G and Λ are order-of-magnitude slogans. Couplings sit at measured values."
        ),
    }


def gauge3() -> dict:
    return {
        "level": "gauge3",
        "verdict": "fail",
        "why": (
            "The app does not claim a 3-meet. It treats the SM miss as evidence "
            "for topology. That is still only gauge3, and it is not a pass."
        ),
    }


def run(out: Path | None = None) -> dict:
    clusters = unique_clusters(COSMO_SIXTEEN)
    payload = {
        "meta": {
            "catalog": "official CosmoEvolution 3D Topology vs Gauge table",
            "cosmos_list_found": True,
            "cosmos_core_equation_public": False,
            "this_list_is_reconstructed_R": False,
            "not_a_unifier": True,
            "do_not_accept_16_of_16": True,
            "source": SOURCE,
        },
        "sixteen": COSMO_SIXTEEN,
        "clusters": clusters,
        "app_level": APP_LEVEL,
        "split_55": SPLIT_55,
        "overlap_with_reconstructed_16": OVERLAP,
        "gauge3": gauge3(),
        "nature4": nature4(),
        "produce_all_fail": produce_all_fail(COSMO_SIXTEEN),
        "collapsed": False,
        "how_far": [
            "Cosmo 16 names are in the repo (list-found = true)",
            "core equation still private (P3 / collapse still fail)",
            "produce fails for all 16 slots",
            "app 16/16 claim fails the same screen as everyone else",
            "manifold λ1/λ2 = cos θ_W already failed in the app (0/10)",
            "Koide is one 1981 relation counted three times",
            "G and ℓ_P are one leftover",
            "Weinberg 3/8 → 0.231 is standard GUT running",
            "G and Λ remain the same GQ leftovers the score already hit",
            "Σ m_ν ≈ 0.06 eV is the only forward number; untested; F still hidden",
            "55-parameter split is counts only; names not extracted",
            "reconstructed 4×4 stays a different catalog; 16th there is R, here Σ m_ν",
        ],
        "next_da_move": (
            "Blocked on a public producing-map from a named topology to "
            "(g_s, g_w, g_em, G_N, Λ). Do not retune, do not glue catalogs, "
            "do not treat 16/16 as a pass."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_cosmo.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("Official Cosmo 16. List found. Core equation still private.")
    print(f"source: {SOURCE['url']}")
    print(f"{'#':>2} {'name':<36} {'app':<18} produce nature")
    for r in payload["sixteen"]:
        prod = next(h["verdict"] for h in r["hand"] if h["name"] == "produce")
        nat = next(h["verdict"] for h in r["hand"] if h["name"] == "nature")
        print(f"{r['id']:2d} {r['name']:<36} {r['app_match']:<18} {prod:<7} {nat}")
    print("clusters:", payload["clusters"]["n_clusters"], "from", payload["clusters"]["n_slots"])
    print("gauge3:", payload["gauge3"]["verdict"], "nature4:", payload["nature4"]["verdict"])
    print("16/16:", next(a["verdict"] for a in APP_LEVEL if a["name"] == "DA_predicts_16_of_16"))
    print("collapsed:", payload["collapsed"])
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
