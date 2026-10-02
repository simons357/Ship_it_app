#!/usr/bin/env python3
"""Young occupation keeps nu. Algebra only.

Packages the stated local envelope

    T_loc = alpha chi kappa^{3/2} X D_s^{1/2}

as

    T_loc <= (1/2) nu D_s + alpha^2 chi^2 kappa^3 X^2 / (2 nu).

Dividing the remainder by Y = kappa^2 X leaves
alpha^2 chi^2 kappa X / (2 nu). Occupation (constants dropped)
is integral alpha^2 chi^2 kappa X dt / nu < infinity.

Does not prove the envelope. Does not prove occupation.
Does not drop nu. A8-R construction is not on this tree.
NS is not solved.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


MISSING_SOURCES = (
    "I3_WEIGHTED_TARGET_2026-09-20.md",
    "K,K,L regrouping file",
    "A8-R construction",
    "cube-field run",
    "54/46 quartic test",
)


def young_split(
    alpha: float, chi: float, kappa: float, X: float, Ds: float, nu: float
) -> dict:
    env = alpha * chi * (kappa**1.5) * X * math.sqrt(Ds)
    visc = 0.5 * nu * Ds
    rem = (alpha**2 * chi**2 * (kappa**3) * (X**2)) / (2.0 * nu)
    Y = (kappa**2) * X
    rem_over_Y = rem / Y
    expect_half = (alpha**2 * chi**2 * kappa * X) / (2.0 * nu)
    occupation_density = (alpha**2 * chi**2 * kappa * X) / nu
    return {
        "envelope": env,
        "viscous_slot": visc,
        "remainder": rem,
        "Y": Y,
        "remainder_over_Y": rem_over_Y,
        "expect_half_nu": expect_half,
        "occupation_density": occupation_density,
        "covers": visc + rem + 1e-12 >= env,
        "remainder_identity": abs(rem_over_Y - expect_half)
        <= 1e-12 * max(1.0, abs(expect_half)),
    }


def equality_case(alpha: float, chi: float, kappa: float, X: float, nu: float) -> dict:
    # Equality in Young when nu sqrt(Ds) = alpha chi kappa^{3/2} X.
    Ds = ((alpha * chi * (kappa**1.5) * X) / nu) ** 2
    row = young_split(alpha, chi, kappa, X, Ds, nu)
    gap = abs((row["viscous_slot"] + row["remainder"]) - row["envelope"])
    row["D_s"] = Ds
    row["equality_gap"] = gap
    row["equality_ok"] = gap <= 1e-10 * max(1.0, abs(row["envelope"]))
    return row


def a8r_scaling(a: float, nu: float, t: float, Tc_over_Ds_U: float) -> dict:
    # u = a nu t^{-2} U. Homogeneity: Tc ~ amp^3, Ds ~ amp^2.
    amp = a * nu * (t**-2)
    Tc_factor = amp**3
    Ds_factor = amp**2
    ratio = Tc_factor / (nu * Ds_factor)
    expect = a * (t**-2) * Tc_over_Ds_U
    raw = ratio * Tc_over_Ds_U
    return {
        "T_c_over_nu_D_s": raw,
        "expect_a_t_inv2": expect,
        "identity_ok": abs(raw - expect) <= 1e-12 * max(1.0, abs(expect)),
        "order_one_if_Tc_Ds_is_C_t2": abs(a * 1.0 - a) <= 1e-15,
    }


def missing_on_disk() -> dict:
    hits = []
    patterns = (
        "I3_WEIGHTED_TARGET_2026-09-20.md",
        "I3_WEIGHTED_TARGET",
        "A8-R",
        "A8_R",
        "cube-field",
        "cube_field",
        "54/46",
        "54_46",
        "KKL-REGROUP",
        "K_K_L_REGROUP",
    )
    for path in ROOT.rglob("*"):
        if ".git" in path.parts or path.suffix in {".pyc"}:
            continue
        name = path.name
        if any(p in name for p in patterns):
            hits.append(str(path.relative_to(ROOT)))
    return {
        "named_sources": list(MISSING_SOURCES),
        "unexpected_filename_hits": hits,
        "all_named_sources_absent": hits == [],
    }


def run() -> dict:
    covers = []
    samples = (
        (1.0, 1.0, 2.0, 3.0, 0.5, 1.0),
        (0.4, 2.0, 5.0, 1.5, 8.0, 0.25),
        (1.2, 0.7, 0.8, 4.0, 2.0, 3.0),
    )
    all_ok = True
    for args in samples:
        row = young_split(*args)
        covers.append(row)
        all_ok = all_ok and row["covers"] and row["remainder_identity"]
    eq = equality_case(1.0, 1.0, 2.0, 3.0, 0.5)
    all_ok = all_ok and eq["equality_ok"]
    crit = a8r_scaling(a=2.0, nu=0.3, t=4.0, Tc_over_Ds_U=16.0)
    # If Tc/Ds(U) = C t^2 with C=1, t=4 => Tc/Ds=16, ratio = a C = 2.
    crit_C = a8r_scaling(a=2.0, nu=0.3, t=4.0, Tc_over_Ds_U=1.0 * (4.0**2))
    all_ok = all_ok and crit["identity_ok"] and crit_C["identity_ok"]
    missing = missing_on_disk()
    return {
        "ns_solved": False,
        "envelope_proved": False,
        "occupation_proved": False,
        "nu_dropped": False,
        "occupation_condition": "int alpha^2 chi^2 kappa X dt / nu < infinity",
        "remainder_over_Y": "alpha^2 chi^2 kappa X / (2 nu)",
        "covers_samples": all_ok,
        "samples": covers,
        "equality": eq,
        "a8r_scaling": crit,
        "a8r_critical_ratio": crit_C,
        "a8r_construction_on_this_tree": False,
        "a8r_leading_coefficient_proved": False,
        "missing_sources": missing,
        "i3_weighted_proved_internally": False,
        "kkl_regrouping_proved_internally": False,
        "fiber_verdict_separated": "NEUTRAL",
        "comparable_KKK": "OPEN",
        "q4_0_executed": False,
        "da_ns_2": "OPEN",
        "gate_altered": {
            "sbp": False,
            "phi_vs_d": False,
            "low_tail_snapshot": False,
            "sign_realizability": False,
            "s_pq": False,
        },
        "all_identities_ok": all_ok and missing["all_named_sources_absent"],
    }


def main() -> int:
    payload = run()
    out = ROOT / "results" / "da_gate_young_occupation_nu.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, indent=2))
    return 0 if payload["all_identities_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
