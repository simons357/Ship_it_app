# Fourier triangles — exact mechanism, arithmetic, remaining estimate

Reconstruction and audit — 20 September 2026.
**Identities and working estimates. Not a theorem.
Not a close. No claim of global regularity,
singularity, or mathematical novelty.**

Unaugmented NS on
\(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\).
No \(Q_1\). No \(\Phi\)-cancel. No
SND persistence. No Theorem H. No
Route A weld. Unrestricted
\(\sup\mathcal R_\star<\infty\) stays
**KILLED** by \(v_n\).

The exact geometry survives. The
current working chain controls more
than isolated triangles: an
exact-sphere weighted estimate, the
complete repeated-radius
contribution, and a fixed-low-frequency
complement. The remaining sufficient
theorem is a bound on the accumulated
positive transfer from all-high
scalene triads, uniform in the
Galerkin cutoff for each fixed smooth
initial datum. \(I_3\) prime tests
determine which integer triangles
exist; they do not determine evolving
amplitudes, polarizations, phases, or
cumulative signed transfer.

This page uses the September 20
repeated-radius and prime-branch
developments. It does **not** revert
their status to older census-only
summaries. The older reading of
\(I_3\) as \(\sum T_k=0\) (energy
conservation of \(B\)) is
**withdrawn**. \(I_3\) is the cubic
lattice. Independent specialist
review of the research chain remains
pending.

Code:
`scripts/ns_attacks/fourier_triangle_audit.py`.
Lemma A stays unaltered:
[`LEMMA-A-SBP.md`](LEMMA-A-SBP.md).
The first-variation sign gate stays
frozen:
[`STATIC-SIGN-REALIZABILITY.md`](STATIC-SIGN-REALIZABILITY.md).

Four kinds of sentence, never mixed:

| Tag | Meaning |
|---|---|
| **EXACT** | Identity. Keep the hypotheses. |
| **CLAIMED** | Working estimate, not a proof of regularity. |
| **NUMERICAL** | Printed sample or reported trajectory. Not \(C_0\). |
| **ILLUSTRATIVE** | Motion / picture. Not a bound. |

**DEAD** stays dead.

---

## Convention

Work on the normalized torus
\((\mathbb{R}/2\pi\mathbb{Z})^3\),
Fourier characters \(e^{ik\cdot x}\),
real mean-zero divergence-free
velocity, ordinary viscosity
\(\nu>0\).

\[
u(x,t)=\sum_{k\in\mathbb{Z}^3\setminus\{0\}}
u_k(t)\,e^{ik\cdot x},
\qquad
u_{-k}=\overline{u_k},
\qquad
k\cdot u_k=0.
\]

\(A=-P\Delta\), symbol \(\lvert k\rvert^2\)
on divergence-free fields.
\(B(v,w)=P[(v\cdot\nabla)w]\).
Dot products with real wavevectors
are complex bilinear; norms and real
\(L^2\) pairings use conjugation.
A shell label \(a\) means squared
radius \(\lvert k\rvert^2=a\), not
radius \(\lvert k\rvert=a\). An exact
shell and a thick dyadic annulus are
different sets.

For one interaction \(p+q=k\),

\[
a=\lvert p\rvert^2,\quad
b=\lvert q\rvert^2,\quad
c=\lvert k\rvert^2,\quad
s=p\cdot q=\frac{c-a-b}{2},\quad
\Delta=ab-s^2=\lvert p\times q\rvert^2.
\]

Thus \(\cos\theta=s/\sqrt{ab}\) and

\[
(\sqrt a-\sqrt b)^2\le c\le(\sqrt a+\sqrt b)^2.
\]

---

## 1. Shape and shell placement (EXACT)

For a noncollinear triangle choose
\(e_0=k/\sqrt{c}\), \(e_1\) in the
triangle plane perpendicular to \(k\),
and \(e_2\) normal to that plane.

\[
p=x e_0+h e_1,\qquad
q=y e_0-h e_1,
\]

