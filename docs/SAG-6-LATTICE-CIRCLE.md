# SAG-6 — one output, equal-input lattice circle

24 September 2026.
**A named test of signed assembly
on the full equal-input circle.
Not a \(T_c\) bound. Not a close.
NS not solved.**

Parent:
[`SIGNED-ASSEMBLY-GATE.md`](SIGNED-ASSEMBLY-GATE.md).
SAG-5:
[`SAG-5-COMPATIBILITY.md`](SAG-5-COMPATIBILITY.md).
Identities:
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md).

\[
\boxed{\text{SAG-6: one output }k\text{, full equal-input lattice circle}}
\]

\[
p_j+q_j=k,
\qquad
\lvert p_j\rvert^2=\lvert q_j\rvert^2=\alpha,
\qquad
p_j\cdot k=\frac{\lvert k\rvert^2}{2}.
\]

The centered prefactor
\(\lambda_k(\lambda_k-\Lambda)\)
is a **common** factor on this
circle. It is kept off the sum.
It cannot create vector-sum
depletion by itself.

Unaugmented NS on \(\mathbb{T}^3\).
No \(Q_1\). No \(\Phi\)-cancel. No
SND. No Theorem H. No Route A weld.
Unrestricted \(\star\) stays
**KILLED**. Claimed \(K\le 16/9\)
stays CLAIMED (different
normalization). No occupancy
envelope. No
\(\lvert\sum S\rvert\to\sum\lvert S\rvert\).

---

## The test

Incoming effective vectors in
\(k^\perp\), one globally
compatible divergence-free
field, unit amplitudes:

\[
w_j
=(k\cdot v_{p_j})\,P_k v_{q_j},
\qquad
\Sigma=\sum_j w_j\in k^\perp\otimes\mathbb{C}.
\]

Natural size of one ordered
triangle:

\[
w_{\mathrm{nat}}
=\lvert k_\perp\rvert
=\sqrt{\beta\bigl(1-\beta/(4\alpha)\bigr)}.
\]

\(N=\) number of lattice points
on the circle \(=\) number of
ordered equal-input pairs.

\[
\boxed{
\|\Sigma\|
\stackrel{?}{\lesssim}
N^{1/2}\times w_{\mathrm{nat}}
}
\]

or a comparable gain strong
enough to pay the old half-power
counting loss.

If an aligned legal configuration
destroys that, **mark the
obstruction**. Do not massage it.
If the geometry forces dispersion,
try to turn that into an exact
theorem.

---

## Circle geometry (EXACT)

\(p\cdot k=\beta/2\) is the plane
\((p-k/2)\perp k\). Intersecting
\(\lvert p\rvert^2=\alpha\) gives
a circle

\[
\text{center }=k/2,
\qquad
r^2=\alpha-\beta/4,
\]

in the plane \(k^\perp\), provided
\(\beta\le 4\alpha\). Flat
\(\beta=4\alpha\) is a point:
\(k_\perp=0\), nothing transfers.

The partner \(q=k-p\) is the
antipode: \(q-k/2=-(p-k/2)\).
Hermitian reality identifies this
circle with the conjugate circle
of output \(-k\), not with a
second copy of the same circle
(\(-p\) has \(-p\cdot k=-\beta/2\)).
A real field is legal by setting
\(v_{-m}=\overline{v_m}\). That
does **not** constrain the sum
at this single \(k\).

Write \(p=k/2+r_p\),
\(u_p=P_k v_p\in k^\perp\otimes\mathbb{C}\).
Divergence-free forces

\[
k\cdot v_p
=-2\,r_p\cdot u_p
\]

(bilinear, no conjugate). Then

\[
\Sigma
=\sum_p(-2\,r_p\cdot u_p)\,u_{k-p}.
\]

Grouped by antipodal pairs:

\[
W_{\{p,q\}}
=2\bigl[(u_q\cdot r_p)\,u_p
-(u_p\cdot r_p)\,u_q\bigr].
\]

If \(u_p\parallel u_q\), the pair
cancels.

---

## Alignments that disperse (EXACT)

These legal fields give
\(\Sigma=0\) on every equal-input
circle:

- **constant** \(u_p\equiv e\in k^\perp\);
- **radial / saturating**
  \(u_p\parallel r_p\)
  (the one-mode maximizer of
  \(\lvert k\cdot v_p\rvert\);
  after Leray it is radial in
  the circle plane);
- **tangential** \(u_p\parallel k\times r_p\)
  (then \(k\cdot v_p=0\)).

The geometry **does** kill the
naive “point every \(k_\perp\)
the same way” picture. That is
not yet a theorem that
\(\|\Sigma\|\lesssim N^{1/2}w_{\mathrm{nat}}\).
It is pair cancellation for
fields with \(u_p\parallel u_{k-p}\).

---

## The alignment that does not disperse

Split the circle by a plane in
\(k^\perp\). Choose \(e_1\in k^\perp\)
maximizing \(\sum_p\lvert r_p\cdot e_1\rvert\),
\(e_2=\hat k\times e_1\), and set

\[
u_p
=
\begin{cases}
\mu_p e_1 & r_p\cdot e_1\ge 0,\\
\mu_p e_2 & r_p\cdot e_1<0,
\end{cases}
\]

