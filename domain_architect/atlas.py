"""Scientific map: closed shortcuts are first-class, not buried notes.

The Taylor–Green negative result is a closed shortcut:

    Broad spectral state ⇏ pointwise viscous payment of the dangerous term.

Atlas exists so those closed doors are easy to see. An error that
produced this statement did not disappear; it became a map entry.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from .errata import LIVE_TAYLOR_GREEN, WITHDRAWN_TAYLOR_GREEN
from .q4_runs import CLOSED_SHORTCUT
from .schema import SCHEMA_VERSION


@dataclass(frozen=True)
class Shortcut:
    shortcut_id: str
    statement: str
    boxed: str
    status: str
    origin: str
    evidence_role: str
    notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


TAYLOR_GREEN_SHORTCUT = Shortcut(
    shortcut_id="TG-BROAD-NOT-POINTWISE-PAYMENT",
    statement=CLOSED_SHORTCUT,
    boxed=(
        r"\boxed{\text{Broad spectral state}\not\Rightarrow "
        r"\text{pointwise viscous payment of the dangerous term}.}"
    ),
    status="closed_shortcut",
    origin="Q4-1 v1 failed consistency check + Taylor–Green negative result",
    evidence_role=(
        "Closed negative. Not a proof of regularity. Not a reason to "
        "retry the withdrawn 3915/663 fraction as evidence."
    ),
    notes=(
        "Live values: "
        f"r^2={LIVE_TAYLOR_GREEN['r_squared']}, "
        f"T_c/(ν D_s)={LIVE_TAYLOR_GREEN['T_c_over_nu_D_s']}. "
        "Old fraction marked WITHDRAWN."
    ),
)


@dataclass
class ScientificMap:
    schema_version: str = SCHEMA_VERSION
    title: str = "Atlas — closed shortcuts and live claims"
    shortcuts: list[Shortcut] = field(default_factory=lambda: [TAYLOR_GREEN_SHORTCUT])
    live_values: dict[str, Any] = field(default_factory=lambda: dict(LIVE_TAYLOR_GREEN))
    withdrawn_values: dict[str, Any] = field(
        default_factory=lambda: dict(WITHDRAWN_TAYLOR_GREEN)
    )
    ns_solved: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "title": self.title,
            "ns_solved": self.ns_solved,
            "shortcuts": [s.to_dict() for s in self.shortcuts],
            "live_values": self.live_values,
            "withdrawn_values": self.withdrawn_values,
        }

    def prominent_shortcuts(self) -> list[Shortcut]:
        return [s for s in self.shortcuts if s.status == "closed_shortcut"]


def default_atlas() -> ScientificMap:
    return ScientificMap()
