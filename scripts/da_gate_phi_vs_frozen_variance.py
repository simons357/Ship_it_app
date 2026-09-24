"""Compare the frozen SBP capacity weight phi_kappa with frozen variance d_kappa.

Locks (A), (B), the shell limit 5/(8 kappa^2), and the comparable-annulus
bound (C). Identifies the LOW-FREQUENCY TAIL as the only blow-up of phi/d.
Does not run Taylor-Green. Does not invent B_prim. NS is not solved.

Convention: FROZEN epoch (kappa = kappa_e, lambda_e = kappa^2).
Do not mix with live Lambda.
"""

from __future__ import annotations

import json
from pathlib import Path


def phi(m: float, kappa: float) -> float:
    return 0.5 * (m - kappa) ** 2 * (m * m + 2.0 * kappa * m + 2.0 * kappa * kappa)


def d_weight(m: float, kappa: float) -> float:
    """Frozen spectral-variance weight: m^2 (m^2 - kappa^2)^2."""
    return (m * m) * (m * m - kappa * kappa) ** 2


def ratio_A(m: float, kappa: float) -> float:
    """Exact cancelled ratio for m != kappa."""
    return (m * m + 2.0 * kappa * m + 2.0 * kappa * kappa) / (
        2.0 * m * m * (m + kappa) ** 2
    )


def f_x(x: float) -> float:
    """(x^2 + 2x + 2) / (x^2 (x+1)^2). Continuous at x=1 with value 5/4."""
    return (x * x + 2.0 * x + 2.0) / (x * x * (x + 1.0) ** 2)


def ratio_B(x: float, kappa: float) -> float:
    return (0.5 / (kappa * kappa)) * f_x(x)


def C_ab(a: float) -> float:
    """C(a,b) = (1/2) f(a). Independent of b: f is decreasing on (0, inf)."""
    return 0.5 * f_x(a)


def L_e(kappa: float, E_low: float, Y: float) -> float:
    return (kappa**4 * E_low) / Y


def _rel_close(a: float, b: float, tol: float = 1e-12) -> bool:
    return abs(a - b) <= tol * max(1.0, abs(b))


def check_ratio_identities(kappa: float = 3.0) -> dict:
    samples = []
    ok = True
    for m in (0.25, 0.5, 1.0, 2.0, 2.9, 3.1, 6.0, 12.0, 30.0):
        ph = phi(m, kappa)
        dw = d_weight(m, kappa)
        raw = ph / dw
        a = ratio_A(m, kappa)
        x = m / kappa
        b = ratio_B(x, kappa)
        match_a = _rel_close(raw, a)
        match_b = _rel_close(raw, b)
        ok = ok and match_a and match_b
        samples.append(
            {
                "m": m,
                "x": x,
                "phi_over_d": raw,
                "ratio_A": a,
                "ratio_B": b,
                "match_A": match_a,
                "match_B": match_b,
            }
        )
    # shell limit of the cancelled ratio
    x_shell = 1.0
    lim = ratio_B(x_shell, kappa)
    lim_pred = 5.0 / (8.0 * kappa * kappa)
    # raw phi/d approaches the cancelled limit; shrink dx twice
    sides = []
    sides_ok = True
    for dx in (1e-3, 1e-4, 1e-5):
        left = phi(kappa * (1.0 - dx), kappa) / d_weight(kappa * (1.0 - dx), kappa)
        right = phi(kappa * (1.0 + dx), kappa) / d_weight(kappa * (1.0 + dx), kappa)
        err = max(abs(left - lim_pred), abs(right - lim_pred))
        sides.append({"dx": dx, "left": left, "right": right, "abs_err": err})
        sides_ok = sides_ok and err < 20.0 * dx * lim_pred
    return {
        "kappa": kappa,
        "samples": samples,
        "shell_limit": lim,
        "shell_limit_pred": lim_pred,
        "shell_limit_ok": _rel_close(lim, lim_pred) and sides_ok,
        "side_approach": sides,
        "C_at_shell": C_ab(1.0),
        "C_at_shell_is_5_8": _rel_close(C_ab(1.0), 5.0 / 8.0),
        "ok": ok
        and _rel_close(lim, lim_pred)
        and sides_ok
        and _rel_close(C_ab(1.0), 5.0 / 8.0),
    }


