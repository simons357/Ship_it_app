# Signed Gate-B sharp-band packet — locations

**Author uploads are on disk. This pointer is not the packet.**

## Attachment pack

`handoff/gate-d-signed-packet-2026-10-08/`

- `Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt`
- `verify_signed_gate.py`
- `Signed-Gate-Checks.json`
- `gated_initial.py` (author initial-sweep driver)

Initial sweep JSON (`nu=1e-5`, cutoff `8H`): static only — **not** \(B_{I_H}\).

```bash
cd handoff/gate-d-signed-packet-2026-10-08
python3 verify_signed_gate.py
python3 gated_initial.py 1 8
```
