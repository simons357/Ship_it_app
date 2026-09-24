# Fourier triangles — exact mechanism, arithmetic restrictions, remaining time estimate

Reconstruction and audit — 20 September 2026
(implemented 24 September 2026).

**Identities, finite regressions, and one
open sufficient theorem.
Not a close. NS not solved.**

This page is the working reconstruction
of the September 20 notes (exact-sphere
weighted estimate, complete
repeated-radius contribution, fixed-low
complement, I3 prime branch). It does
**not** revert those developments to
older census-only summaries.

The loop-gauge / telescopic-capacity
board and the arithmetic
sign-realizability gate are **not
reopened**. Those pages stay frozen:

- [`LOOP-GAUGE-AND-TELESCOPIC-CAPACITY.md`](LOOP-GAUGE-AND-TELESCOPIC-CAPACITY.md)
- [`ARITHMETIC-SIGN-REALIZABILITY.md`](ARITHMETIC-SIGN-REALIZABILITY.md)

The older page
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md)
keeps the seated geometry. Its §7
reading of \(I_3\) as the unweighted
energy sum is **superseded here**:
\(I_3\) on this page is the cubic
lattice and the Gram/Hilbert test.

Code:

```bash
PYTHONPATH=scripts python3 -m unittest tests.test_fourier_triangle_audit -q
PYTHONPATH=scripts python3 scripts/ns_attacks/run_triangle_audit.py
```

`scripts/ns_attacks/fourier_triangle_geom.py`,
`i3_primes.py`, `triangle_examples.py`.
Report: `results/fourier_triangle_audit.json`.

No claim of global regularity,
singularity, or mathematical novelty.
Independent specialist review of the
research chain remains pending.

---

## Convention

Normalized torus
\((\mathbb{R}/2\pi\mathbb{Z})^3\),
characters \(e^{ik\cdot x}\), real
mean-zero divergence-free velocity,
viscosity \(\nu>0\).

\[
u(x,t)=\sum_{k\in\mathbb{Z}^3\setminus\{0\}}
u_k(t)\,e^{ik\cdot x},
\qquad
u_{-k}=\overline{u_k},
\qquad
k\cdot u_k=0.
\]

\(A=-P\Delta\) with symbol \(\lvert k\rvert^2\)
on divergence-free fields.
\(B(v,w)=P[(v\cdot\nabla)w]\).
Dot products with real wavevectors are
complex bilinear. Norms and real
\(L^2\) pairings use conjugation.

A shell label \(a\) means squared
radius \(\lvert k\rvert^2=a\), not
radius \(\lvert k\rvert=a\). An exact
shell and a thick dyadic annulus are
different sets.

---

## 1. Exact triangle geometry

For one interaction \(p+q=k\),

\[
a=\lvert p\rvert^2,\quad
b=\lvert q\rvert^2,\quad
c=\lvert k\rvert^2,\quad
s=p\cdot q=\frac{c-a-b}{2},\quad
\Delta=ab-s^2=\lvert p\times q\rvert^2.
\]

Included angle:
\(\cos\theta=s/\sqrt{ab}\), and

\[
(\sqrt{a}-\sqrt{b})^2\le c\le(\sqrt{a}+\sqrt{b})^2.
\]

Noncollinear frame: \(e_0=k/\sqrt{c}\),
\(e_1\) in the triangle plane
\(\perp k\), \(e_2=e_0\times e_1\).

\[
p=x e_0+h e_1,\qquad
q=y e_0-h e_1,
\]
\[
x=\frac{c+a-b}{2\sqrt{c}},\quad
y=\frac{c+b-a}{2\sqrt{c}},\quad
h=\sqrt{\Delta/c}.
\]

At fixed \(k,a,b\), admissible \(p\)
lie on a circle (sphere \(\cap\) plane).
The integer points on that circle are
the Fourier interactions. **The
geometric circle is not a fluid
trajectory.**

---

## 2. Polarization and identities (1)–(4)

The coefficient at \(p\) lies in the
two-dimensional complex plane
\(\perp p\):

