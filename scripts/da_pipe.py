#!/usr/bin/env python3
"""
Live science pipe for the think tank.

The historical dream team stays. This is the now-bench: typed
streams (catalogs, strain, maps, graphs, satellite, holographic
boundary data) plus a rule that every pass/fail must be put
under a killer. Inference stays inside the slot. Primes do not
update black holes. A press release does not close Track B.

Snapshot dated 2026-09-03. Live arXiv sample is optional.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path


SNAPSHOT = "2026-09-03"


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


# How the data arrives. A form is not a theory.
FORMS = [
    rec(
        "F1",
        "time_series",
        "form",
        "strain, pulsar TOAs, light curves",
        "pass",
        "A legal form. LVK and IPTA already speak this.",
        examples="GWOSC strain; IPTA-DR3 times of arrival",
    ),
    rec(
        "F2",
        "spectrum",
        "form",
        "CMB C_ℓ, QNM frequencies, L-functions",
        "pass",
        "Same English word, three objects. Do not glue.",
        examples="Planck/ACT; Kerr QNM; LMFDB L-functions",
    ),
    rec(
        "F3",
        "image_map",
        "form",
        "EHT reconstructions, CMB maps, JWST fields",
        "pass",
        "An image is a processed observable, not a theorem.",
        examples="M87* 2017/2018/2021; Planck SMICA",
    ),
    rec(
        "F4",
        "catalog",
        "form",
        "event lists and parameter tables",
        "pass",
        "The form the now-bench actually updates from.",
        examples="GWTC-5.0; PDG; DESI galaxy catalog",
    ),
    rec(
        "F5",
        "graph",
        "form",
        "plots, networks, cosmic-web graphs, prime-gap plots",
        "pass",
        "A graph is a drawing of a table. It does not close a PDE.",
        examples="LVK time-frequency spectrograms; DESI clustering; gap graphs",
    ),
    rec(
        "F6",
        "satellite",
        "form",
        "space-borne time series, spectra, and maps",
        "pass",
        "Planck, Gaia, Fermi, Euclid, GRACE. Earth-orbit is still nature.",
        examples="Planck HFI; Gaia DR; Euclid Q1; Fermi-LAT",
    ),
    rec(
        "F7",
        "holographic_boundary",
        "form",
        "boundary correlators / interferometric visibilities used to reconstruct a bulk or an image",
        "open",
        "A data form, not AdS/CFT as a ToE and not a Cosmo hologram. EHT visibilities reconstruct a ring. That is not HB.",
        examples="EHT (u,v) visibilities; AdS/CFT correlators in papers",
    ),
]


# Typed streams. Each names a slot, a form, what it can kill, what it cannot.
PIPES = [
    rec(
        "P1",
        "LVK_GWTC5",
        "pipe",
        "LIGO–Virgo–KAGRA GWTC-5.0 (released 2026-05-26): 390 confirmed events, 161 new from O4b",
        "open",
        "Updates strong-field GR and remnant statistics. Does not speak 1/r^4.",
        slot="U",
        form="catalog+time_series+graph",
        can_kill="a claim that binary black holes are not seen; a wrong remnant-mass formula",
        cannot="Track B regularity; inverse-GCD; F; nodes.json",
        url="https://www.ligo.caltech.edu/news/ligo20260526",
        asof="2026-05-26",
    ),
    rec(
        "P2",
        "EHT_M87",
        "pipe",
        "EHT M87* 2021-epoch papers (2026): stable ring, evolving polarization, jet-base hint",
        "open",
        "Image + visibility (holographic reconstruction of an image). Horizon-scale plasma. Not HB Experiment 01.",
        slot="U",
        form="image_map+holographic_boundary",
        can_kill="a claim that M87* has no ring; a zero-spin MAD model at the margin",
        cannot="retune nodes.json; write F; close NS; prove primes",
        url="https://eventhorizontelescope.org/",
        asof="2026-02",
    ),
    rec(
        "P3",
        "DESI_DR2",
        "pipe",
        "DESI DR2 BAO (2025): 14M galaxies; ΛCDM challenged at ~3σ when combined; Σm_ν < 0.064 eV (ΛCDM)",
        "open",
        "Satellite-adjacent cosmology. Preference for w0wa is a tension, not F. Bayesian caution exists.",
        slot="U",
        form="catalog+spectrum+graph+satellite",
        can_kill="a claim that Λ is unchallengeable; Cosmo 0.06 eV as a derivation if it misses the bound",
        cannot="produce (g_s,g,g'); Track A or B; primes",
        url="https://www.desi.lbl.gov/2025/03/19/desi-dr2-results-march-19-guide/",
        asof="2025-03-19",
    ),
    rec(
        "P4",
        "IPTA_NANOGrav",
        "pipe",
        "IPTA-DR3 + NANOGrav 15 yr: nHz background, spectrum still being reconstructed (2026 PPL paper)",
        "open",
        "Time series from radio telescopes (not LVK band). Common-spectrum process. Source still open.",
        slot="U",
        form="time_series+spectrum",
        can_kill="a claim that there is no nHz common-spectrum process",
        cannot="identify the source as HB; close nature4",
        url="https://doi.org/10.1088/1742-6596/3177/1/012065",
        asof="2026-02",
    ),
    rec(
        "P5",
        "PDG_LHC",
        "pipe",
        "PDG + LHC run updates: the numbers L_SM consumes",
        "pass",
        "Already on the dream team as nature. The pipe keeps the table current.",
        slot="U",
        form="catalog",
        can_kill="a poster number that drifts outside PDG error",
        cannot="why those numbers",
        url="https://pdg.lbl.gov/",
        asof="rolling",
    ),
    rec(
        "P6",
        "LMFDB_NT",
        "pipe",
        "LMFDB + arXiv math.NT: L-functions, modular forms, prime-gap records (unconditional H=246 still stands)",
        "open",
        "The arithmetic stream. Heuristic gap papers are not theorems. Twin primes still open.",
        slot="Q",
        form="catalog+spectrum+graph",
        can_kill="a false λ_min(Q_N)>-1/2 for all N; a wrong L-function table",
        cannot="black-hole QNMs; NS regularity; F",
        url="https://www.lmfdb.org/",
        asof="2026-09",
    ),
    rec(
        "P7",
        "arXiv_math_AP",
        "pipe",
        "arXiv math.AP / fluids: new lemmas may sit on B if they keep 1/r^4 and name a check",
        "open",
        "A preprint is not a regularity pass. It is a proposal the Track B checker may score.",
        slot="B",
        form="catalog",
        can_kill="a B lemma whose identity fails on a named field",
        cannot="close domain B by press release",
        url="https://arxiv.org/list/math.AP/recent",
        asof="rolling",
    ),
    rec(
        "P8",
        "Euclid_JWST_Planck",
        "pipe",
        "Euclid / JWST / Planck–ACT–SPT: maps and spectra of the sky",
        "open",
        "Satellite and space-telescope forms. Update H0/Λ/structure tensions. Not Cosmo F.",
        slot="U",
        form="satellite+image_map+spectrum",
        can_kill="a cosmology number outside the current tension box",
        cannot="Track B; inverse-GCD; unshelve SFE",
        url="https://www.esa.int/Science_Exploration/Space_Science/Euclid",
        asof="rolling",
    ),
    rec(
        "P9",
        "IceCube_neutrino",
        "pipe",
        "IceCube / KM3NeT / oscillation data: Σm_ν and astrophysical neutrinos",
        "open",
        "Nature already sat as neutrino/cosmology. The pipe is the refresh.",
        slot="U",
        form="catalog+time_series",
        can_kill="a Σm_ν claim that misses the DESI+CMB bound",
        cannot="Cosmo 16th as F",
        url="https://icecube.wisc.edu/",
        asof="rolling",
    ),
]


# Historical team is not replaced. These are the now interpreters.
NOW = [
    {
        "name": "LVK collaboration",
        "slot": "U",
        "side": "now",
        "reads": "GWTC-5.0 strain and catalogs",
        "settles": "390 compact-binary detections through O4b",
        "cannot": "classical NS; primes; F",
        "suggest": "keep GW data on U as GR in the strong field; do not import it into the tube",
    },
    {
        "name": "EHT collaboration",
        "slot": "U",
        "side": "now",
        "reads": "M87* / Sgr A* visibilities and images",
        "settles": "a stable ring; time-varying polarization",
        "cannot": "HB Experiment 01; nodes.json",
        "suggest": "treat the image as a reconstructed observable; do not retune the shelved ringdown test",
    },
    {
        "name": "DESI collaboration",
        "slot": "U",
        "side": "now",
        "reads": "galaxy BAO + Lyα forest",
        "settles": "a live tension with plain ΛCDM; a Σm_ν bound",
        "cannot": "write F; finish nature4",
        "suggest": "Λ is an input that data may challenge; Cosmo produce still fails",
    },
    {
        "name": "IPTA / NANOGrav",
        "slot": "U",
        "side": "now",
        "reads": "pulsar timing arrays",
        "settles": "a nHz common-spectrum process exists at current evidence",
        "cannot": "name the source; glue to LVK band or to HB",
        "suggest": "keep the nHz spectrum on U, separate from LVK and from Q",
    },
    {
        "name": "PDG + LHC analyses",
        "slot": "U",
        "side": "now",
        "reads": "particle catalogs",
        "settles": "the consumed numbers this year",
        "cannot": "why those numbers",
        "suggest": "refresh the poster inputs; do not call a PDG update a derivation",
    },
    {
        "name": "LMFDB / analytic NT",
        "slot": "Q",
        "side": "now",
        "reads": "L-functions, modular forms, gap tables",
        "settles": "arithmetic facts that can kill a false floor",
        "cannot": "black holes; fluids",
        "suggest": "keep Q arithmetic; a new gap paper is not ω·Sω",
    },
    {
        "name": "math.AP authors (current)",
        "slot": "B",
        "side": "now",
        "reads": "preprints and papers on NSE / Euler",
        "settles": "nothing until a lemma hits the Track B checker",
        "cannot": "close domain B by announcement",
        "suggest": "if it keeps 1/r^4 and names a check, score it; regularity stays open",
    },
]


# Every desk verdict gets a kill test (pass) or a resurrection test (fail).
VERDICTS = [
    rec(
        "V1",
        "B1_low_flux",
        "falsify",
        "B1 pass: ∫(u_≤j·∇)u_j·u_j = 0",
        "pass",
        "Identity. Try to falsify: exhibit a periodic div-free field where the integral is not zero.",
        killer="named counterexample field on T^3",
        if_killed="drop B1; T2 rewrite",
        if_survives="still just an identity, not regularity",
        slot="B",
    ),
    rec(
        "V2",
        "B_regularity",
        "falsify",
        "domain B stays open",
        "open",
        "Not a pass. Killer of the open: a closed estimate for X. Fake pass killer: any BKM-from-L2 slogan.",
        killer="closed bound on X, or a proven blowup",
        if_killed="domain would move; not happened",
        if_survives="open remains the honest state",
        slot="B",
    ),
    rec(
        "V3",
        "B4b_Itube",
        "falsify",
        "B4b open: Hardy absorbs I_tube",
        "open",
        "The live tube write. Falsify the hope: a data class where the wall term wins.",
        killer="a tube family with wall ≳ I_tube at δ ~ 2^{-j*}",
        if_killed="B4b → fail; next write changes",
        if_survives="still open, not a pass",
        slot="B",
    ),
    rec(
        "V4",
        "A_theorem",
        "falsify",
        "Track A pass for this PDE, ε>0",
        "pass",
        "Try to falsify: break the energy identity or uniqueness at fixed ε>0. ε→0 is not this claim.",
        killer="Galerkin energy identity fails, or two H^1 solutions at the same ε",
        if_killed="Theorem A withdrawn for this write",
        if_survives="still not Track B",
        slot="A",
    ),
    rec(
        "V5",
        "Q_full_floor",
        "falsify",
        "full λ_min(Q_N)>-1/2 is fail",
        "fail",
        "Already killed. Resurrection: a proof for all N, against the known counterexamples.",
        killer="already exhibited; floor is false",
        if_killed="stays fail",
        if_survives="n/a — dead claim",
        slot="Q",
    ),
    rec(
        "V6",
        "F_exists",
        "falsify",
        "producing-map F is fail",
        "fail",
        "Affine holdout already lost. Resurrection: a public F with χ²_ext ≤ ε².",
        killer="holdout already ran",
        if_killed="stays fail until a new F is written and beaten against the null",
        if_survives="n/a",
        slot="U",
    ),
    rec(
        "V7",
        "destination_spectrum",
        "falsify",
        "spectrum-not-a-bag is open",
        "open",
        "Falsify the destination-as-done: we already did (no named D). Falsify the destination-as-program: show no operator can have those numbers as eigenvalues — that is a different, harder kill.",
        killer="named D whose eigenvalues are the couplings, or a no-go theorem",
        if_killed="C3 would move",
        if_survives="program stays open",
        slot="U",
    ),
    rec(
        "V8",
        "hb_exp01",
        "falsify",
        "HB Experiment 01 did not reject H0",
        "fail",
        "Already run. Resurrection would be a new protocol, not a retune of nodes.json.",
        killer="H0 not rejected",
        if_killed="stays fail; do not retune",
        if_survives="n/a",
        slot="U",
    ),
]


def claims() -> list[dict]:
    return [
        rec(
            "C1",
            "pipe_upgrades_tank",
            "method",
            "A typed live pipe belongs next to the dream team",
            "pass",
            "The past bench is paper. The now bench is collaborations reading current data. Both sit.",
        ),
        rec(
            "C2",
            "pipe_replaces_past",
            "method",
            "The pipe replaces Leray / Einstein / the historical team",
            "fail",
            "Additive. A new catalog does not unseat an old theorem.",
        ),
        rec(
            "C3",
            "spectrum_glue",
            "glue",
            "CMB spectrum, Kerr QNMs, and L-functions are one discovery",
            "fail",
            "Three objects. The word 'spectrum' is not entanglement.",
        ),
        rec(
            "C4",
            "gwtc_closes_B",
            "glue",
            "GWTC-5.0 closes classical NS regularity",
            "fail",
            "Strain on interferometers is not 1/r^4 on T^3.",
        ),
        rec(
            "C5",
            "desi_writes_F",
            "glue",
            "DESI dynamical-DE tension writes F or Cosmo 16",
            "fail",
            "A ~3σ tension is a U update. Produce still fails.",
        ),
        rec(
            "C6",
            "eht_unshelves_hb",
            "glue",
            "EHT images unshelve HB or allow retuning nodes.json",
            "fail",
            "Experiment 01 is closed. An image of M87* is not that test.",
        ),
        rec(
            "C7",
            "primes_are_qnms",
            "glue",
            "Current prime-gap and black-hole work are the same stream",
            "fail",
            "P6 is Q. P1/P2 are U. Learning a lot in both is not glue.",
        ),
        rec(
            "C8",
            "hologram_is_toe",
            "glue",
            "Holographic-boundary form (AdS/CFT or EHT visibilities) is nature4",
            "fail",
            "A form. Not a producing-map.",
        ),
        rec(
            "C9",
            "pass_needs_killer",
            "method",
            "A pass with no named killer is not a scientific pass",
            "pass",
            "Wave rule, applied to the desk. Survival is not truth.",
        ),
        rec(
            "C10",
            "all_science_ingested",
            "method",
            "This repo now contains a constant stream of all hard science",
            "fail",
            "It contains a typed pipe, a dated snapshot, and an optional arXiv sample. That is the program, not omniscience.",
        ),
    ]


ARXIV_QUERY = (
    "http://export.arxiv.org/api/query?"
    "search_query=cat:gr-qc+OR+cat:astro-ph.HE+OR+cat:astro-ph.CO"
    "+OR+cat:math.NT+OR+cat:math.AP"
    "&start=0&max_results=5&sortBy=submittedDate&sortOrder=descending"
)


def fetch_arxiv(timeout: float = 8.0) -> dict:
    """Optional live sample. Failure is open, not a desk fail."""
    out: dict = {
        "attempted": True,
        "ok": False,
        "n": 0,
        "items": [],
        "error": None,
        "query": ARXIV_QUERY,
    }
    try:
        req = urllib.request.Request(
            ARXIV_QUERY,
            headers={"User-Agent": "Ship_it_app-DA-pipe/0.1 (research notebook)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
        ns = {"a": "http://www.w3.org/2005/Atom"}
        root = ET.fromstring(raw)
        items = []
        for entry in root.findall("a:entry", ns):
            title = (entry.findtext("a:title", default="", namespaces=ns) or "").strip()
            title = " ".join(title.split())
            updated = (entry.findtext("a:updated", default="", namespaces=ns) or "")[:10]
            items.append({"title": title, "updated": updated})
        out["ok"] = True
        out["n"] = len(items)
        out["items"] = items
    except (urllib.error.URLError, TimeoutError, ET.ParseError, OSError) as exc:
        out["error"] = str(exc)
    return out


def infer(rows: list[dict]) -> list[str]:
    """Only inferences the falsification system is allowed to draw."""
    return [
        "A kill stays in its slot. LVK does not move B. LMFDB does not move U couplings.",
        "Same word 'spectrum' is not an edge. CMB, QNM, and L-functions stay unentangled.",
        "A survived kill on a pass is still a pass, not truth (wave rule).",
        "A fail with no resurrection on the desk stays fail (F, full Q floor, HB Exp 01).",
        "New catalogs update the now-bench and U numbers-as-inputs. They do not write F.",
        "DESI tension: Λ is challengeable as a model, still not an output of L_SM.",
        "GWTC-5.0: black holes are seen in strain. That is not 1/r^4 and not primes.",
    ]


def run(out: Path | None = None, fetch: bool = True) -> dict:
    scored = claims()
    live = fetch_arxiv() if fetch else {"attempted": False, "ok": False, "n": 0, "items": []}
    payload = {
        "meta": {
            "question": "pipe current hard science into the think tank and falsify every verdict",
            "snapshot": SNAPSHOT,
            "additive_to_team": True,
            "does_not_replace_past": True,
            "not_a_unifier": True,
            "does_not_retune_nodes": True,
            "does_not_glue_primes_to_holes": True,
            "uses_wave_falsification": True,
        },
        "forms": FORMS,
        "pipes": PIPES,
        "now": NOW,
        "verdicts": VERDICTS,
        "claims": scored,
        "live": live,
        "inferences": infer(scored),
        "counts": {
            "forms": len(FORMS),
            "pipes": len(PIPES),
            "now": len(NOW),
            "verdicts": len(VERDICTS),
            "claims_pass": sum(1 for c in scored if c["verdict"] == "pass"),
            "claims_fail": sum(1 for c in scored if c["verdict"] == "fail"),
            "live_ok": bool(live.get("ok")),
            "live_n": int(live.get("n") or 0),
        },
        "how_far": [
            "typed seven data forms including graph, satellite, holographic-boundary",
            "nine pipes dated; GWTC-5.0, EHT 2026, DESI DR2, IPTA-DR3, LMFDB, PDG, AP, Euclid/JWST, IceCube",
            "now-bench seated as collaborations, not chatbots",
            "every listed desk verdict has a killer or a resurrection",
            "glue of primes/QNM/NS/F/HB refused",
            "optional arXiv sample attempted; omniscience claim failed",
        ],
        "next_da_move": (
            "Refresh the snapshot; score any math.AP preprint that keeps 1/r^4. "
            "Do not let GWTC or EHT touch the tube. Next B write is still Hardy → I_tube."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_pipe.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA pipe. Now-bench + falsify every verdict. Past team stays.")
    print("snapshot", payload["meta"]["snapshot"])
    print("pipes:")
    for p in payload["pipes"]:
        print(f"  [{p['verdict']}] {p['name']} → {p['slot']}: {p['cannot']}")
    print("falsify verdicts:")
    for v in payload["verdicts"]:
        print(f"  [{v['verdict']}] {v['id']}: {v['killer']}")
    print("claims:")
    for c in payload["claims"]:
        print(f"  [{c['verdict']}] {c['id']}: {c['statement']}")
    live = payload["live"]
    print("live arXiv:", "ok" if live.get("ok") else "miss", "n=", live.get("n"))
    for item in live.get("items") or []:
        print(f"  {item.get('updated')} {item.get('title')[:80]}")
    print("inferences:")
    for line in payload["inferences"]:
        print(" -", line)
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
