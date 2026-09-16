# Same-scale transfer \(T_{j\leftarrow j}\) — attack candidates

**Date:** 2026-09-16  
**Face:** unaugmented 3D NS shell budget (axisymmetric restriction labeled where used).  
**Honesty lock:** [`UNAUG-PROOF-CHAIN.md`](./UNAUG-PROOF-CHAIN.md) · companions [`PROOF-CHAIN-CLEAN.md`](./PROOF-CHAIN-CLEAN.md), [`SCIENTIFIC-REPORT.md`](./SCIENTIFIC-REPORT.md).  
**Finished (this chat):** honesty lock + diagnostics + conditional Gronwall packaging — **not** a proof.  
**Finished (as a proof):** still need a real handle on \(T_{j\leftarrow j}\) (and a path to (A) that is not circular) — **NOT done. NS / Clay B not solved.**

**Forbidden recycling:** do **not** bound \(T_{j\leftarrow j}\) by \(\dot e_j\), \(\dot Z\), \(\dot Z_j\), or \(\Lambda'\). Spectral-shift identity ≠ Lemma★. Occupancy / alignment samples ≠ depletion.

**Repo anchors:** historical axisym shell / TJJ chain on `cursor/tjj-estimate-chain-e5c5` (`docs/TJJ-ESTIMATE.md`, `docs/AXISYM-SHELL.md`, `scripts/tjj_estimate.py`); five-lane / HH / near-shell under `scripts/ns_attacks/` (`attack3_bony_hh_l.py`, `lemma_star_near_shell_search.py`, `product_bound_probe.py`, `attack9b_exact_shell_K.py`); Φ-renorm KEEP card [`PHI-RENORM-WHAT-IS-KEPT.md`](./PHI-RENORM-WHAT-IS-KEPT.md).

Probe runner (this branch): `python3 scripts/ns_attacks/tj_same_scale_candidate_probes.py`

---

## 0. What “(A)” means here

On the unaugmented shell face, (A) is the enstrophy–palinstrophy comparison route in which \(\rho_j<\nu\) (normalized by palinstrophy \(P_j\)) can enter the estimate. It is **not** absorption of same-scale transfer into the shell-energy viscous term \(\nu Z_j\). Closing \(T_{j\leftarrow j}\) needs either (A) itself, or a **depletion** estimate that implies (A), without recycling the quantity being bounded.

---

## 1. Candidate shortlist (narrow first)

| ID | Name | One-line idea | Why it might work | Failure / circularity risk | Kill criterion | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | Energy+viscosity \(R\) (requested Young line) | \(\lvert T_{j\leftarrow j}\rvert\le\varepsilon\nu D_j+C\,\mathcal{E}\,Z_j\) | Would finish the shell budget with allowed bookkeeping | Concentration \(u^\lambda=\lambda^{3/2}\varphi(\lambda x)\) sends ratio \(\to\infty\) (Prop. TJJ-E-false) | Ratio \(\lvert T\rvert/(\varepsilon\nu D+C\mathcal{E}Z)\to\infty\) along \(\lambda\to\infty\) | **DEAD** |
| C2 | Centrifugal-only leftover (“axisym swirl depletion”) | Under axisym-with-swirl, only \(T^{\mathrm{ss}}\) (centrifugal \(1/r^4\) pairing) remains; meridional piece free by 2D regularity | Pure swirl pairing vanishes; Φ-identity rewrites swirl source | Mixed samples: \(T^{\mathrm{mm}}\) is the **bulk**, not \(T^{\mathrm{ss}}\) | On mixed compact swirl+meridional, \(\lvert T^{\mathrm{mm}}\rvert\gg\lvert T^{\mathrm{ss}}\rvert\) on energy-carrying shells | **DEAD** *(conditional class)* |
| C3 | Circular Gronwall recycle | Bound \(T_{j\leftarrow j}\) from \(\dot e_j\), \(\dot Z_j\), or \(\Lambda'\) | Algebraically available from AS-Id / spectral-shift | Restates the identity; honesty lock forbids | Any proposed bound that substitutes \(\dot Z_j\) or \(\Lambda'\) for \(T\) | **DEAD** (forbidden) |
| C4 | Occupancy≈1 + alignment≈½ ⇒ depletion ⇒ (A) | Restricted-disk numerics imply depletion strong enough for (A) | Samples look quiet | Explicitly refused on the honesty card; no \(K_{\max}\to\infty\) uniformity | Claim “numerics ⇒ (A)” without a depletion theorem | **DEAD** (refuse) |
| C5 | Pure-swirl vanishing as class bound | Axisym pure swirl \(\Rightarrow T_{j\leftarrow j}=0\), upgrade to mixed class | Prop. TJJ-pure sits; probe residual \(\sim 0\) | Only pure subclass; mixed class still has \(T^{\mathrm{mm}}\) | Using pure-swirl zero as a bound on swirl+meridional | **BLOCKED** *(subclass only)* |
| C6 | Axisym Door-3 / \(\alpha_+\) control | Control \(\|(\alpha_{\mathrm{loc},j})_+\|_\infty\) (or integrable substitute) so main stretch \(\int\alpha_+\,\lvert\omega_j\rvert^2\) enters (A) or Young | Prop. TJJ-α: main stretch **is** \(\alpha\); transport main term vanishes | \(\alpha_+\) not controlled by energy/\(\{Z_k\}\); Bernstein returns cubic wall; commutators still need \(\|u_{\mathrm{loc}}\|_\infty\) | Either a geometric \(\alpha\) bound, or a family with \(\alpha_+ Z_j\) escaping every allowed \(R\) while identities hold | **TRY** *(conditional if α-hypothesis used)* |
| C7 | HH-only budget on same-scale / near-shell | Bound only HH parent channel of local transfer; HL/LL by classical products | Live bottleneck in Bony diagnostics (`attack3`); HH mass lemma on ★ side | Agmon / \(\|\nabla v_H\|_\infty\) lose geometry-only control; HL/LL “classical free” already killed on ★ packaging | HH channel fraction stays large **and** no geometric HH product appears; or a kill family for the proposed HH form | **TRY** |
| C8 | Near-shell cancellation (Attack 9B laboratory) | Two-shell / near-shell structure forces cancellation so local flux cannot feed blowup of \(\rho_j\) | Exact \(K_{\alpha,\beta}\) limits finite; near-shell search did not diverge on tested families | Restricted family ≠ class bound; occupancy 1 ≠ depletion | Uniform statement over shells fails, or \(K_{\alpha,\beta}\to\infty\) along a named family | **TRY** *(lab / evidence only unless upgraded)* |
| C9 | Structure on triad / closed-triad \(\tau\) rewrite | Rewrite local triad as \(\tau=(\omega(p)-\omega(r))J_p+\cdots\) / shift by lattice \(\omega_*\) to expose cancel | Identities already seated in AXISYM-SHELL §5 | Identity ≠ bound; can hide the same leftover | Rewrite that does not produce an allowed \(R\) (energy / \(Z\) / direction) | **TRY** |
| C10 | Non-circular depletion ⇒ (A) | Prove depletion of upward stretch / enstrophy production that implies \(\rho_j<\nu\) without \(\dot e_j/\dot Z/\Lambda'\) | Named as the honest Step-6 route on the lock card | Easy to smuggle time derivatives or spectral-shift back in | Any argument that reintroduces \(\dot e_j\), \(\dot Z\), or \(\Lambda'\) as the controlling quantity | **TRY** *(principal live)* |
| C11 | Meridional \(T^{\mathrm{mm}}\) geometric cancel *(axisym)* | After C2 death: attack \(T^{\mathrm{mm}}\) directly (structure / cancel under SO(2)) | Mixed-sample bulk is meridional; axisym kills free helical HHH | Meridional piece of a *mixed* field is not a no-swirl solution; 2D regularity does not transfer | \(T^{\mathrm{mm}}\) saturates every proposed geometric \(R\) on mixed blobs | **TRY** *(conditional: axisym)* |
| C12 | SND / shell-concentration conditional | Assume SND-type shell texture; write flux / Gronwall cleanly under that hypothesis | Optional texture already named on the chain map | Conditional ≠ Clay; must not be sold as unaugmented close | Hypothesis used without label, or SND itself fails on a named family | **TRY** *(conditional only)* |

---

## 2. Run-now set (survivors worth probing)

Narrowed **now** (drop DEAD / BLOCKED / forbidden):

| Priority | ID | Probe mode | Why now |
| --- | --- | --- | --- |
| 1 | **C10** | Analytic checklist: depletion ⇒ (A) without forbidden slots | Principal honest door; cheap to reject circular drafts |
| 2 | **C6** | Analytic identities (transport vanish / stretch \(=\alpha\)) + Door-3 status | Already half-seated; kill or condition must be named |
| 3 | **C7** | Light HH channel diagnostic (`attack3`) | Existing harness; confirms bottleneck still live |
| 4 | **C8** | Light near-shell / product-bound ceilings | Existing harness; no claim of uniformity |
| 5 | **C9** + **C11** | Analytic inventory (triad rewrite; \(T^{\mathrm{mm}}\) as bulk target) | Structure routes; C11 labeled **axisym-conditional** |

Not run as live attacks: **C1–C5** (already DEAD/BLOCKED/forbidden). **C12** parked behind an explicit SND hypothesis (conditional paper only).

---

## 3. Probe results (this pass)

Artifacts: `/opt/cursor/artifacts/tj-same-scale-candidates/`  
Command: `python3 scripts/ns_attacks/tj_same_scale_candidate_probes.py`

### 3.1 Analytic (no numerics required)

| ID | Result | Notes |
| --- | --- | --- |
| C1 | **DEAD confirmed** | Scaling ledger: \(Z\sim\lambda^2\), \(D\sim\lambda^4\), \(T\sim\lambda^{9/2}\) ⇒ ratio \(\sim\lambda^{1/2}\to\infty\) |
| C2 | **DEAD (recorded)** | Mixed-sample table from TJJ chain: \(T^{\mathrm{mm}}\) dominates energy-carrying shells |
| C3 | **DEAD (refuse)** | Checklist rejects any bound using \(\dot e_j/\dot Z_j/\Lambda'\) |
| C4 | **DEAD (refuse)** | Honesty card: occupancy 1 + alignment ≈ ½ ≠ depletion |
| C5 | **BLOCKED** | Pure-swirl zero sits; does not upgrade to mixed class |
| C6 | **SURVIVES as TRY** | Identities (transport / \(\alpha\)) remain the seated local split; \(\alpha_+\) control still open |
| C9 | **SURVIVES as TRY** | Triad rewrite remains identity-level; no allowed \(R\) yet |
| C10 | **SURVIVES as TRY** | No circular draft passed the refuse checklist; live target unchanged |
| C11 | **SURVIVES as TRY** *(axisym-conditional)* | After C2 death, \(T^{\mathrm{mm}}\) is the named bulk target |
| C12 | **SURVIVES as conditional-only** | Not promoted to unaugmented close |

### 3.2 Light numerics (finite samples ≠ theorems)

Recorded 2026-09-16 run (`tj_candidate_probe_results.json`):

| Probe | Harness | Outcome | Implication for candidates |
| --- | --- | --- | --- |
| Analytic concentration | in-probe C1 | Ratio growth \(\approx 13\) over \(\lambda=4\to 256\) (\(\sim\lambda^{1/2}\)) | **C1 DEAD confirmed** |
| Circular-slot refuse | in-probe C3 | Refused \(\dot Z_j\), \(\Lambda'\), \(\dot e_j\) drafts | **C3 DEAD** |
| Centrifugal-only table | recorded TJJ mixed samples | \(T^{\mathrm{mm}}\) dominates on \(j=1,2,3\) | **C2 DEAD** |
| Product / \(\mathcal{R}_\star\) ceilings | light two-shell sample | Finite-sample \(\mathcal{R}_\star\) tiny / vacuous on draws | No kill; not a supremum |
| HH channel share | `attack3_bony_hh_l.py` | Verdict `HH_CHANNEL_LIVE_BOTTLENECK_no_closure`; random HH frac mean \(\approx 0.093\), p90 \(\approx 0.51\) | **C7 SURVIVES** |
| Near-shell + HH diagnostic | `lemma_star_near_shell_search.py` (`--n-almost 40 --n-hh 30`) | `LemmaStar_killed=false`; max \(\mathcal{R}_\star\approx 2.3\times 10^{-4}\) on 127 samples; verdict `SURVIVE_numeric_gap_remains` | **C8 SURVIVES as lab** |

---

## 4. Who survived (verdict table)

| ID | After this pass | Next concrete move |
| --- | --- | --- |
| C1 | DEAD | Do not revive energy-linear \(R\) |
| C2 | DEAD | Do not claim centrifugal-only leftover |
| C3 | DEAD | Keep refuse checklist on every draft |
| C4 | DEAD | Keep numerics ≠ depletion |
| C5 | BLOCKED | Pure swirl = check, not class bound |
| **C6** | **SURVIVES (TRY)** | Seek geometric / integrable control of \(\alpha_+\) **or** name an explicit α-hypothesis (conditional) |
| **C7** | **SURVIVES (TRY)** | HH-only product against allowed shell scales; no Agmon smuggling |
| **C8** | **SURVIVES (TRY / lab)** | Upgrade near-shell cancel to a depletion statement feeding (A), or kill via \(K\to\infty\) |
| **C9** | **SURVIVES (TRY)** | Turn \(\tau/\omega_*\) rewrite into an estimate with allowed \(R\) |
| **C10** | **SURVIVES (TRY, principal)** | Write a depletion ⇒ (A) sketch with forbidden slots listed and empty |
| **C11** | **SURVIVES (TRY, axisym-conditional)** | Structure/cancel on \(T^{\mathrm{mm}}\) for mixed swirl+meridional |
| C12 | SURVIVES (conditional-only) | Honest SND paper only; not unaugmented Clay |

**Bottom line:** the live unaugmented remainder is still \(T_{j\leftarrow j}\). Survivors worth pushing next are **C10 (principal)**, then **C6 / C11 (axisym-conditional structure)**, with **C7 / C8 / C9** as supporting laboratory / rewrite lanes. No Clay claim. No Lemma★ close from these probes.

---

## 5. Score (honesty)

| Claim | Status |
| --- | --- |
| Same-scale \(T_{j\leftarrow j}\) controlled | **OPEN** |
| Path to (A) without circular recycling | **OPEN** |
| Spectral-shift ⇒ ★ / regularity | **Refuse** |
| NS / Clay B solved | **Not claimed** |
| This note as a proof | **No** — candidate filter + light probes only |