\[
u_p
=
A_1\frac{h e_0-x e_1}{\sqrt{a}}
+A_2 e_2,
\qquad
u_q
=
B_1\frac{h e_0+y e_1}{\sqrt{b}}
+B_2 e_2.
\]

No common helicity or common phase is
assumed. Incompressibility gives

\[
q\cdot u_p=k\cdot u_p,
\qquad
p\cdot u_q=k\cdot u_q.
\]

Output projector
\(P_k=I-k\otimes k/\lvert k\rvert^2\)
is a contraction. It does **not**
supply a universal small factor on
every admissible interaction.

\[
S_{pq}
=
P_k\bigl[(q\cdot u_p)u_q+(p\cdot u_q)u_p\bigr].
\]

**EXACT (1).**

\[
\boxed{
S_{pq}
=
\frac{h(b-a)}{\sqrt{ab}}A_1 B_1\,e_1
+
\sqrt{c}\,h
\Bigl(
\frac{A_1 B_2}{\sqrt{a}}
+
\frac{A_2 B_1}{\sqrt{b}}
\Bigr)e_2.
}
\]

**EXACT (2).** Full ordered operator:

\[
\widehat B(u,u)(k)
=
i P_k\sum_{p+q=k}(q\cdot u_p)u_q
=
\frac{i}{2}\sum_{p+q=k}S_{pq}.
\]

The factor \(1/2\) belongs to the
ordered symmetrized sum. Dropping it
changes the constants.

**EXACT (3).** Equal lengths
\(a=b=\alpha\), \(c=\beta\):

\[
\boxed{
S_{pq}
=
\sqrt{\beta\bigl(1-\beta/(4\alpha)\bigr)}
\,(A_1 B_2+A_2 B_1)\,e_2.
}
\]

The in-plane transverse component
cancels. The normal component
generally remains. Purely in-plane
inputs kill that normal component as
well; general three-dimensional
inputs do not. At \(\beta=0\) or
\(\beta=4\alpha\) the collinear
interaction vanishes by divergence
freedom, without a degenerate frame.

**EXACT (4).** Unequal-length
coordinate-free defect:

\[
\boxed{
(P_k p)\cdot S_{pq}
=
\frac{b-a}{c}(k\cdot u_p)(k\cdot u_q).
}
\]

Proof: \(t=(p\cdot k)/c\),
\(\ell=P_k p\), then
\(\ell\cdot u_p=-t(k\cdot u_p)\),
\(\ell\cdot u_q=(1-t)(k\cdot u_q)\),
and \(1-2t=(b-a)/c\). This does
**not** estimate the normal component
or the sum over unequal radii.

Near-equal radii make the displayed
defect small relative to the frequency
scale. Thick comparable shells allow
\(b-a\) of the same order as \(a\)
and \(b\). Comparable size alone is
not this smallness.

Audit lock: identities (1) and (4)
on four mixed-polarization integer
triangles; identity (3) on
\(p=(2,1,0)\), \(q=(-1,2,0)\).
In-plane inputs kill the normal
component to machine precision.

---

## 3. Signed transfer and the phase twins

\[
\tau_k=-\operatorname{Re}\bigl[\widehat B(k)\cdot\overline{u_k}\bigr],
\qquad
\tfrac12\frac{d}{dt}\lvert u_k\rvert^2
+\nu\lvert k\rvert^2\lvert u_k\rvert^2
=\tau_k,
\qquad
\mathcal T(u)=\sum_k\lvert k\rvert^2\tau_k.
\tag{5}
\]

The paired contribution is
\(\operatorname{Im}(S_{pq}\cdot\overline{u_k})\);
the full ordered sum uses the
corresponding \(1/2\). Phase
dependence is
\(\operatorname{Im}\bigl[C_{pqk}e^{i(\phi_p+\phi_q-\phi_k)}\bigr]\).
\(C\) need not be real. A triangle
or a power spectrum alone does **not**
determine the sign. Replacing \(u\)
by \(-u\) preserves all quadratic
moments and reverses the cubic
transfers.

