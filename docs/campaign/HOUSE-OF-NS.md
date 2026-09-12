# The house of Navier–Stokes

A caring, plain-language face for the journey.  
**Not a claim that NS is solved.** A claim that we know **where we are**.

Navier–Stokes is a house. Below is the map of **what our study has revealed so far** — rooms we can name, doors we can describe, wings we keep separate. Nothing more is drawn than the work supports.

---

## The picture in words

We’re not in *every* room yet.  
Some floors are still for specialists.  
We know where we stand: **at the door of this floor** — the spectral **barycenter**, the center of mass of the energy in frequency space.

Here is **how the room looks**.  
Here is **how it behaves**.  
Here is **how you go through the door** (the estimate that still has to be closed).  

Pictures first. Math one click away. If you don’t want depth, keep walking. If you do — the map is lit.

---

## What “this room” is (technical, still kind)

On the 3-torus, a smooth divergence-free field has an enstrophy-weighted mean frequency:

\[
\Lambda = Y/X.
\]

That \(\Lambda\) is the **barycenter**. Relative to it we keep score of:

- **spread** \(D_s\) — how far the energy sits from the center  
- **centered stretch** \(T_c\) — the cascade measured about \(\Lambda\), not about zero  
- **shape score** \(\mathcal{R}_\star = (T_c)_+^2/(D_s\, E\, Y)\) — tug-of-war at that center  

**Being in the room** = the bookkeeping is correctly centered there.  
**The last door on this floor** = prove the shape score stays finite for every smooth field: \(\sup_v\mathcal{R}_\star(v)<\infty\) (geometry-only constant). That is what would freeze blowup of \(\Lambda(t)\) in this packaging.  
**Upstairs** = full regularity / Clay packaging — mapped as open territory, not claimed as finished.

---

## Floor plan (what the study has mapped)

Drawn only from definitions, identities, probes, and honesty locks in the scientific face. Status words mean what they say.

### Ground floor — classical entry

| Room | What the study shows | Status |
| --- | --- | --- |
| Front door / setting | Smooth mean-zero divergence-free velocity on \(\mathbb{T}^3\) | Mapped |
| Projector closet | Leray projector \(P\), Stokes operator \(A=-P\Delta\), bilinear \(B(v,v)\) | Mapped |
| Viscosity dial | \(\nu>0\) in the classical NSE | Mapped |

### First floor — spectral bookkeeping (where we stand)

