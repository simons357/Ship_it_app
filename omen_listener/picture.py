"""OMEN decision window.

The window opens only when listeners have a real track that is coming toward
the protected point. It then says where the contact is and how many seconds
are left to decide to get inside.

The clock is conservative. Bearing error becomes a circle, the circle becomes
seconds, and those seconds are subtracted before the number is shown. This is
a shelter clock. It is not a cue for a weapon, a jammer, or an intercept.
"""

from __future__ import annotations

import math
from typing import Any

from omen_listener.detect import MIN_SCORE
from omen_listener.geo import (
    ang_diff_deg,
    compass_deg,
    intersect_bearings,
    to_geo,
    to_local,
    where_text,
)

# Same knobs are duplicated in portable/omen_listener.js.
BIN_S = 1.0
MIN_CROSS = 0.20
MIN_SPEED_M_S = 8.0
MAX_SPEED_M_S = 90.0
MIN_PATH_M = 40.0
MIN_SPAN_S = 1.5
MAX_SEGMENT_HEADING_DEG = 40.0
DEFAULT_LEAD_S = 30.0
DEFAULT_WATCH_RADIUS_M = 1000.0
DEFAULT_STALE_AFTER_S = 8.0
DEFAULT_HOLD_S = 120.0
DEFAULT_MAX_EXTRAP_S = 45.0
MAX_RANGE_M = 20_000.0
MAX_OPEN_UNCERTAINTY_M = 800.0
OVERHEAD_M = 150.0
EXTRAP_GROWTH_M_PER_S = 5.0
FUTURE_SKEW_S = 5.0
MOVE_WITHIN_S = 180.0
APPROX_WHEN_M = 150.0

DEFAULT_SIGMA_DEG = {
    "treetop": 3.0,
    "phone": 8.0,
    "wearable": 12.0,
}

SHELTER_WORDS = (
    "engage",
    "intercept",
    "jam",
    "weapon",
    "shoot",
    "strike",
    "neutralize",
)


def _sigma_deg(obs: dict[str, Any]) -> float:
    if obs.get("azimuth_sigma_deg") is not None:
        return float(obs["azimuth_sigma_deg"])
    return DEFAULT_SIGMA_DEG.get(str(obs.get("kind") or ""), 8.0)


def _recent(observations: list[dict[str, Any]], now: float, hold_s: float) -> list[dict[str, Any]]:
    kept = []
    for obs in observations:
        t = float(obs["t"])
        if now - hold_s <= t <= now + FUTURE_SKEW_S:
            kept.append(obs)
    kept.sort(key=lambda item: (float(item["t"]), str(item["node_id"])))
    return kept


def _fixes(
    observations: list[dict[str, Any]],
    origin_lat: float,
    origin_lon: float,
) -> list[dict[str, Any]]:
    groups: dict[int, list[dict[str, Any]]] = {}
    for obs in observations:
        if obs.get("azimuth_deg") is None or float(obs.get("score", 0.0)) < MIN_SCORE:
            continue
        key = math.floor(float(obs["t"]) / BIN_S)
        groups.setdefault(key, []).append(obs)
    fixes = []
    for key in sorted(groups):
        latest: dict[str, dict[str, Any]] = {}
        for obs in groups[key]:
            prev = latest.get(obs["node_id"])
            if prev is None or float(obs["t"]) >= float(prev["t"]):
                latest[obs["node_id"]] = obs
        nodes = [latest[node_id] for node_id in sorted(latest)]
        if len(nodes) < 2:
            continue
        weighted_e = 0.0
        weighted_n = 0.0
        weighted_u = 0.0
        weight_sum = 0.0
        times = []
        for i, left in enumerate(nodes):
            left_xy = to_local(left["lat"], left["lon"], origin_lat, origin_lon)
            for right in nodes[i + 1 :]:
                right_xy = to_local(right["lat"], right["lon"], origin_lat, origin_lon)
                hit = intersect_bearings(
                    left_xy,
                    float(left["azimuth_deg"]),
                    right_xy,
                    float(right["azimuth_deg"]),
                    MIN_CROSS,
                    MAX_RANGE_M,
                )
                if hit is None:
                    continue
                east, north, sin_cross, range_a, range_b = hit
                sigma = math.radians(max(_sigma_deg(left), _sigma_deg(right)))
                uncertainty = (sigma * max(range_a, range_b)) / max(sin_cross, MIN_CROSS)
                uncertainty = max(20.0, uncertainty)
                weight = sin_cross
                weighted_e += east * weight
                weighted_n += north * weight
                weighted_u += uncertainty * weight
                weight_sum += weight
                times.append(0.5 * (float(left["t"]) + float(right["t"])))
        if weight_sum <= 0.0:
            continue
        fixes.append(
            {
                "t": sum(times) / len(times),
                "east_m": weighted_e / weight_sum,
                "north_m": weighted_n / weight_sum,
                "uncertainty_m": weighted_u / weight_sum,
            }
        )
    return fixes


