# Overleaf value audit vs controlling pack

**Filed:** 25 August 2026 into `Ship_it_app` as historical hygiene.  
**Original date:** 15 August 2026  
**Source:** `OVERLEAF_VALUE_AUDIT 2.md` (Desktop / pack control).  
**This git repo is not that Desktop pack.** RH, \(Q_6\), GCD Paper1, anesthesia CI, and Ring-lemma faces listed below are **other books**. They are not live Domain Architect.

## Addendum for this branch (25 August 2026)

The 15 August verdict still holds for **old Overleaf**: April–June Clay / SERPENT / “unconditional regularity” projects are a museum. Do not reopen them as source of truth. Do not upload them.

For **swirl on this branch**, the 15 August “controlling face” `NS_PhiRenorm_complete.tex` in the Desktop pack is **older than**:

`docs/papers/swirl/Simons_PhiRenorm_Swirl_2026-08-22.tex`

Use the 22 August TeX here. Classical unaugmented swirl stays **open**. \(\varepsilon\)-smoothness is not Clay. April Overleaf mains that claim unconditional Leray–Hopf / Clay stay **quarantine**.

QStack, de-augmentation “bridges,” and SERPENT stay historical. Domain Architect does not revive them.

Overleaf, if used at all: blank project, paste **this** TeX, compile PDF. Never the April projects.

---

# Overleaf value audit vs controlling pack

**Date:** 15 August 2026  
**Pack control:** `RH_Proof_Chain_Synthesis` (`03_submission_draft`, `07_zenodo_final_pack_2026-08-15`, `08_publish_queue_2026-08-15`, `06_navier_stokes_shelf`)  
**Access honesty:** **No Overleaf login.** This audit is from **local exports + inventory only**. Live Overleaf project dashboards / share URLs were **not** inspected. No `https://www.overleaf.com/project/…` share links were found on Desktop / pack / frankie dump (only generic “use Overleaf to compile” mentions).

---

## Verdict (plain)

**Ignore existing Overleaf projects for scientific control.**  
They are **April–June 2026 NS / Clay / QStack** snapshots. They do **not** hold PAPER_A, PAPER_B, updated GCD Paper1, NS Paper2 Aug 1 FIXED, Ring June 19 controlling TeX, Phi-renorm complete, or anesthesia CI.

**Desktop pack is enough** for Zenodo Wave 1–2 and anesthesia A1 submit.  
Overleaf is **optional only as a PDF printer**: upload **fresh TeX from the pack**, compile, download PDF — **do not reopen old projects** as source of truth. Local MacTeX / TeX Live works the same; this environment has no `pdflatex`.

---

## Inventory of Overleaf-related artifacts found

| Artifact | Location | Date stamp | What it is |
|---|---|---|---|
| `219709d19_CLAY_FINAL_OVERLEAF/` | `Downloads/` | Apr 23 | `CLAY_FINAL.tex` + shared NS figs — Ring/QStack **augmented** Clay-era draft |
| `e399df8e7_SERPENT_FINAL_OVERLEAF/` | `Downloads/` | Apr 23 | `SERPENT_FINAL.tex` — self-stabilizing NS + “Theorem D Clay Equivalence” |
| `8a2077729_WHAT_I_FOUND_OVERLEAF/` | `Downloads/` | Apr 23 | `WHAT_I_FOUND.tex` — narrative NS / Ring picture essay |
| `b6e5416c8_simons_ns_overleaf/` | `Downloads/` | Apr 30 | `main.tex` + lemmas — **claims unconditional Leray–Hopf global regularity / Clay** |
| `3673bad0d_simons_overleaf_FINAL/` | `Downloads/` | Apr 30 | **Identical** `main.tex` SHA to above (+ figs) |
| `overleaf_package/` | Frankie raw gather → pack `01_canonical_sources/…/files/overleaf_package/` | Jun 25 | 3 PDFs + flow PNG (Q3 / QStack audit / Step6 de-aug) |
| Zip `.textClipping` stubs | `Downloads/` | Apr 23 | Point at CLAY zip download UI — no extra TeX |
| Pack mentions of Overleaf | `05_zenodo_upload_kit/`, `07_…/README.md`, status publish lists | Aug 14–15 | **Compile helper only** — not a content source |
| ChatVault / chat exports | generic “open Overleaf.com” compile tips | older | No project list / no controlling TeX |

**Not found in any Overleaf export folder:** `PAPER_A_*`, `PAPER_B_*`, `GCD_Spectral_Paper1_UPDATED_*`, `Simons_NS_Paper2_*REPAIRED*`, anesthesia CI face, Zenodo Wave kits.

---

## Map: Overleaf-held → current controlling faces

