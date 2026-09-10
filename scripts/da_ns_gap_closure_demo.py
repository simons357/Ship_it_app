#!/usr/bin/env python3
"""End-to-end DA diagnosis: where the NS/SND/Theorem-H weld breaks → how to close it.

Prints Broken weld → Suggested closure lines. Refuses unconditional Clay glue.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
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
from domain_architect.schema import CANONICAL_SFE_STATUS


def _section(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def main() -> int:
    print("Domain Architect — NS/SND gap closure demo")
    print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}")
    print("Closer mode: Broken weld → Suggested closure (not status-only OPEN).")

    _section("1. Classical NS-B (honest book — no Clay refuse)")
    gap_ns = diagnose_gap(EXPR_NS_B)
    print(gap_ns.narrative())

    _section("2. SND hypothesis KEEP framing")
    print(diagnose_gap(EXPR_SND_HYP).narrative())

    _section("3. Theorem H as written (X≤M) — incomplete keystone")
    print(diagnose_gap(EXPR_THM_H_WRITTEN).narrative())

    _section("4. Illegal glue: Theorem H (X≤M) ⇒ Clay B")
    glue = diagnose_gap(EXPR_CLAY_GLUE)
    print(glue.narrative())
    assert glue.refuses_unconditional_clay

    _section("5. Dual compare SND-C vs SND-U")
    dual = snd_c_vs_snd_u_compare()
    print(dual["narrative"])
    print(f"Relation: {dual['relation']}")
    print(f"Why: {dual['why_incompatible']}")

    _section("6. Compare HB maps: NS-B vs SND-augmented claim vs Q1")
    left = audit_expression(EXPR_NS_B)
    mid = audit_expression(EXPR_SND_C)
    right = audit_expression(EXPR_Q1)
    print("--- NS-B vs SND-C ---")
    print(compare_reports(left, mid).narrative())
    print()
    print("--- NS-B vs Q1 claim ---")
    print(compare_reports(left, right).narrative())

    _section("7. Registry: INCOMPATIBLE welds force honest routing")
    reg = EquationRegistry.load_default()
    for c in reg.conflicts:
        if {c.left_id, c.right_id} & {
            "SND-C001",
            "SND-U001",
            "CLAY-B001",
            "THM-H001",
        }:
            if c.relation == "INCOMPATIBLE":
                print(f"  {c.left_id} ≁ {c.right_id}: {c.evidence[:100]}…")

    _section("8. Ranked top-5 closure moves (tractable first)")
    for m in ranked_top_closures(5):
        print(f"  {m.tractability_rank}. [{m.kind}] {m.headline()}")
        print(f"     {m.patch_sketch[:110]}…")

    _section("9. Incompleteness JSON snippet on glue claim")
    report = audit_expression(EXPR_CLAY_GLUE)
    welds = [
        c
        for c in (report.incompleteness or {}).get("candidates") or []
        if c.get("kind") == "gap_closure_weld"
    ]
    print(json.dumps(welds[:3], indent=2))

    print()
    print("Demo complete. Door to shut: remove X≤M from the keystone or stop claiming Clay.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
