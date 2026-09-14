> **Transfer note (14 September 2026).** Inverse-GCD arithmetic only.
> **Not** live Domain Architect. Clay is **NOT CLAIMED.** This does **not**
> prove the Riemann hypothesis. Do **not** import into `domain_architect/`.
> Do **not** paste compact SFE \(\Delta[(P\cdot H\cdot\psi)^2\lambda]=\Phi\)
> into this book. Do **not** glue Möbius–GCD \(Q_N=\mu(\gcd)/\gcd\) (that
> RH bridge is a **NO-GO**). Letters collide: Q6 \(H_N\) \(\neq\) Paper2
> \(H_N[a]\) \(\neq\) FRA \(H\).

# Q6 \(\to\) Mertens transfer — still OPEN

**Tried.** Locked the August inverse-GCD matrix, ran the June 8 Gap 1
trial, and compared it to a catalog equivalent of RH. The arrow does
**not** close. A visible gap is kept.

Control: [`GAP1_RECONCILIATION_HANDOFF.RECEIPT.md`](GAP1_RECONCILIATION_HANDOFF.RECEIPT.md)
already rejected “RH follows” / “95% complete.” This note is the
calculation behind that rejection, not a replacement close.

Public Q6 face: [`04_q6_inverse_gcd.pdf`](04_q6_inverse_gcd.pdf).
What still stands there: definitions, Bridge\* on a single prime pair,
nonnegative cone. Full-spectrum \(\lambda_{\min}>-1/2\) stays **false**.

Probe: [`q6_mertens_bridge.py`](q6_mertens_bridge.py).

---

## 1. What “the transfer” would have to be

Littlewood: RH \(\Leftrightarrow\) \(M(x)=O(x^{1/2+\varepsilon})\) for every
\(\varepsilon>0\), where \(M(x)=\sum_{n\le x}\mu(n)\).

A transfer lemma is a proved identity or inequality that turns a
**spectral** fact about one locked matrix into that bound (or into
\(\sum_{n\le x}\mu(n)/n=O(x^{-1/2+\varepsilon})\), which is the same
catalog).

Writing a field equation does not write that lemma. Neither does a
numeric table of \(\lambda_{\min}/\log N\).

---

## 2. Locked operator

August \(\widetilde Q_N\):

\[
\widetilde Q_N(i,j)=\frac{1}{\gcd(i,j)\sqrt{ij}},\qquad 1\le i,j\le N.
\]

Every entry is **positive**. \(\widetilde Q_N(1,1)=1\), not \(M(N)\).

Gap 1 Operator B (different matrix):

\[
Q_N^{(B)}(i,j)=\mu(i/g)\mu(j/g)\,g/\sqrt{ij},\qquad g=\gcd(i,j).
\]

Frobenius \(\|\widetilde Q_{30}-Q_{30}^{(B)}\|_F\approx 9.054\), matching
the handoff’s \(9.05\). They are **not** the same operator. Same
spectral limit is a **task**, not a theorem.

---

## 3. A transfer that already exists — on a different matrix

Cardinal (2008), arXiv:0811.3701: a symmetric matrix \(\mathcal{M}_n\)
with \(M(n)\) as an entry, hence

\[
|M(n)|\le \|\mathcal{M}_n\|.
\]

So \(\|\mathcal{M}_n\|=O(n^{1/2+\varepsilon})\) would imply RH. That is a
real transfer because Mertens is **built into the matrix**. Lagarias–
Montague later gave a Frobenius-norm **equivalence**. The bound on
Cardinal’s \(\|\mathcal{M}_n\|\) is still a conjecture.

\(\widetilde Q_N\) is not Cardinal’s matrix. It is not Redheffer’s
matrix (where \(\det R_n=M(n)\)). The Cardinal/Redheffer arrow does
**not** copy onto inverse-GCD.

---

## 4. Proved obstructions on the locked matrix

**4.1 One-sided Rayleigh.** For any \(v\neq 0\),

\[
\lambda_{\min}(\widetilde Q_N)\le R(v):=\frac{v^\top\widetilde Q_N v}{\|v\|_2^2}.
\]

A trial vector can only **upper-bound** \(\lambda_{\min}\). It cannot,
by itself, force \(M(x)=O(x^{1/2+\varepsilon})\).

