# Theorem H — Gap Attack Plan

**Author program:** Jonathan R. Simons / Harmonic Blueprint  
**Date:** 2026-08-25  
**Builds on:** [`ARCHON-PANEL-ADVERSARIAL-VERDICT.md`](./ARCHON-PANEL-ADVERSARIAL-VERDICT.md)  
**Tone lock:** attack the *gap*, not the competitor with fake Clay closure.

---

## 0. Frozen definitions (do not blur)

| Symbol | Definition |
| --- | --- |
| \(X(t)\) | \(\|\nabla u(t)\|_{L^2}^2\) (enstrophy / \(H^1\) square) |
| \(X_j(t)\) | shell enstrophy in dyadic shell \(S_j\) |
| \(J(t)\) | \(\max_j X_j(t)\) |
| \(\rho(t)\) | \(J(t)/X(t)\) |
| \(c_*\) | putative positive floor for \(\rho\) |

### SND-U (needed for Clay Statement B)

**Unconditional Spectral Non-Dispersal:**

\[
\inf_{t\ge 0}\, \frac{J(t)}{X(t)}\ \ge\ c_*>0
\]

for **all** (suitable) Leray–Hopf / \(H^1(\mathbb{T}^3)\) data, with \(c_*\) produced from \(\|u_0\|_{H^1}\) and \(\nu\) **without** an a priori ceiling \(X\le M\).

**Status:** **OPEN / HYPOTHESIS.** Not proved in the available manuscripts.

### SND-C (what Theorem H actually proves)

**Conditional shell-flux control** in the *spread* regime \(\rho\le\rho_0\ll 1\), under hypotheses that include:

- \(X\ge\delta_*>0\),
- **\(X\le M\)** (a priori enstrophy ceiling),
- geometric / structure constants \(C_S\), viscosity \(\nu\),

yielding a bound on dominant-shell flux \(\Pi_{j_*}\) with

\[
C_*=C_*(\nu,\delta_*,M,\rho_0,C_S).
\]

**Status:** **CONDITIONAL toolkit object.** Legitimate research lemma. **Circular for Clay B** because Clay B is precisely the problem of producing uniform \(H^1\) control from data alone.

### Clay Statement (B)

Global regularity for (suitable) \(H^1\) data on \(\mathbb{T}^3\) without an extra unproved structural hypothesis such as SND-U or an a priori \(X\le M\).

**Status:** **NOT resolved.** KEEP framing: Zenodo `22050976`. PARK packaging: `20405526`.

---

## 1. Lemmas that *almost* close the gap — and where each fails

| Piece | What it almost does | Where it fails for SND-U / Clay B |
| --- | --- | --- |
| **Theorem H (as written)** | Controls \(\Pi_{j_*}\) when \(\rho\) is small | Assumes \(X\le M\). That is the conclusion Clay needs, smuggled as hypothesis (**Gap H1**). |
| **Theorem G** | (SND-C) ⇒ \(\rho\ge c_*\) | \(c_*\) still depends on \(M\). Does not remove the ceiling (**Gap H3**). |
| **Dominant-shell “propagation”** | ODE argument \(\dot\rho>0\) when \(\rho\) small | Runs under (SND-C)+\(M\)-dependent constants, not for all Leray–Hopf data (**Gap H4**). |
| **Ring Lemma + BVB/CF on \(E_c\)** | Band-limited geometric control of vorticity direction | Hypotheses: Fourier support in one shell; Lipschitz direction on \(E_c\). Does **not** give global CF or SND-U for arbitrary fields. |
| **Phi-renormalization** | Cancels \(1/r^4\) axis term in axisymmetric swirl | Algebraic method note. Does **not** feed unconditional 3D Clay; do not route Phi → Theorem H. |
| **Q1 hyperdissipative approx.** | Smooth approximants → Leray–Hopf idea | SND / \(H^1\) bounds need not survive \(\varepsilon\to 0\) without a separate limit theorem (**Gap H7 / Q1**). |
| **Small-data / short-time / bounded-\(H^2\) regimes** | Honest local SND-type control | Not large-data closure. Publish carefully; do not green as Main Theorem. |
| **\(c_*=6/\pi^2\)** | Clean arithmetic constant (\(\zeta(2)^{-1}\)) | Number-theoretic analogy / Triple Lock packaging. **Not** a proved continuum NS floor (**Gap H5**). |
| **Claim-paper Main Theorem / Q6 glue** | Appears to enforce SND dynamically | Relies on withdrawn Bridge / inverse-GCD damper story (**Gap H6**). |

**One-line lock (from adversarial verdict):** Theorem H ≠ unconditional SND. \(X\le M\) remains the keystone gap.

---

## 2. Attack routes (ranked by plausibility)

### Route 1 — Bootstrap: remove \(X\le M\) by closing a self-improving estimate *(top pick)*

**Idea.** Treat \(M\) as a *bootstrap ceiling*: assume \(X\le M\) on \([0,T_*)\), derive from SND-C + energy/enstrophy inequalities a stricter bound \(X\le M/2\) (or \(X\le M_0(\|u_0\|_{H^1},\nu)\)) that depends only on data, then continue.

**Why ranked #1.** This is the classical fluids bootstrap pattern. It attacks Gap H1 head-on without inventing new arithmetic glue. If it works, SND-C upgrades toward SND-U (or at least toward a data-only \(M\)).

**Hard part.** The constants \(C_*(M)\) and Theorem G’s \(c_*(M)\) typically *worsen* with \(M\). You need a quantitative regime where the improvement beats the degradation — or a different coercive quantity than raw \(X\).

