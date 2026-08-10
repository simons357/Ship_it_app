#!/usr/bin/env python3
"""
Harmonic Blueprint Experiment 01
Cross-Event Spectral Selection in Black-Hole Ringdown

Tests whether dimensionless ringdown-mode relationships cluster around
predefined spectral node families more strongly than a Monte Carlo null,
with Benjamini–Hochberg FDR control and leave-one-event-out stability.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

# Geometric G=c=1 conversion: solar mass in seconds
MSUN_SECONDS = 4.925490947e-6


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class NodeFamily:
    name: str
    nodes: np.ndarray
    hypothesis: str = "control"


@dataclass
class ScoreResult:
    family: str
    hypothesis: str
    score: float
    n_obs: int
    p_value: float
    q_value: float
    loo_min_score: float
    loo_max_score: float
    loo_driven_by_one: bool


# ---------------------------------------------------------------------------
# Loading
# ---------------------------------------------------------------------------

def load_nodes(path: Path, rng: np.random.Generator) -> List[NodeFamily]:
    """Load node families from JSON. Random families are realized once and frozen."""
    raw = json.loads(path.read_text())
    sigma = float(raw.get("sigma", 0.05))
    families: List[NodeFamily] = []
    for item in raw["families"]:
        name = item["name"]
        hypothesis = item.get("hypothesis", "control")
        if "nodes" in item:
            nodes = np.asarray(item["nodes"], dtype=float)
        elif item.get("generator") == "log_uniform_random":
            n = int(item.get("n", 20))
            lo = float(item.get("min", 0.5))
            hi = float(item.get("max", 2.0))
            # Draw once so the family is fixed for the whole run
            nodes = np.exp(rng.uniform(np.log(lo), np.log(hi), size=n))
            nodes.sort()
        else:
            raise ValueError(f"Family {name!r} needs 'nodes' or a supported generator")
        if np.any(nodes <= 0):
            raise ValueError(f"Family {name!r} contains non-positive nodes")
        families.append(NodeFamily(name=name, nodes=nodes, hypothesis=hypothesis))
    return families, sigma, raw.get("observable", "frequency_ratio"), raw.get("meta", {})


def load_events(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"event_id", "mode", "split"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV missing columns: {sorted(missing)}")
    return df


# ---------------------------------------------------------------------------
# Observables (dimensionless)
# ---------------------------------------------------------------------------

def geometric_mass(m_msun: float) -> float:
    return float(m_msun) * MSUN_SECONDS


def mode_omega_r(row: pd.Series) -> Optional[float]:
    """Return angular frequency omega_R in rad/s if available."""
    if "omega_R" in row and pd.notna(row["omega_R"]):
        return float(row["omega_R"])
    if "f_Hz" in row and pd.notna(row["f_Hz"]):
        return 2.0 * math.pi * float(row["f_Hz"])
    return None


def mode_omega_i(row: pd.Series) -> Optional[float]:
    """Return |omega_I| in rad/s if available."""
    if "omega_I" in row and pd.notna(row["omega_I"]):
        return abs(float(row["omega_I"]))
    if "tau_s" in row and pd.notna(row["tau_s"]) and float(row["tau_s"]) > 0:
        return 1.0 / float(row["tau_s"])
    if "tau_ms" in row and pd.notna(row["tau_ms"]) and float(row["tau_ms"]) > 0:
        return 1000.0 / float(row["tau_ms"])
    return None


def dimensionless_m_omega(df: pd.DataFrame) -> List[Tuple[str, float]]:
    out: List[Tuple[str, float]] = []
    for _, row in df.iterrows():
        om = mode_omega_r(row)
        if om is None or pd.isna(row.get("M_msun")):
            continue
        m = geometric_mass(float(row["M_msun"]))
        x = m * om
        if x > 0:
            out.append((str(row["event_id"]), float(x)))
    return out


def frequency_ratios(df: pd.DataFrame) -> List[Tuple[str, float]]:
    """Pairwise omega_R(i)/omega_R(j) for i != j within each event, j lower mode label."""
    out: List[Tuple[str, float]] = []
    for event_id, group in df.groupby("event_id"):
        modes = []
        for _, row in group.iterrows():
            om = mode_omega_r(row)
            if om is not None and om > 0:
                modes.append((str(row["mode"]), om))
        modes.sort(key=lambda t: t[0])
        for i in range(len(modes)):
            for j in range(i):
                ratio = modes[i][1] / modes[j][1]
                if ratio > 0:
                    out.append((str(event_id), float(ratio)))
                    # also reciprocal so node families covering both >1 and <1 are usable
                    out.append((str(event_id), float(1.0 / ratio)))
    return out


def quality_factors(df: pd.DataFrame) -> List[Tuple[str, float]]:
    out: List[Tuple[str, float]] = []
    for _, row in df.iterrows():
        om_r = mode_omega_r(row)
        om_i = mode_omega_i(row)
        if om_r is None or om_i is None or om_i <= 0:
            continue
        q = om_r / (2.0 * om_i)
        if q > 0:
            out.append((str(row["event_id"]), float(q)))
    return out


def nonlinear_detuning(df: pd.DataFrame) -> List[Tuple[str, float]]:
    """
    For triples i,j,k within an event:
        D_ijk = |omega_i + omega_j - omega_k| / omega_k
    Prefer labeled combinations when modes look like 220,221,440-style harmonics.
    """
    out: List[Tuple[str, float]] = []
    for event_id, group in df.groupby("event_id"):
        entries = []
        for _, row in group.iterrows():
            om = mode_omega_r(row)
            if om is not None and om > 0:
                entries.append((str(row["mode"]), om))
        if len(entries) < 2:
            continue
        # All ordered triples with distinct indices when >=3 modes;
        # for 2 modes, also form  i+i ~ k style self-coupling proxy.
        n = len(entries)
        if n >= 3:
            for i in range(n):
                for j in range(i, n):
                    for k in range(n):
                        if k == i or k == j:
                            continue
                        wi, wj, wk = entries[i][1], entries[j][1], entries[k][1]
                        d = abs(wi + wj - wk) / wk
                        if d > 0:
                            out.append((str(event_id), float(d)))
        else:
            w0, w1 = entries[0][1], entries[1][1]
            for a, b, c in ((w0, w0, w1), (w1, w1, w0), (w0, w1, w1)):
                d = abs(a + b - c) / c
                if d > 0:
                    out.append((str(event_id), float(d)))
    return out


OBSERVABLE_BUILDERS = {
    "m_omega": dimensionless_m_omega,
    "frequency_ratio": frequency_ratios,
    "quality_factor": quality_factors,
    "detuning": nonlinear_detuning,
}


def build_observables(df: pd.DataFrame, observable: str) -> List[Tuple[str, float]]:
    if observable not in OBSERVABLE_BUILDERS:
        raise ValueError(
            f"Unknown observable {observable!r}. "
            f"Choose from: {sorted(OBSERVABLE_BUILDERS)}"
        )
    xs = OBSERVABLE_BUILDERS[observable](df)
    if not xs:
        raise ValueError(f"No observables of type {observable!r} could be built from CSV")
    return xs


# ---------------------------------------------------------------------------
# Spectral proximity statistic
# ---------------------------------------------------------------------------

def log_distance(x: float, nodes: np.ndarray) -> float:
    return float(np.min(np.abs(np.log(x / nodes))))


def compatibility(x: float, nodes: np.ndarray, sigma: float) -> float:
    d = log_distance(x, nodes)
    return math.exp(-(d * d) / (2.0 * sigma * sigma))


def score(values: Sequence[float], nodes: np.ndarray, sigma: float) -> float:
    if not values:
        return float("nan")
    return float(np.mean([compatibility(x, nodes, sigma) for x in values]))


# ---------------------------------------------------------------------------
# Null model and multiple comparisons
# ---------------------------------------------------------------------------

def log_uniform_null_scores(
    values: Sequence[float],
    nodes: np.ndarray,
    sigma: float,
    n_mc: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    Simple built-in null: redraw the same number of values log-uniform on the
    observed global range. Preserve count only (event structure optional).
    """
    arr = np.asarray(values, dtype=float)
    lo, hi = float(arr.min()), float(arr.max())
    if lo <= 0 or hi <= 0:
        raise ValueError("Observed values must be positive for log-uniform null")
    if math.isclose(lo, hi):
        # Degenerate range: jitter slightly so MC is still defined
        hi = lo * (1.0 + 1e-6)
    log_lo, log_hi = math.log(lo), math.log(hi)
    n = len(arr)
    draws = np.exp(rng.uniform(log_lo, log_hi, size=(n_mc, n)))
    # Vectorized score
    # for each draw row, mean_i exp(-min_r |log(x/r)|^2 / 2sig^2)
    log_nodes = np.log(nodes)
    # draws: (n_mc, n); log_nodes: (k,)
    log_x = np.log(draws)[..., None]  # (n_mc, n, 1)
    d = np.min(np.abs(log_x - log_nodes), axis=-1)  # (n_mc, n)
    s = np.exp(-(d * d) / (2.0 * sigma * sigma))
    return s.mean(axis=1)


