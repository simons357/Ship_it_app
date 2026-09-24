# SAG-6 — bisector-plane stack

24 September 2026.
**One output. Equal-input circles
stacked in the bisector plane.
Not a \(T_c\) bound. Not a close.
NS not solved.**

Parent:
[`SIGNED-ASSEMBLY-GATE.md`](SIGNED-ASSEMBLY-GATE.md).
SAG-5:
[`SAG-5-COMPATIBILITY.md`](SAG-5-COMPATIBILITY.md).
Identities:
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md).

\[
\boxed{\text{SAG-6A: bisector-plane decomposition — EXACT}}
\]

\[
\boxed{\text{SAG-6B: single-circle arithmetic — sparse; not source of power loss}}
\]

\[
\boxed{\text{SAG-6C: inter-circle compatible alignment — OPEN, then seated}}
\]

\[
\boxed{\text{SAG-6D: scale-decay or coherent-family adversary — DECISIVE}}
\]

Unaugmented NS on \(\mathbb{T}^3\).
No \(Q_1\). No \(\Phi\). No SND. No
Theorem H. No Route A weld.
Unrestricted \(\star\) stays
**KILLED**. Claimed \(K\le 16/9\)
stays CLAIMED. No occupancy
envelope. No
\(\lvert\sum S\rvert\to\sum\lvert S\rvert\).
Do not impose random phase.

---

## SAG-6A — bisector plane (EXACT)

Fix output \(k\), \(\beta=\lvert k\rvert^2\).
Equal-input pairs are

\[
p+q=k,
\qquad
\lvert p\rvert=\lvert q\rvert,
\]

hence

\[
p=\frac{k}{2}+r,
\qquad
q=\frac{k}{2}-r,
\qquad
r\cdot k=0.
\]

On a fixed shell \(\alpha=\lvert p\rvert^2\),

\[
\lvert r\rvert^2
=\alpha-\frac{\beta}{4}.
\]

\[
\boxed{
\text{bisector plane}
=
\bigsqcup_\alpha C_{\alpha,k}.
}
\]

Modulo \(r\leftrightarrow -r\), each
physical triangle is counted once.
The circles partition the
equal-input lattice. They do
**not** share input modes.

The seated one-output object is

\[
\boxed{
T^{\mathrm{eq}}_{c,k}
=
\sum_\alpha
G_\Lambda(\alpha,\beta)\,
W_{\alpha,k}.
}
\]

\(W_{\alpha,k}\) is the signed,
globally compatible vector in
\(k^\perp\) of the **entire**
\(\alpha\)-circle, not its
occupancy:

\[
W_{\alpha,k}
=\sum_{p\in C_{\alpha,k}}
(k\cdot v_p)\,P_k v_{k-p}.
\]

The exact \(T_c\) weight on this
output is

\[
G^{T_c}(\alpha,\beta)
=\beta(\beta-\Lambda).
\]

It does **not** depend on
\(\alpha\). It factors out of
\(\rho_k\). An \(\alpha\)-dependent
\(G\) is a different pairing and
must be named. Default \(\rho_k\)
uses \(G=1\), which is the
\(T_c\) ratio.

---

## SAG-6B — one circle is not the loss

A single \(\alpha\)-circle is
arithmetically sparse
(\(r_2(n)\)). It is not the
source of the old half-power
counting loss.

What still sits on one circle,
from the previous write:

- center \(k/2\), \(r^2=\alpha-\beta/4\),
  \(k\cdot v_p=-2 r_p\cdot u_p\)
  EXACT;
- constant / radial / tangential
  fields: \(\Sigma=0\) EXACT
  (\(u_p\parallel u_{k-p}\));
- hemisphere on one circle:
  \(\|\Sigma\|\ge(1/(2\pi))
  \sqrt{\beta/\alpha}\,N\,w_{\mathrm{nat}}\)
  EXACT;
- intra-circle
  \(\|\Sigma\|\lesssim N^{1/2}
  w_{\mathrm{nat}}\) is
  **OBSTRUCTED**.

That obstruction is real. It is
**not** the assembly loss we were
trying to pay. The meaningful
object is the **stack**.

---

## The estimate that matters

For a cutoff with
\(\alpha\lesssim N^2\),

\[
\boxed{
\rho_k(N)
=
\frac{
\bigl\|
\sum_{\alpha\lesssim N^2}
G_\Lambda(\alpha,\beta)\,W_{\alpha,k}
\bigr\|
}{
\sum_{\alpha\lesssim N^2}
\lvert G_\Lambda(\alpha,\beta)\rvert
\,\|W_{\alpha,k}\|
}.
}
\]

DA’s rule, as asked:

- \(\rho_k(N)\le c<1\) is
  interesting and **nonclosing**;
- the sought mechanism is

\[
\boxed{\rho_k(N)\lesssim N^{-\delta}}
\]

with \(\delta\) large enough,
after matching variables, to pay
the assembly loss.

The objective of this page:

\[
\boxed{
\textbf{Does stacking the lattice circles force increasing angular/phase incompatibility?}
}
\]

The matched adversary:

