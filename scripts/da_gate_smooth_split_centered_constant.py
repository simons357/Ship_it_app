"""Smooth-split finite centered constant: identities and six-mode family.

Instantaneous estimate on finite Fourier fields. Not NSE regularity.
Unrestricted star stays dead. Time budget stays open. NS is not solved.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import centered_drift_triad_test as cdt  # noqa: E402
import da_gate_tc_l3_sqrt_yds as l3  # noqa: E402
import growing_layer_counterexample as gl  # noqa: E402
import ns_lemma_star_core as core  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "da_gate_smooth_split_centered_constant.json"


def _jsonable(obj):
    if isinstance(obj, dict):
        return {str(k): _jsonable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_jsonable(v) for v in obj]
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.floating,)):
        return float(obj)
    if isinstance(obj, float) and (math.isnan(obj) or math.isinf(obj)):
        return None
    return obj


def chi_hat(s_over_lam: float) -> float:
    """C^0 cutoff with the proof's supports: 1 on [0,1/4], 0 on [1/2, inf)."""
    x = float(s_over_lam)
    if x <= 0.25:
        return 1.0
    if x >= 0.5:
        return 0.0
    t = (x - 0.25) / 0.25
    return 1.0 - t


def split_field(field: core.Field, lam: float) -> tuple[core.Field, core.Field]:
    v = core.Field()
    h = core.Field()
    seen = set()
    for k, vk in field.modes.items():
        if k in seen:
            continue
        nk = (-k[0], -k[1], -k[2])
        seen.add(k)
        seen.add(nk)
        s = core.lam(k)
        c = chi_hat(s / lam if lam > 0 else 0.0)
        if c != 0.0:
            v.set_mode(k, c * vk)
        if c != 1.0:
            h.set_mode(k, (1.0 - c) * vk)
    return v, h


def N_of(field: core.Field) -> float:
    total = 0.0
    for k, vk in field.modes.items():
        Bk = core.B_hat_at(field, k)
        Tk = -float(np.real(np.dot(Bk, np.conj(vk))))
        total += core.lam(k) * Tk
    return total


def M_of(field: core.Field) -> float:
    total = 0.0
    for k, vk in field.modes.items():
        Bk = core.B_hat_at(field, k)
        Tk = -float(np.real(np.dot(Bk, np.conj(vk))))
        ell = core.lam(k)
        total += ell * ell * Tk
    return total


def six_mode(j: int) -> core.Field:
    if j < 3:
        raise ValueError("j >= 3")
    field = core.Field()
    inv = j ** (-0.5)
    field.set_mode((1, 0, 0), np.array([0.0, 1.0, 0.0], dtype=complex))
    field.set_mode((j, j, 0), np.array([0.0, 0.0, inv], dtype=complex))
    field.set_mode((1 + j, j, 0), np.array([0.0, 0.0, 1j * inv], dtype=complex))
    return field


def grad_L2_from_modes(field: core.Field) -> float:
    return math.sqrt(sum(core.lam(k) * float(np.vdot(vk, vk).real) for k, vk in field.modes.items()))


def A_L2(field: core.Field) -> float:
    return math.sqrt(
        sum((core.lam(k) ** 2) * float(np.vdot(vk, vk).real) for k, vk in field.modes.items())
    )


def grad_Aw_L2(field: core.Field, lam: float) -> float:
    return math.sqrt(
        sum(
            core.lam(k) * ((core.lam(k) - lam) ** 2) * float(np.vdot(vk, vk).real)
            for k, vk in field.modes.items()
        )
    )


def split_bounds(field: core.Field) -> dict:
    rec = core.R_star(field)
    lam = float(rec["Lambda"])
    ds = float(rec["D_s"])
    y = float(rec["Y"])
    v, h = split_field(field, lam)
    gv = grad_L2_from_modes(v)
    eh = math.sqrt(h.energy())
    ah = A_L2(h)
    gwh = grad_Aw_L2(h, lam)
    return {
        "Lambda": lam,
        "D_s": ds,
        "Y": y,
        "Lambda_grad_v": lam * gv,
        "two_sqrt_Ds": 2.0 * math.sqrt(ds) if ds > 0 else 0.0,
        "low_ok": bool(lam * gv <= 2.0 * math.sqrt(ds) + 1e-9),
        "Lambda_h": lam * eh,
        "four_sqrt_Y": 4.0 * math.sqrt(y),
        "high_amp_ok": bool(lam * eh <= 4.0 * math.sqrt(y) + 1e-9),
        "Ah": ah,
        "Ah_ok": bool(ah <= math.sqrt(y) + 1e-9),
        "grad_A_minus_Lambda_h": gwh,
        "sqrt_Ds": math.sqrt(ds) if ds > 0 else 0.0,
        "high_spread_ok": bool(gwh <= math.sqrt(ds) + 1e-9),
        "v_max_s": max((core.lam(k) for k in v.modes), default=0.0),
        "h_min_s": min((core.lam(k) for k in h.modes), default=float("inf")),
        "v_supported_le_half": bool(
            all(core.lam(k) <= lam / 2 + 1e-12 for k in v.modes)
        ),
        "h_vanishes_le_quarter": bool(
            all(core.lam(k) >= lam / 4 - 1e-12 for k in h.modes)
        ),
    }


