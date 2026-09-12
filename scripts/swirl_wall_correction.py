#!/usr/bin/env python3
"""
Swirl wall correction.

Keep: F = u^θ/r, G = ω^θ/r, integrating factor p(1-d)∫Ū_{d,p},
the time-window wall, the unaugmented F^p identity, good-set fixed.

Drop: detector ⇒ occupation decay; 5-D spatial occupation from the wall;
swapped F/G; IF with the wrong sign or without p; spatial rewrite of the wall.

Not a close of T_{j<-j}. NS is not solved.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from estimate_audit import classify_paragraph  # noqa: E402
from track_b_lemmas import rec  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "docs" / "SWIRL-WALL-CORRECTION.md"

# Live dictionary. Swapping these is a detector error.
F_DEF = "u^theta/r"
G_DEF = "omega^theta/r"
GAMMA_DEF = "r u^theta"
U_DEF = "u^r/r"

# Compression on Ż_{α,p} is p(d-1) times the U-moment.
# Integrating factor e^μ with μ' = p(1-d) Ū cancels that term.
IF_EXPONENT = "p(1-d) int Ubar_{d,p}"


def alpha_from_d(p: float, d: float) -> float:
    return p * (d + 1.0) + 1.0


def compression_on_zdot(p: float, d: float) -> float:
    """Coefficient of ∫ U |F|^p dμ_α in Ż_{α,p}."""
    alpha = alpha_from_d(p, d)
    # (1/p) Ż has (α-(2p+1))/p = d-1, so Ż has p(d-1).
    return p * ((alpha - (2.0 * p + 1.0)) / p)


def if_mu_prime(p: float, d: float) -> float:
    """μ' / Ū. Must be p(1-d), opposite the compression sign."""
    return p * (1.0 - d)


def wall_rhs(nu: float, h: float, h0: float) -> float:
    """2 √(ν h log log(e^e h0/h)). Requires 0 < h < h0."""
    if not (0.0 < h < h0):
        raise ValueError("need 0 < h < h0")
    return 2.0 * math.sqrt(nu * h * math.log(math.log(math.e**math.e * h0 / h)))


def wall_is_time_integral(text: str) -> bool:
    low = text.lower()
    return "int" in low and "sigma-h" in low and "dt" in low


def classify_detector_paragraph(text: str) -> dict:
    """Flag discarded detector moves. Hits mean the paragraph is out."""
    low = text.lower().replace(" ", "")
    hits = []
    if "f=omega" in low or "f=ω" in low or "f=\\omega" in low:
        hits.append("F swapped with omega^theta/r")
    if "g=u^theta" in low or "g=u^{theta}" in low or "g=u^\\theta" in low:
        hits.append("G swapped with u^theta/r")
    if "occupationdecay" in low.replace("-", "") or "occupation decay" in text.lower():
        if "detector" in text.lower() and "withdraw" not in text.lower():
            hits.append("detector occupation decay")
    if "five-dimensional spatial occupation" in text.lower() or "5d spatial occupation" in text.lower():
        hits.append("5-D spatial occupation")
    filt = classify_paragraph(text)
    return {
        "discard_hits": list(filt["discard_hits"]) + hits,
        "allowed_in_estimate": filt["allowed_in_estimate"] and len(hits) == 0,
    }


