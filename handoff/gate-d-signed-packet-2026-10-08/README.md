# Gate D — NS-agent attachment pack (author uploads)

**Individual files. Copy these onto the NS machine. Do not rebuild from a pointer.**

## Required attachments

| File | Role |
|---|---|
| `Signed-Gate-B-Sharp-Band-Exponent-2026-10-07.txt` | Six-box adversary note |
| `verify_signed_gate.py` | Exact packet construction + checks |
| `Signed-Gate-Checks.json` | PASS outputs |
| `gated_initial.py` | **Author** initial-sweep driver |

Also present:

| File | Role |
|---|---|
| `GATE-D-INITIAL-SWEEP-2026-10-08.json` | Output of `gated_initial.py` at \(\nu=10^{-5}\), cutoff \(8H\) |
| `gate_d_adversarial_run.py` | Separate evolution driver (for \(I_H\), \(B_{I_H}\)) |
| `NS_EPISODE_BALANCE_NOTE_2026-09-20.md` | Full episode identity (\(D,Q_\Sigma,V,M\)) |
| `NS_ORBIT_R4_SMALL_DATA_2026-09-20.md` | Small-\(\ell^1\) \(\int UW\) prototype |
| `SHA256SUMS.txt` | Checksums |

## Commands

```bash
python3 verify_signed_gate.py
# PASS

# Initial static sweep (NOT B_IH): nu=1e-5, cutoff 8H
python3 -c "import gated_initial as g, json; from pathlib import Path
rows=[g.run(n,1e-5,8) for n in (1,2,3,4)]
Path('GATE-D-INITIAL-SWEEP-2026-10-08.json').write_text(json.dumps({'rows':rows,'computes_B_IH':False},indent=2)+'\n')"

# Or single-n: python3 gated_initial.py <n> <cutmul>
python3 gated_initial.py 1 8
```

## Hard rules

- Six-box Signed-Gate only. **No Gaussian.**
- `GATE-D-INITIAL-SWEEP` is t=0 / local-clock only — **not** \(B_{I_H}\).
- Lemma not stamped until real episode evolution is scored.
- (17) not claimed.

Artifact mirror: `/opt/cursor/artifacts/gate-d-ns-attachments/`.
