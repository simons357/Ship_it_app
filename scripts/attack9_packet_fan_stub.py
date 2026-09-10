#!/usr/bin/env python3
"""Attack 9 — Coherent Packet/Fan Test stub (protocol + refusals only).

Documents required controls and the γ decision rule.
Does NOT claim Lemma★ from samples. NS NOT SOLVED. No SFE.

See docs/ns-review/ATTACK-9-COHERENT-PACKET-FAN.md.
"""

from __future__ import annotations

import argparse
import json
from typing import Any

from domain_architect.lemma_star import analyze_lemma_star, refuse_proved_lemma_star
from domain_architect.rstar_quantities import (
    EXACT_R_STAR_FORMULA,
    KILL_LANE_STATUS,
    check_rstar_invariances,
    refuse_kill_lane_closed,
    warn_rstar_comparison_without_attestation,
)

CONTROLS: tuple[str, ...] = (
    "R_star(a*v) = R_star(v)",
    "R_star(v(n·)) = R_star(v)",
    "sum_k T_k = 0",
    "direct triad summation agrees with dealiased FFT evaluation",
    "report TOTAL T_c (not only favorable HH→L portion)",
    "fit growth against packet size m",
)

DECISION_RULE = {
    "fit": "R_star(v_m) ~ m^gamma",
    "gamma_gt_0_sustained": "counterexample route (falsification advancing)",
    "flat": (
        "next analytic target: square-summation or orthogonality mechanism "
        "preventing coherent triad accumulation"
    ),
    "proves_lemma_star": False,
}


def attack9_protocol(*, claim_star_from_samples: bool = False) -> dict[str, Any]:
    """Return Attack 9 protocol bundle; refuse ★ greening from samples."""
    inv = check_rstar_invariances()
    kill = refuse_kill_lane_closed("the kill lane is closed")
    compare = warn_rstar_comparison_without_attestation(
        ["0.065", "0.073", "1.93e-3"],
        each_exact_rstar_attested=False,
    )
    green = refuse_proved_lemma_star(
        "Attack 9 samples prove Lemma★; kill lane closed; greening"
    )
    analysis = analyze_lemma_star("Attack 9 Coherent Packet/Fan via R_star")

    out: dict[str, Any] = {
        "name": "Attack 9 — Coherent Packet/Fan Test",
        "doc": "docs/ns-review/ATTACK-9-COHERENT-PACKET-FAN.md",
        "exact_formula": EXACT_R_STAR_FORMULA,
        "objective": (
            "Maximize complete R_star over conjugate-closed packets P,Q,R "
            "with R=P+Q; increase packet cardinality m; optimize amplitudes, "
            "phases, divergence-free polarizations."
        ),
        "controls": list(CONTROLS),
        "decision_rule": dict(DECISION_RULE),
        "kill_lane": dict(KILL_LANE_STATUS),
        "invariances_check": inv,
        "refuse_kill_lane_closed": kill,
        "refuse_legacy_comparison": compare,
        "refuse_star_from_samples": green,
        "lemma_star_status": analysis.status,
        "ns_solved": False,
        "sfe": False,
        "run_status": "PROTOCOL_STUB_ONLY — not an executed sweep",
        "jonathan_action": "none (or only: run Attack 9 when ready)",
    }

    if claim_star_from_samples:
        out["refused"] = True
        out["message"] = (
            "REFUSE: Attack 9 samples do not establish Lemma★. "
            "Kill lane LIVE. NS NOT SOLVED."
        )
    else:
        out["refused"] = False
        out["message"] = (
            "Protocol ready. Run packet/fan sweep under controls; report γ. "
            "Do not claim ★ from samples."
        )
    return out


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--claim-star",
        action="store_true",
        help="Demonstrate refusal of claiming ★ from Attack 9 samples",
    )
    p.add_argument("--json", action="store_true", help="Print JSON only")
    args = p.parse_args(argv)
    rep = attack9_protocol(claim_star_from_samples=args.claim_star)
    if args.json:
        print(json.dumps(rep, indent=2, sort_keys=True))
    else:
        print("Attack 9 — Coherent Packet/Fan Test (stub)")
        print(f"Exact R_★: {rep['exact_formula']}")
        print(f"Kill lane: {rep['kill_lane']['status']} "
              f"(falsification={rep['kill_lane']['falsification']}, "
              f"proof={rep['kill_lane']['proof']})")
        print("Controls:")
        for c in CONTROLS:
            print(f"  • {c}")
        print(f"Decision: {DECISION_RULE['fit']}")
        print(f"  γ>0 sustained → {DECISION_RULE['gamma_gt_0_sustained']}")
        print(f"  flat → {DECISION_RULE['flat']}")
        print(f"Invariances OK: {rep['invariances_check']['ok']}")
        print(f"Refuse kill-lane-closed: {rep['refuse_kill_lane_closed']['refused']}")
        print(f"Refuse legacy R compare: {rep['refuse_legacy_comparison']['refused']}")
        print(f"Refuse ★ from samples: {rep['refuse_star_from_samples']['refused']}")
        print(f"NS solved: {rep['ns_solved']}")
        print(rep["message"])
        print(f"Jonathan action: {rep['jonathan_action']}")
    return 2 if (args.claim_star and rep.get("refused")) else 0


if __name__ == "__main__":
    raise SystemExit(main())
