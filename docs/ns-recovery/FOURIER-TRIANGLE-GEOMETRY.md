# Fourier-triangle geometry — reconstruction

**20 September 2026.** Identities sit. No new proof.
The centered equation stays

\[
\Lambda'=-\frac{2\nu}{X}D_s+\frac{2}{X}T_c.
\]

Ordinary NS is not solved. Soft X silent.

Defs: [`../math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](../math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
Centered equation: [`CENTERED-EQUATION.md`](CENTERED-EQUATION.md).
Need★ (two-shell, unwritten): `origin/cursor/unaug-ns-unified-status-a7a2:docs/NEED-STAR-HH-L-DUAL.md`.

Three buckets below. Do not mix them.

---

## 0. The triangle and the kernel \(I_3\)

A Fourier triangle is an ordered lattice triple with

\[
p+q=k,\qquad p,q,k\in\mathbb Z^3\setminus\{0\}.
\]

Equivalently \(p+q+r=0\) with \(r=-k\). Shell placement is by eigenvalues
\(\lambda_p=|p|^2\), \(\lambda_q=|q|^2\), \(\lambda_k=|k|^2\).

The per-triangle signed transfer already used in the evaluator is

\[
I_3(p,q;k)
:=
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

Keep \(\mathrm{Im}\). Do not replace it by an absolute value.

---

## I. Exact identities

### Shells, polarizations, Leray

Mean-zero, divergence-free, reality:

\[
k\cdot v_k=0,\qquad v_{-k}=\overline{v_k}.
\]

Two complex transverse polarizations at each \(k\neq 0\). Leray

\[
P_k=I-\frac{k\otimes k}{|k|^2},\qquad
\widehat B_k=i\,P_k\sum_{p+q=k}(q\cdot v_p)v_q.
\]

Incompressibility at \(p\) gives, for every triangle (equal or not),

\[
p\cdot v_p=0
\qquad\Rightarrow\qquad
q\cdot v_p=(k-p)\cdot v_p=k\cdot v_p.
\]

So the live bilinear is \(i\,P_k\sum(k\cdot v_p)v_q\). Against a
divergence-free \(v_k\), \(P_k^*v_k=v_k\), and

\[
T_k=-\mathrm{Re}(\widehat B_k\cdot\overline{v_k})
=\sum_{p+q=k}I_3(p,q;k).
\]

Ordered convolution is half the symmetrization, complex coefficients
allowed:

\[
\sum_{p+q=k}(q\cdot v_p)v_q
=
\frac12\sum_{p+q=k}\bigl[(q\cdot v_p)v_q+(p\cdot v_q)v_p\bigr].
\]

### Equal-length cancellation

On an exact input shell \(\lambda_p=\lambda_q=\alpha\), output
\(\lambda_k=\beta\le 4\alpha\):

\[
k\cdot p=k\cdot q=\frac\beta2,
\qquad
|k_\perp|^2=\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr),
\]

where \(k_\parallel=(\beta/(2\alpha))p\) and \(k_\perp\perp p\). Then
\(k\cdot v_p=k_\perp\cdot v_p\) and

\[
|k\cdot v_p|
\le
\sqrt{\beta\bigl(1-\beta/(4\alpha)\bigr)}\,|v_p|.
\]

At \(\beta=4\alpha\) the pairs are collinear, \(k_\perp=0\), and those
contributions vanish. No division by \(1-\beta/(4\alpha)\).

Counting on a fixed output: \(q=k-p\), at most one partner per input.
Two-shell gap-cancel (exactly two eigenvalues \(\alpha>\beta\)):

\[
T_\alpha+T_\beta=0,
\qquad
T_c=(\alpha-\beta)\frac{\alpha\beta E}{X}T_\alpha
=-(\alpha-\beta)\frac{\alpha\beta E}{X}T_\beta,
\]

\[
D_s=\frac{\alpha\beta(\alpha-\beta)^2 e_\alpha e_\beta}{X}.
\]

When \(T_c>0\), the gap drops from \(\mathcal R_\star\):

\[
\mathcal R_\star=\frac{\alpha\beta E\,T_\beta^2}{X\,e_\alpha e_\beta Y}.
\]

### Unequal-length defect

If \(\lambda_p\neq\lambda_q\), then \(k\cdot p\neq\beta/2\) in general:

\[
k\cdot p=\lambda_p+p\cdot q,
\qquad
|k_{\perp p}|^2=\lambda_k-\frac{(k\cdot p)^2}{\lambda_p}.
\]

The equal-length factor \(1-\beta/(4\alpha)\) is **unavailable**.
The identity \(q\cdot v_p=k\cdot v_p\) still holds. The size control
does not.

### Phase-dependent signed transfer

\(I_3\) is odd in the field: \(I_3(-v)=-I_3(v)\). Homogeneous of degree
three. A global phase on one leg rotates the \(\mathrm{Im}\). The complete
sum

\[
T_c=\sum_{p+q=k}\lambda_k(\lambda_k-\Lambda)\,I_3(p,q;k)
\]

is the only object that enters the centered equation. An HH→L split
identifies a channel; it is not a replacement for the complete sum.

### Centered equation (not an estimate)

\[
\Lambda'=-\frac{2\nu}{X}D_s+\frac{2}{X}T_c.
\]

If a remainder \(T_c\le\theta\nu D_s+KX\) with \(\theta<1\) sat, then
\(\Lambda'\le 2K\). That implication is algebra. The remainder is not
granted.

---

## II. Numerical observations (not identities)

- K=0 form \(T_c\le\theta\nu D_s\): \(\lvert T_c\rvert/D_s\) grows with
  amplitude on a fixed high triad. Dead.
- \(C_*\approx 0.004\) on that one triad is a sample of
  \(T_c/(X^{3/2}\Lambda)\), not a theorem.
- Bony HH fraction: all of \(T_c\) on a pure high triad; random
  p90 \(\approx 0.51\). Channel diagnostic. No bound.
- Growing layer \(v_n\): not exact-shell, aspect 6, eigenvalues
  \(n^2,2n^2,5n^2\) at \(j=0\), \(N=0\), evaluator
  \(T_c=3n^5(3n^2+3n+1)\) for \(n=1\ldots 8\),
  \(\mathcal R_\star\gtrsim n/165888\to\infty\). Instantaneous class,
  not a trajectory.
- Need★ machine, seed 1390, aligned HH→L closers \((\alpha,\beta)=(5,4)\),
  \((9,4)\): gap-cancel residual \(10^{-16}\); printed
  \(\mathcal N_\star\approx 0.099\). Sample. Not Need★.
- Unsigned CS \(\lvert T_\beta\rvert\le\sqrt{\beta}\,E\sqrt{s\,e_\beta}\)
  holds on those fields and hides occupancy \(s\).

---

## III. Illustrative motion (not the PDE)

`high_triad_field` and \(v_n\) are frozen Fourier shapes. They test
instantaneous identities and remainders. They do not solve

\[
\partial_t u+B(u,u)=-\nu Au.
\]

Phases and polarizations on a genuine trajectory move. A cancellation
seen on a snapshot is not a conserved law. Do not animate a triad and
call it \(\Lambda(t)\).

---

## IV. Where the geometry is lost

**1. Inside one output mode.** The sum \(T_k=\sum_{p+q=k}I_3\) adds
triangles that do not share a single \(k_\perp\). Equal-length
\(|k_\perp|\) control is per pair. Passing to \(\lvert T_k\rvert\le
\sqrt{\lambda_k}\,E\,\lvert v_k\rvert\) (or occupancy \(s\)) throws away
sign, phase, and the \(k_\perp\) direction.

**2. Across output modes.** \(T_c=\sum_k\lambda_k(\lambda_k-\Lambda)T_k\)
keeps the centering weight. It does not keep a common polarization.
Unequal-length triangles (the \(v_n\) support) never had the
\(1-\beta/(4\alpha)\) factor to begin with.

**3. Under time evolution.** The centered equation needs a bound on the
**sum** \(T_c(t)\), not on one triangle. Instantaneous \(I_3(t)\) is
recomputed from the current field. No written law carries
equal-length cancellation, phase, or \(k_\perp\) from time \(t\) to
\(t+dt\).

Loss point, precisely: the map

\[
\bigl\{I_3(p,q;k)\bigr\}
\;\longrightarrow\;
T_c
=\sum_{p+q=k}\lambda_k(\lambda_k-\Lambda)\,I_3(p,q;k)
\]

is exact, but every **size** estimate used after that sum is either
unsigned (occupancy) or a uniform \(C\) on \(T_c/\sqrt{D_s EY}\)
(false on \(v_n\)).

---

## V. \(I_3\) prime restrictions

“Prime” here means the **principal restrictions already written on
\(I_3\)**. Assessed inside this mechanism only.

| Restriction | Status in the mechanism |
|---|---|
| Div-free / Leray / \(q\cdot v_p=k\cdot v_p\) | **Identity.** Survives the sum against \(v_k\). |
| Reality \(v_{-k}=\overline{v_k}\) | **Identity.** |
| Equal-length \(k_\perp\) and \(\beta\le 4\alpha\) | **Identity on one input shell.** Lost as soon as a second input eigenvalue is live, or as soon as the sum is replaced by unsigned CS. |
| Two-shell gap-cancel | **Identity.** Converts \(T_c\) to \(T_\beta\). Does not bound \(T_\beta\). |
| Exact-shell occupancy / \(K\le 16s\) | **Bound that hides \(s\).** Different object from \(K(t)\). |
| Signed dual Need★ on HH→L | **Unwritten.** The leftover on the two-shell channel. |
| Goldbach prime-pairs \(p+q=k\) with \(p,q\) prime | **Different leftover.** Inverse-GCD Rayleigh on a prime-difference vector. Not a restriction of \(I_3(v)\) and not a bound on \(T_c\). Do not glue. |

The equal-length identities do not restrict the growing-layer support.
The Goldbach prime-pair restriction does not sit inside \(B(u,u)\).

---

## VI. First missing implication to the time-dependent bound

The time-dependent object is already named: keep \(\Lambda(t)\) finite
through the centered equation. Algebra already gives

\[
T_c\le\theta\nu D_s+K(t)X,\quad\theta<1
\qquad\Longrightarrow\qquad
\Lambda'\le 2K.
\]

The **first missing implication** is the step that would feed that
algebra from the triangles:

\[
\boxed{
\sum_{p+q=k}I_3(p,q;k)
\text{ with the identities of §I}
\;\Longrightarrow\;
T_c\le\theta\nu D_s+K(t)X
\text{ with }K\in L^1_{\mathrm{loc}},
\text{ without }H^1/L^\infty/\mathrm{BKM}.
}
\]

On the two-shell HH→L face this is Need★ (either displayed form).
On the full field it is a different sentence; unrestricted uniform
\(C\) in \(T_c\le C\sqrt{D_s EY}\) is false on \(v_n\).

Tautological \(K=(T_c-\theta\nu D_s)_+/X\) is not that implication.

No new estimate is written here.
