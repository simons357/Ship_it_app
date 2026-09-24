# Fourier triangles — exact mechanism, arithmetic restrictions, remaining time estimate

**Reconstruction and audit, 20 September 2026.**
Filed 24 September 2026. Machine-checked identities only.
Independent specialist review of the research chain remains pending.

**Classical unaugmented 3-D Navier–Stokes stays open.**
DA-NS-2 stays **OPEN**. The missing scalene theorem (17) stays **OPEN**.
No claim of global regularity, singularity, or mathematical novelty.

This reconstruction uses the current source notes, including the
20 September repeated-radius and prime-branch developments. It does
**not** revert their status to older census-only summaries. It does
**not** alter the 24 Sep RMS/SBP gate or the static-frontier lock
(separate PRs).

Machine: [`scripts/fourier_triangles_audit.py`](../scripts/fourier_triangles_audit.py).
Lock: [`data/fourier_triangles_audit_2026-09-20.json`](../data/fourier_triangles_audit_2026-09-20.json).

\(I_3\) here is integer realizability of wavevectors on the cubic
lattice. It does **not** determine evolving amplitudes, polarizations,
phases, or cumulative signed transfer. It is not an NS remainder.

---

## Status

| Item | Bucket |
|---|---|
| Geometry, frame, (1)–(4), (6)–(7) | **EXACT** |
| Transfer bookkeeping (5); equal-sphere (8)–(10) | **EXACT** / retained estimates |
| Repeated-radius signed bound (11) | **EXACT** (retained estimate) |
| Local-to-global \(I_3\) criterion (12) | **EXACT** (classical quadratic forms) |
| Galerkin motion (13); block derivative (14) | **EXACT** |
| Complement + conditional \(H^1\) bound (16) | **EXACT** (conditional on \(\mathcal S\)) |
| Centered drift (18) | **EXACT** |
| Finite transfers \(0,+24,-24\); generated mode; shear \(3/4\); Hilbert regressions | **EXACT finite** |
| Missing scalene budget (17) | **OPEN** — the remaining sufficient theorem |
| \(W_{ij}\) | **NOT RECONSTRUCTED** |
| Fixed-data \(\mathcal S(1)\) at \(N^2=6,12,20\) | **REPORTED**, not rerun here |
| DA-NS-2 | **OPEN** — a distinct sufficient route |

---

## Convention

Normalized torus \((\mathbb R/2\pi\mathbb Z)^3\), characters
\(e^{ik\cdot x}\), real mean-zero divergence-free velocity,
\(\nu>0\).

\[
u(x,t)=\sum_{k\in\mathbb Z^3\setminus\{0\}}u_k(t)e^{ik\cdot x},
\qquad u_{-k}=\overline{u_k},\qquad k\cdot u_k=0.
\]

\(A=-P\Delta\) with symbol \(|k|^2\) on divergence-free fields,
\(B(v,w)=P[(v\cdot\nabla)w]\). A shell label \(a\) means squared
radius \(|k|^2=a\), not radius \(|k|=a\). An exact shell and a thick
dyadic annulus are different sets.

For one interaction \(p+q=k\),

\[
a=|p|^2,\quad b=|q|^2,\quad c=|k|^2,\quad
s=p\cdot q=\frac{c-a-b}{2},\quad
\Delta=ab-s^2=|p\times q|^2.
\]

\[
(\sqrt a-\sqrt b)^2\le c\le(\sqrt a+\sqrt b)^2.
\]

Noncollinear frame: \(e_0=k/\sqrt c\), \(e_1\) in the triangle plane
perpendicular to \(k\), \(e_2\) normal to that plane.

\[
p=x e_0+h e_1,\qquad q=y e_0-h e_1,
\]
\[
x=\frac{c+a-b}{2\sqrt c},\quad
y=\frac{c+b-a}{2\sqrt c},\quad
h=\sqrt{\Delta/c}.
\]

