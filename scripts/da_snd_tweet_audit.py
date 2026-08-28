#!/usr/bin/env python3
"""DA audit for Jonathan Simons June 2026 SND tweet equations.

Writes JSON/text artifacts to /opt/cursor/artifacts/da-snd-equations/
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = Path("/opt/cursor/artifacts/da-snd-equations")
ART.mkdir(parents=True, exist_ok=True)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from domain_architect.audit import audit_expression
from domain_architect.gap_closure import diagnose_gap, snd_c_vs_snd_u_compare
from domain_architect.hb_loop import build_hb_map, compare_reports
from domain_architect.registry import EquationRegistry
from domain_architect.snd_claims import anatomize_claim

TWEET_EXPRESSIONS = {
    "center": (
        "inf_{t>=0} lambda_min(tilde_H_N[u(t)]) / "
        "lambda_max(tilde_H_N[u(t)]) > -1/2"
    ),
    "snd_jx": "inf_t J(t)/X(t) >= c_* > 0",
    "thm_d": "Clay Statement B <=> [SND]",
    "thm_h": (
        "Theorem H (SND-C): (X>=delta_*, X<=M, rho<=rho_0) => "
        "|Pi_{j*}| <= C_*(nu,delta_*,M,rho_0,C_S)"
    ),
    "bypass": "Bypass Lemma: tilde_H_N norm bound with 5× safety margin on T^3",
    "ring": (
        "Ring Lemma: Borromean triadic cancellation on interlocked "
        "Littlewood-Paley shells"
    ),
    "main": "Main result: global regularity on T^3 — no finite-time blowup (proved)",
    "ns_b": "partial_t u + (u·nabla)u = -nabla p + nu Delta u; div u = 0",
}

COMPARE_PAIRS = [
    ("center vs snd_jx", "center", "snd_jx"),
    ("thm_h vs snd_jx", "thm_h", "snd_jx"),
    ("thm_d vs main", "thm_d", "main"),
    ("ring vs snd_jx", "ring", "snd_jx"),
    ("ns_b vs snd_jx", "ns_b", "snd_jx"),
]

GAP_KEYS = ["thm_d", "main", "thm_h", "bypass", "center", "snd_jx", "ring"]

CLAIMS = [
    "Clay Statement B <=> [SND]",
    "Main result: global regularity on T^3 proved",
    "Theorem H (SND-C) under X<=M",
    "inf_t J(t)/X(t) >= c_* unconditional SND for all H^1 data",
]


def _write(name: str, payload: object) -> None:
    path = ART / name
    if isinstance(payload, str):
        path.write_text(payload, encoding="utf-8")
    else:
        path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    print(f"  wrote {path}")


def main() -> int:
    print("DA SND tweet audit run")
    print(f"Artifacts → {ART}")

    reg = EquationRegistry.load_default()
    _write("registry-tweet-snippet.json", {
        k: reg.equations[k].to_dict()
        for k in reg.equations
        if k.startswith("SND-TWEET-")
    })

    audits = {}
    hb_maps = {}
    for label, expr in TWEET_EXPRESSIONS.items():
        report = audit_expression(expr)
        audits[label] = report.to_dict()
        hb_maps[label] = build_hb_map(report).to_dict()
        (ART / f"audit_{label}.txt").write_text(
            subprocess.run(
                ["python3", "-m", "domain_architect", expr],
                cwd=ROOT,
                capture_output=True,
                text=True,
            ).stdout,
            encoding="utf-8",
        )
    _write("audits-all.json", audits)
    _write("hb-maps-all.json", hb_maps)

    compares = {}
    for label, left_key, right_key in COMPARE_PAIRS:
        cmp = compare_reports(
            audit_expression(TWEET_EXPRESSIONS[left_key]),
            audit_expression(TWEET_EXPRESSIONS[right_key]),
        )
        compares[label] = cmp.to_dict()
    _write("compares-all.json", compares)

    gaps = {}
    for key in GAP_KEYS:
        gap = diagnose_gap(TWEET_EXPRESSIONS[key])
        gaps[key] = gap.to_dict()
    _write("gap-closure-all.json", gaps)

    claims = {c[:40]: anatomize_claim(c).to_dict() for c in CLAIMS}
    _write("snd-claims-all.json", claims)
    _write("snd-dual.json", snd_c_vs_snd_u_compare())

    summary = {
        "tweet_center_book": hb_maps["center"]["domain_book"],
        "tweet_snd_jx_book": hb_maps["snd_jx"]["domain_book"],
        "thm_d_refuses": gaps["thm_d"]["refuses_unconditional_clay"],
        "main_refuses": gaps["main"]["refuses_unconditional_clay"],
        "thm_h_warn_only": not gaps["thm_h"]["refuses_unconditional_clay"],
        "center_vs_snd_jx_shared_roles": compares["center vs snd_jx"]["shared_roles"],
        "tweet_thm_d_disposition": reg.equations["SND-TWEET-THM-D001"].audit_disposition,
        "tweet_main_disposition": reg.equations["SND-TWEET-MAIN001"].audit_disposition,
        "clay_b_retire": reg.equations["CLAY-B001"].audit_disposition,
    }
    _write("summary-flags.json", summary)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
