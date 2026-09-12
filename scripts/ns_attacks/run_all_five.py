#!/usr/bin/env python3
"""Launch all five NS attack lanes (optionally in parallel subprocesses).

Numerics ≠ proof. Probes are subordinate to analysis — light sanity/kill
checks only, not an HPC arms race. See docs/ns-review/RESEARCH-POLICY.md.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    ("attack1", ROOT / "attack1_covariance.py"),
    ("attack2", ROOT / "attack2_triad_k0_cstar.py"),
    ("attack3", ROOT / "attack3_bony_hh_l.py"),
    ("attack4", ROOT / "attack4_stokes.py"),
    ("attack5", ROOT / "attack5_route2_kill.py"),
]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--outdir", type=str, required=True)
    ap.add_argument("--serial", action="store_true")
    args = ap.parse_args()
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    procs = []
    t0 = time.time()
    for name, script in SCRIPTS:
        out_json = outdir / f"{name}.json"
        log = outdir / f"{name}.log"
        cmd = [sys.executable, str(script), "--out", str(out_json)]
        if name == "attack1":
            cmd += ["--n-random", "200"]
        if name == "attack5":
            cmd += ["--n-random", "500"]
        print(f"launch {name}: {' '.join(cmd)}", flush=True)
        if args.serial:
            with log.open("w") as lf:
                subprocess.run(cmd, stdout=lf, stderr=subprocess.STDOUT, check=False)
            procs.append((name, None, log, out_json))
        else:
            lf = log.open("w")
            p = subprocess.Popen(cmd, stdout=lf, stderr=subprocess.STDOUT)
            procs.append((name, p, log, out_json, lf))

    summaries = {}
    if not args.serial:
        for name, p, log, out_json, lf in procs:
            rc = p.wait()
            lf.close()
            print(f"{name} exit={rc}", flush=True)
            if out_json.exists():
                summaries[name] = json.loads(out_json.read_text())
            else:
                summaries[name] = {"error": f"missing json, rc={rc}", "log": str(log)}
    else:
        for name, _, log, out_json in procs:
            if out_json.exists():
                summaries[name] = json.loads(out_json.read_text())

    merged = {
        "elapsed_sec": time.time() - t0,
        "ns_solved": False,
        "lanes": summaries,
        "headline": {
            "attack1": summaries.get("attack1", {}).get("verdict"),
            "attack2": summaries.get("attack2", {}).get("verdict"),
            "attack3": summaries.get("attack3", {}).get("verdict"),
            "attack4": summaries.get("attack4", {}).get("verdict"),
            "attack5": summaries.get("attack5", {}).get("verdict"),
            "LemmaStar_C0_killed": summaries.get("attack5", {}).get("LemmaStar_C0_killed"),
        },
    }
    merged_path = outdir / "SYNTHESIS_RUNTIME.json"
    merged_path.write_text(json.dumps(merged, indent=2))
    print(json.dumps(merged["headline"], indent=2), flush=True)
    print(f"wrote {merged_path}", flush=True)


if __name__ == "__main__":
    main()
