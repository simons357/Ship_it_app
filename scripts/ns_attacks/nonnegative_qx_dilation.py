#!/usr/bin/env python3
"""Similar-triad dilation: nonnegative Q_x forces θ ≥ 1/2.

Homogeneity of the September 20 majorant, not all-radii counting.
Exact optimal θ remains OPEN. Not (17). NS is not solved.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ns_attacks.qx_kernel import (  # noqa: E402
    C_abc,
    equal_energy_amplitudes,
    energy_enstrophy,
    l2,
    nonnegative_Q,
    similar_seed_triad,
    theta_hat,
)


def single_triad_ratio(n: int) -> dict:
    u, v, w, a, b, c = similar_seed_triad(n)
    f = equal_energy_amplitudes([a, b, c])
    Q = nonnegative_Q([(u, v, w, a, b, c)], f)
    E, Omega, Lam = energy_enstrophy(f)
    Q2 = l2(Q.values())
    T_plus = sum(f[x] * Q.get(x, 0.0) for x in f)
    return {
        "n": n,
        "a": a,
        "b": b,
        "c": c,
        "Lambda": Lam,
        "E": E,
        "Omega": Omega,
        "C_abc": C_abc(a, b, c),
        "Q2": Q2,
        "Q2_over_Omega": Q2 / Omega if Omega else float("nan"),
        "T_plus": T_plus,
        "cs1_holds": T_plus <= (E**0.5) * Q2 + 1e-12,
        "homogeneity_C_over_n3": C_abc(a, b, c) / (n**3) if n else float("nan"),
        "ratio_over_n": (Q2 / Omega) / n if Omega and n else float("nan"),
    }


def report() -> dict:
    ns = (4, 8, 16, 32)
    rows = [single_triad_ratio(n) for n in ns]
    thetas = [
        {
            "from_n": rows[i]["n"],
            "to_n": rows[i + 1]["n"],
            "theta_hat": theta_hat(
                rows[i]["Q2_over_Omega"],
                rows[i + 1]["Q2_over_Omega"],
                rows[i]["Lambda"],
                rows[i + 1]["Lambda"],
            ),
        }
        for i in range(len(rows) - 1)
    ]
    mean_theta = sum(t["theta_hat"] for t in thetas) / len(thetas)
    return {
        "family": "similar_triad_equal_energy",
        "rows": rows,
        "pairwise_theta": thetas,
        "mean_theta_hat": mean_theta,
        "requires_theta_ge_half": True,
        "theta_proved_equal_half_uniformly": False,
        "cs1_holds_on_family": all(r["cs1_holds"] for r in rows),
        "depends_on_all_radii_counting": False,
        "theorem_17_proved": False,
        "ns_solved": False,
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Nonnegative Q_x similar-triad dilation")
    p.add_argument(
        "--out",
        type=Path,
        default=Path("scripts/ns_attacks/NONNEGATIVE-QX-DILATION.json"),
    )
    args = p.parse_args()
    payload = report()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2))
    print("mean theta_hat:", payload["mean_theta_hat"])
    print("requires theta >= 1/2:", payload["requires_theta_ge_half"])
    print("CS-1 holds:", payload["cs1_holds_on_family"])
    print(f"wrote {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
