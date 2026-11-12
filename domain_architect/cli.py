"""Command-line interface for Domain Architect audits."""

from __future__ import annotations

import argparse
import json
import sys

from .audit import audit_expression
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
        "--da-ns-2",
        action="store_true",
        help="print the DA-NS-2 Y-cousin occupation card (OPEN; NS not solved)",
    )
    parser.add_argument(
        "--navigate",
        metavar="BOOK",
        help="print a Domain Architect book card (currently: DA-NS-2)",
    )
    args = parser.parse_args(argv)

    if args.da_ns_2 or (args.navigate and args.navigate.strip().upper().replace(" ", "-") in {"DA-NS-2", "DANS2"}):
        from .da_ns_2 import express_as_proved, navigate_da_ns_2

        card = navigate_da_ns_2()
        if args.json:
            json.dump(card.to_dict(), sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(card.narrative())
            print()
            refusal = express_as_proved()
            print(f"EXPRESS/PROVED refused: {refusal['reason']}")
        return 0

    if args.navigate:
        parser.error(f"unknown book {args.navigate!r}; known: DA-NS-2")

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
        parser.error("expression is required unless --registry, --da-ns-2, or --navigate is set")

    from .da_ns_2 import express_as_proved, looks_like_da_ns_2, navigate_da_ns_2

    if looks_like_da_ns_2(args.expression):
        card = navigate_da_ns_2()
        if args.json:
            json.dump(card.to_dict(), sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(card.narrative())
            print()
            refusal = express_as_proved()
            print(f"EXPRESS/PROVED refused: {refusal['reason']}")
            print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
        return 0

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
