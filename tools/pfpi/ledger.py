"""Load and filter DA ledger entries."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.pfpi.paths import LEDGER_JSON


def load_ledger(path: Path = LEDGER_JSON) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def filter_ledger(
    *,
    status: str | None = None,
    path: Path = LEDGER_JSON,
) -> list[dict[str, Any]]:
    data = load_ledger(path)
    entries = data.get("entries", [])
    if status:
        entries = [e for e in entries if e.get("status") == status.upper()]
    return entries


def ledger_summary(path: Path = LEDGER_JSON) -> dict[str, int]:
    data = load_ledger(path)
    return dict(data.get("summary", {}))
