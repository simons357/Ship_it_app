"""Attack 9B quantity K_{α,β} — exact-shell + closing packet (stub).

Family:
    v_ε = w_α + ε z_β,   A w_α = α w_α,   A z_β = β z_β
    z_β ∥ Π_β B(w_α, w_α)

Boxed quantity:
    K_{α,β} = sup_{A w = α w}  β ‖Π_β B(w,w)‖₂² / (α² ‖w‖₂⁴)

Lock-ins:
- Attack 9A (AP packet) = negative for kill (D_s grew faster) — NOT a proof of ★.
- Kill lane LIVE; refuse "AP packet closed kill lane".
- Pure same-shell w_α ⇒ D_s = 0; D_s opens only via closing component.
- ε-dependence cancels in the limiting quotient.
- Narrow ≠ O(1) D_s on the lattice.
- NS NOT SOLVED. No SFE.

See docs/ns-review/ATTACK-9B-EXACT-SHELL-CLOSING.md.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence

from .rstar_quantities import (
    KILL_LANE_STATUS,
    EXACT_R_STAR_FORMULA,
    spectral_moments,
    two_shell_D_s,
)

DOC_PATH = "docs/ns-review/ATTACK-9B-EXACT-SHELL-CLOSING.md"
ATTACK_9_DOC = "docs/ns-review/ATTACK-9-COHERENT-PACKET-FAN.md"
EXACT_FORMULAS_DOC = "docs/ns-review/LEMMA-STAR-EXACT-FORMULAS.md"

KAB_FORMULA = (
    "K_{alpha,beta} = "
    "sup_{A w = alpha w} "
    "beta * ||Pi_beta B(w,w)||_2^2 / (alpha^2 * ||w||_2^4)"
)

ATTACK_9A_STATUS: dict[str, Any] = {
    "id": "ATTACK-9A-AP-PACKET",
    "verdict": "NEGATIVE_FOR_KILL",
    "killed_lemma_star": False,
    "proved_lemma_star": False,
    "note": (
        "AP packet increased T_c, but widening spectral variance increased "
        "D_s faster. Assumption D_s||v||_2^2 Y = O(1) in packet size was "
        "FALSE for that family. Not a proof of ★ either."
    ),
    "doc": ATTACK_9_DOC,
}

ATTACK_9B_STATUS: dict[str, Any] = {
    "id": "ATTACK-9B-EXACT-SHELL-CLOSING",
    "verdict": "PROTOCOL_QUANTITY_LOCK",
    "family": "v_eps = w_alpha + eps z_beta",
    "closing": "z_beta parallel Pi_beta B(w_alpha, w_alpha)",
    "quantity": KAB_FORMULA,
    "next_clean_test": [
        "exact-shell coherent fan",
        "controlled finite shell thickness",
        "NOT another widening AP packet",
    ],
    "caveat": (
        "Narrow packet ≠ automatic D_s=O(1) on lattice; "
        "D_s = sum_k lambda (lambda-Lambda)^2 |v_k|^2 amplifies small gaps"
    ),
    "doc": DOC_PATH,
}


def kab_rayleigh(
    alpha: float,
    beta: float,
    pi_beta_B_ww_norm_sq: float,
    w_norm_sq: float,
) -> dict[str, Any]:
    """Single-field Rayleigh quotient inside the K_{α,β} supremum.

    Returns
        beta * ||Π_β B(w,w)||₂² / (α² ‖w‖₂⁴)
    for one eigenfield w on shell α (not the supremum itself).
    """
    a = float(alpha)
    b = float(beta)
    num_mode = float(pi_beta_B_ww_norm_sq)
    w2 = float(w_norm_sq)
    if a == 0.0:
        raise ValueError("alpha must be nonzero")
    if w2 <= 0.0:
        raise ValueError("||w||_2^2 must be positive")
    if num_mode < 0.0:
        raise ValueError("||Pi_beta B(w,w)||_2^2 must be nonnegative")
    value = (b * num_mode) / ((a * a) * (w2 * w2))
    return {
        "ok": True,
        "alpha": a,
        "beta": b,
        "pi_beta_B_ww_norm_sq": num_mode,
        "w_norm_sq": w2,
        "rayleigh": value,
        "formula": KAB_FORMULA,
        "is_supremum": False,
        "note": "Single-field quotient — not yet the shell supremum K_{α,β}",
    }


def limiting_closing_quotient(
    alpha: float,
    beta: float,
    *,
    e_alpha: float = 1.0,
    z_norm_sq: float = 1.0,
    pi_beta_B_ww_norm_sq: float,
    epsilons: Sequence[float] = (1e-1, 1e-2, 1e-3, 1e-4),
) -> dict[str, Any]:
    """Narrative check: ε-dependence cancels in the two-shell D_s / ε² limit.

    For v_ε = w_α + ε z_β with e_β(ε) = ε² ‖z‖₂² and e_α fixed,
        D_s(ε) / ε² → α β (α−β)² e_α ‖z‖₂² / (α e_α)   as ε→0
    (denominator X → α e_α). The Rayleigh piece for K is ε-free by definition.
    """
    a = float(alpha)
    b = float(beta)
    ea = float(e_alpha)
    zn = float(z_norm_sq)
    if ea <= 0.0 or zn <= 0.0:
        raise ValueError("e_alpha and z_norm_sq must be positive")
    if a == b:
        raise ValueError("closing shell beta must differ from alpha")

    ray = kab_rayleigh(a, b, pi_beta_B_ww_norm_sq, ea)
    rows: list[dict[str, float]] = []
    limit_ds_over_eps2 = (a * b * (a - b) ** 2 * ea * zn) / (a * ea)
    for eps in epsilons:
        e = float(eps)
        eb = (e * e) * zn
        ds = two_shell_D_s(a, b, ea, eb)
        rows.append(
            {
                "eps": e,
                "e_beta": eb,
                "D_s": ds,
                "D_s_over_eps2": ds / (e * e) if e != 0.0 else float("nan"),
            }
        )

    last = rows[-1]["D_s_over_eps2"]
    rel = abs(last - limit_ds_over_eps2) / max(abs(limit_ds_over_eps2), 1e-30)

    return {
        "ok": rel < 1e-6,
        "alpha": a,
        "beta": b,
        "rayleigh": ray["rayleigh"],
        "eps_cancel_narrative": True,
        "limit_D_s_over_eps2": limit_ds_over_eps2,
        "rows": rows,
        "relative_error_smallest_eps": rel,
        "kab_formula": KAB_FORMULA,
        "note": (
            "ε enters D_s through e_β=ε²‖z‖²; D_s/ε² → finite limit; "
            "K_{α,β} Rayleigh piece is ε-free"
        ),
        "doc": DOC_PATH,
    }


def same_shell_D_s_zero(energies_on_alpha: Mapping[Any, float]) -> dict[str, Any]:
    """Pure exact-shell energies ⇒ D_s = 0 (Attack 9B base packet)."""
    moments = spectral_moments(energies_on_alpha)
    ds0 = abs(moments.D_s) <= 1e-14
    single = ds0 and moments.energy_l2 > 0.0
    return {
        "ok": single and ds0,
        "single_shell": single,
        "D_s": moments.D_s,
        "Lambda": moments.Lambda,
        "n_modes": moments.n_modes,
        "message": (
            "Pure same-shell w_α has D_s=0 — closing component required to open D_s"
            if single and ds0
            else "Not a pure exact shell (D_s may be positive)"
        ),
        "doc": DOC_PATH,
    }


def refuse_ap_packet_closed_kill_lane(text: str | None = None) -> dict[str, Any]:
    """Refuse claiming Attack 9A / AP packet closed the kill lane."""
    raw = (text or "").strip().lower()
    triggers = (
        "ap packet closed kill lane",
        "ap-packet closed kill lane",
        "attack 9a closed kill lane",
        "attack 9 closed kill lane",
        "packet closed the kill lane",
        "packet fan closed kill lane",
        "9a closed kill",
        "ap packet closed the kill",
    )
    hit = any(t in raw for t in triggers) if raw else True
    if raw and not hit:
        if ("ap packet" in raw or "attack 9a" in raw or "9a" in raw) and (
            "kill lane closed" in raw
            or "closed the kill" in raw
            or "kill-lane closed" in raw
        ):
            hit = True
    return {
        "refused": bool(hit),
        "ok": not hit,
        "attack_9a": dict(ATTACK_9A_STATUS),
        "kill_lane": dict(KILL_LANE_STATUS),
        "message": (
            "REFUSE: Attack 9A (AP packet) did not kill ★ and does NOT close "
            "the kill lane (D_s grew faster). Kill lane LIVE. NS NOT SOLVED."
            if hit
            else "No 'AP packet closed kill lane' claim detected; kill lane LIVE."
        ),
        "doc": ATTACK_9_DOC,
    }


def kab_inventory() -> dict[str, Any]:
    """Machine-readable Attack 9A/9B / K_{α,β} inventory (no SFE)."""
    return {
        "ns_solved": False,
        "sfe": False,
        "lemma_star_proved": False,
        "kill_lane": dict(KILL_LANE_STATUS),
        "attack_9a": dict(ATTACK_9A_STATUS),
        "attack_9b": dict(ATTACK_9B_STATUS),
        "K_alpha_beta": KAB_FORMULA,
        "exact_R_star": EXACT_R_STAR_FORMULA,
        "docs": {
            "attack_9": ATTACK_9_DOC,
            "attack_9b": DOC_PATH,
            "exact_formulas": EXACT_FORMULAS_DOC,
        },
        "refusals": [
            "AP packet closed kill lane",
            "kill lane closed",
            "almost proved",
            "numerics prove ★",
            "narrow packet ⇒ D_s=O(1)",
        ],
        "jonathan_action": "none",
    }
