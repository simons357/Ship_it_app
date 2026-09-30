# Navier-Stokes Brute-Force Extraction Ledger

**Project:** Simons Navier-Stokes / SND / Ring Lemma / Route N  
**Purpose:** Deduplicate recovered fragments and isolate only material that can advance a rigorous classical Navier-Stokes bridge.  
**Status labels:** **KEEP** (rigorous/useful), **REPAIR** (promising but incorrect or incomplete), **CONTEXT** (standard background), **DROP** (metaphor, duplicate, or mathematically unusable).

## Current bridge target

For a matrix cutoff (M), distinguish it from the number (L(M)) of dyadic shells and write

\[
H_M[a]=\sum_{j=0}^{L(M)-1}a_jB_{M,j},\qquad a_j\ge0,\qquad \sum_j a_j=1.
\]

The candidate Route N bypass is the elementary convexity bound

\[
\lambda_{\min}(H_M[a])
\ge \sum_j a_j\lambda_{\min}(B_{M,j})
\ge \min_j\lambda_{\min}(B_{M,j}).
\]

Thus a uniform shellwise theorem

\[
B_{M,j}\succeq\left(-\frac12+\delta\right)I
\quad\text{for every }M,j
\]

would eliminate the dynamic simplex-stability, dominant-shell ratio, and eigenvalue no-crossing problems for this auxiliary operator. It would **not by itself** prove Navier-Stokes regularity; a separate PDE theorem must show that this GCD quadratic form controls the actual vortex-stretching or shell-transfer functional.

## Batch 001 - Screenshot archive

| Files | Extracted content | Status | Disposition |
|---|---|---:|---|
| IMG_0816-0818 | Chladni/sand analogy linking viscosity, RH tuning, Goldbach gaps, and NS blowup | DROP | Metaphorical visualization; no inequality or operator derivation. |
| IMG_0900-0905 | Historical audit questions about SFE/UHF/DHFA, prime controls, coherence, damping, and prediction | CONTEXT | Useful as an audit checklist, not proof material. |
| IMG_0918-0919 | Explicit contradiction: a positive-semidefinite raw GCD matrix was also assigned a negative eigenvalue | **KEEP** | Confirms that raw GCD, Mobius-decorated, centered, normalized, and shell-weighted matrices must receive separate notation. |
| IMG_0962-0969 | Classical vorticity equation, LP decomposition, Bony splitting, geometric depletion, claimed BKM closure | REPAIR | Correctly locates vortex stretching as the obstruction. The claimed closure assumes the unproved alignment estimate and misuses the energy budget. |
| IMG_0981-0985 | Standard energy/enstrophy/scaling/BKM overview | CONTEXT | Accurate at the conceptual level; no new bridge estimate. |
| IMG_5503, 5508, 5510 | Hexagonal lattice, torus, critical-line, and micro-vortex narrative | DROP | Speculative geometry; no established map to NS or the arithmetic operator. |

## Batch 002 - Three-page Ring Lemma brief

**Files:** `PDF document.pdf`, `PDF document(1).pdf`, `PDF document(20260822-142604).pdf`  
**Recovered title:** *A Bound on the Vorticity Direction Field via Finite Triad Geometry on T3*.

### Extracted claims

1. For a single LP shell (S_{j_*}), define
   \[
   E_c=\{x:|\omega(x)|\ge c,2^{j_*}\|u\|_2\}.
   \]
2. Claim
   \[
   \|\nabla(\omega/|\omega|)\|_{L^\infty(E_c)}\le C2^{j_*}.
   \]
3. Use the claimed single-shell direction bound in a spread/concentrated dichotomy and then invoke a prime-indexed (Q_6) damping operator to claim global regularity for a threshold class.

### Audit

| Component | Status | Reason |
|---|---:|---|
| Single-shell identity (\nabla\xi=(I-\xi\otimes\xi)\nabla\omega/|\omega|) | **KEEP** | Correct wherever (\omega\ne0). |
| Finite lattice support on (\mathbb T^3) | **KEEP** | True, but finiteness alone does not give a scale-uniform constant. |
| Bernstein line (\|\nabla\omega\|_\infty\lesssim 2^{2j_*}\|u\|_2) | **REPAIR** | In three dimensions the standard estimate is (\|\nabla\omega\|_\infty\lesssim2^{7j_*/2}\|u\|_2). The draft omits the (2^{3j_*/2}) lattice-volume factor. |
| Division by the stated (E_c) threshold | **REPAIR** | With the correct Bernstein scaling it yields (\|\nabla\xi\|_\infty\lesssim2^{5j_*/2}), not (2^{j_*}). |
| Transfer from a dominant shell to the full vorticity direction | **OPEN** | An (L^2) remainder is not pointwise control; high-frequency tails can dominate (\nabla\xi). |
| Constantin-Fefferman closure from a bounded angle | **DROP as written** | The displayed conclusion only makes a dimensionless angle bounded, which is already trivial. The required high-vorticity coherence/integrability condition is not established. |
| Use of (Q_6) damping in a theorem about classical NS | **DROP as written** | A nonzero damping operator changes the equation. Removal/de-augmentation requires a uniform limiting estimate. |
| Threshold-class theorem | **CONTEXT** | The stated (H^1)-smallness class is in the territory of classical small-data regularity; the supplied new proof chain is not valid. |

### Batch verdict

**Relevant but not the bridge.** Preserve the single-shell direction identity and the exact point where a pointwise tail estimate is needed. Do not reuse the claimed Bernstein exponent, the full-flow transfer, or the (Q_6)-assisted classical conclusion.

### Salvaged single-shell lemma

The intended Lipschitz estimate becomes correct after replacing the (L^2)-normalized high-vorticity set by a sup-normalized set:

\[
E_{c,\infty}=\{x:|\omega(x)|\ge c\|\omega\|_\infty\},\qquad 0<c<1.
\]

For a field supported in one dyadic shell, Bernstein in the form

\[
\|\nabla\omega\|_\infty\le C2^{j_*}\|\omega\|_\infty
\]

and

\[
\nabla\left(\frac{\omega}{|\omega|}\right)
=\frac{(I-\xi\otimes\xi)\nabla\omega}{|\omega|}
\]

give

\[
\|\nabla\xi\|_{L^\infty(E_{c,\infty})}
\le \frac{C}{c}2^{j_*}.
\]

Because the torus is compact and a nonzero trigonometric polynomial attains its maximum, (E_{c,\infty}) contains a neighborhood of a maximizer and has positive measure. This is a valid single-shell result. It does not supply a cutoff-uniform lower bound on that measure, control the full-flow vorticity direction, or by itself verify a Constantin-Fefferman/BVB space-time criterion.

## Route N finite computation checkpoint

For the Mobius-decorated, degree-normalized matrix and shell matrices exactly as written in `Paper2_NS_Regularity_SND_FIXED.tex`, direct diagonalization gave:

| Matrix cutoff (M) | Worst tested shell eigenvalue | Margin above (-1/2) |
|---:|---:|---:|
| 16 | -0.249891 | 0.250109 |
| 32 | -0.259314 | 0.240686 |
| 64 | -0.267348 | 0.232652 |
| 100 | -0.253363 | 0.246637 |
| 200 | -0.258468 | 0.241532 |
| 400 | -0.261906 | 0.238094 |
| 800 | -0.265787 | 0.234213 |
| 1023 | -0.287991 | 0.212009 |
| 1600 | -0.268738 | 0.231262 |

This is numerical evidence, not a uniform analytic theorem. It also exposes a definition mismatch: the written uniform shell average does not reproduce the frozen eigenvalue near (-0.297) claimed elsewhere. The matrix cutoff, shell count, normalization, and reference weights must be disentangled before theorem writing.

## Active mathematical obligations

1. **Arithmetic shell theorem:** prove or refute (B_{M,j}\succeq(-1/2+\delta)I) uniformly in (M,j).
2. **Operator-definition repair:** separate the raw GCD matrix, Mobius-decorated matrix, degree-normalized matrix, and time-dependent shell-weighted operator.
3. **PDE bridge:** derive an exact inequality connecting the arithmetic quadratic form to the signed NS tail-transfer or vortex-stretching functional, with constants uniform in cutoff.
4. **Classical-equation integrity:** do not use nonvanishing (Q_1,Q_3,Q_6) damping inside a conclusion about unaugmented NS without a uniform removal theorem.

