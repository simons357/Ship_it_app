# Shape–Texture Ontology

**Status:** August 2026 — navigation framework extension  
**Author insight:** Jonathan R. Simons — *"think of the math object as a shape. It's a shape; it has different textures, but the object is there."*

Domain Architect (DA) does **not** prove Millennium problems. DA maps what is already in the library and navigates between theory books by comparing **shapes** first, then flagging **texture** mismatches.

## Core metaphor → code

| Concept | Meaning | DA module |
|---------|---------|-----------|
| **SHAPE** | Invariant structural skeleton: HB five-finger roles (P, H, ψ, λ, Φ, E), dependency hints, compatibility class (e.g. `NS-B`, `SND-C`, `Q6`) | `domain_architect/shape_texture.py` → `extract_shape()` |
| **TEXTURE** | Surface chart: notation (NS PDE, shell-helical operator, Clay packaging), domain (T³, arithmetic lattice), hypothesis tags (`X<=M`, `SND-U_or_floor`) | `extract_texture()` |
| **OBJECT** | Shape + texture bundle, tagged with Millennium problem and KEEP/HYPOTHESIS/PARK status | `library_index.py` manifest entries |

### HB five-finger mapping

The Harmonic Blueprint organizational grammar maps directly onto shape fingers:

| Finger | FRA symbol | Role |
|--------|------------|------|
| P | admissibility | selection / div-free / Leray |
| H | interaction | coupling / advection / shell flux |
| ψ | state | velocity / vorticity / flow state |
| λ | scale_response | viscosity / spectral coordinate / shell ratio |
| Φ | realized_output | pressure / bound / regularity claim |
| E | environment | geometry, IC/BC, spread regime, bootstrap |

Same **shape** (all six roles present) can wear different **textures**: NS PDE notation vs tweet `J/X` vs Bypass `λ_min/λ_max`.

## AI overclaim vs DA navigation

AI systems (including earlier agent runs) overclaimed: they treated notation collisions as proof routes and conflated conditional SND-C with unconditional Clay B.

DA refuses that. It:

1. **Maps** what exists in `historical_equations.json`, `snd_claim_inventory.json`, `millennium_books.json`, tweet equations, and docs.
2. **Compares shapes** before attempting any theory splice.
3. **Flags texture mismatches** (e.g. `J/X` vs `λ_min/λ_max`) without asserting an automatic proof.
4. **Integrates theory splicer** (`cut`, `insert`, `splice`, `screen`, `express`) only after shape audit.

*"Everything we need is in the library"* — DA reports coverage gaps honestly when assets are missing (e.g. Zenodo metadata file absent).

## Operations

```bash
# Extract shape from book or expression
python -m domain_architect --shape SND-C
python -m domain_architect --shape "partial_t omega = nu Delta omega"

# Extract texture
python -m domain_architect --texture SND-C

# Shape-first compare (then texture delta)
python -m domain_architect --shape-compare SND-C BOOT-M
python -m domain_architect --shape-compare "inf J/X >= c_*" "lambda_min/lambda_max > -1/2"

# Index library → data/domain_architect/library_manifest.json
python -m domain_architect --library-scan

# One Millennium problem at a time
python -m domain_architect --navigate NS
python -m domain_architect --navigate RH

# Full demo with artifacts
python scripts/da_shape_navigate_demo.py
```

Add `--json` to any command for machine-readable output.

## One theory per session

### Navier–Stokes (NS)

1. `--library-scan` — build manifest.
2. `--navigate NS` — list objects tagged NS sharing shape with `NS-B`, `SND-C`, `BOOT-M`.
3. `--shape-compare SND-C BOOT-M` — compatible shape; texture weld (Bootstrap M) still open.
4. `--shape-compare "inf J/X" "lambda_min/lambda_max"` — same-shape-different-texture; tweet conflation flagged.
5. `--splice-screen NS` + `--splice-cut SND-C THM-D-CLAY` — remove illegal Clay glue.

### Riemann Hypothesis (RH)

1. `--navigate RH` — Q6 arithmetic operator, Route C exploratory, Montgomery–Dyson archive.
2. `--shape-compare Q6 RH-ROUTE-C` — open weld; insufficient information for proof splice.
3. `--shape-compare Q6 NS-B` — incompatible shapes; refuse cross-problem glue.

## Theory splicer integration

Shape–texture audit runs **before** splice:

- `COMPATIBLE` shape → splice may proceed (with weld lemma if `COMPATIBLE_DISTINCT`).
- `SAME_SHAPE_DIFFERENT_TEXTURE` → `texture_translate()` suggests hypothesis-only chart change; explicit weld required.
- `INCOMPATIBLE` → splice refused (e.g. SFE→NS, Q6→NS, SND-C→Clay B).

## Artifacts

Demo output: `/opt/cursor/artifacts/da-shape-texture/`

## What this does NOT claim

- Clay Statement B is not proved.
- RH is not proved.
- Texture translation is not automatic proof.
- Library scan does not invent missing manuscripts.

DA provides a **navigation map** — the object (shape) is there; textures are choices of coordinates on it.
