"""Neighborhood-scale geometry for the listener.

Flat earth, meters east and north of the protected point. Good for a few
kilometers — a block, a tree line, a small city district. Not a survey.
"""

from __future__ import annotations

import math

M_PER_DEG_LAT = 111_320.0

COMPASS_8 = (
    "north",
    "northeast",
    "east",
    "southeast",
    "south",
    "southwest",
    "west",
    "northwest",
)


def meters_per_deg_lon(lat_deg: float) -> float:
    return M_PER_DEG_LAT * math.cos(math.radians(lat_deg))


def to_local(
    lat: float,
    lon: float,
    origin_lat: float,
    origin_lon: float,
) -> tuple[float, float]:
    """Return (east_m, north_m) relative to the origin."""
    east = (lon - origin_lon) * meters_per_deg_lon(origin_lat)
    north = (lat - origin_lat) * M_PER_DEG_LAT
    return east, north


def to_geo(
    east_m: float,
    north_m: float,
    origin_lat: float,
    origin_lon: float,
) -> tuple[float, float]:
    lat = origin_lat + north_m / M_PER_DEG_LAT
    lon = origin_lon + east_m / meters_per_deg_lon(origin_lat)
    return lat, lon


def compass_deg(east_m: float, north_m: float) -> float:
    """Degrees clockwise from north."""
    return math.degrees(math.atan2(east_m, north_m)) % 360.0


def direction(azimuth_deg: float) -> tuple[float, float]:
    """Unit (east, north) for a compass azimuth."""
    radians = math.radians(azimuth_deg)
    return math.sin(radians), math.cos(radians)


def ang_diff_deg(a: float, b: float) -> float:
    return abs((a - b + 180.0) % 360.0 - 180.0)


def compass_name(azimuth_deg: float) -> str:
    index = int((azimuth_deg + 22.5) // 45.0) % 8
    return COMPASS_8[index]


def where_text(east_m: float, north_m: float, approximate: bool) -> str:
    dist = math.hypot(east_m, north_m)
    if dist < 15.0:
        phrase = "at the protected point"
    else:
        if dist >= 1000.0:
            amount = f"{dist / 1000.0:.1f} km"
        else:
            amount = f"{int(round(dist))} m"
        phrase = f"{amount} {compass_name(compass_deg(east_m, north_m))} of the protected point"
    if approximate and dist >= 15.0:
        return f"about {phrase}"
    return phrase


def intersect_bearings(
    origin_a: tuple[float, float],
    azimuth_a: float,
    origin_b: tuple[float, float],
    azimuth_b: float,
    min_cross: float,
    max_range_m: float,
) -> tuple[float, float, float, float, float] | None:
    """Cross two compass rays.

    Returns (east, north, sin_cross, range_a_m, range_b_m), or None when the
    rays are too shallow, parallel, behind either listener, or past max range.
    """
    dir_a = direction(azimuth_a)
    dir_b = direction(azimuth_b)
    det = dir_a[0] * dir_b[1] - dir_a[1] * dir_b[0]
    sin_cross = abs(det)
    if sin_cross < min_cross:
        return None
    dx = origin_b[0] - origin_a[0]
    dy = origin_b[1] - origin_a[1]
    range_a = (dx * dir_b[1] - dy * dir_b[0]) / det
    range_b = (dx * dir_a[1] - dy * dir_a[0]) / det
    if range_a < 0.0 or range_b < 0.0:
        return None
    if range_a > max_range_m or range_b > max_range_m:
        return None
    east = origin_a[0] + range_a * dir_a[0]
    north = origin_a[1] + range_a * dir_a[1]
    return east, north, sin_cross, range_a, range_b
