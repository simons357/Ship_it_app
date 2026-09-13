"""Shared config loader for platform spine."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

_PKG_DIR = Path(__file__).resolve().parent
REGISTRY_PATH = _PKG_DIR / "product_registry.json"
SPELL_REGISTRY_PATH = _PKG_DIR / "spell_registry.json"


def _load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_registry(path: Path | None = None) -> dict[str, Any]:
    """Load product registry with optional env URL overrides.

    Env overrides (optional):
      PF_FIELD_LOCK_URL, PF_CHATVAULT_URL, PF_NAV42_URL, PF_SHIP_IT_URL
    """
    registry = _load_json(path or REGISTRY_PATH)
    overrides = {
        "field-lock": os.environ.get("PF_FIELD_LOCK_URL"),
        "chatvault": os.environ.get("PF_CHATVAULT_URL"),
        "nav-42": os.environ.get("PF_NAV42_URL"),
        "ship-it": os.environ.get("PF_SHIP_IT_URL"),
    }
    products = registry.get("products", {})
    for product_id, url in overrides.items():
        if url and product_id in products:
            products[product_id].setdefault("urls", {})["canonical"] = url
    return registry


def load_spell_registry(path: Path | None = None) -> dict[str, Any]:
    """Load spell registry mapping spell ids to scripts and tags."""
    return _load_json(path or SPELL_REGISTRY_PATH)


def get_product(registry: dict[str, Any], product_id: str) -> dict[str, Any]:
    """Return one product entry or raise KeyError."""
    try:
        return registry["products"][product_id]
    except KeyError as exc:
        raise KeyError(f"Unknown product: {product_id}") from exc
