"""Command-line interface for Domain Architect audits."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .audit import audit_expression
from .chatvault_bridge import drain_audit, try_enqueue, write_drain
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
    parser.add_argument("--drain-host", default="127.0.0.1")
    parser.add_argument("--drain-port", type=int, default=7847)
    parser.add_argument("--site-port", type=int, default=DEFAULT_SITE_PORT)
    args = parser.parse_args(argv)

    if args.site:
        serve_site(args.drain_host, args.site_port)
        return 0

    if args.drain_server:
        serve(args.drain_host, args.drain_port)
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
        parser.error("expression is required unless --registry, --drain-server, or --site is set")

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
