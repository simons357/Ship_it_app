"""Offline bundle merge.

Listeners pass these JSON bundles by whatever still works: a local radio,
Bluetooth, a laptop on the same block, or a file carried across the street.
Nothing here opens a socket. A shared community token only stops two
neighborhoods from mixing their packets by accident. It is not authentication.
"""

from __future__ import annotations

import json
from typing import Any


def observation_key(obs: dict[str, Any]) -> str:
    azimuth = obs.get("azimuth_deg")
    azimuth_text = "" if azimuth is None else f"{float(azimuth):.2f}"
    return "|".join(
        (
            str(obs.get("node_id", "")),
            f"{float(obs['t']):.3f}",
            azimuth_text,
            f"{float(obs.get('score', 0.0)):.3f}",
        )
    )


def normalize_observation(raw: dict[str, Any]) -> dict[str, Any]:
    lat = float(raw["lat"])
    lon = float(raw["lon"])
    if not -90.0 <= lat <= 90.0 or not -180.0 <= lon <= 180.0:
        raise ValueError("observation lat/lon out of range")
    score = float(raw["score"])
    if score < 0.0:
        score = 0.0
    elif score > 1.0:
        score = 1.0
    azimuth = raw.get("azimuth_deg")
    sigma = raw.get("azimuth_sigma_deg")
    normalized = {
        "node_id": str(raw["node_id"]),
        "kind": str(raw.get("kind") or "phone"),
        "t": float(raw["t"]),
        "lat": lat,
        "lon": lon,
        "score": score,
        "azimuth_deg": None if azimuth is None else float(azimuth) % 360.0,
        "alert_id": str(raw.get("alert_id") or ""),
        "community_id": str(raw.get("community_id") or ""),
    }
    if raw.get("alt_m") is not None:
        normalized["alt_m"] = float(raw["alt_m"])
    if sigma is not None:
        normalized["azimuth_sigma_deg"] = float(sigma)
    if raw.get("fundamental_hz") is not None:
        normalized["fundamental_hz"] = float(raw["fundamental_hz"])
    return normalized


def make_bundle(
    *,
    community_id: str,
    alert_id: str,
    origin_id: str,
    sent_at: float,
    observations: list[dict[str, Any]],
    hop: int = 0,
    community_token: str | None = None,
    field_notes: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    bundle: dict[str, Any] = {
        "type": "omen.bundle",
        "version": 1,
        "community_id": community_id,
        "alert_id": alert_id,
        "origin_id": origin_id,
        "sent_at": float(sent_at),
        "hop": int(hop),
        "observations": observations,
    }
    if field_notes is not None:
        bundle["field_notes"] = field_notes
    if community_token is not None:
        bundle["community_token"] = community_token
    return bundle


def merge_bundles(
    bundles: list[dict[str, Any]],
    *,
    community_id: str,
    alert_id: str,
    community_token: str | None = None,
) -> list[dict[str, Any]]:
    """Union observations. Same measurement (node, time, score, bearing) collapses."""
    merged: dict[str, dict[str, Any]] = {}
    for bundle in bundles:
        if not isinstance(bundle, dict):
            continue
        if bundle.get("type") not in (None, "omen.bundle"):
            continue
        if bundle.get("community_id") not in (None, "", community_id):
            continue
        bundle_alert = str(bundle.get("alert_id") or "")
        if alert_id and bundle_alert not in ("", alert_id):
            continue
        if community_token is not None and bundle.get("community_token") != community_token:
            continue
        for raw in bundle.get("observations") or []:
            if not isinstance(raw, dict):
                continue
            try:
                obs = normalize_observation(raw)
            except (KeyError, TypeError, ValueError):
                continue
            if obs["community_id"] not in ("", community_id):
                continue
            if alert_id and obs["alert_id"] not in ("", alert_id):
                continue
            obs["community_id"] = community_id
            if alert_id:
                obs["alert_id"] = alert_id
            merged[observation_key(obs)] = obs
    return [merged[key] for key in sorted(merged)]


def bundle_json(bundle: dict[str, Any]) -> str:
    return json.dumps(bundle, sort_keys=True, separators=(",", ":"))
