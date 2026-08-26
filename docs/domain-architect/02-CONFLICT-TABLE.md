# Conflict table

Incompatible definitions stay incompatible. This table does not pick a winner by preferring the symbols \(P,H,\psi,\lambda,\Phi\).

Columns:

- **Left / Right:** two statements that cannot both be used as the current baseline.
- **Object:** what is in conflict (equation, symbol, claim, or protocol).
- **Resolution in this freeze.**

---

## 1. Identity of the Simons Field Equation

| ID | Left | Right | Object | Resolution |
|---|---|---|---|---|
| C-SFE-1 | FRA-5: SFE is an unresolved realization map \(\Phi=\mathcal F_S(\ldots)\) | SFE-PUB: \(\Phi(x,t)=\sum_p A_p\sin(2\pi f_p t/\varphi(x)+\delta_p)\) is “the” SFE | Which formula is SFE | **Do not merge.** FRA-5 is the current architectural name. SFE-PUB is a retired public formula |
| C-SFE-2 | FRA-5 | SFE-QM: \(\Delta((P\cdot H\cdot\psi)^2\lambda)=\Phi\) | Which formula is SFE | **Do not merge.** SFE-QM is retired. Same letters, different types and claims |
| C-SFE-3 | SFE-PUB is a classical prime oscillator | SFE-HAM is a Fock Hamiltonian on occupation numbers | Type of SFE | **Do not merge.** Neither is a justified canonical SFE |
| C-SFE-4 | SFE-QM is called a Lagrangian | SFE-QM is also called an equation of motion | What the displayed string *is* | A Lagrangian density and an Euler–Lagrange equation are different objects. **RETIRE** until one is defined |
| C-SFE-5 | Prior NS agent: “this is what SFE actually is” (SFE-PUB) | Audited handoff: canonical SFE remains unresolved | Whether a canonical formula exists | The handoff wins. Naming SFE-PUB as canonical was a drift |
| C-SFE-6 | Early guess: SFE = Shell Flux Estimate | Later correction: SFE ≠ NS flux | Acronym | **RETIRE** the guess. Flux bounds stay in the fluids book |

---

## 2. Role meanings for the same letters

| ID | Left | Right | Object | Resolution |
|---|---|---|---|---|
| C-P-1 | Audited \(P\): permission projector / selector | SFE-HAM: “prime pressure,” identified with the \(Q_N\) interaction | \(P\) | Audited \(P\) is the baseline. Prize-paper \(P\) is retired |
| C-P-2 | Audited \(P\) | Track A \(\mathbb P\): Leray / Helmholtz projector | \(P\) / \(\mathbb P\) | Different books. Write the fluids projector as \(\mathbb P_{\mathrm{Leray}}\) |
| C-P-3 | Audited \(P\) | NS packet mass \(P_{j_*}=X_{j_*-1}+X_{j_*}+X_{j_*+1}\) | \(P\) | Different books. Never reuse \(P_{j_*}\) in a FRA gravity note |
| C-P-4 | Audited \(P\) | Arithmetic restriction \(\widetilde Q\rvert_P\) to the prime set | \(P\) as a set | Use \(\mathbb P\) for the prime set |
| C-Φ-1 | Audited \(\Phi\): realized output | SFE-PUB \(\Phi(x,t)\): oscillatory field | \(\Phi\) | Same letter, acceptable only inside a declared SFE-PUB archive note |
| C-Φ-2 | Audited \(\Phi\) | Swirl \(\Phi=u_\theta/r\) | \(\Phi\) | **Hard collision.** Fluids notes must use \(\Phi_{\theta}\) or keep \(\Gamma\) |
| C-Φ-3 | Audited \(\Phi\) | Golden ratio \(\varphi=(1+\sqrt5)/2\) | \(\Phi\) vs \(\varphi\) | Already corrected in the handoff. Enforce in software |
| C-Φ-4 | SFE-PUB \(\varphi(x)\) as a spatial phase / divisor of frequency | Golden ratio \(\varphi\) | \(\varphi\) | Third collision. If SFE-PUB is archived, write \(\varphi_{\mathrm{pub}}(x)\) |
| C-H-1 | Audited \(H\): coupling / interaction | Arithmetic \(H_N=D^{-1/2}\widetilde Q_N D^{-1/2}\) | \(H\) | Different books. Never call \(H_N\) a FRA coupling |
| C-λ-1 | Audited \(\lambda\): scale response (wavelength **or** eigenvalue **or** inverse operator **or** propagator) | Gravity uses \(\lambda_n=1/k_n\) specifically | Type of \(\lambda\) | **REVISE** the role: \(\lambda\) is a role name, not a single mathematical type. Each instance must declare its type |
| C-S-1 | GRV-4: \(S_n=\rho_n\) | GRV-5: \(\rho_n=S_n\psi_n\) | What \(S\) is | Internal conflict in the audited gravity map. Do not use both in one laboratory without an explicit independence argument |

