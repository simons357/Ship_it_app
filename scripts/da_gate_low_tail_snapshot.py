"""Snapshot L_e / Phi split on families already on this tree.

Locks the exact polynomial
    phi(m) = kappa^4 - kappa^3 m - (1/2) kappa^2 m^2 + (1/2) m^4
hence
    Phi_e = kappa^4 E - kappa^3 H - (1/2) kappa^2 X + (1/2) Y
with H = ||u||_{Hdot^{1/2}}^2 = sum |k| |a_k|^2.

Snapshot convention: freeze kappa_e = sqrt(Lambda) of the current field.
That is a diagnostic at a frozen-at-now epoch. It is not mixed into the
SBP identity, and it makes the moving term vanish by construction.
Not Taylor-Green. Not a theorem. NS is not solved.
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
import centered_width_crossover as width  # noqa: E402
import da_gate_phi_vs_frozen_variance as cmp  # noqa: E402
import growing_layer_counterexample as gl  # noqa: E402
import ns_lemma_star_core as core  # noqa: E402


def phi_poly(m: float, kappa: float) -> float:
    return (
        kappa**4
        - (kappa**3) * m
        - 0.5 * (kappa**2) * (m * m)
        + 0.5 * (m**4)
    )


def check_polynomial(kappa: float = 3.0) -> dict:
    samples = []
    ok = True
    for m in (0.0, 0.4, 1.0, kappa, 5.0, 12.0):
        a = cmp.phi(m, kappa)
        b = phi_poly(m, kappa)
        match = abs(a - b) <= 1e-12 * max(1.0, abs(a))
        ok = ok and match
        samples.append({"m": m, "phi": a, "poly": b, "match": match})
    return {
        "kappa": kappa,
        "samples": samples,
        "phi_at_zero_is_kappa_fourth": abs(phi_poly(0.0, kappa) - kappa**4) < 1e-12,
        "phi_at_shell_is_zero": abs(phi_poly(kappa, kappa)) < 1e-12,
        "ok": ok,
    }


def field_weights(field: core.Field, kappa: float) -> dict:
    E = H = X = Y = Phi = D_frozen = 0.0
    min_m = float("inf")
    max_m = 0.0
    for k, vk in field.modes.items():
        e = float(np.vdot(vk, vk).real)
        m = math.sqrt(core.lam(k))
        min_m = min(min_m, m)
        max_m = max(max_m, m)
        E += e
        H += m * e
        X += (m * m) * e
        Y += (m**4) * e
        Phi += cmp.phi(m, kappa) * e
        D_frozen += cmp.d_weight(m, kappa) * e
    Phi_moments = (kappa**4) * E - (kappa**3) * H - 0.5 * (kappa**2) * X + 0.5 * Y
    return {
        "E": E,
        "H_hdot_half": H,
        "X": X,
        "Y": Y,
        "Phi": Phi,
        "Phi_from_moments": Phi_moments,
        "moments_match": abs(Phi - Phi_moments) <= 1e-10 * max(1.0, abs(Phi)),
        "D_frozen": D_frozen,
        "min_m": min_m,
        "max_m": max_m,
    }


def split_field(field: core.Field, a: float = 0.5, b: float = 2.0) -> dict:
    """Snapshot freeze kappa = sqrt(Lambda). Low: m < a kappa; high: m > b kappa."""
    E, X, Y, Z, Lam = core.moments(field)
    kappa = math.sqrt(Lam) if Lam > 0 else float("nan")
    w = field_weights(field, kappa)
    low = {"E": 0.0, "Phi": 0.0, "Y": 0.0, "D_frozen": 0.0, "n_modes": 0}
    core_b = {"E": 0.0, "Phi": 0.0, "Y": 0.0, "D_frozen": 0.0, "n_modes": 0}
    high = {"E": 0.0, "Phi": 0.0, "Y": 0.0, "D_frozen": 0.0, "n_modes": 0}
    for k, vk in field.modes.items():
        e = float(np.vdot(vk, vk).real)
        m = math.sqrt(core.lam(k))
        ph = cmp.phi(m, kappa) * e
        yy = (m**4) * e
        df = cmp.d_weight(m, kappa) * e
        x = m / kappa if kappa else float("inf")
        if x < a:
            bucket = low
        elif x > b:
            bucket = high
        else:
            bucket = core_b
        bucket["E"] += e
        bucket["Phi"] += ph
        bucket["Y"] += yy
        bucket["D_frozen"] += df
        bucket["n_modes"] += 1
    Phi = w["Phi"]
    Le = (kappa**4 * low["E"] / Y) if Y else float("nan")
    Phi_over_Y = Phi / Y if Y else float("nan")
    low_share = low["Phi"] / Phi if Phi > 1e-30 else 0.0
    return {
        "convention": "SNAPSHOT_kappa_eq_sqrt_Lambda",
        "not_mixed_into_sbp_identity": True,
        "a": a,
        "b": b,
        "E": E,
        "X": X,
        "Y": Y,
        "Lambda": Lam,
        "kappa": kappa,
        "H_hdot_half": w["H_hdot_half"],
        "Phi": Phi,
        "Phi_from_moments": w["Phi_from_moments"],
        "moments_match": w["moments_match"],
        "D_frozen": w["D_frozen"],
        "min_m": w["min_m"],
        "max_m": w["max_m"],
        "min_x": w["min_m"] / kappa if kappa else float("nan"),
        "max_x": w["max_m"] / kappa if kappa else float("nan"),
        "has_low_tail": low["n_modes"] > 0,
        "L_e": Le,
        "Phi_over_Y": Phi_over_Y,
        "low_tail_share_of_Phi": low_share,
        "Phi_is_low_tail_dominated": bool(Phi > 1e-30 and low_share > 0.5),
        "low": low,
        "core": core_b,
        "high": high,
    }


def run() -> dict:
    poly = check_polynomial()
    note = split_field(cdt.near_scale_triad())
    sep = []
    for L in (2, 4, 8, 16):
        rec = split_field(cdt.separated_triad(L))
        sep.append({"L": L, **rec})
    vn = []
    for n in (1, 2, 4, 8):
        rec = split_field(gl.growing_layer(n))
        vn.append({"n": n, **rec})
    near = []
    for eps in (0.2, 0.05, 0.025):
        field = width.annular_field(5, 4, eps)
        if field is None:
            continue
        rec = split_field(field)
        near.append({"eps": eps, **rec})
    all_match = (
        poly["ok"]
        and note["moments_match"]
        and all(r["moments_match"] for r in sep)
        and all(r["moments_match"] for r in vn)
        and all(r["moments_match"] for r in near)
    )
    # v_n lives on m >= n; snapshot kappa is Theta(n). No room for m/kappa -> 0.
    # v_n: min_m = n scales with kappa; a=1/2 nicks the inner edge of a fat annulus.
    vn_min_x = [r["min_x"] for r in vn]
    vn_min_m_scales = all(abs(r["min_m"] / r["n"] - 1.0) < 1e-12 for r in vn)
    vn_cut_at_0p4 = [split_field(gl.growing_layer(r["n"]), a=0.4, b=2.0) for r in vn]
    vn_no_low_at_0p4 = all(not r["has_low_tail"] for r in vn_cut_at_0p4)
    # separated triad: m=1 frozen under kappa ~ L. Phi/Y and L_e -> 1/3.
    sep_has_low = all(r["has_low_tail"] for r in sep if r["L"] >= 4)
    sep_low_dom = all(r["Phi_is_low_tail_dominated"] for r in sep if r["L"] >= 4)
    sep_Le = [r["L_e"] for r in sep]
    sep_limit_third = abs(sep[-1]["L_e"] - 1.0 / 3.0) < 0.01
    # core comparison (C) on the comparable band, using inner edge of that band
    def core_bound_ok(rec: dict) -> bool:
        kappa = rec["kappa"]
        a_used = rec["a"]
        C = cmp.C_ab(a_used)
        bound = (C / (kappa * kappa)) * rec["core"]["D_frozen"]
        return rec["core"]["Phi"] <= bound * (1.0 + 1e-9) + 1e-12

    core_ok = all(core_bound_ok(r) for r in [note] + sep + vn + near)
    return {
        "ns_solved": False,
        "taylor_green_measured": False,
        "snapshot_only": True,
        "do_not_mix_with_sbp_identity": True,
        "polynomial": poly,
        "note_triad": note,
        "separated": sep,
        "growing_layer": vn,
        "near_shell": near,
        "v_n_min_x": vn_min_x,
        "v_n_min_m_equals_n": vn_min_m_scales,
        "v_n_has_no_low_tail_at_a_0p4": vn_no_low_at_0p4,
        "v_n_cut_at_a_0p4": [
            {"n": n, "has_low_tail": r["has_low_tail"], "L_e": r["L_e"], "min_x": r["min_x"]}
            for n, r in zip((1, 2, 4, 8), vn_cut_at_0p4)
        ],
        "separated_L_ge_4_has_low_tail": sep_has_low,
        "separated_Phi_low_tail_dominated": sep_low_dom,
        "separated_L_e": sep_Le,
        "separated_L_e_approaches_one_third": sep_limit_third,
        "core_bound_C_holds_on_comparable_band": core_ok,
        "all_identities_ok": all_match and vn_min_m_scales and vn_no_low_at_0p4 and core_ok,
        "note": (
            "phi = kappa^4 - kappa^3 m - (1/2) kappa^2 m^2 + (1/2) m^4 is exact. "
            "Phi_e is therefore a combination of E, Hdot^{1/2}, X, Y. "
            "Snapshot freeze is kappa=sqrt(Lambda) of the current field. "
            "v_n is a comparable annulus: min_m = n scales with kappa; "
            "a=1/2 nicks the inner edge, a=0.4 leaves no low tail. "
            "Separated triad is the on-tree high-core + m=1 reservoir; "
            "Phi is low-tail dominated and L_e -> 1/3. "
            "TG 64/96 not on this tree. NS not solved."
        ),
    }


def main() -> int:
    payload = run()
    out = Path(__file__).resolve().parents[1] / "results" / "da_gate_low_tail_snapshot.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2), flush=True)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
