"""Training / validation / held-out test separation.

If parameters or selectors are optimized on data, the same data must not
be used as confirmatory evidence. The experimental configuration is hashed
before the held-out set is opened.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from typing import Any, Sequence


@dataclass(frozen=True)
class FrozenProtocol:
    config: dict[str, Any]
    protocol_hash: str
    frozen: bool = True


def freeze_protocol(config: dict[str, Any]) -> FrozenProtocol:
    payload = json.dumps(config, sort_keys=True, default=str)
    digest = hashlib.sha256(payload.encode()).hexdigest()
    return FrozenProtocol(config=dict(config), protocol_hash=digest)


@dataclass
class DataSplit:
    development: list[Any]
    validation: list[Any]
    test: list[Any]
    protocol: FrozenProtocol
    opened_test: bool = False

    def open_test(self, expected_hash: str) -> list[Any]:
        if expected_hash != self.protocol.protocol_hash:
            raise ValueError(
                "held-out test refused: protocol hash does not match the freeze"
            )
        self.opened_test = True
        return list(self.test)


def split_sets(
    items: Sequence[Any],
    *,
    fractions: tuple[float, float, float] = (0.5, 0.25, 0.25),
    seed: int = 0,
) -> DataSplit:
    if abs(sum(fractions) - 1.0) > 1e-9:
        raise ValueError("fractions must sum to 1")
    rng_items = list(items)
    # Deterministic shuffle without numpy so the module stays light.
    n = len(rng_items)
    order = list(range(n))
    # simple LCG shuffle
    state = seed & 0xFFFFFFFF
    for i in range(n - 1, 0, -1):
        state = (1664525 * state + 1013904223) & 0xFFFFFFFF
        j = state % (i + 1)
        order[i], order[j] = order[j], order[i]
    shuffled = [rng_items[i] for i in order]
    n_dev = int(round(fractions[0] * n))
    n_val = int(round(fractions[1] * n))
    n_dev = min(n_dev, n)
    n_val = min(n_val, n - n_dev)
    development = shuffled[:n_dev]
    validation = shuffled[n_dev : n_dev + n_val]
    test = shuffled[n_dev + n_val :]
    protocol = freeze_protocol(
        {
            "seed": seed,
            "fractions": list(fractions),
            "n": n,
            "development_ids": list(map(str, development)),
            "validation_ids": list(map(str, validation)),
            "test_ids_hidden_until_open": True,
        }
    )
    return DataSplit(
        development=development,
        validation=validation,
        test=test,
        protocol=protocol,
    )