def score_six(j: int) -> dict:
    field = six_mode(j)
    rec = core.R_star(field)
    N = N_of(field)
    M = M_of(field)
    grid = l3.physical_grad_norms(field)
    y = float(rec["Y"])
    ds = float(rec["D_s"])
    lam = float(rec["Lambda"])
    tc = float(rec["T_c"])
    g = grid["grad_L3"]
    sqrt_yds = math.sqrt(y * ds) if y > 0 and ds > 0 else float("nan")
    n_form = -2.0 * (2 * j + 1)
    width = ds / (lam * y) if lam > 0 and y > 0 else None
    quot = abs(lam * N) / (g * sqrt_yds) if sqrt_yds == sqrt_yds and g > 0 else None
    tc_quot = abs(tc) / (g * sqrt_yds) if sqrt_yds == sqrt_yds and g > 0 else None
    return {
        "j": j,
        "n_modes": len(field.modes),
        "E": rec["E"],
        "X": rec["X"],
        "Y": y,
        "Lambda": lam,
        "D_s": ds,
        "N": N,
        "M": M,
        "T_c": tc,
        "N_formula": n_form,
        "N_matches_formula": bool(abs(N - n_form) <= 1e-8 * max(1.0, abs(n_form))),
        "R_star": rec["R_star"],
        "Ds_over_Lambda_Y": width,
        "width_times_4j": (width * 4 * j) if width is not None else None,
        "Lambda_N_over_g_sqrtYDs": quot,
        "T_c_over_g_sqrtYDs": tc_quot,
        "grad_L3": g,
        "grad_L2_matches_sqrt_X": bool(abs(grid["grad_L2"] - math.sqrt(rec["X"])) <= 1e-8 * math.sqrt(rec["X"])),
        **{f"split_{k}": v for k, v in split_bounds(field).items() if k.endswith("_ok") or k in ("v_supported_le_half", "h_vanishes_le_quarter")},
    }


def amgm_packaging() -> dict:
    """|Tc| <= C g sqrt(Y Ds) => (log Lambda)' <= C^2 g^2 / (2 nu) by AM-GM."""
    # Symbolic check with numbers: a = C g sqrt(Y), then a sqrt(Ds) - nu Ds <= a^2/(4 nu)
    C, g, Y, Ds, nu = 2.0, 3.0, 5.0, 1.7, 0.4
    a = C * g * math.sqrt(Y)
    lhs = a * math.sqrt(Ds) - nu * Ds
    rhs = a * a / (4.0 * nu)
    pack = 2.0 * rhs / Y
    claimed = (C * C * g * g) / (2.0 * nu)
    return {
        "amgm_ok": bool(lhs <= rhs + 1e-12),
        "log_lambda_pack_ok": bool(abs(pack - claimed) <= 1e-12 * max(1.0, claimed)),
        "claimed": r"(log Lambda)' <= C^2 g^2 / (2 nu)",
    }


def fx_from_classical_N() -> dict:
    """|N| <= Cs g sqrt(X Y) => (log X)' <= 2(Cs g sqrt(Lambda) - nu Lambda) = F_X (unsigned)."""
    Cs, g, X, Y, nu = 1.3, 2.0, 4.0, 9.0, 0.5
    lam = Y / X
    Nbound = Cs * g * math.sqrt(X * Y)
    logx = -2.0 * nu * lam + 2.0 * Nbound / X
    Fx = 2.0 * (Cs * g * math.sqrt(lam) - nu * lam)
    return {
        "classical_implies_Fx": bool(abs(logx - Fx) <= 1e-12 * max(1.0, abs(Fx))),
        "Fx_formula": r"F_X = 2 (Cs g sqrt(Lambda) - nu Lambda)_+",
        "active_when": r"g > nu sqrt(Lambda) / Cs",
    }


