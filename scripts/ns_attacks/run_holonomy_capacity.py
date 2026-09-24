#!/usr/bin/env python3
"""Run the loop-gauge, polarization, and telescopic-capacity strikes.

Not a close. NS is not solved.
"""

from __future__ import annotations

import argparse
import json
from typing import Sequence

from ns_attacks.loop_gauge import parallelogram_report, star_report
from ns_attacks.polarization_holonomy import parallelogram_polarization, star_polarization
from ns_attacks.telescopic_capacity import report as capacity_report


def _py(x):
    if isinstance(x, complex):
        return {"re": x.real, "im": x.imag}
    if isinstance(x, dict):
        return {str(k): _py(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [_py(v) for v in x]
    return x


def report() -> dict:
    return {
        "strike": "polarization holonomy + telescopic capacity",
        "date": "2026-09-24",
        "loop": {
            "star": star_report(),
            "parallelogram": parallelogram_report(),
        },
        "polarization": {
            "star": star_polarization(),
            "parallelogram": parallelogram_polarization(),
        },
        "jgc": capacity_report(),
        "locks": {
            "topology_alone_does_not_force_phase_frustration": True,
            "additive_gauge_is_translation_invariance": True,
            "epoch_count_is_the_wrong_target": True,
            "circular_lambda_motion_rejected": True,
            "not_a_close": True,
        },
    }


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args(list(argv) if argv is not None else None)
    print(json.dumps(_py(report()), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
