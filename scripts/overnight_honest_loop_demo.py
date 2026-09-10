#!/usr/bin/env python3
"""Overnight demo: amazing but honest Domain Architect full loop.

Shows:
  auto role-assign → reconstruct → compare → tuning export → incompleteness
  (+ drill-down / recompose, dual-SFE compare)

Non-claims (enforced by tone and software):
  - not a Theory of Everything
  - not a Clay / Millennium regularity proof
  - does not bake λ_min(Q_N)>-1/2 into NS
  - P is not assumed prime
  - Canonical SFE status remains unresolved
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from domain_architect.audit import audit_expression
from domain_architect.hb_loop import compare_reports
from domain_architect.incompleteness import sketch_from_roles
from domain_architect.schema import CANONICAL_SFE_STATUS
from domain_architect.sfe_compare import compare_sfe_pair


NS_FULL = "partial_t omega = (omega * nabla) u + nu Delta omega"
NS_THIN = "partial_t omega = nu Delta omega"  # missing advection term
GRAVITY = "nabla^2 Phi = 4 pi G rho"


def _section(title: str) -> None:
    print()
    print("=" * 72)
    print(title)
    print("=" * 72)


def main() -> int:
    print("Domain Architect — overnight honest loop demo")
    print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}")
    print(
        "Structural translator only. No ToE, no Clay, no prime-P, "
        "no λ_min bake-in."
    )

    _section("1. AUTO — classical NS-B role assign")
    ns = audit_expression(NS_FULL)
    print(f"Input: {NS_FULL}")
    print(f"Book: {ns.hb_map and ns.hb_map.get('domain_book')}")
    for item in ns.role_assignments:
        print(
            f"  {item.get('symbol')}: {item.get('candidate_role')} "
            f"[{item.get('subtype')}]"
        )

    _section("2. RECONSTRUCT — inventory closure (not a PDE solve)")
    recon = ns.reconstruction or {}
    print(f"passed={recon.get('passed')} kind={recon.get('kind')}")
    print(recon.get("statement"))
    print(f"recomposed: {recon.get('recomposed_summary')}")

    _section("3. COMPARE — NS-B vs gravity-poisson (unlike books)")
    grav = audit_expression(GRAVITY)
    cmp = compare_reports(ns, grav)
    print(cmp.narrative())

    _section("4. TUNING EXPORT — control variables for bridge apps")
    te = ns.tuning_export or {}
    print(f"domain_book={te.get('domain_book')} auto_assigned={te.get('auto_assigned')}")
    for c in te.get("controls") or []:
        if c.get("status") in {"free", "protocol_selector"}:
            print(f"  - {c.get('name')} [{c.get('status')}]: {c.get('why')}")

    _section("5. INCOMPLETENESS — thin NS missing advection")
    thin = audit_expression(NS_THIN)
    inc = thin.incompleteness or {}
    print(f"Input: {NS_THIN}")
    print(f"complete={inc.get('is_complete')}")
    print(f"missing_terms={inc.get('missing_terms')}")
    for c in inc.get("candidates") or []:
        print(f"  candidate [{c.get('kind')}/{c.get('confidence')}]: {c.get('proposal')}")
    print(inc.get("statement"))

    _section("5b. ROLES-IN → candidate sketch")
    sketch = sketch_from_roles(
        ["admissibility", "interaction", "state", "scale_response", "realized_output"],
        book="NS-B",
    )
    print(sketch.equation_sketch)
    print(sketch.statement)

    _section("6. DRILL-DOWN + RECOMPOSE — H → (H1,H2,…)")
    dec = ns.decomposition or {}
    print(
        f"book={dec.get('domain_book')} depth={dec.get('depth')} "
        f"terminals={dec.get('terminal_count')} "
        f"recompose_ok={dec.get('all_recompose_ok')}"
    )
    print(dec.get("statement"))
    root = (dec.get("root") or {})
    for child in root.get("children") or []:
        print(
            f"  {child.get('module_id')}: {child.get('label')} "
            f"({child.get('kind')}) recompose={child.get('recompose_ok')}"
        )
        for grand in child.get("children") or []:
            stop = grand.get("stop_reason") or ""
            print(f"    {grand.get('module_id')}: {grand.get('label')} [{stop}]")

    _section("7. PUT SFE IN TWICE — dual historical candidates")
    dual = compare_sfe_pair("SFE-H001", "SFE-H002", include_audits=False)
    print(dual.narrative())

    _section("8. MACHINE SUMMARY (JSON excerpt)")
    summary = {
        "canonical_sfe_status": CANONICAL_SFE_STATUS,
        "ns_book": ns.hb_map.get("domain_book") if ns.hb_map else None,
        "reconstruction_passed": recon.get("passed"),
        "tuning_controls": [
            c.get("name")
            for c in (te.get("controls") or [])
            if c.get("status") in {"free", "protocol_selector"}
        ],
        "thin_missing_terms": inc.get("missing_terms"),
        "decompose_recompose_ok": dec.get("all_recompose_ok"),
        "sfe_dual_relation": dual.registry_relation,
        "non_claims": [
            "not_ToE",
            "not_Clay",
            "no_lambda_min_bake_in",
            "P_not_prime",
            "SFE_unresolved",
        ],
    }
    print(json.dumps(summary, indent=2))

    out = Path("/opt/cursor/artifacts/overnight_honest_loop_summary.json")
    try:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(summary, indent=2) + "\n")
        print(f"\nWrote {out}")
    except OSError as exc:
        print(f"\n(artifact write skipped: {exc})", file=sys.stderr)

    print("\nDone. Amazing but honest — structural translator, not a unifier.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
