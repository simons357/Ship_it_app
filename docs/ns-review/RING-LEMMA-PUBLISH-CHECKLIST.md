# Ring Lemma — publish checklist

**Question:** Should Jonathan publish the Ring Lemma?  
**Answer:** **YES** — as a **short spatial geometry note**, after the edits below.  
**Not:** as an NS / PDE / Clay paper. Ring is spatial-only; the classical unaugmented close gate remains \(T_{j\leftarrow j}\) / C10 \(\alpha_+\) / PRODUCT-BLOCK (see [`../campaign/NSE-VISUAL-PROGRESS.md`](../campaign/NSE-VISUAL-PROGRESS.md)).

**Geometric SoT:** Oct 2 corrected note — on recon tip:  
`docs/ns-review/ring-lemma/RingLemma_Corrected_Geometric_Note_2026-10-02.tex`  
(also Jonathan upload `RingLemma_Corrected_Geometric_Note_2026-10-02_f623.tex`).

**Archive only (do not publish as current geometry):**  
`RingLemma_Simons_June19_2026.tex` — June linear \(2^{j^*}\) bound on \(E_c\) **superseded / withdrawn**; Bernstein gap + sharpness.

**Governing recon:** `RING-LEMMA-RECONCILIATION-2026-10.md` on `cursor/ring-lemma-recon-0cc5` (PR #160).

---

## Verdict box

| | |
| --- | --- |
| **Publish?** | **YES** — short **spatial geometry** note |
| **Edit first?** | **MUST** — strip PDE / NS / Clay claims; point at Oct 2 corrected note |
| **Channels** | Zenodo (geometry deposit) and/or Substack (plain-language companion) — after checklist green |
| **Must not** | Clay trophy language · “Ring ⇒ regularity” · June 19 as SoT · SND as proved for classical |

---

## What may be claimed (RL-G1…G3)

Publish only what the Oct 2 note proves for **band-limited** vorticity on \(\mathbb{T}^3\):

| ID | Claim | Status |
| --- | --- | --- |
| **RL-G1** | On \(E_c=\{|\omega|\ge c\|\omega\|_2\}\): \(\|\nabla\xi\|_{L^\infty(E_c)}\le (C/c)\,L^{5/2}\) | **PROVED** — publish |
| **RL-G2** | Sharpness: order \(L^{5/2}\) on \(E_{1/2}\) (fixed \(c<1\)); uniform \(CL\) on fixed-\(c\) \(E_c\) **false** | **PROVED** — publish |
| **RL-G3** | Peak set \(F_a\): order \(L\); or on \(E_c\) under amplitude ratio \(A=\|\omega\|_\infty/\|\omega\|_2\) | **PROVED** — publish (spatial / amplitude-conditioned) |
| **RL-G4** | Dynamical amplitude control + PDE regularity consequence | **OPEN** — do **not** claim |

Title / abstract framing examples that stay honest:

- “A sharp band-limited bound on vorticity-direction gradients”
- “Spatial geometry of \(\nabla\xi\) on frequency-localized fields”

Avoid titles that say Navier–Stokes, regularity, Millennium, or Clay.

---

## MUST strip before Zenodo / Substack

Edit the public face (new short note derived from Oct 2 — or a ruthlessly cut Oct 2) until every row below is gone or explicitly marked open / not claimed.

| Strip / refuse | Why |
| --- | --- |
| Any **PDE evolution** / “preserved under NS” claim | Oct 2 Remark refuses dynamical consequence |
| **Classical regularity** / Statement B / Clay / Millennium | Never implied by spatial Ring |
| **“Ring ⇒ CF / Beale–Kato–Majda close”** without matching exact hypotheses + dynamics | Overclaim even with corrected power |
| June 19 dashboard: Main Theorem / CF closes / “only gap is dynamical SND” | Superseded packaging; dangerous |
| June **linear** \(\|\nabla\xi\|\lesssim 2^{j^*}\) on \(E_c\) | **False** — use \(L^{5/2}\) + sharpness |
| **SND proved** for classical Leray–Hopf | NS-10 **OPEN**; SND = conditional texture |
| **Augmented \(Q\)-program** as proved dissipation / de-augmentation bridge | Separate book; recon flags sign/gaps |
| **Zeta-clock / RH / prime spacetime** as fluid proof | Not PDE; do not import |
| **HH / \(N=32\) / IPR numerics ⇒ theorem** | Numerics ≠ proof |
| July **NS-6 three-shell \(H_N\)** claimed via vorticity Ring | Different object — leave SOURCE MISSING / OPEN |
| Prize / trophy / “we’re first” framing | Reputation lock — map the geometry, don’t billboard |

Keep the Oct 2 note’s own honesty Remark (frequency localization alone ⇒ \(A\lesssim L^{3/2}\); single-shell support not generally nonlinear-invariant; no PDE conclusion without a geometric criterion’s exact hypotheses).

---

## Edit list (do these, then deposit)

### A. Manuscript (Zenodo-ready TeX)

1. **Start from** `RingLemma_Corrected_Geometric_Note_2026-10-02.tex` — not June 19.
2. **Title + abstract:** spatial / band-limited / sharp; zero NS-solved vocabulary.
3. **Body:** Props 1–3 (RL-G1…G3) + sharpness family; keep proofs tight.
4. **Explicit non-claims section** (short): no dynamical preservation; no regularity theorem; no Clay.
5. **Remove or footnote** any leftover June narrative, CF corollary, SND “only gap,” augmented Main Theorem.
6. **Notation:** \(\xi=\omega/|\omega|\), \(E_c\), \(L\) (band limit), \(F_a\) — match Oct 2.
7. **Bibliography:** geometric / Fourier analysis refs; do not cite withdrawn Clay packaging DOIs as support.
8. **Compile clean** once; one PDF face only for the deposit.

### B. Substack / public prose (optional companion)

1. One plain-language piece: “what \(\nabla\xi\) means,” “why \(5/2\),” “why amplitude buys linearity.”
2. Link the Zenodo PDF; say this is **geometry**, not a fluid-existence proof.
3. Point readers who care about the NSE map to [`../campaign/NSE-VISUAL-PROGRESS.md`](../campaign/NSE-VISUAL-PROGRESS.md) — live gate named there.
4. No prize framing. Captain Obvious welcome: spatial lemma ≠ time-dependent close.

### C. Ledger / house alignment (repo, not the paper)

1. Keep **NS-6a** = RL-G1…G3 **PROVED (spatial, scoped)**; **NS-6b** three-shell \(H_N\) **OPEN / SOURCE MISSING**.
2. Keep **NS-10 OPEN**, **NS-11 NOT CLAIMED**.
3. Do not green PRODUCT-BLOCK or \(T_{j\leftarrow j}\) because Ring published.

### D. Final gate before hit Publish

- [ ] Abstract has no PDE close / Clay words  
- [ ] June linear bound nowhere as current claim  
- [ ] RL-G4 / dynamics marked open or absent  
- [ ] Oct 2 is the cited geometric authority  
- [ ] Progress board still shows classical gate **OPEN**  
- [ ] Zenodo metadata: geometry keywords; not “Millennium” / “Clay problem solved”

---

## One-liner for Jonathan

**Publish yes — short spatial geometry note after edits; strip PDE/NS/Clay; Oct 2 is SoT; classical gate stays \(T_{j\leftarrow j}\) / C10 / PRODUCT-BLOCK.**
