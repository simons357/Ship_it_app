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
        "checker": ["python3", "-m", "unittest", "tests.test_unifier_exercise", "tests.test_unifier_combo", "-v"],
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
    if re.search(r"\bunifier\b|realization|\block_r\b|cosmos|hierarchy|vacuum", text):
        return {"domain": "U", "verdict": "open", "reason": "looks like score U; run check U"}
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
