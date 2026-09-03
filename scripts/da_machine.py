#!/usr/bin/env python3
"""
Domain Architect process machine.

Operator needs no chops. AI proposes. Checkers verdict. Glue is refused.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LOG = ROOT / "results" / "da_machine_log.json"

SLOTS = {
    "A": {
        "object": "Q1-augmented NS, eps>0",
        "note": "docs/AUGMENTED-NS-PROOF-CHAIN.md",
        "checker": ["python3", "-m", "unittest", "tests.test_augmented_ns_verify", "-v"],
    },
    "B": {
        "object": "classical NS, keep 1/r^4",
        "note": "docs/TRACK-B-LEMMAS.md",
        "checker": ["python3", "-m", "unittest", "tests.test_track_b_lemmas", "-v"],
        "domain_pass_means": "open",
        "why_no_pass": "Lemma identities may hold. Regularity stays open.",
    },
    "Q": {
        "object": "inverse-GCD floors",
        "note": "docs/SPECTRAL-FLOOR-EXPLORATION.md",
        "checker": ["python3", "-m", "unittest", "tests.test_spectral_floor_explore", "-v"],
    },
    "U": {
        "object": "realization score R (exercise, not a unifier)",
        "note": "docs/UNIFIER-EXERCISE.md",
        "checker": [
            "python3",
            "-m",
            "unittest",
            "tests.test_unifier_exercise",
            "tests.test_unifier_combo",
            "tests.test_da_sixteen",
            "tests.test_da_fingers",
            "tests.test_da_how",
            "tests.test_da_flush",
            "tests.test_da_wave",
            "tests.test_da_game",
            "tests.test_da_screen",
            "tests.test_da_gq",
            "tests.test_da_separate",
            "tests.test_da_cosmo",
            "tests.test_da_sm",
            "-v",
        ],
    },
}

FORBIDDEN = [
    (r"\bsolved (navier|ns|rh|riemann)\b", "prize-style close"),
    (r"lambda_?min\s*\(\s*(q|qtilde|\\widetilde\s*q)", "full-spectrum Q floor"),
    (r"cos\s*\(?\s*alpha_?3", "Biot-Savart depletion slogan"),
    (r"beale|bkm", "BKM-from-L2 style close"),
    (r"\bsfe\b|\buhf\b|\bdhfa\b", "shelved HB stack"),
    (r"track\s*a\s*(implies|=>|⇒)\s*track\s*b", "A=>B glue"),
    (r"bridge.*=.*snd|snd.*=.*bridge", "triple-lock glue"),
]


def load_log() -> dict:
    if LOG.exists():
        return json.loads(LOG.read_text())
    return {
        "meta": {
            "experiment": "DA-process-machine",
            "operator_needs_chops": False,
            "ai_is_generator": True,
            "not_a_unifier": True,
        },
        "runs": [],
        "counts": {"scored": 0, "pass": 0, "fail": 0, "open": 0},
    }


def save_log(data: dict) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    LOG.write_text(json.dumps(data, indent=2))


def classify_claim(claim: str) -> dict:
    text = claim.lower()
    for pat, why in FORBIDDEN:
        if re.search(pat, text, flags=re.I):
            return {"domain": None, "verdict": "fail", "reason": f"forbidden: {why}"}
    if re.search(r"\bq_?1\b|augmented|ladyzhenskaya", text):
        return {"domain": "A", "verdict": "open", "reason": "looks like Track A; run check A"}
    if re.search(
        r"1/r\^?4|ring|bony|3-conc|spread|tube|vorticity|hardy|\bgamma\b|triad|track b|t2 lemma",
        text,
    ):
        return {
            "domain": "B",
            "verdict": "open",
            "reason": "looks like Track B; run trackb. Regularity stays open.",
        }
    if re.search(r"bridge|prime.?block|h_n|inverse.?gcd|qtilde|theorem p", text):
        return {"domain": "Q", "verdict": "open", "reason": "looks like Track Q; run check Q"}
    if re.search(
        r"\bunifier\b|realization|\block_r\b|cosmos|hierarchy|vacuum|\b16\b|finger|wave|falsif|superposition|entangle|standard model|lagrangian|yukawa|weinberg",
        text,
    ):
        return {"domain": "U", "verdict": "open", "reason": "looks like score U / SM Lagrangian / waveform; run sm or how"}
    return {"domain": None, "verdict": "open", "reason": "no slot; rephrase into A, B, Q, or U"}


def run_checker(domain: str) -> dict:
    slot = SLOTS[domain]
    if slot["checker"] is None:
        return {"domain": domain, "verdict": "open", "reason": slot["why_no_pass"]}
    proc = subprocess.run(slot["checker"], cwd=ROOT, capture_output=True, text=True)
    tail = (proc.stdout + proc.stderr).strip().splitlines()
    if proc.returncode != 0:
        return {
            "domain": domain,
            "verdict": "fail",
            "reason": "checker exit %s" % proc.returncode,
            "tail": tail[-8:],
        }
    # Slot B: lemma tests holding is not a regularity pass.
    if slot.get("domain_pass_means") == "open":
        return {
            "domain": domain,
            "verdict": "open",
            "reason": slot["why_no_pass"],
            "tail": tail[-8:],
        }
    return {
        "domain": domain,
        "verdict": "pass",
        "reason": "checker exit 0",
        "tail": tail[-8:],
    }


def append_run(domain: str | None, claim: str, verdict: str, note: str) -> dict:
    data = load_log()
    rec = {
        "t": datetime.now(timezone.utc).isoformat(),
        "domain": domain,
        "claim": claim,
        "verdict": verdict,
        "note": note,
    }
    data["runs"].append(rec)
    data["counts"]["scored"] = len(data["runs"])
    data["counts"]["pass"] = sum(1 for r in data["runs"] if r["verdict"] == "pass")
    data["counts"]["fail"] = sum(1 for r in data["runs"] if r["verdict"] == "fail")
    data["counts"]["open"] = sum(1 for r in data["runs"] if r["verdict"] == "open")
    save_log(data)
    return rec


def cmd_status() -> int:
    data = load_log()
    print("DA process machine. Operator needs no chops.")
    print("Slots:")
    for key, slot in SLOTS.items():
        print(f"  {key}  {slot['object']}")
        print(f"      {slot['note']}")
    print("counts", json.dumps(data["counts"]))
    return 0


def cosmos_drill() -> dict:
    """DA drill-down: official Cosmo 16 names, must-hits, score core, missing F."""
    return {
        "slot": "U",
        "cosmos_list_found": True,
        "cosmos_core_equation_public": False,
        "n_claimed": 16,
        "n_confirmed": 16,
        "source": "https://cosmoevolution3d.base44.app",
        "catalog": "docs/COSMO-SIXTEEN.md",
        "possibility_claim": {
            "statement": "unification is possible with about 16 variables",
            "verdict": "open",
            "why": (
                "Names exist. A finite n is a real narrowing IF one public map F "
                "of those n hits the four couplings. The app saying 16/16 is "
                "not the check. The check is χ²_ext(F(x)) ≤ ε². F is still private."
            ),
        },
        "layers": [
            {
                "layer": 0,
                "name": "official Cosmo 16 (Topology vs Gauge table)",
                "pieces": [
                    "Koide",
                    "m_tau",
                    "generations",
                    "charge",
                    "alpha",
                    "sin2_theta_W",
                    "m_mu/m_e",
                    "v",
                    "m_H",
                    "CKM_theta12",
                    "alpha_s",
                    "m_p/m_e",
                    "Lambda",
                    "G",
                    "ell_P",
                    "sum_m_nu",
                ],
                "status": "names found; 16th is sum m_nu, not R; F still private",
            },
            {
                "layer": 1,
                "name": "must-hit observables (any four-force unifier)",
                "pieces": [
                    "log_alpha_em",
                    "log_alpha_s",
                    "sin2_theta_w",
                    "log_hierarchy",
                    "log_cc_ratio",
                    "log_qcd_ratio",
                    "log_weak_ratio",
                ],
                "status": "cannot drop gravity or vacuum energy and still call it nature",
            },
            {
                "layer": 2,
                "name": "score core from lock-R search",
                "pieces": ["log_cc_ratio", "log_hierarchy"],
                "status": "in every best subset of size ≥ 2",
            },
            {
                "layer": 3,
                "name": "next lock-R pieces",
                "pieces": ["S_coh", "delta_spread", "grad_coh"],
                "status": "raise lock_R to 0.70 at k=5; still not F",
            },
            {
                "layer": 4,
                "name": "not in any best set",
                "pieces": [
                    "A_mean",
                    "f_mean",
                    "phi_scale",
                    "p_cut",
                    "log_alpha_em",
                    "log_alpha_s",
                    "sin2_theta_w",
                    "log_weak_ratio",
                ],
                "status": "do not drill these first",
            },
        ],
        "rebuild": (
            "Names exist. Rebuild is still blocked on a public F from a named "
            "topology to the four couplings plus G_N and Λ. Sitting at measured "
            "values is not that map. Do not glue this table to the reconstructed 4×4."
        ),
        "how_to_get_the_16": [
            "Done: official table is docs/COSMO-SIXTEEN.md / scripts/da_cosmo.py",
            "Still missing: the public producing-map (core equation is trade secret)",
        ],
        "next_da_move": (
            "Run the isolated Cosmo screen (da_cosmo). Do not treat 16/16 as a pass."
        ),
    }


def cmd_cosmos() -> int:
    from da_cosmo import run as cosmo_run

    drill = cosmos_drill()
    out = ROOT / "results" / "da_cosmos_drill.json"
    out.write_text(json.dumps(drill, indent=2))
    payload = cosmo_run()
    print("DA Cosmos drill. Official 16 found. Core equation still private.")
    print("source:", drill["source"])
    print("n_claimed:", drill["n_claimed"], "n_confirmed:", drill["n_confirmed"])
    for layer in drill["layers"]:
        print(f"L{layer['layer']} {layer['name']}: {', '.join(layer['pieces'])}")
        print(f"    {layer['status']}")
    print("16/16 UI:", "fail")
    print("gauge3:", payload["gauge3"]["verdict"], "nature4:", payload["nature4"]["verdict"])
    print("collapsed:", payload["collapsed"])
    print("rebuild:", drill["rebuild"])
    print("next:", drill["next_da_move"])
    append_run(
        "U",
        "Cosmos drill: official 16 from cosmoevolution3d.base44.app",
        "open",
        "names found; F private; 16/16 is not a pass; produce fails for all 16",
    )
    print(f"wrote {out}")
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_sixteen() -> int:
    from da_sixteen import run as sixteen_run

    payload = sixteen_run()
    print("DA 16. The 16th is R (realization). Official Cosmo 16 is a different catalog.")
    print("possibility-from-count:", payload["possibility_from_count"]["why"])
    print(f"baseline R={payload['baseline_R']:.4f}")
    for f in payload["each_one"]:
        d = "" if f["delta"] is None else f"{f['delta']:+.3f}"
        print(f"{f['id']:3d} {f['family']:<16} {f['name']:<18} {f['lock_R']:7.4f} {f['fits']} {d}")
    print("fits that move R:", payload["fits_that_move_R"])
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print("next:", payload["next_da_move"])
    append_run(
        "U",
        "Identify the 16 from gauge / gravity-gauge / teleological / harmonic and test each",
        "open",
        "16th is R; four singletons raise lock-R; affine F to the four couplings fails",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_fingers() -> int:
    from da_fingers import run as fingers_run

    payload = fingers_run()
    print("DA five fingers on:", payload["meta"]["line"])
    print("The 16th is still R. Official Cosmo 16 is a different catalog.")
    for f in payload["tree"]["fingers"]:
        print(f"[{f['verdict']}] {f['name']}: {f['piece']}")
        print(f"    {f['why']}")
        for g in f.get("fingers", []):
            print(f"    [{g['verdict']}] {g['name']}: {g['piece']}")
    print("equal-width flattens χ²_ext:", payload["checks"]["equal_width_flattens_ext"])
    print("16 fates:")
    for rec in payload["candidates"]:
        print(f"  {rec['id']:2d} {rec['category']:<16} {rec['fate']:<22} {rec['name']}")
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print("next:", payload["next_da_move"])
    append_run(
        "U",
        "Five-finger DA on R = exp(-1/2 χ²_ext) exp(-1/2 χ²_int), then each piece, then the 16",
        "open",
        "product passes; implied F fails; vacuum/Planck width artifact; θ is the topological leftover",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_fate() -> int:
    from da_fingers import run as fingers_run

    payload = fingers_run()
    print("DA 16 candidates. Category, general fate, then smaller pieces.")
    print("Same five questions on each: kind / nature / score / produce / next.")
    for rec in payload["candidates"]:
        print(f"{rec['id']:2d} {rec['name']:<16} {rec['category']:<16} {rec['fate']}")
        for f in rec.get("hand", []):
            print(f"    [{f['verdict']}] {f['name']}: {f['why']}")
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    append_run(
        "U",
        "Category and general fate for each of the 16, then DA the smaller pieces",
        "open",
        "kind/nature/score/produce/next on all 16; produce fails; R is output; θ is topological",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_how() -> int:
    from da_how import run as how_run

    payload = how_run()
    print("DA how-it-knew. Cosmos internals not in the repo.")
    enum = payload["enumerator"]
    print(
        f"X_eligible={enum['X_eligible']}  X_must_hit={enum['X_must_hit_nature']}  "
        f"possible_by_count={enum['possible_by_count']}"
    )
    print("able means:", enum["able_means"])
    for step in enum["how_it_could_know"]:
        print(" -", step)
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print("next:", payload["next_da_move"])
    append_run(
        "U",
        "How can a typed catalog say possible and emit X candidates without F?",
        "open",
        "P1 n>k is the only pre-name possible; X is a type-count; P3 explicit F fails",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_flush() -> int:
    from da_flush import run as flush_run

    payload = flush_run()
    print("DA Hilbert flush. Not Quantum Lens. Not a quantum computer.")
    print("flushed:", payload["flushed"])
    for row in payload["best_combination_by_born_mass"]:
        print(f"k={row['k']}  mass={row['born_mass']:.3f}  {row['set']}")
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    append_run(
        "U",
        "Hilbert flush of combinations on the reconstructed 16",
        "open",
        "Born mass on vacuum, Planck, S_c, delta; rewrite of lock-R, not F",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_wave() -> int:
    from da_wave import run as wave_run

    payload = wave_run()
    print("DA waveform rules. Slots A/B/Q untouched. Not Quantum Lens.")
    print("collapsed:", payload["waveform"]["collapsed"], "emerged:", payload["waveform"]["emerged"])
    print("still in superposition:", payload["waveform"]["still_in_superposition"])
    print("falsification (head):")
    for row in payload["falsification"][:6]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    append_run(
        "U",
        "Waveform rules: superposition, entanglement, collapse, falsification",
        "open",
        "not collapsed; unfalsifiable_might_be_true fails; F_exists fails; possible_by_count open",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_game() -> int:
    from da_game import run as game_run

    payload = game_run()
    print("DA game theory. Two games. Neither is F.")
    print("Game R top4:", payload["game_R"]["top4"], "same as flush:", payload["game_R"]["same_four_as_flush"])
    print("narrows past flush:", payload["game_R"]["narrows_past_flush"])
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    append_run(
        "U",
        "Shapley on lock-R vs must-hit unifier game",
        "open",
        "Game R agrees with the flush four; Game U protects must-hits by definition; no F",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_screen() -> int:
    from da_screen import run as screen_run

    payload = screen_run()
    print("DA unification screen. Two levels. Do not glue them.")
    print(f"{'claim':<42} {'kind':<16} {'gauge3':<6} {'nature4'}")
    for c in payload["claims"]:
        print(f"{c['name']:<42} {c['kind']:<16} {c['gauge3_verdict']:<6} {c['nature4_verdict']}")
    print("still open as gauge3:", payload["still_open_as_gauge3"])
    print("passed nature4:", payload["passed_nature4"])
    print(payload["discernment"])
    append_run(
        "U",
        "Screen published unification claims at gauge3 vs nature4",
        "open",
        "nothing passes nature4; MSSM-class stays open as gauge3; SU(5) minimal and SM fail",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_gq() -> int:
    from da_gq import run as gq_run

    payload = gq_run()
    print("DA gravity + quantum. What is coupled? Each pair separate.")
    print(payload["what_is_coupled"])
    for p in payload["pairs"]:
        print(f"  [{p['verdict']}] {p['name']}: {p['coupling']}")
    print("leftovers:", payload["leftovers"])
    append_run(
        "U",
        "Start at gravity + quantum: what is coupled?",
        "open",
        "universal couple is (g,T) via G; vacuum leftover fails as a prediction; gauge3 not coupled to G",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_trackb() -> int:
    from track_b_lemmas import run as trackb_run

    payload = trackb_run()
    print("DA Track B. Lemma identities scored. Regularity stays open.")
    for row in payload["lemmas"]:
        print(f"  [{row['verdict']}] {row['name']}: {row['why']}")
    print("counts", payload["counts"])
    print("domain:", payload["meta"]["domain_verdict"])
    print("next:", payload["next_da_move"])
    for row in payload["lemmas"]:
        append_run("B", row["statement"], row["verdict"], row["name"] + ": " + row["why"])
    append_run(
        "B",
        "classical 3D NS globally regular (domain close)",
        "open",
        "lemma identities held or correctly failed; no closed estimate for X",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_sm() -> int:
    from da_sm import run as sm_run

    payload = sm_run()
    print("DA SM Lagrangian. Started over from L_SM. Cosmo 16 not used.")
    print("realized:", payload["realized_equation"]["equation"])
    print("working couple:", payload["realized_equation"]["working_couple"])
    print("gauge3:", payload["gauge3"], "nature4:", payload["nature4"])
    for b in payload["blocks"]:
        print(f"  [{b['verdict']}] {b['name']}")
    append_run(
        "U",
        "Analyze the SM Lagrangian; realize the two-sided Einstein+T_SM equation",
        "open",
        "L consumes couplings; working couple pass; nature4 fail; A/B/Q untouched",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_separate() -> int:
    from da_separate import run as separate_run

    payload = separate_run()
    print("DA separate. One object, one verdict. No bundles.")
    print("GQ:")
    for r in payload["GQ"]:
        print(f"  [{r['verdict']}] {r['name']}: {r['coupling']}")
    print("PUB:")
    for r in payload["PUB"]:
        print(f"  gauge3={r['gauge3_alone']:<5} nature4={r['nature4_alone']:<5}  {r['name']}")
    print("SIX:")
    for r in payload["SIX"]:
        d = "" if r.get("delta_lock_R") is None else f" Δ={r['delta_lock_R']:+.3f}"
        print(f"  {r['id']:2d} [{r['verdict']}] {r['name']:<16}{d}")
    append_run(
        "U",
        "Run each GQ pair, published claim, reconstructed slot, and Cosmo slot alone",
        "open",
        "isolation did not write F; Cosmo produce fails alone; Einstein passes alone; MSSM open only as gauge3",
    )
    print(f"wrote {payload.get('_wrote')}")
    return 0


def cmd_check(domain: str) -> int:
    domains = list(SLOTS) if domain == "all" else [domain]
    rc = 0
    for d in domains:
        result = run_checker(d)
        print(d, result["verdict"], result["reason"])
        if result.get("tail"):
            print("  " + "\n  ".join(result["tail"]))
        append_run(d, f"automatic check {d}", result["verdict"], result["reason"])
        if result["verdict"] == "fail":
            rc = 1
    return rc


def main() -> int:
    p = argparse.ArgumentParser(description="Domain Architect process machine")
    sub = p.add_subparsers(dest="cmd", required=True)
    sub.add_parser("status")
    sub.add_parser("cosmos", help="official Cosmo 16 plus isolated screen")
    sub.add_parser("sixteen", help="identify 4x4 list, run each, name the 16th")
    sub.add_parser("fingers", help="five-finger DA on the R line, recurse, fate the 16")
    sub.add_parser("fate", help="category + general fate for each of the 16, then smaller pieces")
    sub.add_parser("how", help="how a typed catalog can say possible and emit X")
    sub.add_parser("flush", help="Hilbert flush of which candidates carry the score")
    sub.add_parser("wave", help="waveform rules: superposition, entanglement, collapse, falsification")
    sub.add_parser("game", help="Shapley on the score vs the unifier-claim game")
    sub.add_parser("screen", help="screen published unification claims at gauge3 vs nature4")
    sub.add_parser("gq", help="start at gravity + quantum: what is coupled")
    sub.add_parser("separate", help="run each GQ pair, published claim, and slot alone")
    sub.add_parser("trackb", help="score Track B lemmas; regularity stays open")
    sub.add_parser("sm", help="analyze the SM Lagrangian; realize Einstein+T_SM")
    c = sub.add_parser("check")
    c.add_argument("--domain", default="all", choices=["all", "A", "B", "Q", "U"])
    cl = sub.add_parser("classify")
    cl.add_argument("--claim", required=True)
    lg = sub.add_parser("log")
    lg.add_argument("--domain", required=True, choices=["A", "B", "Q", "U"])
    lg.add_argument("--claim", required=True)
    lg.add_argument("--verdict", required=True, choices=["pass", "fail", "open"])
    lg.add_argument("--note", default="")
    args = p.parse_args()

    if args.cmd == "status":
        return cmd_status()
    if args.cmd == "cosmos":
        return cmd_cosmos()
    if args.cmd == "sixteen":
        return cmd_sixteen()
    if args.cmd == "fingers":
        return cmd_fingers()
    if args.cmd == "fate":
        return cmd_fate()
    if args.cmd == "how":
        return cmd_how()
    if args.cmd == "flush":
        return cmd_flush()
    if args.cmd == "wave":
        return cmd_wave()
    if args.cmd == "game":
        return cmd_game()
    if args.cmd == "screen":
        return cmd_screen()
    if args.cmd == "gq":
        return cmd_gq()
    if args.cmd == "separate":
        return cmd_separate()
    if args.cmd == "trackb":
        return cmd_trackb()
    if args.cmd == "sm":
        return cmd_sm()
    if args.cmd == "check":
        return cmd_check(args.domain)
    if args.cmd == "classify":
        result = classify_claim(args.claim)
        print(json.dumps(result, indent=2))
        return 0
    rec = append_run(args.domain, args.claim, args.verdict, args.note)
    print(json.dumps(rec, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
