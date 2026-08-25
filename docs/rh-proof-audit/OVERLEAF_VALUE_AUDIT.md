# Overleaf value audit vs controlling pack

**Date:** 15 August 2026  
**Original Mac path (not mounted on this VM):** `/Users/jonathansimons/Desktop/RH_Proof_Chain_Synthesis/00_status/OVERLEAF_VALUE_AUDIT.md`  
**Salvage (25 August 2026):** this file is the standing policy from that audit. The 117-line Desktop original was **not** found on this VM. No Overleaf share URLs are invented here. This document does **not** claim that RH or Navier–Stokes is proved.

---

## Standing salvage

Take anything useful. Ignore the item if this repository already has it, or has a better copy. Jonathan’s question (“we are not doing anything with this?”) is about **whether Overleaf projects still control the science**. They do not.

This salvage is **not** a request to prove RH or NS.

---

## Scientific control (lock this)

| Role | What | Status |
|---|---|---|
| **Scientific truth** | Desktop pack `RH_Proof_Chain_Synthesis` | **Controlling** |
| Pack folders | `03_submission_draft`, `07_zenodo_final_pack_2026-08-15`, `08_publish_queue_2026-08-15`, `06_navier_stokes_shelf` | Use these names even if the files are absent from this VM |
| Existing Overleaf projects | April–June 2026 NS / Clay / QStack snapshots | **Ignore for scientific control** |
| Overleaf login / live URLs | None in the 15 August audit; none found | Do **not** invent share URLs |
| Overleaf going forward | Optional **PDF printer only** | Upload **fresh TeX from the pack**, compile, download. Do **not** reopen old projects as source of truth |

**Hard rule:** no “Clay NS proved” and no “RH proved” claims from old Overleaf faces.

---

## Controlling faces NOW

Use these **names** in docs even if the files are not on this VM.

| Face | Controlling filename | Pack location (Desktop) |
|---|---|---|
| Inv/RH | `PAPER_A_Inverse_GCD_CORRECTED.tex` | pack (`03_submission_draft` / RH faces) |
| Möbius Q6 | `PAPER_B_Mobius_GCD_Q6.tex` | pack (`03_submission_draft` / RH faces) |
| Positive GCD | `GCD_Spectral_Paper1_UPDATED_2026-08-14.tex` | pack |
| Ring | `c8a03f315_RingLemma_Simons_June19_2026.tex` | `06_navier_stokes_shelf/01_ring_lemma/` |
| Phi-renorm | `NS_PhiRenorm_complete.tex` | `07_zenodo_final_pack_2026-08-15/NS/` |
| Paper2 | `Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex` + FIXED PDF (Aug 1) | pack; **simplex OPEN** |
| Anesthesia | `PAPER1_REBUILT_Coherence_Index.md` | `08_publish_queue_2026-08-15/ANESTHESIA/face_manuscript/` |

Paper2 is a **conditional** face. The Aug 1 FIXED PDF keeps **simplex OPEN**. It is not a Clay existence/uniqueness/regularity proof.

---

## QUARANTINE (do not cite as current)

| Item | Why quarantined |
|---|---|
| `b6e5416c8` / `3673bad0d` `simons_ns_overleaf` `main.tex` | Unconditional Clay / global regularity language |
| `CLAY_FINAL.tex` | Old Overleaf face; not the pack controller |
| `SERPENT_FINAL.tex` | Old Overleaf face; not the pack controller |
| `WHAT_I_FOUND.tex` | Old Overleaf face; not the pack controller |

These are **museum**. Do not reopen them as source of truth. Do not cite them for current scientific claims. Do not treat their compiled PDFs as the public face.

---

## Overleaf as printer (optional)

If a PDF is needed:

1. Copy **fresh TeX from the Desktop pack** (controlling filenames above).
2. Upload to a **new** Overleaf project (or a blank one). Do not revive April–June snapshots.
3. Compile. Download the PDF.
4. Discard the Overleaf copy as a working original. The pack remains the original.

Do not log into old projects to “see what we had.” Those faces are the quarantine table.

---

## What this VM has / does not have

| Object | On this cloud VM? |
|---|---|
| `RH_Proof_Chain_Synthesis` Desktop pack | **No** |
| `06_navier_stokes_shelf` | **No** |
| Ring June 19 TeX (`c8a03f315_…`) | **No** |
| `NS_PhiRenorm_complete.tex` | **No** |
| Original `OVERLEAF_VALUE_AUDIT.md` (117 lines) | **No** |
| This salvage + README | **Yes** (`docs/rh-proof-audit/`) |

Related git branches may hold **other** Ring / Φ-renorm / Q6 notes (Zenodo remediation, Tao panel, swirl continuation). Those are **not** this Desktop pack and **not** a license to treat old Overleaf as controlling.

---

## Claims this file refuses

- Riemann Hypothesis is **not** proved by this salvage, by old Overleaf, or by naming Paper A / Paper B.
- Clay Navier–Stokes (unconditional 3D global regularity) is **not** proved by this salvage, by quarantined `main.tex`, or by Paper2 / Ring / Φ-renorm faces.
- Paper2 simplex stability remains **OPEN**.
- Φ-renorm is an **augmented / swirl** writeup in the pack, not a Clay closer.

---

## Pointers inside this folder

- Policy (this file): `docs/rh-proof-audit/OVERLEAF_VALUE_AUDIT.md`
- Folder README: `docs/rh-proof-audit/README.md`
- Other agents may add numerics (e.g. `qn_gap_numerics.py`) **alongside**. Do not delete them. They are not a substitute for the Desktop pack.