At fixed \(k,a,b\), the possible \(p\) lie on a circle when
nondegenerate. Integer points on that circle are the actual Fourier
interactions. This geometric circle is not a fluid trajectory.

---

## Polarization and the pair vector

\[
u_p=A_1\frac{h e_0-x e_1}{\sqrt a}+A_2 e_2,
\qquad
u_q=B_1\frac{h e_0+y e_1}{\sqrt b}+B_2 e_2.
\]

Arbitrary complex divergence-free polarizations; no common helicity
or common phase. Then \(q\cdot u_p=k\cdot u_p\) and
\(p\cdot u_q=k\cdot u_q\). The output projector
\(P_k=I-k\otimes k/|k|^2\) is a contraction. It does not provide a
universal small factor on every admissible interaction.

\[
S_{pq}=P_k[(q\cdot u_p)u_q+(p\cdot u_q)u_p].
\]

\[
\boxed{
S_{pq}
=
\frac{h(b-a)}{\sqrt{ab}}A_1B_1\,e_1
+
\sqrt c\,h
\left(
\frac{A_1B_2}{\sqrt a}+\frac{A_2B_1}{\sqrt b}
\right)e_2.
}
\tag{1}
\]

\[
\widehat B(u,u)(k)
=
iP_k\sum_{p+q=k}(q\cdot u_p)u_q
=
\frac i2\sum_{p+q=k}S_{pq}.
\tag{2}
\]

The factor \(1/2\) belongs to the ordered symmetrized sum. Dropping
it changes the constants. Rechecked in sympy.

---

## Equal-length cancellation and the unequal defect

If \(a=b=\alpha\) and \(c=\beta\), then \(x=y=\sqrt\beta/2\) and
\(h=\sqrt{\alpha-\beta/4}\).

\[
\boxed{
S_{pq}
=
\sqrt{\beta\left(1-\frac{\beta}{4\alpha}\right)}
(A_1B_2+A_2B_1)\,e_2.
}
\tag{3}
\]

The in-plane transverse component cancels. The normal component
generally remains. Purely in-plane inputs make that normal component
zero as well; general three-dimensional inputs do not. At
\(\beta=0\) or \(\beta=4\alpha\), the collinear interaction vanishes
by divergence freedom.

\[
\boxed{
(P_kp)\cdot S_{pq}
=
\frac{b-a}{c}(k\cdot u_p)(k\cdot u_q).
}
\tag{4}
\]

With \(t=(p\cdot k)/c\) and \(\ell=P_kp\): \(\ell\cdot u_p=-t(k\cdot u_p)\),
\(\ell\cdot u_q=(1-t)(k\cdot u_q)\), and \(1-2t=(b-a)/c\). This is a
complete proof of this component identity. It does not estimate the
normal component or the sum over unequal radii. Near equal radii the
displayed defect is small relative to the frequency scale. Thick
comparable shells allow \(b-a\) of the same order as \(a\) and \(b\).

---

## Signed transfer

\[
\tau_k=-\operatorname{Re}[\widehat B(k)\cdot\overline{u_k}].
\]

\[
\frac12\frac d{dt}|u_k|^2+\nu|k|^2|u_k|^2=\tau_k,
\qquad
\mathcal T(u)=\sum_k|k|^2\tau_k.
\tag{5}
\]

The paired contribution is \(\operatorname{Im}(S_{pq}\cdot\overline{u_k})\);
a full ordered symmetrized sum uses the corresponding \(1/2\). Phase
dependence has the form
\(\operatorname{Im}[C_{pqk}e^{i(\phi_p+\phi_q-\phi_k)}]\).
A triangle or a power spectrum alone does not determine the sign.
Replacing the field by \(-u\) preserves quadratic moments and
reverses cubic transfers.

Exact finite example
\(u=(2\cos 2y,\ 0,\ 2\cos 3x+f(3x+2y))\).
All three choices have \(E=6\), \(X=52\), \(Y=532\), \(Z=5980\).

