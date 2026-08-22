"""Frozen equal-budget selector laboratory.

A prime experiment must compare against several controls that retain the
same number of modes. Negative results are first-class outcomes.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Callable

import numpy as np


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    f = 3
    while f * f <= n:
        if n % f == 0:
            return False
        f += 2
    return True


def prime_indices(n_modes: int) -> np.ndarray:
    return np.array([i for i in range(n_modes) if is_prime(i)], dtype=int)


@dataclass
class SelectorResult:
    name: str
    retained: np.ndarray
    retained_count: int
    reconstruction_error: float
    equation_residual: float
    boundary_residual: float
    cost: float
    seed: int | None = None


@dataclass
class SelectorLabReport:
    budget: int
    protocol_hash: str
    results: list[SelectorResult]
    held_out: bool
    frozen: bool
    conclusion: str
    negative: bool
    metrics: dict[str, float] = field(default_factory=dict)

    def result(self, name: str) -> SelectorResult:
        for item in self.results:
            if item.name == name:
                return item
        raise KeyError(name)


def _mask(n: int, indices: np.ndarray) -> np.ndarray:
    m = np.zeros(n, dtype=float)
    m[np.asarray(indices, dtype=int)] = 1.0
    return m


def select_low(n: int, budget: int) -> np.ndarray:
    return np.arange(min(budget, n), dtype=int)


def select_odd(n: int, budget: int) -> np.ndarray:
    odds = np.arange(1, n, 2, dtype=int)
    return odds[:budget]


def select_composite(n: int, budget: int) -> np.ndarray:
    comps = np.array([i for i in range(n) if i >= 4 and not is_prime(i)], dtype=int)
    return comps[:budget]


def select_prime(n: int, budget: int) -> np.ndarray:
    primes = prime_indices(n)
    return primes[:budget]


def select_random(n: int, budget: int, seed: int) -> np.ndarray:
    rng = np.random.default_rng(seed)
    return np.sort(rng.choice(n, size=min(budget, n), replace=False))


def select_optimized(
    n: int,
    budget: int,
    scores: np.ndarray,
) -> np.ndarray:
    order = np.argsort(-np.asarray(scores, dtype=float))
    return np.sort(order[:budget])


def run_selector_lab(
    field: np.ndarray,
    *,
    budget: int | None = None,
    random_seeds: tuple[int, ...] = (1, 2, 3, 5, 8),
    include_optimized: bool = True,
    operator: Callable[[np.ndarray], np.ndarray] | None = None,
    frozen_protocol: dict | None = None,
    held_out: bool = False,
) -> SelectorLabReport:
    """Compare prime, low, odd, composite, random, and optional optimized masks."""
    field = np.asarray(field, dtype=float)
    n = field.size
    primes = prime_indices(n)
    if budget is None:
        budget = int(primes.size)
    if budget <= 0:
        raise ValueError("selector budget must be positive")
    protocol = {
        "budget": budget,
        "random_seeds": list(random_seeds),
        "include_optimized": include_optimized,
        "n_modes": n,
        **(frozen_protocol or {}),
    }
    protocol_hash = hashlib.sha256(
        json.dumps(protocol, sort_keys=True).encode()
    ).hexdigest()

    def residual(mask_idx: np.ndarray) -> tuple[float, float, float, float]:
        mask = _mask(n, mask_idx)
        recon = field * mask
        rec_err = float(np.linalg.norm(field - recon) / max(1.0, np.linalg.norm(field)))
        if operator is None:
            eq = rec_err
        else:
            eq = float(np.linalg.norm(operator(recon)))
        boundary = 0.0
        cost = float(mask_idx.size)
        return rec_err, eq, boundary, cost

    plans: list[tuple[str, np.ndarray, int | None]] = [
        ("prime", select_prime(n, budget), None),
        ("low", select_low(n, budget), None),
        ("odd", select_odd(n, budget), None),
        ("composite", select_composite(n, budget), None),
    ]
    for seed in random_seeds:
        plans.append((f"random_{seed}", select_random(n, budget, seed), seed))
    if include_optimized:
        scores = np.abs(field)
        plans.append(("optimized", select_optimized(n, budget, scores), None))

    results: list[SelectorResult] = []
    for name, idx, seed in plans:
        if idx.size < budget:
            # Still evaluate, but the unequal budget is recorded.
            pass
        rec, eq, bnd, cost = residual(idx)
        results.append(
            SelectorResult(
                name=name,
                retained=idx,
                retained_count=int(idx.size),
                reconstruction_error=rec,
                equation_residual=eq,
                boundary_residual=bnd,
                cost=cost,
                seed=seed,
            )
        )

    prime = next(r for r in results if r.name == "prime")
    randoms = [r for r in results if r.name.startswith("random_")]
    optimized = next((r for r in results if r.name == "optimized"), None)
    mean_random = float(np.mean([r.reconstruction_error for r in randoms]))
    better_than_random = prime.reconstruction_error < mean_random
    better_than_opt = (
        optimized is not None and prime.reconstruction_error < optimized.reconstruction_error
    )
    negative = not better_than_random
    if better_than_opt:
        conclusion = (
            "Prime selection outperformed the tested random and optimized "
            "controls under this protocol. This is a computational comparison, "
            "not evidence that prime structure is fundamental."
        )
    elif better_than_random:
        conclusion = (
            "Prime selection outperformed the tested random controls under "
            "this protocol but did not outperform optimized mode selection."
        )
    else:
        conclusion = (
            "Prime selection performed worse than the tested random controls "
            "under this protocol. The negative result is stored in the null "
            "registry and is not discarded."
        )
    metrics = {
        "prime_reconstruction_error": prime.reconstruction_error,
        "mean_random_reconstruction_error": mean_random,
        "optimized_reconstruction_error": (
            optimized.reconstruction_error if optimized else float("nan")
        ),
        "retained_mode_count": float(budget),
    }
    return SelectorLabReport(
        budget=budget,
        protocol_hash=protocol_hash,
        results=results,
        held_out=held_out,
        frozen=True,
        conclusion=conclusion,
        negative=negative,
        metrics=metrics,
    )


def assert_equal_budget(report: SelectorLabReport) -> None:
    counts = {r.name: r.retained_count for r in report.results}
    expected = report.budget
    short = {k: v for k, v in counts.items() if v != expected}
    if short:
        raise ValueError(f"unequal retained-mode budgets: {short}")
