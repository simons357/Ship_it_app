# R2 folder — G3 computed-evidence TSV pair

`M.tsv` and `b_exact.tsv` are transcribed from
`g3_corrected_channel_quotient.json`.

**Status: `COMPUTED_EVIDENCE_ONLY`.** The verifier is **read-only**.
This is not the missing Library JSON
(`87745b3cb585e138b6768ab5b9e330f3f045ff4d4ad82ba6f71f0b6fe86be898`)
and not a canonical locked-r2 identity. No integer kernel, holonomy,
MIN-CYCLE, Q-orbit, or return-time was computed.

| File | Shape | Content |
|---|---|---|
| `g3_corrected_channel_quotient.json` | gate payload | Source paste: 20 Γ rows, 12 (mode, helicity) columns, targets `b=π/2−arg(g_sym)` |
| `M.tsv` | 20×12 integers | Γ rows in that order |
| `b_exact.tsv` | 20 rationals | Exact `b/(2π)` as fractions of a turn |

The six B42 weak-row identities hold on this Γ. That does not promote
the pair to a Library JSON lock. Classical Navier–Stokes remains open.

```bash
python3 scripts/r2_read_only_verifier.py
python3 -m unittest tests.test_r2_lock_tsvs
```
