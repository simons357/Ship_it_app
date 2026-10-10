# Signed transfer against the static obstruction

Date: 2026-10-08
Status: check only. Not a dynamical handoff. Not an NSE claim.

## Objects

Profile from the 2026-10-07 audit:

\[
A = e^{-r^2/2}(xy,\, xz,\, x+yz), \qquad U = \nabla \times A.
\]

div \(U = 0\). Full \(L^2\) mass and production:

\[
E_0 = \int |U|^2 = \tfrac52 \pi^{3/2}, \qquad
N_0 = \int \omega\cdot S(U)\,\omega = \tfrac{4\sqrt6}{27}\pi^{3/2} > 0.
\]

Absolute assembly on the same profile, recomputed by Gauss–Hermite on the degree-9 Gaussian density:

\[
Q_0 = \int \bigl|\omega\cdot S(U)\,\omega\bigr| \approx 14.049, \qquad
\rho_0 = N_0/Q_0 \approx 0.1438.
\]

Scaled family used for the obstruction:

\[
u(x) = a\, U(Kx), \qquad a = c\,\nu K.
\]

Then

\[
N(u) = a^3 N_0, \qquad Y(u) := \int |\nabla \omega|^2 = a^2 K\, Y_0,
\]

\[
\frac{N}{\nu Y} = c\,\frac{N_0}{Y_0}, \qquad E(u) = a^2 K^{-3} E_0 = c^2\nu^2 K^{-1} E_0.
\]

Positive production comparable to vorticity dissipation, on energy that can be arbitrarily small. Static coexistence only.

## Signed test

The signed transfer is

\[
T(u) = \int \omega\cdot S(u)\,\omega.
\]

On this family \(T = \rho_0 Q\), and \(\rho_0\) does not depend on \(a\) or \(K\). The same holds for any frozen profile: the cancellation fraction is invariant under the two-parameter scaling that produced the obstruction.

Consequences:

1. Sign retention multiplies the source by a profile constant. It does not change the power of \(K\), nor the relation \(E\sim \nu^2/K\).
2. The audited packet already keeps its signs, and still has \(\rho_0 > 0\). Covering that family forces any bound inherited from \(|T|\le Q\) to carry the same exponent obstruction as the nonnegative assembly.
3. A smaller functional is not a better power. \(|T|/(\sqrt E\, Y)\) grows like \(K^{1/2}\) on this family, so it is not a uniform improvement over the \(\theta = 1/2\) threshold.

Verdict: retaining signs does not overcome the static obstruction. It names a different integrand. The saturating family remains admissible for that integrand.

## What the time-dependent estimate still needs

The frozen family is not an NSE trajectory. A pointwise or scale-by-scale regrouping of \(T\) cannot supply the missing gain. The estimate has to be an integral over a turnover window, and it has to use the deformation of the packet.

Minimum content:

- Persistence of alignment. Bound the time on which \(\rho(t)\) can stay bounded away from zero while \(a(t)\sim \nu K(t)\). The static calculation gives no decay of \(\rho\).
- Back-reaction on the strain. Production at rate comparable to \(\nu Y\), sitting on energy \(E\sim \nu^2/K\), has to be charged against the coherent strain that sustains \(T\). The needed output is a depletion time shorter than the time required to regenerate the high-frequency enstrophy.
- Transport. The positive-production profile is not advected as a frozen shape. The estimate has to say what the advection and the self-stretching do to \(S\) and to the direction of \(\omega\), not only to the scalar \(T\).

Until one of those is closed, signed cancellation stays a constant factor on a non-solution. Critical high-frequency regeneration and positive production \(\beta\) remain the filed gates. Static \(C_{10}\) is not reopened by this check.
