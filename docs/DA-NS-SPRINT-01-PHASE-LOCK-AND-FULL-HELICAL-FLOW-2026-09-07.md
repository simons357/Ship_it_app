# Domain Architect Navier–Stokes Sprint 01

## Phase, Symmetry, Zeros and the Frozen Charge

Date: September 7, 2026
Equation: classical, unforced, unaugmented three-dimensional incompressible Navier–Stokes on \(\mathbb T^3\)
Status: exact finite-Galerkin algebra and falsification results; no unconditional regularity proof
Fixed endpoint: DA-NS-2, the Galerkin-uniform (\(L_t^1\)) bound for the positive centered drift

This file is the Sprint 01 source of truth. The 28 September
channel stamp in `docs/CANONICAL-CHANNEL-GAMMA.md` is
subordinate to the identities below. v2 is not run.
DA-NS-2 remains open. Navier–Stokes is not solved.

────────

## 1. Executive verdict

The exact full-flow phase algebra survives, but the dynamic
interpretation has changed materially.

> The one-channel real-coupling truncation has exact \((0/\pi)\)
> invariant rays. That signed channel is not invariant in the
> actual vector Galerkin systems: other helical directions
> become large. Nevertheless, the tracked raw interaction
> monomial remains real because the chosen data lie in an exact
> coplanar 2D3C half-turn fixed-point class. Positive orientation
> can end through a modal-amplitude zero or through a zero of
> the moving radial multiplier. This defeats unconditional
> automatic dephasing; it does not prove dangerous locking in a
> genuinely three-dimensional network.

The two-door lock/rotate dichotomy is therefore retired. The
admissible research partition is hierarchical:

1. capacity, radial or geometric degeneracy: the instantaneous
   channel contribution is zero or small, but repeated resets
   still require a cutoff-uniform time budget;
2. exact regular invariant geometry: the demonstrated persistent
   lock lies in a globally regular 2D3C sector; a merely
   near-planar field is not discharged for free;
3. nondegenerate rotation: control the raw angular current and
   its positive-time occupation without dividing by amplitudes;
4. nonrotating paid charge: sum the connected heterochiral
   network before taking positive parts and obtain a one-sided
   or bounded-total-variation charge estimate.

The full helical decomposition agrees with the undecomposed
Navier–Stokes centered drift through all tested channels. A
new frozen logarithmic charge identity also has exact
leading-order core and narrow-band viscous cancellations at
the signed endpoint \((\theta=1)\). It does not close the
required fixed-\((\theta<1)\) endpoint: the term

\[
(1-\theta)\nu\frac{\mathcal D_s}{Y}
\]

survives, and a bounded charge range does not control its
positive variation after amplitude-zero resets.

What has been closed in this sprint is the algebraic
representation, the invariant-symmetry lemma and several
fail-fast tests. DA-NS-2 remains open. There is no claim
here that Navier–Stokes or the Riemann hypothesis has been
solved.

────────

## 2. The unchanged closure endpoint

Let

\[
X=\lvert A^{1/2}u\rvert_2^2,\qquad
Y=\lvert Au\rvert_2^2,\qquad
Z=\lvert A^{3/2}u\rvert_2^2,\qquad
\Lambda=\frac YX,
\]

\[
\mathfrak T_c=\mathcal M-\Lambda\mathcal N,
\qquad
\mathcal D_s=Z-\Lambda Y\ge 0.
\]

The exact barycenter identity is

\[
(\log\Lambda)'=\frac{2}{Y}
\bigl(\mathfrak T_c-\nu\mathcal D_s\bigr).
\]

For \(0\le\theta<1\), define

\[
K_{\min,\theta}^{(n)}
=
\frac{\bigl[\mathfrak T_c^{(n)}-\theta\nu\mathcal D_s^{(n)}\bigr]_+}
{Y^{(n)}}.
\]

The remaining proof obligation is still

\[
\boxed{
\sup_n\int_0^T K_{\min,\theta}^{(n)}(t)\,dt
\le F(\nu,T,u_0)<\infty
}
\tag{DA-NS-2}
\]

without assuming a continuation norm. Phase variables are
useful only if they prove this bound rather than rename it.

────────

## 3. Exact phase-resolved helical network

For each nonzero Fourier mode choose helical vectors

\[
i k\times h_s(k)=s\lvert k\rvert h_s(k),\qquad s\in\{-1,+1\},
\]

and write

\[
\widehat u_k=\sum_{s=\pm}a_k^s h_s(k).
\]

Take a real geometric triad \(\Delta=(k,p,q)\) with
\(k+p+q=0\), radii

\[
x=\lvert k\rvert,\qquad y=\lvert p\rvert,\qquad z=\lvert q\rvert,
\]

and helicity signs \(\sigma=(s_k,s_p,s_q)\). Set the signed
curl eigenvalues

\[
a=s_k x,\qquad b=s_p y,\qquad c=s_q z.
\]

For the three representative-mode energy transfers,

\[
(\tau_k,\tau_p,\tau_q)
=\Theta_{\Delta,\sigma}(b-c,c-a,a-b),
\]

where, in the tested basis convention,

\[
\Theta_{\Delta,\sigma}
=\operatorname{Re}\!\left(
g_{\Delta,\sigma}\,
\overline{a_k^{s_k}a_p^{s_p}a_q^{s_q}}
\right).
\]

The conjugation is essential. It follows from the real-field
interaction of \((-p,-q)\) in the \(k\) equation together with
the conjugation in the energy pairing. Dropping it can make
aggregate sums look plausible while assigning the wrong phase
to individual channels.

