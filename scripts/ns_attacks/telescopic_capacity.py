"""Telescopic capacity: do not count resets; make the jump nonpositive.

Nearest-center identity. At a fixed physical state,

    W_K = D_s + X(Λ − K)^2
        = Σ_k λ_k (λ_k − K)^2 |v_k|^2.

A chart change K_e → K_{e+1} therefore costs exactly

    ΔW = X[(Λ − K_{e+1})^2 − (Λ − K_e)^2].

Choosing the center nearer to Λ guarantees ΔW ≤ 0. So the
artificial reset cost of center selection can be killed by
design.

That does not solve reset summability. A nearest-shell rule
can switch every time Λ crosses another midpoint. The number
of those switches is governed by how far Λ travels, and

    (log Λ)' = 2/Y (T_c − ν D_s)

is the quantity the Gate is trying to control. Any estimate
of the form

    “few resets because Λ cannot move much”

is circular unless it comes from an independent budget.

Target: do not prove #{epochs} < ∞ or even Σ |ΔK_e| < ∞.
Design a capacity whose chart change is nonpositive or
telescopes against an already-paid physical quantity:

    Q_{e+1}(u) ≤ Q_e(u) + (already paid).

Best case: Q_{e+1}(u) ≤ Q_e(u) at every reset. Then
infinitely many resets are harmless.

Rejected: any proposed reset bound that requires prior
control of Λ's total motion.

Not DA-NS-2. Not a close. NS is not solved.
"""

from __future__ import annotations

import math
from typing import Callable, Dict, Iterable, List, Sequence, Tuple


def W_from_moments(X: float, Y: float, Z: float, K: float) -> dict:
    """Exact identities. X,Y,Z are the seated Stokes moments."""
    if X <= 0.0:
        raise ValueError("X must be positive")
    Lam = Y / X
    Ds = Z - Lam * Y
    W = Ds + X * (Lam - K) ** 2
    W_direct = Z - 2.0 * K * Y + (K ** 2) * X
    return {
        "X": X,
        "Y": Y,
        "Z": Z,
        "Lambda": Lam,
        "D_s": Ds,
        "K": K,
        "W": W,
        "W_expanded": W_direct,
        "identity_holds": abs(W - W_direct) <= 1e-12 * max(1.0, abs(W_direct)),
    }


def W_from_spectrum(
    lambdas: Sequence[float],
    energies: Sequence[float],
    K: float,
) -> dict:
    """W_K = Σ λ (λ − K)^2 e, with e = |v_k|^2, λ = |k|^2."""
    if len(lambdas) != len(energies):
        raise ValueError("spectrum length mismatch")
    X = 0.0
    Y = 0.0
    Z = 0.0
    W = 0.0
    for lam, e in zip(lambdas, energies):
        if e < 0.0:
            raise ValueError("modal energy must be nonnegative")
        X += lam * e
        Y += (lam ** 2) * e
        Z += (lam ** 3) * e
        W += lam * (lam - K) ** 2 * e
    mom = W_from_moments(X, Y, Z, K)
    mom["W_spectral"] = W
    mom["spectral_matches"] = abs(W - mom["W"]) <= 1e-12 * max(1.0, abs(W))
    return mom


def reset_jump(X: float, Lam: float, K_from: float, K_to: float) -> dict:
    dW = X * ((Lam - K_to) ** 2 - (Lam - K_from) ** 2)
    return {
        "X": X,
        "Lambda": Lam,
        "K_from": K_from,
        "K_to": K_to,
        "dW": dW,
        "nonpositive": dW <= 1e-15,
        "formula": "X[((Λ-K_{e+1})^2 - (Λ-K_e)^2)]",
    }


def nearest_center(Lam: float, charts: Sequence[float]) -> float:
    if not charts:
        raise ValueError("empty chart set")
    return min(charts, key=lambda K: (abs(K - Lam), abs(K), K))


def nearest_center_reset(X: float, Lam: float, K_from: float, charts: Sequence[float]) -> dict:
    K_to = nearest_center(Lam, charts)
    jump = reset_jump(X, Lam, K_from, K_to)
    jump["K_to"] = K_to
    jump["nearest"] = True
    jump["design_kills_reset_cost"] = jump["nonpositive"]
    return jump


def midpoint_crossings(path: Sequence[float], charts: Sequence[float]) -> dict:
    """How many nearest-center switches a Λ-path forces.

    This is a diagnostic, not a bound. The count is governed by
    the travel of Λ through the midpoints of the chart set.
    """
    ordered = sorted(set(float(K) for K in charts))
    if len(ordered) < 2:
        return {
            "n_switches": 0,
            "midpoints": [],
            "path_variation": 0.0 if not path else 0.0,
            "circular": True,
            "reason": "one or fewer charts: no midpoint switch is possible",
        }
    mids = [0.5 * (ordered[i] + ordered[i + 1]) for i in range(len(ordered) - 1)]
    switches = 0
    if path:
        prev = nearest_center(path[0], ordered)
        for lam in path[1:]:
            cur = nearest_center(lam, ordered)
            if cur != prev:
                switches += 1
                prev = cur
    var = 0.0
    for a, b in zip(path, path[1:]):
        var += abs(b - a)
    return {
        "n_switches": switches,
        "midpoints": mids,
        "path_variation": var,
        "spacing_min": min(ordered[i + 1] - ordered[i] for i in range(len(ordered) - 1)),
        "circular": True,
        "reason": (
            "the number of nearest-center changes is controlled by how far "
            "Λ travels through spectral scale. (log Λ)' = 2/Y (T_c − ν D_s) "
            "is the Gate quantity. Counting resets from this path is circular."
        ),
    }


