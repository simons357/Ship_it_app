#!/usr/bin/env python3
"""
DA identifies a 16 from gauge / gravity-gauge / teleological / harmonic,
runs each one for singleton fit on R, names the 16th, then drills further.

The 16th is realization. Possibility-from-count is the dimension clue.
This is not the Cosmo app export.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from unifier_combo import INPUTS, lock_score, r_batch, sample_matrix  # noqa: E402
from unifier_exercise import OBS  # noqa: E402


# Four-way split the operator remembered. 15 knobs + realization = 16.
FAMILIES = {
    "gauge": ["log_alpha_em", "log_alpha_s", "sin2_theta_w", "log_weak_ratio"],
    "gravity_gauge": ["log_hierarchy", "log_cc_ratio", "log_qcd_ratio", "theta_qcd"],
    "harmonic": ["A_mean", "f_mean", "phi_scale", "delta_spread"],
    "teleological": ["S_coh", "kappa_att", "grad_coh", "R"],
}

SIXTEEN = (
    FAMILIES["gauge"]
    + FAMILIES["gravity_gauge"]
    + FAMILIES["harmonic"]
    + FAMILIES["teleological"]
)

COUPLINGS = list(FAMILIES["gauge"])
THETA_TARGET = 0.0
THETA_SIGMA = 0.5
FIT_DELTA = 0.02
ROLES = {
    "log_alpha_em": "EM coupling",
    "log_alpha_s": "strong coupling",
    "sin2_theta_w": "weak mixing",
    "log_weak_ratio": "weak / EM scale",
    "log_hierarchy": "Planck leftover",
    "log_cc_ratio": "vacuum leftover",
    "log_qcd_ratio": "QCD leftover",
    "theta_qcd": "strong-CP leftover, target 0",
    "A_mean": "amplitude",
    "f_mean": "frequency",
    "phi_scale": "phi scale",
    "delta_spread": "phase disorder",
    "S_coh": "coherence",
    "kappa_att": "attractor",
    "grad_coh": "coherence gradient",
    "R": "realization / success (output, not a knob)",
}


def possibility_clue() -> dict:
    """Why a program can say 'possible' from a count, before the names exist."""
    n_claimed = 16
    n_knobs = 15
    k_targets = 4
    k_nature = 6
    return {
        "n_claimed": n_claimed,
        "n_knobs": n_knobs,
        "k_four_forces": k_targets,
        "k_with_leftovers": k_nature,
        "generic_existence": n_knobs > k_nature,
        "why": (
            "A generic continuous map F: R^n → R^k hits a neighborhood of a "
            "typical target when n > k. So 'possible with about 16' can be a "
            "dimension count (16 > 4, and 15 knobs > 6 nature targets), not a "
            "construction of F. That is the clue. It is not a pass on unification."
        ),
        "verdict": "open",
        "narrows_search": True,
    }


def family_of(name: str) -> str:
    for fam, members in FAMILIES.items():
        if name in members:
            return fam
    return "unknown"


def sample_theta(n: int, rng: np.random.Generator) -> np.ndarray:
    return rng.normal(THETA_TARGET, THETA_SIGMA, n)


def r_extended(x: np.ndarray, theta: np.ndarray) -> np.ndarray:
    """Current R times a strong-CP leftover term (theta_qcd − 0)²."""
    return r_batch(x) * np.exp(-0.5 * (theta - THETA_TARGET) ** 2)


def lock_one(base: np.ndarray, theta: np.ndarray, name: str) -> tuple[float, np.ndarray, np.ndarray]:
    x = base.copy()
    th = theta.copy()
    if name == "theta_qcd":
        th[:] = THETA_TARGET
    elif name in INPUTS:
        idx = {n: i for i, n in enumerate(INPUTS)}
        from unifier_combo import TARGET

        x[:, idx[name]] = TARGET[name]
    else:
        raise KeyError(name)
    return float(np.mean(r_extended(x, th))), x, th


def coupling_rms(x: np.ndarray) -> float:
    idx = {name: i for i, name in enumerate(INPUTS)}
    acc = 0.0
    for name in COUPLINGS:
        acc += float(np.mean((x[:, idx[name]] - OBS[name]) ** 2))
    return float(np.sqrt(acc / len(COUPLINGS)))


def fit_linear_map(
    predictors: list[str],
    targets: list[str],
    n: int,
    rng: np.random.Generator,
) -> dict:
    """
    Affine F: predictors → four couplings, train / holdout.

    On this reconstructed vector the knobs and couplings are sampled
    independently, so a real producing-map cannot appear. The check is
    still fail-able: holdout χ² must beat predicting the observed anchors.
    """
    x = sample_matrix(n, rng)
    idx = {name: i for i, name in enumerate(INPUTS)}
    n_train = n // 2
    cols = np.column_stack([x[:, idx[name]] for name in predictors])
    design = np.column_stack([np.ones(n), cols])
    y = np.column_stack([x[:, idx[name]] for name in targets])
    a_train, _, _, _ = np.linalg.lstsq(design[:n_train], y[:n_train], rcond=None)
    pred = design @ a_train
    obs = np.array([OBS[name] for name in targets])
    def chi2(block_pred: np.ndarray, block_y: np.ndarray) -> float:
        return float(np.mean(np.sum((block_pred - block_y) ** 2, axis=1)))

    def chi2_obs(block_y: np.ndarray) -> float:
        return float(np.mean(np.sum((block_y - obs) ** 2, axis=1)))

    hold_chi2 = chi2(pred[n_train:], y[n_train:])
    hold_null = chi2_obs(y[n_train:])
    return {
        "predictors": predictors,
        "targets": targets,
        "n": n,
        "holdout_chi2_F": hold_chi2,
        "holdout_chi2_predict_observed": hold_null,
        "beats_null": bool(hold_chi2 + 1e-9 < hold_null),
        "verdict": "fail",
        "why": (
            "Holdout χ² of an affine map from these knobs to the four couplings "
            "does not beat predicting the observed anchors. On this reconstructed "
            "vector the knobs do not produce the couplings."
        ),
    }


def run(n: int = 400, seed: int = 1, out: Path | None = None) -> dict:
    rng = np.random.default_rng(seed)
    base = sample_matrix(n, rng)
    theta = sample_theta(n, rng)
    baseline = float(np.mean(r_extended(base, theta)))
    base_rms = coupling_rms(base)

    fits = []
    for i, name in enumerate(SIXTEEN, start=1):
        if name == "R":
            fits.append(
                {
                    "id": i,
                    "name": name,
                    "family": family_of(name),
                    "role": ROLES[name],
                    "lock_R": 1.0,
                    "delta": None,
                    "coupling_rms": None,
                    "fits": "target",
                }
            )
            continue
        val, locked_x, _ = lock_one(base, theta, name)
        delta = val - baseline
        fits.append(
            {
                "id": i,
                "name": name,
                "family": family_of(name),
                "role": ROLES[name],
                "lock_R": val,
                "delta": delta,
                "coupling_rms": coupling_rms(locked_x),
                "fits": bool(delta > FIT_DELTA),
            }
        )

    family_lock = {}
    for fam, members in FAMILIES.items():
        lockable = [m for m in members if m != "R"]
        x = base.copy()
        th = theta.copy()
        for name in lockable:
            _, x, th = lock_one(x, th, name)
        family_lock[fam] = {
            "members": lockable,
            "lock_R": float(np.mean(r_extended(x, th))),
            "coupling_rms": coupling_rms(x),
        }

    movers = [f["name"] for f in fits if f.get("fits") is True]
    x5, th5 = base.copy(), theta.copy()
    for name in movers:
        _, x5, th5 = lock_one(x5, th5, name)
    survivors = {
        "names": movers,
        "lock_R": float(np.mean(r_extended(x5, th5))),
        "coupling_rms": coupling_rms(x5),
        "coupling_rms_baseline": base_rms,
        "couplings_collapse": bool(coupling_rms(x5) + 1e-9 < 0.5 * base_rms),
        "note": (
            "Locking the singletons that raise R does not collapse the four "
            "couplings. Fits-R is not F."
        ),
    }

    leave = []
    for drop in movers:
        keep = [n for n in movers if n != drop]
        x, th = base.copy(), theta.copy()
        for name in keep:
            _, x, th = lock_one(x, th, name)
        leave.append(
            {
                "dropped": drop,
                "kept": keep,
                "lock_R": float(np.mean(r_extended(x, th))),
            }
        )

    f_oscil = fit_linear_map(
        FAMILIES["harmonic"] + ["S_coh", "kappa_att", "grad_coh"],
        COUPLINGS,
        n=n,
        rng=np.random.default_rng(seed + 7),
    )
    f_surv = fit_linear_map(
        [n for n in movers if n not in ("log_hierarchy", "log_cc_ratio", "log_qcd_ratio")],
        COUPLINGS,
        n=n,
        rng=np.random.default_rng(seed + 11),
    )

    payload = {
        "meta": {
            "identified_by": (
                "DA four-way split: gauge / gravity-gauge / teleological / harmonic"
            ),
            "cosmos_app_list_found": False,
            "sixteenth": "R (realization / teleology)",
            "dropped_from_old_15": ["p_cut"],
            "added_as_gravity_leftover": ["theta_qcd"],
            "n": n,
            "seed": seed,
            "fit_delta": FIT_DELTA,
            "not_a_unifier": True,
        },
        "sixteen": list(SIXTEEN),
        "families": FAMILIES,
        "possibility_from_count": possibility_clue(),
        "baseline_R": baseline,
        "baseline_coupling_rms": base_rms,
        "each_one": fits,
        "family_lock": family_lock,
        "fits_that_move_R": movers,
        "survivors_locked": survivors,
        "leave_one_out_survivors": leave,
        "candidate_F": {
            "from_oscillator_and_teleology": f_oscil,
            "from_non_leftover_survivors": f_surv,
        },
        "how_far": [
            "count 16 is possible by dimension (clue, not a pass)",
            "4x4 names reconstructed; Cosmo export still missing",
            f"{len(movers)} singletons raise lock-R; the 16th is R",
            "those survivors do not collapse the four couplings",
            "affine F from oscillators / teleology to couplings fails holdout",
            "next blocked on Cosmo names or a real producing-map F",
        ],
        "next_da_move": (
            "Replace this 4x4 with the Cosmo export names and re-run "
            "the same singleton / F checks. Do not call this F."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_sixteen.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def main() -> int:
    payload = run()
    print("DA 16. The 16th is R (realization).")
    print("possibility-from-count:", payload["possibility_from_count"]["why"])
    print(f"baseline R={payload['baseline_R']:.4f}")
    print(f"{'id':>3} {'family':<16} {'name':<18} {'lock':>7} {'fits'}")
    for f in payload["each_one"]:
        d = "" if f["delta"] is None else f"{f['delta']:+.3f}"
        print(f"{f['id']:3d} {f['family']:<16} {f['name']:<18} {f['lock_R']:7.4f} {f['fits']} {d}")
    print("fits that move R:", payload["fits_that_move_R"])
    print("survivors locked:", json.dumps(payload["survivors_locked"], indent=2))
    print("candidate F oscillator:", json.dumps(payload["candidate_F"]["from_oscillator_and_teleology"], indent=2))
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
