"""Command-line interface for Domain Architect audits."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .audit import audit_expression
from .chatvault_bridge import drain_audit, try_enqueue, write_drain
from .chatvault_ingest import DEFAULT_INBOX, ingest_path
from .drain_server import serve
from .site_server import DEFAULT_SITE_PORT, serve_site
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
        "--drain-chatvault",
        action="store_true",
        help="emit a ChatVault export JSON for the audited expression (does not prove it)",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="write JSON to this path (used with --json or --drain-chatvault)",
    )
    parser.add_argument(
        "--drain-server",
        action="store_true",
        help="listen on 127.0.0.1:7847 so ChatVault can pull finished audits",
    )
    parser.add_argument(
        "--site",
        action="store_true",
        help="serve Domain Architect homepage + ChatVault on 127.0.0.1:8765",
    )
    parser.add_argument(
        "--ingest-chatvault",
        metavar="PATH",
        help="ingest a file or directory into the ChatVault repo inbox (JSON sidecars + local media copy)",
    )
    parser.add_argument(
        "--inbox",
        help="inbox directory for --ingest-chatvault (default: chatvault/inbox)",
    )
    parser.add_argument("--drain-host", default="127.0.0.1")
    parser.add_argument("--drain-port", type=int, default=7847)
    parser.add_argument("--site-port", type=int, default=DEFAULT_SITE_PORT)
    parser.add_argument(
        "--track-b-mobius",
        nargs="?",
        const="48",
        metavar="N",
        help=(
            "run the RH Track B (Möbius–GCD) attack: identities, spectral "
            "snapshot, and missing-bridge routes. Does not claim RH."
        ),
    )
    args = parser.parse_args(argv)

    if args.site:
        serve_site(args.drain_host, args.site_port)
        return 0

    if args.drain_server:
        serve(args.drain_host, args.drain_port)
        return 0

    if args.ingest_chatvault:
        inbox = Path(args.inbox) if args.inbox else DEFAULT_INBOX
        result = ingest_path(args.ingest_chatvault, inbox)
        print(f"Wrote {len(result.written)} ChatVault sidecar(s) ({result.count} record(s)) to {inbox}")
        for warning in result.warnings:
            print(f"warning: {warning}", file=sys.stderr)
        for skipped in result.skipped:
            print(f"skipped: {skipped}", file=sys.stderr)
        if args.output and result.entries:
            write_drain(
                {
                    "format": "chatvault-export",
                    "schema_version": result.entries[0].get("schema_version"),
                    "source": "chatvault-inbox",
                    "count": result.count,
                    "entries": result.entries,
                },
                args.output,
            )
            print(f"Also wrote combined export to {args.output}")
        return 0

    if args.track_b_mobius is not None:
        from .track_b_mobius import attack

        n = int(args.track_b_mobius)
        report = attack(identity_ns=(min(6, n), min(12, n), min(24, n)), spectral_n=n, adversarial_n=n)
        payload = report.to_dict()
        if args.json or args.output:
            text = json.dumps(payload, indent=2, default=str)
            if args.output:
                Path(args.output).write_text(text + "\n", encoding="utf-8")
            else:
                sys.stdout.write(text)
                sys.stdout.write("\n")
        else:
            print(report.narrative())
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
            "expression is required unless --registry, --drain-server, --site, "
            "--ingest-chatvault, or --track-b-mobius is set"
        )

    if args.drain_chatvault:
        payload = drain_audit(args.expression)
        queued = try_enqueue(payload, host=args.drain_host, port=args.drain_port)
        if args.output:
            write_drain(payload, args.output)
            print(f"Wrote ChatVault export to {args.output}")
        else:
            json.dump(payload, sys.stdout, indent=2, default=str)
            sys.stdout.write("\n")
        if queued:
            print("Queued on local ChatVault drain (127.0.0.1:7847).", file=sys.stderr)
        elif not args.output:
            print(
                "Drain server was not listening. Start it with "
                "`python -m domain_architect --drain-server` or drop this JSON on ChatVault ingest.",
                file=sys.stderr,
            )
        return 0

    report = audit_expression(args.expression)
    if args.json:
        text = json.dumps(report.to_dict(), indent=2, default=str)
        if args.output:
            Path(args.output).write_text(text + "\n", encoding="utf-8")
        else:
            sys.stdout.write(text)
            sys.stdout.write("\n")
    else:
        print(report.narrative())
        print()
        print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