CIRCULAR_MARKERS = (
    "total variation of lambda",
    "tv(lambda)",
    "int |lambda'|",
    "int |lam'|",
    "int |t_c - nu d_s|",
    "int |tc - nu ds|",
    "lambda cannot move",
    "lambda stays bounded",
    "few resets because lambda",
    "sup lambda",
    "int d_s / y",
    "int y",
)


def reject_if_circular(proposal: str) -> dict:
    """Any reset estimate that needs prior control of Λ's motion is rejected."""
    text = " ".join(proposal.lower().split())
    hits = [m for m in CIRCULAR_MARKERS if m in text]
    return {
        "proposal": proposal,
        "rejected": bool(hits),
        "hits": hits,
        "rule": (
            "Rejected as circular: a reset estimate that requires prior "
            "control of Λ's total motion. Search for a capacity whose "
            "chart change is nonpositive or telescopes at every reset."
        ),
    }


def telescopic_score(jump: float, paid: float = 0.0, tol: float = 1e-12) -> dict:
    """Q_{e+1} ≤ Q_e + paid. Best case paid = 0."""
    ok = jump <= paid + tol
    return {
        "jump": jump,
        "paid": paid,
        "telescopic": ok,
        "nonpositive_reset": jump <= tol,
        "best_case": jump <= tol,
    }


def candidate_capacities() -> List[dict]:
    """Named designs. Identities, not estimates."""
    return [
        {
            "name": "W_K",
            "formula": "D_s + X(Λ-K)^2 = Σ λ(λ-K)^2 e",
            "reset": "nearest-center ⇒ ΔW ≤ 0",
            "intra_epoch": (
                "K frozen: W' = −2ν Σ λ^2 (λ-K)^2 e + 2 Σ λ(λ-K)^2 τ. "
                "The nonlinear piece is not T_c and is not absorbed."
            ),
            "telescopic_at_reset": True,
            "closes_DA_NS_2": False,
            "note": "kills center-selection reset cost by design; does not bound #epochs",
        },
        {
            "name": "D_s",
            "formula": "Z − Λ Y",
            "reset": "independent of K; ΔD_s = 0 at a chart change",
            "intra_epoch": "D_s' still carries T_c. Not a bound.",
            "telescopic_at_reset": True,
            "closes_DA_NS_2": False,
            "note": "no chart to reset; the frozen-K estimates are gone",
        },
        {
            "name": "epoch-count",
            "formula": "#{e : K_e ≠ K_{e+1}}",
            "reset": "counts midpoint crossings of Λ",
            "intra_epoch": "n/a",
            "telescopic_at_reset": False,
            "closes_DA_NS_2": False,
            "note": "rejected: #epochs < ∞ is the wrong target",
        },
        {
            "name": "sum |ΔK|",
            "formula": "Σ_e |K_{e+1} − K_e|",
            "reset": "controlled by travel of Λ through the chart",
            "intra_epoch": "n/a",
            "telescopic_at_reset": False,
            "closes_DA_NS_2": False,
            "note": "rejected unless the variation is already paid independently",
        },
    ]


def log_lambda_identity() -> dict:
    return {
        "identity": "(log Λ)' = 2/Y (T_c − ν D_s)",
        "also": "Λ' = 2/X (T_c − ν D_s)",
        "status": "EXACT. Seated. Not an estimate.",
        "warning": (
            "this is the Gate quantity. It cannot be used as a hypothesis "
            "to bound the number of chart resets."
        ),
    }


def report() -> dict:
    # Locked §4 triad moments from the centered-drift note: X=10, Y=14, Z=22.
    note = W_from_moments(10.0, 14.0, 22.0, K=1.0)
    # Same moments as the locked §4 triad: X=10, Y=14, Z=22.
    spec = W_from_spectrum([1.0, 1.0, 2.0], [3.0, 3.0, 2.0], K=1.0)
    # Nearest-center: charts {1,2,4}, Λ=7/5=1.4 → nearest is 1.
    jump_good = nearest_center_reset(10.0, 1.4, 2.0, [1.0, 2.0, 4.0])
    jump_away = reset_jump(10.0, 1.4, 1.0, 4.0)
    path = [0.5, 1.2, 1.6, 2.4, 3.1, 3.9, 4.2]
    crossings = midpoint_crossings(path, [1.0, 2.0, 3.0, 4.0])
    proposals = [
        reject_if_circular("few resets because Lambda cannot move much"),
        reject_if_circular("sum |ΔK_e| ≤ C int |Lambda'| dt"),
        reject_if_circular("Q_{e+1}(u) ≤ Q_e(u) at every nearest-center reset"),
        reject_if_circular("nearest-center ΔW ≤ 0, no motion hypothesis"),
    ]
    return {
        "note_triad_W": note,
        "spectral_identity": spec,
        "nearest_center_jump": jump_good,
        "away_from_center_jump": jump_away,
        "midpoint_crossings": crossings,
        "candidates": candidate_capacities(),
        "proposals": proposals,
        "log_lambda": log_lambda_identity(),
        "locks": {
            "center_selection_reset_cost_killed_by_design": jump_good["nonpositive"],
            "reset_summability_not_solved": True,
            "epoch_count_is_the_wrong_target": True,
            "circular_lambda_motion_rejected": True,
            "not_a_close": True,
        },
        "next": (
            "Search for a capacity whose chart change is nonpositive or "
            "telescopes at every center/projector/component reset. "
            "W_K with nearest-center does the jump. The intra-epoch "
            "derivative is still open. DA-NS-2 is not seated."
        ),
    }