With \(w(r)=r^2(r^2-\Lambda)\), the real six-mode channel
contribution is

\[
\mathfrak T_{c,\Delta,\sigma}
=2C_{\Delta,\sigma}(\Lambda)\Theta_{\Delta,\sigma},
\]

where

\[
C_{\Delta,\sigma}
=-(a-b)(b-c)(c-a)
\left(a^2+b^2+c^2+ab+bc+ca-\Lambda\right).
\]

Separate the gauge-invariant raw interaction monomial from
the real moving radial multiplier:

\[
W_{\Delta,\sigma}
=g_{\Delta,\sigma}
\overline{a_k^{s_k}a_p^{s_p}a_q^{s_q}},
\]

\[
\psi_{\Delta,\sigma}=\arg W_{\Delta,\sigma},
\qquad
\mathfrak T_{c,\Delta,\sigma}
=2C_{\Delta,\sigma}\lvert W_{\Delta,\sigma}\rvert\cos\psi_{\Delta,\sigma}.
\]

For instantaneous reconstruction only, define the
upward-oriented monomial

\[
\mathcal Z_{\Delta,\sigma}=C_{\Delta,\sigma}W_{\Delta,\sigma},
\]

the effective channel capacity

\[
\mathcal A_{\Delta,\sigma}=2\lvert\mathcal Z_{\Delta,\sigma}\rvert,
\]

and its upward phase angle

\[
\Psi_{\Delta,\sigma}=\arg\mathcal Z_{\Delta,\sigma}.
\]

Then the exact full-network formula is

\[
\boxed{
\mathfrak T_c
=\sum_{\Delta,\sigma}
\mathcal A_{\Delta,\sigma}\cos\Psi_{\Delta,\sigma}.
}
\tag{3.1}
\]

This is the corrected mathematical meaning of dangerous phase
coherence. At a snapshot, 100% upward coherence means every
active, capacity-weighted channel has \(\cos\Psi=1\). For
dynamics, however, \(\psi=\arg W\) must be tracked separately:
a sign change of the real factor \(C(\Lambda)\) reverses
\(\Psi\) without rotating the raw interaction phase. A scalar
shell profile cannot see either distinction.

### Reconstruction tests

| Field | Signed channels | Direct \(\mathfrak T_c\) | Phase sum | Reconstruction error | Signed network alignment \(\mathfrak T_c/\sum\mathcal A\) |
|---|---:|---:|---:|---:|---:|
| Exhibit B | 8 | 4.0000000 | 4.0000000 | \(9.8\times 10^{-15}\) | 0.06763 |
| Exhibit C | 8 | 0.3976285 | 0.3976285 | \(5.6\times 10^{-17}\) | 0.50000 |
| Random full cube, radius 1 | 176 | 50.1274496 | 50.1274496 | \(8.5\times 10^{-14}\) | 0.13667 |
| Random full cube, radius 2 | 4,272 | 6,757.65113 | 6,757.65113 | \(7.3\times 10^{-12}\) | 0.03452 |

The largest individual-channel factorization residual was
approximately \(2.1\times 10^{-12}\) in the 4,272-channel test.
These computations certify the implementation of the finite
algebra; they do not establish a cutoff-uniform analytic bound.

────────

## 4. Projected locked rays versus the exact vector symmetry lock

### 4.1 What the one-channel model proves

If one further projects a single geometric triad onto one
selected helicity-sign channel, its three complex amplitudes
can be gauged into

\[
\dot a_i+\nu k_i^2 a_i
=\alpha_i\overline{a_j a_\ell},
\qquad
(\alpha_1,\alpha_2,\alpha_3)
=\gamma(b-c,c-a,a-b),
\]

with real \(\gamma\). Away from amplitude zeros, if
\(a_j=r_j e^{i\phi_j}\) and \(\Phi\) includes the fixed
interaction-coefficient phase, then

\[
\dot\Phi
=-\sin\Phi\left(
\alpha_1\frac{r_2 r_3}{r_1}
+\alpha_2\frac{r_3 r_1}{r_2}
+\alpha_3\frac{r_1 r_2}{r_3}
\right).
\]

Thus \(0\) and \(\pi\) are invariant rays of this
channel-decimated ODE, and viscosity contributes no direct
rotation. This is not an invariant single-helicity subsystem
of the actual vector Navier–Stokes Galerkin equation. In the
dynamic tests, the initial vector field already points
87–93% outside the tracked signed-helicity subspace, and the
later combined leakage reaches 79–98%. The older phrase
“true isolated NS triad” is therefore withdrawn.

### 4.2 Exact symmetry lemma for the actual vector equation

For the tested seed, let

\[
n=\frac{(0,1,-1)}{\sqrt{2}},
\qquad
P=n^\perp=\{k:k_y=k_z\},
\]

and let the half-turn about \(n\) be

\[
R=2nn^\top-I
=\begin{pmatrix}
-1&0&0\\
0&0&-1\\
0&-1&0
\end{pmatrix}.
\]

Define the real linear fixed-point space

\[
\mathcal S
=\left\{u:
\operatorname{supp}\widehat u\subset P,
\quad
\widehat u_k=R\overline{\widehat u_k}
\right\}.
\tag{4.1}
\]

This space is invariant for the full Navier–Stokes equation
and for every tested symmetric Galerkin cube. The plane is
convolution-closed, \(P+P\subset P\). Navier–Stokes, Leray
projection and viscosity are equivariant under the physical
rotation \(u(x)\mapsto Ru(Rx)\). On \(P\), \(Rk=-k\), so
reality converts the fixed-point condition into (4.1).

