# Proof chain — Hodge conjecture

Aimed at: every rational Hodge class on a smooth
complex projective variety is algebraic.

The operator names the problem. They do not need the chops.

```
python3 scripts/da_machine.py proof --problem HODGE
python3 scripts/da_machine.py next --ask "Hodge conjecture?"
```

The phone file `BSD final.pdf` is **not** this leftover.
That file is Zenodo 20552682, a BSD zeta-prototype
paper. Elliptic rank is not a Hodge class. Q is not
Hodge. The Hodge Laplacian on this desk (Betti as
\(\dim\ker\Delta\)) is not the Hodge conjecture.

No Simons Hodge paper sits on this desk.

---

## Theorem (aimed)

Let \(X\) be a smooth complex projective variety.
For every integer \(p\ge 0\), every class in

\[
\operatorname{Hdg}^p(X)
=H^{2p}(X,\mathbb{Q})\cap H^{p,p}(X)
\]

is a \(\mathbb{Q}\)-linear combination of classes of
algebraic cycles of codimension \(p\).

---

## Proof

**(1)** **Hodge decomposition.** For compact Kähler
\(X\), \(H^k(X,\mathbb{C})=\bigoplus_{p+q=k}H^{p,q}(X)\).
*[have]*

**(2)** **Hodge classes.**
\(\operatorname{Hdg}^p(X)=H^{2p}(X,\mathbb{Q})\cap H^{p,p}(X)\).
These are the rational \((p,p)\) classes.
*[have]*

**(3)** **Cycle class.** An algebraic cycle of
codimension \(p\) maps to a Hodge class. Algebraic
implies Hodge. The converse is the write.
*[have]*

**(4)** **Lefschetz (1,1).** Every Hodge class of
type \((1,1)\) is algebraic (divisors). \(p=1\) sits.
Literature, not a theorem of this desk.
*[have]*

**(5)** **Special cases.** The conjecture is known
for some abelian varieties, some complete
intersections, and other listed families.
Literature, not a theorem of this desk. The integer
coefficient form is false (Atiyah–Hirzebruch).
The aimed statement is over \(\mathbb{Q}\).
*[have]*

**(6)** **Write.** For every smooth complex
projective \(X\) and every \(p\), every rational
Hodge class is algebraic.
*[the next write]*

**(7)** **Then.** If (6) sits, Hodge classes are
algebraic cycles. Still not BSD. Still not RH.
Still not NS. Still not YM. Still not Q.
*[follows from (6)]*

If (6) sits, (7) is the classical consequence.

---

## Completion

| Lines | Status |
|---|---|
| (1)–(5) | **done** |
| (6) every rational Hodge class algebraic | **not done** |
| (7) | waiting on (6) |

Emit is not a finish.

---

## Candidates for (6)

Classify one:

- every rational Hodge class algebraic, all smooth complex projective \(X\), all \(p\)
- a named obstruction that some Hodge class cannot be algebraic
- not Lefschetz (1,1) reprinted as the full write
- not the Hodge Laplacian \(\to\) Betti on this desk
- not `BSD final.pdf` / 20552682
- not the enclosed SFE letter

---

## Documented

The enclosed letter, *Resolution of the Hodge
Conjecture via the Simons Field Equation (SFE)*,
is **not** leftover (6).

Lemma 1 builds the close into the word
“coherence.” Lemma 2 is the known direction:
algebraic implies Hodge. \(\Delta\Phi=0\) is the
Hodge Laplacian on this desk. That is Betti as
\(\dim\ker\Delta\). It is not an algebraic cycle.

SFE is shelved. Naming SFE is allowed. Emitting
SFE as Hodge is the refuse. Proof C18 **fail**.

**Documented, 5 September 2026:** Hodge leftover
(6) stays open.

---

## Not this leftover

| Named | Why not Hodge (6) |
|---|---|
| `BSD final.pdf` / 20552682 | elliptic \(L(E,s)\), not Hodge classes |
| Inverse-GCD / Theorem P | Q |
| Hodge Laplacian \(\to\) Betti | vocabulary on U, not algebraic cycles |
| Track A / Track B | Navier–Stokes |
| SFE letter (this paste) | shelved; coherence assumes the close; \(\Delta\Phi=0\) is not (6) |
| SFE / Harmonic Blueprint | shelved; SFE coherence is not an algebraic cycle |

Machine: [`DA-PROOF.md`](DA-PROOF.md)  
BSD chain: [`BSD-PROOF-CHAIN.md`](BSD-PROOF-CHAIN.md)
