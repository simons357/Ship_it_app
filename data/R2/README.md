# R2 folder — lock TSV pair

`M.tsv` and `b_exact.tsv` live here.

B42 asked for a comparison against locked

- `M.tsv` — integer 20×12 row matrix
- `b_exact.tsv` — exact rational target phases

Those files were not in this repository, not on any checked branch, and
not in the hashed Library JSON
(`87745b3cb585e138b6768ab5b9e330f3f045ff4d4ad82ba6f71f0b6fe86be898`).
This folder is the R2 home for the pair.

## What is in these files

The committed pair is **reconstructed** from the B42 integer-row
identities and the B40 π/12 weak residues so the verifier has something
to load:

| File | Shape | Content |
|---|---|---|
| `M.tsv` | 20×12 integers | Strong rows 0–13 as `I_12` plus two extra integer rows; weak rows 14–19 from the six B42 identities |
| `b_exact.tsv` | 20×1 rationals | Target phases β_γ as fractions of a turn, at certificate `y_A = 0` |

This is **not** a claim that the Library JSON has been opened. Canonical
locked-r2 identity remains unverified. Classical Navier–Stokes remains
open.

If the original lock pair exists, replace both TSV files in this folder
and re-run the writer/tests. `PROVENANCE.json` records hashes and the
reconstruction convention.

## Format

Tab-separated values. Lines starting with `#` are comments. Fractions
are `p/q` in lowest terms. The loader also accepts commas.

```bash
python3 scripts/r2_lock_tsvs.py
python3 -m unittest tests.test_r2_lock_tsvs
```
