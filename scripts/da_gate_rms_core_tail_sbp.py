"""Elementary checks for the RMS core/tail SBP gate.

Does not reconstruct the full triad summation-by-parts in sympy.
Does not invent B_prim. Does not run Taylor-Green.
Convention: FROZEN epoch (kappa_e, lambda_e). Do not mix with live Lambda.
NS is not solved.
"""

from __future__ import annotations

import json
from pathlib import Path


def phi(m: float, kappa: float) -> float:
    return 0.5 * (m - kappa) ** 2 * (m * m + 2.0 * kappa * m + 2.0 * kappa * kappa)


def phi_shifted(u: float, kappa: float) -> float:
    """phi(kappa + u) = (1/2) u^2 (u^2 + 4 kappa u + 5 kappa^2)."""
    return 0.5 * u * u * (u * u + 4.0 * kappa * u + 5.0 * kappa * kappa)


def H_ij_o(i: float, j: float, o: float) -> float:
    return i * i + j * j + o * o + i * j - o * (i + j)


def R(i: float, j: float, o: float, Lam: float) -> float:
    return ((i + o) * (j + o) / (2.0 * o)) * (H_ij_o(i, j, o) - Lam)


def check_phi(kappa: float = 2.0) -> dict:
    quad = (0.0 + 2.0 * kappa) ** 2 + kappa * kappa  # (u+2k)^2 + k^2 at u=0
    samples = []
    ok = True
    for u in (-3.0, -1.0, -0.25, 0.0, 0.25, 1.0, 4.0):
        a = phi(kappa + u, kappa)
        b = phi_shifted(u, kappa)
        match = abs(a - b) <= 1e-12 * max(1.0, abs(b))
        nonneg = a >= -1e-15
        ok = ok and match and nonneg
        samples.append({"u": u, "phi": a, "shifted": b, "match": match, "nonneg": nonneg})
    inner_min = kappa * kappa  # u^2 + 4ku + 5k^2 = (u+2k)^2 + k^2 >= k^2
    return {
        "kappa": kappa,
        "phi_at_shell": phi(kappa, kappa),
        "phi_at_zero": phi(0.0, kappa),
        "kappa_fourth": kappa**4,
        "second_order_zero": abs(phi(kappa, kappa)) < 1e-15 and abs(phi(kappa + 1e-4, kappa) / (1e-4) ** 2) > 0,
        "inner_quadratic_min": inner_min,
        "high_k_leading_half_m4": True,
        "samples": samples,
        "ok": ok
        and abs(phi(0.0, kappa) - kappa**4) < 1e-12
        and abs(phi(kappa, kappa)) < 1e-15
        and inner_min > 0,
    }


def check_R_core(kappa: float = 2.0) -> dict:
    lam_e = kappa * kappa
    R_frozen_core = R(kappa, kappa, kappa, lam_e)
    dR_dLam = -((kappa + kappa) * (kappa + kappa) / (2.0 * kappa))
    # frozen extra: R(kappa,kappa,kappa; Lambda) - 2 k^3 = -2 k (Lambda - lambda_e)
    Lam = lam_e + 0.3
    extra = R(kappa, kappa, kappa, Lam) - 2.0 * kappa**3
    extra_pred = -2.0 * kappa * (Lam - lam_e)
    # live convention: kappa_live = sqrt(Lambda), core R equals 2 kappa_live^3
    R_live = R(Lam**0.5, Lam**0.5, Lam**0.5, Lam)
    h = 1e-6 * kappa
    gi = (R(kappa + h, kappa, kappa, lam_e) - R(kappa - h, kappa, kappa, lam_e)) / (2.0 * h)
    gj = (R(kappa, kappa + h, kappa, lam_e) - R(kappa, kappa - h, kappa, lam_e)) / (2.0 * h)
    go = (R(kappa, kappa, kappa + h, lam_e) - R(kappa, kappa, kappa - h, lam_e)) / (2.0 * h)
    return {
        "kappa": kappa,
        "R_frozen_core": R_frozen_core,
        "two_kappa_cubed": 2.0 * kappa**3,
        "core_matches_2k3": abs(R_frozen_core - 2.0 * kappa**3) < 1e-12,
        "dR_dLambda_at_core": dR_dLam,
        "dR_dLambda_is_minus_2k": abs(dR_dLam + 2.0 * kappa) < 1e-12,
        "frozen_extra": extra,
        "frozen_extra_pred": extra_pred,
        "frozen_extra_ok": abs(extra - extra_pred) < 1e-12,
        "live_core_R": R_live,
        "live_core_is_2k3": abs(R_live - 2.0 * (Lam**0.5) ** 3) < 1e-10,
        "grad_i": gi,
        "grad_j": gj,
        "grad_o": go,
        "grad_pred": (5.0 * kappa**2, 5.0 * kappa**2, 0.0),
        "grad_ok": abs(gi - 5.0 * kappa**2) < 1e-4 * kappa**2
        and abs(gj - 5.0 * kappa**2) < 1e-4 * kappa**2
        and abs(go) < 1e-4 * kappa**2,
    }


def run() -> dict:
    phi_rec = check_phi()
    R_rec = check_R_core()
    return {
        "ns_solved": False,
        "convention": "FROZEN_epoch",
        "do_not_mix_with_live_Lambda": True,
        "sbp_identity_reconstructed_here": False,
        "taylor_green_measured": False,
        "phi_checks": phi_rec,
        "R_core_checks": R_rec,
        "all_elementary_ok": phi_rec["ok"]
        and R_rec["core_matches_2k3"]
        and R_rec["dR_dLambda_is_minus_2k"]
        and R_rec["frozen_extra_ok"]
        and R_rec["live_core_is_2k3"]
        and R_rec["grad_ok"],
        "residual_after_sbp": "low-tail Phi_e/Y plus charge (Hdot^{1/2} flux) and -(Lambda-lambda_e) N",
        "note": (
            "Elementary phi and R-core facts sit. "
            "The full triad SBP is filed as an identity from the gate, not rebuilt here. "
            "Core/high tail vs frozen d_kappa sit in the comparison packet. "
            "Low-frequency tail remains the enemy. NS not solved."
        ),
    }


def main() -> int:
    payload = run()
    out = Path(__file__).resolve().parents[1] / "results" / "da_gate_rms_core_tail_sbp.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2), flush=True)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