Equivalently, these are 2D3C fields \(u=v+\vartheta n\),
\(\partial_n u=0\), with two-dimensional incompressible
\(v\), a passive scalar \(\vartheta\) and the additional
half-turn parity. In the common planar helical gauge,

\[
h_s(k)=\frac{n\times\widehat k+i s n}{\sqrt{2}},
\]

the symmetry makes every helical amplitude purely imaginary
while every planar Waleffe triple product is purely
imaginary. Hence

\[
W_{\Delta,\sigma}
=g_{\Delta,\sigma}\overline{a_1 a_2 a_3}
\in\mathbb R
\]

for every active planar channel. The raw generalized phase
is therefore pinned to the union of the \(0\) and \(\pi\)
rays away from zeros. This is an exact symmetry proof, not
a numerical inference. It is also a separately regular 2D3C
sector, not a dangerous genuinely three-dimensional locked
example.

### 4.3 Dynamic diagnostics and two different sign changes

The seed uses

\[
k=(1,0,0),\quad p=(0,1,1),\quad q=(-1,-1,-1),
\qquad\sigma=(+,+,-).
\]

All maxima below are over the sampled output times; roots
were then numerically resolved using dense solver output.

| Evolution | Horizon | Max distance of raw phase from \((0/\pi)\) | Sign-change mechanism | Max energy outside original six modes | Max combined departure from tracked signed channel | Max off-plane energy |
|---|---:|---:|---|---:|---:|---:|
| Six-mode vector Galerkin projection | 2 | \(2.59\times 10^{-14}\) | 2 modal-product zeros | 0 | 97.95% | 0 |
| Complete radius-one cube | 2 | \(1.05\times 10^{-13}\) | 1 modal-product zero | 39.40% | 91.17% | 0 |
| Complete radius-two cube | 1 | \(1.41\times 10^{-15}\) | 1 radial zero (\(C(\Lambda)=0\)) | 31.48% | 78.61% | 0 |
| One random radius-one cube | 0.5 | 0.485 | no tracked zero | n/a | 94.12% | 75.95% |

For radius one, the raw monomial crosses zero because one
tracked modal amplitude vanishes while
\(\lvert C(\Lambda)\rvert\approx 1.915\). Its displayed
argument switches between \(0\) and \(\pi\), but the
argument is undefined at the zero; this is not angular
transport. For radius two, the raw phase does not change,
while the oriented centered contribution reverses because
\(C(\Lambda)\) itself crosses zero. The two events must
never be conflated.

### 4.4 Transverse rank-three stress test

A second triad was added in a different plane from the seed
triad, sharing one mode and initially placed on a compatible
real phase ray. Each triad is planar, but their union spans
\(\mathbb R^3\). The tracked original channel then showed:

| Transverse amplitude \(\varepsilon\) | Max raw argument change | Max sampled raw phase rate | Max off-plane energy |
|---:|---:|---:|---:|
| 0.1 | 0.0051095 | 0.0388317 | 1.7606% |
| 0.3 | 0.0473405 | 0.339127 | 14.1484% |
| 1.0 | 2.19028 | 17.1870 | 59.2682% |

This is finite-time, finite-Galerkin numerical evidence that
rank-three coupling can generate rotation. The first two
sampled rates are approximately proportional to
\(\varepsilon^2\); that scaling is empirical, not a theorem.
By finite-dimensional continuous dependence, the exact lock
is a degeneracy boundary: no all-data phase-escape constant
can be uniform without an explicit transversality or
distance-from-symmetry parameter.

────────

## 5. The phase-twin obstruction

For the same \((++-)\) triad, changing one amplitude by a
phase of \(\pi\) gives two fields with identical

\[
X,\; Y,\; Z,\; \Lambda,\; \mathcal D_s,
\quad\text{and}\quad \lvert\nabla u\rvert_3,
\]

but opposite centered drift:

\[
\mathfrak T_c(u)=-0.79707557316,
\qquad
\mathfrak T_c(\widetilde u)=+0.79707557316.
\]

This proves that intensities and quadratic spectral moments
alone cannot determine the dangerous sign. Any successful
estimate must retain phase, genuine interaction geometry,
time evolution, or an equivalent signed quantity.

────────

## 6. Why the Q1 memory was relevant—and what it cannot prove

The earlier Q1 work introduced an adaptive coherence-viscosity
term of the form

\[
Q_1[u]
=-\varepsilon^\alpha\lvert\nabla u\rvert^\beta\Delta u
\]

or a later scale-selective version concentrated near the
parabolic annulus. For fixed augmentation strength, the
revised calculation supplied a genuine one-derivative
high-frequency barrier: its damping scaled one dyadic
derivative above the commutator it opposed.

That is why the remembered language about preventing
coherence from reaching 100% was conceptually connected to
the present phase lock. Q1 imposed an external penalty on a
locked high-gradient transfer state.

The boundary is equally important:

- Q1 changes the Navier–Stokes equation;
- the proved spectral threshold worsens as the augmentation
  is removed;
- no uniform \((\varepsilon\to 0)\) de-augmentation theorem
  was established;
- the earlier claim that fixed-Q1 regularity automatically
  closed classical NS was withdrawn.

The current task is to determine whether the unaugmented
overlapping triad network supplies an endogenous replacement.
That has not yet been proved.

────────

## 7. Exact phase-to-charge bridge

The strongest new structural fact concerns heterochiral
channels. Let \((i,j)\) be the radii of the two equal-helicity
modes and \((o)\) the radius of the odd-helicity mode. Set