| Receiving term \(f(\theta)\) | Full signed enstrophy transfer \(\mathcal T\) |
|---|---:|
| \(2\cos\theta\) | \(0\) |
| \(2\sin\theta\) | \(+24\) |
| \(-2\sin\theta\) | \(-24\) |

Recomputed here with the ordered Fourier operator. Unweighted
kinetic-energy transfer sums to zero in every case. In the cosine
field the initially absent mode \((3,-2,0)\) has
\(\widehat B=3i\,e_3\), so a zero instantaneous transfer does not
make the interaction inactive later.

For a complete triad, modal energy transfers sum to zero. If all
three radii equal \(a\), enstrophy weights are equal and total
enstrophy transfer is zero. A field supported on one exact sphere
can still generate modes outside that sphere.

---

## Repeated radius and scalene grouping

When the radius multiset is \(\{a,a,b\}\) with \(b\neq a\),

\[
\tau_{b\leftarrow aa}=-\operatorname{Re}\langle B(u_a,u_a),u_b\rangle,
\qquad
\mathcal T_{\{a,a,b\}}=(b-a)\tau_{b\leftarrow aa}.
\tag{6}
\]

The equal-input portion is \(b\tau\); the unequal-input portion is
\(-a\tau\). Calling all unequal-input terms uncontrolled discards a
completed part of the argument.

For three distinct squared radii \(a<b<c\), with \(p+q+r=0\),

\[
I_p
=
\sum_{\substack{p+q+r=0\\|p|^2=a,\ |q|^2=b,\ |r|^2=c}}
\operatorname{Im}[(q\cdot u_p)(u_q\cdot u_r)],
\]

and \(I_q,I_r\) cyclically on the same indexed set.

\[
\boxed{
\mathcal T_{abc}=(c-b)I_p+(a-c)I_q+(b-a)I_r.
}
\tag{7}
\]

The negative triple is already included. There is no extra
conjugation or factor of two in this closed-triad convention.
Taking absolute values before the receiver choices are combined
loses the radius-difference factors in (6) and (7).

---

## Exact-sphere estimates that survive

For nonnegative \(r_p\) on \(|p|^2=\alpha\), \(F=\sum r_p^2\),
\(L_k=\sum_{p+q=k}r_pr_q\),

\[
\sum_{|k|^2=\beta}L_k^2\le 3F^2\qquad(\beta>0).
\tag{8}
\]

Diagonal \(\le F^2\). Distinct nonantipodal inputs determine at most
two real \(k\); the antipodal case is incompatible with \(\beta>0\).
Off-diagonal \(\le 2F^2\). No bound on an individual circle fiber is
assumed.

With the factors \(1/4\), \(\beta(1-\beta/(4\alpha))\), and \(3\)
retained, for \(Aw=\alpha w\),

\[
|\Pi_\beta B(w,w)|_2^2
\le
\frac34\beta\left(1-\frac\beta{4\alpha}\right)|w|_2^4.
\tag{9}
\]

For \(r=\beta/\alpha\),

\[
\frac{16}{9}-\frac34 r^2\Bigl(1-\frac r4\Bigr)
=
\frac{(3r+4)(3r-8)^2}{144}\ge0.
\]

This is an upper bound. Attainment and optimality are not asserted.
The field \(w=(\sin y,\sin z,\sin x)\) gives \(E=3/2\), twelve
nonzero output coefficients on \(\beta=2\), and squared output norm
\(3/4\). Rechecked here.

\[
|A^{1/2}B_{\mathrm{equal}}(u,u)|_2\le 2\sqrt{XY}.
\tag{10}
\]

Regrouping repeated-radius receiver choices:

\[
\boxed{
|\mathcal T_{\mathrm{rep}}(u)|\le\frac{\sqrt3}{2}X\sqrt Y.
}
\tag{11}
\]

