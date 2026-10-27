"""Python mirror of LISTENER contracts for the hub and tests."""

from __future__ import annotations

from typing import Any

FAILURE_SCOUT_LOST = "Scout connection lost. Still recording — we'll sync when you're back."
FAILURE_MIC_DENIED = "This phone needs the microphone to keep the original. Your session is still here."
COH_INSUFFICIENT = {"display": "—", "status": "INSUFFICIENT FIELD DATA", "computed": False}


def coarse_location(lat: float, lon: float) -> dict[str, Any] | None:
    try:
        lat_f = float(lat)
        lon_f = float(lon)
    except (TypeError, ValueError):
        return None
    if lat_f != lat_f or lon_f != lon_f:  # NaN
        return None
    return {
        "lat": round(lat_f * 10) / 10.0,
        "lon": round(lon_f * 10) / 10.0,
        "precision": "coarse",
    }


def process_signal(*, probable_human_speech: bool = False, label: str | None = None) -> dict[str, Any]:
    if probable_human_speech:
        return {
            "createEncounter": False,
            "contribute": False,
            "kind": "probable_human_excluded",
            "internalLabel": "probable-human-exclusion",
            "transcript": None,
            "speakerId": None,
            "candidateSpecies": None,
        }
    words = (label or "").strip() or "UNKNOWN"
    return {
        "createEncounter": True,
        "contribute": "opt-in-after-confirm",
        "kind": "unknown",
        "internalLabel": "unknown-biological-candidate",
        "transcript": None,
        "speakerId": None,
        "candidateSpecies": None,
        "label": words,
    }


def first_sound_decision(user_words: str = "") -> dict[str, Any]:
    """Rain or any first listen: UNKNOWN or the user's words. Never a species."""
    return process_signal(probable_human_speech=False, label=user_words)


def can_contribute(encounter: dict[str, Any] | None) -> dict[str, Any]:
    if not encounter:
        return {"ok": False, "reason": "No signal selected."}
    if encounter.get("kind") == "probable_human_excluded" or encounter.get("excluded"):
        return {"ok": False, "reason": "Probable human speech stays off the wildlife library."}
    if encounter.get("humanSpeechGate") != "excluded":
        return {"ok": False, "reason": "Confirm this is not human speech before sending it to the library."}
    return {"ok": True}


def coherence_from_field(nodes: list[dict[str, Any]], window_ms: float = 0, measured=None) -> dict[str, Any]:
    nearby = [n for n in nodes if n.get("nearby") and n.get("synchronized")]
    if len(nearby) < 2 or window_ms <= 0 or measured is None:
        return dict(COH_INSUFFICIENT)
    return {"display": str(measured), "status": "MEASURED", "computed": True, "value": measured}
