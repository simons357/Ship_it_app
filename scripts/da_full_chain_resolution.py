#!/usr/bin/env python3
"""Exhaustive DA audit/compare for full NS/SND/ARCHON/Theorem-H chain.

Writes JSON artifacts to /opt/cursor/artifacts/da-full-resolution/
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = Path("/opt/cursor/artifacts/da-full-resolution")
ART.mkdir(parents=True, exist_ok=True)

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from domain_architect.audit import audit_expression
from domain_architect.gap_closure import (
    EXPR_CLAY_GLUE,
    EXPR_NS_B,
    EXPR_Q1,
    EXPR_SND_C,
    EXPR_SND_HYP,
    EXPR_SND_U,
    EXPR_THM_H_WRITTEN,
    diagnose_gap,
    ranked_top_closures,
    snd_c_vs_snd_u_compare,
)
from domain_architect.hb_loop import compare_reports
from domain_architect.registry import EquationRegistry
from domain_architect.sfe_compare import compare_sfe_pair, list_sfe_candidates


# Claim-chain expressions to audit
AUDIT_EXPRESSIONS = {
    "NS-B-vorticity": EXPR_NS_B,
    "NS-B-velocity": "partial_t u + (u·nabla)u = -grad p + nu Delta u, div u = 0",
    "SND-HYP": EXPR_SND_HYP,
    "SND-C": EXPR_SND_C,
    "SND-U-claim": EXPR_SND_U,
    "Theorem-H-written": EXPR_THM_H_WRITTEN,
    "Clay-glue": EXPR_CLAY_GLUE,
    "Q1-hyperdissipative": EXPR_Q1,
    "Ring-Lemma": (
        "Ring Lemma: on shell S_j*, direction of omega Lipschitz on "
        "E_c={|omega|>=c 2^j* ||u||_L2}"
    ),
    "BVB-Ec-bridge": (
        "BVB on E_c: weighted integral bound linking vorticity direction "
        "to shell flux (band-limited)"
    ),
    "Phi-swirl": "Gamma=r u_theta, Phi_swirl=Gamma/r^2, r^{-4} dz(Gamma^2)=dz(Phi^2)",
    "cstar-arithmetic": "c_* = 6/pi^2 = zeta(2)^{-1} as SND floor for NS",
    "bootstrap-M-slot": (
        "Bootstrap lemma OPEN: M = M(||u0||_{H^1}) s.t. X(t)<=M without "
        "circular input to Theorem H SND-C"
    ),
    "Ring-rescue-Clay": (
        "Ring Lemma + BVB on E_c implies Clay Statement B resolved"
    ),
    "Q1-Clay-glue": "Q1 epsilon->0; Clay Statement B resolved via SND",
}

COMPARE_PAIRS = [
    ("NS-B vs SND-U", EXPR_NS_B, EXPR_SND_U),
    ("NS-B vs SND-C", EXPR_NS_B, EXPR_SND_C),
    ("NS-B vs SND-HYP", EXPR_NS_B, EXPR_SND_HYP),
    ("NS-B vs Q1", EXPR_NS_B, EXPR_Q1),
    ("SND-C vs SND-U", EXPR_SND_C, EXPR_SND_U),
    ("SND-C vs SND-HYP", EXPR_SND_C, EXPR_SND_HYP),
    ("SND-C vs Clay-glue", EXPR_SND_C, EXPR_CLAY_GLUE),
    ("Q1 vs SND-U", EXPR_Q1, EXPR_SND_U),
    ("Ring+BVB vs Clay", AUDIT_EXPRESSIONS["Ring-Lemma"], EXPR_CLAY_GLUE),
    ("Bootstrap vs SND-C", AUDIT_EXPRESSIONS["bootstrap-M-slot"], EXPR_SND_C),
]

GAP_CLOSURE_VARIANTS = [
    EXPR_CLAY_GLUE,
    EXPR_SND_U,
    EXPR_THM_H_WRITTEN,
    EXPR_SND_C,
    EXPR_Q1,
    "Ring Lemma + BVB implies unconditional regularity and Clay B",
    "c_*=6/pi^2 is the fluids SND threshold proving Clay Statement B",
    AUDIT_EXPRESSIONS["bootstrap-M-slot"],
    "SFE derives Navier-Stokes global regularity",
]

KEY_INCOMPLETENESS = [
    EXPR_NS_B,
    EXPR_SND_C,
    EXPR_SND_U,
    EXPR_Q1,
    EXPR_CLAY_GLUE,
    AUDIT_EXPRESSIONS["bootstrap-M-slot"],
    AUDIT_EXPRESSIONS["Ring-Lemma"],
]


def _write(name: str, payload: object) -> None:
    path = ART / name
    path.write_text(json.dumps(payload, indent=2, default=str) + "\n", encoding="utf-8")
    print(f"  wrote {path}")


def main() -> int:
    print("DA full-chain resolution run")
    print(f"Artifacts → {ART}")

    # Registry
    reg = EquationRegistry.load_default()
    _write("registry.json", reg.export())

    # Audits
    audits = {}
    for label, expr in AUDIT_EXPRESSIONS.items():
        report = audit_expression(expr)
        audits[label] = report.to_dict()
    _write("audits-all.json", audits)

    # Compares
    compares = {}
    for label, left, right in COMPARE_PAIRS:
        cmp = compare_reports(audit_expression(left), audit_expression(right))
        compares[label] = cmp.to_dict()
    _write("compares-all.json", compares)

    # Gap closure variants
    gaps = {}
    for i, expr in enumerate(GAP_CLOSURE_VARIANTS):
        gap = diagnose_gap(expr)
        gaps[f"variant_{i}"] = gap.to_dict()
    _write("gap-closure-all.json", gaps)

    # SND dual
    _write("snd-dual.json", snd_c_vs_snd_u_compare())

    # Ranked closures (full catalog)
    _write(
        "ranked-closures.json",
        {"closures": [m.to_dict() for m in ranked_top_closures(10)]},
    )

    # Incompleteness + decompose on key expressions
    incompleteness = {}
    decompose = {}
    inc_keys = {
        "NS-B": EXPR_NS_B,
        "SND-C": EXPR_SND_C,
        "SND-U": EXPR_SND_U,
        "Q1": EXPR_Q1,
        "Clay-glue": EXPR_CLAY_GLUE,
        "bootstrap-M": AUDIT_EXPRESSIONS["bootstrap-M-slot"],
        "Ring-Lemma": AUDIT_EXPRESSIONS["Ring-Lemma"],
    }
    for label, expr in inc_keys.items():
        r = audit_expression(expr)
        incompleteness[label] = r.incompleteness
        decompose[label] = r.decomposition
    _write("incompleteness-key.json", incompleteness)
    _write("decompose-key.json", decompose)

    # SFE compare
    sfe = list_sfe_candidates()
    _write("sfe-candidates.json", {"sfe": sfe})
    sfe_pairs = {}
    for a, b in [("SFE-H001", "NS-B001"), ("SFE-H002", "NS-B001"), ("SFE-H001", "SFE-H002")]:
        try:
            sfe_pairs[f"{a}-vs-{b}"] = compare_sfe_pair(a, b).to_dict()
        except Exception as exc:
            sfe_pairs[f"{a}-vs-{b}"] = {"error": str(exc)}
    _write("sfe-compare.json", sfe_pairs)

    # CLI subprocess captures
    cli_cmds = [
        ["python3", "-m", "domain_architect", "--snd-dual", "--json"],
        ["python3", "-m", "domain_architect", "--list-closures", "--json"],
        ["python3", "-m", "domain_architect", "--registry", "--json"],
    ]
    for cmd in cli_cmds:
        out = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, check=False)
        fname = cmd[3].lstrip("-").replace("-", "_") + "_cli.json"
        _write(fname, {"cmd": cmd, "exit": out.returncode, "stdout": out.stdout, "stderr": out.stderr})

    # Summary flags
    summary = {
        "refuses_clay_glue": gaps["variant_0"]["refuses_unconditional_clay"],
        "snd_dual_incompatible": True,
        "clay_b_retire": reg.equations["CLAY-B001"].audit_disposition,
        "snd_u_retire": reg.equations["SND-U001"].audit_disposition,
        "ring_clay_incompatible": any(
            c.left_id == "RING-LEM001" and c.right_id == "CLAY-B001"
            for c in reg.conflicts
        ),
        "sfe_ns_incompatible": any(
            c.left_id.startswith("SFE") and c.right_id == "NS-B001"
            for c in reg.conflicts
        ),
        "bootstrap_slot_present": "BOOT-M001" in reg.equations,
    }
    _write("summary-flags.json", summary)

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
