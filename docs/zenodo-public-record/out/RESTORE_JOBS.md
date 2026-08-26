# Restore jobs (agent + PAT, not 27 clicks)

Do not click Edit on each Zenodo record. Titles are restored by:

```bash
python3 docs/zenodo-public-record/api_restore_titles.py --apply
```

That command needs a Zenodo **personal access token** in `ZENODO_TOKEN` or `ZENODO_ACCESS_TOKEN` (scopes `deposit:write`, `deposit:actions`). Create one at https://zenodo.org/account/settings/applications/tokens/new/ and tell an agent: “use this token”. Never a zenodo.org password.

Planned jobs: status-note rename (2 version IDs) + 20 stamped restores = 22 title writes. Optional 22045478 is off unless `--include-optional`.

**Status note title:** August 2026 status note: live stack and walked-back prize language

## Job titles (source of truth: titles.json)

- `22050978` / `22045484` → August 2026 status note: live stack and walked-back prize language
- `20405526` → Global Regularity of the Navier-Stokes Equations on T3: Spectral Non-Dispersal, the Ring Lemma, Phi-Renormalization, and the Shell-Conditioned Commutator Estimate
- `20269843` → The Quantum Lens: A Spectral Framework Connecting the Millennium Prize Problems
- `20405593` → The Montgomery–Dyson Coincidence as a Q6 Prime Lattice Eigenvalue Identity
- `20518294` → Route C: Spectral Closure of the Zero-Density Law — Conditional on Two Analytic Gaps
- `20518250` → Route C: Spectral Closure of the Zero-Density Law — Conditional on Two Analytic Gaps
- `20552400` → A Universal Non-Concentration Principle: SND ≡ GNC ≡ Bridge
- `20552682` → The Prime Lattice as a Prototype for the BSD Hamiltonian: Rank as Spectral Multiplicity and the Zeta-Function Case of the Birch and Swinnerton-Dyer Conjecture
- `20552171` → A Quantum Field Theory on the Prime Manifold: Navier–Stokes, Riemann, and Goldbach Under a Single Hamiltonian
- `20552223` → A Quantum Field Theory on the Prime Manifold: Navier–Stokes, Riemann Hypothesis, and Goldbach Under a Single Hamiltonian
- `19842060` → Borromean Triads, the Ring Lemma, and Spectral Non-Dispersal
- `20272545` → Spectral Non-Concentration Implies Global Regularity for 3D Navier–Stokes on T³
- `20271457` → The Ramanujan–Möbius Identity and Prime Lattice Spectral Theory: GCD Operators, Spectral Floors, and the Arithmetic Casimir Constant
- `20272622` → The Quantum Millennium: A Spectral Unification of the Navier–Stokes Problem and the Millennium Prize Conjectures
- `20405585` → Borromean Triads, the Ring Lemma, and Spectral Non-Dispersal: A Conditional Regularity Framework for 3D Navier-Stokes
- `20405599` → The GCD Spectral Attractor: A Unified Structural Framework for Navier-Stokes, the Riemann Hypothesis, and the Simons Field Equation
- `20269536` → Spectral Non-Concentration Criteria for Navier–Stokes Regularity on T³
- `20405591` → The Q_N Operator: Self-Adjointness, Spectral Floor, and a Route to the Riemann Hypothesis via Renormalized GCD Eigenvalues
- `20183673` → Diffuse Cascade in 3D Navier–Stokes: Time-Resolved Evidence for Triad Equidistribution
- `20184148` → The Montgomery–Dyson Coincidence Resolved by the Q6 Prime Lattice Operator
- `20271879` → Spectral Properties of GCD Operators and Ramanujan Quadratic Forms

## Calm description pointer (API writes this; do not paste by hand)

<p>August 2026: prize-claim language in this deposit is walked back. The file remains published and open. See the footnote on page 1 and the errata on page 2 of the status note <a href="https://doi.org/10.5281/zenodo.22050978">10.5281/zenodo.22050978</a>. Live Route C: <a href="https://doi.org/10.5281/zenodo.22050963">10.5281/zenodo.22050963</a>. Live Φ-renormalization: <a href="https://doi.org/10.5281/zenodo.22050974">10.5281/zenodo.22050974</a>. Live Ring: <a href="https://doi.org/10.5281/zenodo.22050976">10.5281/zenodo.22050976</a>. Unconditional 3D Navier–Stokes, the Riemann hypothesis, and Goldbach are not claimed.</p>

## Optional (`--include-optional`)

- `22045478` → The Inverse-GCD Operator Q_N: Definitions and a Restricted Rayleigh Bound
  - Optional. Latest sibling 10.5281/zenodo.22050962 / concept 20405588 is already cleaner. Do not put WITHDRAWN in the new title.
