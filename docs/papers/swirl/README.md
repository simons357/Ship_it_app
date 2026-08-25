# Axisymmetric swirl — separate book

This is **not** live Domain Architect. DA may route to this book. It must
not glue swirl \(\Phi = u_\theta/r\) to FRA output \(\Phi\).

## Paper (22 August 2026)

[`Simons_PhiRenorm_Swirl_2026-08-22.tex`](Simons_PhiRenorm_Swirl_2026-08-22.tex)

**Phi-renormalization for axisymmetric Navier–Stokes with swirl: identity, circulation principle, and the five-dimensional energy**

Four theorems: the algebraic identity \(\frac1{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\) with \(\Gamma=ru_\theta\), \(\Phi=u_\theta/r\); the \(\Gamma\) maximum principle; the intensive energy identity in the \(r^3\) measure; global smoothness of the \(\varepsilon\)-hyperviscous system. Classical unaugmented swirl remains open. Strain estimates are recorded, not closed.

## Public May 2026 deposit

- Concept DOI: https://doi.org/10.5281/zenodo.20405404
- Latest file DOI: https://doi.org/10.5281/zenodo.20405405
- PDF: https://zenodo.org/records/20405405/files/PhiRenorm_TrackB.pdf
- Short companion: https://doi.org/10.5281/zenodo.20405597

## Status note

[`SWIRL-CONTINUATION.md`](SWIRL-CONTINUATION.md) is the 22 August reconstruction of what stands. [`phi_renorm_continuation.tex`](phi_renorm_continuation.tex) is the earlier continuation sketch.

## May 2026 geometry-bridge essay

[`PHI_GEOMETRY_BRIDGE.md`](PHI_GEOMETRY_BRIDGE.md) is the author’s
essay *The Phi-Renormalization as Universal Geometry*. It links the
axis identity to CMB, Saturn, a dodecahedral lattice, and Kabbalah.

That essay is a **correspondence hypothesis**. Domain Architect does
not award it as physical equivalence. The DA reading is
[`DA-ON-PHI-GEOMETRY.md`](DA-ON-PHI-GEOMETRY.md). The 22 August
theorem paper does not use Q6 / primes / spectral clock as load-bearing
mathematics.

One paste-ready file for a **new** ChatGPT chat (not Chat Vault):
[`docs/packets/DA-AND-NS-CHATGPT.md`](../../packets/DA-AND-NS-CHATGPT.md).

## Try it in Domain Architect

Launch the desktop app, open **Decompose**, and click **Swirl identity** (or paste the lines below). Live Decompose currently returns `unclassified` at Level 0 and warns that \(\Phi\) is an identifier, not a gravitational potential. That is expected: this lab is not a fluids solver, and swirl \(\Phi=u_\theta/r\) must not be glued to FRA output \(\Phi\).

```
(1/r^4)*dz(Gamma^2) = dz(Phi^2)
```

or the intensive field:

```
dt F + ur*dr F + uz*dz F + 2*(ur/r)*F = nu*(drr F + (3/r)*dr F + dzz F)
```