def constant_arithmetic() -> dict:
    # |Tc-Lambda N| <= 3 Cs g sqrt(YDs)
    # |Lambda N| <= (4 + 6 M) Cs g sqrt(YDs)
    # |Tc| <= (7 + 6 M) Cs g sqrt(YDs)
    m = 2.5
    step1 = 3.0
    lamN = 4.0 + 6.0 * m
    tc = step1 + lamN
    return {
        "step1": 3.0,
        "lambda_N_coeff": "4 + 6 M_mult",
        "Tc_coeff": "7 + 6 M_mult",
        "sum_ok": bool(abs(tc - (7.0 + 6.0 * m)) < 1e-15),
        "M_mult": "1 + int |K|",
    }


def run() -> dict:
    note = cdt.near_scale_triad()
    note_rec = core.R_star(note)
    note_N = N_of(note)
    note_split = split_bounds(note)
    note_grid = l3.physical_grad_norms(note)
    note_g = note_grid["grad_L3"]
    note_sqrt = math.sqrt(note_rec["Y"] * note_rec["D_s"])
    note_tc_q = abs(note_rec["T_c"]) / (note_g * note_sqrt)
    note_lamN_q = abs(note_rec["Lambda"] * note_N) / (note_g * note_sqrt)

    six = [score_six(j) for j in (3, 4, 6, 8, 12)]
    six_N_ok = all(r["N_matches_formula"] for r in six)
    six_quot_decays = all(
        six[i]["Lambda_N_over_g_sqrtYDs"] > six[i + 1]["Lambda_N_over_g_sqrtYDs"]
        for i in range(len(six) - 1)
    )
    six_width_near = all(abs(r["width_times_4j"] - 1.0) < 0.35 for r in six)

    vn1 = split_bounds(gl.growing_layer(1))
    split_ok = all(
        note_split[k] and vn1[k] and all(r[f"split_{k}"] for r in six)
        for k in ("low_ok", "high_amp_ok", "Ah_ok", "high_spread_ok", "v_supported_le_half", "h_vanishes_le_quarter")
    )

    seated = [note_tc_q, note_lamN_q] + [r["T_c_over_g_sqrtYDs"] for r in six] + [
        r["Lambda_N_over_g_sqrtYDs"] for r in six
    ]
    seated_max = max(seated)
    return {
        "ns_solved": False,
        "time_budget_proved": False,
        "unrestricted_star_restored": False,
        "crossover_stamped": False,
        "optimized_C_computed": False,
        "instantaneous_estimate_written": True,
        "witness_C_gt_0p4_recomputed": False,
        "witness_C_gt_0p4_status": "REPORTED_from_handoff_not_recovered_on_seated_families",
        "seated_max_Tc_or_LambdaN_over_g_sqrtYDs": seated_max,
        "constant_arithmetic": constant_arithmetic(),
        "amgm": amgm_packaging(),
        "Fx": fx_from_classical_N(),
        "note_triad": {
            "T_c": note_rec["T_c"],
            "N": note_N,
            "Lambda": note_rec["Lambda"],
            "T_c_over_g_sqrtYDs": note_tc_q,
            "Lambda_N_over_g_sqrtYDs": note_lamN_q,
            "split": {k: note_split[k] for k in note_split if k.endswith("_ok") or "support" in k or "vanish" in k},
        },
        "six_mode": six,
        "six_mode_N_formula_ok": six_N_ok,
        "six_mode_LambdaN_quotient_decreases": six_quot_decays,
        "six_mode_width_near_one_over_4j": six_width_near,
        "split_inequalities_ok": split_ok,
        "all_identities_ok": bool(
            split_ok
            and six_N_ok
            and six_quot_decays
            and constant_arithmetic()["sum_ok"]
            and amgm_packaging()["amgm_ok"]
            and amgm_packaging()["log_lambda_pack_ok"]
            and fx_from_classical_N()["classical_implies_Fx"]
        ),
        "gate_altered": {
            "sbp": False,
            "phi_vs_d": False,
            "low_tail_snapshot": False,
            "sign_realizability": False,
            "s_pq": False,
            "local_star": False,
        },
        "note": (
            "Instantaneous |Tc| <= (7+6 M_mult) Cs g sqrt(Y Ds) on finite "
            "Fourier fields. Derivation is the reviewable basis. Time budget "
            "and NSE regularity remain open. Unrestricted star stays dead. "
            "NS not solved."
        ),
    }


def main() -> int:
    payload = _jsonable(run())
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2), flush=True)
    print(f"wrote {OUT}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
