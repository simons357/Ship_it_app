# Proof chain — Birch–Swinnerton-Dyer

Aimed at: algebraic rank of \(E(\mathbb{Q})\) equals
analytic rank of \(L(E,s)\), \(\Sha\) finite, leading term.

The operator names the problem. They do not need the chops.

```
python3 scripts/da_machine.py proof --problem BSD
python3 scripts/da_machine.py next --ask "Please write BSD"
python3 scripts/da_machine.py next --ask "BSD proof chain"
python3 scripts/da_machine.py next --ask "spectral framework"
python3 scripts/da_machine.py next --ask "BSD final"
```

Phone file `BSD final.pdf` is not a second public
deposit. The only Simons BSD record on Zenodo is
20552682 (`BSD_SPECTRAL_FRAMEWORK.pdf`). A local
export named “final” is that paper, or a private
draft this VM cannot read. It is not leftover (6).
It is not the Hodge conjecture.

Best paper on this desk: Jonathan Robert Simons,
*The Prime Lattice as a Prototype for the BSD
Hamiltonian* (Zenodo 20552682, 5 Jun 2026;
`BSD_SPECTRAL_FRAMEWORK.pdf`). That paper is **Q**
as a zeta prototype. It is not line (6). The paper
does not prove BSD. Inverse-GCD is not \(L(E,s)\).
Do not glue.

---

## Theorem (aimed)

Let \(E/\mathbb{Q}\) be an elliptic curve. Let
\(r=\operatorname{rank} E(\mathbb{Q})\) and
\(r_{\mathrm{an}}=\operatorname{ord}_{s=1}L(E,s)\).
Then \(r=r_{\mathrm{an}}\), \(\Sha(E/\mathbb{Q})\) is finite, and

