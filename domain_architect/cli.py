"""Command-line interface for Domain Architect v1.0."""

from __future__ import annotations

import argparse
import json
import sys

from .audit import audit_expression
from .pipeline import run_benchmarks, run_named_cycle
from .registry import EquationRegistry
from .schema import PRIMARY_OPERATIONS, PRODUCT_DESCRIPTION
from .synthesize import inverse_design_architecture
from .translate import (
    mechanical_electrical_translation,
    snd_vs_h_translation,
    translate_expressions,
)


_COMMANDS = {"decompose", "translate", "synthesize", "cycle", "benchmark", "app"}


def main(argv: list[str] | None = None) -> int:
    argv = list(sys.argv[1:] if argv is None else argv)
    positionals = [a for a in argv if not a.startswith("-")]
    if positionals and positionals[0] not in _COMMANDS:
        argv = ["decompose", *argv]

    parser = argparse.ArgumentParser(description=PRODUCT_DESCRIPTION)
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    parser.add_argument(
        "--archive",
        action="store_true",
        help="print archived SFE / UHF / DHFA / HB inventory",
    )
    parser.add_argument(
        "--registry",
        action="store_true",
        help="alias for --archive (historical)",
    )
    sub = parser.add_subparsers(dest="command")

    p_dec = sub.add_parser("decompose", help="DECOMPOSE an expression")
    p_dec.add_argument("expression")

    p_tr = sub.add_parser("translate", help="TRANSLATE two expressions or the RLC analog")
    p_tr.add_argument("--a", dest="left", help="left expression")
    p_tr.add_argument("--b", dest="right", help="right expression")
    p_tr.add_argument(
        "--example",
        choices=("mechanical-electrical", "snd-vs-h"),
        help="run a built-in translation pair",
    )

    p_sy = sub.add_parser("synthesize", help="inverse-design required architecture")
    p_sy.add_argument("--target", required=True)
    p_sy.add_argument("--constraint", action="append", default=[])

    p_cy = sub.add_parser("cycle", help="run a named DA cycle")
    p_cy.add_argument(
        "name",
        nargs="?",
        default="missing-damping",
        help="missing-damping | control | mechanical-electrical | drag | leftover-repair | localized-repair | open-board | turbulence-intensity | available-turbulence",
    )
    p_cy.add_argument(
        "--excise",
        default=None,
        help="cut step k of an n-step chain (localized-repair). Example: --excise 2",
    )
    p_cy.add_argument(
        "--chain",
        default=None,
        help="paper2 | classical | unaugmented | toy (localized-repair only)",
    )

    p_bm = sub.add_parser("benchmark", help="run the v1.0 computational benchmarks")
    p_app = sub.add_parser("app", help="launch the Domain Architect desktop app")
    p_app.add_argument("--port", type=int, default=8765)
    p_app.add_argument("--no-browser", action="store_true")
    p_app.add_argument(
        "--install-shortcut",
        action="store_true",
        help="write a Desktop / applications shortcut and exit",
    )

    args = parser.parse_args(argv)
    as_json = bool(getattr(args, "json", False))

    if args.archive or args.registry:
        return _print_archive(as_json)

    command = args.command
    if command == "decompose":
        return _print_decompose(args.expression, as_json)
    if command == "translate":
        return _print_translate(args, as_json)
    if command == "synthesize":
        from .available_turbulence import maybe_available_stack

        stacked = maybe_available_stack(args.target, list(args.constraint))
        payload = stacked or inverse_design_architecture(
            args.target, list(args.constraint)
        ).to_dict()
        return _emit(payload, as_json, _synth_text(payload))
    if command == "cycle":
        report = run_named_cycle(
            args.name,
            chain=getattr(args, "chain", None),
            excise=getattr(args, "excise", None),
        )
        return _emit(report.to_dict(), as_json, _cycle_text(report.to_dict()))
    if command == "benchmark":
        payload = run_benchmarks()
        return _emit(payload, as_json, _benchmark_text(payload))
    if command == "app":
        from .app import install_desktop_shortcut, serve

        if args.install_shortcut:
            path = install_desktop_shortcut()
            print(f"Desktop shortcut written: {path}")
            return 0
        serve(port=args.port, open_browser=not args.no_browser)
        return 0

    parser.print_help()
    print()
    print(f"Primary operations: {PRIMARY_OPERATIONS}")
    return 0


