"""Canonical URL resolver — one link policy across products."""

from __future__ import annotations

from typing import Any

from packages.shared_core.config import get_product, load_registry

# Statuses that must not be used for cold outreach or embeds
BLOCKED_STATUSES = frozenset({"hollow", "cut", "unknown", "gated"})


def resolve_url(product_id: str, registry: dict[str, Any] | None = None) -> str | None:
    """Return the canonical public URL for a product.

    Policy:
      1. Use urls.canonical when set
      2. For live Replit products, never fall back to hollow hub routes
      3. Return None when no safe URL exists
    """
    reg = registry or load_registry()
    product = get_product(reg, product_id)
    urls = product.get("urls") or {}
    canonical = urls.get("canonical")
    if canonical:
        return canonical

    status = product.get("status")
    if status in BLOCKED_STATUSES:
        return None

    # Last resort: hub route only for non-hollow products
    hub = urls.get("hub")
    if hub and status == "live":
        return hub

    return urls.get("repo")


def link_status(product_id: str, registry: dict[str, Any] | None = None) -> dict[str, Any]:
    """Summarize whether a product link is safe to share."""
    reg = registry or load_registry()
    product = get_product(reg, product_id)
    status = product.get("status", "unknown")
    url = resolve_url(product_id, reg)
    safe_for_outreach = (
        url is not None
        and status not in BLOCKED_STATUSES
        and product.get("keep_cut") != "CUT"
    )
    return {
        "product_id": product_id,
        "name": product.get("name"),
        "status": status,
        "keep_cut": product.get("keep_cut"),
        "url": url,
        "safe_for_outreach": safe_for_outreach,
        "reason": _status_reason(product, url),
    }


def _status_reason(product: dict[str, Any], url: str | None) -> str:
    status = product.get("status")
    if product.get("keep_cut") == "CUT":
        return "Product CUT from catalog — do not promote."
    if status == "hollow":
        return "Hollow public URL — ship MVP or drop from catalog."
    if status == "gated":
        return "Base44 permissions may block strangers — fix publish first."
    if status == "unknown":
        return "Product location unknown — supply URL/repo."
    if url is None:
        return "No canonical URL configured."
    if status == "live":
        return "Live — verify incognito before cold outreach."
    return f"Status: {status}"
