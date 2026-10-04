# NSE visual progress board

**Audience:** Jonathan — one glance at where the Navier–Stokes study stands.  
**Tone:** friendly host / map guide. **Captain Obvious** here is the old commercial joke (“it was so obvious…”), not shade.  
**Base tip:** branched from `cursor/visual-ns-book-0cc5` (campaign + visual assets).  
**Companions:** [`REPUTATION-LOCK.md`](./REPUTATION-LOCK.md) · [`HOUSE-OF-NS.md`](./HOUSE-OF-NS.md) · [`VISUAL-NS-BOOK/`](./VISUAL-NS-BOOK/) · [`../ns-review/UNAUG-PROOF-CHAIN.md`](../ns-review/UNAUG-PROOF-CHAIN.md) · Ring publish checklist [`../ns-review/RING-LEMMA-PUBLISH-CHECKLIST.md`](../ns-review/RING-LEMMA-PUBLISH-CHECKLIST.md)

**No Clay trophy language.** No Millennium prize framing, no “we won / we lost,” no Statement-B billboard. We’re mapping the house. We’re at the door. We’re not claiming we opened it.

---

## What gate are we at now?

| | |
| --- | --- |
| **NOW** | **Spatial Ring: DONE · Classical unaugmented close gate: \(T_{j\leftarrow j}\) / C10 (\(\alpha_+\)) still OPEN** |

**Context (locked):** Ring is **spatial-only** (RL-G1…G3 on band-limited vorticity direction). It does **not** close the classical unaugmented face. The live gate remains:

\[
T_{j\leftarrow j}\quad/\quad\text{C10 }\alpha_+\quad/\quad\text{PRODUCT-BLOCK }
(\sup\mathcal{R}_\star).
\]

NS-10 dynamic SND stays **OPEN** as conditional texture — not a classical close by itself.

---

## DONE

Locked wins and honest kills. Green means “settled on the map,” not “Clay.”

