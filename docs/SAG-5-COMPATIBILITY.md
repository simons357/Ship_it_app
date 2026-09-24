# SAG-5 — Global Compatibility Defect

24 September 2026.
**A split of the signed-assembly
blank. Not a theorem. Not a
\(T_c\) bound. Not a close.
NS not solved.**

Parent gate:
[`SIGNED-ASSEMBLY-GATE.md`](SIGNED-ASSEMBLY-GATE.md).
Triangle identities:
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md).

Do not stamp a SAG-5 theorem from
a rank calculation alone. That
calculation is **SAG-5A**: a local
fact about one reused polarization.
The signed term still contains the
partner \(v_q\), the output \(v_k\),
Hermitian identifications,
amplitudes, and phases.

Unaugmented NS on \(\mathbb{T}^3\).
No \(Q_1\). No \(\Phi\)-cancel. No
SND. No Theorem H. No Route A weld.
Unrestricted \(\star\) stays
**KILLED**. Claimed \(K\le 16/9\)
stays CLAIMED. Prime masks stay
optional. No occupancy bound on
this page.

\[
\boxed{\text{SAG-5 = GLOBAL COMPATIBILITY DEFECT}}
\]

\[
\boxed{\text{5A: shared-input rank defect}}
\qquad
\boxed{\text{5B: partner/output cocycle compatibility}}
\]

\[
\boxed{\text{NO }|\sum S|\to\sum|S|}
\qquad
\boxed{\text{NO occupancy bound yet}}
\]

---

## What Grok seated, and what it did not

\[
\boxed{\text{one shared input mode does not obstruct two triangles}}
\]

\[
\boxed{\text{one shared input mode can obstruct three or more triangles}}
\]

For \(v_p\in p^\perp\otimes\mathbb{C}\)
there are **four real** degrees of
freedom. The two-triangle coupling
map has enough rank to assign two
complex coupling scalars
independently. Three complex
requirements generically
overdetermine those four real
degrees of freedom.

That is a genuine distinction.
It is **not** the full signed
transfer. The obstruction that can
already appear at two triangles is
the **output / partner
identification**. Rank does not
see it.

Attack 8 is the complementary
direction: fixed-fiber cancellation
worked; global assembly returned a
counting loss. Here individual
triangles can saturate; the
question is whether they can
saturate **simultaneously** once
coefficients are shared. Two sides
of the same assembly problem.
Neither side is an occupancy
envelope.

---

## SAG-5A — shared-input polarization

Fix \(p\in\mathbb{Z}^3\setminus\{0\}\).
Let the triangles through \(p\) be

\[
p+q_j=k_j,
\qquad
j=1,\ldots,d(p).
\]

The relevant linear functionals on
\(v_p\in p^\perp_{\mathbb{C}}\) are

\[
L_j(v_p)=k_j\cdot v_p.
\]

(If \(p\cdot v_p=0\), then
\(k_j\cdot v_p=q_j\cdot v_p=
k_{j,\perp}\cdot v_p\).)

\[
\dim_{\mathbb{R}}p^\perp_{\mathbb{C}}=4,
\qquad
\dim_{\mathbb{C}}p^\perp_{\mathbb{C}}=2.
\]

At most two arbitrary complex
values can generically be imposed
independently. The vector
\((L_1(v_p),\ldots,L_n(v_p))\)
does not range freely through
\(\mathbb{C}^n\) once \(n>2\).

All those values lie in the image
of one map

\[
\boxed{
L_p:p^\perp_{\mathbb{C}}\longrightarrow\mathbb{C}^{d(p)},
\qquad
v_p\mapsto(k_j\cdot v_p)_j.
}
\]

\[
\boxed{\operatorname{rank}_{\mathbb{C}}L_p\le 2.}
\]

This is EXACT. For a high-degree
mode it is a large coherence
defect **on the coupling vector**.
It is not a bound on \(T_c\).

What 5A does **not** prove:

- that \(\Gamma(\mathcal{H})<1\)
  for every two-triangle
  hypergraph (two independent
  complex couplings can still be
  assigned; a frozen \(|v_p|\)
  budget is a different object);
- that three triangles cannot
  saturate a particular signed
  objective (the objective may
  still lie in \(\mathrm{im}\,L_p\));
- partner / output compatibility;
- an occupancy bound;
- a time-dependent \(K(t)\).

---

## SAG-5B — full phase compatibility

The seated signed term is

\[
S_\triangle
=
\mathrm{Im}
\bigl[
(k\cdot v_p)
(v_q\cdot\overline{v_k})
\bigr].
\]

Maximizing every triangle
separately would require
simultaneous compatibility of
three families

\[
v_p,\qquad v_{q_j},\qquad v_{k_j},
\]

