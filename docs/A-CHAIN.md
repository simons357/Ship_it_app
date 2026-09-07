# Augmented NS — completed chain (this PDE)

7 September 2026. Latest Aug NS. \(Q_1\) system. Extra dissipation.
\(\varepsilon>0\), \(\beta\ge 1/2\). Not classical NS.
No \(\Phi\).

**Theorem A sits.** This PDE is closed. Emitting the
chain is not a new close. Uniform \(H^1\) as
\(\varepsilon\to 0\) is a later write on A. Classical
NS is Track B. \(A\Rightarrow B\) stays fail.

Machine write-up: [`A-PROOF-CHAIN.md`](A-PROOF-CHAIN.md).
Long form: [`AUGMENTED-NS-PROOF-CHAIN.md`](AUGMENTED-NS-PROOF-CHAIN.md).
Gap: [`TRACK-A-GAP.md`](TRACK-A-GAP.md).
Paper: [`THEOREM-A-Q1.pdf`](THEOREM-A-Q1.pdf).
LaTeX: [`tex/theorem-a-q1.tex`](../tex/theorem-a-q1.tex).
Deposit: [`THEOREM-A-DEPOSIT.md`](THEOREM-A-DEPOSIT.md),
[`DA-ZENODO-SAY.md`](DA-ZENODO-SAY.md).
B leftover: [`UNAUGMENTED-NS-CHAIN.md`](UNAUGMENTED-NS-CHAIN.md).

This records Ladyzhenskaya / \(p\)-Laplacian
regularity in \(Q_1\) notation (Ladyzhenskaya
1968/1969; Málek–Nečas–Růžička 1996). It is not
a new existence theory.

The **note is yours**. You wrote it. The
**class was already known**: extra stress of
this kind already gives global regularity.
You put that fact in Q1 notation. You did
not invent the class. You do not lose the
write-up. You do not gain a new existence
theory. Cite those papers. Keep your name
on your note.

HB (Harmonic Blueprint) was thrown out as a
unifier. That throw-out stands. The write that
actually sits after that is Theorem A for this
equation. That is a real finish for this PDE.
It is not ordinary NS. Both sentences are true.

---

## Theorem A (sits)

Let \(\nu>0\), \(\varepsilon>0\), \(\alpha>0\),
\(\beta\ge 1/2\), and \(u_0\in H^1(\mathbb{T}^3)\)
divergence-free. The \(Q_1\) system

\[
\partial_t u+(u\cdot\nabla)u
=-\nabla p+\nu\Delta u
+\varepsilon^\alpha\,\mathbb{P}\,\mathrm{div}\bigl(|\nabla u|^\beta\nabla u\bigr),
\qquad
\nabla\cdot u=0
\]

has a unique solution

\[
u\in C^\infty(\mathbb{T}^3\times(0,\infty))\cap L^\infty(0,\infty;H^1).
\]

No finite-time singularity **for this PDE**.
Data need not be axisymmetric.

---

## Have (this PDE is complete)

**(1) The PDE.** Ladyzhenskaya / \(p\)-Laplacian
stress. Write \(p=\beta+2\), so \(\beta\ge 1/2\) is
\(p\ge 5/2\). Not the scalar
\(-\varepsilon^\alpha|\nabla u|^\beta\Delta u\).
Not classical NS. No \(\Phi\).

**(2) Energy.** Test against \(u\):

\[
\frac12\frac{d}{dt}\|u\|_2^2
+\nu\|\nabla u\|_2^2
+\varepsilon^\alpha\|\nabla u\|_{L^{\beta+2}}^{\beta+2}
=0.
\]

**(3) Galerkin.** Finite Stokes modes, same energy,
no blowup of \(\|u_n\|_2\). Weak limit is a weak
solution (Minty–Browder on the extra stress).

**(4) \(\beta\ge 1/2\) in 3D.** Extra integrability
of \(\nabla u\) meets Ladyzhenskaya \(p\ge 5/2\).
Unique strong solution in
\(L^\infty_t H^1\cap L^2_t H^2\). The constant
depends on \(\varepsilon\) and blows up as
\(\varepsilon\to 0\).

**(5) Bootstrap.** Frozen \(\varepsilon>0\),
uniformly elliptic Stokes. Difference quotients
to \(H^k\), then \(C^\infty\).

**(6) Theorem A.** Unique
\(u\in C^\infty(\mathbb{T}^3\times(0,\infty))\cap L^\infty_t H^1\)
at \(\varepsilon>0\), \(\beta\ge 1/2\). This PDE
is closed.

---

## Later write on A — not needed for Theorem A

**(7)** \(\|u\|_{H^1}\le C\) with \(C\) independent
of \(\varepsilon\), for all smooth divergence-free
\(H^1\) data, or a named obstruction that \(C\)
must blow up. A decaying \(Q_1\) integral is not
that bound (A9).

If (7) sits, **(8) Uniform Lemma 4** follows.
**(9) Still not B.** Classical NS is a separate
write: integrable \(\mathcal{R}\) on the unaugmented
equation. Keep \(1/r^4\). No \(Q_1\).

---

## What this is / is not

**Is:** global regularity for the \(Q_1\)-augmented
equation at \(\varepsilon>0\).

**Is not:** unaugmented Navier–Stokes. Uniform
\(H^1\) as \(\varepsilon\to 0\). A certificate
for weather, engines, or leftover (6) on B.

Do not submit A as B. Do not hope a reader
overlooks \(\varepsilon\).

---

## Status

- (1)–(6) Theorem A: **done**
- (7) uniform \(H^1\): **not done**
- (8): waiting on (7)
- (9) / Track B: separate leftover; still open
