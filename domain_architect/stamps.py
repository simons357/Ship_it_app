"""F-X2 / relabel: opaque DA-STAMPED becomes typed v5 stamps.

Finish this before Process Console reads a ledger. A leftover
"DA-STAMPED" string is a schema error, not a compliment.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Mapping

from .process_schema import SchemaError, StampRecord, parse_stamp_kind
from .schema import OPAQUE_STAMP_LABELS, SCHEMA_VERSION, StampKind


FX2_ID = "F-X2"
FX2_TITLE = "Relabel opaque DA-STAMPED into typed v5 stamps"


@dataclass(frozen=True)
class RelabelResult:
    original: str
    kind: StampKind | None
    accepted: bool
    reason: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "fix": FX2_ID,
            "schema_version": SCHEMA_VERSION,
            "original": self.original,
            "kind": None if self.kind is None else self.kind.value,
            "accepted": self.accepted,
            "reason": self.reason,
        }


def is_opaque_stamp(raw: str) -> bool:
    token = " ".join(raw.strip().upper().replace("_", "-").split())
    compact = token.replace("-", " ")
    return token in OPAQUE_STAMP_LABELS or compact in {"DA STAMPED", "DA STAMP"}


def relabel_stamp(raw: str, *, intended_kind: str | None = None) -> RelabelResult:
    """Map a legacy stamp token onto a v5 StampKind.

    If the token is opaque (DA-STAMPED) and no intended kind is given,
    the relabel fails. Console must not invent what DA did.
    """
    if is_opaque_stamp(raw):
        if not intended_kind:
            return RelabelResult(
                original=raw,
                kind=None,
                accepted=False,
                reason=(
                    "F-X2 refused opaque DA-STAMPED: say PROVED, "
                    "REPRODUCED, or CONSISTENCY CHECK."
                ),
            )
        kind = parse_stamp_kind(intended_kind)
        return RelabelResult(
            original=raw,
            kind=kind,
            accepted=True,
            reason=f"F-X2 relabeled DA-STAMPED → {kind.value}.",
        )
    try:
        kind = parse_stamp_kind(raw)
    except SchemaError as exc:
        return RelabelResult(original=raw, kind=None, accepted=False, reason=str(exc))
    return RelabelResult(
        original=raw,
        kind=kind,
        accepted=True,
        reason=f"already a v5 stamp kind: {kind.value}",
    )


def relabel_records(
    records: Iterable[Mapping[str, Any]],
) -> list[StampRecord]:
    """Convert a list of {kind, ...} dicts, refusing opaque leftovers."""
    out: list[StampRecord] = []
    for raw in records:
        token = str(raw.get("kind", ""))
        intended = raw.get("intended_kind")
        result = relabel_stamp(token, intended_kind=intended)
        if not result.accepted or result.kind is None:
            raise SchemaError(result.reason)
        out.append(
            StampRecord(
                kind=result.kind,
                statement=str(raw.get("statement", "")),
                status=str(raw.get("status", "recorded")),
                notes=str(raw.get("notes", result.reason)),
            )
        )
    return out


def fx2_complete(stamps: Iterable[StampRecord]) -> bool:
    """F-X2 is finished when every stamp is a typed v5 kind."""
    return all(isinstance(s.kind, StampKind) for s in stamps)
