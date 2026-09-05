# Proof chain — Birch–Swinnerton-Dyer

Aimed at: algebraic rank of \(E(\mathbb{Q})\) equals
analytic rank of \(L(E,s)\), \(\Sha\) finite, leading term.

The operator names the problem. They do not need the chops.

```
python3 scripts/da_machine.py proof --problem BSD
python3 scripts/da_machine.py next --ask "Please write BSD"
python3 scripts/da_machine.py next --ask "BSD proof chain"
```

This desk’s furthest arithmetic paper is inverse-GCD (Q).
That paper is **not** line (6). Theorem P is not BSD.
\(L(E,s)\) is not zeta. Do not glue.

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
*[the next write]*

**(7)** **Then.** If (6) sits, the arithmetic of \(E(\mathbb{Q})\)
is read from \(L(E,s)\). Still not RH. Still not Q.
Still not Goldbach. Still not NS.
*[follows from (6)]*

If (6) sits, (7) is the classical consequence.

---

## Candidates for (6)

Classify one:

- \(r=r_{\mathrm{an}}\) for every \(E/\mathbb{Q}\), including analytic rank \(\ge 2\)
- \(\Sha(E/\mathbb{Q})\) finite for every \(E/\mathbb{Q}\)
- the leading-term formula for every \(E/\mathbb{Q}\)

Do not emit Gross–Zagier / Kolyvagin for ranks \(0\) and \(1\)
as the full write. Do not use Theorem P, Bridge*, or a
\(Q\)-floor. Those are inverse-GCD. Different object.
Do not use a zero of zeta as a zero of \(L(E,s)\).

---

Machine: [`DA-PROOF.md`](DA-PROOF.md)
