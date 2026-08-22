"""Command-line interface for Domain Architect audits."""

from __future__ import annotations

import argparse
import json
import sys

from .audit import audit_expression
from .hb_loop import compare_reports
from .registry import EquationRegistry
from .schema import CANONICAL_SFE_STATUS, PRODUCT_DESCRIPTION


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
        help="optional second equation for --compare",
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
    args = parser.parse_args(argv)

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
        parser.error("expression is required unless --registry is set")

    report = audit_expression(args.expression)
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