## Batch 003 - Full conditional SND/Ring-Lemma manuscript

**Recovered title:** *Conditional Regularity for the Standard 3D Incompressible Navier--Stokes Equations via Spectral Non-Dispersal and the Ring Lemma*.

### Decisive audit

| Claim or step | Status | Reason |
|---|---:|---|
| LP definitions and projected transfer functional | **KEEP** | Standard after retaining quasi-orthogonality constants. |
| “Exact” shell balance with dissipation coefficient \(2^{2j}\) | **REPAIR** | For a smooth LP block the exact coefficient is \(q_j=\|\nabla\Delta_j u\|_2^2/\|\Delta_j u\|_2^2\), only comparable to \(2^{2j}\). |
| Borromean transfer bound \(|\mathcal T_j|\le C2^jE_j\sqrt{1-\kappa_j}\) | **DROP** | It violates amplitude homogeneity: \(\mathcal T_j[Au]=A^3\mathcal T_j[u]\), while the proposed right side scales like \(A^2\). The low--high commutator coefficient \(\|\nabla S_{j-2}u\|_\infty\) is also left uncontrolled. |
| Kinetic-shell SND \(\sup_j E_j/E\le\kappa^*<1\) controls singularity formation | **OPEN / insufficient as stated** | A high shell may carry small kinetic energy but large enstrophy \(2^{2j}E_j\). The condition does not control the critical tail. |
| Full-flow Ring Lemma | **DROP as proved** | Dominance in kinetic energy does not imply dominance in vorticity; the high-frequency tail is not pointwise controlled; high vorticity at a center does not make an entire dyadic ball a high-vorticity set. |
| Periodic Biot--Savart and endpoint strain estimate | **REPAIR** | The torus kernel is periodic, not the displayed Euclidean kernel. Calderón--Zygmund operators map \(L^\infty\) to BMO, so any logarithmic endpoint estimate requires its precise hypotheses. |
| CF time-integrability through \(E_{\min}>0\) | **DROP** | \(E_{\min}:=\inf_t E_{j^*(t)}(t)>0\) is assumed, not derived. The SND upper bound supplies no such lower bound. |
| Higher-order “Gronwall” step | **DROP** | The displayed inequality is Riccati-type, \(y'\lesssim y^2\), and a uniform \(H^1\) bound alone does not make it a Gronwall estimate. |
| BKM closure | **DROP** | In three dimensions \(\|\omega\|_\infty\lesssim\|\nabla\omega\|_2\) is false; the claimed Sobolev embedding is one derivative short. |

### Batch verdict

**Bridge-critical but not valid as a conditional theorem in its present form.** The amplitude-scaling contradiction alone invalidates the proposed transfer lemma. Preserve the LP setup, the exact transfer definition, and the repaired one-shell direction lemma. Any replacement SND criterion must control a scale-critical enstrophy or signed tail quantity and must carry the necessary amplitude dependence.

## Batch 004 - ARCHON NS final-review panel sheet

### Classification

| Item | Status | Reason |
|---|---:|---|
| Named panel and “consensus verdict” | **DROP as evidence** | The sheet documents hypothetical review roles, not authenticated reviews or endorsements by the named mathematicians. |
| Displayed SND condition \(X(t)\ge c_*J(t)\) | **DROP as a regularity mechanism** | If \(J=\max_j X_j\) and \(X=\sum_jX_j\), then \(J\le X\), so the inequality is automatic for every \(0<c_*\le1\). |
| Reverse dominant-shell condition \(J(t)\ge c_*X(t)\) | **OPEN and non-universal** | This is the nontrivial direction, but no universal positive \(c_*\) can hold for all \(H^1\) data: smooth data can distribute comparable enstrophy among arbitrarily many shells. |
| \(c_*=6/\pi^2\) from coprime density | **DROP** | Coprime integer density is not a derived lower bound for arbitrary NS shell-energy distributions. |
| Theorem H unconditional propagation | **NOT ESTABLISHED HERE** | The panel sheet states the desired result but supplies no proof of dominant-shell propagation. |
| \(E_c\)/CF/BVB closure | **UNVERIFIED** | The sheet asserts the conclusion but does not provide the pairwise coherence and weighted space--time estimates needed for audit. |
| Exact document handles | **KEEP** | Search for `Theorem-H`, `Appendix-app:Ec`, `NS_PROOF_CHAIN.html`, and `NS_FINAL_MERGED_UNCONDITIONAL.tex`. |

### Batch verdict

**Useful provenance and search index; no new mathematical closure.** The sheet cannot support an unconditional claim, and the listed “panel verdicts” must not be represented as statements by those people without direct confirmation.

## Batch 005 - Master research manifest

**File:** `MASTER_RESEARCH_MANIFEST.md`  
**Prepared:** August 14, 2026.

### Extracted status

| Manifest item | Status | Extraction consequence |
|---|---:|---|
| `Simons_NS_Paper2_SND_GNC_REPAIRED_2026.tex` designated controlling manuscript | **KEEP as provenance** | This is the next exact source target; the manifest itself says it is conditional, not an unconditional NS proof. |
| August 1 conditional audit | **KEEP** | Confirms that general unaugmented Leray--Hopf SND/simplex stability remains open. |
| Route J | **KEEP as numerical lead** | Explicitly classified as numerical/analytically incomplete; it cannot be promoted to a theorem without the missing uniform estimate. |
| Frozen spectral-gap implication | **CONDITIONAL** | A finite/static operator statement does not by itself control the time-dependent NS flow. |
| June 10 Archon and April 29 computational reports | **HISTORICAL** | Preserve for chronology only; epsilon-uniform numerics do not prove the epsilon-zero PDE bridge. |
| App inventory | **KEEP as operational index** | Identifies Archon Fluids Analysis, NavierLens, ShellFlow Dynamics, TriadFlow, Q-Regular Viewer, and NAV42 as possible code/data sources. |
| Bundle folder map | **KEEP as recovery map** | Highest-value targets are `01_latest_ns/` and `02_routej_bridge/`; `03_archon/` is useful mainly for numerical harnesses. |

### Availability check

The exact controlling TeX filename was not recovered as a standalone Library item in the current search. The only exact match is this manifest. Therefore the folder map is valuable, but the underlying bundle or `01_latest_ns/` and `02_routej_bridge/` contents are still required for a theorem-level audit.

### Batch verdict

**Highly relevant organizational evidence, but not a proof source.** It corroborates the ledger's controlling conclusion: the live mathematical target is the uniform-in-time dynamical bridge for classical, unaugmented NS. It also prevents older “unconditional” artifacts from overriding the later conditional audit.

## Batch 006 - QNAV Geometry Suppression Lab vortex export

**Generated:** April 16, 2026  
**Configuration:** \(64\times64\) grid, \(\Delta t=0.16\), \(\nu=0.035\); coherence gain \(0.22\), NAV42 gain \(0.15\), prime gain \(0.09\).

### Data-integrity audit

| Export component | Status | Consequence |
|---|---:|---|
| Time-series schema | **KEEP as recovery metadata** | Lists vorticity, alignment, GB, normalized GB, stretching, and enstrophy fields for NS/NAV42/QNAV42. |
| Time-series observations | **EMPTY** | No data rows follow the header, so no cross-model calculation or plot is possible. |
| Vortex registry | **EMPTY** | All models report zero tracked and zero active vortices with zeroed summary statistics. |
| Individual/proxy records | **EMPTY** | Both record tables contain headers only. |
| Geometry-suppression conclusion | **UNTESTED** | An empty tracker is neither evidence of suppression nor evidence against it; initialization, execution, detection threshold, or export may have failed. |

### Batch verdict

**Operational lead only.** Preserve the parameters and schema to identify the producing Archon/QNAV lab, but exclude this export from all numerical-evidence tables. A usable rerun must contain actual time rows, nontrivial initial-condition metadata, tracker thresholds, model equations, and preferably raw field snapshots or checksums.

## Batch 007 - Q1-augmented regularization announcement draft

### Claim audit

| Promotional claim | Status | Required correction |
|---|---:|---|
| Global smooth solutions for the augmented system | **POTENTIALLY KEEP** | State the exact augmented PDE, parameter range, datum class, and whether constants depend on the augmentation parameter. This is not classical NS regularity. |
| Uniform \(H^1\) bounds | **AMBIGUOUS** | Uniform in time for fixed augmentation is different from uniform as \(\varepsilon\to0\). Only the latter could support removal, and that estimate is not established in the recovered audit. |
| Strong \(H^1_{\mathrm{loc}}\) convergence in the regularization limit | **DROP unless independently proved** | Such convergence would transfer the decisive derivative control. The recovered Q1 audit instead identifies degeneration as \(\varepsilon\to0\) and leaves removal open. |
| Prevention of CSTY fast blow-up rates in axisymmetric swirl | **REPAIR / contextualize** | A modified dissipative equation may suppress those scenarios without proving regularity for the unmodified axisymmetric-swirl problem. |
| Arbitrary vortex stretching controlled in the full non-axisymmetric setting | **DROP as stated** | This is essentially the unresolved 3D mechanism unless the claim is restricted to the augmented PDE with an explicit coercive estimate. |
| CKN partial regularity upgraded to full regularity | **RETRACT** | The later Q1 revision explicitly retracts the logarithmic CKN improvement; full regularity for the augmented system does not strengthen CKN for suitable weak solutions of classical NS. |
| Directly overcomes Tao's supercriticality barrier | **OVERSTATED** | Extra dissipation changes the equation. It demonstrates a regularization mechanism, not a resolution of the classical barrier. |
| Numerical superiority to mollification/hyperdissipation | **UNVERIFIED** | Requires a defined benchmark, matched resolution and dissipation, reproducible data, and quantitative error/stability metrics. |

### Batch verdict

**Historical promotional artifact.** Its defensible scientific core is a fixed-augmentation regularity theorem, if the exact energy estimate checks out. It supplies no epsilon-zero removal theorem and therefore no classical Navier--Stokes closure. Do not repost this wording without a claim-boundary rewrite.

## Batch 008 - Prime Harmonics / DHFA paper

**Classification:** **DROP from the NS extraction.** The paper contains no Navier--Stokes equation, vorticity estimate, shell-transfer bound, SND propagation theorem, or arithmetic-to-PDE bridge.

Preserve only as early UHF/DHFA historical provenance. Its reported prime-resonance alignment is not independent evidence because the proposed potential already contains an explicit sum over primes. The stated 81.7% result has no supplied null model, selection rule, code, dataset, or multiple-testing control, and the quantum, gravitational, black-hole, and consciousness claims are speculative rather than derived.

## Batch 009 - Q1 axisymmetric regularity paper

**File:** `qstack regularity paper(20260822-143521).pdf`.

### Decisive defects

1. **The displayed Q1 term has the wrong form and sign.** The paper writes
   \[
   \partial_tu+(u\cdot\nabla)u=-\nabla p+\nu\Delta u-\varepsilon^\alpha|\nabla u|^\beta\Delta u.
   \]
   With the standard negative-definite Laplacian convention used for \(\nu\Delta u\), the last term is anti-diffusive when its coefficient is frozen. Moreover,
   \(-|\nabla u|^\beta\Delta u\) is not the divergence-form operator
   \(-\nabla\cdot(|\nabla u|^\beta\nabla u)\); integration by parts produces an additional derivative-of-coefficient term with no fixed sign. Thus the claimed identity
   \(\varepsilon^\alpha\int|\nabla u|^{\beta+2}\) does not follow from the stated PDE.
2. **Uniform parabolicity does not prove global smoothness.** Classical 3D NS is already uniformly parabolic; continuation requires a global critical estimate. The argument for \(0<\beta<1/2\) is therefore invalid, and the Serrin calculation for the remaining range is not derived from the stated energy bound.
3. **The \(\Gamma\) maximum principle does not bound \(\Phi=u^\theta/r\).** The asserted \(\|\Phi\|_\infty\le C M_0/\nu\) is unsupported. The algebraic identity removing the written \(r^{-4}\) factor is true for smooth axis-compatible fields, but it supplies no independent bound on \(\Phi\).
4. **The stability damping uses a false lower bound.** Type-I information does not give the pointwise lower bound \(|\nabla u_\varepsilon|^\beta\ge\tau^{-\beta}\). For \(\beta<1\), \(\varepsilon\tau^{-\beta}\) is weaker than \(\tau^{-1}\) near \(\tau=0\), not stronger; the near-blowup inequality is reversed. Choosing energy weights proportional to \(1/\varepsilon\) also destroys the claimed epsilon-uniform equivalence.
5. **The contradiction step is invalid.** Strong \(L^2_tH^1_x\) convergence does not yield the asserted pointwise \(L^{\beta+2}\) lower bound, and \(\varepsilon\cdot\infty\) cannot be used as a limiting contradiction. Type-I/Type-II scenarios as defined are not an exhaustive classification of possible singular behavior.

### Salvage

**REPAIR, not discard.** The appropriate augmented model is a projected/divergence-form generalized viscosity,
\[
\partial_tu+(u\cdot\nabla)u+\nabla p
=\nu\Delta u+\varepsilon^\alpha\nabla\cdot(|\nabla u|^\beta\nabla u),
\qquad\nabla\cdot u=0,
\]
for which the extra energy contribution is genuinely dissipative. Fixed-parameter well-posedness must then be stated with the correct exponent range and generalized-Newtonian-fluid theory. It still would not provide an epsilon-uniform removal theorem.

## Batch 010 - March QStack framework report

**File:** `DuckDuckGo(20260822-143543).pdf`.

| Component | Status | Reason |
|---|---:|---|
| Explicit statement that de-augmentation is open | **KEEP** | Correctly separates a modified system from classical NS and identifies the missing uniform \(H^1\) estimate. |
| Resonant attractor \(\Omega_*\) | **UNPROVED** | Existence, invariance, compactness, and attraction are stated as proof sketches or deferred to SFE. |
| Coherence-viscosity floor \(c_\psi>0\) | **FALSE as universal statement** | The infimum can vanish, including at zero or configurations for which the defining source vanishes. |
| Prime-phase force | **UNDEFINED/REPAIR** | The complex phase multiplier, reality condition, divergence-free projection, convergence of the sum, and energy sign are not established. |
| Uniform vorticity bound and Lyapunov decay | **UNPROVED** | They are asserted rather than derived from coercive estimates. |
| Claimed \(512^3\) computation | **UNVERIFIED** | No raw fields, executable solver, logs, convergence study, or dataset accompany the figures. |

**Verdict:** retain Section 8's honest gap statement as provenance; do not treat the earlier QStack theorems or plots as verified.

## Batch 011 - QNAV Geometry Suppression Lab source

**File:** `QNavGeometrySuppressionLab(20260822-143526).pdf`.

This is a scalar stochastic recurrence/UI demonstration, not a spatial Navier--Stokes solver. “Plain NS” evolves clamped proxies \((E,\Omega,\text{alignment},\text{fragmentation})\); NAV42 and QNAV42 receive larger damping, geometry-break, redistribution, and fragmentation coefficients by construction. The models also use different random streams. Consequently their relative improvement is encoded in the update rules rather than discovered from a PDE computation.

The displayed geometric functional is also nearly tautological in the low-regularization limit: with the code's definitions, its ratio reduces approximately to the alignment proxy. **KEEP only as a product-interface prototype and experiment-design shell; DROP as numerical NS evidence.**

## Batch 012 - NAV42 provisional/IP manuscript and mechanism note

**Files:** `971eb1e3a_NAV42_FINAL_V3_WITH_FIGURES.pdf` and the “core mechanism of action” note.

**Cross-domain; exclude from the NS proof.** The potentially testable engineering hypothesis is that a passive compliant microstructured coating, driven by ambient structural vibration, may alter near-wall coherent-structure regeneration. The current documents do not establish drag reduction, phase-lock disruption, micron-scale sufficiency, or superiority over static surfaces. Statements that coherent vortices are the only reason turbulent drag persists, that static coatings necessarily fail because turbulence “learns” the wall, and that attractors cannot stabilize are advocacy language rather than demonstrated mechanics.

Preserve in the NAV42 IP/experimental program, with conventional material parameters and boundary-layer observables separated from SFE/UHF terminology.

## Batch 013 - April/May unconditional SND manuscript source

**File:** `Pasted text(20260822-143632).txt`.

This is the already-audited pre-V9 unconditional chain. In addition to the Theorem-H, Ring-Lemma, and classical/augmented-equation defects logged above, its Theorem I minimization is algebraically incorrect. Ignoring fixed positive constants, for
\[
F(N,\varepsilon)=\varepsilon N^{23/10}+\varepsilon^{5/13}N^{-13/10},
\]
direct differentiation gives
\[
N_{\rm opt}\asymp\varepsilon^{-20/117},\qquad
F_*(\varepsilon)\asymp\varepsilon^{71/117},
\]
not the exponents stated in the manuscript. Correcting this calculus does not create an \(H^1\) estimate because the two terms have not been rigorously derived as a cutoff-uniform classical-NS bound. The final proof also imports Q6 damping into the “concentrated regime,” thereby changing the PDE.

## Batch 014 - ARCHON Taylor--Green screenshot

**Run shown:** \(N=64\), \(\nu=0.05\), \(T=2\), 57 snapshots; reported maxima and means are of order \(10^{-15}\).

**Classification:** numerical-null diagnostic, not regularity evidence. Values at \(10^{-15}\) are floating-point roundoff and indicate that the numerator in the implemented \(C(T)=|N|/A\) diagnostic is being cancelled to machine precision for this symmetric test or by the implementation. A single Taylor--Green run at one resolution cannot support a general stretching-to-enstrophy inequality. Until the exact code and definition of \(N,A,D\) are recovered and checked on a manufactured nonzero case, this screenshot should be treated as a symmetry/bug detector.

## Batch 015 - Recovered `NS_FINAL_UNCONDITIONAL` HTML

**File:** `54db6d0ba_NS_FINAL_UNCONDITIONAL 2.html`.

This is the exact historical “complete proof” artifact previously missing. It confirms rather than repairs the defects already isolated:

- Q1 is again written as \(-\varepsilon^\alpha|\nabla u|^\beta\Delta u\) with the invalid dissipative identity.
- Theorem C is a proof sketch that simply asserts Phi cancellation absorbs the full difference nonlinearity; it does not supply the missing epsilon-uniform stability estimate.
- Theorem H repeats the abbreviated Bony/CCFS argument without the required low/high-tail summations and uses the same invalid shell estimates.
- The Ring Lemma repeats the incorrect three-dimensional \(L^2\to L^\infty\) Bernstein scaling and a backwards “measure bound via Chebyshev.”
- Theorem I contains the already-verified exponent error in its own derivative calculation.
- The final “classical” proof explicitly uses nonzero Q6 damping in the concentrated regime and nonvanishing Q3 transfer damping, so it proves neither the unaugmented equation nor an epsilon-zero removal theorem.
- Its statement that the infinite-bandwidth Gaussian Q6 reduces to a GCD-weighted coupling is unsupported: a flat Gaussian weight does not generate \(1/\gcd(j,k)\) arithmetic weights.

**Verdict:** **KEEP only as the definitive historical overclaim artifact.** It contains no later repair beyond the source already audited.

## Batch 016 - Recovered SND preservation tracker

**File:** `188c63c6e_snd_tracker 2.html`.

### Decisive provenance

The tracker is the strongest contemporaneous status record recovered. Its dashboard reports:

- **38% overall completion**;
- **3 of 9 lemmas closed**;
- **6 open problems** and **4 active gaps**;
- active critical items: de-augmentation, SND preservation, dominant-shell non-drift, and time-dependent spectral stability;
- blocked global regularity transfer because weak-solution identification/uniqueness is unavailable;
- the explicit journal statement: frozen Hamiltonian routes do not prove \(\lambda_{\min}(\widehat H_N(t))>-1/2\) along the actual NS flow, and “this is the real Clay gap.”

### Route/bypass extraction

The tracker names `NS_BYPASS_LEMMA.tex` and the normalized condition
\[
\|\widetilde H_N[u]-\widetilde H_N^\mu\|_{\rm op}=d_{\gcd}(a,\mu)<0.20.
\]
This is a valid finite-dimensional Weyl-style reduction once the operator is fixed. However, the tracker itself leaves one decisive step open: prove the AET/simplex bound uniformly in time for every admissible classical NS trajectory. Defining `SND_q` to be precisely \(d_{\gcd}<0.20\) does not prove that condition; it merely renames the dynamical bridge. Monte Carlo samples of random simplex vectors and an empirical AET maximum do not establish the uniform PDE theorem.

The standalone files `NS_BYPASS_LEMMA.tex` and `DYNAMIC_COEFFICIENT_STABILITY_LEMMA.tex` were not recovered in the current Library search; the only exact occurrence is inside this tracker.

### Batch verdict

**KEEP as controlling historical status evidence.** It directly resolves the archive contradiction: the “unconditional” HTML was an overclaim, while the tracker contemporaneously recorded the proof as incomplete. The most defensible recovered publication anchor is the later `NS_Regularity_Final_Polished.pdf`, whose own claim boundary states that it is a conditional criterion and does not resolve classical NS.

## Vortex-search closure

The vortex/SND archive sweep is complete for the supplied material. No hidden unconditional closure was recovered. The mathematically viable assets are the corrected single-shell direction lemma, the shell-spread/moment viewpoint, the finite normalized-operator computations, the explicit conditional SND formulation, and the no-cancellation Hardy reconstruction. The remaining classical-PDE bridge is still uniform dynamical control of the critical shell/tail quantity without Q1/Q3/Q6 enforcement.

## Batch 017 - Diffuse Cascade / effective triad participation

**Identified paper:** *Diffuse Cascade in 3D Navier--Stokes: Time-Resolved Evidence for Triad Equidistribution* (April 30, 2026; archived in the tracker as Zenodo DOI `10.5281/zenodo.19842061`). The supplied Overleaf build URL is access-restricted, so the full paper still needs to be attached for a line-by-line audit. This entry classifies the recovered abstract, tracker description, and the signed shell-triad data already present in the workspace.

### Mathematical asset

For nonnegative triad magnitudes $a_\tau$ contributing to a receiver shell $j$, set
\[
A_j=\sum_{\tau\in\mathcal T_j}a_\tau,
\qquad p_\tau=\frac{a_\tau}{A_j},
\qquad
N_{\mathrm{eff},j}=\frac{1}{\sum_\tau p_\tau^2}
=\frac{A_j^2}{\sum_\tau a_\tau^2}.
\]
This is a legitimate inverse-participation number. It gives the deterministic anti-concentration estimate
\[
\max_\tau p_\tau\le
\Big(\sum_\tau p_\tau^2\Big)^{1/2}
=N_{\mathrm{eff},j}^{-1/2}.
\]
Thus a large $N_{\mathrm{eff},j}$ rules out domination by one triad and quantifies the missing high--high concentration variable that Leray's energy inequality does not control.

### Exact limitation

Let the signed shell flux be
\[
\Pi_j=\sum_{\tau\in\mathcal T_j}s_\tau a_\tau,
\qquad |s_\tau|\le1.
\]
Large participation alone does not make $|\Pi_j|$ small: taking $s_\tau=1$ for every triad gives $|\Pi_j|=A_j$ for arbitrarily large $N_{\mathrm{eff},j}$. Therefore triad equidistribution of magnitudes is not equivalent to nonlinear cancellation.

The bridge needs a second, signed discrepancy/coherence estimate, for example
\[
\left|\sum_\tau s_\tau p_\tau\right|
\le C\,N_{\mathrm{eff},j}^{-1/2},
\]
with $C$ uniform in shell, cutoff/resolution, time, and admissible data, or an alternative time-integrated estimate strong enough to absorb the positive transfer into viscosity. That estimate is not supplied by Leray and is not implied by the definition of $N_{\mathrm{eff},j}$.

### Cross-check against the recovered signed-triad runs

The strictly dealiased pseudo-spectral tensor reconstructs direct nonlinear shell transfer to relative error near $10^{-16}$. With paired random phases and equal initial enstrophy density:

| Grid | Low-weighted mean peak $C_+$ | High-weighted mean peak $C_+$ | Low/high amplification |
|---:|---:|---:|---:|
| $24^3$ | 1.446 | 0.110 | 13.19 |
| $32^3$ | 1.578 | 0.154 | 10.24 |

Here $C_+$ is positive nonlinear enstrophy transfer normalized by total viscous removal. The low-weighted case is super-viscous at both resolutions, dominated by the donor ladder $(B_0,B_0)\to B_1$ and $(B_0,B_1)\to B_2$. The extended $24^3$, $t=1$ run reaches mean peak $C_+=1.676$ and mean net ratio $1.375$. These data show that shell ordering and signed donor geometry materially affect transfer. They do not establish a universal inequality, but they also prevent replacing signed flux control by an unsigned equidistribution statistic.

### Claim repair

| Claim | Status | Defensible replacement |
|---|---:|---|
| Triad amplitudes “remain equidistributed across shells and time” | **TOO BROAD pending full protocol** | State the tested grids, initial data, viscosities, time windows, normalization, and uncertainty; call the result time-resolved numerical evidence of anti-concentration in those runs. |
| $N_{\mathrm{eff},j}$ identifies a variable missing from Leray control | **KEEP** | This is the paper's strongest structural contribution. |
| Large triadic participation prevents blowup | **OPEN** | Requires the signed discrepancy estimate and a scale/cutoff-uniform absorption argument. |
| Equidistribution proves SND/Theorem H | **NOT ESTABLISHED** | A numerical participation bound neither propagates SND for all data nor controls signed high--high flux. |
| “Enforce” participation in classical NS | **REPAIR** | For the unmodified equation, participation must be derived or conditionally assumed; enforcing it changes the PDE. |

### Batch verdict

**KEEP as one of the strongest numerical/structural papers in the program.** It cleanly introduces an anti-concentration observable and isolates high--high triadic concentration as a real obstruction. It does not close the classical problem because magnitude participation and signed cancellation are distinct. The sharp next bridge is a cutoff-uniform theorem coupling $N_{\mathrm{eff},j}$ to signed phase/discrepancy control and viscous absorption.
## Batch 018 — Q6/coherence paper and the missing signed-flux variable

### Source

- `762f54c8-e43e-4501-ade6-c4b4825f4abc.docx`
- User's coherence notes and the two attached vortex illustrations.

### What the Q6 paper tries to do

The paper defines

\[
-\Delta\psi=\nabla\cdot(|u|^2u),\qquad
\lambda_H[u]=\alpha\|\nabla\psi\|_2^2,
\]

selects a dominant shell (j^*(t)), and adds a shell-selective feedback term

\[
Q_6=-\gamma\mathbb P[m_{j^*}(D,t)u].
\]

It then claims global regularity for the augmented flow and conditional removal of the augmentation.

### Decisive defects

1. With the manuscript's convention that (\Delta) is negative definite, the term written as
   \[
   \nu\Delta u-\lambda_H[u]\Delta u
   \]
   is anti-diffusive in its second part. A dissipative scalar-viscosity term would have the opposite sign.
2. The asserted Lyapunov functional (E_Q=E+\frac\alpha2\|\nabla\psi\|_2^2) is not derived. The time derivative of the (\psi)-term is omitted, and (\lambda_H) is not shown to be a variational derivative that produces the claimed identity.
3. The coefficient (\lambda_H\ge0) has no proved coercive lower bound in terms of dangerous vortex stretching, high-high transfer, or triad phase alignment. Calling it a coherence viscosity does not supply that theorem.
4. The map (u\mapsto j^*(u)) jumps at shell-tie hypersurfaces. Consequently (Q_6(u)) is not locally Lipschitz there, contrary to the Carathéodory argument in the paper.
5. The cutoff (\varphi(2^{-j^*}\xi)), with support in ((1/2,2)) and plateau on ([3/4,3/2]), is not uniformly coercive on all three shells (j^*-1,j^*,j^*+1). The lower neighboring shell is partly outside the support and the upper shell approaches the zero edge.
6. On (\mathbb R^3), the estimate (E\le T/(2\sigma)) ignores the (L^2) component of the (H^1) energy; there is no torus-style Poincaré rescue.
7. The Case-II inequality (E'\le CE^3) is local only. No estimate proves that Case II must terminate or that the damped case must re-enter.
8. The ODE comparison has the wrong sign: (y'=Cy^3) gives (y(t)=(y_0^{-2}-2Ct)^{-1/2}), not a decaying denominator with (+2Ct).
9. The higher-order and BKM arguments assume the global bound they are meant to prove. The compact-attractor claim on (\mathbb R^3) also ignores translation noncompactness.
10. The deaugmentation parameters are inconsistent: the PDE uses (\alpha,\gamma), the limiting family is labeled (\varepsilon), and the proof alternately sends (\varepsilon\) and (\gamma\) to zero. The fixed positive (\gamma_0) used for uniform control cannot simultaneously vanish. The stated compactness gives at most strong (L^2_{\rm loc}), not strong (H^1_{\rm loc}).

### What is genuinely useful

The user's phase-coherence description supplies the second variable missing from the earlier effective-triad-count analysis. For signed triad contributions write

\[
\Pi_j=\sum_{\tau}a_\tau e^{i\theta_\tau},\qquad
A_j=\sum_\tau a_\tau,\qquad
p_\tau=\frac{a_\tau}{A_j},\qquad
Z_j=\sum_\tau p_\tau e^{i\theta_\tau}.
\]

Then

\[
|\Pi_j|=A_j|Z_j|,
\qquad
N_{{\rm eff},j}=\frac1{\sum_τ p_\tau^2}.
\]

Thus (N_{\rm eff}) measures amplitude participation, while (|Z_j|) measures phase coherence. The sharp quantitative bridge target is

\[
|Z_j|\le C N_{{\rm eff},j}^{-1/2},
\]

or an integrable-in-time relaxation of it. This turns the qualitative phrase “coherence breaks down” into a signed-flux discrepancy estimate.

For the existing signed shell-tensor runs, the diagnostic

\[
\chi_j:=\sqrt{N_{{\rm eff},j}}\,
\frac{|\sum_τ t_\tau|}{\sum_τ|t_\tau|}
\]

was usually (O(1)), approximately (1.1\)–(1.4) in the full (N=24,32) samples and reaching about (1.8) in the shorter (N=24,T=1) runs. This is encouraging finite-resolution evidence for square-root cancellation, not a uniform theorem.

The attached shock/ramp and necklace-vortex pictures illustrate coherent structures physically, but they do not establish any incompressible 3D spectral estimate.

## Batch 019 — Route N focused audit

### Recovered formulation

The SND tracker describes a normalized operator with coefficients

\[
\widetilde\gamma_j[u]=\sum_{i\ne j}\frac{a_i}{\gcd(i,j)},
\]

and claims

\[
\|\widetilde H_N[u]-\widetilde H_N^\mu\|_{\rm op}
=d_{\gcd}(a,\mu),
\qquad
d_{\gcd}(a,\mu)<\delta_0=0.20.
\]

The proposed chain is

\[
\text{AET/SND}_q\Longrightarrow d_{\gcd}<0.20
\Longrightarrow \lambda_{\min}>-\tfrac12
\Longrightarrow \text{regularity}.
\]

No standalone `NS_BYPASS_LEMMA.tex` or `DYNAMIC_COEFFICIENT_STABILITY_LEMMA.tex` was recovered. The tracker itself identifies uniform-in-time AET as open.

### What survives numerically

The available normalized Möbius/GCD shell-matrix test gives a substantial finite-(N) static margin. For (N=16,32,64,100,200,400), the worst single-shell eigenvalues were approximately

\[
-0.250,-0.259,-0.267,-0.253,-0.258,-0.262,
\]

leaving a margin of roughly (0.23\)–(0.25) above (-1/2). This is useful static numerical evidence.

However, that script builds a degree-normalized Möbius/GCD matrix, whereas the tracker states the coefficient formula above. Their exact identity has not been proved. Route N still fails the “one fixed operator throughout” gate.

### Direct obstruction to the fixed-uniform reference

Let (\mu=(1/N,\ldots,1/N)) and take a perfectly smooth divergence-free datum whose energy lies in one dyadic shell, so (a=e_k). Direct evaluation of the tracker's own (d_{\gcd}) gives, over all (k),

| (N) | minimum (d_{\gcd}(e_k,\mu)) | maximum |
|---:|---:|---:|
| 16 | 0.526 | 0.938 |
| 32 | 0.539 | 0.969 |
| 64 | 0.533 | 0.984 |
| 100 | 0.533 | 0.990 |
| 200 | 0.535 | 0.995 |
| 400 | 0.534 | 0.998 |

No single-shell datum satisfies (d_{\gcd}<0.20). Likewise, the claimed empirical uniform-simplex estimate (\|a(t)-\mu\|_1\le0.039) is impossible at (t=0), where the distance is (2(1-1/N)). Therefore the fixed-uniform version of Route N cannot be an unconditional theorem for all smooth (H^1) data.

### Dynamic margin experiment

On the (N=24,T=1) signed-transfer data, testing a bare pointwise margin (δ=0.20) gave:

- minimum tail-coherence gap: (-0.8403);
- positive-gap fraction: (0.139);
- maximum transfer/dissipation ratio: (1.8403).

Thus pure viscous absorption with a universal (0.20) margin fails in these coarse adversarial runs. A drift-corrected form remains plausible:

\[
\mathcal N_+(t)\le(1-δ)\nu D(t)+K(t)X(t),
\qquad K\in L^1_t.
\]

In these runs the inferred (K) had finite numerical time integral, but this is evidence only.

### Viable Route N replacement

The fixed uniform simplex point must be replaced by one of:

1. a data-dependent, restarted viscous/heat reference (\mu(t;t_0));
2. an entry-time theorem that proves approach to the good set before the local strong solution can fail;
3. a direct signed-flux theorem using the pair ((N_{\rm eff},Z_j)), avoiding fixed simplex distance;
4. a drift-corrected no-crossing inequality with a rigorously integrable (K(t)).

The strongest current direction is (3) combined with (4). It matches the actual Navier--Stokes transfer term and is not refuted by single-shell initial data.

## Batch 020 — Canonical Route J package, repaired Paper 2, and shell stress test

### Sources

- `CANONICAL_NS_ROUTE_J_BRIDGE_MANIFEST_AUG1_2026.md`
- `TRACK_NS_FLUID_Q_SUMMARY.md`
- `Paper2_NS_Regularity_SND_FIXED(1).pdf`
- `Paper2_NS_Regularity_SND 2.pdf`
- `Simons_NS_Shell_Stress_Test(1).xlsx`
- Route N screenshots and `RH_FULL_ASSAULT_BRIEF_JUNE7.md` used only for provenance.

### Controlling status recovered

The manifest correctly distinguishes Route J--NS from Route J--RH. Route J--NS is a frozen/static spectral-gap claim. The classical dynamic bridge remains open. The repaired Paper 2 correctly relabels Lemma 6.1, T1, and T2 as open and removes the earlier internally contradictory claim that T2 had been closed.

What is genuinely proved inside Paper 2 is the finite-dimensional perturbation implication

$$
\|H_N[a(t)]-H_N[\mu]\|_{\mathrm{op}}<\delta_0
\quad\Longrightarrow\quad
\lambda_{\min}(H_N[a(t)])>-\tfrac12,
$$

provided the frozen reference gap is supplied independently. This is a direct application of Weyl's inequality.

The earlier PDF's Section 7 is invalid: its flux estimate is asserted without proof, its positive damping rate is not derived uniformly, its numerical ratio is substituted for an analytic bound, and the local-existence transient argument cannot turn an initial distance as large as 2 into 0.039. The corrected PDF properly converts this section into a proposed program.

### Additional operator-definition mismatch

Paper 2 uses $N$ simultaneously as the arithmetic matrix dimension, the number of shell weights, and the upper shell index. Yet indices $1,\ldots,N$ occupy only

$$
L=\lfloor\log_2N\rfloor+1
$$

dyadic shells. With the literal definitions

$$
H_N[a]=\sum_{j=1}^N a_jB_j,
\qquad
(B_j)_{ik}=\widehat H_N(i,k)\mathbf1_{\{\lfloor\log_2\max(i,k)\rfloor=j\}},
\qquad \mu_j=1/N,
$$

most $B_j$ are zero and $H_N[\mu]$ is essentially the degree-normalized matrix divided by $N$. Direct reconstruction gives:

| $N$ | active dyadic shells | $\lambda_{\min}(\widehat H_N)$ | literal $\lambda_{\min}(H_N[\mu])$ |
|---:|---:|---:|---:|
| 16 | 5 | -0.0749 | -0.00790 |
| 32 | 6 | -0.0907 | -0.00329 |
| 64 | 7 | -0.1014 | -0.00162 |
| 100 | 7 | -0.1026 | -0.00103 |
| 200 | 8 | -0.1108 | -0.000555 |
| 400 | 9 | -0.1171 | -0.000293 |

Thus the displayed equations do not reproduce the claimed frozen limit near $-0.297$. The companion frozen operator may be a different object, but its identity with Paper 2's $H_N[\mu]$ is not established.

There is also no theorem in either Paper 2 PDF proving

$$
\lambda_{\min}(H_N[a(t)])>-\tfrac12
\quad\Longrightarrow\quad
\text{BKM, Serrin, Constantin--Fefferman, or an }H^1\text{ bound}.
$$

Consequently the package proves a conditional matrix-gap statement, not yet a conditional Navier--Stokes regularity theorem.

### Workbook audit

The workbook is a well-formed, internally validated $24^3$ pseudospectral stress test with 24 runs, 624 sampled states, $\nu=0.035$, $dt=0.0025$, horizon $T=0.25$, conservative CFL, strict dealiasing, and a kinetic-energy transfer residual near machine precision.

It contains four-band normalized **enstrophy** shares, signed band transfers, and band dissipation. Paper 2 instead defines $a_j$ using shell **kinetic energy**. Therefore this workbook does not directly compute Paper 2's Route N variable, $d_{\gcd}$, $H_N(t)$, or its eigenvalues.

Its substantive result is nevertheless important:

- the single-middle-shell cases stay highly concentrated but are strongly damped;
- the high-frequency-weighted cases are also strongly damped;
- the low-frequency-weighted high-amplitude cases are the only ones with $C_+>1$ and $C_{\rm net}>1$;
- donor/receiver ordering and signed transfer matter more than dominant-shell fraction alone.

Using the tracker's four-band fixed-uniform $d_{\gcd}$ formula as a diagnostic gives, over all 624 states:

| diagnostic | minimum | maximum | mean | fraction below 0.20 | fraction at/below 0.039 |
|---|---:|---:|---:|---:|---:|
| $\|p-\mu\|_1$ | 0 | 1.50 | 0.717 | 7.2% | 1.3% |
| $d_{\gcd}(p,\mu)$ | 0 | 0.75 | 0.324 | 32.9% | 4.5% |

All pure single-band starts have $d_{\gcd}=0.75$. Hence the reported Monte Carlo maximum 0.145 necessarily sampled a restricted interior distribution, used another metric, or omitted simplex corners. It cannot support a universal all-data statement.

### Exact smooth-flow obstruction to a fixed uniform reference

The fixed-uniform Route N condition is contradicted by exact smooth Navier--Stokes shear solutions. For example,

$$
u(x,t)=\sum_m A_m e^{-\nu |k_m|^2t}\sin(k_mx_1)e_2
$$

has $(u\cdot\nabla)u=0$ and evolves purely by heat flow. If more than one shell is initially occupied, its normalized shell weights move toward the lowest occupied shell as $t\to\infty$, not toward the uniform vector. Thus $d_{\gcd}(a(t),\mu)$ eventually approaches a single-shell value above 0.20 while the solution remains globally smooth.

This proves that fixed-uniform simplex proximity is neither dynamically universal nor necessary for regularity. Normalization removes amplitude and the old $C_N$ factor only algebraically; it does not remove this geometric obstruction.

### Route N/J verdict

- Frozen finite-dimensional continuity plus Weyl: valid.
- Repaired Paper 2 status correction: valid and useful.
- Fixed-uniform $d_{\gcd}<0.20$ for all smooth $H^1$ data: false.
- Monte Carlo/AET evidence: restricted numerical evidence, not an analytic bridge.
- Matrix gap to recognized NS regularity criterion: absent.
- Best replacement: a restarted heat/viscous reference together with the signed-flux variables $(N_{\rm eff},Z_j)$ and an integrable drift defect $K(t)$.

The Route N screenshots identify the still-missing source files `NS_BYPASS_LEMMA.tex`, `SND_FORMAL_PROOFS.tex`, and `Simons_NS_CLAY_SUBMIT.tex`. Their claims cannot override the explicit counterexamples above; at most they may contain a different, data-dependent definition worth recovering.

## Batch 021 — Route J / Route N / Bypass comprehensive dossier

### Source

- `Pasted markdown.md` — “Route J / Route N / Bypass Lemma / Bridge Lemma — Comprehensive research dossier,” dated August 22, 2026.

### What the dossier confirms

This document is an internal referee-style audit, not a new proof. Its controlling classifications agree with the present ledger:

- Route J's RH arithmetic input is numerical and analytically incomplete.
- The all-$N$ mixed-block estimate remains open.
- The normalized Route N construction preserves a useful one-sided perturbation estimate.
- The claimed two-sided norm equivalence is not proved.
- The Bypass and Bridge chains remain conditional because dynamic SND, same-operator frozen coercivity, and the passage from a matrix gap to a recognized Navier--Stokes regularity criterion are not established.
- Classical unaugmented three-dimensional Navier--Stokes regularity is not proved.

For normalized weights $a_i\ge0$, $\sum_i a_i=1$, and

$$
g_j(a)=\sum_{i\ne j}\frac{a_i}{\gcd(i,j)},
\qquad
\widetilde H_N[a]=\sum_j g_j(a)\Pi_j,
$$

the coefficient estimate

$$
|g_j(a)-g_j(b)|
\le \sum_{i\ne j}|a_i-b_i|
\le \|a-b\|_1
$$

is valid. If the $\Pi_j$ are mutually orthogonal block projections, it yields

$$
\|\widetilde H_N[a]-\widetilde H_N[b]\|_{\mathrm{op}}
\le \max_j|g_j(a)-g_j(b)|
\le \|a-b\|_1.
$$

This is the durable mathematical content of Route N. It removes an amplitude-dependent constant from this particular upper bound, but it does not establish the reverse inequality or dynamic proximity to a fixed reference.

### The advertised “equivalence” is one-sided

The dossier explicitly records that the displayed Route N argument proves only

$$
\|a-\mu\|_1<0.20
\quad\Longrightarrow\quad
\|\widetilde H_N[a]-\widetilde H_N[\mu]\|_{\mathrm{op}}<0.20,
$$

subject to the projection structure above. It does not prove the converse. Any reverse estimate would require a quantitative injectivity/coercivity theorem for the map $a\mapsto(g_j(a))_j$, and may incur dimension dependence or fail on its kernel. Therefore the manuscript's “if and only if” statement must be removed unless such a theorem is supplied.

### The dossier's own numerical evidence rejects the universal $0.20$ premise

The document reports that a simplified AET model with $\lambda_j=j^2$ reached

$$
\max_t\|a(t)-\mu\|_1\approx1.88,
$$

far above $0.20$. This is consistent with the workbook audit and the exact smooth shear-flow counterexample in Batch 020. Accordingly, the earlier claims “AET always $0.039$” and “500 Monte Carlo trials have maximum $0.145$” cannot be universal statements over admissible shell distributions or all $H^1$ data.

### Five missing links remain explicit

The dossier correctly states that a complete Bypass proof would need all of the following on one fixed set of definitions:

1. the exact normalized operator and projection structure;
2. the valid operator-distance inequality;
3. a frozen gap theorem for that same operator;
4. an all-time dynamical SND theorem for every admissible datum;
5. a theorem converting the resulting matrix gap into BKM, Serrin, Constantin--Fefferman, or another accepted regularity criterion.

Only item 2 is presently isolated in a defensible form, and even it depends on the stated projection structure. The dossier therefore strengthens, rather than overturns, the Batch 020 verdict.

### Source inventory recovered

The dossier names the actual historical source files that would be worth recovering for provenance and definition checking:

- `NS_BYPASS_LEMMA.tex`
- `SND_CLOSURE_STATUS_JUNE4.md`
- `SND_PRESERVATION_CLOSURE.tex`
- `PROOF_TOOLKIT_MASTER.tex`
- `HONEST_GAP_ANALYSIS.md`
- `DYNAMIC_GAP_THEOREM.tex`
- `NS_PROOF_AUDIT_JUNE9.md`
- `ALBRITTON_SFD_EMAIL.md`

The attached dossier does not include their full contents. Recovering them can clarify which operator and metric were intended, but cannot rescue a fixed-uniform all-time condition already refuted by an exact smooth Navier--Stokes solution. A genuinely different, restarted or data-dependent reference remains the viable path.

### Batch verdict

- Useful new extraction: the normalized coefficient map is $1$-Lipschitz from $\ell^1$ into $\ell^\infty$, and hence into operator norm when the block-projection hypothesis is verified.
- Rejected: two-sided norm equivalence without coercivity.
- Rejected: universal fixed-uniform threshold $d_{\gcd}<0.20$.
- Still open: all-time SND, same-operator frozen gap, and the matrix-gap-to-PDE bridge.
- Next mathematical target: replace the fixed reference by restarted heat weights and estimate the signed nonlinear defect with an integrable drift coefficient.

## Batch 022 — `SND_PRESERVATION_CLOSURE.tex`

### Source and claimed result

- Public source recovered from Base44: `SND_PRESERVATION_CLOSURE.tex`, dated May 31 / June 7, 2026.
- The manuscript claims that initial $(\mathrm{SND}_q)$ implies all-time $(\mathrm{SND}_q)$, a uniform AET bound $\|a(t)-\mu\|_1\le0.039$, a normalized spectral floor above $-1/2$, and global smoothness for the classical unaugmented Navier--Stokes equations.

### Decisive counterexample to Lemma 2

The load-bearing statement at lines 61--94 asserts that an **inter-shell** condition,

$$
d_{\gcd}(a,\mu)<0.20,
$$

forces **intra-shell** participation

$$
P_j=\frac{(\sum_{k\in\Lambda_j}|\widehat u(k)|^2)^2}
{\sum_{k\in\Lambda_j}|\widehat u(k)|^4}
\ge c|\Lambda_j|.
$$

These variables are independent at a fixed time. Let $k_j=(2^j,0,0)$ and choose

$$
u_0(x)=\sum_{j=1}^M A_j\sin(2^jx_1)e_2,
$$

with amplitudes chosen so the occupied shells have equal kinetic energy. This is a smooth, real, mean-zero, divergence-free field. Its normalized shell vector is exactly uniform, $a(0)=\mu$, so every metric satisfying $d_{\gcd}(\mu,\mu)=0$ obeys $(\mathrm{SND}_q)$ with maximum margin.

Within each shell, however, only the real Fourier pair $\pm k_j$ is occupied. Therefore

$$
P_j
=\frac{(2|A_j/2|^2)^2}{2|A_j/2|^4}
=2,
$$

whereas $|\Lambda_j|\asymp2^{3j}$. No solution-independent $c>0$ can make $P_j\ge c|\Lambda_j|$ as $j$ and the cutoff grow. More generally, fixing the shell energies fixes $a$ but leaves their distribution among modes within each shell free. Thus no quantitative intra-shell participation bound can follow from an inter-shell distance alone.

If $c$ is allowed to depend arbitrarily on the field and cutoff, the lemma becomes vacuous and cannot yield the subsequent universal $0.039$ estimate.

The same example is an exact Navier--Stokes shear solution:

$$
u(x,t)=\sum_{j=1}^M A_j e^{-\nu2^{2j}t}\sin(2^jx_1)e_2,
\qquad (u\cdot\nabla)u=0.
$$

It is globally smooth, but differential heat decay drives its normalized shell vector away from a fixed uniform reference. This also refutes the claimed universal fixed-reference preservation mechanism.

### Circular preservation argument

The proof first derives participation from $(\mathrm{SND}_q)$ only at $t=0$. It then states that $(\mathrm{SND}_q)$ is “self-consistent” and cannot be violated because a coupling coefficient switches off near concentration. No evolution equation for $d_{\gcd}(a(t),\mu)$, first-contact inequality, invariant-region argument, or sign estimate is supplied.

This is the loop

$$
(\mathrm{SND}_q)\Longrightarrow P_j\text{ large}
\Longrightarrow\text{AET}
\Longrightarrow(\mathrm{SND}_q),
$$

not a forward propagation theorem. A coefficient tending to zero does not by itself reverse concentration; it may simply freeze it, while unequal viscous decay can increase fixed-reference distance.

### The $0.039$ step is not analytic

Even granting the separate participation-to-triad lemma, the displayed estimates contain unspecified constants $C_{\mathrm{AET}}$ and $c'$. The value

$$
1/\sqrt{654}\approx0.039
$$

is imported from one $N=32$ Archon measurement and silently sets the constants to one. It supplies neither an all-resolution nor an all-time theorem, and it does not cover low-cardinality shells.

There is also an immediate endpoint contradiction: the theorem assumes only $d_{\gcd}(a(0),\mu)<0.20$ but concludes $\|a(0)-\mu\|_1\le0.039$. Initial data can be chosen with distance strictly between these values. Navier--Stokes evolution cannot retroactively strengthen the hypothesis at $t=0$.

### Hidden hypotheses and definition changes

The participation-to-AET lemma assumes bounded helical geometry `(BG)` and non-degenerate triad sampling `(ND)`. The final theorem says its only hypothesis is initial $(\mathrm{SND}_q)$ and does not prove that BG and ND hold quantitatively for every Leray--Hopf solution.

The manuscript also changes metrics mid-proof:

- Lemma 2 defines $(\mathrm{SND}_q)$ using $d_{\gcd}(a,\mu)<0.20$.
- Step 1 replaces H3 by $\|a-\mu\|_1<0.20$.

No implication from the displayed $d_{\gcd}$ condition to the required $\ell^1$ condition is proved. This is the same missing reverse/coercive estimate isolated in Batch 021.

### Later spectral and PDE steps remain unsupported

The finite-dimensional Weyl inequality in Step 5 is valid only if:

1. the frozen gap $\lambda_{\min}(\widetilde H_N^\mu)>-0.30$ is proved for the same operator and uniformly in the cutoff;
2. the dynamic operator-distance bound is valid;
3. the cutoff can be connected uniformly to the infinite-shell PDE.

The controlling Route J audit does not supply item 1. Step 6 then simply asserts that the matrix floor implies no finite-time blowup. It proves no bridge to BKM, Serrin, Constantin--Fefferman, an $H^1$ estimate, or another recognized regularity criterion.

### Batch verdict

- Lemma “SND $\Rightarrow$ shell participation with $\delta=1$”: **false as stated**, with an explicit smooth Fourier counterexample.
- All-time preservation: **not proved**; the argument is circular and has no first-contact differential estimate.
- Universal AET constant $0.039$: **numerical**, not derived analytically.
- Route N metric passage: **definition mismatch / missing coercivity**.
- Weyl step: **conditionally valid** after unavailable same-operator inputs.
- Matrix gap $\Rightarrow$ NS regularity: **absent**.
- Claimed “unconditional closure”: **rejected**.

The next referenced source worth inspecting is `LERAY_NONCONC_BRIDGE.md`, because it contains the claimed participation-to-triad estimate. That source cannot repair the false inter-shell-to-intra-shell implication, but it may contain a separately publishable conditional counting lemma.

### Route J numerical provenance note

The current archive summaries disagree on the recorded $N=500$ mixed-block row maximum: one gives $0.596$ and another $0.604$. Both exceed the later proposed $0.55$ threshold, so the logical verdict is unchanged. Neither decimal should be treated as canonical until the underlying numerical table and its precise norm are recovered.

## Batch 023 — `LERAY_NONCONC_BRIDGE.md`

### Claimed conditional lemma

The manuscript claims that shell participation

$$
P_j=\frac{(\sum_{k\in\Lambda_j}A_k^2)^2}{\sum_{k\in\Lambda_j}A_k^4}
\ge c|\Lambda_j|^\delta,
\qquad\delta>\frac23,
$$

together with bounded helical geometry `(BG)` and an unweighted degree condition `(ND)`, implies a lower bound on effective triad count

$$
N_{\mathrm{eff},j}
=\frac{(\sum_{\tau\in\mathcal T_j}|a_\tau|)^2}
{\sum_{\tau\in\mathcal T_j}|a_\tau|^2}
\ge c'|\mathcal T_j|^{(3\delta-2)/2}.
$$

The norm interpolation in Step 4 is valid, and the unconstrained-product upper bound in Step 3 is valid. The proof nevertheless fails at both lower-bound inputs.

### Failure 1 — helical amplitudes are not uniformly bounded below by total modal amplitudes

The proof fixes one helicity sector but defines $A_k=|\widehat u(k)|$ using the total Fourier-vector magnitude. A field can have $A_k>0$ while the selected helical coefficient $u^{s_k}(k)$ is zero. Hence there is no lower bound

$$
|a_{kpq}|\ge c,2^jA_kA_pA_q
$$

for a fixed sector in terms of the total amplitudes.

Even within a populated sector, the Waleffe factor

$$
|s_p|p|-s_q|q||
$$

has no uniform lower bound comparable to $2^j$. It vanishes when the signed radii match and can be arbitrarily small for near-matching radii. Excluding those sectors or triads is not harmless: the solution's energy may be supported precisely there.

Likewise, a scale-independent lower bound on the helical Gram coefficient is not automatic for all lattice triads; nearly degenerate geometries can approach zero. `(BG)` may be imposed as an extra restricted-class hypothesis, but it is not established for arbitrary Navier--Stokes shell data by merely citing the Ring Lemma.

### Failure 2 — unweighted degree does not imply weighted triadic mixing

The crucial Step 2 claims

$$
\sum_{k=p+q}A_kA_pA_q
\ge \eta|\Lambda_j|^{-1}\Big(\sum_kA_k\Big)^3
$$

from the fact that each vertex of the full triad hypergraph belongs to many triads. This implication is false. A lower degree bound counts available edges; it says nothing about whether the vertices carrying the amplitudes form edges with one another.

The proof replaces an average over a neighbor subset by the global mean and labels this as AM. A subset average may be smaller than the global average, including zero. This is not a valid application of AM--GM, Cauchy--Schwarz, or lattice counting.

Concretely, amplitudes can be supported on a large additive/sum-free portion of a dyadic shell. For example, take a narrow outer radial band inside two opposite small angular caps. Sums of two modes in the same cap lie above the shell, while sums from opposite caps lie below it. Such a set can contain a positive proportion of the shell modes, so

$$
P_j\asymp|\Lambda_j|,
$$

yet it contains no comparable-scale internal triads. The full shell may satisfy the manuscript's degree condition, but the amplitude support does not. Thus high modal participation does not force high triadic participation.

### Counting inconsistency

The ND discussion states that the number of decompositions is $O(2^{2j})$ and then treats this as proportional to $|\Lambda_j|$. For a three-dimensional dyadic annulus of thickness comparable to its radius, $|\Lambda_j|\asymp2^{3j}$, so $2^{2j}=|\Lambda_j|^{2/3}$, not a constant multiple of $|\Lambda_j|$. The manuscript later uses $|\mathcal T_j|\asymp|\Lambda_j|^2$. These assertions require one consistent shell thickness and an actual lattice-counting lemma.

### What survives

The interpolation inequality

$$
\sum_kA_k
\ge\frac{(\sum_kA_k^2)^{3/2}}{(\sum_kA_k^4)^{1/2}}
$$

is correct. So is

$$
\sum_{k=p+q}A_k^2A_p^2A_q^2
\le\Big(\sum_kA_k^2\Big)^3.
$$

If one separately assumed the **weighted hypergraph expansion inequality**

$$
\sum_{k=p+q}A_kA_pA_q
\ge \eta|\Lambda_j|^{-1}\Big(\sum_kA_k\Big)^3
$$

and a valid sectorwise lower bound for the helical factors, then the algebra in Steps 5--7 would yield

$$
N_{\mathrm{eff},j}\gtrsim|\Lambda_j|^{-2}P_j^3.
$$

But that weighted expansion is much stronger than ND and is false for arbitrary nonnegative shell amplitudes because of sum-free/concentrated supports. Imposing it would amount to a new phase/additive-uniformity hypothesis, not a consequence of ordinary participation.

### Batch verdict

- Step 3 upper bound: **valid**.
- Step 4 interpolation: **valid**.
- Uniform sectorwise factorization lower bound: **false/unproved**.
- ND $\Rightarrow$ weighted convolution lower bound: **false**.
- Participation $P_j\Rightarrow$ triadic non-concentration: **not proved and false under the stated assumptions**.
- Claimed sharp exponent and “tightness”: **not established**.
- Possible salvage: publish the interpolation calculation as a conditional proposition under an explicitly stated weighted triadic-expansion hypothesis, while recognizing that the new hypothesis is the true missing mechanism.

This source therefore does not supply Lemma 1 of `SND_PRESERVATION_CLOSURE.tex`; it introduces a second independent gap after the already-false inter-shell-to-intra-shell implication.
