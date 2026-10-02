"""Score |T_c| / (||∇u||_3 √(Y D_s)) on seated families.

The candidate is OPEN: not a proved bound, not unrestricted Lemma★.
||∇u||_3 is the physical L^3 of the Frobenius gradient on the volume-1
torus of LEMMA_STAR_EXACT_FORMULAS.md (Haar measure, Plancherel
||v||_2^2 = ∑ |v_k|^2). Quadrature is a fine FFT grid, not a proxy.
Locked SBP / φ/d / low-tail / sign / S_pq / local-★ packets are not
altered. Localized bump is not on this tree. NS is not solved.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

SCRIPTS = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS))

import centered_drift_triad_split as split  # noqa: E402
import centered_drift_triad_test as cdt  # noqa: E402
import growing_layer_counterexample as gl  # noqa: E402
import ns_lemma_star_core as core  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "results" / "da_gate_tc_l3_sqrt_yds.json"

NEAR_SHELL_EPS = (0.20, 0.10, 0.05, 0.025)
V_N = (1, 2, 4, 8)
SEED = 20260922


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


def max_abs_k(field: core.Field) -> int:
    if not field.modes:
        return 0
    return max(max(abs(int(c)) for c in k) for k in field.modes)


def next_pow2(n: int) -> int:
    p = 1
    while p < n:
        p *= 2
    return p


def recommended_grid(
    field: core.Field, oversample: int = 4, minimum: int = 32, max_n: int = 128
) -> int:
    """Nyquist for |∇u|^2 needs N > 4 max|k|_∞; exact |∇u|^4 needs N > 8 max|k|_∞."""
    kmax = max(max_abs_k(field), 1)
    need = next_pow2(max(oversample * kmax + 2, 8 * kmax + 2))
    return max(minimum, min(need, max_n))


def physical_grad_norms(field: core.Field, n: int | None = None) -> dict:
    """Haar L^p of the Frobenius gradient via an N^3 trapezoid grid.

    v(x) = ∑ v_k e^{ik·x} on T^3 = (R/2πZ)^3. Book Plancherel:
    ||v||_2^2 = (2π)^{-3} ∫ |v|^2 = ∑ |v_k|^2, so discrete Haar is
    the grid mean. |∇v|^2 = ∑_{i,j} |∂_j v_i|^2. Then
    ||∇v||_2^2 must recover X = ∑ |k|^2 |v_k|^2 when N beats 4 max|k|.
    """
    if n is None:
        n = recommended_grid(field)
    kmax = max_abs_k(field)
    if n <= 2 * kmax:
        raise ValueError(f"grid N={n} aliases the field (max|k|_∞={kmax})")

    freqs = np.fft.fftfreq(n) * n
    kx, ky, kz = np.meshgrid(freqs, freqs, freqs, indexing="ij")
    hat = np.zeros((3, n, n, n), dtype=complex)
    for k, vk in field.modes.items():
        ix, iy, iz = (int(k[0]) % n, int(k[1]) % n, int(k[2]) % n)
        hat[:, ix, iy, iz] = vk

    scale = float(n) ** 3
    grad_sq = np.zeros((n, n, n), dtype=float)
    vel_sq = np.zeros((n, n, n), dtype=float)
    for i in range(3):
        phys_v = np.fft.ifftn(hat[i]) * scale
        vel_sq += np.abs(phys_v) ** 2
        for kj in (kx, ky, kz):
            phys_d = np.fft.ifftn(1j * kj * hat[i]) * scale
            grad_sq += np.abs(phys_d) ** 2

    abs_grad = np.sqrt(np.maximum(grad_sq, 0.0))
    l2 = float(np.sqrt(np.mean(grad_sq)))
    l3 = float(np.mean(abs_grad**3) ** (1.0 / 3.0))
    l4 = float(np.mean(grad_sq**2) ** 0.25)
    e_phys = float(np.mean(vel_sq))
    return {
        "N": int(n),
        "kmax": int(kmax),
        "grad_L2": l2,
        "grad_L3": l3,
        "grad_L4": l4,
        "L4_certified": bool(n > 8 * kmax),
        "E_phys": e_phys,
        "max_abs_grad": float(abs_grad.max()),
    }


def fourier_grad_linf(field: core.Field) -> float:
    """Triangle bound ||∇u||_∞ ≤ ∑ |k| |u_k|. Exact arithmetic, usually loose."""
    total = 0.0
    for k, vk in field.modes.items():
        total += math.sqrt(core.lam(k)) * float(np.linalg.norm(vk))
    return total


def score_field(field: core.Field, n: int | None = None, refine: bool = False) -> dict:
    rec = core.R_star(field, verify=True, tol=1e-9)
    grid = physical_grad_norms(field, n=n)
    X = float(rec["X"])
    Y = float(rec["Y"])
    E = float(rec["E"])
    Ds = float(rec["D_s"])
    Tc = float(rec["T_c"])
    abs_tc = abs(Tc)
    l3 = grid["grad_L3"]
    l2_exact = math.sqrt(X) if X > 0 else float("nan")
    l4 = grid["grad_L4"]
    linf = fourier_grad_linf(field)
    sqrt_yds = math.sqrt(Y * Ds) if Y > 0 and Ds > 0 else float("nan")
    # Volume-1 interpolation: ||f||_3 ≤ ||f||_2^{1/3} ||f||_4^{2/3} when L^4 is exact.
    l3_upper = (
        (l2_exact ** (1.0 / 3.0)) * (l4 ** (2.0 / 3.0))
        if grid["L4_certified"] and l2_exact == l2_exact
        else linf
    )
    l3_upper_tag = "L2_L4" if grid["L4_certified"] else "fourier_l1"
    denom_l3 = l3 * sqrt_yds if l3 > 0 and sqrt_yds == sqrt_yds else float("nan")
    denom_l2 = l2_exact * sqrt_yds if l2_exact > 0 and sqrt_yds == sqrt_yds else float("nan")
    denom_star = math.sqrt(Ds * E * Y) if Ds > 0 and E > 0 and Y > 0 else float("nan")
    denom_lower = l3_upper * sqrt_yds if l3_upper > 0 and sqrt_yds == sqrt_yds else float("nan")
    out = {
        **{k: rec[k] for k in ("E", "X", "Y", "Z", "Lambda", "D_s", "T_c", "R_star")},
        **grid,
        "abs_T_c": abs_tc,
        "grad_L2_exact": l2_exact,
        "grad_Linf_bound": linf,
        "grad_L3_upper_cert": l3_upper,
        "L3_upper_from": l3_upper_tag,
        "T_c_over_Ds": (Tc / Ds) if Ds > 0 else None,
        "T_c_over_sqrt_Ds": (abs_tc / math.sqrt(Ds)) if Ds > 0 else None,
        "ratio_l3": (abs_tc / denom_l3) if denom_l3 == denom_l3 and denom_l3 > 0 else None,
        "ratio_l2": (abs_tc / denom_l2) if denom_l2 == denom_l2 and denom_l2 > 0 else None,
        "ratio_star": (abs_tc / denom_star) if denom_star == denom_star and denom_star > 0 else None,
        "ratio_cert_upper": (
            abs_tc / denom_l2 if denom_l2 == denom_l2 and denom_l2 > 0 else None
        ),
        "ratio_cert_lower": (
            abs_tc / denom_lower if denom_lower == denom_lower and denom_lower > 0 else None
        ),
        "quadrature_cannot_certify_kill": True,
        "sqrt_Y_Ds": sqrt_yds if sqrt_yds == sqrt_yds else None,
        "grad_L2_matches_sqrt_X": bool(
            abs(grid["grad_L2"] - l2_exact) <= 1e-8 * max(1.0, l2_exact)
        ),
        "E_phys_matches_E": bool(abs(grid["E_phys"] - E) <= 1e-8 * max(1.0, E)),
        "vacuous_single_shell": rec["vacuous_single_shell"],
    }
    if refine:
        n2 = grid["N"] * 2
        grid2 = physical_grad_norms(field, n=n2)
        out["refine"] = {
            "N": grid2["N"],
            "grad_L3": grid2["grad_L3"],
            "rel_change": abs(grid2["grad_L3"] - l3) / max(l3, 1e-300),
        }
    return out


def two_shell_populated(
    alpha: int, beta: int, rng: np.random.Generator, e_beta: float = 0.25
) -> core.Field:
    """Nearly single-shell: both neighboring shells occupied, many triads."""
    if not 0.0 < e_beta < 1.0:
        raise ValueError("e_beta in (0,1)")
    w = core.random_shell_field(alpha, rng, target_E=1.0 - e_beta)
    z = core.random_shell_field(beta, rng, target_E=e_beta)
    return w.add(z)


def separated_varied(L: int, scale_p: float, scale_q: float, scale_r: float) -> core.Field:
    """Widely separated triad with independent amplitudes."""
    if L < 2:
        raise ValueError("L must be >= 2")
    field = core.Field()
    p, q, r = (1, 0, 0), (0, L, 0), (1, L, 0)
    a = scale_p * np.array([0.0, 1.0, 0.0], dtype=complex)
    b = scale_q * np.array([1.0, 0.0, 1.0], dtype=complex)
    q_dot_a = float(np.dot(np.array(q, dtype=float), a.real))
    p_dot_b = float(np.dot(np.array(p, dtype=float), b.real))
    raw = core.project_perp(r, q_dot_a * b + p_dot_b * a)
    nrm = float(np.linalg.norm(raw))
    if nrm < 1e-15:
        raise ValueError("vanishing closing polarization")
    field.set_mode(p, a)
    field.set_mode(q, b)
    field.set_mode(r, -1j * scale_r * (raw / nrm))
    return field


def _helical(k, sign: float = 1.0):
    kf = np.array(k, dtype=float)
    a = np.array([1.0, 0.0, 0.0])
    if abs(np.dot(a, kf)) > 0.9 * np.linalg.norm(kf):
        a = np.array([0.0, 1.0, 0.0])
    e1 = a - (np.dot(a, kf) / np.dot(kf, kf)) * kf
    e1 = e1 / np.linalg.norm(e1)
    e2 = np.cross(kf, e1)
    e2 = e2 / np.linalg.norm(e2)
    return e1 + 1j * sign * e2


def coherent_packet(
    center: tuple[int, int, int],
    halfwidth: int,
    phase: float = 0.0,
    mixed: bool = True,
) -> core.Field:
    """Dense box around `center`. Mixed helicity: same-sign is Beltrami, T_c=0."""
    field = core.Field()
    w = int(halfwidth)
    twist = np.exp(1j * phase)
    for i in range(-w, w + 1):
        for j in range(-w, w + 1):
            for kk in range(-w, w + 1):
                k = (center[0] + i, center[1] + j, center[2] + kk)
                if k == (0, 0, 0):
                    continue
                sign = -1.0 if mixed and ((i + j + kk) % 2) else 1.0
                field.set_mode(k, twist * _helical(k, sign))
    return field


def clustered_aligned_triads() -> core.Field:
    """Several neighboring triads, each with the aligned closer. Coordinated, not Beltrami."""
    A = np.array([0.0, 1.0, 0.0], dtype=complex)
    B = np.array([1.0, 0.0, 1.0], dtype=complex)
    field = core.Field()
    pairs = (
        ((1, 0, 0), (0, 1, 0)),
        ((1, 0, 0), (0, 1, 1)),
        ((1, 0, 1), (0, 1, 0)),
        ((2, 0, 0), (0, 1, 0)),
        ((1, 0, 0), (0, 2, 0)),
        ((1, 1, 0), (0, 1, 0)),
    )
    for p, q in pairs:
        Bq = core.project_perp(q, B)
        if float(np.linalg.norm(Bq)) < 1e-15:
            continue
        try:
            piece = split.aligned_closer(p, q, A, Bq, phase=-math.pi / 2)
        except ValueError:
            continue
        field = field.add(piece)
    return field


def annular_field(alpha: int, beta: int, rng: np.random.Generator, eps: float) -> core.Field | None:
    w = core.random_shell_field(alpha, rng, target_E=1.0)
    z, _raw = core.build_closing_direction(w, beta)
    if z is None:
        return None
    sign = core.choose_closing_sign(w, z)
    return core.combine_eps(w, z, sign * eps)


def _growth(a: float | None, b: float | None, factor: float = 2.0) -> dict:
    if a is None or b is None or a == 0:
        return {"first": a, "last": b, "ratio": None, "grows": False, "bounded": False}
    rel = b / a
    grows = bool(b > factor * a)
    decays = bool(b < a / factor)
    return {
        "first": a,
        "last": b,
        "ratio": rel,
        "grows": grows,
        "decays": decays,
        "bounded": (not grows) and (not decays),
    }


def compact(rec: dict, extra: tuple = ()) -> dict:
    keys = (
        "E",
        "X",
        "Y",
        "Lambda",
        "D_s",
        "T_c",
        "R_star",
        "N",
        "kmax",
        "grad_L2",
        "grad_L3",
        "grad_L4",
        "L4_certified",
        "grad_L3_upper_cert",
        "L3_upper_from",
        "T_c_over_Ds",
        "T_c_over_sqrt_Ds",
        "ratio_l3",
        "ratio_l2",
        "ratio_star",
        "ratio_cert_upper",
        "ratio_cert_lower",
        "grad_L2_matches_sqrt_X",
        "E_phys_matches_E",
        *extra,
    )
    return {k: rec[k] for k in keys if k in rec}


def run() -> dict:
    note_field = cdt.near_scale_triad()
    note = score_field(note_field, refine=True)
    scaled = score_field(note_field.scale(2.0))
    sep = score_field(cdt.separated_triad(8))
    hh = score_field(split.hh_to_l_triad())

    vn = []
    for n in V_N:
        rec = score_field(gl.growing_layer(n))
        vn.append({"n": n, **compact(rec)})

    annular = []
    for eps in NEAR_SHELL_EPS:
        field = annular_field(5, 4, np.random.default_rng(SEED), eps)
        if field is None:
            annular.append({"eps": eps, "empty_closer": True})
            continue
        rec = score_field(field, refine=(eps == NEAR_SHELL_EPS[0]))
        annular.append({"eps": eps, "empty_closer": False, **compact(rec, extra=("refine",))})

    l3_vn = _growth(vn[0]["ratio_l3"], vn[-1]["ratio_l3"])
    star_vn = _growth(vn[0]["ratio_star"], vn[-1]["ratio_star"])
    live = [r for r in annular if not r.get("empty_closer") and r.get("ratio_l3")]
    l3_ns = _growth(live[0]["ratio_l3"], live[-1]["ratio_l3"]) if len(live) >= 2 else {}
    tc_ds_ns = _growth(live[0]["T_c_over_Ds"], live[-1]["T_c_over_Ds"]) if len(live) >= 2 else {}
    sqrt_ds_ns = (
        _growth(live[0]["T_c_over_sqrt_Ds"], live[-1]["T_c_over_sqrt_Ds"]) if len(live) >= 2 else {}
    )

    note_scale_ok = (
        note["ratio_l3"] is not None
        and scaled["ratio_l3"] is not None
        and abs(note["ratio_l3"] - scaled["ratio_l3"])
        <= 1e-8 * max(1.0, abs(note["ratio_l3"]))
    )
    parseval_ok = all(
        [note["grad_L2_matches_sqrt_X"], note["E_phys_matches_E"], sep["grad_L2_matches_sqrt_X"]]
        + [r["grad_L2_matches_sqrt_X"] and r["E_phys_matches_E"] for r in vn]
        + [
            r.get("grad_L2_matches_sqrt_X", False) and r.get("E_phys_matches_E", False)
            for r in live
        ]
    )
    refine_ok = bool(note.get("refine", {}).get("rel_change", 1.0) < 0.02)

    small = []
    fat = None
    fat_name = None
    for alpha, beta in ((9, 8), (9, 10), (9, 5), (13, 9)):
        fat = annular_field(alpha, beta, np.random.default_rng(SEED + 1), 0.05)
        if fat is not None:
            fat_name = f"fat_near_shell_{alpha}_{beta}_eps0.05"
            break
    if fat is not None:
        small.append({"name": fat_name, **compact(score_field(fat))})
    small.append(
        {
            "name": "two_shell_5_6_e0.25",
            **compact(score_field(two_shell_populated(5, 6, np.random.default_rng(SEED + 2), 0.25))),
        }
    )
    for L, scales in (
        (8, (1.0, 0.1, 1.0)),
        (8, (1.0, 4.0, 0.25)),
        (16, (1.0, 0.25, 1.0)),
    ):
        rec = score_field(separated_varied(L, *scales))
        small.append(
            {
                "name": f"separated_L{L}_amp{scales[0]:g}_{scales[1]:g}_{scales[2]:g}",
                **compact(rec),
            }
        )
    beltrami = coherent_packet((3, 1, 0), 1, phase=0.0, mixed=False)
    small.append({"name": "beltrami_packet_c310_w1", **compact(score_field(beltrami))})
    small.append({"name": "clustered_aligned_triads", **compact(score_field(clustered_aligned_triads()))})
    small_max_l2 = max(r["ratio_cert_upper"] for r in small if r.get("ratio_cert_upper"))
    small_max_l3 = max(r["ratio_l3"] for r in small if r.get("ratio_l3"))

    return {
        "ns_solved": False,
        "candidate_proved": False,
        "unrestricted_star_restored": False,
        "crossover_stamped": False,
        "localized_bump_on_this_tree": False,
        "quadrature_cannot_certify_kill": True,
        "uniform_inequality_is_separate_obligation": True,
        "gate_altered": {
            "sbp": False,
            "phi_vs_d": False,
            "low_tail_snapshot": False,
            "sign_realizability": False,
            "s_pq": False,
            "local_star": False,
        },
        "candidate": r"|T_c| <= C ||∇u||_3 √(Y D_s)",
        "Y_is": "||A v||_2^2 = sum λ_k^2 |v_k|^2",
        "grad_norm": "Frobenius, Haar measure on T^3=(R/2πZ)^3",
        "note_triad": compact(note, extra=("refine",)),
        "note_triad_scale_2": compact(scaled),
        "homogeneity_ratio_invariant": note_scale_ok,
        "separated_L8": compact(sep),
        "hh_to_l": compact(hh),
        "growing_layer": vn,
        "near_shell": annular,
        "small_case": small,
        "small_case_max_ratio_cert_upper": small_max_l2,
        "small_case_max_ratio_l3": small_max_l3,
        "growth": {
            "v_n_ratio_l3": l3_vn,
            "v_n_ratio_star": star_vn,
            "near_shell_ratio_l3": l3_ns,
            "near_shell_T_c_over_Ds": tc_ds_ns,
            "near_shell_T_c_over_sqrt_Ds": sqrt_ds_ns,
        },
        "parseval_ok": parseval_ok,
        "l3_quadrature_stable_on_note": refine_ok,
        "linear_in_Ds_obstructed_by_near_shell": bool(tc_ds_ns.get("grows")),
        "sqrt_Ds_scale_finite_on_near_shell": bool(sqrt_ds_ns.get("bounded")),
        "new_ratio_bounded_on_near_shell": bool(l3_ns.get("bounded")),
        "new_ratio_grows_on_v_n": bool(l3_vn.get("grows")),
        "v_n_kills_new_slot": bool(l3_vn.get("grows")),
        "old_star_grows_on_v_n": bool(star_vn.get("grows")),
        "uniform_C_proved": False,
        "all_identities_ok": bool(parseval_ok and note_scale_ok and refine_ok),
        "note": (
            "Near-shell makes T_c/D_s blow while T_c/√D_s stays finite: "
            "that is the exact obstruction to a linear-in-D_s bound and "
            "the reason the square-root scale is the attack. "
            "The obstruction motivates the candidate and does not establish it. "
            "Quadrature of ||∇u||_3 cannot certify a counterexample; "
            "T_c, Y, D_s and ||∇u||_2=√X are exact Fourier arithmetic. "
            "A script run verifies identities. The uniform inequality "
            "and its time budget remain separate proof obligations. "
            "The candidate itself is not proved. Unrestricted ★ stays dead. "
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
