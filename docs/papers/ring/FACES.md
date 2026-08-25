# Ring book has several faces. They are not a compile of 21 August.

Do **not** treat [`RingLemma_Final.tex`](RingLemma_Final.tex) as a compile of
[`02_ring_lemma_snd_conditional.pdf`](02_ring_lemma_snd_conditional.pdf).
Do **not** overwrite that PDF.
Do **not** glue Ring SND to Paper2 operator-norm SND.
Do **not** treat this book as Clay, swirl \(\Phi\), or Paper2 FIXED.tex.

**Usable Ring SND** on this branch remains \(\inf J(t)/X(t)\ge c_*>0\).
Unconditional SND for arbitrary large \(H^1\) data is **OPEN**. Clay is
**NOT CLAIMED**. DA-VC-01 still **FAIL**.

| Face | File | What it is |
|---|---|---|
| Controlling public PDF (21 August 2026) | [`02_ring_lemma_snd_conditional.pdf`](02_ring_lemma_snd_conditional.pdf) | Zenodo [10.5281/zenodo.22050976](https://doi.org/10.5281/zenodo.22050976). Title *A Ring Lemma for Band-Limited Vorticity Direction and a Conditional Spectral Non-Dispersal Criterion on the Three-Dimensional Torus.* Face date **Corrected preprint — August 2026**. pdfTeX CreationDate `2026-08-20`. 3 pages, 241 673 bytes. SHA-256 `0304f039406c…`. SND here is \(\inf J/X\ge c_*\). Remark 1.2: an upper-bound companion \(\sup_j a_j\le\rho_0\) is **related but not identical**; this PDF freezes the lower-bound form. **Do not overwrite.** **Not** a Clay claim. **Not** the June FIXED PDF. |
| April / June-era TeX | [`RingLemma_Final.tex`](RingLemma_Final.tex) | Base44 download `492e0654f_RingLemma_Final.tex` (HTTP 200, 25 Aug 2026). Title *Borromean Triads, the Ring Lemma, and Spectral Non-Dispersal.* `\date{April 2026 \| Preprint}`. 448 lines, 21 216 bytes. SHA-256 `4602065ef68a…`. Standalone Ring lemma + augmented \(Q_1,Q_3,Q_6\) framework. **June 20-ish source** (drop name); face date is **April 2026**. Labels `lem:ring`, `cor:CF`, `lem:gsl`, `prop:H1`, `thm:main` (**augmented** NS). **No** `lem:triad_bound_formal`, `eq:triad_bound_result`, `prop:CF_integrability`, `E_{\min}`, `thm:CF93_theorem`. **Not** a compile of the 21 Aug Zenodo PDF (proved: different titles, April vs August face dates, PDF created 2026-08-20). **Not** the same bytes as the June 19 pack TeX. **Not** `Paper2_NS_Regularity_SND_FIXED.tex`. **Not** Clay. |
| June 19 pack TeX | [`RingLemma_Simons_June19_2026.tex`](RingLemma_Simons_June19_2026.tex) | Mac `…/07_zenodo_final_pack_2026-08-15/NS/c8a03f315_RingLemma_Simons_June19_2026.tex` was **not readable** here. Bytes fetched 25 Aug 2026 from Base44 `https://base44.app/api/apps/69b28657b0df374441f0302e/files/mp/public/69b28657b0df374441f0302e/c8a03f315_RingLemma_Simons_June19_2026.tex` (HTTP **302** then **200**; 44 368 bytes). Bare name `RingLemma_Simons_June19_2026.tex` on the same app is HTTP **302** then CDN **403**, 0 bytes — hash-prefix is the public object. Filename is an **untrusted alias**; identify from title + `\date` + SHA-256 only. Title still *Borromean Triads, the Ring Lemma, and Spectral Non-Dispersal.* `\date{June 19, 2026}`. Footer still says May 2026. 887 lines (`wc -l`). SHA-256 `a73d949f51a122ada93d6341926990991f7fd04e6cd5146a79b27d3d4ca99961`. **Not** the same bytes as [`RingLemma_Final.tex`](RingLemma_Final.tex) (`4602065ef68a…`, 21 216 bytes, April date). Same SND1–4 + \(\rho=J/X\); extra RH/zeta/\(Q_6\) “spacetime” sections. **No** \(\kappa_j\). Dashboard: Main Theorem is **augmented** NS; dynamical [SND] for *classical* NS is **Open**; unconditional classical regularity is **Not claimed**. **Not** the \(\kappa\)-SND / \(E_{\min}\) / unaugmented `thm:main` paste. **Not** a compile of the 21 Aug PDF (`0304f039…`; **not overwritten**). **Not** Clay. **Not** FIXED.tex. Hash-prefix name **not re-filed** as a second copy. Drive offered `RingLemma_Final.tex` as stand-in — **REJECT as identity**. Packet [`docs/packets/MISSING-FIFTEEN-RECOVERY-AUDIT-2026-08-25.md`](../../packets/MISSING-FIFTEEN-RECOVERY-AUDIT-2026-08-25.md). |
| Unaugmented \(\kappa\)-SND / CF93 / BKM tail | [`KAPPA-SND-CF-BKM-FRAGMENT.md`](KAPPA-SND-CF-BKM-FRAGMENT.md) | Chat paste only (starts mid-document after `\end{equation}`). Unique labels **absent** from every filed Ring/Paper2 source. Full TeX **not received** — do not invent a preamble. **CONDITIONAL.** Clay **NOT CLAIMED.** |

## SND definitions (do not merge; naming collision)

- **21 Aug PDF (usable):** \(\inf_t J(t)/X(t)\ge c_*>0\). Dominant Littlewood–Paley shell of **enstrophy**. Lower bound.
- **April / June 19 TeX:** Definition [SND] is four shell-energy clauses (SND1–4). The Shell-Spread Poincaré inequality still writes \(\rho=J(t)/X(t)\). Dashboard: dynamical [SND] for *classical* NS is **Open**; unconditional classical regularity is **Not claimed**.
- **Pasted \(\kappa\)-SND (not usable here):** \(\kappa_j(t)=E_j/E\le\kappa^*<1\). Upper bound on shell **energy** fraction (non-concentration style). The manuscript still calls this Spectral Non-Dispersal. **Collision:** that name is used for a lower bound on enstrophy concentration in the public PDF. Do not “fix” the paper. Do **not** glue \(\kappa\)-SND to \(J/X\).
- **Paper2:** \(\|H_N[a]-\widehat H_N^\mu\|_{\mathrm{op}}\). Do not identify any of the above with this.

Do not replace the usable criterion with SND1–4 or with \(\kappa_j\le\kappa^*\).

## \(E_{\min}\) flag (FACES/map only — not a live DA proof)

The pasted CF93 step uses \(E_{\min}:=\inf E_{j^*(t)}>0\) as if it were free.
That lower bound is **not** implied by \(\kappa_j\le\kappa^*\). Do **not**
declare CF closed for Clay. Live DA must **not** import this as Spe /
`TRANSFORMABLE` without a real structure map \(T\).

The CF/BKM bootstrap that then claims unaugmented global \(C^\infty\) on
\(\mathbb{T}^3\) is **conditional** on those hypotheses. It is **not** Clay.

## What they agree on (honest reading)

Ring Lemma: on a single LP shell, \(\|\nabla\xi\|_{L^\infty}\) is controlled by shell frequency, not by vorticity amplitude. Conditional \(H^1\) under an SND hypothesis. Unconditional SND for large \(H^1\) remains **open**. No Clay claim. The ring face is not a Clay claim and not the June FIXED PDF.

## Which face to use

- **Public / usable SND:** 21 August Zenodo PDF. Do not overwrite.
- **April / June-era source:** `RingLemma_Final.tex`. File it; do not compile it as the 21 Aug PDF; do not cash the augmented Main Theorem as Clay.
- **June 19 pack TeX:** filed. Same augmented book; still **not** Clay. Drive `RingLemma_Final.tex` stand-in is **REJECT as identity** (SHA/size differ).
- **Drive Missing Fifteen:** `c8a03f315_` is already this June 19 file. Do not re-file Final as June 19. Packet [`docs/packets/MISSING-FIFTEEN-RECOVERY-AUDIT-2026-08-25.md`](../../packets/MISSING-FIFTEEN-RECOVERY-AUDIT-2026-08-25.md).
- **\(\kappa\)-SND / \(E_{\min}\) / unaugmented CF–BKM tail:** classification note only. Not a complete source. Not live DA.
- **Do not merge them into one claim.**
- **Equation Explorer matplotlib paste:** historical toy [`docs/archive/sfe-hb/equation_explorer_simons_field.py`](../../archive/sfe-hb/equation_explorer_simons_field.py). **Not** Ring SND. **Not** this book. **Not** live DA.
- **SFE black-hole matplotlib paste:** Track C toy [`docs/archive/nav-42-cbfd-2026-04/sfe_black_hole_simulator_paste.py`](../../archive/nav-42-cbfd-2026-04/sfe_black_hole_simulator_paste.py). **25 Aug chat paste arrived.** **Not** Ring SND. **Not** \(\inf J/X\). **Not** this book. **Not** live DA.
- **April Overleaf Clay/SERPENT/WHAT_I_FOUND Ring-as-section:** **not received.** Those trees (`CLAY_FINAL`, `SERPENT_FINAL`, `WHAT_I_FOUND`) are **not** the June 19 pack TeX (`a73d949f…` / `c8a03f315_…`) and **not** a compile of the 21 Aug PDF. Policy [`docs/packets/OVERLEAF-VS-PACK-AUDIT-2026-08-15.md`](../../packets/OVERLEAF-VS-PACK-AUDIT-2026-08-15.md). Receipt [`docs/archive/overleaf-2026-04/`](../../archive/overleaf-2026-04/). \(\kappa\)-SND \(\neq\) \(J/X\). Clay **NOT CLAIMED**.
- **April 2026 NAV-42 / CBFD / \(A_3\) Grok dump:** archive [`docs/archive/nav-42-cbfd-2026-04/`](../../archive/nav-42-cbfd-2026-04/). \(A_3\) is **not** Ring \(J=\max_j X_j\) and **not** \(\inf J/X\). RingLemma footers that say “NAV-42 Patent Pending” are **branding**, not that dump and not a compile of \(A_3\). **Not** Clay.

Zenodo [10.5281/zenodo.20269536](https://doi.org/10.5281/zenodo.20269536) is a superseded **Paper2** May 18 TeX (SHA `f51ed5c05ec3…`), not this Ring book. Its status note points at `22045474` as a “corrected version”; that DOI is Ring (`02_ring_lemma_snd_conditional.pdf`), not a Paper2 FIXED repair. Do not glue them.
