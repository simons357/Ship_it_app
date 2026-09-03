# Computing bench — proceed map (2026-09-03)

**Status:** operating-system freeze, not a Millennium close  
**Command:** `python -m domain_architect --proceed`  
**This document is not a unified theory.**

The computing / software bench (Turing, von Neumann, Hamming, Wilkinson,
Kahan, Knuth, Dijkstra, Parnas, Lamport, Hoare, McCarthy, Shannon, Backus)
plus program review (Einstein, Weinberg, Weyl, Wigner, Feynman, Tesla) was
asked how to set the math and the computer for Riemann and Navier–Stokes,
how we are doing, and where to go next. Fluids constraints: Leray,
Beale–Kato–Majda, Caffarelli–Kohn–Nirenberg. RH constraint: LMFDB /
analytic number theory.

A team is not a vote.

## Clip splice

If two equations are almost the same, clip the excess so the **cores**
match. The clipped remainder gets an ID and a measurement. It is never
discarded. Aligned cores are not a proof that the original equations are
the same.

```bash
python -m domain_architect --clip \
  "laplacian Phi = 4 * pi * G * rho" \
  "laplacian Phi = 4 * pi * G * rho + Lambda * Phi"

python -m domain_architect --clip \
  "partial_t u + (u * nabla) * u = - nabla p + nu * laplacian u" \
  "partial_t u + (u * nabla) * u = - nabla p + nu * laplacian u + epsilon * div(f)"
```

The second clip is the Q1 extra term: a `DYNAMICS_TERM` with its own
`CLIP-…` ID. Independently specifiable. Not zero. Not \(A\Rightarrow B\).

## Track B chain (shape per step)

```bash
python -m domain_architect --chain B
```

Each lemma is shown as: statement, what it looks like, verdict, **shape
delta**, and a clip ID if something was cut off. Passes add texture.
Failures clip fake upgrades. Only a closed bound on \(X=\|\omega\|_2^2\)
would change the domain shape. That step is still **open**.

Full geometric analysis (tube, shells, strain, swirl):
[`07-NS-GEOMETRIC-ANALYSIS.md`](07-NS-GEOMETRIC-ANALYSIS.md) and
`python -m domain_architect --geometry B`.

Stop at the wall; see the missing piece and the candidates after it:
[`09-NS-GAP.md`](09-NS-GAP.md) and `python -m domain_architect --gap B`.

Play with the shape (fill the other side, then measure):
[`10-NS-SHAPE-PLAY.md`](10-NS-SHAPE-PLAY.md) and
`python -m domain_architect --shape-play B`. Strain really completes.
The cylinder only completes if you put a mirror in. That is extra \(E\).

Energy as a visual object (see the outside, guess the shape):
[`11-NS-ENERGY-PLAY.md`](11-NS-ENERGY-PLAY.md) and
`python -m domain_architect --energy-play B`. Bernstein really fills
enstrophy from shell energy. Guessing the tube from off-axis energy is
play. Seeing Leray energy does not bound \(X\).

Overlay the done pieces into one general architecture shape, then refine
a hole: [`12-NS-OVERLAY.md`](12-NS-OVERLAY.md) and
`python -m domain_architect --overlay B`. T3a is done on a cylinder and
is **not** transposable onto \(\mathbb{T}^3\). Open layers stay off the
stack.

See it as pictures, not as a terminal dump:
[`13-NS-SEE.md`](13-NS-SEE.md) and `python -m domain_architect --see B`.
Open `see.html` in a browser. CosmoEvolution is not this desk.

The picture is a **package appendage**. It follows the math automatically
(`--tube` rewrites `see-state.json` and the HTML banner). The think tank
stays `--proceed`. Details: [`14-PACKAGE.md`](14-PACKAGE.md).

If a slot is empty, break DA into pieces and scan for a fit:
[`15-NS-SCAN.md`](15-NS-SCAN.md) and `python -m domain_architect --scan B`.
A match is not a weld. Wrong-object pieces (Q, gravity, Cosmo) stay out.

Live tube estimate (Hardy inside, Young outside, \(I_{\mathrm{tube}}\) open):
[`08-NS-TUBE-ESTIMATE.md`](08-NS-TUBE-ESTIMATE.md) and
`python -m domain_architect --tube B`. T3a (wall as a two-sided cylinder)
holds as an identity when swirl vanishes at an outer radius. The weld to
\(I_{\mathrm{off}}\) (`CLIP-T3-WELD`) and outer vanishing on \(\mathbb{T}^3\)
(`CLIP-T3-OUTER`) stay clipped.

## Shape first

The object is a **shape**. Notation is a **texture**. Same shape, different
chart (NS PDE vs \(J/X\)) is legal navigation and still not a proof.
Different shape even when symbols rhyme (\(J/X\) vs \(\lambda_{\min}\)) is
`INCOMPATIBLE_SHAPE`. Cosmo pictures are not the shape of NS or RH.

```bash
python -m domain_architect --shape-compare NS-B J/X
python -m domain_architect --shape-compare J/X LAMBDA-MIN
```

## Who is not the website

| Name | Job | Repo / URL |
|---|---|---|
| **Domain Architect** | compiler / inquiry | this git; working PWA on `cursor/domain-architect-app-f96b` |
| **ChatVault** | search / inbox | `chatvault/` **inside** `Ship_it_app`. Not a separate GitHub repo |
| **CosmoEvolution 3D** | visualization only | https://cosmoevolution3d.base44.app |

ChatVault must not certify a lemma. CosmoEvolution must not compile.

## How we are doing

The lab is real. The public cosmos site is not the lab.

- Four unglued books (A / B / Q / U), refuse-glue, evidence levels, and a
  null registry are the right machine.
- Canonical SFE remains **unresolved**. Experiment 01 remains a **closed null**.
- CosmoEvolution brands itself “Domain Architect — Universe Evolution” and
  claims 16/16 Standard Model parameters from topology. That claim is
  **retired as evidence** (`VIZ-H001`, `NULL-COSMO-UNIFIER`). Keep the
  on-site sentence that no tested vacuum ratio matches \(\cos\theta_W\).

## Where we go from here

1. Navigate by shape first. Do not start from Cosmo symbols.
2. Run this desk as Domain Architect. Do not treat the Cosmo URL as the DA site.
3. Stop at the first open wall (`--gap B`). Name the missing piece
   (GAP-T3: `CLIP-T3-WELD` + `CLIP-T3-OUTER`). T5 is a candidate after
   the gap, not a step. Keep \(1/r^4\). Regularity stays open. No close
   announcement.
4. One Track Q numeric floor, documented. \(\lambda_{\min}(H_N)\ge -1/4\) stays
   numeric until proved. No operator\(\to\zeta\) lemma ⇒ no RH.
5. ChatVault stays search. The 160-page HB2 file, if it surfaces, goes there.
   Do not wait on screenshots before the next lemma.
6. Banner CosmoEvolution `VIZ ONLY`.

Illegal splices are an opcode, not a vibe:

```bash
python -m domain_architect --refuse-splice COSMO B
python -m domain_architect --refuse-splice SEARCH RH
python -m domain_architect --refuse-splice A B
```

All three must print `REFUSED`.

## Machine-readable

- `VIZ-H001`, `SYS-H001` in `data/domain_architect/historical_equations.json`
- `NULL-COSMO-UNIFIER`, `NULL-CHATVAULT-ORACLE` in `null_results.json`
- `domain_architect/desk.py`