with \(\mu_p\) scaled so
\(\lvert v_p\rvert=1\). Antipodes
fall in opposite hemispheres, so
\(u_p\not\parallel u_q\).

Unit-length forces

\[
\mu_p^2
=\frac{1}{1+4(u_p\cdot r_p)^2/\beta}
\ge
\frac{\beta}{4\alpha}.
\]

The pair vectors then share a
sign on one component of \(k^\perp\).
Averaging the axis \(e_1\) over
the circle and taking the max
gives the EXACT lower bound

\[
\boxed{
\|\Sigma_{\mathrm{hem}}\|
\ge
\frac{1}{2\pi}\sqrt{\frac{\beta}{\alpha}}\,N\,w_{\mathrm{nat}}.
}
\]

Hence

\[
\boxed{
\frac{\|\Sigma_{\mathrm{hem}}\|}{N^{1/2}\,w_{\mathrm{nat}}}
\ge
\frac{1}{2\pi}\sqrt{N\,\frac{\beta}{\alpha}}.
}
\]

On any family of lattice circles
with \(N\beta/\alpha\to\infty\)
(fat, well-populated circles:
\(\alpha\sim\beta\), \(r_2(\alpha-\beta/4)\)
large) this ratio is
**unbounded**. The \(N^{1/2}\)
test is destroyed.

This is a legal globally
compatible DF field. Hermitian
extension to \(-k\) does not
touch \(\Sigma\) at \(k\).
Phases were not replaced by
absolute values. Occupancy was
not used.

---

## Verdict

\[
\boxed{\text{OBSTRUCTION}}
\]

Aligned lattice-circle
configurations destroy

\(\|\Sigma\|\lesssim N^{1/2}w_{\mathrm{nat}}\).

Do not massage this into a
bound by changing the
normalization after the fact.
The energy-normalized size
\(\|\Sigma\|/E\) with
\(E=\sum\lvert v_p\rvert^2=N\)
is a **different object**. It
is closer to the claimed
one-shell \(16/9\) lane, and
it is not a repair of the test
that was asked.

Naive alignments cancel.
Hemisphere alignment does not.
Both statements sit. The second
one kills the half-power test
on this circle.

---

## Named circles (NUMERICAL check of the EXACT bound)

Code: `scripts/ns_attacks/sag6_lattice_circle.py`.
Tests: `tests/test_sag6_lattice_circle.py`.

Frozen \(\lvert v_j\rvert=1\). \(G_\triangle=1\).

| circle | \(N\) | \(\beta/\alpha\) | hem \(\|\Sigma\|/(N w_{\mathrm{nat}})\) | hem \(\|\Sigma\|/(\sqrt{N} w_{\mathrm{nat}})\) |
|---|---|---|---|---|
| \(k=(0,0,2)\), \(\alpha=6\) | 8 | \(2/3\) | \(0.260>1/(2\pi)\sqrt{\beta/\alpha}\) | \(0.73\) |
| \(k=(0,0,10)\), \(\alpha=90\) | 16 | \(10/9\) | \(0.291\) | \(1.16\) |
| \(k=(0,0,66)\), \(\alpha=2194\) | 32 | \(\sim 2\) | \(0.313\) | \(1.77\) |
| \(k=(0,0,148)\), \(\alpha=11001\) | 48 | \(\sim 2\) | \(0.311\) | \(2.15\) |

The \(N\)-ratio stays a positive
fraction of \(\sqrt{\beta/\alpha}\)
(coherent). The \(\sqrt{N}\)-ratio
grows. Axis-aligned and 3-D tilted
circles show the same pair
cancellation of constant / radial
/ tangential fields.

---

## What this does not reopen

| Object | Status that stays |
|---|---|
| \(N^{1/2}\) depletion on this circle | **KILLED** by hemisphere alignment |
| Claimed \(K\le 16/9\) | **CLAIMED**, other normalization, freeze |
| Unrestricted \(\star\) | **KILLED** by \(v_n\) |
| Need★ | **MISSING** |
| SAG-5A rank | EXACT, local, not this page |
| SAG-5B \(\Gamma(\mathcal H)\) | OPEN as a growth question |
| Occupancy \(K\le 16s\) | not used; not restored |
| Route A / \(\int a_+\) | Parked |

A later write that wants
depletion on this circle must
name a **different** gain
(energy-normalized, mixed
\(G_\Lambda\) across several
outputs, or a restriction that
forbids hemisphere polarization)
and test it on the same
adversarial field. Do not
rename the dead \(N^{1/2}\)
test.

---

## Lock

Circle center \(k/2\), \(r^2=\alpha-\beta/4\),
\(p\cdot k=\beta/2\) EXACT.
\(k\cdot v_p=-2 r_p\cdot u_p\) EXACT.
Constant / radial / tangential
\(\Sigma=0\) EXACT.
Hemisphere
\(\|\Sigma\|\ge(1/(2\pi))\sqrt{\beta/\alpha}\,N\,w_{\mathrm{nat}}\)
EXACT.
\(N^{1/2}\) test **OBSTRUCTED**.
Centered prefactor stays off.
No \(\lvert\widehat B_k\rvert\) early.
No occupancy bound.
NS not solved.
