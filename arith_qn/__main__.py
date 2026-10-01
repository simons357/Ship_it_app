"""CLI for the Möbius–GCD Mertens identity.

Examples:

    python -m arith_qn --identity 6
    python -m arith_qn --survey --max-n 256 --out results/mertens_spectral
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .experiment import DEFAULT_SURVEY_NS, q6_record, write_survey
from .identity import SCOPE_STATEMENT, trace_identity
from .spectral import assess_transfer, cancellation_diagnostics, spectral_decomposition


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=SCOPE_STATEMENT)
    parser.add_argument("--identity", type=int, metavar="N", help="print Tr(D_N Q_N) = M(N)")
    parser.add_argument("--spectral", type=int, metavar="N", help="print Σ λ_j w_j and weights")
    parser.add_argument("--q6", action="store_true", help="print the locked Q_6 record")
    parser.add_argument("--survey", action="store_true", help="run the computational survey")
    parser.add_argument("--max-n", type=int, default=512, help="largest N in --survey")
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("results/mertens_spectral"),
        help="survey output directory",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.q6:
        print(json.dumps(q6_record(), indent=2))
        return 0
    if args.identity is not None:
        rec = trace_identity(args.identity)
        print(
            json.dumps(
                {
                    "n": rec.n,
                    "mertens": rec.mertens,
                    "trace": rec.trace,
                    "residual": rec.residual,
                    "divisor_residual": rec.divisor_residual,
                },
                indent=2,
            )
        )
        return 0
    if args.spectral is not None:
        decomp = spectral_decomposition(args.spectral)
        transfer = assess_transfer(identity_residual_ok=decomp.residual < 1e-6)
        payload = {
            "n": decomp.n,
            "mertens": decomp.mertens,
            "weighted_sum": decomp.weighted_sum,
            "residual": decomp.residual,
            "op_norm": decomp.op_norm,
            "crude_bound": decomp.crude_bound,
            "weight_min": decomp.weight_min,
            "weight_max": decomp.weight_max,
            "weight_sum": decomp.weight_sum,
            "diagnostics": cancellation_diagnostics(decomp),
            "transfer": transfer.to_dict(),
        }
        print(json.dumps(payload, indent=2))
        return 0
    if args.survey:
        ns = [n for n in DEFAULT_SURVEY_NS if n <= args.max_n]
        if args.max_n not in ns:
            ns.append(args.max_n)
            ns.sort()
        payload = write_survey(args.out, ns)
        print(args.out / "SUMMARY.md")
        print(
            json.dumps(
                {
                    "bridge_complete": payload["bridge_complete"],
                    "cancellation_status": payload["cancellation_status"],
                    "n_count": len(payload["rows"]),
                },
                indent=2,
            )
        )
        return 0
    build_parser().print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
