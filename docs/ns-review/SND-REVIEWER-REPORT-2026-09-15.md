# SND program — comprehensive report for a specialist reviewer

**Author:** Jonathan R. Simons  
**Prepared:** 15 September 2026  
**Audience:** independent specialist (fluids / harmonic analysis), not a campaign reader  
**Honesty lock:** classical 3D Navier–Stokes is **not** solved. Clay Statement (B) is **not** claimed. This document inventories what the SND body of work actually is.

---

## 0. What to tell the reviewer in one page

**SND is a legitimate extra structural hypothesis, not a theorem about all data.**

On \(\mathbb{T}^3\), write Littlewood–Paley enstrophy shells \(X_j\), total enstrophy \(X=\sum_j X_j=\|\omega\|_2^2\), peak shell \(J=\max_j X_j\), and peak fraction \(\rho=J/X\). **SND** (fluids, frozen definition) is

\[
\inf_t \frac{J(t)}{X(t)}\ge c_*>0.
\]

That is a **concentration** statement: a uniform positive fraction of enstrophy stays in a dominant shell. If it held for all Leray–Hopf data *without* assuming the \(H^1\) bound it is meant to produce, and if the SND \(\Rightarrow\) regularity arrow were clean, it would be a spectral cousin of Beale–Kato–Majda. **Neither half is proved for large data.**

**The program is up against \(H^1\) again.** That is not a new discovery. Every spectral route that looked like a close eventually re-imported an a priori enstrophy ceiling \(X\le M\), or else failed to control stretching at energy-class regularity. After the later Lemma★ / exact-shell season (September 2026), the leftover is still an \(H^1\)-class estimate: either produce \(M\) from \(\|u_0\|_{H^1}\) alone, or control tube stretching (Door B / WRITE (6)) without an amplitude-independent rate that the ABC model already kills.

**Keep spectral as language. Do not keep it as the closer.** Littlewood–Paley shells, the Ring Lemma, Bony \(T+T^*+R\), and T2 Lemma 1 are real toolkit. Using them to *claim* large-data regularity, or to glue SND to arithmetic Bridge / Q6 / Triple Lock, is the part that should stay retired.

---

## 1. Three different “H1” objects (do not mix them)

The phrase “up against H1 again” is accurate, but the symbol is overloaded. A reviewer should freeze three distinct objects:

| Label in this report | What it is | Status |
| --- | --- | --- |
| **Sobolev \(H^1\)** | Energy-class / enstrophy control \(\|u\|_{H^1}\) (or \(X=\|\nabla u\|_2^2\)) | The supercritical barrier. 3D NS is a derivative short of scaling-critical. This is Tao’s objection, not a slogan. |
| **TH-H1 (weld)** | Theorem H as written assumes **\(X\le M\)** and a spread regime \(\rho\le\rho_0\), then bounds dominant-shell flux \(\Pi_{j_*}\) | **Circular for Clay.** The keystone estimate smuggles the conclusion. Domain Architect break card `TH-H1`. |
| **Door B / WRITE (6) H1** | Localized stretching \(A_{\mathrm{bad}}\) on a cylinder \(Q_r\) (one vortex tube). Target: a BKM-style bound independent of \(\lvert\omega\rvert\) | **OPEN.** P1 thinness sits; \(J=O(1)\) independent of amplitude **fails** (ABC: \(J\sim A\)). Not estimate-complete. |

There is a fourth, unrelated **H1** in this repo: Harmonic Blueprint ringdown Experiment 01 (held-out TEST did not reject H0). That is an observational protocol. It is **not** this fluids estimate.

**Reading of “again”.** May–June packaging tried to close regularity through SND + Theorem H and hit \(X\le M\). August audits named that weld and retired the Clay green. September Lemma★ / exact-shell / same-shell attacks tried a different spectral-shape box and died or stayed restricted. The live remainder is again an \(H^1\)-class integral (TH-H1 or Door B). That is the honest loop.

---

## 2. What SND is — and the naming bug that must be disclosed

### Frozen fluids definition (KEEP this one)

From the Ring + SND papers (Zenodo concept `20518056`, honest KEEP face `10.5281/zenodo.22050976`):

\[
X(t)=\|\nabla u(t)\|_{L^2}^2,\qquad
J(t)=\max_j X_j(t),\qquad
\rho(t)=J(t)/X(t),
\]

