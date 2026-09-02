"""Archived SFE / UHF / DHFA / HB inventory access.

Live Domain Architect code must not import this module except from
``--archive`` / the desktop Archive pane. It is not part of decompose,
translate, or synthesize.
"""

from __future__ import annotations

from typing import Final

CANONICAL_SFE_STATUS: Final[str] = "archived — not part of Domain Architect v1.0"

HISTORICAL_NOTE: Final[str] = (
    "SFE, UHF, DHFA and the Harmonic Blueprint are archived historical "
    "reference. They are not loaded into the live Domain Architect path."
)
