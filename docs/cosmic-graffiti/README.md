# Cosmic Graffiti — working magazine

**Cosmic Graffiti** is the magazine. **The Frequency** is the news feed that
runs through it. This folder is the live working copy Jonathan Simons can
keep adding to. It is not a second physics engine and it is not Domain
Architect.

Live product remains **Domain Architect**:

```
DECOMPOSE → CROSS-DOMAIN TRANSLATE → SYNTHESIZE
```

Spec: [`docs/DOMAIN-ARCHITECT.md`](../DOMAIN-ARCHITECT.md).  
Operator: [`docs/domain-architect/DA-MODE.md`](../domain-architect/DA-MODE.md).  
Decision: Jon `accept grok table`.

House tone (already on the public HTML stack): wonder first · labels loud ·
for the record / not the last word. Kind. Adult. No slogans pretending to
be theorems.

## Identity (do not fork)

This is the same magazine as the 13 September 2026 Cosmic Graffiti site,
not a rename and not a second brand.

| Piece | Where it already lives |
|---|---|
| Public HTML stack | [cosmic-graffiti-magazine.vercel.app](https://cosmic-graffiti-magazine.vercel.app/) |
| Live look + VAL8000 little box | [`magazine/`](magazine/README.md) — Issue 1 stays the lead; VAL docks in the corner |
| VAL8000 persona | [`val8000.md`](val8000.md) — resident superagent, after the news |
| Locked 13 Sep copy | git branch `cursor/cosmic-graffiti-archive-9d6b` under `docs/archive/cosmic-graffiti-magazine-2026-09-13/` |
| Working markdown (this folder) | issues Jon can edit, plus Frequency items with real URLs |
| Older swirl leftover / “GRAFITTI” typo cut | other branches only; do not revive the misspelling here |

The older Frequency rail was mostly in-house tips (open doors, Zenodo
credit, Issue 1). Jon asked for the next chapter to carry **news of the
area** — math, physics, fluids, primes-as-math, cosmology as public
science — with honest comments. That is an extension of the same feed,
not a new magazine.

## How an issue is built

```
The Frequency (sourced news)
    → CG comment (what was shown vs hype)
    → Around us (one ordinary-life piece)
    → What I’m doing (Jon’s lab, editable)
    → Humor (a check on self-importance, with a picture)
    → Apps for fun (inventory, not fake store listings)
    → Subscriber table (plan vs what already exists)
    → Empty trays (Jon’s stories, photos, later news)
```

Paste-ready Substack markdown lives in `issues/`. A short Skool variant
sits next to the issue. Pictures live in `issues/assets/`. Drop files for
later in `issues/_trays/`.

## How Jon adds to it

1. Open the current issue, or copy it to a new dated file
   `issues/YYYY-MM-DD-the-frequency.md`.
2. Add Frequency items only when you have a date and a URL. If you cannot
   verify a story, drop it. Label preprints as preprints.
3. Put your own writing in the trays, or replace the
   **What I’m doing → Jon’s update** block.
4. Drop photos in `issues/assets/` and link them with alt text.
5. For Substack: paste the issue markdown; upload the PNGs (Substack does
   not read this git folder). For Skool: use the short post file.
6. Do not turn on a paywall in this repo. The subscriber table is a
   **plan**.
7. Do not stamp `TRANSFORMABLE` without a real morphism and witness (A5).
   Do not overwrite `DA-VC-01` as PASS. Do not claim unaugmented
   Navier–Stokes regularity is closed. Do not claim the Riemann
   hypothesis is proved. Do not glue letters (`Φ`, `H_N`, `Q6`, `H`).
8. Autobiography, childhood, and music coincidences stay out of git.
9. Leave [`docs/learn/`](../learn/) alone if someone else is building a
   learning pack there.

## Patents and archive

Domain Architect does **not** file patents. Historical patent-style
documents in [`docs/archive/`](../archive/README.md) are Jon’s IP/archive.
If the magazine ever shares them with subscribers, say that plainly. Do
not call them DA filings. Do not say anyone patented the universe. Jon
has said he is not suing.

A 14 September 2026 equation dump under `docs/archive/sfe-hb/` is a
**shelf book of unknown provenance**. Do not import it here as a live
theory.

## Tests

```bash
python -m unittest tests.test_cosmic_graffiti_frequency tests.test_val8000 tests.test_val8000_box
```