\[
\boxed{
\textbf{Can we construct bisector-plane families with }
\rho_k(N)\not\to 0?
}
\]

Do not try to prove cancellation
first. Try equally hard to build
the family that defeats it.
Those \(W_{\alpha,k}\) come from
one Fourier field. Compatibility
can help or it can permit
coherent alignment. Solve the
extremal problem. Do not
postulate random phase. Do not
count \(O(N^2)\) bisector points
and write \(\sqrt{\#}\).

---

## Heavy tape (what is kept)

For every unordered \(\{r,-r\}\):

- \(\alpha\), \(r\), \(-r\), \(p\), \(q\);
- projected / transverse direction
  \(k_\perp(p)\);
- triangle-plane normal
  \(p\times q\);
- circle id \(\lvert r\rvert^2\);
- every mode-sharing incidence
  across circles.

Occupancy is stored. Occupancy
is not the remainder.
Code: `scripts/ns_attacks/sag6_bisector.py`.

On every scanned even \(k\),
cross-circle **input** collisions
are **zero**. The only coefficient
shared by every circle is the
output \(v_k\), and that
contraction happens **after**
the vectors \(W_{\alpha,k}\) are
formed. Hermitian reality
identifies the \(k\)-plane with
the \(-k\)-plane, not two
circles of the same \(k\).

---

## SAG-6C — what compatibility actually does

Because the circles partition
the input modes, a field may
be chosen independently on each
circle (DF on that circle, unit
amplitudes) and still be one
globally compatible Fourier
field on the stack.

A **single** global hemisphere
in \(k^\perp\) — one axis
\(e_1\), \(u_p=e_1\) or \(e_2\)
according to \(\mathrm{sign}
(r_p\cdot e_1)\) — is legal on
the whole plane at once.

On that field every circle
vector is parallel:

\[
W_{\alpha,k}
\parallel -e_2
\qquad\text{for all }\alpha
\]

(checked on axis \(k\) and on
tilted even \(k\); \(e_1\)
components cancel, \(e_2\)
components add). Therefore

\[
\rho_k(N)=1
\]

exactly, for the seated
\(G=1\) / \(G^{T_c}\) ratio,
at every cutoff scanned.

Stacking does **not** force
increasing angular
incompatibility. It permits
perfect inter-circle alignment.

SAG-6C is seated as that
fact, not as a decay theorem.

---

## SAG-6D — decisive

\[
\boxed{\rho_k(N)\not\to 0.}
\]

The coherent family exists.
It is not a random-phase
fantasy and not an occupancy
count. \(\rho_k(N)=1\) on

| \(k\) | \(r_{\max}\) | circles | input collisions | \(\rho_k\) |
|---|---|---|---|---|
| \((0,0,2)\) | \(2\ldots 12\) | \(3\ldots 58\) | \(0\) | \(1\) |
| \((0,0,4)\) | \(2\ldots 8\) | \(3\ldots 29\) | \(0\) | \(1\) |
| \((2,2,0)\) | \(2\ldots 8\) | \(4\ldots 33\) | \(0\) | \(1\) |

So

\[
\boxed{
\text{coherence-depletion on the one-}k\text{ equal-input stack}
\text{ is not the missing power.}
}
\]

SAG-5 remains an exact finite
phenomenon. Under the board
rule, \(\rho_2=1/\sqrt{2}\) is
**constant** depletion, hence
not this mechanism.

This branch does **not** earn
another Gate by repairing
\(\rho_k\). A later write that
still wants scale-decay must
change the object:

- several outputs (true mode
  reuse across different \(k\));
- unequal-length pairs;
- an \(\alpha\)-dependent
  signed \(G\) that is actually
  forced by \(T_c\) (the seated
  one is not);
- time evolution (Loss B).

Do not rename the dead
one-\(k\) stack test. Do not
massage \(\rho=1\) into
\(16/9\).

---

## SAG-5 stamp (accepted)

\[
\boxed{
\rho_2
=
\frac{
\sqrt{w_1^2+w_2^2+2w_1w_2\lvert\cos\varphi\rvert}
}{
w_1+w_2
}
}
\]

Orthogonal case
\(\varphi=\pi/2\):
\(\rho_2=1/\sqrt{2}\).
Constant depletion. Not the
sought \(N^{-\delta}\).

---

## Lock

6A EXACT: bisector
\(=\bigsqcup_\alpha C_{\alpha,k}\),
\(p=k/2+r\), \(r\cdot k=0\),
\(r\leftrightarrow -r\) once.
\(G^{T_c}=\beta(\beta-\Lambda)\)
factors out of one \(k\).
6B: one circle sparse; intra-circle
\(N^{1/2}\) still obstructed;
not the old half-power source.
6C: input modes disjoint across
circles; global hemisphere
aligns every \(W_{\alpha,k}\).
6D: \(\rho_k(N)=1\), coherent
family exists, route killed as
a source of missing power.
No occupancy remainder.
No random-phase postulate.
SAG-5 \(\rho_2=1/\sqrt{2}\)
stays exact and finite.
NS not solved.
