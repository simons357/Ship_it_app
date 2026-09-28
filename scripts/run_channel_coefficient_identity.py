#!/usr/bin/env python3
"""Run the g_{Δ,σ} identities and emit the official k+p+q=0 24-channel payload.

Does not run v2. Not a close. NS is not solved. DA-NS-2 remains open.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from ns_attacks.channel_coefficient import identity_report
from ns_attacks.full_flow import canonical_24_payload_sum0, full_flow_report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "results",
    )
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    pqk = identity_report()
    flow = full_flow_report()
    payload = canonical_24_payload_sum0()

    ident_path = args.out_dir / "channel_coefficient_identity.json"
    flow_path = args.out_dir / "full_flow_identity.json"
    pay_path = args.out_dir / "canonical_24_channel_payload.json"
    ident_path.write_text(json.dumps(pqk, indent=2) + "\n")
    flow_path.write_text(json.dumps(flow, indent=2) + "\n")
    pay_path.write_text(json.dumps(payload, indent=2) + "\n")

    print("p+q=k coefficient identity")
    print(f"  certified {pqk['n_certified']} heterochiral (Δ,σ) samples")
    print(f"  max phase err          {pqk['max_phase_err']:.3e}")
    print(f"  max axis spread of μ   {pqk['max_axis_spread_of_mu']:.3e}")
    print(f"  max g_W recon err      {pqk['max_gW_recon_err']:.3e}")
    print(f"  max 90-deg rot err     {pqk['max_rotation_err']:.3e}")
    print(f"  g_W = 0 channels       {pqk['n_gW_zero_channels']} (k-leg Vandermonde)")
    print(f"  passed                 {pqk['passed']}")
    print("k+p+q=0 full-flow identities (Sprint 01)")
    print(f"  certified              {flow['n_certified']}")
    print(f"  maxima                 { {k: f'{v:.3e}' for k, v in flow['maxima'].items()} }")
    print(f"  max |U_arg|            {flow['max_U_arg_nonvanishing']:.6f}")
    print(f"  conjugation essential  {flow['conjugation_essential']}")
    print(f"  passed                 {flow['passed']}")
    print("canonical 24-channel payload (k+p+q=0)")
    print(f"  n_channels             {payload['n_channels']}")
    print(f"  convention             {payload['convention']}")
    print(f"  wrote {ident_path}")
    print(f"  wrote {flow_path}")
    print(f"  wrote {pay_path}")
    print("DA-NS-2 open; v2 not run")
    if not pqk["passed"] or not flow["passed"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
