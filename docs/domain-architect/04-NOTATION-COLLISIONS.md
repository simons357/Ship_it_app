# Notation collisions

Functional Role Analysis reuses short letters that already have other meanings in this research program. A role audit must record **which meaning is in force**. Capital \(P\) is never automatically “prime.”

## Permission, primes, and projectors

| Symbol | Allowed meaning in FRA | Other meanings that must be aliased |
|---|---|---|
| \(P\) | permission / admissibility projector or selector | — |
| \(p\) | an individual integer or prime | momentum; pressure |
| \(\mathbb P\) | the set of prime numbers | — |
| \(P_n=\mathbf 1_{\mathbb P}(n)\) | optional prime selector on a frozen index | — |
| \(\mathbb P_{\mathrm{Leray}}\) | — | Helmholtz / Leray projector on vector fields (Track A/B) |
| \(P_{j_*}\) | — | three-shell packet mass in Littlewood–Paley notes |
| \(\widetilde Q\rvert_{\mathbb P}\) | — | inverse-GCD matrix restricted to primes |

## Realized field, golden ratio, swirl, public phase

| Symbol | Allowed meaning in FRA | Other meanings that must be aliased |
|---|---|---|
| \(\Phi\) | realized output (field, potential, observable, next state) | — |
| \(\Phi_g\) | Newtonian gravitational potential (benchmark) | — |
| \(\varphi\) | golden ratio \((1+\sqrt5)/2\), only if derived | — |
| \(\Phi_{\theta}\) or \(\Gamma=ru_\theta\) | — | axisymmetric swirl; do not write this as \(\Phi\) in FRA notes |
| \(\varphi_{\mathrm{pub}}(x)\) | — | undefined spatial factor in retired SFE-PUB |

## Coupling versus arithmetic matrices

| Symbol | Allowed meaning in FRA | Other meanings that must be aliased |
|---|---|---|
| \(H\) | coupling / interaction | Hamiltonian in a declared mechanics model |
| \(H_g=4\pi G\) | Newtonian coupling in the gravity benchmark | — |
| \(H_N\) | — | degree-normalized inverse-GCD matrix |
| \(Q_N\) (RH Track B) | — | \(Q_N(i,j)=\mu(\gcd(i,j))/\gcd(i,j)\). Not \(1/\gcd\), not NS-B |
| \(\hat H_{\mathrm{SFE}}\) | — | retired Fock operator from prize-packaged drafts |

## Scale response

| Symbol | Role | Required declaration at each use |
|---|---|---|
| \(\lambda\) | scale response | type: wavelength, eigenvalue, inverse operator, spectral weight, or propagator |
| \(\lambda_n=1/k_n\) | gravity-benchmark choice | then the map applies \(\lambda_n^2\); say so |
| \(\lambda_i\) | — | strain eigenvalues in \(\omega\cdot S\omega=\lvert\omega\rvert^2\sum\lambda_i\cos^2\alpha_i\) |

## State, source, geometry

| Symbol | FRA meaning | Collision to avoid |
|---|---|---|
| \(\psi\) | state / coherence | wavefunction in a declared quantum model (allowed if that **is** the model) |
| \(S\) | source / drive | strain tensor in vorticity identities |
| \(g\) | geometry / metric / domain | coupling \(g\) in retired SFE-HAM; metric \(g_{ij}\) is fine when geometry is the role |
| \(F\) | external forcing | Flux \(\Pi_j\) in Littlewood–Paley notes (use \(\Pi_j\)) |
| \(\mathcal B\) | boundary and initial conditions | — |
| \(D\) | transformation / evolution operator | degree matrix in \(H_N=D^{-1/2}\widetilde Q D^{-1/2}\) |

## Guard for software

Any classifier must warn, not auto-resolve, when it sees:

- \(P\) without a declared type (permission vs Leray vs packet vs prime set);
- \(\Phi\) in a fluids document;
- \(\varphi\) without a derivation;
- \(\lambda\) without a type;
- the product \(P\cdot H\cdot\psi\) used as if it were a single primitive.
