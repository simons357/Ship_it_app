# Domain Architect — Theory Splicer Whole Package

**Single entry point** for the CRISPR-style theory-book toolkit.

| | |
| --- | --- |
| **Branch** | `cursor/da-lemma-star-five-lane-0cc5` (sync) · base package `cursor/da-theory-splicer-0cc5` |
| **PR** | Package [#40](https://github.com/simons357/Ship_it_app/pull/40) · Lemma★ [#49](https://github.com/simons357/Ship_it_app/pull/49) · five-lane evidence [#48](https://github.com/simons357/Ship_it_app/pull/48) |
| **Companion** | Lemma★ / DA-NS-1 = Millennium packaging (locked); NS-only, no SFE glue |
| **Audience** | Jonathan R. Simons |
| **Honesty lock** | Lemma★ **not proved**; PRODUCT-BLOCK / HH→L gap open; numeric survive ≠ proof; **NS NOT SOLVED** |

---

## What this package is

Domain Architect (DA) runs **CRISPR operations on mathematical theory books**:

`CUT` · `INSERT` · `SPLICE` · `KNOCKOUT` · `SCREEN` · `EXPRESS`

It is a **bullshit destroyer**: it maps welds, refuses illegal glue, and keeps Millennium packaging honest.

It is **not** a Millennium prover. EXPRESS never greens Clay NS, RH, Yang–Mills, etc.

---

## Shape vs texture (one paragraph)

**Shape** is the invariant finger topology (HB roles P, H, ψ, λ, Φ, E / compatibility class). **Texture** is the surface chart (NS PDE vs shell `J/X` vs energy-budget `T_c`/`Λ` vs ζ notation). Same shape can wear different textures; DA compares shape first, then flags texture mismatch — it does not treat a notation collision as a proof route.

Deep dive: [`SHAPE-TEXTURE-ONTOLOGY.md`](./SHAPE-TEXTURE-ONTOLOGY.md) · Ops playbook: [`THEORY-SPLICER-PLAYBOOK.md`](./THEORY-SPLICER-PLAYBOOK.md) · Lemma★: [`../ns-review/LEMMA-STAR-DA-NS-1.md`](../ns-review/LEMMA-STAR-DA-NS-1.md)

---

## File inventory

### Core modules

| Path | Role |
| --- | --- |
| `domain_architect/theory_splicer.py` | CRISPR ops on millennium theory books |
| `domain_architect/shape_texture.py` | Shape extract / texture extract / shape-match / navigate |
| `domain_architect/library_index.py` | Library scan → manifest |
| `domain_architect/lemma_star.py` | Lemma★ / DA-NS-1 NS-only packaging + PRODUCT-BLOCK honesty |
| `domain_architect/cli.py` | CLI flags for splicer, shape/texture, library, Lemma★ |
| `domain_architect/__main__.py` | `python3 -m domain_architect` entry |

### Data

| Path | Role |
| --- | --- |
| `data/domain_architect/millennium_books.json` | Millennium problem → books + welds registry |
| `data/domain_architect/library_manifest.json` | Indexed library objects (KEEP / HYPOTHESIS / PARK) |
| `data/domain_architect/snd_claim_inventory.json` | SND / Lemma★ claim inventory |
| `data/domain_architect/historical_equations.json` | Historical equation library (incl. Lemma★ refs) |
| `data/domain_architect/conflicts.json` | Conflict / weld table |

### Docs

| Path | Role |
| --- | --- |
| `docs/domain-architect/THEORY-SPLICER-PACKAGE.md` | **This file** — whole-package entry |
| `docs/domain-architect/THEORY-SPLICER-PLAYBOOK.md` | CRISPR ops walkthrough (NS then RH) |
| `docs/domain-architect/SHAPE-TEXTURE-ONTOLOGY.md` | Shape / texture ontology |
| `docs/ns-review/LEMMA-STAR-DA-NS-1.md` | Lemma★ Millennium packaging, PRODUCT-BLOCK / HH→L, five-lane sync → PR #48 |

### Demos & tests

| Path | Role |
| --- | --- |
| `scripts/da_theory_splicer_demo.py` | End-to-end splicer demo (NS → RH) |
| `scripts/da_shape_navigate_demo.py` | Shape/texture + library navigate demo |
| `scripts/da_lemma_star_demo.py` | Lemma★ / PRODUCT-BLOCK honesty demo |
| `tests/test_theory_splicer.py` | Splicer unit tests |
| `tests/test_shape_texture.py` | Shape/texture unit tests |
| `tests/test_lemma_star.py` | Lemma★ refuse / WITHHELD tests |

---

## Install / run

From repo root (`Ship_it_app`):

```bash
# no extra install beyond stdlib + repo checkout
python3 -m domain_architect --help
```

Requires Python 3.10+ (dataclasses, `list[str]` typing). Data files ship under `data/domain_architect/`.

---

## Command cheat sheet

```bash
# --- Millennium map ---
python3 -m domain_architect --list-millennium

# --- CRISPR ops ---
python3 -m domain_architect --splice-screen NS
python3 -m domain_architect --splice-screen RH
python3 -m domain_architect --splice-screen LEMMA-STAR
python3 -m domain_architect --splice-cut NS CLAY-B
python3 -m domain_architect --splice-insert BOOT-M "candidate bootstrap lemma"
python3 -m domain_architect --splice-join SND-C BOOT-M
python3 -m domain_architect --theory-express NS-B
python3 -m domain_architect --theory-express DA-NS-1   # refuses PROVED / HYPOTHESIS

# --- Shape / texture / library ---
python3 -m domain_architect --shape SND-C
python3 -m domain_architect --texture SND-C
python3 -m domain_architect --shape-compare SND-C BOOT-M
python3 -m domain_architect --library-scan
python3 -m domain_architect --navigate NS
python3 -m domain_architect --navigate RH
python3 -m domain_architect --navigate DA-NS-1

# --- Lemma★ (NS-only) ---
python3 -m domain_architect --lemma-star
python3 -m domain_architect --lemma-star --json

# --- Demos ---
python3 scripts/da_theory_splicer_demo.py
python3 scripts/da_shape_navigate_demo.py
python3 scripts/da_lemma_star_demo.py

# --- Tests ---
python3 -m unittest tests.test_theory_splicer tests.test_shape_texture tests.test_lemma_star -v
```

JSON on any flag: add `--json`.

---

## One-theory-at-a-time workflow

1. **NS first** — `--splice-screen NS` → cut illegal Clay/SND-U/SFE→NS welds → work BOOT-M / Lemma★ PRODUCT-BLOCK honestly → `--navigate NS` / `--lemma-star`.
2. **Only then RH** — `--splice-screen RH` → Q6 is KEEP arithmetic (no RH claim) → Route-C withheld until operator→zeta lemma → never Q6→NS.
3. Do not jump problems until the current book's welds are honest.

---

## What is REFUSED

| Claim | Verdict |
| --- | --- |
| Clay NS proved / H→Clay glue | **REFUSED** |
| SFE → NS splice | **REFUSED** |
| Q6 → NS / Q6 → RH as proved | **REFUSED** / withheld |
| SND-C → Clay B (X≤M missing) | **INCOMPATIBLE** |
| SND-C → SND-U | **INCOMPATIBLE** |
| Theorem D Clay ⇔ SND | **INCOMPATIBLE** |
| Lemma★ proved without PRODUCT-BLOCK | **REFUSED** (WITHHELD weld; EXPRESS refuses green) |
| Lemma★ “almost proved” / greening / numeric survive = proof | **REFUSED** |
| K=0 absorption as Lemma★ | **DEAD** (five-lane Attack 2 — PR #48) |
| Any Millennium EXPRESS as PROVED | **REFUSED** unless reconstruction honesty path passes (none do for Clay) |

---

## Honest status — Millennium books

| Problem | Registry status | Honest note |
| --- | --- | --- |
| **NS** | OPEN | Clay B NOT proved. **NS NOT SOLVED.** SND-C conditional under X≤M. Lemma★ = Millennium packaging (HYPOTHESIS); Clay weld WITHHELD until PRODUCT-BLOCK / HH→L closes. Five-lane (PR #48): K=0 dead; ★ survives numeric kill only ≠ proved. |
| **RH** | OPEN | NOT proved. Q6 KEEP arithmetic — no RH claim. Route C exploratory. |
| **Yang–Mills** | OPEN | Stub only. |
| **P vs NP** | OPEN | Stub only. |
| **BSD** | OPEN | Stub only. |
| **Hodge** | OPEN | Stub only. |
| **Poincaré** | SOLVED_REFERENCE | Perelman — REFERENCE only, not re-proof. |

NS books of note: `NS-B`, `SND-C`, `SND-U` (RETIRE), `CLAY-B` (RETIRE), `BOOT-M`, `SND-HYP`, `SFE` (RETIRE / no glue), `NS-Q1`, `DA-NS-1` (Lemma★ HYPOTHESIS), `PRODUCT-BLOCK` (OPEN).

---

## Related PRs

| PR | Topic |
| --- | --- |
| **[#40](https://github.com/simons357/Ship_it_app/pull/40)** | Theory splicer whole package + shape/texture + Lemma★ |
| **[#49](https://github.com/simons357/Ship_it_app/pull/49)** | Lemma★ / DA-NS-1 companion (NS-only) |
| **[#48](https://github.com/simons357/Ship_it_app/pull/48)** | Five-lane Lemma★ drill — K=0 dead; ★ survives numeric; HH→L gap; **NS not solved** |
| [#36](https://github.com/simons357/Ship_it_app/pull/36) | DA gap-closure / SND audit / refuse Clay glue |
| [#35](https://github.com/simons357/Ship_it_app/pull/35) | ARCHON Theorem H panel |
| [#28](https://github.com/simons357/Ship_it_app/pull/28) | Five-finger auto-router |
| [#30](https://github.com/simons357/Ship_it_app/pull/30) | Domain Architect v1 |

Five-lane sync branch: `cursor/da-lemma-star-five-lane-0cc5`. Lemma★ earlier companion: `cursor/da-lemma-star-0cc5` (NS-only, **no SFE glue**).

---

## Reproduce

```bash
python3 scripts/da_theory_splicer_demo.py
python3 scripts/da_shape_navigate_demo.py
python3 scripts/da_lemma_star_demo.py
python3 -m unittest tests.test_theory_splicer tests.test_shape_texture tests.test_lemma_star -v
```

**Package-focused tests: 63 OK** (`test_theory_splicer` + `test_shape_texture` + `test_lemma_star`).

Artifacts land under `/opt/cursor/artifacts/da-theory-splicer/`, `da-shape-texture/`, `da-lemma-star/`, and package bundle `da-theory-splicer-package/`.

---

## First 3 commands (right now)

```bash
python3 -m domain_architect --list-millennium
python3 -m domain_architect --splice-screen NS
python3 -m domain_architect --lemma-star
```