**4.2 Positive cone (already Theorem 4.1 in the August PDF).** If
\(v_i\ge 0\) for all \(i\), then \(v^\top\widetilde Q_N v\ge 0\). In
particular the Gap 1 length \(\|v_{\mathrm{alt}}\|^2\sim\log N\) vector
\(v_i=1/\sqrt{i}\) has **positive** Rayleigh on \(\widetilde Q_N\):

| \(N\) | \(R(1/\sqrt{i})\) on \(\widetilde Q_N\) | \(-\log N/(2\pi)\) |
|---|---|---|
| 30 | \(+3.40\) | \(-0.54\) |
| 100 | \(+4.30\) | \(-0.73\) |
| 300 | \(+5.12\) | \(-0.91\) |

Wrong sign, wrong size, wrong direction. That trial **cannot** be the
Gap 1 display \(\langle\hat v,Q\hat v\rangle\to-\log N/(2\pi)\) on the
locked operator.

**4.3 Written Step F sum has the wrong sign.** The handoff’s Task 2
formula

\[
U(N)=\frac{36}{\pi^4}\sum_{\substack{d\le N\\ \mu(d)^2=1}}\frac{(\log N-\log d)^2}{d}
\]

is a sum of squares. \(U(N)>0\) for \(N\ge 2\). At \(N=100\),
\(U(100)\approx 14.81\), while \(-\log 100/(2\pi)\approx-0.73\). The
handoff already flagged \(2\pi\) vs \(\pi^2\). The written main term
cannot equal the claimed negative target.

On Operator B, the same unsigned trial still has **positive** Rayleigh
(\(\approx +0.069\) at \(N=100\)), not \(-\log N/(2\pi)\).

**4.4 Ground state is not Möbius (numeric, \(N\le 300\)).** The bottom
eigenvector of \(\widetilde Q_N\) has correlation \(\approx 0.02\) with
\(\mu(i)/\sqrt{i}\) at \(N=100\), and about half its coordinates are
negative. Möbius-weighted Rayleigh on \(\widetilde Q_N\) sits near \(0\),
not near \(\lambda_{\min}\approx-0.74\). Inserting \(\mu\) by hand into a
trial vector **rewrites** Mertens sums; it does not read them off the
spectrum.

---

## 5. What the \(\lambda_{\min}/\log N\) table is

On \(\widetilde Q_N\), \(\lambda_{\min}/\log N\) sits near \(-1/(2\pi)\approx-0.159\)
for \(N\le 300\) (e.g. \(N=200\) gives \(\approx-0.1594\)). That is the
handoff’s numeric table. It is **not** a theorem. It is **not**
Littlewood’s bound on \(M(x)\). Fujii / \(N(T)\sim T\log T/(2\pi)\) can
put a \(2\pi\) in a **main term** without RH. An RH close needs an
**error term** of quality \(x^{1/2+\varepsilon}\), not the existence of a
\(2\pi\).

Even if \(\lambda_{\min}(\widetilde Q_N)\sim -(\log N)/(2\pi)\) were later
proved unconditionally, that would be a prime-number-theorem-scale
statement unless a second lemma turns the **remainder** into Mertens.
The June 8 biconditional-then-close slogan stays **rejected**.

---

## 6. What remains OPEN

1. A map \(T\) from a spectral quantity of **this** \(\widetilde Q_N\)
   (no \(\mu\) inserted by hand) to \(M(x)\) or \(\sum\mu(n)/n\), with an
   inequality strong enough for Littlewood. No \(T\), no transfer.
2. Identification of the bottom eigenvector of \(\widetilde Q_N\) with a
   Möbius trial. Numerics through \(N=300\) are against it.
3. The Gap 1 Fujii remainder (Step F) as a 10–20 line close. The written
   display is the wrong sign. Do **not** invent a closure.
4. Operator A and Operator B having the same spectral limit.

Parked, not claimed. Clay **NOT CLAIMED.**

---

## 7. What this is not

- **Not** Cardinal \(\mathcal{M}_n\). **Not** Redheffer.
- **Not** the truncated SFE breathing paste. **Not** the 14 August
  harmonic-perspective note as a theorem (that note already said this
  bridge is OPEN).
- **Not** NS. **Not** Goldbach. **Not** live DA.

Usable theory H remains `HN = D^((-1)/2)*Qtilde*D^((-1)/2)`.