| Topic | Old Overleaf / export face | Controlling face **now** (use this) |
|---|---|---|
| Inv / RH-adjacent | *(absent from Overleaf exports)* | `03_submission_draft/PAPER_A_Inverse_GCD_CORRECTED.tex` (= zenodo `RH/`) |
| Möbius \(Q_6\) | *(absent)* | `PAPER_B_Mobius_GCD_Q6.tex` + proved lemmas + `mobius_gcd_v2_1.py` |
| Positive GCD | *(absent from Overleaf dirs; older TeX may sit loose in Downloads)* | `GCD_Spectral_Paper1_UPDATED_2026-08-14.tex` |
| Ring Lemma | Embedded as section inside Apr Clay/SERPENT/WHAT_I_FOUND | `06_…/01_ring_lemma/c8a03f315_RingLemma_Simons_June19_2026.tex` + Zenodo PDF `19a2b85fc_…` |
| Phi-renorm / swirl | *(not in named Overleaf export folders)* | `NS_PhiRenorm_complete.tex` / PDF in `07_…/NS/` |
| NS Paper2 / SND | Apr `simons_ns_overleaf` **unconditional Clay** TeX | **In this git repo:** August TeX [`docs/papers/ns-snd/Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex`](../papers/ns-snd/Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex) and June PDF [`docs/papers/ns-snd/Paper2_NS_Regularity_SND_FIXED.pdf`](../papers/ns-snd/Paper2_NS_Regularity_SND_FIXED.pdf). They are **not** a compile pair. Diff: [`FACES.md`](../papers/ns-snd/FACES.md). Simplex OPEN. |
| QStack / de-aug bridges | `overleaf_package` Jun PDFs + Apr SERPENT/CLAY | Historical only; de-aug **OPEN** per NS shelf |
| Anesthesia CI | *(nothing Overleaf)* | `08_…/ANESTHESIA/face_manuscript/PAPER1_REBUILT_Coherence_Index.md` |

---

## Keep / may still have unique value

| Item | Why (narrow) |
|---|---|
| **NS figure set** in Apr exports (`fig1_three_spheres.png`, `fig2_ring_lemma.png`, `fig3_spread_conc.png`, `fig4_dashboard.png`, `fig5_flow.png` / `d5c406be5_FlowOverHump-1.png`) | Handy art assets; flow PNG already duplicated in frankie/Archon. Useful for slides — **not** for claim text. |
| **`overleaf_package/*.pdf` (Jun 25)** — Q3 BridgeClosed, QStack Bridge Audit Memo, Step6 DeAugmentation | Possibly the only packaged **PDF** snapshots of those memo titles in the gather. Treat as **historical NS/QStack provenance**, not as Aug 2026 science control. |
| **Fresh blank Overleaf project** (if you want PDFs without installing TeX) | Value = **compiler**, not archive. Always paste TeX **from the pack**. |

Nothing in the old Overleaf exports is required for Zenodo Wave 1 or anesthesia A1.

---

## Duplicate of local pack (safe to ignore Overleaf)

| Item | Duplicate of |
|---|---|
| `3673bad0d_simons_overleaf_FINAL/main.tex` | Bit-identical to `b6e5416c8_simons_ns_overleaf/main.tex` |
| Shared fig set across CLAY / SERPENT / WHAT_I_FOUND / ns_overleaf | Same hashes; one copy enough |
| `fig5_flow.png` | = frankie / Archon `d5c406be5_FlowOverHump-1.png` |
| Pack README “compile on Overleaf” lines | Process note only — TeX already in `03_` / `07_` |

**Safe to ignore Overleaf** for: PAPER_A/B, GCD Paper1 updated, Ring June 19, Phi-renorm complete, Paper2 FIXED/Aug1, anesthesia face.

---

## Outdated / wrong / quarantine (do not use)

| Item | Why |
|---|---|
| `b6e5416c8_simons_ns_overleaf` / `3673bad0d_…_FINAL` `main.tex` | Claims **unconditional** global regularity / Clay reduction closed — **superseded** by Aug 1 conditional Paper2 (simplex OPEN). **Do not upload / do not cite as current.** |
| `CLAY_FINAL.tex` | Apr Clay-era augmented “global regularity” packaging — not controlling Ring; not Paper2 FIXED |
| `SERPENT_FINAL.tex` | QStack-augmented NS + Clay-equivalence theater — quarantine vs `NS_MASTER_STACK` |
| `WHAT_I_FOUND.tex` | Narrative / picture-as-proof essay — not a submission face |
| Any live Overleaf project still titled Clay / Serpent / Simons NS FINAL / “Millennium” | Assume **same generation** until proved otherwise by export |
| Using Overleaf as source for RH / Inv / \(Q_6\) | Those controlling faces **never lived** in the exported Overleaf trees |

**Hard rule reminder:** no Clay NS proved / no RH proved claims from these or any other face.

---

## Unknown / need login to check

| Unknown | Why it matters |
|---|---|
| Full list of projects still on the Overleaf **account** | Exports cover only 5 named folders + frankie `overleaf_package`. Other projects may exist (GCD, anesthesia, mid-summer drafts) that were never zipped to Downloads. |
| Whether live projects diverge from Apr exports | Without login, cannot confirm sync / last edit dates. |
| Whether any project holds a **newer** Ring-only or Paper2 edit | Unlikely to beat Aug 1 TeX in the pack, but unverified. |

**If you log in once:** screenshot the project list; anything older than June 2026 → archive/delete; anything that looks like current math → **diff against pack TeX**, then delete or replace with pack upload.

---

## Zenodo + anesthesia: do you need Overleaf?

| Goal | Need Overleaf? | What to use |
|---|---|---|
| **Zenodo Wave 1** (Paper1 / PAPER_A / PAPER_B) | **No** for content. Optional for PDF if you lack local LaTeX. | Upload `.tex` (+ PDF if you want) from `07_zenodo_final_pack_2026-08-15/` |
| **Zenodo Wave 2** (Ring / Phi / Paper2) | **No.** Ring + Phi stay in the pack. Paper2 June PDF and August TeX are now in `docs/papers/ns-snd/` | Prefer git ns-snd faces; do not merge them |
| **Anesthesia A1** | **No.** Face is Markdown in `08_publish_queue_…/ANESTHESIA/` | Export Word/PDF from that MD; Overleaf irrelevant |

---

## One-line policy

**Scientific truth = Desktop pack. Old Overleaf = museum of April Clay/QStack. New Overleaf = disposable PDF machine fed only from the pack.**
