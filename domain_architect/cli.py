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
from .ns_tube import format_tube_estimate, tube_estimate
from .gap import format_gap, gap_report
from .shape_play import format_shape_play, shape_play
from .energy_play import energy_play, format_energy_play
from .overlay import format_overlay, overlay_report
from .scan import format_scan, scan_report
from .shell import format_shell, shell_report
from .jigsaw import format_jigsaw, jigsaw_report
from .think_tank import consult, format_consult
from .visual import follow, format_follow
from .desk_server import serve_site
from .registry import EquationRegistry
from .schema import CANONICAL_SFE_STATUS, PRODUCT_DESCRIPTION


def _follow_math(action: str, book: str = "B", *, json_mode: bool) -> dict:
    """Picture slave of the math. Quiet when stdout is JSON."""
    state = follow(action, book)
    if not json_mode:
        print()
        print(format_follow(state))
    return state


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
        "--consult",
        metavar="TOPIC",
        nargs="?",
        const="method",
        help="ask the inner think tank (method, or B for the worked example)",
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
    parser.add_argument(
        "--tube",
        metavar="BOOK",
        help="print the live tube estimate (B or NS): Hardy, wall, I_tube",
    )
    parser.add_argument(
        "--gap",
        metavar="BOOK",
        help="stop at the first open wall; show the missing piece and candidates after (B or CHAIN)",
    )
    parser.add_argument(
        "--shape-play",
        metavar="BOOK",
        nargs="?",
        const="B",
        help="fill the other side of a shape and measure (B / cylinder / strain)",
    )
    parser.add_argument(
        "--energy-play",
        metavar="BOOK",
        nargs="?",
        const="B",
        help="treat energy as a visual object: see the outside, guess the shape (B)",
    )
    parser.add_argument(
        "--overlay",
        metavar="BOOK",
        nargs="?",
        const="B",
        help="break into pieces, overlay the done transposable ones, refine holes (B)",
    )
    parser.add_argument(
        "--scan",
        metavar="TARGET",
        nargs="?",
        const="ANY",
        help="anatomy machine: leftover holes vs pieces (no book = method; B = worked example)",
    )
    parser.add_argument(
        "--shell",
        metavar="BOOK",
        nargs="?",
        const="B",
        help="inside plus outer shell; silhouette may identify a known object (B / Q)",
    )
    parser.add_argument(
        "--jigsaw",
        metavar="BOOK",
        nargs="?",
        const="B",
        help="literal pieces, assemble, classify holes as damage (B / Q)",
    )
    parser.add_argument(
        "--assemble",
        dest="jigsaw",
        metavar="BOOK",
        nargs="?",
        const="B",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--puzzle",
        dest="jigsaw",
        metavar="BOOK",
        nargs="?",
        const="B",
        help=argparse.SUPPRESS,
    )
    parser.add_argument(
        "--see",
        metavar="BOOK",
        nargs="?",
        const="B",
        help="write a human picture desk (SVG/HTML) from the same math objects (B)",
    )
    parser.add_argument(
        "--site",
        action="store_true",
        help="open the simple scientific desk in a browser (inquire / see / compute)",
    )
    args = parser.parse_args(argv)

    if args.site:
        serve_site()
        return 0

    if args.proceed:
        payload = proceed_report()
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_proceed(payload))
        return 0

    if args.consult is not None:
        payload = consult(args.consult)
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_consult(payload))
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
        _follow_math("compare", json_mode=args.json)
        return 0

    if args.clip:
        clipped = clip_splice(args.clip[0], args.clip[1])
        if args.json:
            json.dump(clipped.to_dict(), sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_clip_splice(clipped))
        _follow_math("clip", json_mode=args.json)
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
        _follow_math("chain", book, json_mode=args.json)
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
        _follow_math("geometry", book, json_mode=args.json)
        return 0

    if args.tube:
        book = args.tube.strip().upper()
        if book not in {"B", "NS", "TRACKB", "NAVIERSTOKES", "NAVIER-STOKES"}:
            print(
                "Only Track B / NS tube estimate is wired. RH is a different book.",
                file=sys.stderr,
            )
            return 2
        payload = tube_estimate()
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_tube_estimate(payload))
        _follow_math("tube", book, json_mode=args.json)
        return 0

    if args.gap:
        payload = gap_report(args.gap)
        if payload.get("error"):
            print(payload["error"], file=sys.stderr)
            return 2
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_gap(payload))
        _follow_math("gap", args.gap, json_mode=args.json)
        return 0

    if args.shape_play is not None:
        book = args.shape_play.strip().upper()
        if book not in {
            "B",
            "NS",
            "TRACKB",
            "TUBE",
            "CYLINDER",
            "STRAIN",
            "NAVIERSTOKES",
            "NAVIER-STOKES",
        }:
            print(
                "Only Track B / cylinder / strain shape-play is wired.",
                file=sys.stderr,
            )
            return 2
        payload = shape_play()
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_shape_play(payload))
        _follow_math("shape-play", book, json_mode=args.json)
        return 0

    if args.energy_play is not None:
        book = args.energy_play.strip().upper()
        if book not in {
            "B",
            "NS",
            "TRACKB",
            "ENERGY",
            "NAVIERSTOKES",
            "NAVIER-STOKES",
        }:
            print(
                "Only Track B / energy-play is wired. RH is a different book.",
                file=sys.stderr,
            )
            return 2
        payload = energy_play()
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_energy_play(payload))
        _follow_math("energy-play", book, json_mode=args.json)
        return 0

    if args.overlay is not None:
        book = args.overlay.strip().upper()
        if book not in {"B", "NS", "TRACKB", "NAVIERSTOKES", "NAVIER-STOKES"}:
            print(
                "Only Track B / NS overlay is wired. RH is a different book.",
                file=sys.stderr,
            )
            return 2
        payload = overlay_report()
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_overlay(payload))
        _follow_math("overlay", book, json_mode=args.json)
        return 0

    if args.scan is not None:
        payload = scan_report(args.scan)
        if payload.get("error"):
            print(payload["error"], file=sys.stderr)
            return 2
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_scan(payload))
        _follow_math("scan", payload.get("book", "B"), json_mode=args.json)
        return 0

    if args.shell is not None:
        payload = shell_report(args.shell)
        if payload.get("error"):
            print(payload["error"], file=sys.stderr)
            return 2
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_shell(payload))
        _follow_math("shell", payload.get("book", "B"), json_mode=args.json)
        return 0

    if args.jigsaw is not None:
        payload = jigsaw_report(args.jigsaw)
        if payload.get("error"):
            print(payload["error"], file=sys.stderr)
            return 2
        if args.json:
            json.dump(payload, sys.stdout, indent=2)
            sys.stdout.write("\n")
        else:
            print(format_jigsaw(payload))
        _follow_math("jigsaw", payload.get("book", "B"), json_mode=args.json)
        return 0

    if args.see is not None:
        book = args.see.strip().upper()
        if book not in {"B", "NS", "TRACKB", "NAVIERSTOKES", "NAVIER-STOKES"}:
            print(
                "Only Track B / NS see-desk is wired. RH is a different book.",
                file=sys.stderr,
            )
            return 2
        state = _follow_math("see", book, json_mode=args.json)
        dest = state.get("picture", "docs/domain-architect/see.html")
        if args.json:
            json.dump(
                {
                    "wrote": str(dest),
                    "not_a_regularity_proof": True,
                    "appendage": "SEE",
                    "action": state["action"],
                },
                sys.stdout,
                indent=2,
            )
            sys.stdout.write("\n")
        else:
            print("Human see. Math is git. Not a proof.")
            print(f"Wrote {dest}")
            print("Open that file in a browser. CosmoEvolution is not this lab.")
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
            "expression is required unless --registry, --proceed, --consult, "
            "--refuse-splice, --shape-compare, --clip, --chain, "
            "--geometry, --tube, --gap, --shape-play, --energy-play, --overlay, --scan, --shell, --jigsaw, --see, or --site is set"
        )

    report = audit_expression(args.expression)
    if args.json:
        json.dump(report.to_dict(), sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
    else:
        print(report.narrative())
        print()
        print(f"Canonical SFE status: {CANONICAL_SFE_STATUS}.")
    _follow_math("audit", json_mode=args.json)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