The output \(b\) of equal inputs \(a\) is even, since
\(b=2a+2p\cdot q\). After (6),

\[
\sum_{\substack{2\le b\le 4a\\ b\ \mathrm{even}}}
(b-a)^2\Bigl(1-\frac b{4a}\Bigr)
=
a^3-\frac{a^2}{2}.
\]

Weighted Cauchy–Schwarz then uses \(\sum a^{3/2}E_a\le\sqrt{XY}\).
Arithmetic is carried through the correct weighted expression. It is
not an unweighted count substituted into a different operator.
Rechecked in sympy.

---

## What is lost

| Operation | What is lost, or what remains to be proved |
|---|---|
| Replace a complex coefficient by its magnitude | Relative phase and vector alignment disappear. |
| Bound each receiver orientation separately | Energy redistribution and radius-difference cancellation disappear. |
| Replace exact radii by a thick annulus | Exact equality, parity and the fixed-sphere incidence geometry no longer give the same estimate. |
| Apply separate Cauchy–Schwarz bounds at each output \(k\) | Shared input coefficients and simultaneous incidence must still be controlled when summing \(k\). |
| Count admissible integer triangles | Coefficient weights, signs, concentration and sharing remain unspecified. |
| Estimate each fixed distinct-radius triple | The simultaneous sum over all such triples is still required. |
| Infer future behavior from one field | Generated modes, changing amplitudes, polarization and nonlinear forcing remain unaccounted for. |
| Integrate a signed derivative inside a positive part | Bounded endpoints do not control repeated positive contributions or total variation. |

The older thick-shell obstruction is not a defect of the exact-sphere
proof. The source provides an explicit projected-convolution family
with \(Q_{i,i+1}\ge 2^{i/2}/2048\) for the displayed unrestricted
\(\tau=1/2\) low-high quotient. That proof retains the original
\(H^1\times H^2\) denominator. It prevents replacing that operator’s
dense assembly factor by the proposed subpower incidence factor. It
does not refute a differently restricted operator, and does not
produce an NS singularity. **No \(W_{ij}\) has been reconstructed
here.**

---

## \(I_3\) specifies integer realizability

\(I_3\) is the ordinary cubic lattice
\((\mathbb Z^3,x_1^2+x_2^2+x_3^2)\). A triangle with prescribed
\(a,b,c\) exists precisely when the binary Gram matrix

\[
G=\begin{pmatrix}a&s\\ s&b\end{pmatrix},
\qquad s=(c-a-b)/2,
\]

has an integer realization \(G=V^TV\) with \(V\) a \(3\times 2\)
integer matrix. The test concerns wavevectors, not velocity
coefficients.

For \(a>0\), \(\Delta=ab-s^2>0\) and integer \(a,b,s\), ordinary
integral representation by \(I_3\) is equivalent to representation
over every \(\mathbb Q_\ell\) and every \(\mathbb Z_\ell\). A finite
criterion is

\[
\boxed{
(a,\Delta)_\ell\,(a,-1)_\ell\,(\Delta,-1)_\ell=1
\quad\text{for every prime }\ell\mid 2a\Delta.
}
\tag{12}
\]

The positive-definite assumption supplies the real-place condition.
Primitive embeddings, prescribed normals, degenerate Grams and
class-group surjectivity are separate questions.

This is an application of classical quadratic-form theory
(Schulze-Pillot, cited local and genus results). It is not a
conclusion drawn from a census alone. The odd-prime enlargement
modifies an abstract lattice in its rational plane. It is not time
evolution of Fourier modes.

Exact regressions recomputed here:

| Gram data \((a,b,s)\) | Local result |
|---|---|
| \((96,96,0)\) | Fails at \(2\) and \(3\) |
| \((2,3,1)\) | Fails at \(2\) and \(5\) |
| \((2,2,-1)\) | Passes all required primes |
| \((14,14,-7)\) | Passes all required primes |