one Fourier coefficient per
lattice mode, reused everywhere
that mode appears, plus
\(v_{-m}=\overline{v_m}\) if the
field is real. This is no longer
an occupancy problem. It is a
constrained phase / polarization
network.

The false independent-triangle
envelope is

\[
\sum_\triangle
\lvert G_\Lambda(\triangle)\rvert
\sup_{\text{triangle alone}}
\lvert S_\triangle\rvert.
\]

That replacement

\[
\bigl\lvert\sum S\bigr\rvert
\;\longrightarrow\;
\sum\lvert S\rvert
\]

is **forbidden** on this desk.
It is Loss A with the geometry
and the signs already thrown away.

---

## The coherence-defect ratio

For a finite Fourier-triangle
hypergraph \(\mathcal{H}\),

\[
\boxed{
\Gamma(\mathcal{H})
=
\frac{
\displaystyle
\sup_{\text{globally compatible }\{v_j\perp j\}}
\left|
\sum_{\triangle\in\mathcal{H}}
G_\triangle S_\triangle
\right|
}{
\displaystyle
\sum_{\triangle\in\mathcal{H}}
\lvert G_\triangle\rvert
\sup_{\text{triangle alone}}\lvert S_\triangle\rvert
}
}
\]

with the same frozen amplitudes
in the numerator and in each
one-triangle supremum, and with
\(G_\triangle=\lambda_k(\lambda_k-\Lambda)\)
when the object is \(T_c\), or
\(G_\triangle=1\) when the object
is pure compatibility.

\[
0\le\Gamma(\mathcal{H})\le 1.
\]

The research question, not a
claim:

> Does the shared-mode structure
> of NSE force \(\Gamma(\mathcal{H})\)
> substantially below \(1\) as
> \(\mathcal{H}\) grows?

A single small \(\Gamma\) is not
that statement. A rank bound is
not that statement. \(\Gamma=1\)
on one pair does not kill 5B;
it moves the experiment to the
smallest configuration where
non-independence is guaranteed.

---

## Named two-triangle geometries

Amplitudes frozen at
\(\lvert v_j\rvert=1\) on occupied
modes. First experiment uses
\(G_\triangle=1\). Weighted
\(G_\Lambda\) is a later pass,
not a theorem on this page.
Complex Fourier coefficients;
Hermitian reality is an extra
5B identification, not the
first test.

Independent one-triangle maximum
(EXACT, unit amplitudes, non-
degenerate):

\[
\sup\lvert S_\triangle\rvert
=
\lvert P_{p^\perp}k\rvert.
\]

Reason: \(\max\lvert k\cdot v_p\rvert
=\lvert P_{p^\perp}k\rvert\), and
\(\max\lvert v_q\cdot\overline{v_k}\rvert=1\)
because \(q\times k\) lies in
both planes.

### H2-in — shared input only

\[
p=(2,0,0),
\quad
\triangle_1:\;q=(0,2,0),\;k=(2,2,0),
\quad
\triangle_2:\;q=(0,0,2),\;k=(2,0,2).
\]

\(P_{p^\perp}k_1=(0,2,0)\),
\(P_{p^\perp}k_2=(0,0,2)\),
orthogonal, equal length.
\(\mathrm{rank}_{\mathbb{C}}L_p=2\)
(5A does **not** obstruct the
coupling pair). With free
partners, only the
\(\lvert v_p\rvert=1\) budget
competes:

\[
\rho_2^{\mathrm{in}}
=
\frac{1}{\sqrt{2}}
\qquad\text{EXACT for this }\mathcal{H}.
\]

This is a polarization-budget
ratio, not a partner cocycle,
and not a bound on every
two-triangle graph. If the two
\(k_\perp\) were parallel, 5A
rank would drop to \(1\) and
the budget would **not** split.

### H2-out — shared output (smallest 5B)

\[
k=(0,0,2),
\quad
\triangle_1:\;p=(2,0,0),\;q=(-2,0,2),
\quad
\triangle_2:\;p=(0,2,0),\;q=(0,-2,2).
\]

Inputs are independent. The
shared \(v_k\) cannot align with
both \(q_1\times k=(0,4,0)\) and
\(q_2\times k=(-4,0,0)\). Those
preferred output directions are
orthogonal. Partner phases
cannot absorb a single
\(v_k\) pointing two real ways.

\[
\rho_2^{\mathrm{out}}
=
\frac{1}{\sqrt{2}}
\qquad\text{EXACT for this }\mathcal{H}.
\]

This **is** a two-triangle
coherence defect of type 5B
(output identification). It is
not occupancy. It is not a
uniform \(\Gamma\).

### H2-role — input of one, output of the other

\[
\triangle_1:\;p=(2,0,0),\;q=(0,0,2),\;k=(2,0,2),
\]

\[
\triangle_2:\;r=(1,1,1),\;s=(1,-1,-1),\;p=r+s.
\]

