#!/usr/bin/env python3
"""Bridge-tuning handoff demo.

Reads a Domain Architect `--tuning-json` export and prints how older
bridge / tuning UIs would wire the dials (P selector, nu, coupling, …).

Honest scope:
  - maps export fields → UI control metaphors
  - does NOT run an optimizer, claim fit quality, or invent physics
  - refuses to treat structural_fixed items as free knobs
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


WIDGET_BY_STATUS = {
    "protocol_selector": "dropdown / mask picker (discrete protocol choice)",
    "free": "slider or numeric field (continuous dial)",
    "structural_fixed": "locked / read-only badge (do not retune casually)",
    "derived": "derived readout (computed, not a primary dial)",
}

# Older bridge-app metaphors Jonathan used when tuning by hand.
LEGACY_UI_ALIASES = {
    "P": "Selector / mask control (baseline must include P=I)",
    "H_g (=4πG)": "Coupling gain dial",
    "rho / S": "Source / drive amplitude channel",
    "nu": "Primary continuous gain (viscosity dial)",
    "u0 / omega0": "Initial-condition preset picker",
    "F (optional body force)": "External drive on/off + amplitude",
}


def _load(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text())
    if not isinstance(data, dict):
        raise SystemExit(f"Expected object JSON in {path}")
    return data


def render(export: dict[str, Any], source: str) -> str:
    book = export.get("domain_book", "?")
    auto = export.get("auto_assigned")
    controls = export.get("controls") or []
    fixed = export.get("fixed_structure") or []

    lines: list[str] = [
        "Bridge tuning handoff (UI wiring sketch)",
        f"  source: {source}",
        f"  domain_book: {book}",
        f"  auto_assigned: {auto}",
        "",
        "How old bridge UIs would wire dials:",
    ]

    if not controls:
        lines.append("  (no controls in export — nothing to wire)")
    for c in controls:
        name = str(c.get("name"))
        status = str(c.get("status"))
        widget = WIDGET_BY_STATUS.get(status, f"unknown widget for status={status}")
        legacy = LEGACY_UI_ALIASES.get(name, c.get("bridge_app_hint") or "(generic dial)")
        lines.append(f"  • {name} [{status}]")
        lines.append(f"      UI widget:  {widget}")
        lines.append(f"      legacy map: {legacy}")
        lines.append(f"      why:        {c.get('why')}")
        lines.append(f"      intervene:  {c.get('default_intervention')}")

    if fixed:
        lines.append("")
        lines.append("Leave locked (structural / honesty constraints):")
        for item in fixed:
            lines.append(f"  ✕ {item}")

    lines.append("")
    lines.append("Non-claims:")
    lines.append("  - This printout is a handoff sketch, not an optimizer.")
    lines.append("  - P is admissibility / mode permission — not 'prime'.")
    lines.append("  - Do not bake λ_min(Q_N)>-1/2 into classical NS-B.")
    lines.append("  - Canonical SFE remains unresolved; no hybrid synthesis.")
    if export.get("protocol_reminder"):
        lines.append("")
        lines.append(f"Protocol: {export['protocol_reminder']}")
    if export.get("statement"):
        lines.append("")
        lines.append(str(export["statement"]))
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Print how bridge/tuning UIs would wire Domain Architect "
            "tuning-json dials (no optimizer)."
        )
    )
    parser.add_argument(
        "tuning_json",
        type=Path,
        help="path to --tuning-json export (or '-' for stdin)",
    )
    args = parser.parse_args(argv)

    if str(args.tuning_json) == "-":
        export = json.load(sys.stdin)
        source = "stdin"
    else:
        export = _load(args.tuning_json)
        source = str(args.tuning_json)

    print(render(export, source))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