def _trajectory(fixes: list[dict[str, Any]]) -> dict[str, Any] | None:
    usable = [fix for fix in fixes if fix["uncertainty_m"] <= MAX_OPEN_UNCERTAINTY_M]
    if len(usable) < 2:
        return None
    start = usable[0]
    end = usable[-1]
    dt = end["t"] - start["t"]
    if dt < MIN_SPAN_S:
        return None
    de = end["east_m"] - start["east_m"]
    dn = end["north_m"] - start["north_m"]
    dist = math.hypot(de, dn)
    if dist < MIN_PATH_M:
        return None
    speed = dist / dt
    if speed < MIN_SPEED_M_S or speed > MAX_SPEED_M_S:
        return None
    heading = compass_deg(de, dn)
    for left, right in zip(usable, usable[1:]):
        seg_dt = right["t"] - left["t"]
        if seg_dt < 0.4:
            continue
        seg_de = right["east_m"] - left["east_m"]
        seg_dn = right["north_m"] - left["north_m"]
        if math.hypot(seg_de, seg_dn) < 10.0:
            continue
        if ang_diff_deg(compass_deg(seg_de, seg_dn), heading) > MAX_SEGMENT_HEADING_DEG:
            return None
    radians = math.radians(heading)
    return {
        "t": end["t"],
        "east_m": end["east_m"],
        "north_m": end["north_m"],
        "vx": speed * math.sin(radians),
        "vy": speed * math.cos(radians),
        "speed_m_s": speed,
        "heading_deg": heading,
        "uncertainty_m": end["uncertainty_m"],
        "fixes": usable,
    }


def _guidance(reason: str, urgency: str, decision_seconds: int | None, where: str) -> str:
    if reason == "trajectory" and urgency == "watch" and decision_seconds is not None:
        text = (
            f"You have {decision_seconds}s to decide. The contact is {where}. "
            "Stay ready to go inside, away from windows."
        )
    elif reason == "trajectory" and urgency == "move" and decision_seconds is not None:
        text = (
            f"You have {decision_seconds}s to decide. The contact is {where}. "
            "Move inside, away from windows."
        )
    elif reason == "trajectory" and urgency == "shelter_now":
        text = (
            f"Decision time is up. The contact is {where}. "
            "Shelter in place, away from windows."
        )
    elif reason == "receding":
        text = "The contact is moving away. The decision window is closed. Keep listening."
    elif reason == "wide_miss":
        text = (
            "A track is passing wide of this point. The decision window stays closed. "
            "You can still see it."
        )
    elif reason == "weak_geometry":
        if where.startswith("heard"):
            text = (
                "Listeners hear a rotor-like sound, but the lines do not place it "
                "well enough to time a decision. You can see who heard it."
            )
        else:
            text = (
                f"The contact is {where}, but the circle is too large to time a decision. "
                "The window stays closed."
            )
    elif reason == "no_bearing":
        text = (
            "Rotor-like sound on a listener, with no direction yet. "
            "You can see which listener heard it. The decision window stays closed."
        )
    elif reason == "no_trajectory":
        text = (
            "Rotor-like sound, no track yet. You can see the cue. "
            "The decision window stays closed until the contact is clearly moving."
        )
    elif reason == "no_contact":
        text = "Listening. No rotor cue yet."
    elif reason == "not_listening":
        text = "Listener is idle. A wearable listen message opens it."
    else:
        text = "Listening."
    lowered = text.lower()
    for banned in SHELTER_WORDS:
        if banned in lowered:
            raise RuntimeError(f"guidance drifted into non-shelter language: {banned}")
    return text


def _point(east: float, north: float, origin_lat: float, origin_lon: float) -> dict[str, float]:
    lat, lon = to_geo(east, north, origin_lat, origin_lon)
    return {
        "lat": lat,
        "lon": lon,
        "east_m": east,
        "north_m": north,
    }


