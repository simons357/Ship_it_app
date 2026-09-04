# Zenodo update map — Tier 1 corrected texts

**Folder:** `docs/papers/submit/`  
**Rule:** Upload these cleaned files as **new versions** of the matching records (or new deposits where noted). Leave overclaim records as archive + short description note.

---

## Q6 in one line

The inverse-GCD **operator** is real. The **prize claims** (Goldbach dark states, full-spectrum \(\lambda_{\min}>-1/2\), RH/NS via Q6) are **not** correct.  
**Proper write-up:** `04_q6_inverse_gcd.tex` (Bridge\* + definitions + explicit withdrawals). Use that to overwrite/supersede `20405589`.

---

## Update these (Tier 1 → corrected file)

| # | Credit | Zenodo DOI to open | Upload this file | New title / description line |
| --- | --- | --- | --- | --- |
| 1 | Phi-renorm | [20405405](https://doi.org/10.5281/zenodo.20405405) **and** [20405597](https://doi.org/10.5281/zenodo.20405597) | `01_phi_renormalization.tex` | *Phi-Renormalization for Axisymmetric Navier–Stokes with Swirl: Algebraic Cancellation of the \(1/r^4\) Axis Term.* Scope: \(Q_1\)-augmented / Phi system; classical 3D NS not claimed. |
| 2+3 | Ring + SND | Prefer [20518057](https://doi.org/10.5281/zenodo.20518057); also soft-update [19842060](https://doi.org/10.5281/zenodo.19842060), [20405585](https://doi.org/10.5281/zenodo.20405585) | `02_ring_lemma_snd_conditional.tex` | *A Ring Lemma for Band-Limited Vorticity Direction and a Conditional Spectral Non-Dispersal Criterion.* Conditional on SND; unconditional SND open. |
| 4 | T2 | [20552080](https://doi.org/10.5281/zenodo.20552080) | `03_t2_shell_flux_gronwall.tex` | Drop “GNC–Goldbach” from title. *Shell-flux Gronwall under SND (T2).* Conditional only. |
| 5 | Route C | [20518388](https://doi.org/10.5281/zenodo.20518388) | `05_route_c_conditional.tex` | Keep “conditional on two gaps.” Remove any “RH proved” language from description. |
| 6 | Bridge\* / **proper Q6** | Prefer **new version** of [20405589](https://doi.org/10.5281/zenodo.20405589) (old Goldbach Q6), or new deposit | **`04_q6_inverse_gcd.tex`** | Title: *The Inverse-GCD Operator \(Q_N\): Definitions, a Restricted Rayleigh Bound, and Withdrawal of Full-Spectrum Floor Claims.* Not Goldbach/RH/NS. Optional short extract: `04_bridge_star_prime_pairs.tex`. |
| 7 | Hygiene | Optional new deposit, or paste into each overclaim description | `06_status_errata.tex` | One-page public status: what stands / what is withdrawn. |

Also soft-update [20272545](https://doi.org/10.5281/zenodo.20272545) description to point at `02_…` as the honest SND framing (or upload `02` there as a new version if you prefer one SND home).

---

## Do **not** replace with Tier 1 math — add a description note only

On each of these, add something like:

> *Correction (Aug 2026): Prize / closure claims in this record are withdrawn. See corrected Tier‑1 notes (Phi / Ring+SND / T2 / Bridge\* / Route C conditional) and the status sheet DOI [fill in]. This file remains as dated archive.*

| DOI | Record |
| --- | --- |
| [20405526](https://doi.org/10.5281/zenodo.20405526) | Global Regularity / Statement (B) |
| [20269843](https://doi.org/10.5281/zenodo.20269843) | Quantum Lens |
| [20405589](https://doi.org/10.5281/zenodo.20405589) | Q6 Goldbach |
| [20405593](https://doi.org/10.5281/zenodo.20405593) | Montgomery–Dyson as Q6 |
| [20552171](https://doi.org/10.5281/zenodo.20552171) | Three-in-one |
| [20552400](https://doi.org/10.5281/zenodo.20552400) | Triple Lock |

---

## Zenodo click path (each record)

1. Open the DOI → **New version** (or Edit metadata if you only change description).
2. Upload the matching `.tex` from `docs/papers/submit/` (PDF optional if Overleaf compiles).
3. Paste the new title + one-sentence scope from the table.
4. Publish version.

Bridge\* and the status sheet: **New upload** → get a fresh DOI → put that DOI into the correction notes on the withdrawn records.

---

## Compile tip

New blank Overleaf project → paste one `.tex` → Recompile → Download PDF → upload PDF + `.tex` to Zenodo. One project per paper. Do not reopen old Quantum Lens / Triple Lock Overleaf projects.
