# B42 lock inputs (not in this checkout)

The coefficient calculation in B42 used a Library JSON with SHA-256

```
87745b3cb585e138b6768ab5b9e330f3f045ff4d4ad82ba6f71f0b6fe86be898
```

and asked for a comparison against locked

- `M.tsv` — integer 20×12 row matrix
- `b_exact.tsv` — exact rational target phases

None of those files is in this repository. Place them here (or anywhere
under `data/`) if they become available. The runner will hash-match the
JSON and re-check the six integer identities.

Until that comparison is done, the exact leading coefficient is a
statement about the *rationalized* 20-row quotient, not a canonical
locked-r2 identity. The symmetrized coefficient convention is likewise
unverified.

Classical Navier–Stokes remains open.
