# Audited baseline — Domain Architect / Functional Role Analysis

**Freeze date:** 2026-08-22  
**Authority:** Jonathan Simons handoff, “The Audited Harmonic Blueprint and Domain Architect”  
**Scope:** methods architecture only. No new physical law is declared here.

## 1. What this is

Functional Role Analysis is a recursive research architecture for reading a mathematical model in terms of:

- admissibility;
- interaction;
- state;
- scale response;
- realization;

while **declaring** rather than hiding additional independent sources, geometry, boundaries, dynamics, forcing, damping, and nonlinearity.

It may be useful for equation communication, model auditing, exposing hidden assumptions, cross-domain structural comparison, experiment design, and recording negative results.

It is **not** a completed unification, a proof that primes structure nature, a canonical Simons Field Equation (SFE), or a Millennium Prize result.

## 2. Required terminology

Use these names. Do not revive informal anatomical metaphors or the words “slot” and “knob.”

| Use | Do not use |
|---|---|
| functional role | — |
| independently specifiable component | “slot” |
| core role | — |
| extension role | — |
| role audit | — |
| expanded formulation | — |
| model component | — |
| tunable parameter (only when actual tuning is intended) | “knob” |
| Domain Architect | informal product nicknames |
| Functional Role Analysis | informal method nicknames |

## 3. Core organizing grammar

Four organizing inputs plus a realized output:

\[
(P,H,\psi,\lambda)\longrightarrow\Phi
\]

or, more honestly,

\[
\Phi=\mathcal F(P,H,\psi,\lambda;E),
\]

where \(E\) contains any additional independent structures required by the model.

These objects need not be scalars. Each may be a vector, tensor, operator, function, distribution, or family of modes.

The framework does **not** claim that every equation contains exactly five components.

### Core roles

| Symbol | Role | Typical occupants |
|---|---|---|
| \(P\) | permission / admissibility | projector, mask, constraint, selection rule, permitted subspace |
| \(H\) | coupling / interaction | coupling constant, matrix, Hamiltonian contribution, kernel, interaction weight |
| \(\psi\) | state / coherence | state vector, amplitude, modal coefficient, phase, density representation |
| \(\lambda\) | scale response (role name only) | must declare a subtype: spectral coordinate \(\kappa\), eigenvalue, wavelength, inverse eigenvalue, transfer function \(R(\kappa)\), propagator, Green function, or spectral weight |
| \(\Phi\) | realized output | field, potential, observable, response, or next state |

### Extension roles

Introduce a distinct component record whenever information would otherwise be hidden.

| Symbol | Role |
|---|---|
| \(S\) | source, input, density, or drive |
| \(g\) | geometry, metric, topology, or domain |
| \(\mathcal B\) | boundary and initial conditions |
| \(D\) | transformation, derivative, propagation, or evolution operator |
| \(\Xi\) | loss, damping, or decoherence |
| \(F\) | external forcing |
| \(N\) | nonlinear response or self-interaction |

A role may be implicit or fixed. Example: \(\Phi=H\psi\) may have \(P=I\) and \(\lambda=1\) implicitly.

## 4. When a component deserves its own record

Record a distinct component when it:

1. can be specified or varied independently;
2. changes an observable distinguishably;
3. has its own measured data, initial condition, or governing equation;
4. has distinct units, tensor type, or transformation behavior;
5. cannot be merged with another component without losing information.

A component may remain combined, implicit, or contextual when it is fixed, uniquely derived, redundant, gauge-dependent, or only identifiable through a product with another parameter.

When observables \(O_i\) and candidate parameters \(x_j\) are defined, local linear identifiability can be examined with

\[
J_{ij}=\frac{\partial O_i}{\partial x_j}.
\]

The rank of \(J\) estimates the number of locally distinguishable continuous parameter combinations. Dependent columns indicate redundant or inseparable components. Discrete selectors are not diagnosed by this Jacobian.

Do not report “the parameters are identifiable” from a local Jacobian. Report instead that the local Jacobian is full rank at the tested point, or that local sensitivity analysis indicates distinguishable parameter directions under the stated observables. Conditioning (singular-value ratios) and global identifiability are separate questions.

Stop decomposing when the remaining object is already a defined primitive, measured input, or standard operator whose internal structure lies outside the intended model.

## 5. Recursive layers (architecture, not laws)

### UHF — configuration layer

\[
\mathcal U=\mathcal F_U(P_U,H_U,\psi_U,\lambda_U;E_U).
\]

