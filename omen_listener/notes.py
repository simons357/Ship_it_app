"""Personal field notes for one listener.

A smart note is one line taken from the picture you already have: seconds,
where, and whether the field is locked. Preset notes are the same idea with
no typing. Clicking a note off removes it from this listener. Sent notes ride
along on the bundle you hand to the next listener.
"""

from __future__ import annotations

from typing import Any

PRESETS = {
    "inside": "Inside",
    "hear": "I hear it",
    "quiet": "I don't hear it",
    "clear": "Clear here",
}


def smart_text(picture: dict[str, Any]) -> str:
    omen = picture.get("omen") or {}
    coherence = picture.get("coherence") or {}
    field = str(coherence.get("state") or "quiet")
    if omen.get("open") and omen.get("decision_seconds") is not None:
        return f"{omen['decision_seconds']}s · {omen.get('where') or 'unplaced'} · field {field}"
    where = str(omen.get("where") or "")
    if where and where != "no contact":
        return f"{where} · field {field}"
    return f"field {field}"


def make_field_note(
    *,
    node_id: str,
    t: float,
    text: str,
    preset: str,
    status: str = "sent",
    note_id: str | None = None,
) -> dict[str, Any]:
    compact = " ".join(str(text).split())
    if len(compact) > 160:
        compact = compact[:157] + "..."
    return {
        "type": "omen.field_note",
        "id": note_id or f"{preset}:{node_id}:{float(t):.3f}",
        "node_id": str(node_id),
        "t": float(t),
        "text": compact,
        "preset": preset,
        "status": status,
    }


def smart_field_note(
    picture: dict[str, Any],
    *,
    node_id: str,
    t: float,
    note_id: str | None = None,
) -> dict[str, Any]:
    return make_field_note(
        node_id=node_id,
        t=t,
        text=smart_text(picture),
        preset="smart",
        status="sent",
        note_id=note_id,
    )


def preset_field_note(
    preset: str,
    *,
    node_id: str,
    t: float,
    note_id: str | None = None,
) -> dict[str, Any]:
    if preset not in PRESETS:
        raise ValueError(f"unknown field note preset: {preset}")
    return make_field_note(
        node_id=node_id,
        t=t,
        text=PRESETS[preset],
        preset=preset,
        status="sent",
        note_id=note_id,
    )