\[
H_{ij\lvert o}=i^2+j^2+o^2+ij-o(i+j).
\]

For that real six-mode channel,

\[
\boxed{
\mathfrak T_{c,\Delta}^{\mathrm{het}}
=R_\Lambda(i,j;o)\,Q_{\mathrm{abs},\Delta}
}
\tag{7.1}
\]

with

\[
R_\Lambda(i,j;o)
=\frac{(i+o)(j+o)(H_{ij\lvert o}-\Lambda)}{2o},
\]

and

\[
Q_{\mathrm{abs},\Delta}
=\sum_{m\in\Delta,\,\pm}\lvert m\rvert\,\tau_m.
\]

This is the nonlinear production of the positive quantity

\[
H_{\mathrm{abs}}
=\sum_{k,s}\lvert k\rvert\,\lvert a_k^s\rvert^2,
\]

not the conserved signed physical helicity. Homochiral triads
satisfy

\[
Q_{\mathrm{abs},\Delta}=0,
\]

while their centered coefficient carries the full radial
Vandermonde factor

\[
(x-y)(y-z)(z-x).
\]

Near a comparable barycentric core \((i,j,o\approx\kappa=\sqrt\Lambda)\),

\[
R_\Lambda(i,j;o)=2\kappa^3+O(\kappa^2\delta),
\]

where \(\delta\) is the radial width. Hence the dominant
locked heterochiral contribution is approximately
\(2\kappa^3 Q_{\mathrm{abs}}\), and the multiplier remainder
gains a radial-gap factor.

The exact full-flow enumeration verified simultaneously that

- the sum of all homochiral and heterochiral centered
  contributions equals \(\mathfrak T_c\);
- every heterochiral channel satisfies (7.1);
- homochiral absolute-helicity production cancels;
- signed physical-helicity production cancels across every
  channel.

This is why “phase” alone is now refined to phase plus charge.

On a real six-mode channel, \(Q_3=2o\tau_o\) is the
three-mode reduction and \(Q_{\mathrm{abs}}=2Q_3\). Do not
rename \(Q_3\) as \(Q_{\mathrm{abs}}\).

────────

## 8. Moving and frozen charge budgets: exact gains and exact poisons

Globally define

\[
H_a=\sum_{k,s}\lvert k\rvert\lvert a_k^s\rvert^2,
\qquad
D_a=\sum_{k,s}\lvert k\rvert^3\lvert a_k^s\rvert^2,
\qquad
\tfrac12 H_a'+\nu D_a=Q_a.
\]

### 8.1 Why the moving normalization does not close

Let

\[
\kappa=\sqrt\Lambda,
\qquad
\Phi=\frac{\kappa H_a}{X},
\qquad
\rho=\mathfrak T_c-2\kappa^3 Q_a,
\qquad
S=\frac{\mathfrak T_c-\nu\mathcal D_s}{Y}.
\]

Direct differentiation gives

\[
\boxed{
(1+\Phi)S
=\Phi'
+\frac{2\Phi\mathcal N}{X}
+\frac{2\nu\kappa}{X}(D_a-\kappa^2 H_a)
+\frac{\rho}{Y}
-\frac{\nu\mathcal D_s}{Y}.
}
\tag{8.1}
\]

This was reconstructed on the 176- and 4,272-channel networks
with residuals of approximately \(1.6\times 10^{-17}\) and
\(1.2\times 10^{-14}\). But \(\Phi\ge 1\) globally, and at
the exact comparable barycentric core
\(\mathcal N/X=\mathfrak T_c/Y\) to leading order. Moving
the apparent normalization term to the left therefore
changes a coefficient proportional to \((1+\Phi)\) into
\((1-\Phi\le 0)\). The moving normalization cancels the
hoped-for gain rather than producing coercivity.

### 8.2 The stronger frozen logarithmic charge

Freeze a positive epoch scale \(\kappa_e\) and define

\[
\boxed{
\mathcal C_e=\log\frac{X}{\kappa_e H_a}.
}
\]

Then exactly

\[
\mathcal C_e'
=\frac{2\mathcal N}{X}
-\frac{2Q_a}{H_a}
+2\nu\left(\frac{D_a}{H_a}-\Lambda\right).
\tag{8.2}
\]

For

\[
G_\theta=\frac{\mathfrak T_c-\theta\nu\mathcal D_s}{Y},
\]

one obtains

\[
\boxed{
G_\theta
=\mathcal C_e'
+\mathcal R_{\mathrm{lock}}
+\nu\mathcal R_{\nu,\theta},
}
\tag{8.3}
\]

where

\[
\mathcal R_{\mathrm{lock}}
=\frac{\mathfrak T_c}{Y}
-\frac{2\mathcal N}{X}
+\frac{2Q_a}{H_a},
\]

\[
\mathcal R_{\nu,\theta}
=2\left(\Lambda-\frac{D_a}{H_a}\right)
-\theta\frac{\mathcal D_s}{Y}.
\]

On a spectrum supported in radii \([a,b]\), \(\mathcal C_e\)
has bounded range,

\[
\log\frac a{\kappa_e}
\le \mathcal C_e\le
\log\frac b{\kappa_e}.
\]

At the exact comparable heterochiral core, the leading part
of \(\mathcal R_{\mathrm{lock}}\) cancels. There is also an
exact narrow-band viscous estimate at \(\theta=1\):

\[
\boxed{
\lvert\mathcal R_{\nu,1}\rvert
\le
\left[\left(\frac ba\right)^3-1\right]
\frac{\mathcal D_s}{Y}.
}
\tag{8.4}
\]