def empirical_pvalue(observed: float, null_scores: np.ndarray) -> float:
    # Upper-tail: fraction of null scores >= observed (with +1 continuity)
    return float((np.sum(null_scores >= observed) + 1.0) / (len(null_scores) + 1.0))


def benjamini_hochberg(p_values: Sequence[float]) -> List[float]:
    """Return BH-adjusted q-values aligned with input order."""
    m = len(p_values)
    if m == 0:
        return []
    order = np.argsort(p_values)
    ranked = np.asarray(p_values, dtype=float)[order]
    q = np.empty(m, dtype=float)
    prev = 1.0
    for i in range(m - 1, -1, -1):
        rank = i + 1
        val = ranked[i] * m / rank
        prev = min(prev, val)
        q[i] = prev
    out = np.empty(m, dtype=float)
    out[order] = np.clip(q, 0.0, 1.0)
    return out.tolist()


# ---------------------------------------------------------------------------
# Leave-one-event-out stability
# ---------------------------------------------------------------------------

def leave_one_event_out(
    pairs: Sequence[Tuple[str, float]],
    nodes: np.ndarray,
    sigma: float,
) -> Tuple[float, float, bool]:
    by_event: Dict[str, List[float]] = {}
    for eid, x in pairs:
        by_event.setdefault(eid, []).append(x)
    if len(by_event) <= 1:
        s = score([x for _, x in pairs], nodes, sigma)
        return s, s, True
    scores = []
    for held in by_event:
        kept = [x for eid, x in pairs if eid != held]
        scores.append(score(kept, nodes, sigma))
    smin, smax = float(min(scores)), float(max(scores))
    # "Driven by one event" if dropping some single event collapses the score
    # relative to the full-sample score by a large fraction.
    full = score([x for _, x in pairs], nodes, sigma)
    driven = (full - smin) > 0.5 * full if full > 0 else True
    return smin, smax, driven


