"""Command-line interface for Domain Architect audits."""

from __future__ import annotations

import argparse
import json
import sys

from .audit import audit_expression
from .clip_splice import clip_splice, format_clip_splice
from .desk import compare_shape, format_proceed, proceed_report, refuse_splice
from .ns_chain import format_ns_chain, ns_chain
from .ns_geometry import format_ns_geometry, ns_geometry
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
    parser.add_argument(
        "--shape-compare",
        nargs=2,
        metavar=("LEFT", "RIGHT"),
        help="compare two library objects by shape, then texture (e.g. J/X LAMBDA-MIN)",
    )
    parser.add_argument(
        "--clip",
        nargs=2,
        metavar=("LEFT", "RIGHT"),
        help="clip excess terms, ID the remainder, and measure it",
    )
    parser.add_argument(
        "--chain",
        metavar="BOOK",
        help="print a proof chain as shapes (B or NS)",
    )
    parser.add_argument(
        "--geometry",
        metavar="BOOK",
        help="print geometric analysis (B or NS): tube, shells, strain, swirl",
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

    if args.shape_compare:
        compared = compare_shape(args.shape_compare[0], args.shape_compare[1])
        if args.json:
            json.dump(compared.to_dict(), sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(f"{compared.verdict}: {compared.left} vs {compared.right}")
            print(f"  {compared.left} [{compared.left_book}] shape={compared.left_shape}")
            print(f"      texture: {compared.left_texture}")
            print(f"  {compared.right} [{compared.right_book}] shape={compared.right_shape}")
            print(f"      texture: {compared.right_texture}")
            print(compared.reason)
        return 0

    if args.clip:
        clipped = clip_splice(args.clip[0], args.clip[1])
        if args.json:
            json.dump(clipped.to_dict(), sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_clip_splice(clipped))
        return 0

    if args.chain:
        book = args.chain.strip().upper()
        if book not in {"B", "NS", "TRACKB", "NAVIERSTOKES", "NAVIER-STOKES"}:
            print(
                "Only Track B / NS is wired. RH is a different book.",
                file=sys.stderr,
            )
            return 2
        payload = ns_chain()
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_ns_chain(payload))
        return 0

    if args.geometry:
        book = args.geometry.strip().upper()
        if book not in {"B", "NS", "TRACKB", "NAVIERSTOKES", "NAVIER-STOKES"}:
            print(
                "Only Track B / NS geometry is wired. RH is a different book.",
                file=sys.stderr,
            )
            return 2
        payload = ns_geometry()
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_ns_geometry(payload))
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
        parser.error(
            "expression is required unless --registry, --proceed, "
            "--refuse-splice, --shape-compare, --clip, --chain, or --geometry is set"
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
