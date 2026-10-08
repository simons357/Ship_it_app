# Signed Gate-B sharp-band packet — locations

7 October 2026 (updated 8 October 2026).

**Bytes are in the vault. Do not treat this file as a substitute for the packet.**

---

## Individual attachment pack (for NS agent)

`handoff/gate-d-signed-packet-2026-10-08/`

| File | Present |
|---|---|
| `Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt` | yes |
| `verify_signed_gate.py` | yes |
| `Signed-Gate-Checks.json` | yes |
| `gate_d_initial_sweep.py` | yes |
| `GATE-D-INITIAL-SWEEP-2026-10-08.json` | yes (static; **not** \(B_{I_H}\)) |
| `gate_d_adversarial_run.py` | yes (evolution) |

Also mirrored under `/opt/cursor/artifacts/gate-d-ns-attachments/`.

## Verify

```bash
cd handoff/gate-d-signed-packet-2026-10-08
python3 verify_signed_gate.py   # PASS
```

## STATUS

PACKET FILES ON DISK. POINTER IS NOT THE PACKET.
INITIAL SWEEP ≠ EPISODE COST.
NS NOT SOLVED.
