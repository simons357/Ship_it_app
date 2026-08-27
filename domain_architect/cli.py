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
    parser.add_argument(
        "--route-c",
        action="store_true",
        help=(
            "print the Route C exploratory face (05_route_c_conditional.pdf). "
            "Does not claim RH and does not file into ChatVault."
        ),
    )
    parser.add_argument(
        "--universe",
        action="store_true",
        help=(
            "print the universe / SFE picture face. Unresolved, exploratory, "
            "not a proof, and not filed into ChatVault."
        ),
    )
    parser.add_argument(
        "--swirl-with-cancel",
        action="store_true",
        help=(
            "print the live Φ-renormalization swirl face (01_phi_renormalization.pdf). "
            "Q1-augmented algebra. Does not claim Clay NS. Not ChatVault."
        ),
    )
    parser.add_argument(
        "--swirl-without-cancel",
        action="store_true",
        help=(
            "print the swirl face with the 1/r^4 axis term still present. "
            "OPEN obstruction. Does not claim Clay NS. Not ChatVault."
        ),
    )
    parser.add_argument(
        "--swirl-compare",
        action="store_true",
        help="compare swirl WITH vs WITHOUT Φ-cancel. Not a Clay proof. Not ChatVault.",
    )
    parser.add_argument(
        "--ns-unaugmented",
        action="store_true",
        help=(
            "print the classical unaugmented 3D Navier–Stokes face. "
            "OPEN / not proved. Does not claim Clay NS. Not ChatVault."
        ),
    )
    parser.add_argument(
        "--honest-mistake",
        action="store_true",
        help=(
            "print the June 2026 packaging honest-mistake note. "
            "Not a proof. Not ChatVault. Does not re-stamp titles."
        ),
    )
    parser.add_argument(
        "--ns-regularity-realization",
        action="store_true",
        help=(
            "run the hypothesized unaugmented NS regularity realization "
            "against the other desk fingers. Not a theorem. Not ChatVault."
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

    if args.route_c:
        from .route_c import face, narrative

        payload = face()
        payload["audit"] = audit_expression(payload["operator"]).to_dict()
        if args.json or args.output:
            text = json.dumps(payload, indent=2, default=str)
            if args.output:
                Path(args.output).write_text(text + "\n", encoding="utf-8")
            else:
                sys.stdout.write(text)
                sys.stdout.write("\n")
        else:
            print(narrative())
            print()
            print(audit_expression(payload["operator"]).narrative())
        return 0

    if args.universe:
        from .universe import UNIVERSE_PROMPT, face, narrative

        payload = face()
        payload["audit"] = audit_expression(UNIVERSE_PROMPT).to_dict()
        if args.json or args.output:
            text = json.dumps(payload, indent=2, default=str)
            if args.output:
                Path(args.output).write_text(text + "\n", encoding="utf-8")
            else:
                sys.stdout.write(text)
                sys.stdout.write("\n")
        else:
            print(narrative())
            print()
            print(audit_expression(UNIVERSE_PROMPT).narrative())
        return 0

    if args.swirl_compare:
        from .swirl import compare_faces, compare_narrative

        payload = compare_faces()
        payload["audit"] = audit_expression(
            "axisymmetric Navier-Stokes with swirl: with vs without cancellation"
        ).to_dict()
        if args.json or args.output:
            text = json.dumps(payload, indent=2, default=str)
            if args.output:
                Path(args.output).write_text(text + "\n", encoding="utf-8")
            else:
                sys.stdout.write(text)
                sys.stdout.write("\n")
        else:
            print(compare_narrative())
            print()
            print(payload["audit"]["narrative"])
        return 0

    if args.swirl_with_cancel:
        from .swirl import SWIRL_WITH_OPERATOR, with_cancel_face, with_cancel_narrative

        payload = with_cancel_face()
        payload["audit"] = audit_expression(SWIRL_WITH_OPERATOR).to_dict()
        if args.json or args.output:
            text = json.dumps(payload, indent=2, default=str)
            if args.output:
                Path(args.output).write_text(text + "\n", encoding="utf-8")
            else:
                sys.stdout.write(text)
                sys.stdout.write("\n")
        else:
            print(with_cancel_narrative())
            print()
            print(audit_expression(SWIRL_WITH_OPERATOR).narrative())
        return 0

    if args.swirl_without_cancel:
        from .swirl import (
            SWIRL_WITHOUT_OPERATOR,
            without_cancel_face,
            without_cancel_narrative,
        )

        payload = without_cancel_face()
        payload["audit"] = audit_expression(SWIRL_WITHOUT_OPERATOR).to_dict()
        if args.json or args.output:
            text = json.dumps(payload, indent=2, default=str)
            if args.output:
                Path(args.output).write_text(text + "\n", encoding="utf-8")
            else:
                sys.stdout.write(text)
                sys.stdout.write("\n")
        else:
            print(without_cancel_narrative())
            print()
            print(audit_expression(SWIRL_WITHOUT_OPERATOR).narrative())
        return 0

    if args.ns_unaugmented:
        from .ns_unaugmented import NS_OPERATOR, face, narrative

        payload = face()
        payload["audit"] = audit_expression(NS_OPERATOR).to_dict()
        if args.json or args.output:
            text = json.dumps(payload, indent=2, default=str)
            if args.output:
                Path(args.output).write_text(text + "\n", encoding="utf-8")
            else:
                sys.stdout.write(text)
                sys.stdout.write("\n")
        else:
            print(narrative())
            print()
            print(audit_expression(NS_OPERATOR).narrative())
        return 0

    if args.honest_mistake:
        from .honest_mistake import HONEST_MISTAKE_PROMPT, face, narrative

        payload = face()
        payload["audit"] = audit_expression(HONEST_MISTAKE_PROMPT).to_dict()
        if args.json or args.output:
            text = json.dumps(payload, indent=2, default=str)
            if args.output:
                Path(args.output).write_text(text + "\n", encoding="utf-8")
            else:
                sys.stdout.write(text)
                sys.stdout.write("\n")
        else:
            print(narrative())
            print()
            print(audit_expression(HONEST_MISTAKE_PROMPT).narrative())
        return 0

    if args.ns_regularity_realization:
        from .ns_regularity_realization import (
            REALIZATION_PROMPT,
            experiment,
            narrative,
            write_outputs,
        )

        payload = experiment()
        payload["audit"] = audit_expression(REALIZATION_PROMPT).to_dict()
        written = write_outputs()
        payload["written"] = {key: str(path) for key, path in written.items()}
        if args.json or args.output:
            text = json.dumps(payload, indent=2, default=str)
            if args.output:
                Path(args.output).write_text(text + "\n", encoding="utf-8")
            else:
                sys.stdout.write(text)
                sys.stdout.write("\n")
        else:
            print(narrative(payload))
            print()
            print(audit_expression(REALIZATION_PROMPT).narrative())
            for key, path in written.items():
                print(f"Wrote {key}: {path}")
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
            "--ingest-chatvault, --track-b-mobius, --route-c, --universe, "
            "--swirl-with-cancel, --swirl-without-cancel, --swirl-compare, "
            "--ns-unaugmented, --honest-mistake, or --ns-regularity-realization is set"
        )

    if args.drain_chatvault:
        from .honest_mistake import looks_like_honest_mistake
        from .ns_regularity_realization import looks_like_ns_regularity_realization
        from .ns_unaugmented import looks_like_ns_t3_archive, looks_like_ns_unaugmented
        from .route_c import looks_like_route_c_operator, looks_like_superseded_june_route_c
        from .swirl import (
            looks_like_swirl_compare,
            looks_like_swirl_with_cancel,
            looks_like_swirl_without_cancel,
        )
        from .universe import looks_like_universe_inquiry

        if looks_like_route_c_operator(args.expression) or looks_like_superseded_june_route_c(
            args.expression
        ):
            print(
                "Route C stays in Domain Architect. Not filed into ChatVault.",
                file=sys.stderr,
            )
            report = audit_expression(args.expression)
            if args.json:
                sys.stdout.write(json.dumps(report.to_dict(), indent=2, default=str))
                sys.stdout.write("\n")
            else:
                print(report.narrative())
            return 0
        if (
            looks_like_swirl_compare(args.expression)
            or looks_like_swirl_with_cancel(args.expression)
            or looks_like_swirl_without_cancel(args.expression)
        ):
            print(
                "Swirl faces stay in Domain Architect. Not filed into ChatVault.",
                file=sys.stderr,
            )
            report = audit_expression(args.expression)
            if args.json:
                sys.stdout.write(json.dumps(report.to_dict(), indent=2, default=str))
                sys.stdout.write("\n")
            else:
                print(report.narrative())
            return 0
        if looks_like_ns_unaugmented(args.expression) or looks_like_ns_t3_archive(
            args.expression
        ):
            print(
                "Unaugmented NS stays in Domain Architect. Not filed into ChatVault.",
                file=sys.stderr,
            )
            report = audit_expression(args.expression)
            if args.json:
                sys.stdout.write(json.dumps(report.to_dict(), indent=2, default=str))
                sys.stdout.write("\n")
            else:
                print(report.narrative())
            return 0
        if looks_like_ns_regularity_realization(args.expression):
            print(
                "NS regularity realization stays in Domain Architect. "
                "Hypothesized, not a theorem. Not filed into ChatVault.",
                file=sys.stderr,
            )
            report = audit_expression(args.expression)
            if args.json:
                sys.stdout.write(json.dumps(report.to_dict(), indent=2, default=str))
                sys.stdout.write("\n")
            else:
                print(report.narrative())
            return 0
        if looks_like_honest_mistake(args.expression):
            print(
                "The honest-mistake note stays in Domain Architect. Not filed into ChatVault.",
                file=sys.stderr,
            )
            report = audit_expression(args.expression)
            if args.json:
                sys.stdout.write(json.dumps(report.to_dict(), indent=2, default=str))
                sys.stdout.write("\n")
            else:
                print(report.narrative())
            return 0
        if looks_like_universe_inquiry(args.expression):
            print(
                "Universe / SFE picture stays in Domain Architect inquiry. "
                "Unresolved. Not filed into ChatVault.",
                file=sys.stderr,
            )
            report = audit_expression(args.expression)
            if args.json:
                sys.stdout.write(json.dumps(report.to_dict(), indent=2, default=str))
                sys.stdout.write("\n")
            else:
                print(report.narrative())
            return 0
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