---

## 3. Claims versus evidence

| ID | Left | Right | Object | Resolution |
|---|---|---|---|---|
| C-CLM-1 | Public site / 2025 LinkedIn: SFE unifies GR and QM; gravity is an emergent harmonic curvature | Audited baseline: architectural mapping is not a derivation; GR is the accepted relativistic theory | Gravity claim | Public unification language is **retired**. GRV-* are benchmarks, not a new theory |
| C-CLM-2 | 2025 LinkedIn: six Millennium solutions “derived from the SFE” | Audited baseline; August errata; KEEP-CUT inventory | Prize claim | **RETIRED.** Do not revive |
| C-CLM-3 | “Primes are arithmetically fundamental, therefore physically privileged” | Audited §8: (1) and (2) do not imply (3) | Prime hypothesis | Keep the three-step separation. Experiment 01 is a null under its protocol |
| C-CLM-4 | Exoplanet “prime height” / Prime Resonance Law | Experiment 01 avoided exoplanet data; later audits cut ExoRatio as evidence | Empirical claim | Not usable as HB support in this freeze |
| C-CLM-5 | Domain Architect sketch audit: Domain Architect is branding / a router | Audited handoff: Domain Architect **is** the product and Functional Role Analysis **is** the method | What Domain Architect is | Both can be true at once if scoped: the **product** classifies roles; it is **not** a proof engine and not an input to \(\Pi_j\) |
| C-CLM-6 | January 2026 LinkedIn: HB “does not replace equations; it tells you how to assign, tune, and test variables” | 2025 site: SFE is the unifying theory | What HB is | The 2026 methods posture matches the audit. The 2025 unifying-theory posture does not |

---

## 4. Prime experiments are not one experiment

| ID | Left | Right | Object | Resolution |
|---|---|---|---|---|
| C-PRIME-1 | GRV-7: \(P_n=\mathbf 1_{\mathbb P}(n)\) on Laplacian mode index \(n\) | EXP01: proximity of frequency *ratios* to a frozen `prime_neighbor_ratios` list | Operational prime hypothesis | **Different tests.** A gravity-harness result cannot confirm or deny Experiment 01, and conversely |
| C-PRIME-2 | Audited protocol: equal mode budgets vs low / odd / composite / random / optimized selectors | Experiment 01 node counts: golden 9, integer 13, Fibonacci 16, prime 24, random 24 | Fairness | Experiment 01 remains a valid closed test **under its own freeze**. It does **not** satisfy the later equal-budget rule. Do not reopen EXP01 to “fix” budgets after TEST |
| C-PRIME-3 | Audited requirement: canonical dimensionless integer label, frozen degeneracies, representation invariance | Laplacian index \(n\) on a 1-D periodic interval is close to canonical; 3-D QNM labels \((\ell,m,n)\) are not a single prime-or-not integer | Index | Gravity 1-D harness can freeze \(n\in\mathbb Z_{>0}\). Ringdown cannot treat “mode 220” as a prime without a declared encoding |
| C-PRIME-4 | “5 Hz is prime” | Frequency is unit-dependent | Dimensional prime claims | **RETIRE** all dimensional prime labels |

---

## 5. Hidden components and preferred counts

| ID | Left | Right | Object | Resolution |
|---|---|---|---|---|
| C-CNT-1 | Compact grammar of four inputs plus output | “Every equation has five components” | Component count | The handoff already forbids the second claim. Enforce in the classifier |
| C-CNT-2 | Full GR needs geometry, stress-energy, gauge, nonlinearity, initial and boundary data | Pressure to keep a short role list | Honesty vs compactness | Prefer the expanded formulation. Missing-role warnings are a feature |
| C-CNT-3 | Prior sketch audit used “domain slot: one equation, one test” | Audited vocabulary forbids “slot” | Terminology | Use “independently specifiable component” or “one equation, one test, no glue” |

---