**[SND]** \(=\ \inf_t J/X \ge c_*>0\).

Call this **SND-U** when the claim is “for all relevant \(H^1(\mathbb{T}^3)\) data, without an a priori ceiling \(M\).”

### A different object that was also called “Theorem H”

**(SND-C)** is a *shell-conditioned flux bound* on the peak shell \(\Pi_{j_*}\) in a **spread** regime \(\rho\le\rho_0\ll 1\), with constant \(C_*=C_*(\nu,\delta_*,M,\rho_0,\ldots)\). Manuscripts prove (or attempt) SND-C **under** \(X\le M\). That is **not** SND-U.

### The June/August opposite-word bug

Some June T2 notes used “SND” for **non-concentration** \(\rho\le\rho_0\) (spread). August Ring notes used “SND” for **concentration** \(\rho\ge c_*\). Those are opposites. Any reviewer packet must freeze one dictionary:

| Regime | Condition | Honest name |
| --- | --- | --- |
| CONC | \(\rho\ge c_*\) or packet \(\sigma=P_{j_*}/X\ge 1/2\) | concentration / SND-U target |
| SPREAD | \(\rho\le\rho_0\) | spread / T2 / SND-C hypotheses |

Do not let one acronym mean both.

### What SND does *not* control (even if the shell bound were clean)

- motion of the peak index \(j_*\)
- Stokes-moment barycenter \(\Lambda=Y/X\) (a **different** quotient)
- continuation of \(X\) for all data
- Constantin–Fefferman alignment
- axisymmetric same-shell remainder \(T_{j\leftarrow j}\)

Closing SND-C under \(X\le M\) does **not** close ordinary NS. Closing SND-U without circular \(M\) would *essentially be* Clay Statement (B) on \(\mathbb{T}^3\), up to a refereed SND \(\Rightarrow\) regularity arrow. That is the Tao-panel one-liner, and it still stands.

---

## 3. KEEP vs PARK — the public inventory a reviewer should cite

### KEEP (cite these)

