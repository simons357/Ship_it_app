# Swirl (Book B) has several faces. They are not a compile of 22 August.

Do **not** treat the May Zenodo PDF, the 30 June PDF, or the older TeX
sources as a compile of [`Simons_PhiRenorm_Swirl_2026-08-22.tex`](Simons_PhiRenorm_Swirl_2026-08-22.tex).
Do **not** glue swirl \(\Phi = u_\theta/r\) to Paper2 \(\Phi_j\) or FRA output \(\Phi\).
Classical unaugmented axisymmetric-with-swirl regularity is **OPEN**. Clay is
**NOT CLAIMED**. Do not stamp DA-VC-01 PASS from these files.

| Face | File | What it is |
|---|---|---|
| Controlling theorem (22 August 2026) | [`Simons_PhiRenorm_Swirl_2026-08-22.tex`](Simons_PhiRenorm_Swirl_2026-08-22.tex) | *Phi-renormalization for axisymmetric Navier–Stokes with swirl: identity, circulation principle, and the five-dimensional energy.* SHA-256 `eec7aa57b32a…`. Four theorems; classical unaugmented leftover open. **Do not overwrite.** |
| May 2026 Zenodo Track B PDF | [`zenodo-may/PhiRenorm_TrackB.pdf`](zenodo-may/PhiRenorm_TrackB.pdf) | Public deposit [10.5281/zenodo.20405405](https://doi.org/10.5281/zenodo.20405405). 13 524 bytes. SHA-256 `477a857f8ab4…`. Older than 22 August. 25 Aug 2026 re-upload `PhiRenorm_TrackB_May16_e075.pdf` was **duplicate** bytes; no second copy. **Not** SFE. |
| May 2026 Zenodo short TeX | [`zenodo-may/Simons_PhiRenorm_Axisymmetric.tex`](zenodo-may/Simons_PhiRenorm_Axisymmetric.tex) | Companion [10.5281/zenodo.20405597](https://doi.org/10.5281/zenodo.20405597). `\date{May 2026 \| Preprint (Track B)}`. 623 lines. SHA-256 `01c47ff4ab90…`. |
| 30 June 2026 PDF (older face) | [`Simons_PhiRenorm_Swirl_2026-06-30.pdf`](Simons_PhiRenorm_Swirl_2026-06-30.pdf) | pdfTeX CreationDate `2026-06-30`. Face date **April 2026 — Preprint**. Title *Phi-Renormalization for Axisymmetric-with-Swirl Navier–Stokes: A Conditional Reduction of Global Regularity.* 12 pages, 416 268 bytes. SHA-256 `2ca8744763cd…`. Distinct from the May Zenodo PDF and from the 22 August TeX. **Not** a compile of 22 August. Conditional on an \(\varepsilon\)-independent Gronwall bound (Open Problem 10). Unconditional swirl regularity is **not proved**. |
| Pack swirl complete TeX | [`NS_PhiRenorm_complete.tex`](NS_PhiRenorm_complete.tex) | Pack name from the lookup list. `\date{April 2026 --- Preprint}`. Same April *Conditional Reduction* title family as the 30 June PDF. 999 lines, 39 950 bytes. SHA-256 `3190b8bd45bc…`. **Older than 22 August.** Not the controlling face. |
| Track B FINAL v2 TeX | [`PhiRenorm_FINAL_v2.tex`](PhiRenorm_FINAL_v2.tex) | Uploaded as `PhiRenorm_FINAL_v2.tex_2`. `\date{June 2026 \| Preprint (Track B)}`. Title *Phi-Renormalization and Global Regularity for Axisymmetric-with-Swirl Navier–Stokes* (algebraic cancellation / Gronwall-free / prime index). 249 lines, 29 703 bytes. SHA-256 `96de5f7c2cae…`. Distinct from the May Zenodo short TeX (May date, different author line, 623 lines). Dashboard table has a **byte-corrupted** `tabular` block; keep the bytes. Status box: classical unaugmented **Open**; Clay Millennium **Not claimed**. Older than 22 August. |

## What they agree on (honest reading)

The algebraic identity \(\frac1{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\) with \(\Gamma=ru_\theta\), \(\Phi=u_\theta/r\) is the keeper. Q1 / \(\varepsilon\)-hyperdissipation smoothness is not classical unaugmented regularity. The leftover after the rewrite is control of \(u^r/r\) (or an \(\varepsilon\)-uniform Gronwall constant). That leftover is **not** Paper2’s simplex \(\|a-\mu\|_{\ell^1}\).

## Which face to use

- **Theorem paper on this branch:** 22 August TeX.
- **Public May deposit:** Zenodo `20405405` / `20405597`.
- **April/June older sources:** file them; do not compile them as 22 August; do not cash Q1 smoothness or “Gronwall-free” May/June lines as Clay.
- **Do not merge them into one claim.**
- **Drive Missing Fifteen:** `SYNTHESIS-AXISYMMETRIC-SND-BRIDGE.md` is **still missing**. Do **not** glue swirl leftover / Ring \(J/X\) / Paper2 SND. Packet [`docs/packets/MISSING-FIFTEEN-RECOVERY-AUDIT-2026-08-25.md`](../../packets/MISSING-FIFTEEN-RECOVERY-AUDIT-2026-08-25.md).
- **Equation Explorer slider `phi`:** historical toy [`docs/archive/sfe-hb/equation_explorer_simons_field.py`](../../archive/sfe-hb/equation_explorer_simons_field.py). **Not** swirl \(\Phi=u_\theta/r\). **Not** this book. **Not** live DA.
- **SFE black-hole matplotlib \(\Phi\):** Track C toy [`docs/archive/nav-42-cbfd-2026-04/sfe_black_hole_simulator_paste.py`](../../archive/nav-42-cbfd-2026-04/sfe_black_hole_simulator_paste.py). **25 Aug chat paste arrived.** **Not** swirl \(\Phi=u_\theta/r\). **Not** GR. **Not** this book. **Not** live DA.
- **April Overleaf Clay/SERPENT drafts:** **quarantine**, **not received** on this VM. **Not** the 22 August TeX. **Not** pack `NS_PhiRenorm_complete.tex` (already filed as historical). `CLAY_FINAL` / `SERPENT_FINAL` / `WHAT_I_FOUND` are **not** this book. Policy [`docs/packets/OVERLEAF-VS-PACK-AUDIT-2026-08-15.md`](../../packets/OVERLEAF-VS-PACK-AUDIT-2026-08-15.md). Receipt [`docs/archive/overleaf-2026-04/`](../../archive/overleaf-2026-04/). Clay **NOT CLAIMED**.
