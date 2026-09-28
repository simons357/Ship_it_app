#!/usr/bin/env python3
"""Run the g_{Δ,σ} ↔ g_ordered identity check and emit the 24-channel payload.

Does not run v2. Not a close. NS is not solved.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ns_attacks.channel_coefficient import canonical_24_payload, identity_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results",
    )
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    report = identity_report()
    payload = canonical_24_payload()
    ident_path = args.out_dir / "channel_coefficient_identity.json"
    pay_path = args.out_dir / "canonical_24_channel_payload.json"
    ident_path.write_text(json.dumps(report, indent=2) + "\n")
    pay_path.write_text(json.dumps(payload, indent=2) + "\n")

    print("coefficient identity")
    print(f"  certified {report['n_certified']} heterochiral (Δ,σ) samples")
    print(f"  max phase err          {report['max_phase_err']:.3e}")
    print(f"  max axis spread of μ   {report['max_axis_spread_of_mu']:.3e}")
    print(f"  max g_W recon err      {report['max_gW_recon_err']:.3e}")
    print(f"  max 90-deg rot err     {report['max_rotation_err']:.3e}")
    print(f"  g_W = 0 channels       {report['n_gW_zero_channels']} (k-leg Vandermonde)")
    print(f"  passed                 {report['passed']}")
    print("canonical 24-channel payload")
    print(f"  n_channels             {payload['n_channels']}")
    print(f"  cycle sum              {payload['cycle_sum']}")
    print(f"  wrote {ident_path}")
    print(f"  wrote {pay_path}")
    print("v2 not run")
    if not report["passed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
