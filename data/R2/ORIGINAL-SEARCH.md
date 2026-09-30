# Original lock-data search for PR #144

30 September 2026.
The original lock pair is **not found**. This note records where we
looked. It does not invent the files.

## What we are looking for

| Artifact | Why |
|---|---|
| Library JSON SHA-256 `87745b3cb585e138b6768ab5b9e330f3f045ff4d4ad82ba6f71f0b6fe86be898` | Named in the B42 user note as the file used for “exact matrix-row checks” |
| Locked `M.tsv` | Integer 20×12 row matrix |
| Locked `b_exact.tsv` | Exact rational target phases |

`data/R2/M.tsv` and `data/R2/b_exact.tsv` on this branch are a
**synthetic fixture**. They are not those originals.

## Searched — not found

- All 157 `origin` heads of `simons357/Ship_it_app`, including B42
  (`cursor/b42-t2-starvation-coeff-f367`), Sprint 01, ChatVault,
  five-lane, and jonathan-handoff trees
- Full git history: the only `.tsv` files ever committed are the
  synthetic pair on `cursor/tsv-data-aa46`
- No deleted `M.tsv` / `b_exact.tsv` in history
- `simons357/ship-it-code` and `simons357/kyrana-oracle`
- GitHub code search for the hash and for `b_exact`
- Live Zenodo inventory already in `data/zenodo/` (papers/TeX/PDF only;
  no TSV lock pair)
- B42, ChatVault, and HB2 cloud-agent transcripts
- Public web for the SHA-256 (no file)

The hash string appears only as a **citation** in B42 docs and in this
fixture’s provenance. No file of that digest is in any checkout we
opened.

## What the B42 note actually contained

The user message on agent
[B42](https://cursor.com/agents/bc-01a0ece0-222b-7906-9e7c-03b56f48f367)
supplied:

- six symbolic row identities (not 20 rows of integers)
- weak residues `(20, −4, 16, 8, 4, 4)` in units of π/12
- the Library JSON SHA-256
- the names `M.tsv` and `b_exact.tsv`

It did **not** attach the files and did not give a disk path. The B42
agent never saw the 20×12 numbers. A Sprint 01 parallelogram
reconstruction is 20×12 and **fails** those identities, so it is not
the Library JSON.

## Most likely remaining locations

These are outside this repository:

1. The chat or machine that wrote the B42 note (the note claims the
   hash was used for the row checks).
2. An **R2 folder** in Files / iCloud / Drive on the phone that sent
   the “R2 folder” / “M.tsv” messages.
3. The other phone’s Google Drive (used before for research dumps).
4. The **iMac Cursor** environment (`Imac cursor account` agent), if
   the Library JSON was generated there and never pushed.
5. ChatVault / Base44 exports, if a Domain Architect library dump was
   stored outside git.

If any of those files appear, drop the real `M.tsv` and `b_exact.tsv`
into `data/R2/` (replacing the synthetic fixture) and run the
read-only verifier. Do not treat the current fixture as the lock.

Canonical locked-r2 identity remains unverified.
Classical Navier–Stokes remains open.
