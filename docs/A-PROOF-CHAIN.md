# Proof chain — \(Q_1\)-augmented Navier–Stokes (Track A)

Aimed at global regularity **for this PDE**. Extra
dissipation. \(\varepsilon>0\), \(\beta\ge 1/2\).
Not classical NS. No \(\Phi\).

Say to DA: `python3 scripts/da_machine.py proof --problem A`  
or: `next --ask "track A write"`  
or both: `next --ask "Track B please write. track A write as well"`

Long form: [`AUGMENTED-NS-PROOF-CHAIN.md`](AUGMENTED-NS-PROOF-CHAIN.md).  
Gap: [`TRACK-A-GAP.md`](TRACK-A-GAP.md).  
Pretty LaTeX: [`tex/theorem-a-q1.tex`](../tex/theorem-a-q1.tex).  
Paper PDF: [`THEOREM-A-Q1.pdf`](THEOREM-A-Q1.pdf).  
Deposit: [`THEOREM-A-DEPOSIT.md`](THEOREM-A-DEPOSIT.md).  
After Continue: [`DA-AFTER-CONTINUE.md`](DA-AFTER-CONTINUE.md).  
Classical leftover is the other note: [`NS-PROOF-CHAIN.md`](NS-PROOF-CHAIN.md).

---

## Theorem A (this PDE — sits)

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

---

## Proof

**(1)** **The PDE.** Ladyzhenskaya / \(p\)-Laplacian
stress. Write \(p=\beta+2\), so \(\beta\ge 1/2\) is
\(p\ge 5/2\). Not the scalar \(-\varepsilon^\alpha|\nabla u|^\beta\Delta u\).
Not classical NS. No \(\Phi\).
*[have]*

**(2)** **Energy.** Test against \(u\):

\[
\frac12\frac{d}{dt}\|u\|_2^2
+\nu\|\nabla u\|_2^2
+\varepsilon^\alpha\|\nabla u\|_{L^{\beta+2}}^{\beta+2}
=0.
\]

*[have]*

**(3)** **Galerkin.** Finite Stokes modes, same energy,
no blowup of \(\|u_n\|_2\). Weak limit is a weak
solution (Minty–Browder on the extra stress).
*[have]*

**(4)** **\(\beta\ge 1/2\) in 3D.** Extra integrability
of \(\nabla u\) meets Ladyzhenskaya \(p\ge 5/2\). Unique
strong solution in \(L^\infty_t H^1\cap L^2_t H^2\).
The constant depends on \(\varepsilon\) and blows up as
\(\varepsilon\to 0\).
*[have]*

**(5)** **Bootstrap.** Frozen \(\varepsilon>0\),
uniformly elliptic Stokes. Difference quotients to
\(H^k\), then \(C^\infty\).
*[have]*

**(6)** **Theorem A.** Unique
\(u\in C^\infty(\mathbb{T}^3\times(0,\infty))\cap L^\infty_t H^1\)
at \(\varepsilon>0\), \(\beta\ge 1/2\). This PDE is
closed. Data need not be axisymmetric.
*[have]*

**(7)** **Write.** \(\|u\|_{H^1}\le C\) with \(C\)
independent of \(\varepsilon\), for all smooth
divergence-free \(H^1\) data, or a named obstruction
that \(C\) must blow up. A decaying \(Q_1\) integral
is not that bound (A9).
*[the next write]*

**(8)** **Uniform Lemma 4.** From (4) and (7), the
\(H^1\) bound stays finite as \(\varepsilon\to 0\).
*[follows from (7)]*

**(9)** **Still not B.** If (7) sits you have a
uniform bound on this family. Classical NS is a
separate Track B write (integrable \(\mathcal{R}\)).
\(A\Rightarrow B\) stays fail.
*[follows from (7); does not close B]*

Theorem A already sits. Emitting the chain is not a
new close of this PDE. (7) is the remaining write.
If (7) sits, (8) follows. (9) still sends classical
NS to Track B.

---

## Candidates for (7)

Classify one:

- \(\|u\|_{H^1}\le C\) independent of \(\varepsilon\)
- a named obstruction that \(C\) must blow up
- not a decaying \(Q_1\) integral
- not \(\Phi\), not a slide onto B

Machine: [`DA-PROOF.md`](DA-PROOF.md)  
Catalog: [`TRACK-A-LEMMAS.md`](TRACK-A-LEMMAS.md)  
Attempt: [`DA-ATTEMPT.md`](DA-ATTEMPT.md)