A usable UHF instance must specify function or Hilbert space, basis, inner product, operator domains, normalization, boundary conditions, and units.

### SFE — realization layer

\[
\Phi=\mathcal F_S(P_S,H_S,\psi_S,\lambda_S;\mathcal U,S,g,E_S).
\]

Several incompatible formulas have historically been called the SFE. **No formula should be chosen merely because it contains the preferred symbols.** A canonical SFE remains unresolved.

A future candidate must have defined variables and operators, dimensional consistency, declared domain and boundary conditions, known-theory limits, mathematical well-posedness, and at least one distinct testable prediction.

### DHFA — evolution layer

\[
\partial_t\Phi=\mathcal F_D(P_D,H_D,\psi_D,\lambda_D;\Phi,F,\Xi,E_D).
\]

“Movement,” “dynamics,” and “energy” are not synonyms. Any energy must be defined as a Hamiltonian, conserved functional, stress-energy component, or other domain-specific quantity.

## 6. Notation that must never be collapsed

\[
P=\text{permission projector or selector},\qquad
p=\text{an individual integer or prime},\qquad
\mathbb P=\text{the set of prime numbers}.
\]

A prime selector is only one experimental choice:

\[
P_n=\mathbf 1_{\mathbb P}(n).
\]

Capital \(P\) does not automatically mean “prime.” Other admissible choices include \(P=I\), ordinary physical or gauge projectors, low-mode masks, odd-mode masks, composite masks, random masks, or optimized selectors.

Also distinguish

\[
\Phi=\text{realized field or output}
\]

from

\[
\varphi=\frac{1+\sqrt5}{2}
\]

(the golden ratio). They are not interchangeable. Any appearance of \(\varphi\) must be derived, not inferred from spirals, imbalance, or recursion.

See [04 — Notation collisions](04-NOTATION-COLLISIONS.md).

## 7. Evidence hierarchy

| Level | Meaning | Current Domain Architect status |
|---|---|---|
| 0 | coherent classification | typical app output |
| 1 | mathematical compatibility | gravity FRA rewrite is **representation recovery** of Poisson, not a derivation |
| 2 | known-limit recovery | only if an independently specified broader model reduces to a known theory under a defined limit; not claimed for a canonical SFE |
| 3 | computational advantage under frozen fair tests | not established; Experiment 01 is a null |
| 4 | distinct quantitative prediction | not established |
| 5 | empirical support | not established |
| 6 | general physical theory with replication | not established |

Agreement among AI systems is not evidence at any level.

## 8. Origin story — motivational only

The origin story (undifferentiated potential, first distinction, permission, interaction, scale, realization, possible prime structure) may motivate research. It is not a physical derivation.

The following remain explicit:

- “Pure potential preceded structure” is philosophical until a state space and dynamics are defined.
- “A first imbalance occurred” resembles symmetry breaking but is not a cosmological derivation.
- “The imbalance was intentional” is theological, not a conclusion of the equations.
- A first imbalance does not mathematically imply the golden ratio.
- Prime structure at the beginning is meaningful only after identifying a canonical integer-indexed physical object.

Logical steps that must stay separate:

1. Primes generate the multiplicative structure of integers.
2. Some physical models use integer-indexed modes.
3. Nature privileges prime-indexed modes.

(1) and (2) do not imply (3). Calling a dimensional quantity such as “5 Hz” prime is unit-dependent.

## 9. Software posture

Domain Architect is a transparent heuristic classifier and laboratory, not a trained scientific language model. Confidence values are heuristic indicators, not probabilities of physical correctness.

The gravity laboratory described in the handoff is a one-dimensional, periodic, zero-mean Poisson test harness. It is not an astrophysical simulation.

The application does not currently construct a complete symbolic abstract syntax tree, prove algebraic equivalence, reliably infer units, enforce tensor-index consistency, solve arbitrary ODEs or PDEs, establish identifiability automatically, validate HB / UHF / SFE / DHFA / prime indexing, or discover new physics by producing a complete-looking map.

There is no live Grok integration in the delivered HTML build. A secure assistant would require an API-backed server so a key is not exposed in downloadable HTML.

## 10. What this freeze retires

- Informal method nicknames removed by the audit.
- Silent merging of incompatible SFE formulas.
- Treating an architectural mapping as a derivation or proof.
- Treating Experiment 01’s null as an invitation to retune nodes after TEST.
- Treating public-site or prize-packaged SFE language as the current scientific baseline.
