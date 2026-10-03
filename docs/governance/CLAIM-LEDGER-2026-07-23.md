# CLAIM LEDGER

**Prime Field Technologies LLC — Jonathan R. Simons**  
**July 23, 2026 — Governing Document**

> **Filing note (repo packaging, 2026-10-02; corrected 2026-10-03).**  
> This is the **July 23, 2026** governing claim ledger (live face).  
> **July wording pin (verbatim, do not rewrite):** [`archive/CLAIM-LEDGER-2026-07-23.verbatim.md`](./archive/CLAIM-LEDGER-2026-07-23.verbatim.md) at git SHA `9242eee0e139b93f20fef7964e585770218d8299`.  
> **Oct 2026 audited corrections card:** [`CLAIM-LEDGER-CORRECTIONS-2026-10.md`](./CLAIM-LEDGER-CORRECTIONS-2026-10.md) (from PR #155). When an audited correction conflicts on a specific bridge, **that correction wins for that bridge**.  
> Later program notes (e.g. Ring **REPAIR**, Theorem H withdrawn / SND propagation **OPEN**, transfer lemma **OPEN**, \(N_{\mathrm{eff},j}\) is diagnostic not a Clay close, centered ledger **EXACT / OPEN / KILLED**, PRODUCT-BLOCK / \(T_{j\leftarrow j}\) / \(\alpha_+\)) may refine further bridges the same way.  
> **Current working focus:** unaugmented NS pathway / diagnostics — **RH program not active yet** (Jonathan: *“we arent on RH yet.”*).  
> **Do not claim** Clay / NS-11 / RH-11 solved.  
> **Q6 IDs:** `Q6-1`…`Q6-9` below are locked; do not renumber or reuse for different claims.

Every claim is categorized as: **PROVED**, **CONDITIONAL**, **NUMERICAL**, **CONJECTURAL**, **OPEN**, or **WITHDRAWN**.

---

## I. NAVIER–STOKES PROGRAM

Source: `RingLemma_Final.tex`, Zenodo DOI [10.5281/zenodo.20405526](https://doi.org/10.5281/zenodo.20405526)

| # | Theorem/Result | Statement (abbreviated) | Assumptions | Status | Classical Consequence | Dependency |
| --- | --- | --- | --- | --- | --- | --- |
| NS-1 | Q1 Dissipation | \(Q_1^\varepsilon[u]=-\varepsilon\|\nabla u\|^\beta\Delta u\) provides strict dissipation in high-frequency shell regime | Augmented system (Q1 present) | PROVED | None — augmented only | — |
| NS-2 | Phi-Renormalization | \(\Phi=u_\theta/r\) substitution eliminates \(r^{-4}\) axis singularity algebraically | Augmented system | PROVED | None — augmented only | NS-1 |
| NS-3 | Energy Rate | Dissipation rate \(O(\varepsilon^{4/(\beta+2)})\) established | Augmented system | PROVED | None — augmented only | NS-1, NS-2 |
| NS-4 | Augmented ↔ SND Equivalence | Exact equivalence between Q1 dynamics and spectral non-concentration [SND] | Augmented system | **WITHDRAWN** (false glue; SND is hypothesis / conditional texture, not an identity with the augmented PDE) | None — do not cite as proved equivalence | NS-1 |
| NS-5 | Shell Regime Classification | Three shell interaction regimes: spread, borderline, dangerous | Augmented system | PROVED | None — augmented only | NS-1–3 |
| NS-6 | Ring Lemma | Three disjoint spectral shells: \(\sum\|P_{S_i}H_N f\|^2\ge C\cdot\|f\|^2\) | \(Q_N\) operator (static) | **OPEN / REVIEW REQUIRED** (scoped geometry only after claim-by-claim journal audit; not a Clay path) | Static structure only — not classical regularity | None |
| NS-7 | Global Summation Lemma | Total time in dangerous regime is finite under [SND] | [SND] assumed | PROVED (conditional) | Conditional classical regularity | NS-5, NS-6 |
| NS-8 | Conditional \(H^1\) bound | If [SND] holds, global \(H^1\) bounds follow | [SND] assumed | PROVED (conditional) | Conditional classical regularity | NS-6, NS-7 |
| NS-9 | Main Theorem | Global \(C^\infty\) regularity for augmented NS | Augmented system (Q1 present), **fixed \(\varepsilon>0\)** Lions threshold | **PROVED (fixed-\(\varepsilon\) only)**. Classical / \(\varepsilon\to0\) limit and \(\|u^r/r\|_\infty\) barrier **OPEN**. Not Statement B. | None — augmented only; not Clay | NS-1–3, NS-5, NS-7–8 |
| NS-10 | Dynamic [SND] for classical NS | Leray–Hopf solutions of classical NS satisfy [SND] | Classical NS (no Q1) | OPEN | If proved: unconditional classical NS regularity | NS-6, NS-8 |
| NS-11 | Unconditional classical 3D NS regularity | Every Leray–Hopf solution of classical NS is smooth | Classical NS | **NOT CLAIMED** | This is the Millennium Prize problem | NS-10 |

**Summary:** 5 results PROVED (NS-1–3, NS-5; NS-9 at fixed-\(\varepsilon\) scope only). 2 results conditional on [SND] (NS-7, NS-8). 2 OPEN (NS-6 review; NS-10). 1 WITHDRAWN result row (NS-4). The Millennium Prize problem (NS-11) is **not claimed**.

**Previously withdrawn outreach claims (not result-row counts):** “Proved unconditionally” (NS one-pager), “All Steps Closed” (NS one-pager), “An unconditional proof of global regularity” (Letter to Marilyn Simons), “Formally closed” (Letter to Simons Foundation). All withdrawn July 23, 2026.

---

## II. RIEMANN HYPOTHESIS PROGRAM

Source: `RH_CANONICAL_2026.tex`, Zenodo DOI [10.5281/zenodo.19842060](https://doi.org/10.5281/zenodo.19842060)

> **Working note:** RH program is **parked** for current work (“we aren’t on RH yet”).  
> **Oct 2026:** bridges that take the withdrawn spectral-limit candidate \(-1/(2\pi)\) as antecedent are **WITHDRAWN as RH vehicles**. Q6 KEEP is operator work **without RH claim**.

| # | Theorem/Result | Statement (abbreviated) | Assumptions | Status | Classical Consequence | Dependency |
| --- | --- | --- | --- | --- | --- | --- |
| RH-1 | Lemma A: Möbius Decomposition | \(Q_N\) decomposes via Möbius function into squarefree/non-squarefree blocks | \(Q_N\) operator | PROVED | Provides spectral structure | None |
| RH-2 | Lemma B: Determinant Formula | \(\det(Q_N^n)=\prod\varphi(k)/k\) | \(Q_N\) operator | PROVED | Provides spectral structure | RH-1 |
| RH-3 | Proposition C: Rayleigh Identity | Rayleigh quotient of \(Q_N\) relates to Dirichlet series | \(Q_N\) operator | PROVED | Provides variational characterization | RH-1, RH-2 |
| RH-4 | Theorem D: Forward Bridge | If spectral limit \(\to -1/(2\pi)\), then RH holds | \(Q_N\) spectral limit | **WITHDRAWN as RH vehicle** (antecedent uses withdrawn \(-1/(2\pi)\) candidate; see QM-1). July wording pinned in archive. | None — RH **NOT CLAIMED** | RH-1–3 |
| RH-5 | Theorem E: T-Transform | The \(1/2\) emerges algebraically from the T-transform | \(Q_N\) operator | PROVED | Explains why critical line is at \(\mathrm{Re}(s)=1/2\) | RH-1–3 |
| RH-6 | Theorem F: Biconditional | RH \(\Leftrightarrow\) spectral limit \(=-1/(2\pi)\) | RH assumed for reverse direction | **WITHDRAWN as RH vehicle** (same withdrawn constant). July wording pinned in archive. | None — RH **NOT CLAIMED** | RH-4 |
| RH-7 | Step C: Unconditional \(v_N^*\) bound | The minimizing eigenvector \(v_N^*\) of \(Q_N\) is bounded as \(N\to\infty\) without assuming RH | None | OPEN | Does **not** currently yield RH via a live bridge; RH remains **NOT CLAIMED** | RH-1–3, RH-5 |
| RH-8 | Route 1: Dirichlet series | \(1/\zeta(s)\) on critical line controls \(v_N^*\) | Needs rigorous implementation | OPEN (candidate route; parked) | Possible path to RH-7 only if revived | RH-3 |
| RH-9 | Route 2: E8 spectral | E8 root lattice spectral properties bound \(v_N^*\) | Needs proof of E8\(\leftrightarrow Q_N\) connection | OPEN (candidate route; parked) | Possible path to RH-7 only if revived | RH-1–3 |
| RH-10 | Route 3: Möbius equidistribution | Local Möbius equidistribution controls \(v_N^*\) | Needs strengthening to global | OPEN (candidate route; parked) | Possible path to RH-7 only if revived | RH-1–3 |
| RH-11 | Riemann Hypothesis | All non-trivial zeros of \(\zeta(s)\) lie on \(\mathrm{Re}(s)=1/2\) | None | **NOT CLAIMED** | This is the Millennium Prize problem | RH-7 |

**Summary:** 4 results PROVED (Lemmas A–B, Prop C, Theorem E). 2 WITHDRAWN as RH vehicles (RH-4, RH-6 — withdrawn-floor bridges). 1 OPEN step (RH-7) with 3 parked candidate routes. The Millennium Prize problem (RH-11) is **not claimed**.

**Previously withdrawn outreach claims (not result-row counts):** “Essentially proved except one bound” (outreach materials). Withdrawn July 23, 2026. The one bound may contain the full difficulty of RH.

---

## III. GOLDBACH PROGRAM

Source: `GOLDBACH_Q1_DEAUGMENTED.md`

| # | Theorem/Result | Statement (abbreviated) | Assumptions | Status | Classical Consequence | Dependency |
| --- | --- | --- | --- | --- | --- | --- |
| GB-1 | Goldbach coupling weight | \(G(n)=\sum_{p+(n-p)=n,\ \mathrm{both\ prime}}1/(\sqrt{p}\cdot\sqrt{n-p})\) | Definition | PROVED (definition) | Reformulates Goldbach as matrix diagonal positivity | None |
| GB-2 | Equivalence | \(G(n)>0\) for all even \(n>2\) \(\Leftrightarrow\) Goldbach’s conjecture | Definition | PROVED (definitional) | Restates Goldbach in spectral language | GB-1 |
| GB-3 | Computational verification | \(G(n)>0\) for all even \(n\le 200\) | Computation | NUMERICAL | Evidence, not proof | GB-1 |
| GB-4 | Prime submatrix stability | \(\lambda_{\min}\) of prime-pair submatrix \(=-0.235\) (above \(-1/2\)) | Computation | NUMERICAL | Evidence of spectral stability | GB-1 |
| GB-5 | Bertrand lower bound | Bertrand’s postulate gives one prime in \((n/2,n)\) | Proved theorem | PROVED (existing result) | Necessary but not sufficient for \(G(n)>0\) | None |
| GB-6 | Goldbach’s conjecture | \(G(n)>0\) for all even \(n>2\) | None | OPEN (= Goldbach) | This IS Goldbach | GB-1–5 |

**Summary:** 3 PROVED (2 definitional equivalences + 1 existing theorem cited). 2 NUMERICAL verifications. 1 OPEN step (GB-6) which is equivalent to Goldbach itself. No proof of Goldbach is claimed.

**Previously withdrawn outreach claims (not result-row counts):** “We have Goldbach” (conversational). Withdrawn July 23, 2026. The reformulation is language, not a proof.

---

## IV. ORBITAL MECHANICS PROGRAM

Source: `MISSING_PLANETS_PAPER_v2.md`, `PRIME_INDEXING_ORBITAL_PAPER.md`

| # | Theorem/Result | Statement (abbreviated) | Assumptions | Status | Classical Consequence | Dependency |
| --- | --- | --- | --- | --- | --- | --- |
| OM-1 | Coprime stability mechanism | Coprime orbital period labels by themselves produce gravitational perturbation cancellation | Newtonian gravity | CONJECTURAL (reduced integer labels are not by themselves a proved stability mechanism) | Possible heuristic only; requires dynamical derivation | None |
| OM-2 | ExoRatio statistic | Population-percentile method for identifying anomalous orbital gaps | Kepler catalog | OPEN (algorithm reconstruction under audit; written formula does not yet reproduce several tabulated examples) | May rank candidate systems after validation | None |
| OM-3 | HD 110067 resonance evidence | HD 110067 is a resonant chain and independent dynamics favor resonant stability | Independent data and N-body analysis | PROVED as external resonance evidence; NOT a validation of a proprietary GCD mechanism | Supports standard resonant-chain stability only | None |
| OM-4 | 27 candidate systems | Draft table of anomalous-gap systems | Preserved 2025 catalog | NUMERICAL — UNDER AUDIT (global counts reproduce, but several system multiplicities/anomaly values do not yet reproduce from the cited file) | No prediction-credit claim until reconstructed and timestamped | OM-2 |
| OM-5 | Missing body prediction | Bodies may be found in predeclared gap zones of locked candidate systems | Validated OM-4 candidates with prediction timestamps predating any public KOI/TCE/candidate/confirmation | CONJECTURAL (prospectively testable) | Prediction priority only if chronology and interval tests pass | OM-2–4 |

**Summary:** 1 PROVED (external resonant-chain evidence). 1 NUMERICAL (under audit). 2 CONJECTURAL. 1 OPEN (ExoRatio reconstruction). The GCD mechanism remains CONJECTURAL. Missing-body predictions remain prospectively testable only after exact, timestamped intervals are locked.

---

## V. MUSIC/ACOUSTICS

Source: `PRIME_EXPLAINER_ILLUSTRATED.md` (Chapter 5)

| # | Result | Statement | Status |
| --- | --- | --- | --- |
| MU-1 | Pythagorean consonance = coprime ratios | 2:1, 3:2, 4:3 are coprime and consonant | PROVED (2500 years of music theory) |
| MU-2 | Consonance mechanism | Coprime ratios → constructive interference; non-coprime → beat frequencies | PROVED (established acoustics) |
| MU-3 | Kepler planetary harmonics | Orbital speed ratios map to musical intervals | PROVED (Kepler 1619, verified) |
| MU-4 | HD 110067 as music | System’s ratios (3:2, 4:3) are literally musical intervals | PROVED (observation) |

**Summary:** 4 PROVED via existing knowledge. No overclaims.

---

## VI. CONSCIOUSNESS/ANESTHESIA

Source: `ANESTHESIA_COHERENCE_FLOW_PAPER_v2.md`, `CONSCIOUSNESS_THRESHOLD_WHITEPAPER.md`

| # | Result | Statement | Status |
| --- | --- | --- | --- |
| CO-1 | Reflex staircase | Sequential brainstem reflex abolition under anesthesia | PROVED (clinical, established) |
| CO-2 | Neural criticality | Brain operates near phase transition | PROVED (Chialvo, Plenz, Shew) |
| CO-3 | Cortical integration loss | Anesthesia disrupts integrated cortical communication | PROVED (Massimini, TMS-EEG) |
| CO-4 | \(\kappa^*=6/\pi^2=0.6079\) as coherence threshold | Universal threshold of neural phase coherence collapse | CONJECTURAL (theory, falsifiable) |
| CO-5 | Reflex staircase = lattice sub-floor collapse | Sequential reflex abolition maps to spectral sub-floor collapse | CONJECTURAL (theory) |
| CO-6 | Stapedial abolition converges on \(\kappa^*\) | Universal across patients and drug classes | CONJECTURAL (testable, not yet tested) |

**Summary:** 3 PROVED (established neuroscience). 3 CONJECTURAL (our framework, falsifiable). No overclaims.

---

## VII. BLACK HOLES / QUASINORMAL MODES

Source: `PRIME_EXPLAINER_ILLUSTRATED.md` (Chapter 6)

| # | Result | Statement | Status |
| --- | --- | --- | --- |
| BH-1 | Perseus black hole sings B-flat | Chandra X-ray detection 2003 | PROVED (observation) |
| BH-2 | B-flat ratio is coprime (16:15, \(\gcd=1\)) | Arithmetic fact | PROVED (arithmetic) |
| BH-3 | LIGO ringdown QNMs show prime-indexed structure | Overtone spacing analysis | **WITHDRAWN from outreach** (Experiment 01 null / RETAIN-NULL; July wording pinned in archive) |
| BH-4 | Prime-indexed QNMs carry information | Prime modes persist, non-prime modes cancel | **WITHDRAWN from outreach** (same Experiment 01 / DA retirement; July wording pinned in archive) |
| BH-5 | Information paradox resolution | Information survives at prime frequencies | CONJECTURAL (theory; do not ship as completed unification) |

**Summary:** 2 PROVED (observation + arithmetic). 2 WITHDRAWN from outreach (BH-3, BH-4). 1 CONJECTURAL (BH-5). No QNM/HB unification claim.

---

## VIII. QUANTUM / SPECTRAL GAPS

Source: `QUANTUM_MILLENNIUM.tex`, `SPECTRAL_UNIFICATION_PAPER.tex`

| # | Result | Statement | Status |
| --- | --- | --- | --- |
| QM-1 | Earlier \(-1/(2\pi)\) normalized-limit candidate | Finite-size ratios were previously interpreted as approaching \(-1/(2\pi)\) | WITHDRAWN as preferred candidate (prime-local hierarchy and data through \(N=500{,}000\) favor approximately \(-0.1470187754\); exact limit remains OPEN) |
| QM-2 | \(C=\pi/2-\ln 2\approx 0.877\) as a Q6 spectral floor | Earlier identification of this constant as the raw Q6 spectral floor | WITHDRAWN (raw \(\lambda_{\min}\) diverges logarithmically negative; the numerical normalized-limit candidate is different) |
| QM-3 | \(\kappa^*=6/\pi^2\) appears across domains | Coprime density floor in E8, NS, RH, consciousness | CONJECTURAL (observed convergence, not proved as universal) |
| QM-4 | Yang–Mills mass gap connection | Heuristic analogy between \(Q_N\) spectral gap and 4D Yang–Mills mass gap | CONJECTURAL (pure heuristic analogy, no mathematical map, physically inconsistent with 4D continuum physics) |
| QM-5 | Five Millennium problems unified | Speculative framing of five Millennium problems under \(Q_N\) operator | CONJECTURAL (speculative framing only, no proven mathematical bridges); **WITHDRAWN from outreach** as solved/unified Clay pack |

**Summary:** 3 CONJECTURAL result rows (QM-3–5). 2 WITHDRAWN result rows (QM-1, QM-2). The “Quantum Millennium” framing is a research program, not a set of proofs; do not ship as unified Clay solutions.

**Previously withdrawn outreach claims (not result-row counts):** “Quantum Millennium” framing suggesting seven problems essentially solved (`SESSION_REPORT_MAY18_2026`). Withdrawn July 23, 2026.

---

## IX. E8 CONNECTION

Source: `CLAUDE_E8_BRIEF_JUNE25_2026.md`, `e8_data.json`

| # | Result | Statement | Status |
| --- | --- | --- | --- |
| E8-1 | Q6 is discretization of E8 root lattice operator | 100% alignment for first 20 primes | NUMERICAL (computed) |
| E8-2 | \(\kappa^*=6/\pi^2\) in E8 root geometry | Coprime density floor appears in E8 | NUMERICAL (computed) |
| E8-3 | E8 rank 8 = K-level count | Rank matches clinical consciousness levels | CONJECTURAL (numerical coincidence or deep connection) |
| E8-4 | E8 triality ↔ Ring Lemma three shells | Three orthogonal root subsystems ↔ three spectral shells | CONJECTURAL (empirically observed, not formalized) |
| E8-5 | E8 spectral properties bound \(v_N^*\) | Route 2 for RH Step C | OPEN (not proved; RH parked) |

**Summary:** 2 NUMERICAL. 2 CONJECTURAL. 1 OPEN (candidate route for RH; parked). E8 is the geometric context, not a proven bridge.

---

## X. CMB

| # | Result | Statement | Status |
| --- | --- | --- | --- |
| CMB-1 | Odd modes dominant in CMB power spectrum | WMAP/Planck observation | PROVED (observation) |
| CMB-2 | GCD kernel predicts odd/prime mode dominance | Prime-adjacent modes are ground state | CONJECTURAL (our interpretation; standard cosmology has a different explanation) |

**Summary:** 1 PROVED (observation). 1 CONJECTURAL (interpretation). The standard cosmological explanation (baryon acoustic oscillations) may fully account for the observation without the GCD kernel.

---

## XI. Q6 NORMALIZED INVERSE-GCD MATRIX

Source: `Q6_TRACE_FORMULA_AND_SPECTRAL_CHASE.tex`, `q6_trace_chase.py`

**Definition:** \(Q_N(i,j)=1/[\gcd(i,j)\sqrt{ij}]\), \(1\le i,j\le N\).

> **ID lock:** The IDs `Q6-1`…`Q6-9` below are the governing numbered SoT. Oct audit drafts that reuse `Q6-1`… for different claims must choose **different** IDs.

| # | Result | Statement | Status |
| --- | --- | --- | --- |
| Q6-1 | Finite-section trace formula | \(\mathrm{Tr}(Q_N)=H_N^{(2)}=\sum_{n\le N}1/n^2\to\zeta(2)\), with exact divisor-layer identity | PROVED |
| Q6-2 | Corrected divisor factorization | \(Q_N=D^{-1/2}A\,\mathrm{diag}(g(d)/d)\,A^T D^{-1/2}\), \(g(d)=\prod_{p\mid d}(1-p)\) | PROVED |
| Q6-3 | Determinant and exact inertia | \(\det(Q_N)=(1/N!)\prod_{d\le N}g(d)/d\); signs equal parity counts of \(\omega(d)\) | PROVED |
| Q6-4 | Second trace moment | \(\mathrm{Tr}(Q_N^2)\sim[\zeta(4)/\zeta(2)](\log N)^2=(\pi^2/15)(\log N)^2\) | PROVED |
| Q6-5 | Two-sided logarithmic branches | \(\lambda_{\max}\ge[\zeta(3)/\zeta(2)]\log N+O(1)\); \(\lambda_{\min}\le\zeta(3)/\zeta(2)/12\log N+O(1)\) | PROVED |
| Q6-6 | Large-\(N\) normalized minimum | Corrected Lanczos through \(N=500{,}000\) and prime-local computation favor \(c_{\mathrm{PL}}\approx -0.1470187754\); residual is approximately constant near \(-0.07\) | NUMERICAL |
| Q6-7 | Exact normalized-limit theorem | Existence and value of \(\lim\lambda_{\min}(Q_N)/\log N\) | OPEN |
| Q6-8 | Finite-period variational reduction | Every fixed periodic amplitude profile has an exact asymptotic Rayleigh/log coefficient \(R_M(c)\) | PROVED |
| Q6-9 | Prime-local limit identification | \(\lim\lambda_{\min}(Q_N)/\log N=c_{\mathrm{PL}}\), where \(c_{\mathrm{PL}}\) is the prime-local Euler-product candidate | CONJECTURAL |

**Boundary:** The convergent diagonal trace is a finite-section identity, not a trace-class infinite-operator trace. Q6-5 proves the raw finite sections have no fixed lower spectral floor. **No RH, Yang–Mills, Goldbach, or classical Navier–Stokes consequence follows from Q6-1 through Q6-5 alone.** Q6 KEEP **without RH claim**.

---

## MASTER SUMMARY

Counts below are **numbered result rows only**. Outreach narrative withdrawals are listed in section prose and are **not** mixed into these numbers.

| Category | PROVED | CONDITIONAL | NUMERICAL | CONJECTURAL | OPEN | WITHDRAWN |
| --- | --- | --- | --- | --- | --- | --- |
| Navier–Stokes | 5 (NS-1–3, NS-5; NS-9 fixed-\(\varepsilon\)) | 2 (NS-7, NS-8 on [SND]) | 0 | 0 | 2 (NS-6 review; NS-10) | 1 (NS-4) |
| Riemann Hypothesis | 4 (RH-1–3, RH-5) | 0 | 0 | 0 | 1 (RH-7) + 3 parked routes | 2 (RH-4, RH-6 as RH vehicles) |
| Goldbach | 3 (GB-1, GB-2, GB-5) | 0 | 2 | 0 | 1 (= Goldbach) | 0 |
| Orbital mechanics | 1 (OM-3) | 0 | 1 (OM-4) | 2 (OM-1, OM-5) | 1 (OM-2) | 0 |
| Music/acoustics | 4 | 0 | 0 | 0 | 0 | 0 |
| Consciousness | 3 | 0 | 0 | 3 (falsifiable) | 0 | 0 |
| Black holes | 2 | 0 | 0 | 1 (BH-5) | 0 | 2 (BH-3, BH-4 outreach) |
| Quantum/Millennium | 0 | 0 | 0 | 3 (QM-3–5) | 0 | 2 (QM-1, QM-2) |
| E8 | 0 | 0 | 2 | 2 | 1 (E8-5) | 0 |
| CMB | 1 | 0 | 0 | 1 | 0 | 0 |
| Q6 inverse-GCD matrix | 6 | 0 | 1 | 1 | 1 | 0 |

**Totals (result rows):** 29 PROVED · 2 CONDITIONAL · 6 NUMERICAL · 13 CONJECTURAL · 7 OPEN · 7 WITHDRAWN

---

## THE RULES GOING FORWARD

1. No result labeled **PROVED** may be described as solving a classical open problem unless the bridge to the original problem is also **PROVED**.
2. No result labeled **CONDITIONAL** may be described as **PROVED** without qualification.
3. No result labeled **NUMERICAL** may be described as **PROVED**.
4. No result labeled **CONJECTURAL** may be described as anything other than a conjecture.
5. The status labels in this ledger are authoritative for outreach **as amended by later audited bridge corrections** (see filing note and [`CLAIM-LEDGER-CORRECTIONS-2026-10.md`](./CLAIM-LEDGER-CORRECTIONS-2026-10.md)). If a document contradicts the amended ledger, **the amended ledger wins**.
6. Any new claim must be added to this ledger before it appears in any external communication.
7. The ledger is updated by Frankie (the agent) and reviewed by Jonathan before any outreach.
8. Master WITHDRAWN / OPEN / PROVED totals count **numbered result rows only** — not separate outreach narrative withdrawals.
9. July wording for corrected rows is preserved in [`archive/CLAIM-LEDGER-2026-07-23.verbatim.md`](./archive/CLAIM-LEDGER-2026-07-23.verbatim.md).

---

This ledger governs all research communications from **Prime Field Technologies LLC**.  
Jonathan Robert Simons, CRNA, MBS  
July 23, 2026 (live face amended 2026-10-03 per audited corrections).
