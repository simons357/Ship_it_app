# R2 folder — synthetic TSV fixture

`M.tsv` and `b_exact.tsv` live here. They are a **synthetic fixture**,
not a locked Library JSON pair. The verifier is **read-only**.

B42 asked for a comparison against locked

- `M.tsv` — integer 20×12 row matrix
- `b_exact.tsv` — exact rational target phases

Those lock files were not in this repository. Search record:
[`ORIGINAL-SEARCH.md`](ORIGINAL-SEARCH.md). This folder holds a
synthetic pair so the read-only verifier has something to load.

## What is in these files

The committed pair is a **synthetic fixture** built from the B42
integer-row identities and the B40 π/12 weak residues:

| File | Shape | Content |
|---|---|---|
| `M.tsv` | 20×12 integers | Strong rows 0–13 as `I_12` plus two extra integer rows; weak rows 14–19 from the six B42 identities |
| `b_exact.tsv` | 20×1 rationals | Target phases β_γ as fractions of a turn, at certificate `y_A = 0` |

This is **not** a claim that the Library JSON has been opened. Canonical
locked-r2 identity remains unverified. Classical Navier–Stokes remains
open.

`PROVENANCE.json` records hashes and the synthetic-fixture convention.
The verifier reads those files; it does not write them.

## Format

Tab-separated values. Lines starting with `#` are comments. Fractions
are `p/q` in lowest terms. The loader also accepts commas.

```bash
python3 scripts/r2_read_only_verifier.py
python3 -m unittest tests.test_r2_lock_tsvs
```
