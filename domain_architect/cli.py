"""Command-line interface for Domain Architect audits."""

from __future__ import annotations

import argparse
import json
import sys

from .audit import audit_expression
from .hb_loop import compare_reports
from .incompleteness import sketch_from_roles
from .registry import EquationRegistry
from .schema import CANONICAL_SFE_STATUS, PRODUCT_DESCRIPTION
from .sfe_compare import compare_sfe_pair, list_sfe_candidates


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=PRODUCT_DESCRIPTION,
    )
    parser.add_argument(
        "expression",
        nargs="?",
        help="equation or term to audit",
    )
    parser.add_argument(
        "expression_b",
        nargs="?",
        help="optional second equation for --compare / --sfe-compare",
    )
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument(
        "--registry",
        action="store_true",
        help="print equation provenance and conflict summary",
    )
    parser.add_argument(
        "--compare",
        action="store_true",
        help="side-by-side HB map compare of two expressions",
    )
    parser.add_argument(
        "--sfe-compare",
        action="store_true",
        help=(
            "put SFE in twice: audit two registry ids (e.g. SFE-H001 SFE-H002) "
            "or two expressions; show conflict/compare; SFE stays unresolved"
        ),
    )
    parser.add_argument(
        "--list-sfe",
        action="store_true",
        help="list historical SFE registry candidates",
    )
    parser.add_argument(
        "--tuning-json",
        action="store_true",
        help="emit only the auto tuning/control-variable export as JSON",
    )
    parser.add_argument(
        "--incompleteness-json",
        action="store_true",
        help="emit only the incompleteness / candidate-completion report as JSON",
    )
    parser.add_argument(
        "--decompose-json",
        action="store_true",
        help="emit only the recursive drill-down / recompose tree as JSON",
    )
    parser.add_argument(
        "--roles-sketch",
        action="store_true",
        help=(
            "roles-in → candidate equation sketch; pass comma-separated roles "
            "as the expression argument (e.g. 'admissibility,interaction,state')"
        ),
    )
    args = parser.parse_args(argv)

    if args.list_sfe:
        items = list_sfe_candidates()
        if args.json:
            json.dump({"canonical_sfe_status": CANONICAL_SFE_STATUS, "sfe": items}, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
            print(f"Historical SFE candidates: {len(items)}")
            for item in items:
                print(
                    f"  {item['equation_id']} [{item['disposition']}] "
                    f"{item['expression'][:72]}"
                )
        return 0

    if args.registry:
        registry = EquationRegistry.load_default()
        payload = registry.export()
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(f"Canonical SFE status: {payload['canonical_sfe_status']}")
            print(f"Historical equations: {len(payload['equations'])}")
            print(f"Conflicts: {len(payload['conflicts'])}")
            print(f"Null / counterexample records: {len(payload['nulls'])}")
            for eq in payload["equations"]:
                print(
                    f"  {eq['equation_id']} [{eq['audit_disposition']}] "
                    f"{eq['original_expression']}"
                )
        return 0

    if args.roles_sketch:
        if not args.expression:
            parser.error("--roles-sketch requires a comma-separated role list")
        roles = [r.strip() for r in args.expression.split(",") if r.strip()]
        book = args.expression_b  # optional book override as 2nd positional
        inc = sketch_from_roles(roles, book=book)
        if args.json or args.incompleteness_json:
            json.dump(inc.to_dict(), sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print(inc.narrative())
        return 0

    if args.sfe_compare:
        if not args.expression or not args.expression_b:
            parser.error("--sfe-compare requires two registry ids or expressions")
        dual = compare_sfe_pair(args.expression, args.expression_b)
        if args.json:
            json.dump(dual.to_dict(), sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print(dual.narrative())
        return 0

    if args.compare:
        if not args.expression or not args.expression_b:
            parser.error("--compare requires two expressions")
        left = audit_expression(args.expression)
        right = audit_expression(args.expression_b)
        cmp = compare_reports(left, right)
        if args.json:
            json.dump(
                {
                    "compare": cmp.to_dict(),
                    "left_audit": left.to_dict(),
                    "right_audit": right.to_dict(),
                },
                sys.stdout,
                indent=2,
                default=str,
            )
            sys.stdout.write("\n")
        else:
            print(cmp.narrative())
            print()
            print("--- left reconstruction ---")
            print(left.reconstruction)
            print("--- right reconstruction ---")
            print(right.reconstruction)
            print()
            print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
        return 0

    if not args.expression:
        parser.error("expression is required unless --registry / --list-sfe is set")

    report = audit_expression(args.expression)
    if args.tuning_json:
        json.dump(report.tuning_export or {}, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
        return 0
    if args.incompleteness_json:
        json.dump(report.incompleteness or {}, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
        return 0
    if args.decompose_json:
        json.dump(report.decomposition or {}, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
        return 0
    if args.json:
        json.dump(report.to_dict(), sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
    else:
        print(report.narrative())
        print()
        print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
