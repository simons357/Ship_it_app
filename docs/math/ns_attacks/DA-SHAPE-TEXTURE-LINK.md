# DA shape–texture artifacts ↔ five-lane Lemma★

**Date:** 2026-09-10  
**Inspection:** `/opt/cursor/artifacts/da-shape-texture/` (regenerated this session from `scripts/da_shape_navigate_demo.py`)  
**Rule:** DA navigates the library. It does **not** prove Clay / NS. Five-lane numerics do **not** prove Lemma★.

## What’s in the folder

JSON-only demo dump (no images, no `.md` inside the artifact dir itself). Produced by Domain Architect’s shape–texture navigator:

| File | Role |
|------|------|
| `00-library-manifest-summary.json` | Library scan: **69** objects (32 KEEP / 20 HYPOTHESIS / 17 PARK); NS=31, RH=3, SFE=6; Zenodo deposit metadata gap |
| `01-ns-shape-textures.json` | HB five-finger shapes + textures for books `NS-B`, `SND-C`, `BOOT-M`, `SND-U` |
| `02-ns-jx-vs-lambda-texture.json` | Tweet conflation drill: `J/X` vs `λ_min/λ_max` → **SAME_SHAPE_DIFFERENT_TEXTURE** (weld required; hypothesis only) |
| `03-ns-navigation.json` | NS map: **12** matching objects, **7** texture mismatches, **13** open welds |
| `04-ns-splicer-integration.json` | Theory-splicer screen/cut/splice on NS (illegal Clay/SND-U glues refused) |
| `05-ns-sndc-boot-shape-match.json` | `SND-C` vs `BOOT-M`: same shape skeleton, different texture chart |
| `06-rh-shape-textures.json` | RH books `Q6`, `RH-ROUTE-C`, `RH-MD` |
| `07-rh-navigation.json` | RH map: **3** matching objects, **3** welds need attention |
| `08-rh-shape-comparisons.json` | `Q6` vs RH / NS shape compare (cross-prize glue refused where incompatible) |
| `09-rh-splicer-integration.json` | RH splicer screen |
| `10-summary.json` | One-page demo summary |

Regenerate:

```bash
# requires Domain Architect shape-texture code (see branch routing below)
python3 scripts/da_shape_navigate_demo.py
```

Ontology: `docs/domain-architect/SHAPE-TEXTURE-ONTOLOGY.md` on `cursor/da-theory-splicer-0cc5`.

## What it means

**SHAPE** = invariant HB role skeleton (P, H, ψ, λ, Φ, E).  
**TEXTURE** = notation / domain / hypothesis chart (NS PDE vs shell `J/X` vs Bypass `λ_min/λ_max`).

Same mathematical object can wear many textures; rhyming symbols are **not** a proof. DA’s job is map → compare shape → flag texture Δ → refuse illegal splices.

## Connection to five-lane attacks / Lemma★ (shape form)

**Canonical ★ is a shape statement** — [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md). Map DA language onto that reframe carefully (metaphor only; **not** a weld):

| DA term | Five-lane / Lemma★ object | Notes |
|---------|---------------------------|-------|
| **SHAPE** \(v\) | Divergence-free field shape in \(u=av\) | Amplitude \(a\) only changes size; geometry lives on \(v\). DA SHAPE = HB role skeleton; five-lane shape = Fourier profile. **Related metaphor, not the same data structure.** |
| **TEXTURE** / ratio | \(\mathcal R_\star(v)=\mathfrak T_c(v)^2/(\mathcal D_s(v)\,E(v)\,Y(v))\) | Stretching per unit spread, energy, and \(Y\). Pure geometry; same for \(av\) as \(v\); independent of \(\nu\). A chart of small \(\mathcal R_\star\) values is **texture on samples**, not a proof that \(\sup\mathcal R_\star<\infty\). |
| Same shape, different texture | Fixed \(v\), different notation / packaging (viscosity ★ vs boxed shape ★ vs pre-Young) | DA `SAME_SHAPE_DIFFERENT_TEXTURE` rhymes with “same \(v\), many remainder writings” — **not** a product estimate. |
| Illegal splice | Treating a finite \(\mathcal R_\star\) list as \(C_{\mathrm{geom}}\), or DA navigation as Clay | Refuse. |

| Layer | Link |
|-------|------|
| Shared language | Five-lane Attack 2 uses **fixed-shape** high triad amplitude sweeps (`B↑`); DA formalizes “shape” as HB roles. |
| Lemma★ packaging | On the DA side, Lemma★ is book **DA-NS-1** / `--lemma-star` (see `docs/ns-review/LEMMA-STAR-DA-NS-1.md` on splicer). Clay weld **WITHHELD** until **PRODUCT-BLOCK** closes. On this branch: shape-form canonical in `LEMMA_STAR_SHAPE_FORM.md` / `PROOF_LemmaStar_STATUS.md`. |
| Five-lane numeric | This branch: Attacks 1–5 kill K=0, leave Lemma★ / \(C_*\) / \(\sup\mathcal R_\star\) **surviving numeric only**. |
| Do not weld | Do **not** treat DA `SAME_SHAPE_DIFFERENT_TEXTURE` as a closed product estimate, and do **not** treat five-lane plots as a DA library proof. **NS not solved.** |

`da-shape-texture` itself is **NS/RH library navigation**, not the five-lane Galerkin kill drill. Lemma★ demo artifacts live separately under `/opt/cursor/artifacts/da-lemma-star/` (when that agent’s pod wrote them).

## Branch routing (important)

| Concern | Branch | Notes |
|---------|--------|-------|
| Shape–texture ontology + CLI + this demo | `cursor/da-theory-splicer-0cc5` (PR #40) | Commit `f318090` + Lemma★ merge tip ~`8520999` |
| Lemma★ DA registry / PRODUCT-BLOCK | same splicer tip / `cursor/da-lemma-star-0cc5` | NS-only; no SFE glue |
| Five-lane Galerkin attacks 1–5 | **`cursor/ns-five-lane-lemma-star-1390` (this branch)** | `scripts/ns_attacks/`, `docs/math/ns_attacks/` |
| Tao SND-H panel | `cursor/tao-snd-h-panel-a0eb` | **Not** the home for shape-texture or five-lane probes |

**Recommendation:** Keep DA navigation on the splicer branch; keep kill-drill numerics here. Sync status with a short cross-link (this file) rather than merging both stacks blindly. Optional later: teach DA’s Lemma★ screen to cite five-lane artifact paths as **numeric evidence only**.

## Next actions

1. On splicer: `python3 -m domain_architect --lemma-star` / `--navigate DA-NS-1` — confirm PRODUCT-BLOCK still OPEN.  
2. On this branch: continue proof/kill work on boxed shape ★ / \(\sup\mathcal R_\star\), or \(C_* X^{3/2}\Lambda\) + HH→L (see `ATTACK_SYNTHESIS_SIMULTANEOUS.md`, `LEMMA_STAR_SHAPE_FORM.md`). Live kill = almost-single-shell with \(\mathcal R_\star\to\infty\).  
3. Do **not** move five-lane attack code onto `tao-snd-h-panel-a0eb`.  
4. If Jonathan wants one desk: merge **docs pointers** first; code merge only after PRODUCT-BLOCK / five-lane doors are explicit.
