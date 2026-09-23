"""First jet of N and T_c along Stokes / Euler / NSE. Not a close.

Exact Galerkin:
  X' = -2ν Y + 2N
  Y' = -2ν Z + 2M
  Λ' = 2/X (T_c − ν D_s)

N and M are cubic. Their t=0 derivatives are the
Gateaux derivatives along u_t = −B(u,u) − ν A u.

On v_n, N=0, so T_c' = M' − Λ N' at t=0.
A nonzero N' means the N=0 slice is not invariant.
That is not a useful K and not a named death of G4.

Do not overwrite stokes_moments.py.
Do not restore ★.
Do not seat B★.
Do not start leftover 1.
Do not treat a t=0 Taylor coefficient as a trajectory.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts" / "ns_attacks"))

from stokes_moments import (  # noqa: E402
    enforce_reality,
    k_norm2,
    leray_project,
    nonlinear_B,
    probe,
    scale_field,
)
from bstar_attack import separated_triad  # noqa: E402
from fourier_triangle import isosceles_hh_l  # noqa: E402
from ns_lemma_star_core import Field  # noqa: E402
from verify_pr24_closure_review import growing_layer_field  # noqa: E402

OUT = ROOT / "results" / "pathwise.json"
ZERO = np.zeros(3, dtype=np.complex128)


def field_to_stokes_dict(field: Field) -> dict:
    return {k: v.copy() for k, v in field.modes.items()}


def add_fields(a: dict, b: dict) -> dict:
    out = {k: v.copy() for k, v in a.items()}
    for k, v in b.items():
        out[k] = out.get(k, ZERO.copy()) + v
    return out


def bilinear_B(left: dict, right: dict) -> dict:
    """P((left·∇)right). bilinear_B(u,u) matches nonlinear_B(u)."""
    left = enforce_reality(left)
    right = enforce_reality(right)
    raw: dict = {}
    for p, up in left.items():
        for q, uq in right.items():
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k == (0, 0, 0):
                continue
            coeff = 1j * np.dot(up, np.array(q, dtype=np.float64))
            raw[k] = raw.get(k, ZERO.copy()) + coeff * uq
    return {k: leray_project(k, v) for k, v in raw.items()}


def pairing(left: dict, right: dict, power: int) -> float:
    """⟨left, A^power right⟩ = Σ λ^power ⟨left_k, right_k⟩."""
    s = 0.0 + 0.0j
    for k in set(left) | set(right):
        kn = k_norm2(k)
        if kn == 0:
            continue
        s += (kn**power) * np.vdot(
            left.get(k, ZERO), right.get(k, ZERO)
        )
    return float(s.real)


def dN_dM(field: dict, w: dict, Buu: dict | None = None) -> tuple[float, float]:
    """Gateaux of N=−⟨B(u,u),Au⟩ and M=−⟨B(u,u),A²u⟩ along w."""
    field = enforce_reality(field)
    w = enforce_reality(w)
    if Buu is None:
        Buu = nonlinear_B(field)
    Buw = bilinear_B(field, w)
    Bwu = bilinear_B(w, field)
    dB = add_fields(Buw, Bwu)
    dN = -pairing(dB, field, 1) - pairing(Buu, w, 1)
    dM = -pairing(dB, field, 2) - pairing(Buu, w, 2)
    return dN, dM


def stokes_dir(field: dict) -> dict:
    """w = −A u, the ν=1 Stokes direction."""
    field = enforce_reality(field)
    return {k: (-k_norm2(k)) * v for k, v in field.items()}


def euler_dir(Buu: dict) -> dict:
    """w = −B(u,u)."""
    return {k: -v.copy() for k, v in Buu.items()}


def jets(field: dict, label: str, nu: float = 1.0) -> dict:
    field = enforce_reality(field)
    pr = probe(field, label=label)
    Buu = nonlinear_B(field)
    # Lock polarized reconstruction of B(u,u).
    Buu2 = bilinear_B(field, field)
    b_err = 0.0
    for k in set(Buu) | set(Buu2):
        b_err += float(
            np.vdot(
                Buu.get(k, ZERO) - Buu2.get(k, ZERO),
                Buu.get(k, ZERO) - Buu2.get(k, ZERO),
            ).real
        )
    ws = stokes_dir(field)
    we = euler_dir(Buu)
    n_s, m_s = dN_dM(field, ws, Buu)
    n_e, m_e = dN_dM(field, we, Buu)
    n_dot = n_e + nu * n_s
    m_dot = m_e + nu * m_s
    lam = pr.Lambda
    # Identity Λ' = 2/X (T_c − ν D_s)
    lam_dot = (2.0 / pr.X) * (pr.Tc - nu * pr.Ds) if pr.X > 0 else float("nan")
    # T_c' = M' − Λ' N − Λ N'
    tc_dot = m_dot - lam_dot * pr.N - lam * n_dot
    tc = pr.Tc
    x = pr.X
    return {
        "label": label,
        "E": pr.E,
        "X": x,
        "Y": pr.Y,
        "Lambda": lam,
        "Ds": pr.Ds,
        "N": pr.N,
        "M": pr.M,
        "Tc": tc,
        "B_match": b_err < 1e-16 * max(1.0, pr.E**2),
        "N_dot_stokes": n_s,
        "M_dot_stokes": m_s,
        "N_dot_euler": n_e,
        "M_dot_euler": m_e,
        "N_dot": n_dot,
        "M_dot": m_dot,
        "Lambda_dot": lam_dot,
        "Tc_dot": tc_dot,
        "N_dot_over_Tc": (n_dot / tc) if abs(tc) > 1e-14 else float("nan"),
        "N_dot_stokes_over_Tc": (n_s / tc) if abs(tc) > 1e-14 else float("nan"),
        "N_dot_euler_over_sqrtX_Tc": (
            n_e / (math.sqrt(x) * tc) if abs(tc) > 1e-14 and x > 0 else float("nan")
        ),
        "Tc_dot_over_Tc": (tc_dot / tc) if abs(tc) > 1e-14 else float("nan"),
        "N_is_zero": abs(pr.N) < 1e-8,
        "N_dot_nonzero": abs(n_dot) > 1e-8 * max(1.0, abs(tc), abs(pr.M)),
        "slice_not_invariant": abs(n_dot) > 1e-8 * max(1.0, abs(tc), abs(pr.M)),
    }


def stokes_fd_check(field: dict, eps: float = 1e-6, nu: float = 1.0) -> dict:
    """Finite-difference lock of the Stokes Gateaux."""
    field = enforce_reality(field)
    pr0 = probe(field)
    bumped = {
        k: (np.exp(-nu * k_norm2(k) * eps) * v) for k, v in field.items()
    }
    pr1 = probe(enforce_reality(bumped))
    n_fd = (pr1.N - pr0.N) / eps
    m_fd = (pr1.M - pr0.M) / eps
    row = jets(field, "fd")
    return {
        "N_fd": n_fd,
        "M_fd": m_fd,
        "N_stokes": nu * row["N_dot_stokes"],
        "M_stokes": nu * row["M_dot_stokes"],
        "N_ok": abs(n_fd - nu * row["N_dot_stokes"])
        < 1e-4 * max(1.0, abs(n_fd), abs(row["N_dot_stokes"])),
        "M_ok": abs(m_fd - nu * row["M_dot_stokes"])
        < 1e-4 * max(1.0, abs(m_fd), abs(row["M_dot_stokes"])),
    }


def amplitude_scan() -> dict:
    base = field_to_stokes_dict(isosceles_hh_l())
    rows = []
    for a in (0.05, 0.2, 1.0, 4.0):
        row = jets(scale_field(base, a), f"amp{a}")
        row["amp"] = a
        rows.append(row)
    r_s = [abs(r["N_dot_stokes_over_Tc"]) for r in rows]
    r_e = [abs(r["N_dot_euler_over_sqrtX_Tc"]) for r in rows]
    return {
        "rows": rows,
        "stokes_over_Tc_flat": max(r_s) / min(r_s) < 1.02,
        "euler_scaled_flat": max(r_e) / min(r_e) < 1.02,
        "B_match": all(r["B_match"] for r in rows),
    }


def record() -> dict:
    amp = amplitude_scan()
    fd = stokes_fd_check(growing_layer_field(1))
    families = []
    for n in (1, 4, 8):
        families.append(jets(growing_layer_field(n), f"vn{n}"))
    for m in (1, 8):
        families.append(jets(separated_triad(m), f"sep{m}"))
    vn = [r for r in families if r["label"].startswith("vn")]
    sep = [r for r in families if r["label"].startswith("sep")]
    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "bstar_not_seated": True,
        "not_a_trajectory": True,
        "identities": {
            "X_prime": "X' = -2ν Y + 2N",
            "Y_prime": "Y' = -2ν Z + 2M",
            "Lambda_prime": "Λ' = 2/X (T_c − ν D_s)",
            "Tc_prime_on_N_zero": "T_c' = M' − Λ N'  when N=0",
        },
        "amplitude": amp,
        "stokes_fd": fd,
        "fd_lock": bool(fd["N_ok"] and fd["M_ok"]),
        "B_match": bool(amp["B_match"] and all(r["B_match"] for r in families)),
        "families": families,
        "vn_N_zero": all(r["N_is_zero"] for r in vn),
        "vn_stokes_preserves_N": all(abs(r["N_dot_stokes"]) < 1e-8 for r in vn),
        "vn_euler_generates_N": all(abs(r["N_dot_euler"]) > 1e-6 * max(1.0, abs(r["Tc"])) for r in vn),
        "vn_slice_not_invariant": all(r["slice_not_invariant"] for r in vn),
        "vn_Tc_grows": all(r["Tc_dot"] > 0 for r in vn),
        "triangle_stokes_is_minus_eight_thirds": abs(
            amp["rows"][2]["N_dot_stokes_over_Tc"] + 8.0 / 3.0
        )
        < 1e-10,
        "sits_as_useful_K": False,
        "sits_as_g4_death": False,
        "g4_stays_open": True,
        "vn_table": [
            {
                "label": r["label"],
                "N": r["N"],
                "Tc": r["Tc"],
                "N_dot_stokes": r["N_dot_stokes"],
                "N_dot_euler": r["N_dot_euler"],
                "N_dot": r["N_dot"],
                "Tc_dot": r["Tc_dot"],
                "Lambda_dot": r["Lambda_dot"],
                "N_dot_stokes_over_Tc": r["N_dot_stokes_over_Tc"],
                "Tc_dot_over_Tc": r["Tc_dot_over_Tc"],
            }
            for r in vn
        ],
        "sep_table": [
            {
                "label": r["label"],
                "N": r["N"],
                "N_dot": r["N_dot"],
                "Tc_dot": r["Tc_dot"],
                "N_dot_over_Tc": r["N_dot_over_Tc"],
            }
            for r in sep
        ],
    }
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    print(json.dumps(row, indent=2))


if __name__ == "__main__":
    main()
