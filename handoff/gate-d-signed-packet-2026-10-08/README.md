# Gate D — Signed packet execution pack

## Named attachments

| File | Role |
|---|---|
| `verify_signed_gate.py` | Exact six-box construction + checks |
| `Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt` | Adversary note |
| `Gate-D-Signed-Packet-Execution.zip` | Bundle (Orbit R4, episode balance, signed-gate txt, verify, run brief) |
| `GATE-D-INITIAL-SWEEP-2026-10-08.json` | Author static sweep (**not** \(B_{I_H}\)) |

Also: `Signed-Gate-Checks.json` (from `python3 verify_signed_gate.py`), `gated_initial.py`, `gated_initial_fast.cpp`.

```bash
python3 verify_signed_gate.py   # PASS
python3 gated_initial.py 1 8    # static only
```

Lemma not stamped. (17) not claimed.
