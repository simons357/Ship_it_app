"""Command-line interface for Domain Architect audits."""

from __future__ import annotations

import argparse
import json
import sys

from .audit import audit_expression
from .desk import format_proceed, proceed_report, refuse_splice
from .registry import EquationRegistry
from .schema import CANONICAL_SFE_STATUS, PRODUCT_DESCRIPTION


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=PRODUCT_DESCRIPTION,
    )
    parser.add_argument("expression", nargs="?", help="equation or term to audit")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument(
        "--registry",
        action="store_true",
        help="print equation provenance and conflict summary",
    )
    parser.add_argument(
        "--proceed",
        action="store_true",
        help="print computing-bench desk: layers, unglued books, next legal moves",
    )
    parser.add_argument(
        "--refuse-splice",
        nargs=2,
        metavar=("SOURCE", "TARGET"),
        help="score a proposed weld (e.g. COSMO B, SEARCH Q, A B)",
    )
    args = parser.parse_args(argv)

    if args.proceed:
        payload = proceed_report()
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_proceed(payload))
        return 0

    if args.refuse_splice:
        decision = refuse_splice(args.refuse_splice[0], args.refuse_splice[1])
        if args.json:
            json.dump(decision.to_dict(), sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(f"{decision.opcode}: {decision.source} → {decision.target}")
            print(decision.reason)
        return 0 if decision.allowed or decision.opcode == "REFUSED" else 1

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

    if not args.expression:
        parser.error(
            "expression is required unless --registry, --proceed, "
            "or --refuse-splice is set"
        )

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