\[
x=\frac{c+a-b}{2\sqrt c},\quad
y=\frac{c+b-a}{2\sqrt c},\quad
h=\sqrt{\Delta/c}.
\]

These equations give the exact shape
and shell placement. At fixed
\(k,a,b\), the possible \(p\) vectors
lie on the intersection of a sphere
with a plane, hence on a circle when
nondegenerate. The integer points on
that circle are the actual Fourier
interactions. This geometric circle
is not a fluid trajectory.

---

## 2. Polarization, Leray, and \(S_{pq}\) (EXACT)

The coefficient at \(p\) lies in the
two-dimensional complex plane
perpendicular to \(p\).

\[
u_p
=A_1\frac{h e_0-x e_1}{\sqrt a}+A_2 e_2,
\qquad
u_q
=B_1\frac{h e_0+y e_1}{\sqrt b}+B_2 e_2.
\]

Arbitrary complex divergence-free
polarizations are permitted. No
common helicity or common phase is
assumed. Incompressibility gives

\[
q\cdot u_p=k\cdot u_p,\qquad
p\cdot u_q=k\cdot u_q.
\]

The output projector

\[
P_k=I-\frac{k\otimes k}{\lvert k\rvert^2}
\]

removes the output component along
\(k\). It is a contraction. It does
**not** provide a universal small
factor on every admissible
interaction.

The symmetrized pair vector

\[
S_{pq}=P_k\bigl[(q\cdot u_p)u_q+(p\cdot u_q)u_p\bigr]
\]

has the full decomposition

\[
\boxed{
S_{pq}
=\frac{h(b-a)}{\sqrt{ab}}A_1 B_1\,e_1
+\sqrt{c}\,h
\Bigl(\frac{A_1 B_2}{\sqrt a}+\frac{A_2 B_1}{\sqrt b}\Bigr)e_2.
}
\tag{1}
\]

The ordered Fourier operator is

\[
\widehat B(u,u)(k)
=i P_k\sum_{p+q=k}(q\cdot u_p)u_q
=\frac i2\sum_{p+q=k}S_{pq}.
\tag{2}
\]

The factor \(1/2\) belongs to the
ordered symmetrized sum. Dropping it
changes the constants.

---

## 3. Equal-length cancellation (EXACT)

If \(a=b=\alpha\) and \(c=\beta\),
then \(x=y=\sqrt{\beta}/2\) and
\(h=\sqrt{\alpha-\beta/4}\).
Equation (1) becomes

\[
\boxed{
S_{pq}
=\sqrt{\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr)}
(A_1 B_2+A_2 B_1)\,e_2.
}
\tag{3}
\]

The in-plane transverse component
cancels. The normal component
generally remains. Purely in-plane
inputs make that normal component
zero as well; general
three-dimensional inputs do not.
At \(\beta=0\) or \(\beta=4\alpha\),
the collinear interaction vanishes
directly by divergence freedom,
without a degenerate frame.

---

## 4. Unequal-length defect (EXACT)

For unequal lengths the
coordinate-free defect is

\[
\boxed{
(P_k p)\cdot S_{pq}
=\frac{b-a}{c}(k\cdot u_p)(k\cdot u_q).
}
\tag{4}
\]

Proof: set \(t=(p\cdot k)/c\) and
\(\ell=P_k p\). Then
\(\ell\cdot u_p=-t(k\cdot u_p)\),
\(\ell\cdot u_q=(1-t)(k\cdot u_q)\),
and \(1-2t=(b-a)/c\). This is a
complete proof of this component
identity. It does **not** estimate
the normal component or the sum over
unequal radii.

Near equal radii, the displayed
defect is small relative to the
appropriate frequency scale. Thick
comparable shells allow \(b-a\) of
the same order as \(a\) and \(b\),
so comparable size alone does not
give this smallness.

---

## 5. Signed transfer (EXACT)

\[
\tau_k=-\operatorname{Re}\bigl[\widehat B(k)\cdot\overline{u_k}\bigr].
\]

