"""Command-line interface for Domain Architect audits."""

from __future__ import annotations

import argparse
import json
import sys

from .audit import audit_expression
from .process_console import ProcessConsole
from .registry import EquationRegistry
from .schema import CANONICAL_SFE_STATUS, PRODUCT_DESCRIPTION, SCHEMA_VERSION


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
        "--console",
        action="store_true",
        help="emit Process Console v5 snapshot (science-outcome independent)",
    )
    args = parser.parse_args(argv)

    if args.console:
        snap = ProcessConsole().snapshot()
        if args.json:
            json.dump(snap.to_dict(), sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(f"Process Console schema {SCHEMA_VERSION}")
            print(f"F-X2 complete: {snap.fx2.get('complete')}")
            for view in snap.runs:
                print(
                    f"  {view.run.run_id}  {view.process_status.value.upper()}  "
                    f"promotion={view.promotion.value}"
                )
                for check in view.failed_checks:
                    print(f"    failed {check['check_id']}: {check['detail']}")
            print(
                "Live TG: r^2="
                f"{snap.live_taylor_green['r_squared']}  "
                f"T_c/(ν D_s)={snap.live_taylor_green['T_c_over_nu_D_s']}"
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