The new test independently verified (8.2)–(8.3) on vector
Galerkin fields to approximately \(10^{-14}\), verified
(8.4) on 10,000 random positive spectra and recovered the
expected narrow-band smallness.

### 8.3 The fixed-\(\theta\) strike

The required endpoint fixes \(\theta<1\), but

\[
\boxed{
\mathcal R_{\nu,\theta}
=\mathcal R_{\nu,1}
+(1-\theta)\frac{\mathcal D_s}{Y}.
}
\tag{8.5}
\]

The surviving positive variance term is not controlled by
the Leray energy budget. A nearly equilateral integer triad
with radii differing by only \(4.86\times 10^{-4}\) gives an
explicit fail-fast example: for every tested \(\theta<1\),
including 0.99 and 0.999, \(G_\theta>0\) while
\(\mathcal C_e'<0\). Thus positive DA occupation can occur
while the proposed charge decreases.

There is a second independent obstruction. A locked raw
phase can cross an amplitude zero and reappear on the
opposite real ray. A bounded range for \(\mathcal C_e\)
controls net change, not

\[
\int[\mathcal C_e']_+\,dt
\]

or total variation. Negative episodes can reset the charge
and allow repeated positive episodes. Consequently, the
frozen charge is a useful signed \((\theta=1)\) narrow-band
identity, but its standalone route to DA-NS-2 is rejected.
Any rescue needs a second admitted budget for the positive
variance term and a cutoff-uniform reset/total-variation
estimate, with localization, cross-band and epoch-return
costs shown explicitly.

────────

## 9. Corrected phase dynamics: use the raw monomial

The dynamic variable is

\[
W_{\Delta,\sigma}
=g_{\Delta,\sigma}\overline{a_k a_p a_q},
\]

not the oriented product \(\mathcal Z=C(\Lambda)W\). Define
the nonsingular raw angular current

\[
\boxed{
\mathcal J^W_{\Delta,\sigma}
=\operatorname{Im}\bigl(
\overline{W_{\Delta,\sigma}}\,\dot W_{\Delta,\sigma}
\bigr).
}
\tag{9.1}
\]

When \(W\neq 0\),

\[
\dot\psi=\frac{\mathcal J^W}{\lvert W\rvert^2}.
\]

At \(W=0\), \(\arg W\) and \(\dot\psi\) are undefined, while
\(\mathcal J^W=0\) algebraically. That zero value alone does
not prove tangency or a passage direction; the full vector
field or an invariant-symmetry lemma must do so. A radial
zero (\(C(\Lambda)=0\)) is different: \(W\) can remain
nonzero and phase-locked while the centered orientation
reverses.

Viscosity contributes only a real decay factor to \(W\) and
therefore no direct angular rotation. Nonlinear interaction
generates rotation. Overlap is needed to kick the particular
locked symmetry trajectory tested here, but an off-lock
channel-decimated ODE can also rotate; no universal
“overlap-only” statement is made.

### 9.1 The centered icosahedron: exact centered geometry, but not a closed flow

The remembered centered icosahedron is mathematically exact
at the geometric level. With \(\phi=(1+\sqrt5)/2\), take

\[
\mathcal I=\{(0,\pm 1,\pm\phi),(\pm 1,\pm\phi,0),(\pm\phi,0,\pm 1)\},
\]

with independent signs. Its twelve vertices obey

\[
\sum_{v\in\mathcal I}v=0,\qquad
\lvert v\rvert^2=R^2=2+\phi,\qquad
\sum_{v\in\mathcal I}v\otimes v=4R^2 I_3.
\tag{9.2}
\]

Thus the origin, common radius and unweighted isotropic
second moment are invariant under the icosahedral rotation
group. Equal orbit weights inherit this isotropy; arbitrary
Fourier amplitudes do not.

There is also an exact barycenter consequence for every
nonzero field supported on one Fourier eigenshell
(\(\lvert k\rvert^2=K\)), whether or not its angular geometry
is icosahedral:

\[
\Lambda(0)=K,\qquad
\mathcal D_s(0)=\mathfrak T_c(0)=0,\qquad
\Lambda'(0)=0.
\tag{9.3}
\]

This is the legitimate “invariant at the center”: all active
radial weights \(\lvert k\rvert^2(\lvert k\rvert^2-\Lambda)\)
vanish at that instant. It is not yet dynamical invariance.
For distinct nonantipodal vertices of the regular icosahedron,

\[
\lvert v+w\rvert^2\in\{4,\,4+4\phi\},
\]

so every nonzero distinct-vertex pair sum leaves the original
radius \(2+\phi\); self-pair output \(2v\) also leaves it and
its incompressible self-interaction vanishes. There are no
retained three-vertex triads. Moreover, exact fivefold
icosahedral rotations cannot preserve a rank-three reciprocal
lattice. Hence the literal golden-ratio vertex set is not a
Fourier orbit on \(\mathbb T^3\), and projecting back to its
twelve vertices merely deletes the nonlinear output.

The torus-compatible exact stress test is the rational
one-shell family

\[
S_{a,b}
=\{(0,\pm b,\pm a),(\pm b,\pm a,0),(\pm a,0,\pm b)\},
\qquad 1<\frac ab<\sqrt3.
\tag{9.4}
\]

Let \(u_0\) be real and divergence free on \(\lvert k\rvert^2=K\),
let \(B_0=P_N B(u_0,u_0)\), and let the Galerkin cutoff contain
all outputs in \(S+S\). Direct differentiation gives the
general one-shell Taylor identities

\[
\mathfrak T_c'(0)
=\sum_q \lvert q\rvert^2(\lvert q\rvert^2-K)\lvert\widehat B_0(q)\rvert^2,
\tag{9.5}
\]

\[
\tfrac12\mathcal D_s''(0)
=\sum_q \lvert q\rvert^2(\lvert q\rvert^2-K)^2\lvert\widehat B_0(q)\rvert^2,
\qquad
\Lambda''(0)=\frac{2\mathfrak T_c'(0)}{X(0)}.
\tag{9.6}
\]

For (9.4), every nonzero active quadratic output is outward.
Therefore \(B_0\neq 0\) implies \(\mathfrak T_c'(0)>0\) and
\(\mathcal D_s''(0)>0\). In particular,

\[
\mathfrak T_c(t)=c_T t+O(t^2),\qquad
\mathcal D_s(t)=c_D t^2+O(t^3),
\qquad c_T,c_D>0.
\tag{9.7}
\]

For every fixed \(\theta<1\), this makes
\(\mathfrak T_c-\theta\nu\mathcal D_s>0\) for all
sufficiently small positive time. The exact integer example
\((a,b)=(3,2)\) numerically corroborates the analytic
coefficients at the stated finite-difference tolerances.
This is a clean static-core-to-breathing-halo reset test and
a strike against pointwise absorption; it is not a long-time
monotonicity theorem or a new closure branch.

────────

## 10. Sprint 02: the reset-safe geometry–phase–capacity–charge gate

On a connected dyadic epoch with a fixed barycentric
projector, route each dangerous comparable heterochiral
component through the following hierarchy.

**Door 1: capacity, radial or geometric degeneracy.**
If a modal product, the geometry coefficient or
\(C_\gamma(\Lambda)\) is zero, then that channel contributes
no centered drift at that instant. Near-zero effective
capacity may be useful only after proving a cutoff-uniform
estimate for the summed network contribution. A numerical
root count, channelwise smallness or an \(O(1)\) fee per
reset is inadmissible.

**Door 2: exact regular invariant geometry.**
Exact 2D or 2D3C invariant sectors may be discharged by
their independent regularity theory. Near-planar data are
not automatically in this door. The transverse experiment
shows that the rotation constant degenerates continuously
toward the exact symmetry class; a near-geometry branch
needs its own quantitative stability estimate.

**Door 3: nondegenerate rotation.**
On the remaining noncollapsed set, define

\[
\mathcal R_e(t)
=\bigl\{\gamma:
\lvert\mathcal J^W_\gamma\rvert
>
\eta\nu\kappa_e^2\lvert W_\gamma\rvert^2
\bigr\}.
\]

Use \(\mathcal J^W_\gamma\), without dividing at zeros, to
prove a cutoff-uniform positive-occupation or
integration-by-parts estimate for the aggregate centered
contribution. The proof must retain amplitude variation,
phase-speed reversals, moving \(\Lambda\), boundary terms
and the degeneration of transversality. Random-phase,
genericity and monotone-phase assumptions are inadmissible.

**Door 4: nonrotating joint gap–charge payment.**
On the slow-current complement, Sprint 01 posed the
following algebraic obligation. Sprint 02 subsequently
falsified its charge-only form and identified the explicit
multiplier covariance that must remain; see Section 15.

**Reset-Safe Full-Network Charge-Coercivity Lemma.**
Let \(\Gamma\) be a connected component of fully symmetrized,
comparable heterochiral channels and set

\[
\mathfrak T_{c,\Gamma}
=\sum_{\gamma\in\Gamma}R_{\Lambda,\gamma}Q_{a,\gamma},
\qquad
Q_{a,\Gamma}=\sum_{\gamma\in\Gamma}Q_{a,\gamma}.
\]

Outside the collapse and exact-regularity doors, and under a
stated slow-current threshold, prove

\[
\boxed{
[\mathfrak T_{c,\Gamma}]_+
\le C\kappa^3[Q_{a,\Gamma}]_+
+\mathcal R_{\Gamma}^{\mathrm{gap}}
+\mathcal F_{\Gamma}^{\mathrm{cross}}.
}
\tag{10.1}
\]

The component must be summed before taking the positive
part. Replacing net charge by \(\sum_\gamma[Q_{a,\gamma}]_+\)
destroys the absolute-helicity balance. The gap remainder
must display an additional radial-difference factor; the
cross-band term must pair with the neighboring band before
absolute values; constants must be cutoff-independent; and
the identity must glue across modal and radial zeros without
a reset charge. A finite connected network with
\(\mathfrak T_{c,\Gamma}>0\), \(Q_{a,\Gamma}\le 0\) and no
rotation, collapse, regular geometry or sufficient remainder
rejects (10.1).

Even success of (10.1) would not finish DA-NS-2. One would
still need reset/epoch summability and a remedy for the
fixed-(\(\theta<1\)) variance term in (8.5). The final proof
must allocate the single available \(\theta\nu\mathcal D_s\)
across aggregate sectors once; it cannot reuse the same
dissipation channel by channel. Any final line requiring
\(\int(\mathcal N/X)_+\,dt\), \(\int\mathcal D_s/Y\,dt\),
\(\sup\Lambda\), or a Serrin/BKM continuation quantity is
out.

This gate is a research specification, not a theorem already
obtained.

────────

## 11. Dream Team lane verdicts

| Lane | Result | Status |
|---|---|---|
| Scalar cumulative energy flux | Exact identity, but its natural centered tail-energy potential is identically zero and differentiation returns the barycenter equation | Rejected as a standalone mechanism |
| Helical signed-curl factorization | Exact for all eight sign channels | Certified algebra |
| Full overlapping flow | Direct and triad/helicity sums agree through 4,272 channels | Certified finite implementation |
| One-channel locked-ray ODE | Exact \((0/\pi)\) rays after a further helical-channel projection | Certified only for the projected model; not invariant vector NS |
| Coplanar half-turn fixed space | Exact NS/Galerkin invariant 2D3C sector; every raw channel monomial is real | Certified symmetry lemma; separately regular geometry |
| Universal automatic dephasing | Incompatible with the exact symmetry-locked sector | Rejected if unconditional |
| Genuinely 3D phase rotation | A transverse rank-three perturbation produces rotation that weakens toward the symmetry plane | Numerical evidence; no uniform theorem |
| Modal/radial zeros | Radius one exits through a modal zero; radius two reverses through \(C(\Lambda)=0\) | Numerically resolved; not a time budget |
| Heterochiral phase-to-charge bridge | \(\mathfrak T_c=R_\Lambda Q_{\mathrm{abs}}\) channel by channel | Certified algebra |
| Moving normalized absolute-helicity budget | Exact, but its leading normalization cancels the target at the comparable core | Rejected standalone |
| Frozen logarithmic charge | Exact core and \((\theta=1)\) narrow-band viscous cancellations | Certified identity; fixed-\((\theta<1)\) route rejected standalone |
| Endpoint \((q=3)\) commutator | Scaling-compatible finite tests; standard proof leaves a centered commutator and, even if resolved, a known critical continuation integral | Conditional lane only |
| Centered icosahedral core | Exact zero center, common radius and isotropic second moment; one-shell centered drift and variance vanish instantaneously | Certified geometry; not a torus Fourier orbit or invariant NS subsystem |
| Rational icosahedral shell | Exact integer one-shell seed generates a strictly outward active halo and satisfies the one-shell Taylor identities | Certified reset stress test; no long-time estimate |
| Reset-safe four-way gate | Collapse, exact regular geometry, raw rotation, or net paid charge | Recommended falsification architecture; all uniform estimates open |
| Reset-safe net-charge coercivity (10.1) | A connected slow-current component can hide charge cancellation | Charge-only form rejected in Sprint 02; explicit covariance retained |

────────

## 12. Literature and novelty guard

The helical basis and triad stability framework are classical;
see Waleffe, *The nature of triad interactions in homogeneous
turbulence*. Kang, Protas and Bustamante give the exact
coefficient-corrected generalized helical phase and
capacity-times-cosine flux representation; their
three-dimensional phase-organization results are numerical
diagnostics, not a phase-escape theorem: arXiv:2105.09425.

The one-channel caution is substantive. Moffatt compares a
single-triad truncation with exact Euler evolution and shows
that the truncation has additional structure not shared by
the PDE: *A note on the triad interactions of homogeneous
turbulence*. The correct phrase here is therefore
“single-channel Galerkin truncation using the exact
coefficient,” never “isolated invariant full-NS triad.”

The 2D3C split into two-dimensional Navier–Stokes plus a
passive third component, and the fact that a superposition
of differently oriented triads need not remain 2D3C, are
discussed by Biferale, Buzzicotti and Linkmann: arXiv:1706.02371.
The same work shows why a one-sign helical sector is not
invariant without reprojection. Biferale and Titi’s global
regularity theorem applies to the explicitly helical-decimated
equation, not full Navier–Stokes: arXiv:1303.1215. Physical
screw/helical symmetry is a different notion from Waleffe
helicity sign; the invariant global regularity result of
Mahalov, Titi and Leibovich concerns that spatial symmetry:
DOI 10.1007/BF00381234.

The crystallographic restriction is decisive for the centered
icosahedron. Zappa, Dykeman and Twarock show that fivefold
symmetry is forbidden for three-dimensional lattices; their
standard crystallographic lift containing the physical
three-dimensional icosahedral representation and its
Galois-conjugate three-dimensional representation is
six-dimensional: *Acta Crystallographica* A 70 (2014).
Whole-space Navier–Stokes is rotationally equivariant, so an
icosahedral fixed-point class can persist over a solution’s
existing lifespan, but Brandolese explicitly does not obtain
unconditional large-data global existence from that symmetry:
arXiv:math/0304436. This matches the computation: an exact
geometric center does not give a finite invariant torus shell.

The conserved signed physical helicity controls the difference
of the two helical sectors, not the positive absolute-helicity
sum used in the charge attempt; see Lei, Lin and Zhou,
arXiv:1505.00142. Invariant-only arguments cannot suffice:
Tao’s averaged Navier–Stokes construction can preserve energy
and helicity while permitting finite-time blowup, so any
successful proof must use rigidity of the genuine symbol or
dynamics destroyed by averaging: arXiv:1402.0290.

There is a sharp 2026 prior-art collision. Inage’s
peer-reviewed April 2026 paper already uses a closely related
High–High coherent-core, low-phase-drift, curvature/coercivity
and residence-time-compression architecture, while explicitly
limiting its conclusion to the stated structural framework:
*Structural Reduction Framework and Residence-Time
Compression…*. Separate manuscripts claiming full
phase-nonpersistence closure remain unrefereed: March
preprint, April preprint. Consistently, the Clay Mathematics
Institute still lists Navier–Stokes as unsolved.

No novelty claim is made for helical decomposition, phase
variables, phase–flux cosine laws, 2D3C reduction, homochiral
decimation or absolute-helicity diagnostics. The potentially
distinctive combination, still requiring external expert
review and a broader novelty search, is the moving
centered-barycenter weight, the signed-curl Vandermonde
factorization, the exact heterochiral
centered-drift/absolute-helicity multiplier, the explicit
coplanar-plus-half-turn locked symmetry and the reset-safe
full-network gate.

────────

## 13. Reproducibility

The original Sprint 01 scripts (not vendored in this
repository) were:

```
python test_centered_flux_identity.py
python test_full_helical_flow.py
python test_helical_phase_network.py
python test_phase_rotation_dynamics.py
python test_frozen_log_charge.py
python test_icosahedral_core.py
```

The coefficient stamp in this repository certifies the
channel algebra of §§3 and 7 on the seed plus the locked
parallelogram:

```
python tests/test_channel_coefficient.py
python tests/test_full_flow.py
python scripts/run_channel_coefficient_identity.py
```

The phase-network script performs the 4,272-channel
reconstruction. The dynamic script integrates the six-mode
and complete-cube systems and may take roughly twenty
seconds. The frozen-charge script includes 10,000 positive
spectral tests and the nearly equilateral fixed-\(\theta\)
counterexample. The icosahedral script uses exact arithmetic
in \(\mathbb Q(\phi)\) for the abstract geometry and an exact
integer shell with a finite-difference Taylor check for the
torus-compatible stress test. All dynamical computations use
finite symmetric Fourier–Galerkin systems and fixed random
seeds.

v2 is not run from this lock.

────────

## 14. Court finding

The phase instinct was substantive. It identifies information
that \((X,Y,Z,\Lambda)\), spectral concentration and ordinary
norm estimates cannot see. The corrected full-flow analysis
also shows exactly why the older phase claim could not be
accepted: the projected signed-channel ODE was mistaken for
actual vector dynamics, the oriented radial sign was mixed
with raw phase and no deterministic cutoff-uniform
positive-occupation budget was proved.

The new result is sharper. An exact coplanar 2D3C half-turn
symmetry pins every raw channel monomial to the real rays
even while the selected signed-helicity subspace leaks
heavily. A transverse rank-three perturbation produces phase
motion, but the observed rate degenerates toward the
symmetry manifold. Meanwhile, modal and radial zeros permit
sign resets without angular rotation, and the strongest
frozen charge reaches only a signed \((\theta=1)\)
narrow-band cancellation before failing the fixed-\((\theta<1)\)
DA test.

The centered icosahedron now has an exact place in that map.
Its zero center and equal-radius isotropy are real, and every
nonzero one-shell field is instantaneously centered. But the
regular vertices are neither a \(\mathbb Z^3\) orbit nor
convolution closed. Their honest dynamical content is a
core-to-halo Taylor stress test: the center can be static at
one instant while the nonlinear flow immediately begins the
radial breathing that DA-NS-2 must budget.

The present frontier is therefore

\[
\boxed{
\text{collapse}
\text{ or }
\text{exact regular geometry}
\text{ or }
\text{raw phase rotation}
\text{ or }
\text{net paid charge}
\quad\Longrightarrow?\quad
\int_0^T K_{\min,\theta}^{(n)}\,dt\le F.
}
\]

The question mark is real. None of the four branches yet
supplies the required Galerkin-uniform positive-part
estimate. Sprint 02 decides (10.1): the charge-only form
fails, the explicit covariance split survives and the next
target is a Joint Gap–Charge Epoch Budget with reset
summability and fixed-\(\theta\) control.

────────

## 15. Sprint 02 disposition of the proposed net-charge lemma

The test proposed in (10.1) has now been decided at the
finite algebraic level.

For a connected heterochiral component,

\[
\mathfrak T_{c,\Gamma}^{\mathrm{het}}
=2\kappa^3 Q_{a,\Gamma}+\rho_\Gamma,
\qquad
\rho_\Gamma
=\sum_{\gamma\in\Gamma}
(R_{\Lambda,\gamma}-2\kappa^3)Q_{a,\gamma}.
\]

Thus

\[
[\mathfrak T_{c,\Gamma}^{\mathrm{het}}]_+
\le 2\kappa^3[Q_{a,\Gamma}]_++[\rho_\Gamma]_+.
\]

An exact-formula, rank-three, mixed-helicity two-triad
witness has \(Q_{a,\Gamma}=0\),
\(\mathfrak T_{c,\Gamma}^{\mathrm{het}}>0\) and zero raw
angular currents at the checkpoint. It proves that the
inequality without \(\rho_\Gamma\) is false. A second
rank-three witness has negative net charge, a negative
common multiplier and positive centered drift. The
gap/covariance term is therefore structurally necessary.

The surviving identity is quotient-free in modal amplitude
and phase and continuous through the tested amplitude and
centered-multiplier zeros for \(X>0\), but it is not an
analytic estimate until \([\rho_\Gamma]_+/Y\) has a
cutoff-uniform time budget. A conservative signed-helicity
cross-radius identity now gives exact cancellation before
positive parts and a frozen quadratic potential; barycenter
motion, opposite orientations, external edges and epoch
resets remain unpaid.

The next proof obligation is no longer (10.1) as originally
phrased. It is the Joint Gap–Charge Epoch Budget. It must
target the fixed \((\theta<1)\) endpoint directly, include
the moving-to-frozen scale correction, allocate dissipation
only once and bound every positive reset jump uniformly in
the Galerkin cutoff.

These results do not prove DA-NS-2 or global regularity.