| Object | Honest label | Public face |
| --- | --- | --- |
| **Ring Lemma** | Band-limited vorticity-direction bound: \(\|\nabla\xi_0\|_{L^\infty(E_c)}\le C\,2^{j_*}\) on \(\{|\omega|\ge c\|\omega\|_2\}\) | `10.5281/zenodo.22050976` |
| **SND as hypothesis** | Conditional spectral regularity criterion; not proved for all Leray–Hopf data | same KEEP DOI |
| **T2 under SND** | Shell-flux Gronwall **conditional on** a spread/SND hypothesis. Lemma 1 (div-free kills far-low self-flux) is the solid brick | `10.5281/zenodo.22050965` |
| **Φ-renorm algebra** | \(\frac1{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\). Axisymmetric-with-swirl **identity**, not Clay | `10.5281/zenodo.22050974` / `22050975`; June 30 conditional reduction `21071991` |
| **Status / errata index** | What stands / what is withdrawn | `10.5281/zenodo.22050978` |
| **Q6 operator note** | Inverse-GCD definitions; **no RH, no NS** | `10.5281/zenodo.22050962` |

Φ-renorm open barrier (unchanged, 22 Aug 2026 audit): \(\|u^r/r\|_{L^\infty}\) uniform in \(\varepsilon\) — equivalent difficulty to axisymmetric-with-swirl global regularity. Relabel \(\dot H^{2.6}\to\dot H^{1.3}\) was notation, not a repair of the barrier.

### PARK / withdrawn (do not let a reviewer cite as current claims)

| Object | Why |
| --- | --- |
| “Clay Statement (B) proved” / May global-regularity note | `10.5281/zenodo.20405526` — PARK. Status table greened objects the proofs did not establish. |
| **Triple Lock** `SND ≡ GNC ≡ Bridge` | Identity false. Full-spectrum \(\lambda_{\min}(Q_N)>-1/2\) false (e.g. \(Q_{10}\approx-1.90\)). Domain Architect **C-GLUE-2 RETIRED**. |
| “SND implies global regularity” (May packaging) | `10.5281/zenodo.20272545` — PARK. SND was not a proved closure. |
| Older SND framework | `10.5281/zenodo.20518057` — superseded by corrected Ring+SND KEEP. |
| Unconditional “Theorem H = SND for all \(H^1\) data” | Mislabel of SND-C. Favorable ARCHON 10-expert panel is **synthetic roleplay, not peer review** (adversarial verdict 25 Aug 2026). |
| \(c_*=6/\pi^2=\zeta(2)^{-1}\) as fluids SND floor | Arithmetic density, not a continuum threshold. |
| Q6 / inverse-GCD as damper of the dominant shell that “enforces SND” | Withdrawn glue. Dominant shell \(j_*\) is an LP fact; Q6 is a matrix. |
| Φ-renorm \(\to\) Theorem H \(\to\) Clay | **C-GLUE-4**. The identity does not feed Fourier-shell H. |
| Track A \(Q_1\)-augmented Theorem A as \(\varepsilon\to 0\) export | Different PDE. Uniform \(H^1\) as \(\varepsilon\to 0\) is **open**. \(A\Rightarrow B\) fails. |

### Later September objects (adjacent, not SND itself)

These grew out of the spectral program and must be on the table so a reviewer does not think SND is still the live closer:

| Object | Status (Sept 2026, draft PRs) |
| --- | --- |
| **Spectral-shift identity** | Exact triad/shell **bookkeeping** (axisymmetric shell budget / Door-1 split). **≠** Lemma★ ratio bound. Establishing it does not control \(T_{j\leftarrow j}\). |
| **Lemma★ / \(\mathcal{R}_\star\)** | Shape quotient for nonlinear transfer on \(\mathbb{T}^3\). Unrestricted \(\sup_v\mathcal{R}_\star<\infty\) is **claimed killed** (12 Sep) on family \(v_n\) with \(\mathcal{R}_\star(v_n)\gtrsim n/165888\to\infty\). That is a counterexample to the boxed instantaneous estimate, **not** a singular NS solution. |
| **Exact-shell 9D** \(K\le 16/9\) | **CLAIMED** on one input shell; internal checks passed; independent specialist review pending. Does **not** control multi-shell fields and does **not** restore Lemma★. |
| **Same-shell \(T_{j\leftarrow j}\)** | Principal remainder of the unaugmented shell chain. Requested energy-class \(R\) **cannot be written**. “The chain stays a chain.” |
| **Centered spectral drift** \(\Lambda=Y/X\), \(T_c=M-\Lambda N\) | Named package **not recovered** as a complete proved argument in this repo. Do not invent it. It is **not** SND’s \(J/X\). |

---

## 4. Proof graph (phi-free) — what would have to sit

No edge from Φ-renorm into this chain:

```text
LP shells X_j, X, J, ρ = J/X
        │
        ▼
   SND-U: inf J/X ≥ c_* > 0          OPEN for all H¹ data
        │
        ├──────────► Ring Lemma (band-limited CF on E_c)     KEEP toolkit
        │
        ├──────────► T2 Lemma 1 (div-free far-low)           KEEP
        │                 │
        │                 ▼
        │            T2 Gronwall under spread                 CONDITIONAL
        │
        └──────────► SND-C / Theorem H under X ≤ M, ρ ≤ ρ₀    CONDITIONAL
                          │
                          ✕  TH-H1 weld: M is the Clay output
                          │
                          ▼
                 conditional regularity under SND              NOT Clay B
```

**Missing conjuncts for a non-circular skeleton** (status-report synthesis, document not finished):

1. uniform SND-C in SPREAD **without** feeding \(M\) from the conclusion;
2. Ring control in a genuine 3-shell CONC regime;
3. a **drift law** for \(j_*\) / \(\Lambda\) that prevents unbounded climb.

(3) is missing. Occupation time \(\tau_C+\tau_S=T\) is not a bound on \(X\). Instantaneous random CONC does not produce a “saving climb”; viscosity tends to pull the barycenter down.

**Theorem G** (SND-C \(\Rightarrow\) SND) still has \(c_*=c_*(\nu,\delta_*,M,\ldots)\). Even the spectral-gap conclusion carries the ceiling. That is break **TH-H3**.

**Q1 approximants.** Smooth hyperdissipative SND need not pass to the Leray–Hopf limit. That is **TH-H7-Q1**.

---

## 5. Should you keep spectral?

### Recommendation (for the reviewer, and for the author)

**Keep the spectral machine. Retire spectral as the large-data closer. Do not glue it to Door B H1 to fake a second close.**

#### Keep (fluids Track B)

- Littlewood–Paley shells \(X_j\), peak \(j_*\), fractions \(\rho,\sigma\)
- Bony decomposition \(T+T^*+R\) for peak-shell flux
- Ring Lemma as a **band-limited** geometric bound (hypotheses on the table)
- T2 Lemma 1 (incompressibility identity)
- SND **named as an extra hypothesis**, same genus as BKM/LPS
- Spectral-shift identity as **bookkeeping only**
- Honest KEEP DOI `22050976`

#### Keep, but in a different book

- Φ-renorm swirl algebra (axisymmetric; barrier \(\|u^r/r\|_\infty\) open)
- Inverse-GCD / \(H_N\ge -1\) as **matrix facts** (no PDE map)
- Route C / Q6 exploratory notes **without** NS or RH claims

#### Retire from the unaugmented close

- One word “SND” for both CONC and SPREAD
- Theorem H relabeled as “SND for all \(H^1\) data”
- Triple Lock / Bridge / Q6 damper of the dominant shell
- Φ-cancel as an input to Fourier-shell H
- Unrestricted Lemma★ as a box (if the \(v_n\) kill survives specialist check)
- Exact-shell 9D as if it restored a regularity path
- Restricted-disk numerics (occupancy \(\approx 1\), alignment \(\approx 1/2\)) as depletion
- \(\rho_j<\nu\) as absorption on the displayed shell-energy budget (wrong viscous slot)
- Centered-drift \(\Lambda=Y/X\) invented back into SND

#### Why not drop spectral entirely?

Because the alternative is not a proved geometric close either. Door B H1 is the *same leftover stretching*, rewritten on one cylinder. The spectral dictionary is still the right way to **state** the extra hypothesis (peak-shell occupation) and to **separate** CONC from SPREAD. Dropping LP/Bony would erase the only clean description of what SND even is. What should be dropped is the belief that shell language manufactures the missing derivative.

Tao reading, still the right standard: energy-supercritical methods cannot close large-data 3D NS by abstract bounds alone. SND is an *extra* hypothesis. Until it (or an equivalent critical control) is proved for all data without circular \(H^1\) bounds, NS remains open. Averaged-NS blowup (Tao 2014) is the obstruction to “energy methods plus optimism.”

---

## 6. What “up against H1 again” should mean operationally

Two live estimates, **one row each, not glued**:

### Row 1 — TH-H1 (spectral)

Produce \(M=M(\|u_0\|_{H^1})\) or remove \(M\) from \(C_*\) and from \(c_*\). Until that sits, Theorem H is a conditional lemma in a bounded-enstrophy class, not Clay B.

Attack plan already written (`THEOREM-H-ATTACK-PLAN.md`): bootstrap / replace the worst \(M\)-power in the flux estimate by energy + dissipation; freeze a clean **SND-U \(\Rightarrow\) regularity** writeup as a separate depositable win; do not re-green Statement B.

### Row 2 — Door B H1 (geometric)

Target on one cylinder (sketch):

\[
A_{\mathrm{bad}}(Q_r)
\le
\frac{\nu}{8}\iint_{Q_r}\lvert\nabla\omega\rvert^2\phi
+ C r^{-2}\iint_{Q_r}\lvert\omega\rvert^2.
\]

Wanted BKM-style: \(\int_0^\tau\|(\xi\cdot\nabla u\cdot\xi)_+\|_{L^\infty(\mathrm{tube})}\,dt\le C(\rho,L)\).

**What sits:** P1 / P1-loc thinness, some path-cost bookkeeping.  
**What fails:** \(J(Q)=O(1)\) independent of \(\lvert\omega\rvert\) (ABC: \(J\sim A\)); angular viscosity vs tube flux climbing with \(j_*\); packet ceiling under climbing \(j_*\); derived waiting time; Outside-\(\mathcal E\) identity (**blocked, no candidate**).  
**Rule:** do not glue H1 to Lemma★, to matrix \(H_N\), or to the Ring Lemma. Do not add a remainder \(K(t)\) to the PDE by hand.

If the packet / Lemma★ line is shelved, Door B is the other writing of leftover WRITE (6). It is **not** “almost proved.”

---

## 7. Body of work — what exists where

This repository’s `main` only holds a slice (Φ-renorm KEEP card, Zenodo inventory, Domain Architect hygiene). The SND corpus lives on draft branches / PRs and Zenodo. A reviewer should not be asked to merge 100 drafts; they should be given **this list**.

### Public deposits (post-August honesty)

| DOI | Role |
| --- | --- |
| [10.5281/zenodo.22050976](https://doi.org/10.5281/zenodo.22050976) | **Cite this:** Ring Lemma + SND **conditional / hypothesis** |
| [10.5281/zenodo.22050965](https://doi.org/10.5281/zenodo.22050965) | T2 Gronwall **under SND** |
| [10.5281/zenodo.22050978](https://doi.org/10.5281/zenodo.22050978) | Status and errata index |
| [10.5281/zenodo.20405526](https://doi.org/10.5281/zenodo.20405526) | PARK — withdrawn Statement (B) packaging |
| [10.5281/zenodo.20552400](https://doi.org/10.5281/zenodo.20552400) | PARK — Triple Lock |
| [10.5281/zenodo.20272545](https://doi.org/10.5281/zenodo.20272545) | PARK — “SND implies regularity” |

### Specialist notes in this repo family (open PRs)

| PR | What a reviewer actually needs |
| --- | --- |
| [#11](https://github.com/simons357/Ship_it_app/pull/11) | Early SND ≡ GNC ≡ Bridge rigor memo — **historical**; identity later retired |
| [#22](https://github.com/simons357/Ship_it_app/pull/22) | Tao–SND / Theorem H panel; T2 \(\nu\) errata; spectral-object map |
| [#24](https://github.com/simons357/Ship_it_app/pull/24) | Unaugmented living line (large working desk, draft) |
| [#35](https://github.com/simons357/Ship_it_app/pull/35) | **Adversarial ARCHON verdict:** Theorem H ≠ unconditional SND |
| [#36](https://github.com/simons357/Ship_it_app/pull/36) | Gap-closure playbook; DA refuses Clay glue at \(X\le M\) |
| [#48](https://github.com/simons357/Ship_it_app/pull/48) | Five-lane Lemma★ SoT; spectral-shift ≠ ratio bound |
| [#70](https://github.com/simons357/Ship_it_app/pull/70) | Axisymmetric shell estimate; spectral-shift identity locked |
| [#72](https://github.com/simons357/Ship_it_app/pull/72) | Strict scientific NS report |
| [#74](https://github.com/simons357/Ship_it_app/pull/74) | Exact-shell claimed vs unrestricted ★ kill — 20 specialist Q&A |
| [#76](https://github.com/simons357/Ship_it_app/pull/76) | Exact-shell 9D review face (still CLAIMED) |
| [#78](https://github.com/simons357/Ship_it_app/pull/78) | Unaugmented proof-chain honesty: identity ≠ bound |

### Domain Architect (hygiene, not a proof engine)

- `--gap-closure` / `--snd-dual` refuse Theorem H \(\to\) Clay B
- Conflict **C-GLUE-2**: Triple Lock retired
- Conflict **C-GLUE-4**: Φ-cancel is algebra only
- Conditional PASS on claim hygiene ≠ peer review

---

## 8. What is real mathematical content vs what fails scrutiny

### Real

1. **August 2026 public audit** — unusually clear retractions; KEEP set is the right cite list.
2. **Ring Lemma** — Bernstein on a band-limited direction field; correctly scoped when hypotheses stay on the page.
3. **T2 Lemma 1** — incompressibility identity; pass.
4. **Φ-renorm cancel** — algebraic identity; independent 22 Aug audit left the PDE and Lions bookkeeping intact and the strain barrier open.
5. **Bridge\* single-pair** Rayleigh on inverse-GCD test vectors — true **number theory**, orthogonal to NS.
6. **Regime split CONC vs SPREAD** after the naming repair.
7. **TH-H1 diagnosis** — Theorem H assumes \(X\le M\); that is the correct keystone objection, written down in adversarial form so a loud false positive can be answered in one paragraph.

### Fails (or is not ready)

1. May global-regularity packaging and any “Main Theorem / Statement (B) proved” table.
2. Dynamic SND-U for arbitrary finite-energy data.
3. Uniform low Bony \(T\) as \(\rho\to 0\) (supercritical hole: the low paraproduct still wants a derivative).
4. Occupation-time glue between CONC and SPREAD as an a priori on \(X\).
5. Geometry from Ring \(\Rightarrow\) CF alignment / cubic depletion (tested packets: median \(\lvert\cos\alpha_3\rvert\sim 1/2\), not \(\to 0\)).
6. Cross-domain bridges (fluids SND = arithmetic Bridge = RH).
7. Unrestricted Lemma★ (if \(v_n\) is admissible — specialist check still requested).
8. Exact-shell 9D as a regularity consequence (even if the \(16/9\) bound is later signed).
9. Door B H1 as “the remaining estimate that is basically done.”

---

## 9. Suggested packet for the reviewer (do not send 600 files)

Send **five documents**, in this order:

1. This report.
2. Tao panel: `docs/math/TAO-MATH-PANEL-SND-H.md` (PR #22).
3. Adversarial Theorem H verdict: `docs/ns-review/ARCHON-PANEL-ADVERSARIAL-VERDICT.md` (PR #35).
4. KEEP deposit abstract + PDF: [10.5281/zenodo.22050976](https://doi.org/10.5281/zenodo.22050976).
5. Unaugmented honesty card: `docs/ns-review/UNAUG-PROOF-CHAIN.md` (PR #78), so spectral-shift is not read as a bound.

Optional sixth, only if they ask about September: PR #74 specialist Q&A (exact-shell claimed / unrestricted ★ dead / NS still open).

**Competitor / referee kill line (already locked):**

> Theorem H as written assumes \(X\le M\). Clay Statement (B) is the problem of producing that bound from data. An airtight proof of SND-C under an a priori ceiling does not resolve B.

---

## 10. Bottom line for the reviewer

Jonathan Simons has a **conditional spectral regularity program** for 3D Navier–Stokes on \(\mathbb{T}^3\), built from Littlewood–Paley occupation, a band-limited Ring Lemma, and a shell-flux estimate that currently needs an enstrophy ceiling. After an honest August retraction of Clay packaging and Triple Lock glue, and after a September season that killed or restricted the Lemma★ shape box, **the leftover is again \(H^1\)**: either remove \(M\) from Theorem H, or control stretching by a geometric estimate that is not yet estimate-complete.

**Spectral should be kept as the dictionary and the toolkit. It should not be kept as a claimed close.** Door B H1 is a parallel writing of the same leftover, not a rescue of SND. Φ-renorm is a separate axisymmetric identity with its own open barrier. Arithmetic Q6 / Bridge is a third book.

**No Millennium claim. Clarification progress, not closure.**

---

## Appendix A — symbol card (fluids only)

| Symbol | Meaning |
| --- | --- |
| \(X_j\) | LP enstrophy (or, in the energy-shell note, energy) in shell \(j\) — **say which** |
| \(X\) | \(\sum_j X_j=\|\omega\|_2^2\) (enstrophy convention) |
| \(J\) | \(\max_j X_j\) |
| \(\rho\) | \(J/X\) |
| \(j_*\) | \(\arg\max_j X_j\) |
| \(\Pi_{j_*}\) | peak-shell flux |
| \(M\) | a priori enstrophy ceiling (the circular input) |
| \(\Lambda\) | Stokes-moment quotient \(Y/X\) — **not** \(\rho\) |
| \(\mathcal{R}_\star\) | Lemma★ shape ratio — **not** the spectral-shift identity |
| \(\Phi\) | swirl \(u_\theta/r\) — **not** DA gravitational \(\Phi\), not Paper2 shell \(\Phi_j\) |
| \(H_N\) | inverse-GCD matrix — **not** Theorem H |

## Appendix B — one-sentence answers the reviewer will ask

**Is SND proved?** No. It is a hypothesis about peak-shell occupation.

**Does SND imply regularity?** Conditionally, if the arrow is cleaned and \(M\) is not smuggled. Unconditionally, that *is* the hard problem.

**Is Theorem H SND for all data?** No. Theorem H as written is SND-C under \(X\le M\) and spread.

**Should spectral be dropped?** No. Drop the close, not the language.

**Are you claiming Clay B?** No.

**What is the next estimate?** One of: M-free (or data-only \(M\)) Theorem H; Door B cylinder H1; axisymmetric \(T_{j\leftarrow j}\) — **not all three glued**.