\[
\frac12\frac{d}{dt}\lvert u_k\rvert^2+\nu\lvert k\rvert^2\lvert u_k\rvert^2
=\tau_k,
\qquad
\mathcal T(u)=\sum_k\lvert k\rvert^2\tau_k.
\tag{5}
\]

The paired \(p,q\) contribution to
\(\tau_k\) is
\(\operatorname{Im}(S_{pq}\cdot\overline{u_k})\);
a full ordered symmetrized sum uses
the corresponding \(1/2\). For fixed
polarization vectors and coefficient
phases, the phase dependence has the
form

\[
\operatorname{Im}\bigl[C_{pqk}e^{i(\phi_p+\phi_q-\phi_k)}\bigr].
\]

\(C\) includes amplitudes,
polarization, and geometry; it need
not be real. A triangle or a power
spectrum alone does not determine
the sign. Replacing the whole field
by \(-u\) preserves all quadratic
moments and reverses the cubic
transfers.

An exact finite example is

\[
u=\bigl(2\cos 2y,\;0,\;2\cos 3x+f(3x+2y)\bigr).
\]

All three choices below have
\(E=6\), \(X=52\), \(Y=532\),
\(Z=5980\).

| Receiving term \(f(\theta)\) | Full signed enstrophy transfer \(\mathcal T\) |
|---|---:|
| \(2\cos\theta\) | \(0\) |
| \(2\sin\theta\) | \(+24\) |
| \(-2\sin\theta\) | \(-24\) |

These values include all ordered
interactions and both Fourier signs,
including compensating donor
transfers. Unweighted kinetic-energy
transfer sums to zero in every case.
They were recomputed here with
rational arithmetic.

There is also cancellation between
the different receiver choices. For
a complete triad, modal energy
transfers sum to zero. If all three
radii equal \(a\), their enstrophy
weights are equal, so their total
enstrophy transfer is zero. The two
cancellations act at different
levels: a field supported on one
exact sphere can generate modes
outside that sphere even while its
initial enstrophy transfer vanishes.

---

## 6. Repeated-radius and scalene blocks (EXACT)

When the radius multiset is
\(\{a,a,b\}\) with \(b\neq a\),

\[
\tau_{b\leftarrow aa}
=-\operatorname{Re}\langle B(u_a,u_a),u_b\rangle.
\]

All receiver choices together give

\[
\mathcal T_{\{a,a,b\}}=(b-a)\tau_{b\leftarrow aa}.
\tag{6}
\]

The equal-input portion is \(b\tau\);
the unequal-input portion is
\(-a\tau\). Calling all
unequal-input terms uncontrolled
would discard a completed part of
the current argument.

For three distinct squared radii
\(a<b<c\), use \(p+q+r=0\) and

\[
I_p
=\sum_{\substack{p+q+r=0\\ \lvert p\rvert^2=a,\,\lvert q\rvert^2=b,\,\lvert r\rvert^2=c}}
\operatorname{Im}\bigl[(q\cdot u_p)(u_q\cdot u_r)\bigr],
\]

with \(I_q\) and \(I_r\) defined
cyclically on the same indexed set.
Then

\[
\boxed{
\mathcal T_{abc}
=(c-b)I_p+(a-c)I_q+(b-a)I_r.
}
\tag{7}
\]

The negative triple is already
included. There is no additional
conjugation or factor of two in this
closed-triad convention. Taking
absolute values before the receiver
choices are combined loses the
radius-difference factors in (6)
and (7).

---

## 7. Exact-sphere bound and repeated-radius estimate

For nonnegative coefficients \(r_p\)
supported on \(\lvert p\rvert^2=\alpha\),
put \(F=\sum r_p^2\) and
\(L_k=\sum_{p+q=k} r_p r_q\). The
exact-sphere argument proves

\[
\sum_{\lvert k\rvert^2=\beta}L_k^2\le 3F^2
\qquad(\beta>0).
\tag{8}
\]

