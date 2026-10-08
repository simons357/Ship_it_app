# Gate D — NS-agent attachment pack (8 October 2026)

**Individual files for the NS agent. Drop these onto that machine. Do not rebuild from a pointer.**

## Required attachments (evolution unlock)

| # | File | Role |
|---|---|---|
| 1 | `Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt` | Six-box adversary note |
| 2 | `verify_signed_gate.py` | Exact packet construction + checks |
| 3 | `Signed-Gate-Checks.json` | Expected PASS outputs |
| 4 | `gate_d_initial_sweep.py` | Driver for `GATE-D-INITIAL-SWEEP-2026-10-08.json` |
| 5 | `GATE-D-INITIAL-SWEEP-2026-10-08.json` | Static t=0 sweep (**not** \(B_{I_H}\)) |
| 6 | `gate_d_adversarial_run.py` | Galerkin evolution driver for \(I_H\), \(B_{I_H}\) |

Also included (full source text, not excerpts):

- `NS_EPISODE_BALANCE_NOTE_2026-09-20.md` — defines \(D,Q_\Sigma,V,M\) and episode identity
- `NS_ORBIT_R4_SMALL_DATA_2026-09-20.md` — small-\(\ell^1\) \(\int UW\) prototype
- `GATE-D-RUN-BRIEF.txt` — author execution brief
- `SHA256SUMS.txt`

## Verify on the NS machine

```bash
python3 verify_signed_gate.py
# expect status PASS; writes/matches Signed-Gate-Checks.json

python3 gate_d_initial_sweep.py --n 1 2 3 4
# writes GATE-D-INITIAL-SWEEP-2026-10-08.json
# This is NOT B_IH. Do not score it as episode cost.

python3 gate_d_adversarial_run.py --n 1
# evolution: D_H(0), D_H'(0), I_H, B_IH, resource spends
```

## Hard rules

- Use the six-box Signed-Gate packet only. **No Gaussian substitute.**
- Initial sweep ≠ episode measurement.
- Lemma not stamped until real \(B_{I_H}\) family data exist and are scored.
- (17) not claimed.

## Artifact mirror

Identical copies of the three signed-gate files + both drivers also live under
`/opt/cursor/artifacts/gate-d-ns-attachments/` in the producing cloud agent.
