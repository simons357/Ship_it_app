# Historical equation inventory

**Purpose:** list distinct formulas that have been called UHF, SFE, DHFA, gravity-as-HB, or prime-index structure, without merging them.

**Rule:** one row, one formula, one declared meaning. Incompatible formulas stay incompatible.

**Coverage:** this pass uses (a) the August 2026 audited handoff, (b) this repository’s closed ringdown experiment, (c) prior Cursor agents on this repo, (d) public-site / LinkedIn fragments those agents retrieved, and (e) historical papers mirrored on branch `cursor/tao-snd-h-panel-a0eb`. It does **not** yet include the working paper PDF/DOCX/MD, Domain Architect v1.4 source, or `GUIDE.md`, which are not in this repository.

Disposition codes:

| Code | Meaning |
|---|---|
| **RETAIN-ARCH** | Keep as architecture / role grammar, not as a physical law |
| **RETAIN-BENCH** | Keep as a known-theory benchmark |
| **RETAIN-NULL** | Keep as a closed, frozen negative or null result |
| **REVISE** | Keep the object only after repairing definitions, units, or claims |
| **RETIRE** | Do not use as a current scientific statement |
| **UNRESOLVED** | Named, but no unique justified formula |

---

## A. Functional Role Analysis (audited, 2026-08)

| ID | Formula | Declared meaning | Disposition |
|---|---|---|---|
| FRA-1 | \((P,H,\psi,\lambda)\longrightarrow\Phi\) | Compact organizing grammar | **RETAIN-ARCH** |
| FRA-2 | \(\Phi=\mathcal F(P,H,\psi,\lambda;E)\) | Honest expanded grammar; \(E\) holds extra independent structure | **RETAIN-ARCH** |
| FRA-3 | \(\Phi=H\psi\) with \(P=I\), \(\lambda=1\) implicit | Example of hidden / fixed roles | **RETAIN-ARCH** |
| FRA-4 | \(\mathcal U=\mathcal F_U(P_U,H_U,\psi_U,\lambda_U;E_U)\) | UHF as configuration layer | **RETAIN-ARCH** / **UNRESOLVED** as a unique PDE |
| FRA-5 | \(\Phi=\mathcal F_S(P_S,H_S,\psi_S,\lambda_S;\mathcal U,S,g,E_S)\) | SFE as realization layer | **RETAIN-ARCH** / **UNRESOLVED** as a unique PDE |
| FRA-6 | \(\partial_t\Phi=\mathcal F_D(P_D,H_D,\psi_D,\lambda_D;\Phi,F,\Xi,E_D)\) | DHFA as evolution layer | **RETAIN-ARCH** / **UNRESOLVED** as a unique PDE |
| FRA-7 | \(J_{ij}=\partial O_i/\partial x_j\) | Local linear identifiability diagnostic | **RETAIN-ARCH** (continuous parameters only) |
| FRA-8 | \(P_n=\mathbf 1_{\mathbb P}(n)\) | Optional prime selector; one experimental choice for \(P\) | **RETAIN-ARCH** as a selector family, not as physics |

---

## B. Gravity benchmarks (audited)

| ID | Formula | Declared meaning | Disposition |
|---|---|---|---|
| GRV-1 | \(\nabla^2\Phi_g=4\pi G\rho\) | Newtonian gravity | **RETAIN-BENCH** (standard physics) |
| GRV-2 | \(-\nabla^2 u_n=k_n^2 u_n\) | Laplacian eigenfunctions | **RETAIN-BENCH** |
| GRV-3 | \(\Phi_{g,n}=-(4\pi G/k_n^2)\rho_n\) | Modal Poisson solution, nonzero modes | **RETAIN-BENCH** |
| GRV-4 | \(\Phi_{g,n}=-P_n H_g\lambda_n^2 S_n\) with \(H_g=4\pi G\), \(\lambda_n=1/k_n\), \(S_n=\rho_n\) | Functional Role Analysis of GRV-3 | **RETAIN-BENCH** at evidence Levels 1–2 when \(P_n=1\) |
| GRV-5 | \(\rho_n=S_n\psi_n\) and \(\Phi_{g,n}=-P_n H_g\lambda_n^2 S_n\psi_n\) | Optional split of source amplitude and phase | **REVISE** — conflicts with GRV-4’s assignment \(S_n=\rho_n\); keep only if the split is independently justified |
| GRV-6 | \(\square\bar h_{\mu\nu}=-(16\pi G/c^4)T_{\mu\nu}\) | Linearized gravity in harmonic gauge (handoff formatting dropped the equals sign) | **RETAIN-BENCH** after declaring metric signature, gauge, and units |
| GRV-7 | \(P_n=\mathbf 1_{\mathbb P}(n)\) inside GRV-4 | Prime-mask compression experiment on a frozen Laplacian basis | **RETAIN-ARCH** as a representation hypothesis only |