**EXACT finite example.**

\[
u=\bigl(2\cos 2y,\ 0,\ 2\cos 3x+f(3x+2y)\bigr).
\]

All three receiver choices have
\(E=6\), \(X=52\), \(Y=532\),
\(Z=5980\).

| \(f(\theta)\) | \(\mathcal T\) |
|---|---:|
| \(2\cos\theta\) | \(0\) |
| \(2\sin\theta\) | \(+24\) |
| \(-2\sin\theta\) | \(-24\) |

Recomputed here with the seated
ordered Im-sum, including both
Fourier signs and compensating
donors. Unweighted
\(\sum_k\tau_k=0\) in every case.

A complete triad has modal energy
transfers summing to zero. If all
three radii equal \(a\), enstrophy
weights are equal, so total
enstrophy transfer vanishes. The
two cancellations act at different
levels: a field supported on one
exact sphere can generate modes
**outside** that sphere even while
its initial enstrophy transfer
vanishes.

On the cosine (zero-transfer) field
the initially absent mode
\((3,-2,0)\) has
\(\widehat B=3i\,e_3\). A zero
instantaneous transfer or empty
receiving mode is not an inactive
interaction at later time.

---

## 4. Repeated-radius and scalene grouping

Radius multiset \(\{a,a,b\}\) with
\(b\neq a\):

\[
\tau_{b\leftarrow aa}
=-\operatorname{Re}\langle B(u_a,u_a),u_b\rangle,
\qquad
\boxed{
\mathcal T_{\{a,a,b\}}
=(b-a)\,\tau_{b\leftarrow aa}.
}
\tag{6}
\]

The equal-input portion is \(b\tau\);
the unequal-input portion is
\(-a\tau\). Calling all
unequal-input terms uncontrolled
discards a completed part of the
argument.

Three distinct squared radii
\(a<b<c\), \(p+q+r=0\):

\[
I_p
=\sum_{\substack{p+q+r=0\\ \lvert p\rvert^2=a,\,\lvert q\rvert^2=b,\,\lvert r\rvert^2=c}}
\operatorname{Im}\bigl[(q\cdot u_p)(u_q\cdot u_r)\bigr],
\]

and cyclic. **EXACT (7).**

\[
\boxed{
\mathcal T_{abc}
=(c-b)I_p+(a-c)I_q+(b-a)I_r.
}
\]

The negative triple is already in
the sum. No extra conjugation or
factor of two in this closed-triad
convention. Taking absolute values
before combining receivers loses
the radius-difference factors.

---

## 5. Exact-sphere weighted estimate

Nonnegative \(r_p\) on
\(\lvert p\rvert^2=\alpha\),
\(F=\sum r_p^2\),
\(L_k=\sum_{p+q=k}r_p r_q\).

**EXACT (8).**

\[
\sum_{\lvert k\rvert^2=\beta}L_k^2\le 3F^2
\qquad(\beta>0).
\]

Diagonal \(\le F^2\). Distinct
nonantipodal inputs: at most two
real \(k\) (sphere + two planes).
Antipodal is incompatible with
\(\beta>0\). Off-diagonal
\(\le 2F^2\). No bound on the
number of points in an individual
circle fiber is assumed.

Small audit check: \(\alpha=1\),
\(\beta=2\), \(r_p=1\) on the six
axis modes, \(F=6\),
\(\sum L_k^2\le 3F^2\) holds.

Equations (2), (3), (8) retain
\(1/4\), \(\beta(1-\beta/(4\alpha))\),
and \(3\). For \(Aw=\alpha w\),

**EXACT (9).**

\[
\lvert\Pi_\beta B(w,w)\rvert_2^2
\le
\frac34\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)
\lvert w\rvert_2^4.
\]

For \(r=\beta/\alpha\), the
normalized ratio is at most
\(16/9\):

\[
\frac{16}{9}-\frac34 r^2\bigl(1-r/4\bigr)
=
\frac{(3r+4)(3r-8)^2}{144}\ge 0.
\]