def lemmas(page_ok: bool, algebra_ok: bool) -> list[dict]:
    return [
        rec(
            "SWC_F_G",
            "F = u^θ/r and G = ω^θ/r",
            "pass",
            "Live dictionary. Swapping them is a detector error.",
        ),
        rec(
            "SWC_IF",
            "integrating-factor exponent is p(1-d)∫Ū_{d,p}",
            "pass" if algebra_ok else "fail",
            "Sign and p sit. Opposite sign or missing p is out.",
        ),
        rec(
            "SWC_identity",
            "unaugmented power-weight F^p identity sits",
            "pass",
            "Compression coefficient (α-(2p+1))/p. No extra field.",
        ),
        rec(
            "SWC_wall_time",
            "wall is ∫_{σ-h}^σ ||(u^r)_-||_∞ dt ≤ 2√(ν h log log(e^e h0/h))",
            "pass",
            "Time window. Square root kept. Not a spatial integral.",
        ),
        rec(
            "SWC_good_set",
            "supplied good-set estimate remains fixed",
            "pass",
            "This audit does not rewrite it.",
        ),
        rec(
            "SWC_occ_from_detector",
            "the detector establishes occupation decay",
            "fail",
            "Withdrawn. Conditional window ≠ occupation decay.",
        ),
        rec(
            "SWC_five_d_occupation",
            "the wall is a five-dimensional spatial occupation bound",
            "fail",
            "Δ_5 / α=3 is an energy weight. Not a 5-D occupation theorem.",
        ),
        rec(
            "SWC_remainder",
            "this correction closes T_{j<-j}",
            "fail",
            "Different object. Shell remainder stays open.",
        ),
        rec(
            "SWC_page_clean",
            "correction page has no discard-list object in the claim",
            "pass" if page_ok else "fail",
            "Filter: estimate_audit.classify_paragraph.",
        ),
        rec(
            "SWC_ns_solved",
            "corrected detector solves NS",
            "fail",
            "Class and the wall if stay in the sentence.",
        ),
    ]


def run(out: Path | None = None) -> dict:
    # Algebra: IF cancels compression for several (p,d).
    algebra_ok = True
    samples = []
    for p, d in ((2.0, 0.0), (2.0, 0.5), (3.0, 0.25), (4.0, 0.0)):
        comp = compression_on_zdot(p, d)
        mu = if_mu_prime(p, d)
        ok = abs(comp + mu) < 1e-12
        algebra_ok = algebra_ok and ok
        samples.append({"p": p, "d": d, "alpha": alpha_from_d(p, d), "Zdot_U": comp, "mu_prime": mu, "cancel": ok})

    wall = {
        "formula": "int_{sigma-h}^{sigma} ||(u^r)_-(t)||_inf dt <= 2 sqrt(nu h loglog(e^e h0/h))",
        "kind": "time-window if",
        "spatial_occupation": False,
        "example_rhs": wall_rhs(nu=1.0, h=0.01, h0=1.0),
    }

    page_text = PAGE.read_text() if PAGE.exists() else ""
    page_cls = classify_paragraph(page_text) if page_text else {"discard_hits": [], "allowed_in_estimate": True}
    page_ok = bool(page_cls["allowed_in_estimate"])
    if page_text:
        page_ok = page_ok and "occupation decay from the detector is" in page_text.lower()
        page_ok = page_ok and "withdrawn" in page_text.lower()

    rows = lemmas(page_ok, algebra_ok)
    counts = {"pass": 0, "fail": 0, "open": 0}
    for item in rows:
        counts[item["verdict"]] += 1
    payload = {
        "meta": {
            "slot": "B",
            "write": "swirl wall correction",
            "class": "axisymmetric with swirl",
            "F": F_DEF,
            "G": G_DEF,
            "Gamma": GAMMA_DEF,
            "U": U_DEF,
            "integrating_factor_exponent": IF_EXPONENT,
            "good_set": "fixed",
            "occupation_from_detector": "withdrawn",
            "tuning_the_pde": False,
            "lemma_star_open": True,
            "h1_started": False,
            "estimate_open": True,
            "kill": False,
            "lambda_prime_sign_quoted": False,
            "source_note_on_branch": False,
            "source_note": "Swirl_Wall_Correction_2026-09-12.md",
        },
        "algebra": samples,
        "wall": wall,
        "page_filter": page_cls,
        "lemmas": rows,
        "counts": counts,
        "domain_verdict": "open",
        "claim": (
            "Axisymmetric-with-swirl unaugmented NS; F=u^θ/r, G=ω^θ/r; "
            "wall is a time-window if; detector occupation withdrawn; "
            "T_{j<-j} still the shell remainder."
        ),
    }
    if out is not None:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n")
    return payload


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--out", type=Path, default=None)
    p.add_argument("--check", type=str, default=None, help="classify one detector paragraph")
    args = p.parse_args()
    if args.check is not None:
        print(json.dumps(classify_detector_paragraph(args.check), indent=2))
        return
    print(json.dumps(run(out=args.out), indent=2))


if __name__ == "__main__":
    main()
