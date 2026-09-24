"""Run the frozen first-variation sign gate on the lattice.

L_{1,N} = Λ_N ⟨δ_N, T_N^{(0)}⟩ is unaltered.
Neighboring T_m is kept. R_{2,N} is the remainder.

This is a finite-N neighboring-shell helical search.
It is not Heavy scalene loops.
It is not persistence N→∞.
It is not a useful K.
Do not invent a bridge.
Do not start leftover 1.
Do not run Taylor–Green.
Do not alter Lemma A.

Does not overwrite stokes_moments.py.
"""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from ns_lemma_star_core import (  # noqa: E402
    Field,
    T_c_direct,
    T_k_map,
    lam,
    moments,
)

OUT = ROOT / "results" / "sign_run.json"
SEED_OUT = ROOT / "results" / "A_N_plus_seeds.json"

RHO_FLOOR = 0.05
NS = (2, 3, 4, 5, 6, 7, 8)
SCORE_PER_N = 8


def helical(k, s: int) -> np.ndarray:
    """Waleffe helical wave: h^s = (e1 + i s e2)/√2, s=±1."""
    k = np.asarray(k, dtype=float)
    kn = float(np.linalg.norm(k))
    if kn < 1e-15:
        raise ValueError("no helical basis at k=0")
    khat = k / kn
    n = np.array([0.0, 0.0, 1.0]) if abs(khat[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    e1 = np.cross(khat, n)
    e1 /= float(np.linalg.norm(e1))
    e2 = np.cross(khat, e1)
    return (e1 + 1j * float(s) * e2) / math.sqrt(2.0)


def mode_helicity(k, v) -> float:
    """Signed helicity. Equals s on h^s."""
    k = np.asarray(k, dtype=float)
    kn = float(np.linalg.norm(k))
    v = np.asarray(v, dtype=complex)
    n2 = float(np.vdot(v, v).real)
    if kn < 1e-15 or n2 < 1e-15:
        return 0.0
    khat = k / kn
    return float(np.real(1j * np.dot(khat, np.cross(v, np.conj(v))))) / n2


def annulus_keys(n: int, half: int = 1) -> list[tuple[int, int, int]]:
    lo = (n - half) ** 2
    hi = (n + half) ** 2
    r = n + half
    keys = []
    for x in range(-r, r + 1):
        for y in range(-r, r + 1):
            for z in range(-r, r + 1):
                if x == 0 and y == 0 and z == 0:
                    continue
                ell = x * x + y * y + z * z
                if lo <= ell <= hi:
                    keys.append((x, y, z))
    return keys


def _canon_key(k: tuple[int, int, int]) -> tuple[int, int, int]:
    nk = (-k[0], -k[1], -k[2])
    return k if k >= nk else nk


def neighbor_triangles(n: int, half: int = 1) -> list[tuple]:
    keys = annulus_keys(n, half)
    inset = set(keys)
    seen: set[frozenset] = set()
    tris = []
    for i, p in enumerate(keys):
        for q in keys[i + 1 :]:
            k = (p[0] + q[0], p[1] + q[1], p[2] + q[2])
            if k not in inset or k == p or k == q:
                continue
            if p[0] * q[1] - p[1] * q[0] == 0 and p[0] * q[2] - p[2] * q[0] == 0 and p[1] * q[2] - p[2] * q[1] == 0:
                continue
            tag = frozenset({_canon_key(p), _canon_key(q), _canon_key(k)})
            if len(tag) < 3 or tag in seen:
                continue
            spread = max(lam(p), lam(q), lam(k)) - min(lam(p), lam(q), lam(k))
            if spread < 1.0 - 1e-12:
                # Equal-length kills the T_c weight. Not a neighbor. Not sign depletion.
                continue
            seen.add(tag)
            tris.append((spread, p, q, k))
    tris.sort(key=lambda row: (row[0], row[1], row[2], row[3]))
    return [(p, q, k) for _spread, p, q, k in tris]


def helical_field(p, q, k, signs, amp: float = 1.0) -> Field:
    f = Field()
    for key, s in ((p, signs[0]), (q, signs[1]), (k, signs[2])):
        f.set_mode(key, amp * helical(key, s))
    return f


def first_variation(field: Field) -> dict:
    e, x, y, z, lam_b = moments(field)
    tk = T_k_map(field)
    tc = T_c_direct(field, lam_b)
    inner = 0.0
    quad = 0.0
    nrm_d2 = 0.0
    nrm_t2 = 0.0
    for key, t in tk.items():
        d = lam(key) - lam_b
        inner += d * t
        quad += (d * d) * t
        nrm_d2 += d * d
        nrm_t2 += t * t
    l1 = lam_b * inner
    r2 = tc - l1
    nrm_d = math.sqrt(nrm_d2)
    nrm_t = math.sqrt(nrm_t2)
    rho = inner / (nrm_d * nrm_t) if nrm_d > 1e-15 and nrm_t > 1e-15 else 0.0
    return {
        "E": e,
        "X": x,
        "Y": y,
        "Lambda": lam_b,
        "T_c": tc,
        "L1": l1,
        "R2": r2,
        "quad": quad,
        "rho": rho,
        "expansion_ok": abs(r2 - quad) < 1e-8 * max(1.0, abs(tc), abs(quad)),
        "nrm_T": nrm_t,
    }


def _sign_of(rho: float, l1: float) -> int:
    if abs(rho) < RHO_FLOOR:
        return 0
    return 1 if l1 > 0 else -1


def score_triangle(p, q, k) -> dict:
    homo = []
    hetero = []
    for sp in (-1, 1):
        for sq in (-1, 1):
            for sk in (-1, 1):
                signs = (sp, sq, sk)
                f = helical_field(p, q, k, signs)
                row = first_variation(f)
                item = {
                    "signs": list(signs),
                    "L1": row["L1"],
                    "R2": row["R2"],
                    "rho": row["rho"],
                    "T_c": row["T_c"],
                    "expansion_ok": row["expansion_ok"],
                    "sgn": _sign_of(row["rho"], row["L1"]),
                }
                if sp == sq == sk:
                    homo.append(item)
                else:
                    hetero.append(item)
    return {"p": list(p), "q": list(q), "k": list(k), "homo": homo, "hetero": hetero}


def _collect_signs(items: list[dict]) -> set[int]:
    return {it["sgn"] for it in items if it["sgn"] != 0}


def _best_seed(items: list[dict], want: int) -> dict | None:
    cand = [it for it in items if it["sgn"] == want]
    if not cand:
        return None
    cand.sort(key=lambda it: -abs(it["rho"]))
    return cand[0]


def record() -> dict:
    # Basis checks.
    h_ok = True
    for k in ((1, 0, 0), (1, 1, 0), (2, -1, 3), (0, 0, 2)):
        for s in (-1, 1):
            h = helical(k, s)
            h_ok = h_ok and abs(float(np.linalg.norm(h)) - 1.0) < 1e-12
            h_ok = h_ok and abs(complex(np.dot(np.asarray(k, dtype=float), h))) < 1e-12
            h_ok = h_ok and abs(mode_helicity(k, h) - s) < 1e-12

    by_n = []
    seeds = []
    expansion_ok = True
    hetero_plus_ns = []
    hetero_minus_ns = []
    homo_nonzero_ns = []
    no_neighbor_ns = []

    for n in NS:
        tris = neighbor_triangles(n)
        het_signs: set[int] = set()
        homo_signs: set[int] = set()
        n_exp_ok = True
        plus_seed = None
        minus_seed = None
        scored_n = 0
        r2_over_l1 = []
        min_spread = None
        for tri in tris[:SCORE_PER_N]:
            scored = score_triangle(*tri)
            scored_n += 1
            spread = max(lam(tri[0]), lam(tri[1]), lam(tri[2])) - min(lam(tri[0]), lam(tri[1]), lam(tri[2]))
            if min_spread is None or spread < min_spread:
                min_spread = spread
            for bucket, acc in ((scored["hetero"], het_signs), (scored["homo"], homo_signs)):
                for it in bucket:
                    expansion_ok = expansion_ok and it["expansion_ok"]
                    n_exp_ok = n_exp_ok and it["expansion_ok"]
                    if abs(it["L1"]) > 1e-12:
                        r2_over_l1.append(abs(it["R2"] / it["L1"]))
                acc |= _collect_signs(bucket)
            if plus_seed is None:
                hit = _best_seed(scored["hetero"], 1)
                if hit:
                    plus_seed = {**scored, "pick": hit}
            if minus_seed is None:
                hit = _best_seed(scored["hetero"], -1)
                if hit:
                    minus_seed = {**scored, "pick": hit}

        if not tris:
            no_neighbor_ns.append(n)
            bucket = "NO_NEIGHBOR"
        elif 1 in het_signs and -1 in het_signs:
            bucket = "BOTH_SIGNS"
            hetero_plus_ns.append(n)
            hetero_minus_ns.append(n)
        elif 1 in het_signs or -1 in het_signs:
            bucket = "ONE_SIGN"
            if 1 in het_signs:
                hetero_plus_ns.append(n)
            if -1 in het_signs:
                hetero_minus_ns.append(n)
        else:
            bucket = "ZERO_ONLY"

        if homo_signs:
            homo_nonzero_ns.append(n)

        if bucket == "BOTH_SIGNS":
            for tag, seed in (("plus", plus_seed), ("minus", minus_seed)):
                if seed is None:
                    continue
                pick = seed["pick"]
                p, q, k = tuple(seed["p"]), tuple(seed["q"]), tuple(seed["k"])
                signs = tuple(pick["signs"])
                seeds.append(
                    {
                        "N": n,
                        "sign": tag,
                        "p": list(p),
                        "q": list(q),
                        "k": list(k),
                        "helicity": list(signs),
                        "amplitudes": [1.0, 1.0, 1.0],
                        "L1": pick["L1"],
                        "R2": pick["R2"],
                        "rho": pick["rho"],
                        "T_c": pick["T_c"],
                    }
                )
                # polarizations dumped as re/im pairs below (json)

        by_n.append(
            {
                "N": n,
                "n_triangles": len(tris),
                "n_scored": scored_n,
                "min_lambda_spread": min_spread,
                "mean_abs_R2_over_L1": (sum(r2_over_l1) / len(r2_over_l1)) if r2_over_l1 else None,
                "hetero_signs": sorted(het_signs),
                "homo_signs": sorted(homo_signs),
                "bucket": bucket,
                "expansion_ok": n_exp_ok,
            }
        )

    hetero_both_on_range = bool(hetero_plus_ns) and set(hetero_plus_ns) == set(hetero_minus_ns) and set(hetero_plus_ns) == set(NS) - set(no_neighbor_ns)
    hetero_any_both = any(row["bucket"] == "BOTH_SIGNS" for row in by_n)
    homo_zero_only = all(row["homo_signs"] == [] for row in by_n if row["n_triangles"])
    one_sign_only = any(row["bucket"] == "ONE_SIGN" for row in by_n) and not hetero_any_both

    # JSON-safe seeds (split complex).
    seeds_out = []
    for s in seeds:
        pols = {}
        p, q, k = tuple(s["p"]), tuple(s["q"]), tuple(s["k"])
        f = helical_field(p, q, k, tuple(s["helicity"]))
        for key in (p, q, k):
            v = f.get(key)
            pols[str(key)] = {"re": [float(v[i].real) for i in range(3)], "im": [float(v[i].imag) for i in range(3)]}
        seeds_out.append({k: s[k] for k in s if k != "polarizations"} | {"polarizations": pols})

    out = {
        "not_a_close": True,
        "star_stays_killed": True,
        "gate_unaltered": True,
        "lemma_A_unaltered": True,
        "lemma_B_open": True,
        "helical_basis_ok": h_ok,
        "expansion_ok": expansion_ok,
        "rho_floor": RHO_FLOOR,
        "N_range": list(NS),
        "by_N": by_n,
        "no_neighbor_Ns": no_neighbor_ns,
        "hetero_plus_Ns": hetero_plus_ns,
        "hetero_minus_Ns": hetero_minus_ns,
        "homo_nonzero_Ns": homo_nonzero_ns,
        "BOTH_SIGNS_on_printed_range": hetero_any_both,
        "BOTH_SIGNS_at_every_printed_N_with_neighbors": hetero_both_on_range,
        "ONE_SIGN_only_on_printed_range": one_sign_only,
        "ZERO_ONLY_homochiral_on_printed_range": homo_zero_only,
        "NO_NEIGHBOR_appeared": bool(no_neighbor_ns),
        "persistence_open": True,
        "universal_depletion_not_killed": True,
        "universal_depletion_not_proved": True,
        "static_closure_not_stopped": True,
        "A_N_plus_saved_finite_N_only": bool(seeds_out),
        "n_seeds": len(seeds_out),
        "i3_bridge_not_seated": True,
        "vandermonde_not_locked_as_remainder": True,
        "no_more_potentials": True,
        "no_clock_reinterpretation": True,
        "da_ns2_is_not_a_theorem": True,
        "sits_as_useful_K": False,
        "sits_as_g4_death": False,
        "sits_as_da_ns2": False,
        "sits_as_jgc": False,
        "sits_as_bprim": False,
        "g4_stays_open": True,
        "do_not_invent_a_bridge": True,
        "do_not_run_taylor_green": True,
        "do_not_mix_heavy": True,
        "do_not_glue_to_leftover_1": True,
        "finite_N_is_not_persistence": True,
        "static_frontier": "arithmetic sign realizability",
        "dynamic_frontier": "dangerous-state persistence",
        "seeds": seeds_out,
    }
    return out


def main() -> None:
    row = record()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(row, indent=2) + "\n")
    SEED_OUT.write_text(json.dumps({"finite_N_only": True, "persistence_open": True, "seeds": row["seeds"]}, indent=2) + "\n")
    print(json.dumps({k: row[k] for k in row if k != "seeds"}, indent=2))
    print("n_seeds", row["n_seeds"])


if __name__ == "__main__":
    main()