\[
\frac{L^{(r)}(E,1)}{r!}
=\frac{\Omega_E\cdot\operatorname{Reg}(E)\cdot\#\Sha(E/\mathbb{Q})\cdot\prod_p c_p}{\#E(\mathbb{Q})_{\mathrm{tors}}^2}.
\]

---

## Proof

**(1)** **Elliptic curve.** \(E/\mathbb{Q}\), Weierstrass
model, conductor \(N\), finite torsion \(E(\mathbb{Q})_{\mathrm{tors}}\).
*[have]*

**(2)** **Mordell–Weil.** \(E(\mathbb{Q})\) is finitely
generated:

\[
E(\mathbb{Q})\cong\mathbb{Z}^r\oplus E(\mathbb{Q})_{\mathrm{tors}}.
\]

\(r\) is the algebraic rank.
*[have]*

**(3)** **Modularity.** Every \(E/\mathbb{Q}\) is modular
(Wiles / Breuil–Conrad–Diamond–Taylor). So
\(L(E,s)=L(f,s)\) for a weight-2 newform: entire, with
functional equation \(s\leftrightarrow 2-s\).
*[have]*

**(4)** **Analytic rank.** \(r_{\mathrm{an}}=\operatorname{ord}_{s=1}L(E,s)\).
The aimed equality is \(r=r_{\mathrm{an}}\).
*[have]*

**(5)** **Low rank.** If \(r_{\mathrm{an}}\in\{0,1\}\), then
\(r=r_{\mathrm{an}}\) and \(\Sha\) is finite (Gross–Zagier /
Kolyvagin; Coates–Wiles for many CM rank-0 cases).
Literature, not a theorem of this desk.
*[have]*

**(6)** **Write.** For every \(E/\mathbb{Q}\): \(r=r_{\mathrm{an}}\),
\(\Sha(E/\mathbb{Q})\) is finite, and the leading-term formula
holds. This includes \(r_{\mathrm{an}}\ge 2\).

The paper’s leftover is the same close under another
name: \(\dim\ker(\hat H_E|_{s=1})=\operatorname{rank}E(\mathbb{Q})\)
for every \(E\), matching the analytic order. Naming
the kernel is not the dimension.
*[the next write]*

**(7)** **Then.** If (6) sits, the arithmetic of \(E(\mathbb{Q})\)
is read from \(L(E,s)\). Still not RH. Still not Q.
Still not Goldbach. Still not NS.
*[follows from (6)]*

If (6) sits, (7) is the classical consequence.

---

## From your best paper (Q, not BSD)

Zenodo 20552682,
[`BSD_SPECTRAL_FRAMEWORK.pdf`](https://doi.org/10.5281/zenodo.20552682).
The paper’s own statement: it does **not** claim to
prove BSD. Honor that.

**Sits as Q / matrix identity.**

- Twisted Möbius:
  \(\hat H_E^{(N)}(i,j)=\mu_E(\gcd(i,j))/\gcd(i,j)\),
  \(\hat H_E=\sum_d \mu_E(d)\,\phi_E(d)/d^2\,P_d^{(N)}\),
  \(\phi_E(d)=d\prod_{p\mid d}(1-a_p/p)\).
- Zeta-prototype dictionary: \(a_p=1\) sends
  \(\hat H_E\) to raw \(Q_N=1/\gcd\). The pole of
  \(\zeta\) at \(s=1\) is the no-zero-mode case of
  that prototype. Consistency of the dictionary,
  not BSD.

**Structural, not a theorem.**

- BSD as
  \(\operatorname{ord}_{s=1}L(E,s)=\dim\ker(\hat H_E|_{s=1})\)
  and that dimension as \(\operatorname{rank}E(\mathbb{Q})\).
- An arithmetic Atiyah–Singer parallel.
- A prototype ladder NS → RH → BSD. Same technique
  is not implication. A is not B. Q is not RH.
  Q is not BSD.

**Open in the paper, still open here.**

- leftover (6)
- \(\dim\ker(\hat H_E)=\operatorname{rank}E(\mathbb{Q})\)
- a rigorous Hilbert-space \(\hat H_E\)
- the spectral floor of \(\hat H_E\)
- the deformation \(H_N\to\hat H_E\)
- an elliptic analogue of GNC

**Withdrawn — do not revive.**

- The paper’s zeta-prototype “proved” block used
  \(\lambda_{\min}(H_N)\to 6/\pi^2-1/2>0\) and
  “\(\lambda_{\min}(H_N)>-1/2\) through \(N=5000\).”
  That is raw \(Q=1/\gcd\). Full
  \(\lambda_{\min}(Q_N)>-1/2\) is **false**
  (\(Q_{10}\approx-1.90\)). Retracted. Möbius does
  not use that floor. The floor does not come back
  because the paper is on the desk.
- Paper \(H_N\) is raw \(1/\gcd\). Desk \(H_N\) is
  \(D^{-1/2}\widetilde Q D^{-1/2}\). Do not mix the
  three matrices.
- GNC (dark-state / prime-indicator difference)
  is withdrawn. It vanishes on an actual Goldbach
  pair. Do not unshelve it to finish BSD.

These are the prototype. They do not give
\(r=r_{\mathrm{an}}\) for every \(E/\mathbb{Q}\).
A GCD matrix is not \(L(E,s)\). Keep them on Q.
Write (6) as BSD.

---

## Candidates for (6)

Classify one:

- \(r=r_{\mathrm{an}}\) for every \(E/\mathbb{Q}\), including analytic rank \(\ge 2\)
- \(\Sha(E/\mathbb{Q})\) finite for every \(E/\mathbb{Q}\)
- the leading-term formula for every \(E/\mathbb{Q}\)
- \(\dim\ker(\hat H_E|_{s=1})=\operatorname{rank}E(\mathbb{Q})\) for every \(E\), matching \(r_{\mathrm{an}}\)

Do not emit Gross–Zagier / Kolyvagin for ranks \(0\) and \(1\)
as the full write. Do not use Theorem P, Bridge*, or a
\(Q\)-floor. Those are inverse-GCD. Different object.
Do not use a zero of zeta as a zero of \(L(E,s)\).
Do not emit 20552682 as QED.
Do not emit a phone file named `BSD final.pdf` as a
second proof. Filename is not the write.

---

## Documented

The operator said they did not prove BSD, and that
if DA could finish leftover (6) they wanted it
written down that DA closed it.

**Documented, 5 September 2026:** DA did **not**
complete leftover (6). DA did **not** close BSD.
The help that sits is the chain above: HAVE (1)–(5),
WRITE (6) still open. A certificate that DA closed
BSD would be a fake last line. That is the refuse.

---

## Not this leftover

| Named | Why not BSD (6) |
|---|---|
| `BSD final.pdf` (phone) | no second public file; same paper or unread private draft |
| Hodge conjecture | different leftover; this PDF is elliptic rank, not Hodge classes |
| Inverse-GCD / \(Q_N\) / \(H_N\) | zeta prototype of \(\hat H_E\), not \(L(E,s)\) |
| GNC | withdrawn |
| NS → RH → BSD ladder | same technique is not implication |

---

Machine: [`DA-PROOF.md`](DA-PROOF.md)