def check_f_decreasing() -> dict:
    """f'(x)<0 on (0,inf) because the logarithmic derivative bracket is negative.

    n = x^2+2x+2, d = x^2 (x+1)^2,
    n'd - n d' = 2x(x+1) [ -x^3 - 3x^2 - 5x - 2 ] < 0 for x>0.
    """
    grid = [10 ** t for t in (-3, -2, -1, -0.5, 0.0, 0.3, 0.6, 1.0, 1.5)]
    vals = [f_x(x) for x in grid]
    monotone = all(vals[i] > vals[i + 1] for i in range(len(vals) - 1))
    brackets = []
    ok_poly = True
    for x in (0.1, 0.5, 1.0, 2.0, 7.0):
        bracket = -(x**3) - 3.0 * x * x - 5.0 * x - 2.0
        # unique expansion of the derivative numerator factor
        expand = -((x + 1.0) * (x * x + 2.0 * x + 2.0) + x)
        match = _rel_close(bracket, expand)
        ok_poly = ok_poly and match and bracket < 0
        brackets.append({"x": x, "bracket": bracket, "expand": expand, "match": match})
    # C(a,b) depends only on the inner edge
    a, b = 0.4, 2.5
    C_from_a = C_ab(a)
    # max of (1/2) f on a sample of [a,b] must sit at a
    xs = [a + (b - a) * i / 200.0 for i in range(201)]
    C_num = 0.5 * max(f_x(x) for x in xs)
    C_ok = _rel_close(C_from_a, C_num, tol=1e-9)
    return {
        "monotone_on_log_grid": monotone,
        "bracket_negative": ok_poly,
        "brackets": brackets,
        "C_ab_inner_edge": C_from_a,
        "C_ab_sampled_max": C_num,
        "C_independent_of_b": C_ok,
        "ok": monotone and ok_poly and C_ok,
    }


def check_asymptotics(kappa: float = 5.0) -> dict:
    # high tail: phi/d ~ 1/(2 m^2)
    high = []
    high_ok = True
    for m in (50.0, 100.0, 400.0):
        raw = phi(m, kappa) / d_weight(m, kappa)
        pred = 1.0 / (2.0 * m * m)
        rel = abs(raw / pred - 1.0)
        high_ok = high_ok and rel < 0.05
        high.append({"m": m, "ratio": raw, "pred_1_over_2m2": pred, "rel_err": rel})
    # low tail: phi/d ~ 1/m^2
    low = []
    low_ok = True
    for m in (0.05, 0.1, 0.2):
        raw = phi(m, kappa) / d_weight(m, kappa)
        pred = 1.0 / (m * m)
        rel = abs(raw / pred - 1.0)
        low_ok = low_ok and rel < 0.05
        low.append({"m": m, "ratio": raw, "pred_1_over_m2": pred, "rel_err": rel})
    # phi(0) = kappa^4 agrees with the cheap low-tail proxy
    return {
        "kappa": kappa,
        "high_tail": high,
        "high_tail_favorable_1_over_2m2": high_ok,
        "low_tail": low,
        "low_tail_blows_1_over_m2": low_ok,
        "phi_at_zero": phi(0.0, kappa),
        "kappa_fourth": kappa**4,
        "phi_zero_is_kappa_fourth": _rel_close(phi(0.0, kappa), kappa**4),
        "ok": high_ok and low_ok and _rel_close(phi(0.0, kappa), kappa**4),
    }