def _print_archive(as_json: bool) -> int:
    registry = EquationRegistry.load_default()
    payload = registry.export()
    payload["note"] = (
        "Archived historical inventory. SFE, UHF, DHFA and the Harmonic "
        "Blueprint are not part of the live Domain Architect v1.0 core."
    )
    if as_json:
        json.dump(payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
        return 0
    print("Archived historical inventory (not live DA mathematics)")
    print(f"Historical equations: {len(payload['equations'])}")
    print(f"Conflicts: {len(payload['conflicts'])}")
    print(f"Null / counterexample records: {len(payload['nulls'])}")
    for eq in payload["equations"]:
        print(
            f"  {eq['equation_id']} [{eq['audit_disposition']}] "
            f"{eq['original_expression']}"
        )
    return 0


def _print_decompose(expression: str, as_json: bool) -> int:
    report = audit_expression(expression)
    if as_json:
        json.dump(report.to_dict(), sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
        return 0
    print(report.narrative())
    return 0


def _print_translate(args: argparse.Namespace, as_json: bool) -> int:
    if args.example == "snd-vs-h":
        record = snd_vs_h_translation()
    elif args.example == "mechanical-electrical" or not (args.left and args.right):
        record = mechanical_electrical_translation()
    else:
        record = translate_expressions(args.left, args.right)
    payload = record.to_dict()
    text = [
        "Domain Architect — CROSS-DOMAIN TRANSLATE",
        f"{payload['left']}  ↔  {payload['right']}",
        f"kind: {payload['kind']}",
        f"confidence: {payload['confidence']}",
        f"mapping: {payload['mapping']}",
        f"preserved: {payload['preserved']}",
        f"broken: {payload['broken']}",
    ]
    for item in payload["compatibility"]:
        text.append(f"  {item['left']} → {item['right']}: {item['verdict']}")
    return _emit(payload, as_json, "\n".join(text))


def _synth_text(payload: dict) -> str:
    lines = [
        "Domain Architect — SYNTHESIZE",
        payload.get("name") or "",
        payload["hypothesis"],
        "components: " + ", ".join(payload["components"]),
        f"validation gate: {payload['validation_gate']}",
    ]
    board = payload.get("board") or {}
    if isinstance(board, dict) and board.get("text"):
        lines.append(board["text"])
    return "\n".join(lines)


def _cycle_text(payload: dict) -> str:
    lines = [
        f"Domain Architect cycle ({payload['mode']})",
        f"target: {payload['target']}",
        f"constraints: {payload['constraints']}",
        f"validation gate: {payload['validation_gate']}",
    ]
    if payload.get("residual"):
        res = payload["residual"]
        lines.append(
            f"missing role: {res.get('missing_role')} "
            f"({res.get('operator_class')}) recovered={res.get('recovered_parameter')}"
        )
    prediction = payload.get("prediction") or {}
    protocol = prediction.get("protocol") if isinstance(prediction, dict) else None
    if protocol == "turbulence-intensity":
        lines.append(prediction.get("definition") or "")
        lines.append(
            "control x={:.4f}  treated x={:.4f}  relative reduction={:.3f}  "
            "reduced_vs_control={}".format(
                prediction["control_arm"]["terminal_x"],
                prediction["treated_arm"]["terminal_x"],
                prediction["relative_reduction"],
                prediction["reduced_vs_control"],
            )
        )
    elif protocol == "available-turbulence":
        lines.append(prediction.get("headline") or "")
        analog = prediction.get("analog") or {}
        lines.append(
            "desired {}  analog relative reduction={:.3f}  "
            "hardware_realized={}  envelope_contains_15%={}".format(
                prediction.get("desired", {}).get("as_setpoint"),
                analog.get("relative_reduction") or 0.0,
                prediction.get("states", {}).get("hardware_realized", {}).get("value"),
                prediction.get("envelope_can_contain_target"),
            )
        )
        board = prediction.get("board") or {}
        if isinstance(board, dict) and board.get("text"):
            lines.append(board["text"])
    elif isinstance(prediction, dict) and prediction.get("headline"):
        lines.append(prediction["headline"])
        still = prediction.get("still_open") or []
        if still:
            lines.append(
                "still open: " + ", ".join(row.get("id", "") for row in still)
            )
    elif isinstance(prediction, dict) and prediction.get("board"):
        lines.append(prediction["board"].get("text") or "")
    elif prediction:
        lines.append(f"prediction: {payload['prediction']}")
    for note in payload.get("notes") or []:
        lines.append(f"- {note}")
    return "\n".join(lines)


def _benchmark_text(payload: dict) -> str:
    lines = ["Domain Architect v1.0 benchmarks"]
    for key, value in payload.items():
        lines.append(f"{key}: {value}")
    return "\n".join(lines)


def _emit(payload: dict, as_json: bool, text: str) -> int:
    if as_json:
        json.dump(payload, sys.stdout, indent=2, default=str)
        sys.stdout.write("\n")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
