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
        "note": "docs/UNAUGMENTED-R4-VORTICITY-PLAN.md",
        "checker": None,
        "why_no_pass": "No regularity checker. Only fail forbidden closes or mark open.",
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
    if re.search(r"\bq_?1\b|augmented|ladyzhenskaya|energy identity", text):
        return {"domain": "A", "verdict": "open", "reason": "looks like Track A; run check A"}
    if re.search(r"1/r\^?4|ring|bony|3-conc|spread|tube|vorticity", text):
        return {"domain": "B", "verdict": "open", "reason": "looks like Track B; no pass checker"}
    if re.search(r"bridge|prime.?block|h_n|inverse.?gcd|qtilde|theorem p", text):
        return {"domain": "Q", "verdict": "open", "reason": "looks like Track Q; run check Q"}
    if re.search(
        r"\bunifier\b|realization|\block_r\b|cosmos|hierarchy|vacuum|\b16\b|finger|wave|falsif|superposition|entangle",
        text,
    ):
        return {"domain": "U", "verdict": "open", "reason": "looks like score U / waveform rules; run wave or how"}
    return {"domain": None, "verdict": "open", "reason": "no slot; rephrase into A, B, Q, or U"}


def run_checker(domain: str) -> dict:
    slot = SLOTS[domain]
    if slot["checker"] is None:
        return {"domain": domain, "verdict": "open", "reason": slot["why_no_pass"]}
    proc = subprocess.run(slot["checker"], cwd=ROOT, capture_output=True, text=True)
    verdict = "pass" if proc.returncode == 0 else "fail"
    tail = (proc.stdout + proc.stderr).strip().splitlines()
    return {
        "domain": domain,
        "verdict": verdict,
        "reason": "checker exit %s" % proc.returncode,
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
    """DA drill-down: possibility-with-n, must-hits, score core, missing names."""
    return {
        "slot": "U",
        "cosmos_list_found": False,
        "n_claimed": 16,
        "n_confirmed": None,
        "possibility_claim": {
            "statement": "unification is possible with about 16 variables",
            "verdict": "open",
            "why": (
                "A finite n is a real narrowing IF the names exist and one map F "
                "of those n hits the four couplings. The app saying 'possible' is "
                "not the check. The check is χ²_ext(F(x)) ≤ ε²."
            ),
        },
        "layers": [
            {
                "layer": 0,
                "name": "count only",
                "pieces": ["n ≈ 16 (unconfirmed)"],
                "status": "stuck: names missing",
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
            "Rebuild only after names exist: write F from the surviving pieces "
            "(layer 2, then 3) to the four couplings. If F needs a layer-4 knob, "
            "that knob was misclassified and goes back in. That is the drill."
        ),
        "how_to_get_the_16": [
            "Paste or screenshot the Cosmos variable screen into this repo",
            "Export a JSON/CSV of the knobs from the app",
            "Type the 16 names in one message",
        ],
        "next_da_move": "identify names, then re-run lock-R on those names only",
    }


def cmd_cosmos() -> int:
    drill = cosmos_drill()
    out = ROOT / "results" / "da_cosmos_drill.json"
    out.write_text(json.dumps(drill, indent=2))
    print("DA Cosmos drill. List not found. Possibility claim stays open.")
    print("n_claimed:", drill["n_claimed"], "n_confirmed:", drill["n_confirmed"])
    for layer in drill["layers"]:
        print(f"L{layer['layer']} {layer['name']}: {', '.join(layer['pieces'])}")
        print(f"    {layer['status']}")
    print("rebuild:", drill["rebuild"])
    print("next:", drill["next_da_move"])
    append_run(
        "U",
        "Cosmos drill: is unification possible with ~16 named knobs?",
        "open",
        "names missing; core leftovers are vacuum energy and Planck hierarchy",
    )
    print(f"wrote {out}")
    return 0


def cmd_sixteen() -> int:
    from da_sixteen import run as sixteen_run

    payload = sixteen_run()
    print("DA 16. The 16th is R (realization). Cosmo export still missing.")
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
    print("The 16th is still R. Cosmo export still missing.")
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
    sub.add_parser("cosmos", help="drill the ~16 Cosmos knobs")
    sub.add_parser("sixteen", help="identify 4x4 list, run each, name the 16th")
    sub.add_parser("fingers", help="five-finger DA on the R line, recurse, fate the 16")
    sub.add_parser("fate", help="category + general fate for each of the 16, then smaller pieces")
    sub.add_parser("how", help="how a typed catalog can say possible and emit X")
    sub.add_parser("flush", help="Hilbert flush of which candidates carry the score")
    sub.add_parser("wave", help="waveform rules: superposition, entanglement, collapse, falsification")
    sub.add_parser("game", help="Shapley on the score vs the unifier-claim game")
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
