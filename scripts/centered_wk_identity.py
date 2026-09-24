"""Frozen-chart identity W_K = D_s + X (Lambda - K)^2.

Equals ||A^{1/2}(A-K)u||_2^2. At fixed physical state the reset jump is
Delta W = X[(Lambda-K_{e+1})^2 - (Lambda-K_e)^2]. That is the unique
corollary of W_K. It is not a cutoff-uniform reset ledger.
NS is not solved.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import centered_drift_triad_test as cdt  # noqa: E402
import growing_layer_counterexample as gl  # noqa: E402
import ns_lemma_star_core as core  # noqa: E402


def W_from_moments(X: float, Y: float, Z: float, Lam: float, K: float) -> float:
    Ds = Z - Lam * Y
    return Ds + X * (Lam - K) ** 2


def delta_W_fixed_state(X: float, Lam: float, K_old: float, K_new: float) -> float:
    """Physical state fixed: X, Lambda, D_s unchanged. Only the chart center moves."""
    return X * ((Lam - K_new) ** 2 - (Lam - K_old) ** 2)


def W_direct(field: core.Field, K: float) -> float:
    total = 0.0
    for k, vk in field.modes.items():
        ell = core.lam(k)
        e = float(np.vdot(vk, vk).real)
        total += ell * (ell - K) ** 2 * e
    return total


def check_field(field: core.Field, shifts: tuple = (0.0, 1.0, -2.5)) -> dict:
    E, X, Y, Z, Lam = core.moments(field)
    Ds = core.D_s_moment_form(X, Y, Z)
    rows = []
    ok = True
    for K in shifts:
        from_mom = W_from_moments(X, Y, Z, Lam, K)
        direct = W_direct(field, K)
        match = abs(from_mom - direct) <= 1e-9 * max(1.0, abs(direct))
        ok = ok and match
        rows.append(
            {
                "K": K,
                "W_from_moments": from_mom,
                "W_direct": direct,
                "match": match,
            }
        )
    K0, K1 = 1.0, -2.5
    w0 = W_from_moments(X, Y, Z, Lam, K0)
    w1 = W_from_moments(X, Y, Z, Lam, K1)
    jump = delta_W_fixed_state(X, Lam, K0, K1)
    jump_ok = abs((w1 - w0) - jump) <= 1e-9 * max(1.0, abs(jump))
    return {
        "E": E,
        "X": X,
        "Y": Y,
        "Z": Z,
        "Lambda": Lam,
        "D_s": Ds,
        "rows": rows,
        "identities_ok": ok and jump_ok,
        "delta_W": jump,
        "delta_W_from_W": w1 - w0,
        "delta_W_ok": jump_ok,
    }


def run() -> dict:
    note = check_field(cdt.near_scale_triad())
    vn = check_field(gl.growing_layer(2))
    return {
        "ns_solved": False,
        "reset_jump_is_wk_corollary": True,
        "reset_ledger_uniform": False,
        "identity": "W_K = D_s + X (Lambda - K)^2 = ||A^{1/2}(A-K)u||_2^2",
        "delta_W": "X*((Lambda-K_new)^2 - (Lambda-K_old)^2) at fixed physical state",
        "note_triad": note,
        "growing_layer_n2": {
            "identities_ok": vn["identities_ok"],
            "delta_W_ok": vn["delta_W_ok"],
            "Lambda": vn["Lambda"],
            "D_s": vn["D_s"],
        },
        "all_identities_ok": note["identities_ok"] and vn["identities_ok"],
        "note": (
            "W_K and the fixed-state reset jump are algebra. "
            "Cutoff-uniform summability of resets is not obtained. "
            "NS not solved."
        ),
    }


def main() -> int:
    payload = run()
    out = Path(__file__).resolve().parents[1] / "results" / "centered_wk_identity.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, indent=2))
    print(json.dumps(payload, indent=2), flush=True)
    print(f"wrote {out}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