# ---------------------------------------------------------------------------
# Train / test
# ---------------------------------------------------------------------------

def filter_split(df: pd.DataFrame, split: Optional[str]) -> pd.DataFrame:
    if split is None or split == "all":
        return df
    out = df[df["split"].str.lower() == split.lower()].copy()
    if out.empty:
        raise ValueError(f"No rows with split={split!r}")
    return out


def analyze(
    df: pd.DataFrame,
    families: Sequence[NodeFamily],
    observable: str,
    sigma: float,
    n_mc: int,
    rng: np.random.Generator,
) -> Tuple[List[ScoreResult], List[Tuple[str, float]]]:
    pairs = build_observables(df, observable)
    values = [x for _, x in pairs]
    results: List[ScoreResult] = []
    raw_p: List[float] = []
    tmp = []
    for fam in families:
        s = score(values, fam.nodes, sigma)
        null = log_uniform_null_scores(values, fam.nodes, sigma, n_mc, rng)
        p = empirical_pvalue(s, null)
        loo_min, loo_max, driven = leave_one_event_out(pairs, fam.nodes, sigma)
        tmp.append((fam, s, p, loo_min, loo_max, driven, len(values)))
        raw_p.append(p)
    qvals = benjamini_hochberg(raw_p)
    for (fam, s, p, loo_min, loo_max, driven, n_obs), q in zip(tmp, qvals):
        results.append(
            ScoreResult(
                family=fam.name,
                hypothesis=fam.hypothesis,
                score=s,
                n_obs=n_obs,
                p_value=p,
                q_value=q,
                loo_min_score=loo_min,
                loo_max_score=loo_max,
                loo_driven_by_one=driven,
            )
        )
    results.sort(key=lambda r: (-r.score, r.p_value, r.family))
    return results, pairs


def format_table(results: Sequence[ScoreResult]) -> str:
    headers = [
        "family",
        "hypothesis",
        "score",
        "n",
        "p",
        "q_BH",
        "loo_min",
        "loo_max",
        "driven_by_one",
    ]
    rows = [headers]
    for r in results:
        rows.append(
            [
                r.family,
                r.hypothesis,
                f"{r.score:.6f}",
                str(r.n_obs),
                f"{r.p_value:.4g}",
                f"{r.q_value:.4g}",
                f"{r.loo_min_score:.6f}",
                f"{r.loo_max_score:.6f}",
                "yes" if r.loo_driven_by_one else "no",
            ]
        )
    widths = [max(len(row[i]) for row in rows) for i in range(len(headers))]
    lines = []
    for i, row in enumerate(rows):
        line = "  ".join(cell.ljust(widths[j]) for j, cell in enumerate(row))
        lines.append(line)
        if i == 0:
            lines.append("  ".join("-" * w for w in widths))
    return "\n".join(lines)