## 6. Fluids / arithmetic glue that must stay cut

| ID | Left | Right | Object | Resolution |
|---|---|---|---|---|
| C-GLUE-1 | SFE-PUB or SFE-QM as Chapter 1 of unaugmented NS | Track B PDE NS-B | Book identity | **Cut.** Domain Architect may *route* between books. It may not derive NS from SFE |
| C-GLUE-2 | Triple lock `SND ≡ GNC ≡ Bridge` | August audits: identity false | Equivalence | **RETIRED** |
| C-GLUE-3 | \(\lambda_{\min}(Q_N)>-1/2\) for all \(N\) | Computed counterexamples (\(Q_{10}\approx-1.90\), later \(H_4\approx-0.225\)) | Spectral floor | Full-spectrum claim **retired**. Do not import into FRA |
| C-GLUE-4 | Phi-cancel as a path to Theorem H | Identity \(r^{-4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\) is algebra only | Φ-cancel | Keep the identity in the swirl book. Do not feed it to SFE or FRA \(\Phi\) |

---

## 7. Software versus mathematics

| ID | Left | Right | Object | Resolution |
|---|---|---|---|---|
| C-SW-1 | Domain Architect v1.4 heuristic confidence | Physical probability of correctness | Confidence | Heuristic only. Never display as a posterior |
| C-SW-2 | Token extraction of symbols | Symbolic AST / computer-algebra equivalence | Parser | Current app is Level 0. AST work is future, not a silent upgrade of old maps |
| C-SW-3 | Complete-looking UHF / SFE / DHFA map | Validated law | Output meaning | A filled map is classification, not discovery |

---

## 8. Conflicts inside the audited gravity map (repair list)

These are not historical enemies. They are defects to fix before a gravity laboratory is treated as confirmatory.

| ID | Issue | Repair |
|---|---|---|
| C-GRV-EQ | Handoff linearized equation was split so the equals sign vanished | Write \(\square\bar h_{\mu\nu}=-(16\pi G/c^4)T_{\mu\nu}\) and declare signature |
| C-GRV-S | \(S_n=\rho_n\) versus \(\rho_n=S_n\psi_n\) | Choose one laboratory. Default: \(S_n=\rho_n\), \(\psi_n=1\), unless amplitude and phase are independently measured |
| C-GRV-0 | Zero mode of periodic Poisson | Already excluded (“nonzero modes”). Keep the zero-mean constraint as \(\mathcal B\) / solvability, not as a hidden \(P\) |
| C-GRV-λ | Writing \(\lambda_n^2\) hides that the operator is the inverse Laplacian | Prefer \(D=(-\nabla^2)\) and \(\lambda_n=k_n^{-2}\) **or** keep \(\lambda_n=k_n^{-1}\) but state that the model applies \(\lambda_n^2\). Do not switch mid-note |
| C-GRV-J | Identifiability Jacobian does not see a discrete prime mask | Treat selector comparisons as discrete experiments, not as \(\mathrm{rank}(J)\) |

---

## 9. RH Track B versus other books

| ID | Left | Right | Object | Resolution |
|---|---|---|---|---|
| C-TB-1 | RH Track B \(Q_N(i,j)=\mu(\gcd(i,j))/\gcd(i,j)\) | Inverse-GCD \(1/\gcd\) or \(1/(\gcd\sqrt{ij})\) | Operator | **Do not substitute.** Different spectra and proof obligations |
| C-TB-2 | RH Track B | Inventory NS-B (classical vorticity) | The name “Track B” | Different books. RH Track B is Möbius–GCD. NS-B stays fluids |
| C-TB-3 | First-row identity \(M(N)=e_1^{\mathsf T}Q_N\boldsymbol\mu_N\) | Hölder \(O(N)\) bound treated as RH-scale | Inequality | **Obstruction.** Generic pairing of \((\boldsymbol\mu_N,\mathbf 1)\) is \(\Theta(N)\) |
| C-TB-4 | Littlewood–Mertens realization | Route C \(-1/(2\pi)\) or \(\lambda_{\min}>-1/2\) | Inputs | **Quarantine** those historical claims. They are not this operator |
| C-TB-5 | RH Track B \(\mu(\gcd)/\gcd\) | Route C \(1/(\gcd\sqrt{ij})\) in `05_route_c_conditional.pdf` | Book | **Incompatible operators.** Keep Route C exploratory in Domain Architect. Do not file the PDF into ChatVault |