def build_picture(state: dict[str, Any]) -> dict[str, Any]:
    """Build the overlay document from portable listener state."""
    if "protected" not in state or "now" not in state:
        raise ValueError("state needs protected and now")
    origin_lat = float(state["protected"]["lat"])
    origin_lon = float(state["protected"]["lon"])
    now = float(state["now"])
    lead_s = float(state.get("lead_s", DEFAULT_LEAD_S))
    watch_radius_m = float(state.get("watch_radius_m", DEFAULT_WATCH_RADIUS_M))
    hold_s = float(state.get("hold_s", DEFAULT_HOLD_S))
    stale_after_s = float(state.get("stale_after_s", DEFAULT_STALE_AFTER_S))
    max_extrap_s = float(state.get("max_extrap_s", DEFAULT_MAX_EXTRAP_S))
    listening = bool(state.get("listening", False))
    observations = list(state.get("observations") or [])
    recent = _recent(observations, now, hold_s)

    listeners = []
    latest_by_node: dict[str, dict[str, Any]] = {}
    for obs in recent:
        prev = latest_by_node.get(obs["node_id"])
        if prev is None or float(obs["t"]) >= float(prev["t"]):
            latest_by_node[obs["node_id"]] = obs
    for node_id in sorted(latest_by_node):
        obs = latest_by_node[node_id]
        east, north = to_local(float(obs["lat"]), float(obs["lon"]), origin_lat, origin_lon)
        entry = {
            "node_id": node_id,
            "kind": obs.get("kind") or "phone",
            "lat": float(obs["lat"]),
            "lon": float(obs["lon"]),
            "east_m": east,
            "north_m": north,
            "last_score": float(obs.get("score", 0.0)),
            "last_t": float(obs["t"]),
        }
        if obs.get("alt_m") is not None:
            entry["alt_m"] = float(obs["alt_m"])
        if obs.get("azimuth_deg") is not None:
            entry["azimuth_deg"] = float(obs["azimuth_deg"])
        listeners.append(entry)

    systems = sorted({str(item["kind"]) for item in listeners})
    heard_by = [item["node_id"] for item in listeners if item["last_score"] >= MIN_SCORE]
    newest_t = max((float(obs["t"]) for obs in recent), default=None)
    age = None if newest_t is None else max(0.0, now - newest_t)
    if newest_t is None:
        comms = "local" if listening else "idle"
        stale = False
    elif age is not None and age > stale_after_s:
        comms = "down"
        stale = True
    else:
        comms = "local"
        stale = False

    fixes = _fixes(recent, origin_lat, origin_lon)
    track = _trajectory(fixes)
    placed = fixes[-1] if fixes else None
    reason = "no_contact" if listening else "not_listening"
    open_window = False
    urgency = "none"
    decision_seconds: int | None = None
    time_to_closest: float | None = None
    time_uncertainty: float | None = None
    where = "no contact"
    threat = None
    heading = None
    speed = None
    extrapolated_s = 0.0
    clock_estimated = False
    track_points: list[dict[str, Any]] = []

    azimuth_count = sum(1 for obs in recent if obs.get("azimuth_deg") is not None and float(obs.get("score", 0.0)) >= MIN_SCORE)
    if recent and placed is None and azimuth_count >= 2:
        reason = "weak_geometry"
    elif recent and placed is None and azimuth_count == 1:
        reason = "no_trajectory"
    elif recent and placed is None and azimuth_count == 0:
        reason = "no_bearing"
    elif placed is not None and track is None:
        reason = "no_trajectory" if placed["uncertainty_m"] <= MAX_OPEN_UNCERTAINTY_M else "weak_geometry"

    east = north = None
    uncertainty_m = None
    if track is not None:
        dt = max(0.0, now - track["t"])
        extrapolated_s = min(dt, max_extrap_s)
        clock_estimated = extrapolated_s > 1.0
        east = track["east_m"] + track["vx"] * extrapolated_s
        north = track["north_m"] + track["vy"] * extrapolated_s
        uncertainty_m = track["uncertainty_m"] + EXTRAP_GROWTH_M_PER_S * extrapolated_s
        heading = track["heading_deg"]
        speed = track["speed_m_s"]
        rx = -east
        ry = -north
        vv = track["vx"] ** 2 + track["vy"] ** 2
        t_cpa = (rx * track["vx"] + ry * track["vy"]) / vv
        if t_cpa > 0.5:
            miss = math.hypot(east + track["vx"] * t_cpa, north + track["vy"] * t_cpa)
            eta = t_cpa
            approaching = True
        else:
            miss = math.hypot(east, north)
            eta = 0.0
            approaching = False
        time_to_closest = eta
        time_uncertainty = uncertainty_m / speed if speed else None
        where = where_text(east, north, uncertainty_m > APPROX_WHEN_M)
        threat = _point(east, north, origin_lat, origin_lon)
        threat["uncertainty_m"] = uncertainty_m
        outward = east * track["vx"] + north * track["vy"]
        if uncertainty_m > MAX_OPEN_UNCERTAINTY_M:
            reason = "weak_geometry"
        elif approaching and miss <= watch_radius_m:
            reason = "trajectory"
            open_window = True
            conservative = max(0.0, eta - (time_uncertainty or 0.0))
            if conservative <= lead_s:
                urgency = "shelter_now"
                decision_seconds = 0
            elif conservative <= MOVE_WITHIN_S:
                urgency = "move"
                decision_seconds = int(math.floor(conservative - lead_s))
            else:
                urgency = "watch"
                decision_seconds = int(math.floor(conservative - lead_s))
        elif (not approaching) and miss <= OVERHEAD_M:
            # Already at the protected point and moving off it. The decision
            # to relocate has closed; stay inside.
            reason = "trajectory"
            open_window = True
            urgency = "shelter_now"
            decision_seconds = 0
            time_to_closest = 0.0
        elif (not approaching) and outward > 0.0:
            reason = "receding"
        else:
            reason = "wide_miss"
        for fix in track["fixes"]:
            point = _point(fix["east_m"], fix["north_m"], origin_lat, origin_lon)
            point["t"] = fix["t"]
            point["estimated"] = False
            track_points.append(point)
        if clock_estimated:
            tip = _point(east, north, origin_lat, origin_lon)
            tip["t"] = track["t"] + extrapolated_s
            tip["estimated"] = True
            track_points.append(tip)
    elif placed is not None:
        east = placed["east_m"]
        north = placed["north_m"]
        uncertainty_m = placed["uncertainty_m"]
        where = where_text(east, north, uncertainty_m > APPROX_WHEN_M)
        threat = _point(east, north, origin_lat, origin_lon)
        threat["uncertainty_m"] = uncertainty_m

    if threat is None and recent:
        where = "heard, not placed yet"

    guidance = _guidance(reason, urgency, decision_seconds, where)
    if comms == "down" and (threat is not None or recent):
        comms_note = "No new cue. Showing the last listeners on hand. No server required."
    elif comms == "local" and recent:
        comms_note = "Built from listeners on hand. No server required."
    else:
        comms_note = "No server required."

    layers: list[dict[str, Any]] = [
        {
            "type": "protected",
            "lat": origin_lat,
            "lon": origin_lon,
            "east_m": 0.0,
            "north_m": 0.0,
            "label": state["protected"].get("label", "protected point"),
        }
    ]
    for item in listeners:
        layer = {
            "type": "listener",
            "node_id": item["node_id"],
            "kind": item["kind"],
            "lat": item["lat"],
            "lon": item["lon"],
            "east_m": item["east_m"],
            "north_m": item["north_m"],
        }
        if item.get("azimuth_deg") is not None and threat is None:
            layer_bearing = {
                "type": "bearing",
                "node_id": item["node_id"],
                "east_m": item["east_m"],
                "north_m": item["north_m"],
                "azimuth_deg": item["azimuth_deg"],
                "length_m": 1500.0,
            }
            layers.append(layer_bearing)
        layers.append(layer)
    if track_points:
        layers.append({"type": "track", "points": track_points})
    if threat is not None:
        layers.append(
            {
                "type": "threat",
                "lat": threat["lat"],
                "lon": threat["lon"],
                "east_m": threat["east_m"],
                "north_m": threat["north_m"],
                "uncertainty_m": threat["uncertainty_m"],
            }
        )
    if open_window:
        layers.append(
            {
                "type": "decision",
                "seconds": decision_seconds,
                "urgency": urgency,
            }
        )

    contact = None
    if recent:
        contact = {
            "visible": True,
            "placed": threat is not None,
            "heard_by": heard_by,
            "where": where,
        }
        if threat is not None:
            contact.update(threat)

    return {
        "system": "omen-decision-window",
        "version": 1,
        "community_id": state.get("community_id", ""),
        "alert_id": state.get("alert_id", ""),
        "listening": listening,
        "opened_by": state.get("opened_by"),
        "comms": comms,
        "stale": stale,
        "comms_note": comms_note,
        "generated_at": now,
        "protected": {
            "lat": origin_lat,
            "lon": origin_lon,
            "label": state["protected"].get("label", "protected point"),
        },
        "omen": {
            "open": open_window,
            "reason": reason,
            "urgency": urgency,
            "time_to_closest_s": time_to_closest,
            "time_uncertainty_s": time_uncertainty,
            "decision_seconds": decision_seconds,
            "lead_s": lead_s,
            "where": where,
            "threat": threat,
            "track": track_points,
            "heading_deg": heading,
            "speed_m_s": speed,
            "extrapolated_s": extrapolated_s,
            "clock_estimated": clock_estimated,
            "guidance": guidance,
        },
        "contact": contact,
        "listeners": listeners,
        "systems": systems,
        "layers": layers,
    }
