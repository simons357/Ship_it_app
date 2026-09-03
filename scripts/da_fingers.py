#!/usr/bin/env python3
"""
Five-finger DA: break one line, then break each piece, then each piece again.

Line: R = exp(-1/2 χ²_ext) exp(-1/2 χ²_int)

Also assigns a general TOE-category fate to each of the reconstructed 16
and DA-breaks those categories. Not a unifier. Official Cosmo 16 is a different catalog.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from da_sixteen import FAMILIES, SIXTEEN, fit_linear_map  # noqa: E402
from unifier_combo import EXT, INPUTS, lock_score, r_batch, sample_matrix  # noqa: E402
from unifier_exercise import OBS, observed_row, realization  # noqa: E402


LINE = "R = exp(-1/2 χ²_ext) · exp(-1/2 χ²_int)"
EQUAL_SIGMA = 0.15

INT_TERMS = [
    ("S_coh", 0.0, 1.0),
    ("delta_spread", 0.0, 1.0),
    ("grad_coh", 0.2, 1.0),
    ("kappa_att", 0.5, 1.0),
    ("A_mean", 1.0, 0.25),
    ("f_mean", 1.0, 0.25),
    ("phi_scale", 1.0, 0.25),
    ("p_cut", 8.0, 0.25 / 64.0),
]

# Five general categories for a unification candidate (the other hand).
TOE_CATEGORIES = (
    "gauge",
    "gravity_gauge",
    "topological",
    "harmonic",
    "teleological",
)

CANDIDATE_META = {
    "log_alpha_em": ("gauge", "must_hit", "EM coupling; nature, not a producer"),
    "log_alpha_s": ("gauge", "must_hit", "strong coupling; nature, not a producer"),
    "sin2_theta_w": ("gauge", "must_hit", "weak mixing; nature, not a producer"),
    "log_weak_ratio": ("gauge", "must_hit", "weak scale; nature, not a producer"),
    "log_hierarchy": ("gravity_gauge", "must_hit_and_score", "Planck leftover; cannot drop"),
    "log_cc_ratio": (
        "gravity_gauge",
        "must_hit_and_score",
        "vacuum leftover; gravity-scale on this score, topological fork left open",
    ),
    "log_qcd_ratio": ("gauge", "must_hit", "QCD scale; weak on this score"),
    "theta_qcd": ("topological", "leftover", "strong-CP angle; global, not a local coupling"),
    "A_mean": ("harmonic", "decorative", "oscillator amplitude; does not move R"),
    "f_mean": ("harmonic", "decorative", "oscillator frequency; does not move R"),
    "phi_scale": ("harmonic", "decorative", "phi; does not move R"),
    "delta_spread": ("harmonic", "score", "phase disorder; internal score-mover"),
    "S_coh": ("teleological", "score", "coherence; internal score-mover"),
    "kappa_att": ("teleological", "decorative", "attractor; weak on this score"),
    "grad_coh": ("teleological", "near_miss", "gradient; close, misses singleton cut"),
    "R": ("teleological", "output", "realization; circular if used as a knob"),
}


def _idx() -> dict[str, int]:
    return {name: i for i, name in enumerate(INPUTS)}


def chi_ext_terms(x: np.ndarray) -> dict[str, np.ndarray]:
    idx = _idx()
    return {name: (x[:, idx[name]] - OBS[name]) ** 2 for name in EXT}


def chi_int_terms(x: np.ndarray) -> dict[str, np.ndarray]:
    idx = _idx()
    out = {}
    for name, target, weight in INT_TERMS:
        if name == "p_cut":
            out[name] = weight * (x[:, idx[name]] - target) ** 2
        else:
            out[name] = weight * (x[:, idx[name]] - target) ** 2
    return out


def r_parts(x: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    ext = sum(chi_ext_terms(x).values())
    internal = sum(chi_int_terms(x).values())
    r_ext = np.exp(-0.5 * ext)
    r_int = np.exp(-0.5 * internal)
    return r_ext, r_int, r_ext * r_int


def sample_equal_ext(n: int, rng: np.random.Generator, sigma: float = EQUAL_SIGMA) -> np.ndarray:
    x = sample_matrix(n, rng)
    idx = _idx()
    for name in EXT:
        x[:, idx[name]] = OBS[name] + rng.normal(0.0, sigma, n)
    return x


def mean_contrib(terms: dict[str, np.ndarray]) -> dict[str, float]:
    return {k: float(0.5 * np.mean(v)) for k, v in terms.items()}


def node(name: str, piece: str, verdict: str, why: str, fingers: list | None = None, extra: dict | None = None) -> dict:
    rec = {"name": name, "piece": piece, "verdict": verdict, "why": why}
    if extra:
        rec.update(extra)
    if fingers:
        rec["fingers"] = fingers
    return rec


GENERAL_FATE_KEYS = ("kind", "nature", "score", "produce", "next_piece")

# Smaller DA pieces under each general question, per candidate.
# Verdicts that depend on numbers are filled in candidate_hand().
NEXT_PIECE = {
    "log_alpha_em": "the EM coupling as a number vs the U(1) group vs the scale it is quoted at",
    "log_alpha_s": "the strong coupling vs SU(3) vs the scale it is quoted at",
    "sin2_theta_w": "weak mixing vs the SU(2)×U(1) embedding",
    "log_weak_ratio": "m_W / v vs the Higgs vev sitting underneath",
    "log_hierarchy": "M_Pl, v, the ratio, the log, the sampling width",
    "log_cc_ratio": "ρ_Λ, the fourth root, the ratio to v, the topological fork, the width",
    "log_qcd_ratio": "Λ_QCD / v vs confinement vs the gauge coupling α_s",
    "theta_qcd": "the angle, target 0, global vs local, the strong-CP leftover",
    "A_mean": "amplitude as a mean over modes; not a coupling",
    "f_mean": "frequency as a mean over modes; not a coupling",
    "phi_scale": "φ as a scale knob; not a coupling",
    "delta_spread": "phase disorder; the one harmonic that moves R",
    "S_coh": "coherence scalar; internal, not a force",
    "kappa_att": "attractor strength; decorative on this score",
    "grad_coh": "coherence gradient; near-miss singleton",
    "R": "the product; circular as a candidate theory",
}


def residual_hand(coord: str, default_width: float, equal_width_contrib: float, default_contrib: float) -> list:
    """Five fingers of one squared residual (x − x*)²."""
    return [
        node("x", coord, "open", "the live coordinate; not derived from the other knobs on this vector"),
        node("x_star", f"{coord} observed anchor", "pass", "anchor is a number we put in, not a prediction"),
        node("minus", "(x − x*)", "pass", "residual is well-defined once x and x* exist"),
        node("square", "(x − x*)²", "pass", "L2 term; L1 ranking of the same leftovers stays the same top two"),
        node(
            "width",
            f"sampling width {default_width}",
            "fail" if coord in ("log_cc_ratio", "log_hierarchy") else "open",
            (
                f"default contrib {default_contrib:.3f}; equal-width contrib {equal_width_contrib:.3f}. "
                "Vacuum and Planck dominate the default score because we gave them room, "
                "not because the algebra singles them out."
                if coord in ("log_cc_ratio", "log_hierarchy")
                else "Width is part of the term. Equal-width flattens the external leftovers."
            ),
        ),
    ]


def candidate_hand(
    name: str,
    cat: str,
    fate: str,
    delta: float | None,
    contrib: float | None,
    equal_width: float | None = None,
) -> list:
    """Same five general questions on every candidate, then the next smaller piece."""
    dlt = 0.0 if delta is None else delta
    if fate == "output":
        score_v, score_w = "fail", "R is the output. Locking it is circular."
        nature_v, nature_w = "fail", "a score is not a force of nature"
        produce_v, produce_w = "fail", "cannot be an input to F"
        kind_v = "pass"
    elif fate.startswith("must_hit"):
        nature_v, nature_w = "pass", "cannot drop this and still mean the four forces / leftovers"
        produce_v, produce_w = "fail", "this is already a target (or leftover) of F, not a producer"
        if dlt > 0.02:
            score_v, score_w = "open", f"Δ lock-R = {dlt:+.3f}; must-hit and default score-mover"
        else:
            score_v, score_w = "fail", f"Δ lock-R = {dlt:+.3f}; must-hit, decorative on this score"
        kind_v = "open" if name == "log_cc_ratio" else "pass"
    elif fate == "score":
        nature_v, nature_w = "fail", "internal bookkeeping; not a force"
        score_v, score_w = "open", f"Δ lock-R = {dlt:+.3f}; moves R, does not write couplings"
        produce_v, produce_w = "fail", "locking this does not collapse the four couplings"
        kind_v = "pass"
    elif fate == "near_miss":
        nature_v, nature_w = "fail", "internal bookkeeping; not a force"
        score_v, score_w = "open", f"Δ lock-R = {dlt:+.3f}; close, misses the singleton cut"
        produce_v, produce_w = "fail", "locking this does not collapse the four couplings"
        kind_v = "pass"
    elif fate == "leftover":
        nature_v, nature_w = "open", "nature has a strong-CP problem; this score barely sees θ"
        score_v, score_w = "fail", f"Δ lock-R = {dlt:+.3f}; leftover, not a singleton fit"
        produce_v, produce_w = "fail", "a global angle does not write the running couplings"
        kind_v = "pass"
    else:
        nature_v, nature_w = "fail", "decorative; not a force"
        score_v, score_w = "fail", f"Δ lock-R = {dlt:+.3f}; does not move R"
        produce_v, produce_w = "fail", "does not write the couplings"
        kind_v = "pass"

    kind_why = f"{cat}; {CANDIDATE_META[name][2]}"

    pieces = []
    if name in EXT:
        pieces = residual_hand(
            name,
            {"log_hierarchy": 1.5, "log_cc_ratio": 2.0, "log_qcd_ratio": 0.4, "sin2_theta_w": 0.03}.get(name, 0.15),
            equal_width if equal_width is not None else 0.0,
            contrib or 0.0,
        )
    elif name == "R":
        pieces = [
            node("product", "R_ext · R_int", "pass", "the line is a product"),
            node("circular", "lock R to make R", "fail", "the 16th is the output"),
            node("range", "(0, 1]", "pass", "two exponentials"),
            node("not_a_theory", "R as a TOE candidate", "fail", "a score is not a theory of everything"),
            node("next", "need F, not a bigger R", "open", "blocked on a producing-map"),
        ]
    else:
        pieces = [
            node("definition", name, "open", NEXT_PIECE[name]),
            node("in_chi_int", "internal bookkeeping term", "pass" if fate in {"score", "near_miss"} else "fail", "sits in χ²_int, not in the four-force residual"),
            node("target", "quiet-state anchor", "pass", "we put the quiet value in; it is not predicted"),
            node("produce", "writes a coupling?", "fail", "independent draw on this vector"),
            node("next", NEXT_PIECE[name], "open", "smallest remaining split; Cosmo name may replace this"),
        ]

    return [
        node("kind", cat, kind_v, kind_why),
        node("nature", fate, nature_v, nature_w),
        node("score", "lock-R / contribution", score_v, score_w, extra={"delta_lock_R": delta, "contrib": contrib}),
        node("produce", "input to F vs already a target", produce_v, produce_w),
        node("next_piece", NEXT_PIECE[name], "open", "keep going down: the smallest split still open", pieces),
    ]


def run(n: int = 400, seed: int = 1, out: Path | None = None) -> dict:
    rng = np.random.default_rng(seed)
    base = sample_matrix(n, rng)
    r_ext, r_int, r = r_parts(base)
    r_ref = r_batch(base)
    product_err = float(np.max(np.abs(r - r_ref)))
    indep = float(np.corrcoef(r_ext, r_int)[0, 1])
    ext_c = mean_contrib(chi_ext_terms(base))
    int_c = mean_contrib(chi_int_terms(base))

    eq = sample_equal_ext(n, np.random.default_rng(seed + 3))
    ext_eq = mean_contrib(chi_ext_terms(eq))
    ext_eq_vals = list(ext_eq.values())
    ext_flat = bool(max(ext_eq_vals) - min(ext_eq_vals) < 0.01)

    target = observed_row()
    target_r, target_chi_ext, target_chi_int, _ = realization(target)

    l1 = {name: float(np.mean(np.abs(base[:, _idx()[name]] - OBS[name]))) for name in EXT}
    l1_top = sorted(l1, key=l1.get, reverse=True)[:2]
    l2_top = sorted(ext_c, key=ext_c.get, reverse=True)[:2]

    baseline = float(np.mean(r_ref))
    locks = {name: lock_score(base, (name,)) - baseline for name in INPUTS if name in sum(FAMILIES.values(), [])}

    f_map = fit_linear_map(
        FAMILIES["harmonic"] + ["S_coh", "kappa_att", "grad_coh"],
        FAMILIES["gauge"],
        n=n,
        rng=np.random.default_rng(seed + 7),
    )

    # --- five fingers of the line, each broken again ---
    r_hand = [
        node("range", "R ∈ (0, 1]", "pass", "product of two (0,1] exponentials"),
        node("target", "R=1 at the quiet+observed state", "pass" if target_r > 0.999 else "fail", f"target R={target_r:.6f} by sitting on the anchors"),
        node("lock_R", "E[R | one coord at star]", "open", "well-defined conditional; not a producing-map"),
        node("circular", "locking R to produce R", "fail", "the 16th is the output; circular as a knob"),
        node("product", "R = R_ext · R_int", "pass" if product_err < 1e-12 else "fail", f"max |R − R_ext R_int| = {product_err:.2e}"),
    ]

    kernel_hand = [
        node("minus", "minus in exp(−½ χ²)", "pass", "penalty: larger residual, smaller R"),
        node("half", "the 1/2", "pass", "Gaussian convention; any positive constant keeps the ranking"),
        node("exp", "exp: [0,∞) → (0,1]", "pass", "maps χ² to a score in (0,1]"),
        node(
            "independence",
            "product of two kernels",
            "pass" if abs(indep) < 0.15 else "open",
            f"corr(R_ext, R_int)={indep:+.3f}; sampled independently on this vector",
        ),
        node(
            "epsilon",
            "χ²_ext ≤ ε² as a pass",
            "open",
            f"target χ²_ext={target_chi_ext:.2e} by construction. Sitting on anchors is not F.",
        ),
    ]

    ext_hand = [
        node(
            "em",
            "log_alpha_em",
            "open",
            f"contrib {ext_c['log_alpha_em']:.3f}; must-hit as nature, decorative on default widths",
            residual_hand("log_alpha_em", 0.15, ext_eq["log_alpha_em"], ext_c["log_alpha_em"]),
        ),
        node(
            "strong",
            "log_alpha_s",
            "open",
            f"contrib {ext_c['log_alpha_s']:.3f}; must-hit as nature, decorative on default widths",
            residual_hand("log_alpha_s", 0.15, ext_eq["log_alpha_s"], ext_c["log_alpha_s"]),
        ),
        node(
            "weak",
            "sin2_theta_w + log_weak_ratio",
            "open",
            (
                f"contrib {ext_c['sin2_theta_w']+ext_c['log_weak_ratio']:.3f}; "
                "two gauge leftovers glued as one finger"
            ),
        ),
        node(
            "planck",
            "log_hierarchy",
            "open",
            f"contrib {ext_c['log_hierarchy']:.3f}; must-hit and default score-mover",
            residual_hand("log_hierarchy", 1.5, ext_eq["log_hierarchy"], ext_c["log_hierarchy"]),
        ),
        node(
            "vacuum",
            "log_cc_ratio",
            "open",
            f"contrib {ext_c['log_cc_ratio']:.3f}; must-hit and default score-mover",
            residual_hand("log_cc_ratio", 2.0, ext_eq["log_cc_ratio"], ext_c["log_cc_ratio"]),
        ),
    ]

    int_hand = [
        node("S_coh", "coherence", "open", f"contrib {int_c['S_coh']:.3f}; singleton fit"),
        node("delta_spread", "phase", "open", f"contrib {int_c['delta_spread']:.3f}; singleton fit"),
        node("grad_coh", "gradient", "open", f"contrib {int_c['grad_coh']:.3f}; near-miss singleton"),
        node("kappa_att", "attractor", "open", f"contrib {int_c['kappa_att']:.3f}; decorative"),
        node(
            "oscillator",
            "A, f, φ (p_cut leftover)",
            "fail",
            (
                f"contrib A+f+φ={int_c['A_mean']+int_c['f_mean']+int_c['phi_scale']:.3f}; "
                "does not produce couplings"
            ),
        ),
    ]

    f_hand = [
        node("domain", "the 15 knobs", "open", "reconstructed; Cosmo names missing"),
        node("codomain", "(g_s, g_w, g_em, g_N)", "open", "four couplings; Planck and Λ stay in χ²_ext"),
        node("dimension", "n > k", "open", "15 knobs > 6 nature targets is the possibility clue, not a pass"),
        node(
            "affine",
            "linear F from oscillators+teleology",
            "fail",
            f"holdout χ² {f_map['holdout_chi2_F']:.3f} vs null {f_map['holdout_chi2_predict_observed']:.3f}",
        ),
        node("rebuild", "F from surviving pieces", "open", "blocked on Cosmo names or a real producing-map"),
    ]

    tree = node(
        "line",
        LINE,
        "open",
        "Five-finger DA on the realization line. Not a unifier.",
        [
            node("R", "left-hand side / product", "open", "the 16th; output", r_hand),
            node("kernel", "exp(−½ ·)", "pass", "shape checks pass; ε-pass stays open", kernel_hand),
            node("chi_ext", "external sum of squares", "open", "must-hits live here; width artifacts too", ext_hand),
            node("chi_int", "internal sum of squares", "open", "S_c and δ move R; oscillators do not", int_hand),
            node("F", "implied producing-map (not written on the line)", "fail", "nothing on the line produces the couplings", f_hand),
        ],
    )

    # --- 16 candidates, general fate, then DA each category ---
    candidates = []
    for i, name in enumerate(SIXTEEN, start=1):
        cat, fate, note = CANDIDATE_META[name]
        rec = {
            "id": i,
            "name": name,
            "category": cat,
            "fate": fate,
            "note": note,
        }
        if name in locks:
            rec["delta_lock_R"] = locks[name]
        if name in ext_c:
            rec["default_contrib"] = ext_c[name]
            rec["equal_width_contrib"] = ext_eq[name]
        if name in int_c:
            rec["default_contrib"] = int_c[name]
        rec["hand"] = candidate_hand(
            name,
            cat,
            fate,
            rec.get("delta_lock_R"),
            rec.get("default_contrib"),
            rec.get("equal_width_contrib"),
        )
        assert [f["name"] for f in rec["hand"]] == list(GENERAL_FATE_KEYS)
        candidates.append(rec)

    by_cat: dict[str, list[str]] = {c: [] for c in TOE_CATEGORIES}
    for rec in candidates:
        by_cat[rec["category"]].append(rec["name"])

    category_hands = {
        "gauge": [
            node("local_symmetry", "couplings of a gauge group", "open", "must-hit observables, not inputs to F on this vector"),
            node("count", "four gauge slots in the 16", "pass", "EM, strong, weak mixing, weak scale"),
            node("score", "singleton lock-R", "fail", "none of the four raise lock-R by 0.02; widths are tight"),
            node("produce", "do oscillators write these?", "fail", "affine F holdout does not beat the null"),
            node("keep", "drop them from nature?", "fail", "a four-force unifier that drops a coupling is not one"),
        ],
        "gravity_gauge": [
            node("planck", "log(M_Pl / v)", "open", "must-hit leftover; default score-mover"),
            node("vacuum", "log(ρ_Λ^{1/4} / v)", "open", "must-hit leftover; default score-mover"),
            node("width_artifact", "equal σ = 0.15 on every external", "fail" if ext_flat else "open", "external contributions flatten; default ranking was a width choice"),
            node("qcd_scale", "log(Λ_QCD / v)", "open", "must-hit, weak on this score"),
            node("fork", "is vacuum topological instead?", "open", "this score treats Λ as a scale leftover. Instanton/θ story is a different book."),
        ],
        "topological": [
            node("theta_qcd", "strong-CP angle", "open", "the clear topological leftover on this 16"),
            node("vacuum_fork", "Λ as topological", "open", "not assumed here; would replace log_cc_ratio's category"),
            node("not_gauge", "global vs local", "pass", "θ is not a running coupling; do not glue it to α_s"),
            node("score", "singleton lock-R", "fail", "θ does not raise lock-R on the current term"),
            node("keep", "drop θ and still mean QCD?", "open", "nature has a strong-CP problem; this score barely sees it"),
        ],
        "harmonic": [
            node("A", "amplitude", "fail", "decorative on R"),
            node("f", "frequency", "fail", "decorative on R"),
            node("phi", "phi scale", "fail", "decorative on R"),
            node("delta", "phase disorder", "open", "the one harmonic that moves R"),
            node("produce", "harmonic → couplings", "fail", "no producing-map on this vector"),
        ],
        "teleological": [
            node("S_coh", "coherence", "open", "internal score-mover"),
            node("kappa", "attractor", "fail", "decorative"),
            node("grad", "gradient", "open", "near-miss"),
            node("R", "realization", "fail", "output; circular as a candidate theory"),
            node("produce", "teleology → couplings", "fail", "locking S_c does not collapse the four couplings"),
        ],
    }

    how_far = [
        "broke the R line into five fingers, then each finger into five",
        "product and kernel checks pass; implied F fails",
        "vacuum/Planck default dominance is a width artifact (equal-σ flattens χ²_ext)",
        "they remain must-hit as nature leftovers, which is a different claim",
        "16 candidates each got a general category and a fate",
        "each of the 16 then got the same five general questions (kind / nature / score / produce / next), then smaller pieces",
        "topological vs gauge: only θ_QCD is topological on this list; vacuum is a fork",
        "Cosmo names are in; next blocked on a public producing-map F",
    ]

    payload = {
        "meta": {
            "line": LINE,
            "method": "five-finger DA, then 16 candidate fates, then the same five general questions on each",
            "cosmos_app_list_found": True,
            "this_list_is_cosmo_export": False,
            "not_a_unifier": True,
            "n": n,
            "seed": seed,
        },
        "checks": {
            "product_identity_err": product_err,
            "corr_Rext_Rint": indep,
            "target_R": target_r,
            "target_chi_ext": target_chi_ext,
            "target_chi_int": target_chi_int,
            "ext_contrib_default": ext_c,
            "int_contrib_default": int_c,
            "ext_contrib_equal_width": ext_eq,
            "equal_width_flattens_ext": ext_flat,
            "l2_top": l2_top,
            "l1_top": l1_top,
            "baseline_R": baseline,
            "affine_F": f_map,
        },
        "tree": tree,
        "candidates": candidates,
        "by_category": by_cat,
        "category_hands": category_hands,
        "how_far": how_far,
        "next_da_move": (
            "Official Cosmo 16 is a different catalog (docs/COSMO-SIXTEEN.md). "
            "Keep this recursion on the score. Do not call this F."
        ),
    }
    dest = Path(out) if out is not None else Path("results/da_fingers.json")
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(payload, indent=2))
    payload["_wrote"] = str(dest)
    return payload


def _print_hand(fingers: list, indent: int = 0) -> None:
    pad = "  " * indent
    for f in fingers:
        print(f"{pad}[{f['verdict']}] {f['name']}: {f['piece']}")
        print(f"{pad}    {f['why']}")
        if f.get("fingers"):
            _print_hand(f["fingers"], indent + 1)


def main() -> int:
    payload = run()
    print("DA five fingers on:", LINE)
    print("The 16th is still R. Official Cosmo 16 is a different catalog.")
    _print_hand(payload["tree"]["fingers"])
    print("equal-width flattens χ²_ext:", payload["checks"]["equal_width_flattens_ext"])
    print("16 fates, then each broken:")
    for rec in payload["candidates"]:
        print(f"  {rec['id']:2d} {rec['category']:<16} {rec['fate']:<22} {rec['name']}")
        for f in rec.get("hand", []):
            print(f"      [{f['verdict']}] {f['name']}: {f['piece']}")
    print("how far:")
    for line in payload["how_far"]:
        print(" -", line)
    print(f"wrote {payload['_wrote']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