In particular \(a=b=c=\alpha\) forces \(s=-\alpha/2\), so odd
\(\alpha\) cannot support a monochromatic closed triangle. Even
\(\alpha\) is necessary, not sufficient. The old unrestricted
assertion that every proper class of discriminant \(-4\Delta\)
occurs as an orthogonal lattice has been corrected in the prime
note.

For an impossible triple the contribution is identically zero at
every time. For an allowed triple the prime tests impose no
amplitude, polarization, or phase. A successful analytic use must
retain those weights and then control their evolution. The
fixed-sphere weighted lemma and the even-output sum are completed
uses. A universal scalene time estimate is not.

---

## Actual motion

Along full Galerkin NS, \(|k|\le N\),

\[
\dot u_k
=
-\nu|k|^2 u_k
-iP_k\sum_{p+q=k}(q\cdot u_p)u_q.
\tag{13}
\]

The vectors \(p,q,k\) and their arithmetic restrictions remain
fixed. Their coefficients change. Initially zero coefficients can
become nonzero.

Automatic phase rotation cannot be assumed. Purely imaginary
Hermitian coefficients form an invariant real-odd velocity
subspace. With modes \(p=(2,0,0)\), \(q=(0,3,0)\), \(k=(2,3,0)\),
coefficients \(iA e_2\), \(iA e_3\), \(iA e_3\) and conjugates, one
gets \(X=52A^2\), \(Y=532A^2\), \(\mathcal T=24A^3\). At
\(\nu=1\), \(A=24\), \(X'=50688>0\). This disproves a universal
claim that positive transfer must immediately rotate away. It is
not a blowup example.

For a fixed distinct-radius block,

\[
\boxed{
\dot{\mathcal T}_{abc}+\nu(a+b+c)\mathcal T_{abc}
=
\mathcal Q_{abc,N}.
}
\tag{14}
\]

\(\mathcal Q\) is quartic and retains the full nonlinear derivative
in each slot. Inputs are not confined to the displayed triangle or
to the high-frequency projection. A Duhamel denominator
\(1/[\nu(a+b+c)]\) does not by itself bound the total normalized
positive-transfer budget.

---

## The missing implication

\[
h_{K,N}=P_{|k|>K}u_N,
\qquad
\mathcal S_{K,N}(T)
=
\int_0^T
\frac{[\mathcal T_{\mathrm{sc}}(h_{K,N})-\nu Y_N/4]_+}{X_N}\,dt.
\tag{15}
\]

\(\mathcal T_{\mathrm{sc}}\) sums complete triads with three
distinct exact radii. The positive part is taken after this sum and
the specified viscosity subtraction. \(X_N,Y_N\) are moments of the
full field; \(h\) is not autonomous. On the zero trajectory the
integrand is zero.

The controlled complement
\(C=\mathcal T(u_N)-\mathcal T_{\mathrm{sc}}(h)\) obeys

\[
|C|\le 3C_K\sqrt{E_N}\,X_N+\frac{\sqrt3}{2}X_N\sqrt{Y_N},
\qquad
C_K^2=\sum_{0<|k|\le K}|k|^2.
\]

Allocating \(3\nu Y_N/4\) to the repeated-radius term and using
\(E_N'+2\nu X_N=0\) with mean-zero Poincaré,

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
\tag{16}
\]

The missing theorem is

\[
\boxed{
\forall u_0\in C^\infty_{\mathrm{div}},\ \forall\nu>0,\quad
\exists K=K(u_0,\nu)<\infty:\quad
\forall T<\infty,\quad
\sup_N\mathcal S_{K,N}(T)<\infty.
}
\tag{17}
\]

The data, viscosity and \(K\) stay fixed as \(N\) increases. The
bound may depend on the datum and time horizon, but must be
independent of \(N\) and proved without assuming the desired
smoothness bound. Equation (17) would give uniform \(H^1\) control
through (16), then standard continuation and Galerkin limit.
**Equation (17) has not been proved here.**

A fixed absolute squared-radius strip and separated-scale estimates
do not automatically cover the entire all-high scalene sum. A bound
on one episode’s duration does not control its integrated strength
and repetition.

---

## Centered drift remains intact

\[
X=|A^{1/2}u|_2^2,\quad
Y=|Au|_2^2,\quad
Z=|A^{3/2}u|_2^2,\quad
\Lambda=Y/X,
\]
\[
N=-\langle B,Au\rangle_{\mathbb R},\quad
M=-\langle AB,Au\rangle_{\mathbb R},\quad
T_c=M-\Lambda N,
\]
\[
D_s=Z-Y^2/X=\sum_k|k|^2(|k|^2-\Lambda)^2|u_k|^2\ge0,
\]
\[
T_c=-\langle B,A(A-\Lambda)u\rangle_{\mathbb R},
\qquad
\boxed{\Lambda'=\frac2X(T_c-\nu D_s).}
\tag{18}
\]

For a grouped triad with modal transfers \(\tau_j\) summing to zero
and \(w_j=\lambda_j(\lambda_j-\Lambda)\),

\[
\sum_j w_j\tau_j
=
\frac13\sum_{j<l}(w_j-w_l)(\tau_j-\tau_l),
\qquad
w_j-w_l=(\lambda_j-\lambda_l)(\lambda_j+\lambda_l-\Lambda).
\]

This preserves a further exact radial cancellation. It does not
establish the required all-time bound. The old sufficient condition
\(T_c\le\theta\nu D_s+K(t)X\), \(\theta<1\), would imply
\(\Lambda'\le 2K\). Its coefficient must be independently integrable
through a candidate finite endpoint. Defining \(K\) from the unknown
positive remainder does not prove that integrability.

The current scalene criterion (17) and the earlier centered
criterion are **distinct sufficient routes**. Neither is claimed
equivalent to the other. Both locate an unresolved dynamical
estimate beyond the established geometry. Do not splice (17) into
DA-NS-2.

---

## Evidence statuses

| Status | Examples | Permitted conclusion |
|---|---|---|
| Exact algebra and working analytic estimates | (1)–(14), (16), (18), the scoped prime criterion (12) | Retain with their hypotheses. |
| Exact finite computations | Transfers \(0,+24,-24\); generated mode; twelve shear coefficients; prime regressions | Check conventions; demonstrate particular configurations. |
| Numerical evolution | Fixed-data positive-budget episodes at \(N^2=6,12,20\) | Those computed trajectories only. |
| Illustrative motion | Moving triangles, animated arrows, rendered tubes | Explanation only unless tied to specified computed variables. |

The current fixed-data report gives \(\mathcal S(1)\) approximately
\(0.001337845\), \(0.046918627\) and \(0.072599898\) at squared
cutoffs \(6,12,20\), with \(\nu=3/2\) and \(K=1\). These are
reported trajectory computations, **not rerun** in this audit.
Three cutoffs establish neither uniform boundedness nor divergence.

The next required proof is a bound on the summed, normalized,
positive scalene transfer along the actual NS evolution. It must
account for amplitude, alignment, generated modes, forcing, and
repeated episodes. Existence of the Fourier triangles and the
identities governing each interaction remain usable inputs to that
proof.

**NS not solved.**

24 September 2026 Heavy board (exit code 1; G1.(1) failed closed for
missing DA script): [`FOURIER-TRIANGLES-HEAVY-BOARD-2026-09-24.md`](FOURIER-TRIANGLES-HEAVY-BOARD-2026-09-24.md).
Equation (1) DA script: [`scripts/fourier_triangle_eq1_S_pq.py`](../scripts/fourier_triangle_eq1_S_pq.py).
α=98 / 432 is **not** computed. L1 / BOTH SIGNS and (17) stay **OPEN**.
