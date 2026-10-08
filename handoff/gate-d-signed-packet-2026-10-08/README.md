# Gate D — NS-agent attachment pack

## This drop (named files)

| File | Role |
|---|---|
| `verify_signed_gate.py` | Exact signed-gate checks |
| `Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt` | Six-box adversary note |
| `Gate-D-Signed-Packet-Execution.zip` | Bundle: Orbit R4, episode balance, Signed-Gate txt, verifier, run brief |
| `GATE-D-INITIAL-SWEEP-2026-10-08.json` | Author static sweep (**not** \(B_{I_H}\)) |

`from-zip/` is the unpack of the ZIP for convenience.

Also present: `gated_initial.py`, `gated_initial_fast.cpp`, `Signed-Gate-Checks.json`, full Orbit/episode notes.

## Commands

```bash
python3 verify_signed_gate.py
# or
unzip -o Gate-D-Signed-Packet-Execution.zip -d from-zip
python3 from-zip/verify_signed_gate.py
```

Initial sweep ≠ episode cost. Lemma not stamped. (17) not claimed.