Upper bound. Attainment and
optimality of the operator constant
are **not** asserted.

Rational regression of the
polynomial identity on
\(r\in\{0,1/2,1,3/2,2,8/3,4\}\)
is exact (fractions, not floats).

**NUMERICAL / exact finite.**
\(w=(\sin y,\sin z,\sin x)\) gives
\(E=3/2\), squared output norm
\(3/4\) on \(\beta=2\), twelve
nonzero output coefficients,
normalized ratio

\[
\frac{\lvert A^{1/2}\Pi_2 B(w,w)\rvert_2^2}{\lvert w\rvert_2^4}
=\frac23.
\]

Reproduced exactly in this audit.

Summing output radii then input
radii retains

\[
\lvert A^{1/2}B_{\mathrm{equal}}(u,u)\rvert_2
\le 2\sqrt{XY}.
\tag{10}
\]

Regrouping all repeated-radius
receiver choices:

**EXACT (11).**

\[
\boxed{
\lvert\mathcal T_{\mathrm{rep}}(u)\rvert
\le
\frac{\sqrt3}{2}X\sqrt{Y}.
}
\]

One arithmetic fact already enters:
the output \(b\) of equal inputs
\(a\) is even, since
\(b=2a+2p\cdot q\). The exact sum
used after (6) is

\[
\sum_{\substack{2\le b\le 4a\\ b\ \mathrm{even}}}
(b-a)^2\Bigl(1-\frac{b}{4a}\Bigr)
=a^3-\frac{a^2}{2}.
\]

Locked by exact rationals for
\(a=1,2,3,5,8,13,21\). Weighted
Cauchy–Schwarz then uses
\(\sum a^{3/2}E_a\le\sqrt{XY}\).
Arithmetic is carried through the
correct weighted expression. It is
not an unweighted count substituted
into a different operator.

---

## 6. What is lost, and what is not

| Operation | What is lost, or remains to prove |
|---|---|
| Replace a complex coefficient by its magnitude | Relative phase and vector alignment disappear. |
| Bound each receiver orientation separately | Energy redistribution and radius-difference cancellation disappear. |
| Replace exact radii by a thick annulus | Exact equality, parity, and fixed-sphere incidence no longer give the same estimate. |
| Separate Cauchy–Schwarz at each output \(k\) | Shared inputs and simultaneous incidence must still be controlled when summing \(k\). |
| Count admissible integer triangles | Weights, signs, concentration, and sharing remain unspecified. |
| Estimate each fixed distinct-radius triple | The simultaneous sum over all such triples is still required. |
| Infer future behavior from one field | Generated modes, changing amplitudes, polarization, and nonlinear forcing remain unaccounted for. |
| Integrate a signed derivative inside a positive part | Bounded endpoints do not control repeated positive contributions or total variation. |

The older thick-shell obstruction
must **not** be confused with a
defect of the exact-sphere proof.
The source supplies an explicit
projected-convolution family with
\(Q_{i,i+1}\ge 2^{i/2}/2048\) for
the unrestricted \(\tau=1/2\)
low-high quotient, retaining the
original \(H^1\times H^2\)
denominator. That prevents
replacing that operator’s dense
assembly factor by a proposed
subpower incidence factor. It does
**not** refute a differently
restricted operator, and does not
produce an NS singularity. No
\(W_{ij}\) is reconstructed here.

---

## 7. I3: Gram realization and Hilbert symbols

\(I_3\) is the ordinary cubic
lattice \((\mathbb{Z}^3,x_1^2+x_2^2+x_3^2)\).
A triangle with prescribed \(a,b,c\)
exists iff the binary Gram

\[
G=\begin{pmatrix}a&s\\ s&b\end{pmatrix},
\qquad
s=(c-a-b)/2,
\]

has an integer realization
\(G=V^T V\) with \(V\) a \(3\times 2\)
integer matrix. **The test concerns
wavevectors, not velocity
coefficients.**