def check_core_bound(kappa: float = 4.0) -> dict:
    """On a kappa <= m <= b kappa, Phi_core <= C(a,b)/kappa^2 D_frozen_core."""
    a, b = 0.5, 2.0
    C = C_ab(a)
    worst = []
    ok = True
    for x in (0.5, 0.75, 1.0, 1.25, 2.0):
        m = x * kappa
        if abs(x - 1.0) < 1e-15:
            ratio = ratio_B(1.0, kappa)
        else:
            ratio = phi(m, kappa) / d_weight(m, kappa)
        bound = C / (kappa * kappa)
        ok = ok and ratio <= bound * (1.0 + 1e-12)
        worst.append({"x": x, "ratio": ratio, "bound": bound, "ok": ratio <= bound * (1.0 + 1e-12)})
    return {
        "kappa": kappa,
        "a": a,
        "b": b,
        "C_ab": C,
        "C_pred_from_inner_edge": (a * a + 2.0 * a + 2.0) / (2.0 * a * a * (a + 1.0) ** 2),
        "uniform_bound": C / (kappa * kappa),
        "samples": worst,
        "ok": ok and _rel_close(C, (a * a + 2.0 * a + 2.0) / (2.0 * a * a * (a + 1.0) ** 2)),
    }


def check_energy_does_not_pay() -> dict:
    """Ordinary energy / Y_low bounds do not control L_e at high kappa."""
    kappa = 20.0
    # high-frequency core + small low-frequency population
    E_core = 1.0
    E_low = 0.04
    m_core = kappa
    m_low = 1.0
    Y = (m_core**4) * E_core + (m_low**4) * E_low
    Y_low = (m_low**4) * E_low
    E0 = E_core + E_low
    Le = L_e(kappa, E_low, Y)
    Phi_low = phi(m_low, kappa) * E_low
    Phi_core = phi(m_core, kappa) * E_core
    Phi = Phi_low + Phi_core
    low_share = Phi_low / Phi if Phi else 0.0
    # kappa^4 E_low <= kappa^4 Y_low is true and useless (Y_low = E_low here)
    useless = (kappa**4) * Y_low
    # kappa^4 E0 / Y is order 1 and does not force L_e small
    energy_ratio = (kappa**4) * E0 / Y
    return {
        "illustration_only": True,
        "taylor_green": False,
        "kappa": kappa,
        "E_core": E_core,
        "E_low": E_low,
        "Y": Y,
        "Y_low": Y_low,
        "L_e": Le,
        "Phi_low": Phi_low,
        "Phi_core": Phi_core,
        "Phi_over_Y": Phi / Y,
        "low_tail_share_of_Phi": low_share,
        "Phi_is_low_tail_dominated": low_share > 0.99,
        "kappa4_Y_low": useless,
        "kappa4_E0_over_Y": energy_ratio,
        "energy_bound_forces_L_e_small": False,
        "Y_low_bound_useful_at_high_kappa": False,
        "ok": low_share > 0.99 and energy_ratio > 1.0,
    }


def run() -> dict:
    ids = check_ratio_identities()
    dec = check_f_decreasing()
    asym = check_asymptotics()
    core = check_core_bound()
    energy = check_energy_does_not_pay()
    return {
        "ns_solved": False,
        "convention": "FROZEN_epoch",
        "do_not_mix_with_live_Lambda": True,
        "taylor_green_measured": False,
        "enemy": "LOW-FREQUENCY TAIL",
        "ratio_identities": ids,
        "f_decreasing": dec,
        "asymptotics": asym,
        "core_bound": core,
        "energy_does_not_pay": energy,
        "solver_diagnostic": "L_e = kappa_e^4 E_low / Y (or exact phi_e low-tail / Y)",
        "rally": "LOW-TAIL CAPACITY + CHARGE + EPOCH MOTION",
        "all_elementary_ok": ids["ok"]
        and dec["ok"]
        and asym["ok"]
        and core["ok"]
        and energy["ok"],
        "note": (
            "phi/d identities (A)(B), shell limit 5/(8 kappa^2), and "
            "comparable-annulus bound (C) sit. High tail is favorable "
            "(~1/(2m^2)). Low tail blows (~1/m^2). Energy / Y_low do not "
            "pay L_e. TG 64/96 not on this tree. NS not solved."
        ),
    }


def main() -> int:
    payload = run()
    out = Path(__file__).resolve().parents[1] / "results" / "da_gate_phi_vs_frozen_variance.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2), flush=True)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