GRV-4 recovers GRV-3 when \(P_n=1\). That is known-limit recovery, not a new gravity theory.

Full general relativity is **not** GRV-1 or GRV-6. Independently necessary geometry, stress-energy, gauge constraints, nonlinear self-interaction, initial data, and boundary data must not be hidden to preserve a preferred component count.

---

## C. Historical SFE formulas (do not merge)

| ID | Formula | Source | Declared meaning | Disposition |
|---|---|---|---|---|
| SFE-PUB | \(\Phi(x,t)=\sum_p A_p\sin(2\pi f_p t/\varphi(x)+\delta_p)\) | `theharmonicblueprint.com`; prior agents 2026-08-21/22 | “Chapter-1 field”; prime-indexed oscillator plus coherence attractor; public unification language | **RETIRE** as a physical law or unifier. Archive as a historical public formula. Symbols \(A_p,f_p,\varphi(x),\delta_p\) were not defined in the retrieved fragments |
| SFE-QM | \(\Delta\bigl((P\cdot H\cdot\psi)^2\cdot\lambda\bigr)=\Phi\) | `QUANTUM_MILLENNIUM.tex` on `cursor/tao-snd-h-panel-a0eb` | Called both a Lagrangian and an equation of motion of a prime-lattice field theory | **RETIRE** as a current SFE. Undefined \(\Delta\); role meanings contradict FRA; prize packaging |
| SFE-HAM | \(\hat H_{\mathrm{SFE}}=\sum_n n^{-1/2}\hat N_n+\frac g2\sum_{ij}\hat N_i\hat N_j/\gcd(i,j)-\sum_n J_n(\hat a_n+\hat a_n^\dagger)\) | same file | Second-quantized Hamiltonian; free term mapped to \(H\), \(Q_N\) interaction mapped to \(P\), source \(J\) mapped to \(\Phi\) | **RETIRE** as SFE. Arithmetic / Fock model, not the FRA realization layer. Inverse-GCD floor claims in the same paper are withdrawn |
| SFE-GCD | “GCD-attractor SFE” / “one attractor, three prizes” | August errata; KEEP-CUT inventory; NS pathway | Claimed common attractor for NS / RH / Goldbach | **RETIRE** — already withdrawn |
| SFE-FLUX | “SFE = Shell Flux Estimate” | Early NS-pathway guess, later abandoned | Attempt to read SFE as a Littlewood–Paley flux bound | **RETIRE** — acronym collision, not a definition |
| SFE-CANON | (none justified) | audited handoff §6 | Canonical realization equation | **UNRESOLVED** |

Do not choose among SFE-PUB, SFE-QM, and FRA-5 by symbol overlap.

---

## D. Historical UHF / DHFA

| ID | Formula | Source | Declared meaning | Disposition |
|---|---|---|---|---|
| UHF-1 | (no equation found) | public notes; Domain Architect sketch audit | “Wrapper: primes, curvature, zeta, entropy in one recursive story” | **UNRESOLVED**. Name only. FRA-4 is the architectural placeholder |
| DHFA-1 | \(V_{\mathrm{DHFA}}(x,t)\) | Domain Architect sketch audit | “Time-varying potential; standing-wave / coherence engine” | **UNRESOLVED**. Symbol only; no PDE, units, or well-posedness |
| DHFA-2 | (name collision) | early NS-pathway draft | “Directional / harmonic field analysis” as a labeling layer | **RETIRE** as a definition of DHFA |
| DHFA-3 | FRA-6 | audited handoff | Evolution-layer architecture | **RETAIN-ARCH** only |

---

## E. Closed prime-index experiment in this repository

Experiment 01 is a spectral-proximity test, **not** a field equation and **not** the gravity prime mask GRV-7.

| ID | Formula | Meaning | Disposition |
|---|---|---|---|
| EXP01-1 | \(d(x,R)=\min_r\lvert\log(x/r)\rvert\) | log-distance from observation \(x\) to node family \(R\) | **RETAIN-NULL** |
| EXP01-2 | \(s(x,R)=\exp[-d(x,R)^2/(2\sigma^2)]\), \(\sigma=0.05\) frozen | proximity kernel | **RETAIN-NULL** |
| EXP01-3 | \(S(R)=N^{-1}\sum_i s(x_i,R)\) | family score | **RETAIN-NULL** |
| EXP01-4 | default observable \(x=\omega_R(i)/\omega_R(j)\) and reciprocal | dimensionless frequency ratio | **RETAIN-NULL** |
| EXP01-5 | families: integer/rational, Fibonacci, golden ratio, prime-neighbor ratios, frozen random | predefined comparison families | **RETAIN-NULL** |