def interpret(results: Sequence[ScoreResult], alpha: float = 0.05) -> str:
    lines = []
    supported = [r for r in results if r.q_value <= alpha and not r.loo_driven_by_one]
    if not supported:
        lines.append(
            "Interpretation: no node family exceeds the log-uniform null after "
            f"BH-FDR correction at q<={alpha} with leave-one-event-out stability. "
            "Primary H0 is not rejected under this null."
        )
    else:
        names = ", ".join(r.family for r in supported)
        lines.append(
            f"Interpretation: families surviving q<={alpha} and LOO stability: {names}. "
            "Treat as provisional under the simple log-uniform null only; "
            "a GR-informed null is required before scientific claims."
        )
    primes = [r for r in results if r.hypothesis == "prime"]
    controls = [r for r in results if r.hypothesis in {"control", "random"}]
    if primes and controls:
        best_p = max(primes, key=lambda r: r.score)
        best_c = max(controls, key=lambda r: r.score)
        if best_p.score > best_c.score and best_p.q_value <= alpha:
            lines.append(
                f"Secondary: prime family {best_p.family!r} outscores controls "
                f"({best_p.score:.4f} > {best_c.score:.4f}) after FDR."
            )
        else:
            lines.append(
                "Secondary: prime-indexed family does not uniquely outperform "
                "control families under the current null and corrections."
            )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="HB Experiment 01: cross-event ringdown spectral selection test"
    )
    p.add_argument("--csv", type=Path, required=True, help="Path to qnm_events.csv")
    p.add_argument("--nodes", type=Path, required=True, help="Path to nodes.json")
    p.add_argument("--mc", type=int, default=50000, help="Monte Carlo null draws")
    p.add_argument(
        "--split",
        type=str,
        default="test",
        choices=["train", "test", "all"],
        help="Which predefined split to analyze (default: test)",
    )
    p.add_argument(
        "--observable",
        type=str,
        default=None,
        help="Override observable from nodes.json",
    )
    p.add_argument("--sigma", type=float, default=None, help="Override sigma")
    p.add_argument("--seed", type=int, default=42, help="RNG seed")
    p.add_argument(
        "--json-out",
        type=Path,
        default=None,
        help="Optional path to write machine-readable results",
    )
    return p.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    rng = np.random.default_rng(args.seed)
    families, sigma_file, observable_file, meta = load_nodes(args.nodes, rng)
    sigma = float(args.sigma) if args.sigma is not None else float(sigma_file)
    observable = args.observable or observable_file
    df = filter_split(load_events(args.csv), args.split)

    print("HB Ringdown Experiment 01")
    print(f"  csv         : {args.csv}")
    print(f"  nodes       : {args.nodes}")
    print(f"  split       : {args.split}")
    print(f"  observable  : {observable}")
    print(f"  sigma       : {sigma}")
    print(f"  mc          : {args.mc}")
    print(f"  events      : {sorted(df['event_id'].unique())}")
    if meta:
        print(f"  nodes meta  : {meta}")
    print()

    results, pairs = analyze(df, families, observable, sigma, args.mc, rng)
    values = [x for _, x in pairs]
    print(f"Built {len(values)} dimensionless observations "
          f"across {len({e for e, _ in pairs})} events")
    print(f"Value range: [{min(values):.6g}, {max(values):.6g}]")
    print()
    print(format_table(results))
    print()
    print(interpret(results))
    print()
    print(
        "Notes: empirical p-values use a log-uniform null (starting point). "
        "For publication, replace with a GR-informed null from Kerr QNM "
        "predictions, mass/spin uncertainty, detector noise, and mode selection. "
        "Do not retune sigma or node definitions after viewing held-out results."
    )

    if args.json_out:
        payload = {
            "split": args.split,
            "observable": observable,
            "sigma": sigma,
            "mc": args.mc,
            "seed": args.seed,
            "n_obs": len(values),
            "events": sorted({e for e, _ in pairs}),
            "results": [r.__dict__ for r in results],
        }
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(payload, indent=2))
        print(f"\nWrote {args.json_out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