The diagonal contributes at most
\(F^2\). For two distinct
nonantipodal inputs \(p,p'\), the
possible \(k\) satisfy a sphere
equation and two independent plane
equations. There are at most two
such real points. The antipodal case
is incompatible with \(\beta>0\).
After the elementary product
inequality, the off-diagonal
contribution is at most \(2F^2\).
No bound on the number of points in
an individual circle fiber is
assumed.

Equations (2), (3) and (8) retain
the factors \(1/4\),
\(\beta(1-\beta/(4\alpha))\), and
\(3\). Thus, for \(Aw=\alpha w\),

\[
\lvert\Pi_\beta B(w,w)\rvert_2^2
\le
\frac34\beta\Bigl(1-\frac\beta{4\alpha}\Bigr)\lvert w\rvert_2^4.
\tag{9}
\]

For \(r=\beta/\alpha\), the
normalized ratio is at most \(16/9\)
because

\[
\frac{16}{9}-\frac34 r^2\Bigl(1-\frac r4\Bigr)
=\frac{(3r+4)(3r-8)^2}{144}\ge 0.
\]

This is an upper bound. Attainment
and optimality of the operator
constant are **not** asserted.
**CLAIMED**, one input shell only.
The explicit field
\(w=(\sin y,\sin z,\sin x)\) gives
\(E=3/2\), squared output norm
\(3/4\) on \(\beta=2\), and
normalized ratio \(2/3\). The audit
reproduced its twelve nonzero
output coefficients exactly.

Summing output radii and then input
radii gives the retained estimate

\[
\lvert A^{1/2}B_{\mathrm{equal}}(u,u)\rvert_2
\le 2\sqrt{XY}.
\tag{10}
\]

Regrouping all repeated-radius
receiver choices improves the
relevant signed estimate to

\[
\boxed{
\lvert\mathcal T_{\mathrm{rep}}(u)\rvert
\le\frac{\sqrt 3}{2}X\sqrt Y.
}
\tag{11}
\]

One arithmetic fact already enters
this successful estimate: the output
\(b\) of equal inputs \(a\) is even,
since \(b=2a+2\,p\cdot q\). The
exact sum used after (6) is

\[
\sum_{\substack{2\le b\le 4a\\ b\text{ even}}}
(b-a)^2\Bigl(1-\frac{b}{4a}\Bigr)
=a^3-\frac{a^2}{2}.
\]

Weighted Cauchy–Schwarz then uses
\(\sum a^{3/2}E_a\le\sqrt{XY}\).
This is arithmetic carried through
the correct weighted expression. It
is not an unweighted count
substituted into a different
operator.

---

## 8. What is lost, or remains to be proved

| Operation | What is lost, or what remains |
|---|---|
| Replace a complex coefficient by its magnitude | Relative phase and vector alignment disappear. |
| Bound each receiver orientation separately | Energy redistribution and radius-difference cancellation disappear. |
| Replace exact radii by a thick annulus | Exact equality, parity, and the fixed-sphere incidence geometry no longer give the same estimate. |
| Apply separate Cauchy–Schwarz bounds at each output \(k\) | Shared input coefficients and simultaneous incidence must still be controlled when summing \(k\). |
| Count admissible integer triangles | Coefficient weights, signs, concentration, and sharing between triangles remain unspecified. |
| Estimate each fixed distinct-radius triple | The simultaneous sum over all such triples is still required. |
| Infer future behavior from one field | Generated modes, changing amplitudes, polarization, and nonlinear forcing remain unaccounted for. |
| Integrate a signed derivative inside a positive part | Bounded endpoints do not control repeated positive contributions or total variation. |

The older thick-shell obstruction
must not be confused with a defect
of the exact-sphere proof. The
current source provides an explicit
projected-convolution family with
\(Q_{i,i+1}\ge 2^{i/2}/2048\) for
the displayed unrestricted
\(\tau=1/2\) low-high quotient. Its
proof retains the original
\(H^1\) times \(H^2\) denominator.
This prevents replacing that
operator’s dense assembly factor by
the proposed subpower incidence
factor. It does **not** refute a
differently restricted operator, and
does **not** produce an NS
singularity. No \(W_{ij}\) has been
reconstructed here.

---

## 9. \(I_3\) — integer realizability, not amplitudes

\(I_3\) is the ordinary cubic
lattice \((\mathbb{Z}^3,x_1^2+x_2^2+x_3^2)\).
A triangle with prescribed \(a,b,c\)
exists precisely when the binary
Gram matrix

\[
G=\begin{pmatrix}a&s\\ s&b\end{pmatrix},
\qquad
s=(c-a-b)/2,
\]

has an integer realization
\(G=V^T V\) with \(V\) a \(3\times 2\)
integer matrix. The test concerns
wavevectors, not velocity
coefficients.

For \(a>0\), \(\Delta=ab-s^2>0\),
and integer \(a,b,s\), ordinary
integral representation by \(I_3\)
is equivalent to representation
over every \(\mathbb{Q}_\ell\) and
every \(\mathbb{Z}_\ell\). A finite
criterion is

\[
\boxed{
(a,\Delta)_\ell\,(a,-1)_\ell\,(\Delta,-1)_\ell=1
\quad\text{for every prime }\ell\mid 2a\Delta,
}
\tag{12}
\]

where \((\ ,\ )_\ell\) is the Hilbert
symbol. The positive-definite
assumption supplies the real-place
condition. Primitive embeddings,
prescribed normals, degenerate Grams,
and class-group surjectivity are
separate questions.

The rational space to compare is
\(G^\perp\langle\Delta\rangle\),
whose determinant is a square. The
cited local classification supplies
its rational test. The September 20
note supplies the local integrality
step; the one-class genus of \(I_3\)
supplies the integral conclusion.
Referenced statements:
Schulze-Pillot, Corollary 5.29,
Example 6.14, Theorem 6.15,
Corollary 6.16, Theorem 7.32.
This is an application of classical
quadratic-form theory. It is not a
conclusion drawn from a census
alone.

The odd-prime enlargement is also
precise: after diagonalizing as
\(\langle\ell^r u,\ell^t v\rangle\),
\(t\ge 2\) permits adjoining
\(e_2/\ell\). In the exceptional
\(r=t=1\) case, local compatibility
forces \(-v/u\) to be a square
modulo \(\ell\); adjoining
\((x e_1+e_2)/\ell\) then divides
the determinant by \(\ell^2\) while
preserving integrality. This
operation modifies an abstract
lattice in its rational plane. It
is **not** time evolution of
Fourier modes.

Exact regression cases recomputed
in this audit:

| Gram data \((a,b,s)\) | Local result |
|---|---|
| \((96,96,0)\) | Fails at \(2\) and \(3\) |
| \((2,3,1)\) | Fails at \(2\) and \(5\) |
| \((2,2,-1)\) | Passes all required primes |
| \((14,14,-7)\) | Passes all required primes |

In particular, \(a=b=c=\alpha\)
forces \(s=-\alpha/2\), so odd
\(\alpha\) cannot support a
monochromatic closed triangle.
Even \(\alpha\) is only a necessary
condition; it is not sufficient.
The old unrestricted assertion that
every proper class of discriminant
\(-4\Delta\) occurs as an orthogonal
lattice has been corrected in the
prime note.

For an impossible triple, its
contribution is identically zero at
every time. For an allowed triple,
the prime tests alone impose no
velocity amplitude, polarization
alignment, or phase sign. A
successful analytic use must retain
those weights when counting and
must then control their evolution.
The fixed-sphere weighted lemma and
the even-output sum above are
completed uses. A universal scalene
time estimate is **not**.

---

## 10. Actual motion (EXACT kinematics)

Along full Galerkin NS,

\[
\dot u_k
=-\nu\lvert k\rvert^2 u_k
-i P_k\sum_{p+q=k}(q\cdot u_p)u_q,
\qquad
\lvert k\rvert\le N.
\tag{13}
\]

The vectors \(p,q,k\) and their
arithmetic restrictions remain
fixed. Their coefficients change,
and initially zero coefficients can
become nonzero. In the
zero-transfer cosine example, the
initially absent mode \((3,-2,0)\)
has \(B\) coefficient \(3i e_3\),
so its initial derivative is
\(-3i e_3\). A zero instantaneous
transfer or empty receiving mode
therefore does not make the
interaction inactive for later time.

| Display element | Defensible interpretation |
|---|---|
| Fixed Fourier triangle | The actual additive relation between modes |
| Changing line thickness or brightness | An explicitly chosen amplitude, energy, or transfer diagnostic |
| A phase dial or polarization arrow | A coefficient coordinate, using a stated convention |
| Arrows between shells | Signed transfer after the complete required grouping |
| Triangle translating or rotating through Fourier space | Illustration or camera motion unless a separate evolving-coordinate model is supplied |
| Physical-space streamline | A different object from the Fourier triangle |

Automatic phase rotation cannot be
assumed. Purely imaginary Hermitian
coefficients form an invariant
real-odd velocity subspace. With
modes \(p=(2,0,0)\), \(q=(0,3,0)\),
\(k=(2,3,0)\), coefficients
\(iA e_2\), \(iA e_3\), \(iA e_3\)
and their conjugates, one gets
\(X=52A^2\), \(Y=532A^2\), and
\(\mathcal T=24A^3\). At
\(\nu=1\), \(A=24\),
\(X'=50688>0\). The chosen nonzero
triad monomial can retain phase
\(\pi/2\) on a short interval;
generated modes respect the same
symmetry. This disproves a
universal claim that positive
transfer must immediately rotate
away. It is **not** a blowup
example.

For a fixed distinct-radius block,

\[
\boxed{
\dot{\mathcal T}_{abc}+\nu(a+b+c)\mathcal T_{abc}
=\mathcal Q_{abc,N},
}
\tag{14}
\]

where \(\mathcal Q\) is quartic and
retains the full nonlinear
derivative in each slot. Its inputs
are not confined to the displayed
triangle or to the high-frequency
projection. Viscosity supplies a
damping term; it does not remove
that forcing. A Duhamel denominator
\(1/[\nu(a+b+c)]\) therefore does
not by itself bound the total
normalized positive-transfer budget.

---

## 11. The remaining sufficient theorem (OPEN)

Set

\[
h_{K,N}=P_{\lvert k\rvert>K}u_N,
\qquad
\mathcal S_{K,N}(T)
=\int_0^T
\frac{\bigl[\mathcal T_{\mathrm{sc}}(h_{K,N})-\nu Y_N/4\bigr]_+}{X_N}\,dt.
\tag{15}
\]

Here \(\mathcal T_{\mathrm{sc}}\)
sums complete triads with three
distinct exact radii. The positive
part is taken after this sum and
the specified viscosity subtraction.
\(X_N\) and \(Y_N\) are the moments
of the full field; \(h\) is not an
autonomous solution. On the zero
trajectory the integrand is defined
as zero.

The already controlled complement
\(C=\mathcal T(u_N)-\mathcal T_{\mathrm{sc}}(h)\)
obeys

\[
\lvert C\rvert
\le 3C_K\sqrt{E_N}\,X_N+\frac{\sqrt 3}{2}X_N\sqrt{Y_N},
\qquad
C_K^2=\sum_{0<\lvert k\rvert\le K}\lvert k\rvert^2.
\]

The fixed-low estimate follows by
telescoping the three gradient slots
of the enstrophy-production integral
and putting the low-frequency
gradient in \(L^\infty\). For the
repeated-radius term, allocate
\(3\nu Y_N/4\) in Young’s
inequality. Then

\[
\lvert C\rvert
\le\frac{3\nu}{4}Y_N
+\Bigl(3C_K\sqrt{E_N}+\frac{X_N}{4\nu}\Bigr)X_N.
\]

Using \(E_N'+2\nu X_N=0\) and
mean-zero Poincaré gives the
explicit conditional bound

\[
\boxed{
X_N(t)
\le X_N(0)\exp\Biggl[
\frac{6C_K\sqrt{E_0}}{\nu}(1-e^{-\nu T})
+\frac{E_0}{4\nu^2}
+2\mathcal S_{K,N}(T)
\Biggr],
\quad 0\le t\le T.
}
\tag{16}
\]

The missing theorem is

\[
\boxed{
\forall u_0\in C^\infty_{\mathrm{div}},\
\forall\nu>0,\quad
\exists K=K(u_0,\nu)<\infty:\quad
\forall T<\infty,\quad
\sup_N\mathcal S_{K,N}(T)<\infty.
}
\tag{17}
\]

The data, viscosity, and \(K\) stay
fixed as \(N\) increases. The bound
may depend on the datum and time
horizon, but must be independent of
\(N\) and proved without assuming
the desired smoothness bound.
Equation (17) would give uniform
\(H^1\) control through (16),
followed by the standard
strong-solution continuation and
Galerkin-limit steps.
**Equation (17) has not been proved
here.**

A fixed absolute squared-radius
strip and separated-scale estimates
do not automatically cover the
entire all-high scalene sum: broad
comparable triples with growing
squared-radius gaps remain. A bound
on one episode’s duration also does
not control its integrated strength
and repetition.

---

## 12. Centered clock — a distinct sufficient route (EXACT identities)

The earlier centered-drift identity
remains intact.

\[
X=\lvert A^{1/2}u\rvert_2^2,\quad
Y=\lvert Au\rvert_2^2,\quad
Z=\lvert A^{3/2}u\rvert_2^2,\quad
\Lambda=Y/X,
\]

\[
N=-\langle B,Au\rangle_{\mathbb R},\quad
M=-\langle AB,Au\rangle_{\mathbb R},\quad
T_c=M-\Lambda N,
\]

\[
\mathcal D_s=Z-Y^2/X
=\sum_k\lvert k\rvert^2\bigl(\lvert k\rvert^2-\Lambda\bigr)^2\lvert u_k\rvert^2\ge 0,
\]

\[
T_c=-\langle B,A(A-\Lambda)u\rangle_{\mathbb R},
\qquad
\boxed{\Lambda'=\frac2X(T_c-\nu\mathcal D_s).}
\tag{18}
\]

For a grouped triad with modal
transfers \(\tau_j\) summing to
zero, set \(w_j=\lambda_j(\lambda_j-\Lambda)\).
Then its centered contribution
equals

\[
\sum_j w_j\tau_j
=\frac13\sum_{j<\ell}(w_j-w_\ell)(\tau_j-\tau_\ell),
\qquad
w_j-w_\ell
=(\lambda_j-\lambda_\ell)(\lambda_j+\lambda_\ell-\Lambda).
\]

This preserves a further exact
radial cancellation. It does **not**
establish the required all-time
bound. The old sufficient condition
\(T_c\le\theta\nu\mathcal D_s+K(t)X\),
\(\theta<1\), would imply
\(\Lambda'\le 2K\). Its coefficient
must be independently integrable
through a candidate finite endpoint,
not merely on every compact interval
before it. \(X\le E(0)\Lambda\) then
gives continuation. Defining \(K\)
from the unknown positive remainder
does not prove that integrability.

The current scalene criterion (17)
and the earlier centered criterion
are **distinct sufficient routes**.
Neither is claimed equivalent to
the other. Both locate an unresolved
dynamical estimate beyond the
established geometry.

The Signed Assembly Gate
([`SIGNED-ASSEMBLY-GATE.md`](SIGNED-ASSEMBLY-GATE.md))
remains the named assembly blank
before old Gate 5. It is **not** a
substitute for (17). Static
shared-output rescue stays
**KILLED**. Next Gate on that desk
is still
[`JOINT-EPOCH-BUDGET.md`](JOINT-EPOCH-BUDGET.md).

---

## 13. Evidence statuses

| Status | Examples | Permitted conclusion |
|---|---|---|
| Exact algebra and working analytic estimates | (1)–(14), (16), (18); the precisely scoped prime criterion (12); \(\lvert\mathcal T_{\mathrm{rep}}\rvert\le(\sqrt3/2)X\sqrt Y\) | Retain with their hypotheses. Review the analytic proofs separately from finite checks. |
| Exact finite computations | Transfers \(0,+24,-24\); generated mode \(3ie_3\); \(2/3\) shear ratio; prime regression cases | Check conventions and demonstrate particular configurations. |
| Numerical evolution | Fixed-data positive-budget episodes at \(N^2=6,12,20\) | Evidence about those computed trajectories only. |
| Illustrative motion | Moving triangles, animated shell arrows, rendered tubes | Explanation only unless tied to specified computed variables. |

The current fixed-data report gives
\(\mathcal S(1)\approx 0.001337845\),
\(0.046918627\), and \(0.072599898\)
at squared cutoffs \(6,12,20\), with
\(\nu=3/2\) and \(K=1\). These are
reported trajectory computations,
**not rerun** in this audit. Three
cutoffs establish neither uniform
boundedness nor divergence. Earlier
locally-admissible finite censuses
likewise remain computations. The
newer local-to-global result rests
on its separate argument.

The additional audit here used
exact rational arithmetic for
complex polarization tests, full
ordered phase examples, newly
generated coefficients, the
odd-field regression, the shear
ratio, the finite polynomial sums,
small exact-sphere incidence
checks, and the four Hilbert-symbol
regression cases. Those tests
support implementation correctness.
The universal claims rest on the
displayed analytic arguments.

---

## 14. Next required proof

The next required proof is a bound
on the summed, normalized, positive
scalene transfer along the actual
NS evolution — equation (17). It
must account for amplitude,
alignment, generated modes,
forcing, and repeated episodes.
Existence of the Fourier triangles
and the identities governing each
interaction remain usable inputs to
that proof.

Do not prove (17) by declaration.
Do not cash \(S(1)\) samples as
\(\sup_N\mathcal S_{K,N}(T)<\infty\).
Do not restore unrestricted
\(\star\). Do not treat (12) as a
phase or amplitude bound.

---

## Sources

- Attack 9D exact-shell proof, 19 September 2026.
- Repeated radii and scalene target, 20 September 2026.
- Current closure report, sections through the direct sufficient theorem, 20 September 2026.
- \(I_3\) prime branch recovered, 20 September 2026.
- Current status and fixed-data episodes, 20 September 2026.
- Centered spectral drift note, sections containing the exact identities and continuation criteria, 6 September 2026.
- Actual nonlinear packet obstruction, 19 September 2026.
- Rainer Schulze-Pillot, *Lecture Notes on Quadratic Forms and their Arithmetic*, cited local and genus results.
- Classical background on helical triads: Rathmann and Ditlevsen. The particular constants and reductions above are attributed to the working source notes and their displayed derivations, not to that background paper.

Later-tape SoT identities remain on
PR #104. This page does not replace
that tape. It corrects the \(I_3\)
object and names (17) as the
remaining sufficient estimate.

---

## Lock

Shell \(a=\lvert k\rvert^2\) EXACT.
Frame, \(S_{pq}\), (1)–(7) EXACT.
(8)–(11) working estimates;
\(16/9\) CLAIMED, one shell, not
regularity. \(\lvert\mathcal T_{\mathrm{rep}}\rvert\)
retained. \(I_3\) is the cubic
lattice; (12) decides existence
only. Galerkin (13) and
\(\dot{\mathcal T}_{abc}\) (14)
EXACT. Complement plus (16)
conditional. **(17) OPEN.**
Centered clock (18) EXACT; its
sufficient \(T_c\) bound is a
distinct OPEN route.
Finite \(0,+24,-24\), \(3ie_3\),
\(2/3\), Hilbert table: exact
checks. \(S(1)\) samples
NUMERICAL, not rerun.

SAG remains the named assembly
gate, not a substitute for (17).
Static shared-output rescue
**KILLED**. Joint epoch budget
OPEN. Lemma A unaltered. Sign
gate unaltered. ONE SIGN, if it
appears, is the Gram / \(I_3\)
bridge into dynamics — existence
still does not supply amplitudes.
NS not solved.