| Item | What it is | Where |
| --- | --- | --- |
| **Spectral-shift identity** | Bookkeeping \(\Lambda'=2(T_c-\nu D_s)/X\) (and shell Door-1 partition). Algebra only — **≠** Lemma★ bound | [`../ns-review/UNAUG-PROOF-CHAIN.md`](../ns-review/UNAUG-PROOF-CHAIN.md) · [`../ns-review/PROOF-CHAIN-CLEAN.md`](../ns-review/PROOF-CHAIN-CLEAN.md) |
| **Ring spatial RL-G1…G3** | Band-limited \(\|\nabla\xi\|_{L^\infty(E_c)}\lesssim L^{5/2}/c\); sharpness; peak / amplitude-conditioned linear-in-\(L\) | Oct 2 note (see publish checklist); recon on `cursor/ring-lemma-recon-0cc5` |
| **L3 shear energy-only kill** | Exact parallel shears kill universal / energy-only \(S3\) strengthening; L3-5 datum-sensitive still **OPEN** | `docs/ns-review/L3-SHEAR-OBSTRUCTION-2026-10.md` (sibling branch) |
| **Candidate kills C1–C5** | Energy+viscosity \(R\); centrifugal-only leftover; circular Gronwall; numerics⇒depletion; pure-swirl as class bound | `TJ-SAME-SCALE-CANDIDATES.md` (tj-candidates tip) |
| **\(\alpha_+\) conditional hinge** | Absolute \(\alpha_+\) **not seated**; Sobolev escape; C6 survives only as **conditional / geometric** TRY | `ALPHA-PLUS-DEPLETION.md` (alpha-plus tip) |
| **Visual NS book** | Skool + Substack curriculum; map not proof | [`VISUAL-NS-BOOK/`](./VISUAL-NS-BOOK/) |
| **Proof-chain visuals** | Floor-plan figures, captions, one-pager | [`../ns-review/visual-journey/`](../ns-review/visual-journey/) |
| **Cosmic GRAFITTI (NSE-relevant)** | Phone/wall face of the **swirl leftover** magazine — occupation/alignment as graffiti; **not** a regularity proof | `apps/cosmic-grafitti/` on cosmic-grafitti tips; archive note `COSMIC-GRAFITTI-FOUND.md` |
| **Claim ledger fixes** | July overclaim surgery (NS-4/6/9 scope; NS-10 map; NS-11 not claimed) | claim-ledger / ring-lemma recon tips |
| **Unaugmented honesty lock** | Five-paragraph lock: identity ≠ ★; \(\rho_j<\nu\) lives in (A); cross-scale not supplied; \(T_{j\leftarrow j}\) OPEN; numerics ≠ depletion | [`../ns-review/UNAUG-PROOF-CHAIN.md`](../ns-review/UNAUG-PROOF-CHAIN.md) |
| **Φ-renorm KEEP** | Swirl identity kept; \(\|u^r/r\|_\infty\) barrier **OPEN**; conditional reduction only | [`../ns-review/PHI-RENORM-WHAT-IS-KEPT.md`](../ns-review/PHI-RENORM-WHAT-IS-KEPT.md) |
| **Reputation / house map** | Public face = floor plan + barycenter + door; no prize stamps | [`REPUTATION-LOCK.md`](./REPUTATION-LOCK.md) · [`HOUSE-OF-NS.md`](./HOUSE-OF-NS.md) |

---

## LIVE GATES

Still open. These are the doors, named as math objects.

| Gate | Object | Status |
| --- | --- | --- |
| **\(T_{j\leftarrow j}\)** | Same-scale shell transfer on the unaugmented face | **OPEN** — principal classical remainder |
| **C10 \(\alpha_+\) / depletion ⇒ (A)** | Non-circular depletion that implies (A), or geometric \(\alpha_+\) control (C6 hinge) | **OPEN** — principal live TRY |
| **C7 HH** | High×high / near-shell product channel for local transfer / \(T_c\) | **OPEN** — live bottleneck; energy-only HH dead |
| **PRODUCT-BLOCK / uniform \(\mathcal{R}_\star\)** | \(\sup_v\mathcal{R}_\star(v)<\infty\) — Lemma★ last door | **OPEN** — hypothesis, not theorem |
| **NS-10 dynamic SND** | Dynamical shell-concentration preservation for classical Leray–Hopf | **OPEN** — conditional texture (C12); not a solo close |

**Captain Obvious (friendly):** if Ring is spatial-only, of course the live classical gate is still \(T_{j\leftarrow j}\) / C10 / PRODUCT-BLOCK. Naming that out loud keeps the board honest.

**Not a live “we’re almost done” gate:** Clay Statement B / full regularity — **not claimed**, not on this board as a trophy to chase in public copy.

---

## APPS / TOOLS built for NSE

Paths relative to repo root. Built to map, probe, and refuse illegal glue — not to stamp a prize.

| App / tool | Path | Role |
| --- | --- | --- |
| **Visual NS Book** | `docs/campaign/VISUAL-NS-BOOK/` | Skool/Substack visual curriculum (map, not proof) |
| **Proof-chain visual journey** | `docs/ns-review/visual-journey/` · generator `scripts/visual_journey/` | Chain figures, captions, one-pager |
| **Campaign house / feed** | `docs/campaign/` (`HOUSE-OF-NS.md`, `PROOF-JOURNEY.md`, `FEED*.md`) | Plain-language map + daily posts |
| **`ns_attacks` probes** | `scripts/ns_attacks/` | Five-lane / HH / near-shell / product-bound / Lemma★ core; TJ & \(\alpha_+\) probes on sibling tips |
| **Domain Architect** | `domain_architect/` · `docs/domain-architect/` · `data/domain_architect/` | Structural checker; refuse illegal glue (SFE→NS/Clay, etc.) |
| **Cosmic GRAFITTI** | `apps/cosmic-grafitti/` (on cosmic-grafitti tips) | Swirl-leftover magazine wall; NSE-adjacent storytelling, not a close |
| **Lemma-campaign art shelf** | `docs/ns-review/assets/lemma-campaign/` | Shared heroes for book + journey |
| **Scientific face** | `docs/ns-review/SCIENTIFIC-REPORT.md` · `PROOF-CHAIN-CLEAN.md` · `UNAUG-PROOF-CHAIN.md` | Specialist honesty cards |

---

## Pictures index

Existing art — reuse; do not stamp verdicts on heroes.

### Lemma-campaign shelf

`docs/ns-review/assets/lemma-campaign/`

| File | Role |
| --- | --- |
| `lemma-star-barycenter.png` | Spectral barycenter — where we are |
| `00-barycenter-map.png` / `00-barycenter-map-alt.png` | Alternate barycenter crops |
| `03-tug-of-war-stretch-vs-spread.png` | \(T_c\) vs \(D_s\) |
| `02-shape-ne-size.png` / `02b-shape-not-size-hero.png` | Shape ≠ size |
| `06-viscosity-melts-wrapper.png` | Viscosity wrapper |
| `fig_star_david_ring_lemma.png` | Ring / triad geometry |
| `fig_three_spheres.png` | Nested shells |
| `t3_torus_shape_render.png` | \(\mathbb{T}^3\) atmosphere |
| `amp_ratios_triad.png` | Triad amplitude diagnostic |
| `attack5_bounds.png` | Finite-sample ratio drill |
| `IMAGE-INVENTORY.md` | Captions / reuse rules |

### Proof-chain visual pack

`docs/ns-review/visual-journey/`

| Path | Role |
| --- | --- |
| `figures/proof-chain.png` / `.svg` / `.mmd` | House floor-plan chain |
| `figures/chain-status-card.png` | Status card (open doors labeled as math) |
| `proof-chain-onepager.pdf` / `.tex` | One-pager |
| `CAPTIONS.md` · `README.md` | How to read |

### Visual NS Book

`docs/campaign/VISUAL-NS-BOOK/` — [`IMAGE-INVENTORY.md`](./VISUAL-NS-BOOK/IMAGE-INVENTORY.md) · [`SEQUENCE.md`](./VISUAL-NS-BOOK/SEQUENCE.md) · `chapters/`

---

## Honesty locks (quick strip)

| Lock | One line |
| --- | --- |
| Spectral-shift ≠ Lemma★ | Identity is bookkeeping; not a ratio bound |
| Numerics ≠ depletion | Occupancy / alignment samples do not imply (A) |
| Ring ≠ classical close | Spatial RL-G1…G3; RL-G4 / PDE consequence **OPEN** |
| SND = texture | C12 conditional; NS-10 **OPEN** |
| Φ barrier open | \(\|u^r/r\|_\infty\) uniform-in-\(\varepsilon\) still open |
| No Clay | Statement B / Millennium **not claimed** on any face |

---

## Ring publish? (pointer)

**Yes — as a short spatial geometry note, after edits.**  
Full edit list and strip rules: [`../ns-review/RING-LEMMA-PUBLISH-CHECKLIST.md`](../ns-review/RING-LEMMA-PUBLISH-CHECKLIST.md).  
SoT geometry: Oct 2 corrected note. Strip PDE / NS / Clay claims before Zenodo or Substack.

---

## Exit line (locked)

**Spatial Ring: DONE. Classical unaugmented close: still the named gate — \(T_{j\leftarrow j}\) / C10 (\(\alpha_+\)) / PRODUCT-BLOCK. No Clay trophy.**