Five distinct modes. \(v_p\) is
the input coupling of
\(\triangle_1\) and the output
of \(\triangle_2\). That is a
role conflict, not a rank
count.

Reduced maximizer (NUMERICAL,
dense grid on \(v_p\); partners
aligned in closed form):

\[
\rho_2^{\mathrm{role}}
\approx 0.942
\qquad\text{on this }\mathcal{H}.
\]

Less of a defect than the
orthogonal output pair, and
still \(\rho_2<1\). Not closed
as a radical. Not a bound on
every role-conflict pair.

### H3-in — three triangles, one input

\[
p=(2,0,0),
\quad
k_1=(2,2,0),\;
k_2=(2,0,2),\;
k_3=(2,2,2)
\]

with \(q_j=k_j-p\). Then
\(L_3=L_1+L_2\), so
\(\mathrm{rank}_{\mathbb{C}}L_p=2<3\).
The coupling vector cannot be
an arbitrary point of
\(\mathbb{C}^3\). For \(G=1\)
and free partners the signed
objective only sees
\(\lvert L_j\rvert\), and the
budget-optimal point still
lies in \(\mathrm{im}\,L_p\):

\[
\rho_3^{\mathrm{in}}
=
2(\sqrt{2}-1)
\qquad\text{EXACT for this }\mathcal{H}.
\]

Rank is real. Rank does **not**
by itself pull this particular
objective below the
polarization budget. That is
why 5A is not the theorem.

---

## Experiment protocol

The frontier is now a
finite-dimensional optimization
on the smallest interacting
Fourier hypergraphs. Not a
sweep. Not 9D.

1. Take the smallest connected
   pair that genuinely shares
   coefficients (H2-out / H2-role,
   not two abstract copies of
   one triad).
2. Freeze amplitudes.
3. Optimize one globally
   consistent phase /
   polarization assignment.
4. Compute

\[
\rho_2
=
\frac{\text{joint signed maximum}}
{\text{sum of independent triangle maxima}}.
\]

5. If \(\rho_2<1\), record a
   **named** two-triangle
   coherence defect (which
   identification: input budget,
   output, role, Hermitian).
   H2-out is that defect for
   output identification:
   \(\rho_2=1/\sqrt{2}\) on that
   \(\mathcal{H}\). Do not
   promote it to
   \(\sup\Gamma<1\).
6. If \(\rho_2=1\), move to the
   smallest three-triangle
   configuration where 5A
   guarantees the coupling
   vector is not free in
   \(\mathbb{C}^3\), and to a
   mixed-weight \(G_\Lambda\)
   pass (the centered scale can
   ask for a point outside
   \(\mathrm{im}\,L_p\)).

Code: `scripts/ns_attacks/sag5_rho2.py`.
Tests: `tests/test_sag5_rho2.py`.

---

## What would count as a write, or a death

A write of SAG-5 is either

1. a signed assembly estimate on
   a **named** class that keeps
   \(k_\perp\), gap-cancel, and
   \(\mathrm{Im}\), with
   \(\Gamma(\mathcal{H})\)
   controlled by a seated
   mechanism, **or**
2. a named death that every
   globally compatible sum
   reintroduces occupancy \(s\)
   or \(\|\nabla u\|_\infty\).

Death conditions inherited from
the parent gate, plus:

- stamping SAG-5 from
  \(\mathrm{rank}_{\mathbb{C}}L_p\le 2\)
  alone;
- replacing
  \(\lvert\sum S\rvert\) by
  \(\sum\lvert S\rvert\)
  and calling the ratio a
  bound on \(T_c\);
- cashing \(\rho_2=1/\sqrt{2}\)
  on one orthogonal pair as
  \(C_0\) or as \(16/9\);
- restoring unrestricted
  \(\star\);
- jumping to
  \(\int K(t)\,dt<\infty\).

---

## Lock

5A: \(\mathrm{rank}_{\mathbb{C}}L_p\le 2\) EXACT.
Two complex couplings generically free.
Three or more generically not.
5B: the signed term is a
phase / polarization network on
shared \(v_p,v_q,v_k\).
\(\Gamma(\mathcal{H})\in[0,1]\) is
the object. The growth question
is OPEN.

H2-in and H2-out orthogonal
pairs: \(\rho_2=1/\sqrt{2}\)
EXACT on those \(\mathcal{H}\).
H3-in: \(\rho_3=2(\sqrt{2}-1)\)
EXACT on that \(\mathcal{H}\);
rank idle for \(G=1\).
Not a uniform bound.
Not occupancy.
Not Gate 5.
Not a close.

\[
\boxed{\text{SAG-5 = GLOBAL COMPATIBILITY DEFECT}}
\]

before any \(T_c\) envelope.
Do not use \(\lvert\widehat B_k\rvert\)
early. Do not evolve a bound
that was never written.
NS not solved.
