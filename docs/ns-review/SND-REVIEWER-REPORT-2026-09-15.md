# SND program — comprehensive report for a specialist reviewer

**Author:** Jonathan R. Simons  
**Prepared:** 15 September 2026; **revised the same day** after specialist comments and the mathematical audit of the displayed Theorem H formulas  
**Audience:** independent specialist (fluids / harmonic analysis), not a campaign reader  
**Honesty lock:** this program does **not** claim unforced Clay Statement (B) (\(f\equiv 0\) on \(\mathbb{T}^3\)). A forced finite-time singularity (Clay C/D) was **announced** 8 September 2026 and is **under Clay evaluation** as of 11 September; that record is §0A below and is not used as a premise here. This document inventories the SND body of work.

---

## 0. What to tell the reviewer in one page

**Send first:** the manuscript extract [`THEOREM-H-STATEMENT-AND-PROOF.md`](./THEOREM-H-STATEMENT-AND-PROOF.md) **with** [`SND-MATH-CORRECTIONS-2026-09-15.md`](./SND-MATH-CORRECTIONS-2026-09-15.md). Then the 25 August verdict (plus erratum), then this briefing. Cover: [`REVIEWER-PACKET.md`](./REVIEWER-PACKET.md).

**SND is a legitimate extra structural hypothesis, not a theorem about all data.**

On \(\mathbb{T}^3\), write Littlewood–Paley enstrophy shells \(X_j\), total enstrophy \(X=\sum_j X_j=\|\omega\|_2^2\), peak shell \(J=\max_j X_j\), and peak fraction \(\rho=J/X\). **SND** (fluids, frozen definition) is

\[
\inf_t \frac{J(t)}{X(t)}\ge c_*>0.
\]

That is a **concentration** statement: a uniform positive fraction of enstrophy stays in a dominant shell. Treat [SND] as a **per-solution** extra hypothesis. A uniform floor from \(t=0\) for all data of fixed enstrophy is obstructed. The [SND] \(\Rightarrow\) regularity arrow (Theorem D) is a sketch. **Do not call [SND] equivalent to the Clay problem.**

**The displayed Theorem H is not a theorem, even with \(X\le M\).** The leftover is not “remove \(M\).” Rebuild the shell estimate, or work Door B as a **different** integral. Leray–Hopf is not a uniform \(H^1\) ceiling.

**Keep spectral as language and research program. Do not keep the displayed Theorem H as a proved estimate.** The \(X\le M\) weld was correctly flagged and is **incomplete**: with the displayed definition of \(\Pi_j\), the absolute-value bound **fails** on smooth fixed-enstrophy shear fields. The supplied proof drops a viscous tail and uses invalid 3D Sobolev embeddings. A valid \(M\)-dependent bound exists for the nonlinear term \(F_j\) alone; it does not give dominant-shell propagation. Rebuild from the exact shell equation. Using LP tools to *claim* unforced Statement (B), or to glue SND to arithmetic Bridge / Q6 / Triple Lock, stays retired.

Specialist judgment, accepted: (i) \(X\le M\) screenshots were a gap, not a kill of spectral research; (ii) [SND] \(\Leftrightarrow\) Clay was overstated; (iii) the displayed Theorem H is **not** established even with the ceiling; (iv) forced C/D (8–11 Sep) must be named and still do not decide unforced B.

---

## 0A. Public record, 8–11 September 2026 (status wording)

Broad lines of the form “Navier–Stokes is not solved” / “Clay is open” are no longer accurate as *unqualified* status, because a claimed resolution of the prize problem exists in public and Clay has responded. They remain accurate for **this program’s target**.

Official Fefferman statements ([Clay PDF](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf)):