**Falsifiable next step.** Write an explicit bootstrap lemma: “If \(X\le M\) on \([0,T)\) and (SND-C) holds with parameters \((\nu,\delta_*,M,\rho_0)\), then \(X\le \Phi(u_0,\nu)\) independent of the artificial \(M\).” Exhibit \(\Phi\) or prove it cannot exist under current estimates.

### Route 2 — Dominant-shell propagation without a priori \(M\)

**Idea.** Strengthen the \(\dot\rho\) ODE so that when \(\rho\) is small, influx into the dominant shell is controlled by dissipation *and* a data-only bound (energy, Beale–Kato–Majda-type integrals, or shell-local structure), not by \(X\le M\).

**Why #2.** Closest to the papers’ narrative (“dominant shell propagates”). Competitors will claim this first if they can.

**Hard part.** Flux \(\Pi_{j_*}\) estimates currently leak \(M\)-dependence through Littlewood–Paley constants and high-mode interactions. Propagation under (SND-C) is already conditional; removing \(M\) is the same gap in ODE clothing.

### Route 3 — Weak-\(*\) / weak limit of Q1: pass SND to Leray–Hopf

**Idea.** Prove that if Q1 approximants satisfy uniform SND (or uniform \(X\le M_0(u_0)\)), the limit inherits \(\rho\ge c_*\) (or at least a useful lower density of shell mass).

**Why #3.** Turns approximation technology into a Clay-relevant limit theorem. Clean, refereeable target even if full Clay stays open.

**Hard part.** Weak limits can disperse energy across shells. Uniform SND may fail to pass without strong compactness you do not have. Must not silently use smoothness of the limit.

### Route 4 — Enstrophy barrier / conditional BKM-style estimates

**Idea.** Recast SND as a spectral form of a BKM/LPS criterion: bound \(\int \|\omega\|_{L^\infty}\) or a shell-weighted substitute by controlling \(\rho\) and dissipation. Publish the *conditional* chain airtight: **SND-U ⇒ regularity** with no circular \(M\).

**Why #4.** Even without proving SND-U, an airtight conditional theorem is a depositable asset competitors cannot dismiss. Aligns with KEEP `22050976`.

**Hard part.** This does **not** close Clay B by itself. It sharpens the criterion. Win condition: no referee can find a circular hypothesis in the SND⇒regularity arrow.

### Route 5 — Negative result: exhibit (or rigorously obstruct) SND failure *(still a win)*

**Idea.** Either (a) construct / numerically evidence a Leray–Hopf (or Euler) scenario where \(\rho(t)\to 0\) while \(X\) grows, or (b) prove that *any* proof of SND-U via the current Theorem-H pathway must smuggle an equivalent of \(X\le M\).

**Why #5.** A sharp negative or obstruction paper beats a fake positive. It also kills competitors who green Theorem H as Clay.

**Hard part.** Blowup constructions are hard; numerical probes are not proofs. Frame honestly as obstruction / stress test.

---

## 3. Competitor kill criteria

A rival “beats” this program only if they can claim **at least one** of:

1. **SND-U proved** for all relevant \(H^1(\mathbb{T}^3)\) data with \(c_*\) independent of an a priori \(X\le M\), *and* a clean SND⇒regularity arrow; **or**
2. **An equivalent structural law** (different name) that yields Clay B without circular ceilings; **or**
3. **A refereed obstruction** showing SND-U is false, with a clear replacement criterion.

### How the KEEP package blocks them

| Asset | Blocking function |
| --- | --- |
| KEEP DOI `22050976` (Ring + SND hypothesis) | Public, timestamped honest claim surface. Errata banners stay out of the title. |
| PARK `20405526` (Statement B packaging) | Prevents rivals from citing your withdrawn green table as your current claim. |
| Adversarial verdict + this attack plan | Pre-empts “Theorem H = SND-U” marketing. Anyone repeating the favorable panel’s packaging is fighting *your* audit trail. |
| Domain Architect SND inventory (`SND-U` open, `SND-C` conditional, Clay B unresolved) | Overclaims die in audit; tooling refuses “unconditional regularity” routing. |
| Zenodo clean-title remediation | Deposit survives metadata scrubbing; competitors with banner-poisoned titles look worse. |

**If a rival deposits “Clay B solved via Theorem H” without removing \(X\le M\), your kill shot is one paragraph:** Theorem H as written assumes the enstrophy ceiling Clay B is supposed to produce.

---

## 4. Explicit non-goals

- Do **not** claim Clay Statement (B) is resolved.
- Do **not** invent fake ARCHON / Tao panel consensus as peer review.
- Do **not** smuggle \(c_*=6/\pi^2\) as the continuum SND floor.
- Do **not** revive Triple Lock / Q6 / Bridge as NS glue.
- Do **not** pretend numerics prove Theorem H or SND-U.
- Do **not** green “Theorem H: (SND-C) unconditionally” as “SND for all data.”

---

## 5. 48-hour math checklist (attack Route 1)

1. Extract the exact dependence of \(C_*\) and \(c_*\) on \(M\) from `20518057` / claim paper.
2. Write the bootstrap lemma statement (even if unproved) with all constants explicit.
3. Identify the worst \(M\)-power in the flux estimate; try to replace it by energy + dissipation.
4. Parallel note: airtight **SND-U ⇒ regularity** (Route 4) as fallback depositable win.
5. Only after the math note is frozen: apply Zenodo metadata with token; re-deposit KEEP PDF if needed.

**Success metric for the honest race:** sharpest public statement of the gap + sharpest attack path + clean KEEP package — not a fake Millennium checkbox.
