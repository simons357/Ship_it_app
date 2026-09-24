#!/usr/bin/env python3
"""Run the 20 September 2026 Fourier-triangle reconstruction audit."""

from __future__ import annotations

import json
import math
from pathlib import Path

from ns_attacks.triangle_examples import report


def _sanitize(obj):
    if isinstance(obj, complex):
        return {"re": obj.real, "im": obj.imag}
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return str(obj)
        return obj
    if isinstance(obj, dict):
        return {str(k): _sanitize(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_sanitize(v) for v in obj]
    return obj


def main() -> None:
    rep = report()
    root = Path(__file__).resolve().parents[2]
    out = root / "results" / "fourier_triangle_audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(_sanitize(rep), indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: rep["locks"][k] for k in rep["locks"]}, indent=2))
    print("wrote", out)
    print("theorem 17:", rep["missing_theorem"]["status"])
    print("I3 regressions:", rep["I3_primes"]["all_match"])


if __name__ == "__main__":
    main()