| Statement | Domain | Force | Ask |
| --- | --- | --- | --- |
| **(A)** | \(\mathbb{R}^3\) | \(f\equiv 0\) | global smooth solutions for all admissible \(u_0\) |
| **(B)** | \(\mathbb{T}^3\) | \(f\equiv 0\) | same, periodic |
| **(C)** | \(\mathbb{R}^3\) | some smooth \(f\) | finite-time breakdown for some \(u_0,f\) |
| **(D)** | \(\mathbb{T}^3\) | some smooth \(f\) | same, periodic |

**(A) and (B) are compatible with (C) and (D).** Unforced global regularity and a forced blowup can both be true. The prize asks for a proof of **one** of the four.

| Date | What happened | What it does *not* do |
| --- | --- | --- |
| **8 Sep 2026** | [OpenAI announcement](https://openai.com/index/navier-stokes-solution/): analytical write-up + Lean formalization that a fluid at rest with a **smooth external force**, finite energy throughout, develops a singularity in finite time. They present this as Clay **(C) and (D)**. They state they do not intend to claim the prize. A separate Euler result (unforced, \(\nu=0\)) is also described. | Does not prove unforced (A) or (B). Does not become a premise of the SND chain. Evaluation is not this author’s to close. |
| **11 Sep 2026** | [Clay “Navier-Stokes Announcement”](https://www.claymath.org/news/navier-stokes-announcement/): CMI “shares in the excitement … as we contemplate the announcement that the Navier–Stokes problem has **apparently been settled**.” Prize rules “describe the process for evaluating what has been achieved and for assigning credit.” The process is “**deliberately unhurried**”; updates promised. The note does not name a claimant. | Not an award. Not a referee report. Not a decision that unforced (B) is true or false. |

**Wording rule for this packet.** Write: *unforced Statement (B) is not claimed here; forced C/D have a public announcement under Clay evaluation.* Do not write “the Millennium problem is open” as if 8–11 September did not happen. Do not write “Statement (B) is closed.” Do not treat the announcement as a theorem used inside Theorem H.

This program’s SND / Theorem H work is a **conditional unforced regularity** attempt on \(\mathbb{T}^3\). A forced blowup, even if later accepted as C/D, leaves that attempt mathematically live.

---

## 1. Three different “H1” objects (do not mix them)

The phrase “up against H1 again” is accurate, but the symbol is overloaded. A reviewer should freeze three distinct objects:

| Label in this report | What it is | Status |
| --- | --- | --- |
| **Sobolev \(H^1\)** | Velocity \(\|u\|_{H^1}\) (or \(X=\|\nabla u\|_2^2\)) | In 3D, \(\dot H^{1/2}\) is **critical** for the NS scaling \(u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2 t)\); velocity \(H^1\) is **subcritical**. The available **energy** control is supercritical. Leray–Hopf is \(L^\infty_t L^2_x\cap L^2_t H^1_x\), **not** a uniform-in-time \(H^1\) ceiling. |
| **TH-H1 (weld)** | Displayed Theorem H assumes \(X\le M\) and spread, and claims \(\lvert\Pi_{j_*}\rvert\le C_*(\nu 2^{2j_*}X_{j_*}+X^{1/2}\mathcal{D}^{1/2})\) | **False as displayed**, even with \(X\le M\): the proof drops the viscous tail \(S_j\), uses invalid embeddings, and the absolute-value bound fails on high-tail shears. Ceiling dependence was correctly noticed and is not the only defect. |
| **Door B / WRITE (6) H1** | Localized stretching \(A_{\mathrm{bad}}\) on a cylinder \(Q_r\) | **OPEN.** Not estimate-complete. Do not glue to the failed shell-flux statement. |

There is a fourth, unrelated **H1** in this repo: Harmonic Blueprint ringdown Experiment 01 (held-out TEST did not reject H0). That is an observational protocol. It is **not** this fluids estimate.

**Reading of “again”.** May–June packaging tried to close regularity through SND + Theorem H and hit a ceiling \(M\). August named that weld. The 15 September audit shows the displayed absolute-flux bound **already fails at fixed \(M\)**. The live remainder is a **rebuilt shell estimate**, or Door B as a separate integral — not “remove \(M\) from Theorem H.”

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

Call this **SND-U** only when the claim is a **uniform** floor for all relevant data, with \(c_*\) not allowed to depend on a circular ceiling \(M\). That uniform reading is obstructed at \(t=0\) (many equal shells, same \(X=q\)). The original [SND] as a per-solution extra hypothesis is a different statement.

### A different object that was also called “Theorem H”

**(SND-C)** is a *shell-conditioned flux bound* on the peak shell \(\Pi_{j_*}\) in a **spread** regime \(\rho\le\rho_0\ll 1\). The displayed absolute-value form is **not proved**, even under \(X\le M\). That is **not** SND-U. A uniform floor \(c_*(\nu,\delta_*,M,C_S)\) from time zero is obstructed by equal-shell shear data. Distinguish a **solution-by-solution** hypothesis from a uniform theorem.

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

Closing a *valid* flux bound under \(X\le M\) would still not close unforced Statement (B). The displayed (SND-C) is not such a bound. A cleaned [SND] \(\Rightarrow\) regularity arrow (Theorem D) remains a sketch. Small-data theory cannot manufacture a universal initial \(\rho\). The Tao-panel one-liner that equated unconditional SND with Clay B is **withdrawn as packet language**.

---

## 3. KEEP vs PARK — the public inventory a reviewer should cite

### KEEP (cite these)

| Object | Honest label | Public face |
| --- | --- | --- |
| **Ring Lemma** | Band-limited vorticity-direction bound, as *claimed* in KEEP `22050976`. A KEEP label is **not** verification. Elementary Bernstein on \(E_c^\infty=\{|\omega|\ge c\|\omega\|_\infty\}\) gives \(\|\nabla\xi\|_{L^\infty(E_c^\infty)}\le C\lambda/c\) and **changes the threshold**; do not silently replace the manuscript set \(\{|\omega|\ge c\|\omega\|_2\}\). | `10.5281/zenodo.22050976` |
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
| Unconditional “Theorem H = SND for all \(H^1\) data” | **Mislabeling** of (SND-C). Favorable ARCHON 10-expert panel is **synthetic roleplay, not peer review** (adversarial verdict 25 Aug 2026). Displayed Theorem H is not established even with \(X\le M\). |
| \(c_*=6/\pi^2=\zeta(2)^{-1}\) as fluids SND floor | Arithmetic density, not a continuum threshold. |
| Q6 / inverse-GCD as damper of the dominant shell that “enforces SND” | Withdrawn glue. Dominant shell \(j_*\) is an LP fact; Q6 is a matrix. |
| Φ-renorm \(\to\) Theorem H \(\to\) Clay | **C-GLUE-4**. The identity does not feed Fourier-shell H. |
| Track A \(Q_1\)-augmented Theorem A as \(\varepsilon\to 0\) export | Different PDE. Uniform \(H^1\) as \(\varepsilon\to 0\) is **open**. \(A\Rightarrow B\) fails. |

### Later September objects (adjacent, not SND itself)

These grew out of the spectral program and must be on the table so a reviewer does not think Theorem H is still a large-data closer:

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
LP shells X_j, X, J, ρ = J/X     (≍ for general LP; = on the exact-block family)
        │
        ▼
   [SND] per solution: inf J/X ≥ c_* > 0     HYPOTHESIS (not a uniform floor from t=0)
        │
        ├──────────► Ring-type bound on E_c^∞     scoped Bernstein; ≠ manuscript E_c
        │
        ├──────────► T2 Lemma 1 (div-free far-low)           KEEP
        │
        └──────────► displayed Theorem H / |Π_{j_*}|         FAILS even with X ≤ M
                          │
                          ▼
                 valid |F_j| bound under X ≤ M               different estimate
                          │
                          ▼
                 exact ½ Ẋ_j + ν 2^{2j}‖∇Δ_j u‖² = −2^{2j} F_j
                          │
                          ▼
                 rebuild J/X evolution; test shears / amplitude / equal shells
```

**Do not** list “uniform SND-C without \(M\)” as the next repair of *this* displayed estimate. Amplitude scaling already forbids an \(M\)-free quadratic bound on cubic \(F_j\) for every spread field. Start from the boxed shell equation (corrections §8).

**Theorem G** as written still lists \(c_*=c_*(\nu,\delta_*,M,\ldots)\). A uniform such floor from \(t=0\) is obstructed (equal-shell shears). That is stronger than August break **TH-H3**.

**Q1 approximants.** Smooth hyperdissipative SND need not pass to the Leray–Hopf limit. That is **TH-H7-Q1**.

---

## 5. Should you keep spectral?

### Recommendation (for the reviewer, and for the author)

**Keep the spectral machine as a research program. Retire spectral as a claimed close of unforced Statement (B). Do not glue it to Door B H1 to fake a second close.**

The specialist’s judgment is the packet’s judgment: the \(X\le M\) screenshots were a **gap**, not a kill of LP / Ring-type bounds. The displayed Theorem H is a **failed statement**, not a theorem awaiting only the removal of \(M\).

#### Keep (fluids Track B)

- Littlewood–Paley shells \(X_j\), peak \(j_*\), fractions \(\rho,\sigma\) (use \(\asymp\) unless the partition is frozen)
- A **complete** Bony decomposition of \(F_j\), not the displayed identification of \(\Pi_j\) with \(F_j\)
- Elementary Ring-type bound on \(E_c^\infty\), with the changed threshold on the page
- T2 Lemma 1 (incompressibility identity)
- SND **named as a per-solution extra hypothesis**, same genus as BKM/LPS
- Spectral-shift identity as **bookkeeping only**
- Honest KEEP DOI `22050976` as a citation label, not a verification stamp

#### Keep, but in a different book

- Φ-renorm swirl algebra (axisymmetric; barrier \(\|u^r/r\|_\infty\) open)
- Inverse-GCD / \(H_N\ge -1\) as **matrix facts** (no PDE map)
- Route C / Q6 exploratory notes **without** NS or RH claims

#### Retire from the unaugmented close

- One word “SND” for both CONC and SPREAD
- Theorem H relabeled as “SND for all \(H^1\) data”
- “Proved under \(X\le M\)” for the displayed \(|\Pi_{j_*}|\) bound
- “Remove \(M\) from this same estimate for every spread field” as the live target
- Triple Lock / Bridge / Q6 damper of the dominant shell
- Φ-cancel as an input to Fourier-shell H
- Unrestricted Lemma★ as a box (if the \(v_n\) kill survives specialist check)
- Exact-shell 9D as if it restored a regularity path
- Restricted-disk numerics (occupancy \(\approx 1\), alignment \(\approx 1/2\)) as depletion
- \(\rho_j<\nu\) as absorption on the displayed shell-energy budget (wrong viscous slot)
- Centered-drift \(\Lambda=Y/X\) invented back into SND

#### Why not drop spectral entirely?

Because the alternative is not a proved geometric close either. Door B H1 is leftover stretching on a cylinder, a different integral. The spectral dictionary is still the right way to **state** peak-shell occupation. Dropping LP would erase the description of [SND]. Rebuild the estimate from

\[
\tfrac12\dot X_j+\nu\,2^{2j}\|\nabla\Delta_j u\|_2^2=-2^{2j}F_j
\]

and test against high-tail shears, amplitude rescaling, and equal shells.

Tao reading, with scaling stated correctly: energy methods are supercritical; velocity \(H^1\) is subcritical and \(\dot H^{1/2}\) is critical. Averaged-NS blowup (Tao 2014) remains an obstruction to “energy methods plus optimism” for **unforced** large data. That is independent of whether a **forced** C/D announcement is later accepted.

---

## 6. What “up against H1 again” should mean operationally

Two live estimates, **one row each, not glued**:

### Row 1 — spectral shell budget (repaired)

Do **not** try to remove \(M\) from the displayed Theorem H. Write the exact shell equation, decide which evolution of \(J/X\) is needed, and prove an estimate with compatible amplitude powers. Include viscosity and domain constants. For continuation, a bound finite on each finite interval (allowed to depend on \(T\)) can suffice; an all-time \(M(\|u_0\|_{H^1})\) is stronger. Official (B) assumes **smooth** \(u_0\), not \(H^1\).

Test any candidate against the high-tail shears, \(u=Aw\), and \(v_L\).

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
2. **Ring-type bound** — elementary Bernstein on \(E_c^\infty\) is scoped and changes the threshold; manuscript \(E_c\) is not verified by a KEEP label.
3. **T2 Lemma 1** — incompressibility identity; pass.
4. **Φ-renorm cancel** — algebraic identity; independent 22 Aug audit left the PDE and Lions bookkeeping intact and the strain barrier open.
5. **Bridge\* single-pair** Rayleigh on inverse-GCD test vectors — true **number theory**, orthogonal to NS.
6. **Regime split CONC vs SPREAD** after the naming repair.
7. **August \(M\)-diagnosis** — correctly saw the ceiling; **incomplete**, because the displayed \(|\Pi_{j_*}|\) bound already fails at fixed \(M\).
8. **Valid \(F_j\) lemma** — \(|F_j|\le C\sqrt{M/(\nu\lambda_1)}\,X^{1/2}\mathcal{D}^{1/2}\) under mean-zero \(H^2\) and \(X\le M\); not Theorem H.

### Fails (or is not ready)

1. May global-regularity packaging and any “Main Theorem / Statement (B) proved” table.
2. Displayed Theorem H / (SND-C) absolute-flux bound, even with \(X\le M\).
3. Uniform SND floor \(c_*(\nu,\delta_*,M,C_S)\) from \(t=0\) for all data of size \(q\le M\).
4. “Remove \(M\) from this same quadratic estimate for every spread field.”
5. Dynamic [SND] as a theorem about all Leray–Hopf data.
6. Occupation-time glue between CONC and SPREAD as an a priori on \(X\).
7. Geometry from manuscript Ring \(\Rightarrow\) CF alignment / cubic depletion.
8. Cross-domain bridges (fluids SND = arithmetic Bridge = RH).
9. Unrestricted Lemma★ (if \(v_n\) is admissible — specialist check still requested).
10. Exact-shell 9D as a regularity consequence.
11. Door B H1 as “the remaining estimate that is basically done.”

---

## 9. Suggested packet for the reviewer (do not send 600 files)

Cover sheet: [`REVIEWER-PACKET.md`](./REVIEWER-PACKET.md).

Send **four documents**. If only one status file accompanies the extract, send the mathematical corrections.

1. **Manuscript extract** — [`THEOREM-H-STATEMENT-AND-PROOF.md`](./THEOREM-H-STATEMENT-AND-PROOF.md). Object under review, not a claimed theorem.
2. **Mathematical corrections** — [`SND-MATH-CORRECTIONS-2026-09-15.md`](./SND-MATH-CORRECTIONS-2026-09-15.md). Displayed \(|\Pi_{j_*}|\) fails at fixed \(M\); valid \(F_j\) lemma; exact shell equation.
3. **25 August adversarial review** — [`ARCHON-PANEL-ADVERSARIAL-VERDICT.md`](./ARCHON-PANEL-ADVERSARIAL-VERDICT.md), [PR #35](https://github.com/simons357/Ship_it_app/pull/35), plus 15 Sep erratum.
4. **This briefing**.

Cite for public framing: [10.5281/zenodo.22050976](https://doi.org/10.5281/zenodo.22050976) (label, not verification).

**Replacement wording:**

> In the supplied extract, Theorem H is not established even with \(X\le M\). Its proof drops a viscous tail, uses invalid Sobolev embeddings and does not provide a complete Bony decomposition. The displayed absolute-flux estimate fails on smooth fixed-enstrophy shear fields. A valid \(M\)-dependent bound for the nonlinear shell term can be proved separately, but its usefulness for SND propagation remains to be shown. Any SND floor asserted from time zero must respect the initial spectral distribution. Retain the spectral toolkit and rebuild the required estimate from the exact shell evolution.

---

## 10. Bottom line for the reviewer

Jonathan Simons has a **conditional spectral regularity program** for **unforced** 3D Navier–Stokes on \(\mathbb{T}^3\). The displayed Theorem H absolute-flux estimate is **not established**, even with \(X\le M\). A simpler \(M\)-dependent bound on \(F_j\) is valid and does not give the proposed propagation. Rebuild from the exact shell equation. Keep spectral research.

[SND] as a per-solution extra hypothesis is not equivalent to Clay: the regularity implication is itself unproved, and a uniform floor from \(t=0\) is obstructed.

**Forced C/D** have a public announcement (8 Sep) under Clay evaluation (11 Sep). That does not decide **unforced (B)** (smooth periodic \(u_0\), \(f\equiv 0\)), which is **not claimed**.

**No unforced Statement (B) claim. Clarification progress, not closure of (B).**

---

## Appendix A — symbol card (fluids only)

| Symbol | Meaning |
| --- | --- |
| \(X_j\) | LP enstrophy (or, in the energy-shell note, energy) in shell \(j\) — **say which** |
| \(X\) | \(\sum_j X_j\asymp\|\nabla u\|_2^2\) in general LP; equality on the exact-block family |
| \(J\) | \(\max_j X_j\) |
| \(\rho\) | \(J/X\) |
| \(j_*\) | \(\arg\max_j X_j\) |
| \(\Pi_j\) | manuscript \(F_j-S_j\); do not identify with \(F_j\) |
| \(F_j\) | \(\langle(u\cdot\nabla)u,\Delta_j^2 u\rangle\) |
| \(S_j\) | viscous tail \(\nu\sum_{k>j}2^{2k}\|\Delta_k\nabla u\|_2^2\ge 0\) |
| \(M\) | a priori enstrophy ceiling (the circular input) |
| \(\Lambda\) | Stokes-moment quotient \(Y/X\) — **not** \(\rho\) |
| \(\mathcal{R}_\star\) | Lemma★ shape ratio — **not** the spectral-shift identity |
| \(\Phi\) | swirl \(u_\theta/r\) — **not** DA gravitational \(\Phi\), not Paper2 shell \(\Phi_j\) |
| \(H_N\) | inverse-GCD matrix — **not** Theorem H |

## Appendix B — one-sentence answers the reviewer will ask

**Is SND proved?** No. Per-solution extra hypothesis. A uniform floor from \(t=0\) is obstructed.

**Does SND imply regularity?** Not on this manuscript. Theorem D is a sketch.

**Is [SND] equivalent to Clay?** No.

**Is the displayed Theorem H proved under \(X\le M\)?** No. Absolute-value bound fails on high-tail shears; proof drops \(S_j\) and uses invalid embeddings.

**Should spectral be dropped?** No. Rebuild from the exact shell equation.

**Are you claiming unforced Clay (B)?** No. Official (B) is smooth periodic \(u_0\) with \(f\equiv 0\).

**Do OpenAI C/D close your target?** No. Those statements allow a force. Clay’s 11 September note is evaluation, not an award.

**What is the next estimate?** The boxed shell equation, then an \(F_j\) (or \(\Pi_j\)) bound that survives shears, amplitude, and equal shells — **not** glued to Door B.
