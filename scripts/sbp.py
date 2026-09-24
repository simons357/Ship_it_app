"""Score the incoming SBP / Φ_e gate. Not a close.

φ_e(m) = ½(m-κ_e)²(m²+2κ_e m+2κ_e²) ≥ 0.
Φ_e = Σ φ_e(|k|)|a_k|² = ½Y - ½λ_e X - κ_e³ H_{1/2} + λ_e² E.

If (d/dt)_NL H_{1/2} = 2 Q_a, sitting X'=2N, Y'=2M, E'=0
(nonlinear parts) give the elementary rewrite
    T_c = (d/dt)_NL Φ_e + 2κ_e³ Q_a - (Λ-λ_e) N.
That identity moves the tail into Φ_e. It does not pay it.

Λ is |k|². κ=√Λ. Frozen λ_e=κ_e². Do not mix with live κ(t).
N is not S_Γ. Φ_e is not Ψ. Do not invent a bridge.

Does not overwrite stokes_moments.py.
Does not restore ★.
Does not seat B★ or DA-NS-2.
Does not start leftover 1.
Does not run Taylor–Green.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from centered_ledger import two_shell_moments  # noqa: E402

OUT = ROOT / "results" / "sbp.json"


def phi_e(m: float, ke: float) -> float:
    return 0.5 * (m - ke) ** 2 * (m * m + 2.0 * ke * m + 2.0 * ke * ke)


def phi_e_expand(m: float, ke: float) -> float:
    return 0.5 * m**4 - 0.5 * (ke**2) * (m**2) - (ke**3) * m + ke**4


def R_het(i: float, j: float, o: float, lam: float) -> float:
    """R = ((i+o)(j+o)/(2o)) (H - Λ), H = i²+j²+o²+ij-o(i+j)."""
    a = ((i + o) * (j + o)) / (2.0 * o)
    h = i * i + j * j + o * o + i * j - o * (i + j)
    return a * (h - lam)


def record() -> dict:
    ke = 3.0
    samples = [0.0, 0.5, 1.5, 3.0, 4.0, 8.0]
    phi_ok = all(abs(phi_e(m, ke) - phi_e_expand(m, ke)) < 1e-12 for m in samples)
    phi_nonneg = all(phi_e(m, ke) >= -1e-15 for m in samples)
    phi_zero_at_shell = abs(phi_e(ke, ke)) < 1e-15
    phi_at_zero = abs(phi_e(0.0, ke) - ke**4) < 1e-12
    quadratic_pos = all(m * m + 2.0 * ke * m + 2.0 * ke * ke > 0.0 for m in samples)

    # ∇R at the core (κ,κ,κ), Λ=κ².
    kappa = 2.5
    lam = kappa * kappa
    core = R_het(kappa, kappa, kappa, lam)
    two_k3 = 2.0 * kappa**3
    eps = 1e-6
    dRi = (R_het(kappa + eps, kappa, kappa, lam) - R_het(kappa - eps, kappa, kappa, lam)) / (
        2.0 * eps
    )
    dRj = (R_het(kappa, kappa + eps, kappa, lam) - R_het(kappa, kappa - eps, kappa, lam)) / (
        2.0 * eps
    )
    dRo = (R_het(kappa, kappa, kappa + eps, lam) - R_het(kappa, kappa, kappa - eps, lam)) / (
        2.0 * eps
    )
    dRlam = (R_het(kappa, kappa, kappa, lam + eps) - R_het(kappa, kappa, kappa, lam - eps)) / (
        2.0 * eps
    )
    grad_ok = (
        abs(core - two_k3) < 1e-12
        and abs(dRi - 5.0 * kappa**2) < 1e-6
        and abs(dRj - 5.0 * kappa**2) < 1e-6
        and abs(dRo) < 1e-6
        and abs(dRlam + 2.0 * kappa) < 1e-6
    )

    # CS: Λ² E ≥ Y.
    cs_rows = []
    cs_ok = True
    for e, x, y in ((2.0, 6.0, 20.0), (1.0, 4.0, 16.0), (3.0, 12.0, 50.0)):
        lam_i = y / x
        gap = (lam_i**2) * e - y
        # X² ≤ E Y  ⇒  Λ² E - Y = Y(EY/X² - 1) ≥ 0.
        cs_rows.append({"E": e, "X": x, "Y": y, "Lambda2_E_minus_Y": gap})
        cs_ok = cs_ok and gap >= -1e-12

    # Single shell: equality, Φ_e = 0 if κ_e = |k|.
    single_eq = abs((4.0**2) * 1.0 - 16.0) < 1e-15

    # Tail can hold almost all of D_s: tiny far mass on a two-shell field.
    core_shell = two_shell_moments(4.0, 100.0, 1.0, 1e-4)
    near = two_shell_moments(4.0, 5.0, 1.0, 1.0)
    tail_holds_ds = core_shell["Ds"] > 10.0 * near["Ds"] * core_shell["E"] / near["E"]
    tail_ds_over_y = core_shell["Ds"] / core_shell["Y"]
    tail_ds_lives = tail_ds_over_y > 1.0

    # Algebraic Φ_e / Y split. Not Taylor–Green. Frozen κ_e on the core shell
    # except the live-barycenter core sample.
    def phi_row(alpha: float, beta: float, e_a: float, e_b: float, ke: float | None, label: str) -> dict:
        ma = math.sqrt(alpha)
        mb = math.sqrt(beta)
        x = alpha * e_a + beta * e_b
        y = (alpha**2) * e_a + (beta**2) * e_b
        z = (alpha**3) * e_a + (beta**3) * e_b
        e = e_a + e_b
        h12 = ma * e_a + mb * e_b
        lam = y / x
        ds = z - lam * y
        if ke is None:
            ke = math.sqrt(lam)
        le = ke * ke
        phi = phi_e(ma, ke) * e_a + phi_e(mb, ke) * e_b
        phi_id = 0.5 * y - 0.5 * le * x - (ke**3) * h12 + (le**2) * e
        return {
            "label": label,
            "ke": ke,
            "Lambda": lam,
            "Y": y,
            "Ds": ds,
            "r2": ds / (lam * y),
            "Phi": phi,
            "Phi_id": phi_id,
            "Phi_over_Y": phi / y,
            "identity_ok": abs(phi - phi_id) < 1e-9 * max(1.0, abs(phi_id)),
        }

    single = phi_row(4.0, 4.0, 1.0, 0.0, 2.0, "single")
    core_phi = phi_row(4.0, 5.0, 1.0, 1.0, None, "core")
    low = phi_row(1.0e-4, 4.0, 0.01, 1.0, 2.0, "low")
    high = phi_row(4.0, 10000.0, 1.0, 1.0e-6, 2.0, "high")
    phi_rows = [single, core_phi, low, high]
    phi_id_ok = all(row["identity_ok"] for row in phi_rows)
    single_zero = abs(single["Phi"]) < 1e-12
    core_small = core_phi["Phi_over_Y"] < 0.1
    low_beats_r2 = low["Phi_over_Y"] > 100.0 * low["r2"]
    high_order_one = high["Phi_over_Y"] > 0.1

    # Elementary rewrite check on numbers: (d/dt)_NL Φ = M - λ_e N - 2κ_e³ Q
    # then T_c - that = 2κ_e³ Q - (Λ-λ_e) N.
    M, N, Q, lam_live, lam_e = 7.0, 1.5, 0.4, 9.0, 4.0
    ke2 = math.sqrt(lam_e)
    dnl_phi = M - lam_e * N - 2.0 * (ke2**3) * Q
    tc = M - lam_live * N
    residual = 2.0 * (ke2**3) * Q - (lam_live - lam_e) * N
    rewrite_ok = abs(tc - (dnl_phi + residual)) < 1e-12

    # Live convention: λ_e = Λ kills the moving term.
    live = abs((M - lam_live * N) - (M - lam_live * N - 2.0 * (lam_live**1.5) * Q) - 2.0 * (lam_live**1.5) * Q) < 1e-12

    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "bstar_not_seated": True,
        "identities": {
            "phi_e": "φ_e(m)=½(m-κ_e)²(m²+2κ_e m+2κ_e²)=½m⁴-½λ_e m²-κ_e³ m+λ_e²",
            "Phi_e": "Φ_e=½Y-½λ_e X-κ_e³ H_{1/2}+λ_e² E",
            "sbp_if": "If (d/dt)_NL H_{1/2}=2Q_a then T_c=(d/dt)_NL Φ_e+2κ_e³ Q_a-(Λ-λ_e)N",
            "grad_R": "∇_{(i,j,o)}R=(5κ²,5κ²,0), ∂R/∂Λ=-2κ at the core",
            "CS": "Λ² E ≥ Y, equality on one shell",
        },
        "phi_expand_ok": phi_ok,
        "phi_nonneg": phi_nonneg,
        "phi_zero_at_shell": phi_zero_at_shell,
        "phi_at_zero_is_kappa4": phi_at_zero,
        "quadratic_factor_positive": quadratic_pos,
        "R_core": core,
        "two_k3": two_k3,
        "grad_R": {"dRi": dRi, "dRj": dRj, "dRo": dRo, "dRlam": dRlam},
        "grad_R_ok": grad_ok,
        "CS_ok": cs_ok,
        "single_shell_equality": single_eq,
        "cs_rows": cs_rows,
        "tail_sample": {
            "Ds": core_shell["Ds"],
            "Y": core_shell["Y"],
            "Ds_over_Y": tail_ds_over_y,
            "E": core_shell["E"],
        },
        "tail_can_hold_Ds": bool(tail_ds_lives and tail_holds_ds),
        "phi_rows": phi_rows,
        "phi_capacity_identity_ok": phi_id_ok,
        "single_shell_Phi_zero": single_zero,
        "core_Phi_over_Y_small": core_small,
        "low_Phi_over_Y_beats_r2": low_beats_r2,
        "high_Phi_over_Y_order_one": high_order_one,
        "rewrite_ok": rewrite_ok,
        "live_moving_term_vanishes": live,
        "flux_normalization_not_reproduced": True,
        "Phi_is_not_Psi": True,
        "N_is_not_S_Gamma": True,
        "gate_file_not_in_repo": True,
        "chebyshev_not_reproduced": True,
        "do_not_mix_live_and_frozen": True,
        "Phi_over_Y_not_controlled_by_r2": True,
        "identity_is_not_a_payment": True,
        "da_ns2_is_not_a_theorem": True,
        "sits_as_useful_K": False,
        "sits_as_g4_death": False,
        "sits_as_da_ns2": False,
        "sits_as_jgc": False,
        "sits_as_bprim": False,
        "g4_stays_open": True,
        "do_not_invent_a_bridge": True,
        "do_not_run_taylor_green": True,
        "do_not_glue_to_leftover_1": True,
    }
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
