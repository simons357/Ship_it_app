# Domain Architect reading: Phi as universal geometry

**Essay:** [`PHI_GEOMETRY_BRIDGE.md`](PHI_GEOMETRY_BRIDGE.md) (May 2026)  
**Theorem paper:** [`Simons_PhiRenorm_Swirl_2026-08-22.tex`](Simons_PhiRenorm_Swirl_2026-08-22.tex)  
**Status note:** [`SWIRL-CONTINUATION.md`](SWIRL-CONTINUATION.md)

Domain Architect’s standing rule: **functional correspondence is a
hypothesis, not physical equivalence.** Sharing the letter \(\Phi\),
the integer 2, or the pattern “intensive = extensive / scale²” does
not make two systems the same physics.

This file is the DA reading of the essay. It does not rewrite the essay.

## Split

| Claim | Where it lives | DA kind |
|---|---|---|
| \(\Gamma = r u_\theta\), \(\Phi = \Gamma/r^2 = u_\theta/r\) | swirl book | definition in one PDE |
| \(\frac1{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\) on \(\{r>0\}\) | swirl book; May identity | **algebra.** Direct substitution \(T\colon\Gamma\mapsto r^2\Phi\) inside axisymmetric NS |
| Hardy not needed **for that rewrite** | swirl book | true for the rewrite; false if sold as “axis difficulty gone” |
| \(\Gamma\) maximum principle; energy \((*)\) in \(r^3\); \(\varepsilon\)-smoothness | 22 August theorems | swirl book |
| Classical unaugmented swirl globally regular | 22 August, status box | **open** |
| Strain pairing \(\int (u_r/r)\Phi^2 r^3\) absorbed uniformly in \(\varepsilon\) | 22 August §strain | **not closed** |
| Axis / LP shell / Riemann zeros as three prime-lattice quantization boundaries (essay “Theorem 5.4”) | geometry-bridge essay | **not a 22 August theorem.** Packaging. Strip from any submit |
| CMB quadrupole, Saturn hexagon, Venus pentagram, dodecahedral topology, Kabbalah Tikkun **are the same law** | geometry-bridge essay | **analogy at most.** No morphism \(T\) with a witness. Structure-preserving equivalence is **refused** |
| “The universe is a Navier–Stokes fluid at cosmological scale” | essay Part V | extra physical hypothesis; not implied by the identity |
| Swirl \(\Phi=u_\theta/r\) = FRA output \(\Phi\) = Newtonian \(\Phi_g\) | notation collision | **forbidden glue** |

The substitution that makes the identity true is **inside one equation**.
It is not a map from a vortex to the sky, to Saturn, or to a sefirotic
diagram.

## What the identity does and does not do

The identity is a change of dependent variable. Because
\(\partial_z(r^4)=0\), the centrifugal source written in \(\Gamma\)
is the \(z\)-derivative of \(\Phi^2\). That is the keeper.

It does not prove \(\Phi\in L^\infty\). It does not kill the strain
pairing in \((*)\). It does not select a hexagonal eigenmode. The
integer 2 in \(r^2\) is the algebraic weight of that substitution,
not a prime acting on the PDE, the CMB, or the night sky.

## Live lab (verified)

Decompose of `(1/r^4)*dz(Gamma^2) = dz(Phi^2)` returns `unclassified`
at Level 0 and warns that \(\Phi\) is an identifier, not a
gravitational potential.

Translate of that identity against `Phi = Gamma / r^2` returns
`kind: analogy`, confidence 0.2, `broken: no_checked_structure_map`.
That is fail-closed. It is **not** confirmation of a cosmic lattice.
The dump-era mapper also aligns symbols by name and is not a witness.

## How to try the split in the app

1. Decompose tab → **Swirl identity** → Decompose. That is the algebra.
2. Do **not** treat a later Translate into CMB / hexagon / Tikkun
   language as a proof. Until a tested morphism exists, the verdict
   is analogy or incompatible, never physical identity.

Open the app on your Mac with `Open Domain Architect.command` or:

```bash
python3 -m domain_architect app
```
