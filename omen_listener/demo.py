"""Synthetic tree-line picture used by the overlay and the tests.

The truth positions are used only to build the bearings a listener would
report. The window then sees bearings, not the answer.
"""

from __future__ import annotations

from typing import Any

from omen_listener.geo import compass_deg, to_geo
from omen_listener.picture import build_picture

COMMUNITY_ID = "north-oak"
ALERT_ID = "alert-tree-line"
ORIGIN = (40.0, -74.0)


def _node(node_id: str, kind: str, east: float, north: float, alt_m: float) -> dict[str, Any]:
    lat, lon = to_geo(east, north, ORIGIN[0], ORIGIN[1])
    return {
        "node_id": node_id,
        "kind": kind,
        "east": east,
        "north": north,
        "lat": lat,
        "lon": lon,
        "alt_m": alt_m,
    }


def _cue(
    node: dict[str, Any],
    t: float,
    threat_east: float,
    threat_north: float,
    *,
    with_azimuth: bool,
) -> dict[str, Any]:
    azimuth = None
    if with_azimuth:
        azimuth = compass_deg(threat_east - node["east"], threat_north - node["north"])
    return {
        "node_id": node["node_id"],
        "kind": node["kind"],
        "t": t,
        "lat": node["lat"],
        "lon": node["lon"],
        "alt_m": node["alt_m"],
        "score": 0.92,
        "azimuth_deg": azimuth,
        "alert_id": ALERT_ID,
        "community_id": COMMUNITY_ID,
    }


def demo_observations() -> list[dict[str, Any]]:
    """Tree line north of a block, plus a phone and a wearable that only hear it."""
    west = _node("treetop-west", "treetop", -500.0, 40.0, 14.0)
    east = _node("treetop-east", "treetop", 500.0, 40.0, 14.0)
    phone = _node("phone-maple", "phone", 0.0, -160.0, 1.5)
    wearable = _node("wearable-1", "wearable", 70.0, -90.0, 1.2)
    first = (0.0, 1600.0)
    second = (0.0, 1500.0)
    observations = [
        _cue(west, 1000.0, *first, with_azimuth=True),
        _cue(east, 1000.0, *first, with_azimuth=True),
        _cue(west, 1005.0, *second, with_azimuth=True),
        _cue(east, 1005.0, *second, with_azimuth=True),
        _cue(phone, 1005.0, *second, with_azimuth=False),
        _cue(wearable, 1005.0, *second, with_azimuth=False),
    ]
    return observations


def demo_state(now: float) -> dict[str, Any]:
    return {
        "version": 1,
        "community_id": COMMUNITY_ID,
        "alert_id": ALERT_ID,
        "protected": {"lat": ORIGIN[0], "lon": ORIGIN[1], "label": "north oak"},
        "lead_s": 30.0,
        "watch_radius_m": 1000.0,
        "now": now,
        "listening": True,
        "opened_by": "wearable",
        "observations": demo_observations(),
    }


def demo_picture(now: float = 1005.0) -> dict[str, Any]:
    return build_picture(demo_state(now))
