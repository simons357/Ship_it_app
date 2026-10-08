# Gate D — NS-agent attachment pack (author uploads)

## Named attachments (this drop)

| File | Role |
|---|---|
| `gated_initial_fast.cpp` | Fast C++ initial-sweep driver (portable includes; `.AUTHOR.cpp` is verbatim upload) |
| `NS_ORBIT_R4_SMALL_DATA_2026-09-20.md` | Small-ℓ¹ resource prototype |
| `GATE-D-INITIAL-SWEEP-2026-10-08.json` | Author static sweep JSON (**not** \(B_{I_H}\)) |
| `gated_initial.py` | Python initial-sweep driver |
| `Signed-Gate-Checks.json` | VERIFY PASS outputs |

Also required (already in this folder):

- `Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt`
- `verify_signed_gate.py`

## Commands

```bash
python3 verify_signed_gate.py
python3 gated_initial.py 1 8          # nu=1e-5, cutoff 8H
c++ -O3 -std=c++17 -o gated_initial_fast gated_initial_fast.cpp
./gated_initial_fast 1 8
```

Author JSON status: initial-time only; no complete episode; no \(B_{I_H}\).
Lemma not stamped. (17) not claimed.
