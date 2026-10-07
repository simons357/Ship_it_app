#!/usr/bin/env python3
"""First Gate B assembly test: explicit nonnegative Q_x.

Any uniform power bound ||Q(f)||_2 ≤ K Λ^θ Ω(f) on this
nonnegative majorant requires θ ≥ 1/2. The exact optimal
θ remains OPEN.

This is the concentration / regrouping test. It does not
restore signed cancellation. Not (17). NS is not solved.
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
    occupied_shells,
    similar_seed_triad,
    subnet_triads,
    theta_hat,
)


def single_triad_ratio(n: int) -> dict:
    """Equal-energy split on one similar triad at scale n.

    Q_a = C_abc f_b f_c, Ω = (a+b+c)/3, E = 1.
    Homogeneity: C(t²·) = t³ C, Ω(t²·) = t² Ω, so
    ||Q||_2 / Ω scales exactly as t = Λ^{1/2}.
    """
    u, v, w, a, b, c = similar_seed_triad(n)
    f = equal_energy_amplitudes([a, b, c])
    Q = nonnegative_Q([(u, v, w, a, b, c)], f)
    E, Omega, Lam = energy_enstrophy(f)
    Q2 = l2(Q.values())
    Cab = C_abc(a, b, c)
    return {
        "n": n,
        "a": a,
        "b": b,
        "c": c,
        "Lambda": Lam,
        "E": E,
        "Omega": Omega,
        "C_abc": Cab,
        "Q2": Q2,
        "Q2_over_Omega": Q2 / Omega if Omega else float("nan"),
        "Q_a": Q.get(a, 0.0),
        "homogeneity_check_C_over_n3": Cab / (n**3) if n else float("nan"),
        "homogeneity_check_ratio_over_n": (Q2 / Omega) / n if Omega and n else float("nan"),
    }


def subnet_ratio(n: int) -> dict:
    """Equal-energy nonnegative amplitudes on every occupied subnet shell."""
    triads = subnet_triads(n)
    shells = occupied_shells(triads)
    f = equal_energy_amplitudes(shells)
    Q = nonnegative_Q(triads, f)
    E, Omega, Lam = energy_enstrophy(f)
    Q2 = l2(Q.values())
    T_plus = sum(f[x] * Q[x] for x in f)
    return {
        "n": n,
        "c": 2 * n * n,
        "Lambda": Lam,
        "M_shells": len(shells),
        "n_triads": len(triads),
        "E": E,
        "Omega": Omega,
        "Q2": Q2,
        "Q2_over_Omega": Q2 / Omega if Omega else float("nan"),
        "T_plus": T_plus,
        "T_plus_over_sqrtE_Omega": T_plus / (E**0.5 * Omega) if E and Omega else float("nan"),
        "cs_holds": T_plus <= (E**0.5) * Q2 + 1e-9,
    }


def report() -> dict:
    single_ns = (4, 8, 16, 32)
    single_rows = [single_triad_ratio(n) for n in single_ns]
    single_thetas = [
        {
            "from_n": single_rows[i]["n"],
            "to_n": single_rows[i + 1]["n"],
            "theta_hat": theta_hat(
                single_rows[i]["Q2_over_Omega"],
                single_rows[i + 1]["Q2_over_Omega"],
                single_rows[i]["Lambda"],
                single_rows[i + 1]["Lambda"],
            ),
        }
        for i in range(len(single_rows) - 1)
    ]

    subnet_ns = (8, 16, 32)
    subnet_rows = [subnet_ratio(n) for n in subnet_ns]
    subnet_thetas = [
        {
            "from_n": subnet_rows[i]["n"],
            "to_n": subnet_rows[i + 1]["n"],
            "theta_hat": theta_hat(
                subnet_rows[i]["Q2_over_Omega"],
                subnet_rows[i + 1]["Q2_over_Omega"],
                subnet_rows[i]["Lambda"],
                subnet_rows[i + 1]["Lambda"],
            ),
        }
        for i in range(len(subnet_rows) - 1)
    ]

    # Analytic lock: similar dilation of one triad forces θ = 1/2.
    r4 = single_rows[0]
    r8 = single_rows[1]
    scale = r8["n"] / r4["n"]
    C_scale = r8["C_abc"] / r4["C_abc"]
    Omega_scale = r8["Omega"] / r4["Omega"]
    ratio_scale = r8["Q2_over_Omega"] / r4["Q2_over_Omega"]

    mean_single = sum(t["theta_hat"] for t in single_thetas) / len(single_thetas)
    mean_subnet = sum(t["theta_hat"] for t in subnet_thetas) / len(subnet_thetas)

    return {
        "object": "explicit nonnegative Q_x of Dish #3",
        "definition": {
            "Q_x": "sum_{triads with low vertex x} C_xyz f_y f_z",
            "C_abc": "nonnegative September 20 majorant",
            "E": "sum f_x^2",
            "Omega": "sum x f_x^2  (enstrophy; x = |k|^2)",
            "Lambda": "max occupied x",
            "uniform_power_bound": "||Q(f)||_2 <= K Lambda^theta Omega(f) for all f >= 0",
        },
        "lemma_similar_triad": {
            "statement": (
                "On any similar dilation of a fixed positive triad with "
                "equal-energy amplitudes, ||Q||_2 / Omega scales as Lambda^{1/2}. "
                "Hence every uniform power bound on this nonnegative Q_x "
                "requires theta >= 1/2."
            ),
            "rows": single_rows,
            "theta_hats": single_thetas,
            "mean_theta_hat": mean_single,
            "C_scales_as_n3": abs(C_scale / (scale**3) - 1.0) < 1e-12,
            "Omega_scales_as_n2": abs(Omega_scale / (scale**2) - 1.0) < 1e-12,
            "ratio_scales_as_n": abs(ratio_scale / scale - 1.0) < 1e-9,
            "theta_equals_half_on_this_family": abs(mean_single - 0.5) < 1e-9,
        },
        "subnet_diagnostic": {
            "rows": subnet_rows,
            "theta_hats": subnet_thetas,
            "mean_theta_hat": mean_subnet,
            "note": (
                "Many overlapping nonnegative triads. Empirical theta is a "
                "diagnostic, not a new upper bound."
            ),
        },
        "locks": {
            "requires_theta_ge_half": True,
            "theta_optimal_open": True,
            "cannot_gain_by_regrouping_this_majorant": True,
            "next_test_must_preserve_signed_cancellation": True,
            "theta_proved_equal_half_uniformly": False,
            "C_majorant_is_upper_bound": True,
            "theorem_17_proved": False,
            "not_a_close": True,
            "gate_A": "UNRESOLVED / DIAGNOSTIC ONLY",
            "gate_B_active": True,
        },
    }


def main(argv=None) -> int:
    argparse.ArgumentParser(description=__doc__).parse_args(argv)
    payload = report()
    out = Path(__file__).with_name("NONNEGATIVE-QX-ASSEMBLY.json")
    out.write_text(json.dumps(payload, indent=2) + "\n")
    print(json.dumps(payload, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