For \(a>0\), \(\Delta=ab-s^2>0\) and
integer \(a,b,s\), ordinary integral
representation by \(I_3\) is
equivalent to representation over
every \(\mathbb{Q}_\ell\) and every
\(\mathbb{Z}_\ell\). Finite criterion
(positive-definite real place already
granted):

**EXACT (12).**

\[
\boxed{
(a,\Delta)_\ell\,(a,-1)_\ell\,(\Delta,-1)_\ell=1
\quad\text{for every prime }\ell\mid 2a\Delta.
}
\]

\((\ ,\ )_\ell\) is the Hilbert
symbol. Primitive embeddings,
prescribed normals, degenerate Grams,
and class-group surjectivity are
separate questions.

The rational space to compare is
\(G^\perp\langle\Delta\rangle\),
whose determinant is a square. The
cited local classification supplies
the rational test. Local integrality
plus the one-class genus of \(I_3\)
gives the integral conclusion
(Schulze-Pillot, Cor. 5.29, Ex. 6.14,
Thm. 6.15, Cor. 6.16, Thm. 7.32).
This is classical quadratic-form
theory. It is **not** a conclusion
drawn from the census alone.

Odd-prime enlargement: after
diagonalizing as
\(\langle \ell^r u,\ \ell^t v\rangle\),
\(t\ge 2\) permits adjoining
\(e_2/\ell\). In the exceptional
\(r=t=1\) case, local compatibility
forces \(-v/u\) to be a square modulo
\(\ell\); adjoining
\((x e_1+e_2)/\ell\) then divides the
determinant by \(\ell^2\) while
preserving integrality. This modifies
an abstract lattice in its rational
plane. **It is not time evolution of
Fourier modes.**

**EXACT finite regressions**
recomputed here:

| Gram \((a,b,s)\) | Local result |
|---|---|
| \((96,96,0)\) | Fails at \(2\) and \(3\) |
| \((2,3,1)\) | Fails at \(2\) and \(5\) |
| \((2,2,-1)\) | Passes all required primes |
| \((14,14,-7)\) | Passes all required primes |

If \(a=b=c=\alpha\) then
\(s=-\alpha/2\), so **odd \(\alpha\)
cannot support a monochromatic closed
triangle**. Even \(\alpha\) is
necessary, not sufficient.

For an impossible triple the
contribution is identically zero at
every time. For an allowed triple the
prime tests impose **no** velocity
amplitude, polarization alignment, or
phase sign. A successful analytic use
must retain those weights when
counting and then control their
evolution. The fixed-sphere weighted
lemma and the even-output sum are
completed uses. A universal scalene
time estimate is **not**.

---

## 8. Actual motion

Along full Galerkin NS, **EXACT (13):**

\[
\dot u_k
=
-\nu\lvert k\rvert^2 u_k
-i P_k\sum_{p+q=k}(q\cdot u_p)u_q,
\qquad
\lvert k\rvert\le N.
\]

The vectors \(p,q,k\) and their
arithmetic restrictions remain
fixed. Coefficients change.
Initially zero coefficients can
become nonzero.

| Display element | Defensible interpretation |
|---|---|
| Fixed Fourier triangle | The actual additive relation between modes |
| Changing line thickness or brightness | An explicitly chosen amplitude, energy, or transfer diagnostic |
| A phase dial or polarization arrow | A coefficient coordinate, using a stated convention |
| Arrows between shells | Signed transfer after the complete required grouping |
| Triangle translating or rotating through Fourier space | Illustration or camera motion unless a separate evolving-coordinate model is supplied |
| Physical-space streamline | A different object from the Fourier triangle |

Automatic phase rotation **cannot**
be assumed. Purely imaginary
Hermitian coefficients form an
invariant real-odd velocity
subspace. With
\(p=(2,0,0)\), \(q=(0,3,0)\),
\(k=(2,3,0)\) and coefficients
\(iA e_2\), \(iA e_3\), \(iA e_3\)
and conjugates:

\[
X=52A^2,\qquad Y=532A^2,\qquad
\mathcal T=24A^3.
\]

At \(\nu=1\), \(A=24\),
\(X'=50688>0\). Locked in this
audit. The chosen nonzero triad
monomial can retain phase
\(\pi/2\) on a short interval;
generated modes respect the same
symmetry. This disproves a
universal claim that positive
transfer must immediately rotate
away. **It is not a blowup
example.**

For a fixed distinct-radius block,
**EXACT (14):**

\[
\boxed{
\dot{\mathcal T}_{abc}
+\nu(a+b+c)\mathcal T_{abc}
=\mathcal Q_{abc,N}.
}
\]

\(\mathcal Q\) is quartic and
retains the full nonlinear
derivative in each slot. Its
inputs are not confined to the
displayed triangle or to the
high-frequency projection.
Viscosity damps; it does not
remove that forcing. A Duhamel
denominator \(1/[\nu(a+b+c)]\)
does **not** by itself bound the
total normalized
positive-transfer budget.

---

## 9. The missing sufficient theorem

Set

\[
h_{K,N}=P_{\lvert k\rvert>K}u_N,
\qquad
\mathcal S_{K,N}(T)
=
\int_0^T
\frac{
\bigl[\mathcal T_{\mathrm{sc}}(h_{K,N})-\nu Y_N/4\bigr]_+
}{X_N}\,dt.
\tag{15}
\]

\(\mathcal T_{\mathrm{sc}}\) sums
complete triads with three distinct
exact radii. The positive part is
taken after this sum and the
specified viscosity subtraction.
\(X_N\) and \(Y_N\) are moments of
the **full** field; \(h\) is not an
autonomous solution. On the zero
trajectory the integrand is defined
as zero.

The already controlled complement
\(C=\mathcal T(u_N)-\mathcal T_{\mathrm{sc}}(h)\)
obeys

\[
\lvert C\rvert
\le
3C_K\sqrt{E_N}\,X_N
+\frac{\sqrt3}{2}X_N\sqrt{Y_N},
\qquad
C_K^2=\sum_{0<\lvert k\rvert\le K}\lvert k\rvert^2.
\]

Fixed-low: telescope the three
gradient slots and put the
low-frequency gradient in
\(L^\infty\). Repeated-radius:
allocate \(3\nu Y_N/4\) in Young.
Then

\[
\lvert C\rvert
\le
\frac{3\nu}{4}Y_N
+\Bigl(3C_K\sqrt{E_N}+\frac{X_N}{4\nu}\Bigr)X_N.
\]

Using \(E_N'+2\nu X_N=0\) and
mean-zero Poincaré gives the
explicit **conditional** bound
**EXACT (16):**

\[
\boxed{
X_N(t)
\le
X_N(0)
\exp\Biggl[
\frac{6C_K\sqrt{E_0}}{\nu}(1-e^{-\nu T})
+\frac{E_0}{4\nu^2}
+2\mathcal S_{K,N}(T)
\Biggr],
\quad 0\le t\le T.
}
\]

**OPEN (17). The missing theorem.**

\[
\boxed{
\forall u_0\in C^\infty_{\mathrm{div}},\
\forall\nu>0,\quad
\exists K=K(u_0,\nu)<\infty:\quad
\forall T<\infty,\quad
\sup_N\mathcal S_{K,N}(T)<\infty.
}
\]

Data, viscosity, and \(K\) stay
fixed as \(N\) increases. The bound
may depend on the datum and the
time horizon. It must be independent
of \(N\) and proved **without**
assuming the desired smoothness
bound. (17) would give uniform
\(H^1\) control through (16), then
standard strong-solution
continuation and Galerkin-limit
steps.

\[
\boxed{(17)\ \text{has not been proved here.}}
\]

A fixed absolute squared-radius
strip and separated-scale estimates
do not automatically cover the
entire all-high scalene sum: broad
comparable triples with growing
squared-radius gaps remain. A bound
on one episode’s duration does not
control its integrated strength and
repetition.

---

## 10. Centered drift remains intact

**EXACT (18).**

\[
X=\lvert A^{1/2}u\rvert_2^2,\quad
Y=\lvert Au\rvert_2^2,\quad
Z=\lvert A^{3/2}u\rvert_2^2,\quad
\Lambda=Y/X,
\]
\[
D_s=Z-Y^2/X=\sum_k\lvert k\rvert^2(\lvert k\rvert^2-\Lambda)^2\lvert u_k\rvert^2\ge 0,
\]
\[
T_c=-\langle B,A(A-\Lambda)u\rangle_{\mathbb R},
\qquad
\boxed{\Lambda'=\frac{2}{X}(T_c-\nu D_s).}
\]

For a grouped triad with modal
transfers \(\tau_j\) summing to
zero, \(w_j=\lambda_j(\lambda_j-\Lambda)\),

\[
\sum_j w_j\tau_j
=\frac13\sum_{j<\ell}(w_j-w_\ell)(\tau_j-\tau_\ell),
\qquad
w_j-w_\ell
=(\lambda_j-\lambda_\ell)(\lambda_j+\lambda_\ell-\Lambda).
\]

A further exact radial cancellation.
It does **not** establish the
required all-time bound.

The old sufficient condition
\(T_c\le\theta\nu D_s+K(t)X\),
\(\theta<1\), would imply
\(\Lambda'\le 2K\). Its coefficient
must be independently integrable
through a candidate finite endpoint,
not merely on every compact interval
before it. \(X\le E(0)\Lambda\) then
gives continuation. Defining \(K\)
from the unknown positive remainder
does not prove that integrability.

The scalene criterion (17) and the
centered criterion are **distinct
sufficient routes**. Neither is
claimed equivalent to the other.
Both locate an unresolved dynamical
estimate beyond the established
geometry.

The static sign-realizability gate
already produced
\(\mathcal A_N^{+}\) and killed
universal first-order one-sided
narrow depletion. That seed is an
input to the dynamic question. It
does not prove (17).

---

## 11. Evidence status

| Status | Examples | Permitted conclusion |
|---|---|---|
| Exact algebra and working analytic estimates | (1)–(14), (16), (18), the scoped prime criterion (12) | Retain with their hypotheses. Review the analytic proofs separately from finite checks. |
| Exact finite computations | Transfers \(0,+24,-24\); generated mode \(3i e_3\); shear ratio \(2/3\); even-output polynomial; \(16/9\) identity; four Hilbert regressions | Check conventions and demonstrate particular configurations. |
| Numerical evolution | Fixed-data positive-budget episodes at \(N^2=6,12,20\) | Evidence about those computed trajectories only. **Not rerun in this audit.** |
| Illustrative motion | Moving triangles, animated shell arrows, rendered tubes | Explanation only unless tied to specified computed variables. |

Reported, not rerun:
\(\nu=3/2\), \(K=1\),

\[
\mathcal S(1)
\approx
0.001337845,\
0.046918627,\
0.072599898
\]

at squared cutoffs \(6,12,20\).
Three cutoffs establish neither
uniform boundedness nor divergence.

---

## Lock

\[
\boxed{
(1)\text{–}(14),\ (16),\ (18),\ (12)
\text{ sit as algebra / scoped arithmetic.}
}
\]

\[
\boxed{
I_3\text{ tests existence of integer
triangles. They do not determine
amplitudes, polarizations, phases,
or cumulative signed transfer.}
}
\]

\[
\boxed{
(17)\ \sup_N\mathcal S_{K,N}(T)<\infty
\text{ is OPEN. That is the next
required proof.}
}
\]

The next required proof is a bound
on the summed, normalized, positive
scalene transfer along the actual
NS evolution. It must account for
amplitude, alignment, generated
modes, forcing, and repeated
episodes. Existence of the Fourier
triangles and the identities
governing each interaction remain
usable inputs to that proof.

No more potentials. No more
reinterpretation of the same clock.
NS is not solved.
