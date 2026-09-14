"""Command-line interface for Domain Architect audits."""

from __future__ import annotations

import argparse
import json
import sys

from .audit import audit_expression
from .hilbert_polya import (
    audit_candidate,
    default_program_audit,
    list_candidate_ids,
)
from .breakdown_children import run_breakdown_children
from .ns_model import render_ns_model, run_ns_model
from .millennium_overlap import (
    list_pair_ids,
    millennium_look_narrative,
    run_default_pairs,
    run_equation_pair,
)
from .polya_probe import run_polya_probe
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
        "--hilbert-polya",
        action="store_true",
        help=(
            "audit the Hilbert–Pólya program as a Functional Role Analysis "
            "instance (does not prove RH)"
        ),
    )
    parser.add_argument(
        "--candidate",
        default="",
        help=(
            "Hilbert–Pólya candidate id for --hilbert-polya "
            "(unspecified, target-identity, diagonal-zeros, berry-keating, "
            "connes, montgomery-gue, weil-explicit)"
        ),
    )
    parser.add_argument(
        "--polya-probe",
        action="store_true",
        help=(
            "ingest the full Pólya / Hilbert–Pólya briefing and expand E; "
            "does not prove RH"
        ),
    )
    parser.add_argument(
        "--millennium-look",
        action="store_true",
        help=(
            "look at parts of Pólya against open Clay prizes; "
            "does not unify them and does not prove RH or NS"
        ),
    )
    parser.add_argument(
        "--pair",
        nargs="?",
        const="both",
        default="",
        help=(
            "run a look-pair through the auditor: green-biot, phi, or both "
            "(default if flag is present with no name)"
        ),
    )
    parser.add_argument(
        "--breakdown-children",
        action="store_true",
        help=(
            "split parent breakdowns into children, run parseable ones, "
            "and list path guidance from refusals"
        ),
    )
    parser.add_argument(
        "--ns-model",
        action="store_true",
        help=(
            "enter the kept NS model (axisymmetric-with-swirl Φ-renorm) "
            "into Domain Architect and report what happens; Clay NS not claimed"
        ),
    )
    args = parser.parse_args(argv)

    if args.ns_model:
        report = run_ns_model()
        if args.json:
            json.dump(report.to_dict(), sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print(render_ns_model(report))
            print()
            print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
        return 0

    if args.breakdown_children:
        text = run_breakdown_children()
        if args.json:
            from .breakdown_children import breakdown_children, path_guides

            json.dump(
                {
                    "children": [c.to_dict() for c in breakdown_children()],
                    "path_guides": path_guides(),
                    "narrative": text,
                },
                sys.stdout,
                indent=2,
                default=str,
            )
            sys.stdout.write("\n")
        else:
            print(text)
            print()
            print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
        return 0

    if args.pair:
        try:
            text = (
                run_default_pairs()
                if args.pair == "both"
                else run_equation_pair(args.pair)
            )
        except KeyError as exc:
            parser.error(str(exc) + f" known={list_pair_ids() + ['both']}")
        if args.json:
            json.dump({"pair": args.pair, "narrative": text}, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(text)
            print()
            print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
        return 0

    if args.millennium_look:
        text = millennium_look_narrative()
        if args.json:
            from .millennium_overlap import overlap_looks, closest_rhymes

            json.dump(
                {
                    "looks": [look.to_dict() for look in overlap_looks()],
                    "rhymes": closest_rhymes(),
                },
                sys.stdout,
                indent=2,
            )
            sys.stdout.write("\n")
        else:
            print(text)
            print()
            print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
        return 0

    if args.polya_probe:
        probe = run_polya_probe()
        if args.json:
            json.dump(probe.to_dict(), sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print(probe.narrative())
            print()
            print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
        return 0

    if args.hilbert_polya:
        if args.candidate:
            try:
                hp = audit_candidate(args.candidate)
            except KeyError as exc:
                parser.error(str(exc) + f" known={list_candidate_ids()}")
        else:
            hp = default_program_audit()
        if args.json:
            json.dump(hp.to_dict(), sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        else:
            print(hp.narrative())
            print()
            print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
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