Held-out TEST (no retuning): no family met \(q\le 0.05\). Prime family score \(0.807\), \(p=0.171\), \(q_{\mathrm{BH}}=0.381\). Primary H0 was not rejected. Secondary prime/HB hypothesis was not supported.

This is evidence Level 3 **failure** under Experiment 01’s own protocol. It is not a gravity-laboratory result and does not use equal node budgets (see conflict C-BUDGET).

---

## F. Adjacent formulas that must stay in other books

These are real research objects in this repo family. They are **not** UHF, SFE, or DHFA.

| ID | Formula | Book | Disposition relative to Domain Architect |
|---|---|---|---|
| NS-B | \(\partial_t\omega+(u\cdot\nabla)\omega=(\omega\cdot\nabla)u+\nu\Delta\omega\), \(\nabla\cdot u=0\) | Track B, classical NS | Route as a separate domain. Do not derive from SFE |
| NS-A | \(\partial_t u+(u\cdot\nabla)u=-\nabla p+\nu\Delta u+\varepsilon^\alpha\mathbb P\,\mathrm{div}(\lvert\nabla u\rvert^\beta\nabla u)\) | Track A, augmented NS | Different PDE. \(\mathbb P\) here is the Leray projector, not permission \(P\) and not primes |
| NS-Φ | \(\Gamma=ru_\theta\), \(\Phi=\Gamma/r^2=u_\theta/r\), \(r^{-4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\) | axisymmetric swirl algebra; June 30 conditional paper under `docs/papers/swirl/` | **KEEP** algebra. Open barrier \(\|u^r/r\|_\infty\) (see `PHI-RENORM-AUDIT-2026-08-22.md`). **Do not reuse \(\Phi\)** as the FRA output symbol; **not** Clay |
| ARITH-H | \(H_N=D^{-1/2}\widetilde Q_N D^{-1/2}\) | inverse-GCD / spectral floor | Separate arithmetic book. \(H_N\) is not coupling \(H\) |
| ARITH-B | Bridge* pair Rayleigh \(R(e_p-e_q)>-1/2\) | pair vectors only | Keep only as arithmetic, if at all. Not a fluids or SFE input |

---

## G. Hilbert–Pólya program (adjacent book, 2026-09)

This is **not** SFE, not a canonical Hamiltonian, and **not** a proof of RH.
Full write-up: [06 — Hilbert–Pólya program](06-HILBERT-POLYA-PROGRAM.md).
Software: `python -m domain_architect --hilbert-polya`.

Assigning \(\Phi:=\{\gamma_n\}\) is recorded as a circular fill (HP-H007), not as a construction.

| ID | Formula | Declared meaning | Disposition |
|---|---|---|---|
| HP-H001 | \(H=H^\ast\) and \(\operatorname{spec}(H)=\{\gamma_n\}\) \(\Rightarrow\) RH | Program statement / strategy | **RETAIN-ARCH** as a strategy, not a theorem |
| HP-H002 | Weil explicit formula (zeros \(\leftrightarrow\) primes) | Theorem; belongs in \(E\), not as FRA \(H\) | **RETAIN** as theorem |
| HP-H003 | \(H=xp\) (or \((xp+px)/2\)) with cutoff | Berry–Keating heuristic | **UNRESOLVED** as a Hamiltonian |
| HP-H004 | adelic absorption spectrum (missing lines) | Connes program; not the same operator as HP-H003 | **UNRESOLVED** |
| HP-H005 | pair correlation of \(\{\gamma_n\}\) matches GUE | Universality class, not identity | **RETAIN** as statistics only |
| HP-H006 | \(\xi(s)=\xi(1-s)\) | Theorem; possible left-hand side of a \(\det\) identity | **RETAIN** as theorem |
| HP-H007 | \(\Phi:=\{\gamma_n\}\) or \(H=\operatorname{diag}(\gamma_n)\) | Circular FRA fill | **RETIRE** as a construction; keep as a null |
| HP-H008 | Laguerre–Pólya class of \(\xi(1/2+iz)\) | Proven entire-function calculus; parallel RH route | **RETAIN** as theorem; not a Hamiltonian |
| HP-H009 | Jensen polynomials of \(\xi\) \(\to\) Hermite (GORZ) | Asymptotic real-rootedness | **RETAIN**; not RH |
| HP-H010 | \(N(T)=(T/2\pi)\log(T/2\pi e)+S(T)+O(1)\) | Weyl-law target | **RETAIN** as theorem |
| HP-H011 | Pólya 1926 cosine-transform real-zero criterion | Proven sufficient condition; hypotheses unverified for Riemann’s \(\Phi\) | **RETAIN** as theorem; does not fill \(H\) |
| HP-H012 | \(\Xi(z)=\int_0^\infty\Phi(t)\cos(zt)\,dt\) | Shape that makes 1926 applicable in principle | **RETAIN** as representation |
| HP-H013 | \(L(x)=\sum_{n\le x}\lambda(n)\le 0\) | Pólya Liouville conjecture | **RETIRE** — disproved (Haselgrove) |
| HP-H014 | \(\Xi_t\) real-zero for \(t\ge\Lambda\); \(\Lambda\ge 0\); RH \(\Leftrightarrow\Lambda=0\) | de Bruijn–Newman constant | **RETAIN**; \(\Lambda\ge 0\) theorem; \(\Lambda=0\) is RH; not \(H\) |
| HP-H015 | Pólya–Schur multiplier sequences | Algebraic LP filter | **RETAIN**; \(\gamma_k\) multipliers \(\neq\) Riemann \(\gamma_n\) |
| HP-H016 | Pólya 1926 Acta integral representation of \(\xi\) | Distinct from the cosine-zero criterion | **RETAIN** as representation |
| HP-H017 | Pólya frequency / variation-diminishing kernels | Language of the 1926 hypotheses | **RETAIN**; a PF check on Riemann’s \(\Phi\) is not \(H\) |
| HP-H018 | Turán inequalities | Coefficient tests for LP / Jensen | **RETAIN**; not RH unless checked for \(\xi\) without assuming RH |
| HP-H019 | Pólya–Szegő 1951 isoperimetric inequalities in mathematical physics | Capacity, torsion, Laplacian eigenvalues | **RETAIN** as other-book; **INSUFFICIENT** as Clay NS |
| HP-H020 | Pólya 1954 membrane eigenvalues | Domain Weyl law | **RETAIN**; unmerged with \(N(T)\) |
| HP-H021 | Pólya 1937 enumeration theorem | Combinatorics | **RETAIN** as dump; no \(\xi\) map |
| HP-H022 | Pólya 1921 random-walk recurrence/transience | Probability | **RETAIN** as dump; no \(\xi\) map |
| HP-H023 | Pólya 1918 / 1923 zeros of entire functions | Earlier zero-distribution calculus | **RETAIN**; not \(\operatorname{spec}(H)=\{\gamma_n\}\) |
| HP-H024 | Pólya 1915 integer-valued entire functions | Entire functions taking integer values | **RETAIN** as dump; different book from \(\xi\) |

Do not merge HP-H003 with HP-H004, HP-H005, HP-H008, or retired SFE-HAM (`SFE-H003`).

---

## H. Public / web formulas not treated as Simons SFE

Retrieved by prior agents; authorship or domain is mixed or unrelated. Listed so they are not silently absorbed.

| ID | Formula | Note | Disposition |
|---|---|---|---|
| WEB-E | \(E=mc^2(v/c)^{\pm\ln(P)/\ln(27)}\) | Zenodo “Harmonic Framework of Reality” abstract | **RETIRE** from this project unless a primary source ties it to the audited paper |
| WEB-Ψ | \(\Psi_\tau(r,t)=\varepsilon(t)\sin(\omega_\tau t)\exp(-\lambda(t)r^2)\) | “Tau field envelope,” 27 Hz lattice | **RETIRE** from this project pending provenance |
| WEB-h | exoplanet “prime height” \(h=p+q\) | Experiment 01 deliberately avoided this data | **RETIRE** as HB evidence |
| WEB-L | Harmonic Lagrangian (Zenodo `20393974`) | Snippet author listed as Peter James Thompson | **Do not ingest** as Simons SFE |

---

## I. Still missing from the inventory

Until the files in [03 — Reconciliation §6](03-RECONCILIATION.md) arrive, the following historical objects cannot be inventoried from primary text:

- Domain Architect v1.4 classifier rules and gravity-harness equations;
- working paper v1.0 displayed formulas beyond the handoff;
- unpublished SFE / UHF / DHFA book chapters;
- any additional SFE variants that exist only in Kara / Gemini / camera-roll drafts.

A later pass must add those as new IDs, not overwrite the rows above.