| Room | What the study shows | Status |
| --- | --- | --- |
| Moment hall | \(E=\|v\|_2^2\), \(X=\|A^{1/2}v\|_2^2\), \(Y=\|Av\|_2^2\), \(Z=\|A^{3/2}v\|_2^2\) | Mapped (definitions) |
| Barycenter room | \(\Lambda=Y/X\) (enstrophy-weighted mean eigenvalue) | Mapped — **we are here** |
| Spread alcove | \(D_s=Z-\Lambda Y=\|(A-\Lambda)A^{1/2}v\|_2^2\ge 0\) | Mapped (algebra) |
| Stretch alcove | \(T_c=M-\Lambda N=-\langle B(v,v),A(A-\Lambda)v\rangle\) | Mapped (definition) |
| Clock identity | Along strong solutions: \(\Lambda'=2(T_c-\nu D_s)/X\) | Mapped (algebra) |
| Single-shell niche | One shell ⇒ \(D_s=0\) and \(T_c=0\) (shape score vacuous) | Mapped |
| Shape-score desk | \(\mathcal{R}_\star=(T_c)_+^2/(D_s E Y)\); amplitude- and dilation-invariant | Mapped (definition) |

### Same floor — packaging and the last door

| Room | What the study shows | Status |
| --- | --- | --- |
| Lemma★ packaging room | Shape form / Young energy-budget form of ★ | **Hypothesis** — not a theorem |
| Young wrapper shelf | \(T_c\le\theta\nu D_s+C_0(\theta)\nu^{-1} E Y\) as bookkeeping | Mapped as wrapper; \(C_0\) open |
| **Last door (this floor)** | PRODUCT-BLOCK: \(\sup_v\mathcal{R}_\star<\infty\); live stress = high×high triad channel | **Open estimate** |
| False-key bin | Universal \(|T_c|\le C\|v\|_2 X^{3/2}\) | **Retired** (wrong scaling) |
| Continuation stair | If ★ holds ⇒ Gronwall on \(\Lambda\) ⇒ continuation | Mapped **as implication only** |

### Diagnostic closet (five-lane / probes — stress tests, not proofs)

| Drawer | What probes say | Status |
| --- | --- | --- |
| Pure viscous absorption (\(K=0\)) | \(T_c\le\theta\nu D_s\) alone | **Dead** (amplitude scaling) |
| Uniform \(\mathcal{R}_\star\) | Survives kill on tested families | **Open** ≠ proved |
| HH input channel | Flagged as live bottleneck for \(T_c\) | **Gap (live)** |
| Near-shell \(K_{\alpha,\beta}\) | Restricted laboratory | Probe only |
| Kill search | Families with \(\mathcal{R}_\star\to\infty\) | Lane still live |

Reproducible scripts: `scripts/ns_attacks/` (`ns_lemma_star_core.py`, `product_bound_probe.py`, five-lane attacks).

### Upper floor — Clay packaging

| Room | Status |
| --- | --- |
| Statement B / full regularity announcement | **Not claimed** — upstairs is drawn, not occupied |

### Side wing — Φ / swirl (separate house wing)

| Room | What the study shows | Status |
| --- | --- | --- |
| Swirl identity KEEP | \(\partial_z(\Gamma^2)/r^4=\partial_z(\Phi^2)\) | Mapped (algebra) |
| Φ wing door | \(\int\|u^r/r\|_\infty\,dt\) uniform | **Separate open door** |
| Glue to Lemma★ | — | **Refuse** (incompatible books) |

### Basement / archive (do not reopen as live Clay paths)

| Shelf | Disposition |
| --- | --- |
| SFE ↔ NS glue | Incompatible / refuse |
| RH / ARCHON as Clay vehicle | Parked |
| SND / Ring as unconditional Statement B | Parked (conditional texture only) |
| Numeric survival as theorem | Refuse |

---

## Picture → room index

| Picture | Room it lights |
| --- | --- |
| `../ns-review/visual-journey/figures/proof-chain.png` | Whole floor plan (dashed = open doors) |
| `../ns-review/visual-journey/figures/chain-status-card.png` | Status strip for the same plan |
| `../ns-review/visual-journey/assets/lemma-star-barycenter.png` | Barycenter room (this floor) |
| `../ns-review/visual-journey/assets/03-tug-of-war-stretch-vs-spread.png` | Shape-score desk |
| `../ns-review/visual-journey/assets/02-shape-ne-size.png` | Amplitude / dilation invariance |
| `../ns-review/visual-journey/assets/06-viscosity-melts-wrapper.png` | Young wrapper shelf |
| `../ns-review/visual-journey/assets/t3_torus_shape_render.png` | Entry object (velocity on \(\mathbb{T}^3\)) |
| `../ns-review/visual-journey/assets/fig_three_spheres.png` | Shell nesting vocabulary |
| `../ns-review/visual-journey/assets/fig_star_david_ring_lemma.png` | Optional SND / triad atmosphere (not the last door) |

---

## What we show (no trophy line)

| Show | Meaning |
| --- | --- |
| Chain map | Whole layout of the house we’ve mapped |
| Barycenter figure | “This room” — stretch vs spread at \(\Lambda\) |
| Open dashed node | The last door — named as math, not shame |
| Φ / swirl wing | Another wing; its own door \(\|u^r/r\|_\infty\) |
| KEEP shelf | Rooms we stand behind |
| Archive shelf | Earlier furniture moved to storage |

---

## The last door — where it is, how to approach it (legal only)

**Where:** on this floor, after the barycenter bookkeeping, before the continuation stair. Math name: **PRODUCT-BLOCK** = \(\sup_v\mathcal{R}_\star<\infty\).

**Legal directions** (estimates and structure — the only way through):

1. Prove \(\mathcal{R}_\star\) is uniformly bounded with a geometry-only constant, **or** an equivalent Young energy-budget form with geometric \(C_0\).  
2. Hunt cancellations in \(T_c=M-\Lambda N\); budget the **high×high** triad channel separately if HL/LL are classical.  
3. Honest conditional papers (★ under an explicit HH / shell hypothesis) are allowed — labeled conditional, not Clay.  
4. Searching for a family with \(\mathcal{R}_\star\to\infty\) is also legal: that would show this door cannot open this way.  
5. Ordinary energy-only 3D products are not enough. The old universal \(|T_c|\le C\|v\|_2 X^{3/2}\) target is **false** (wrong scaling) — do not use it.  
6. No slogan, no glue from SFE, no numeric “we survived so far” as a key.

Scientific write-up: [`../ns-review/SCIENTIFIC-REPORT.md`](../ns-review/SCIENTIFIC-REPORT.md) §4.  
Until the estimate closes: leave the door described and open as math.

---

## Caring rules for posts

- Lead with a picture.  
- Speak like a host: “here’s the room,” not “we won the building.”  
- Never punch at other people or labs.  
- Mistakes live under the rug (errata in descriptions), not painted on the front door.  
- Specialists who hear the upstairs floorboards will know what the dashed node means.  
- Draw only what the study supports; blank rooms stay blank until the math fills them.

**Entry:** [`PROOF-JOURNEY.md`](./PROOF-JOURNEY.md)  
**Monday hero:** `../ns-review/visual-journey/figures/proof-chain.png`  
**This room:** `../ns-review/visual-journey/assets/lemma-star-barycenter.png`
