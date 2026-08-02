# Bridge\* — proof draft (in progress)

**Operator (locked):**
\[
\tilde Q_N(i,j)=\frac{1}{\gcd(i,j)\sqrt{ij}},\qquad 1\le i,j\le N.
\]

**Goldbach difference vector** (for even \(k\le N\)):
\[
v_k(j)=1_{\mathbb{P}}(j)-1_{\mathbb{P}}(k-j),\qquad j=1,\ldots,N
\]
(with the convention \(1_{\mathbb{P}}(m)=0\) if \(m\notin[1,N]\)).

**Conjecture (Bridge\*).** If \(v_k\not\equiv 0\), then
\[
R_k:=\frac{v_k^\top \tilde Q_N v_k}{\|v_k\|_2^2} \;>\; -\frac12.
\]

**Status:** single-representation case **proved** below; multi-representation case **bounded numerically**, analytic bound in progress.  
**Not claimed:** full \(\lambda_{\min}(\tilde Q_N)>-1/2\) (false).

---

## 1. Expansion

Write \(A=\{j\in[1,N]:j\in\mathbb{P}\}\), \(B=\{j\in[1,N]:k-j\in\mathbb{P}\}\), so \(v_k=1_A-1_B\). Then
\begin{align*}
v_k^\top\tilde Q_N v_k
&=\langle 1_A,\tilde Q_N 1_A\rangle
+\langle 1_B,\tilde Q_N 1_B\rangle
-2\langle 1_A,\tilde Q_N 1_B\rangle.
\end{align*}

For distinct primes \(p,q\), \(\gcd(p,q)=1\), hence
\[
\tilde Q_N(p,q)=\frac{1}{\sqrt{pq}},\qquad
\tilde Q_N(p,p)=\frac{1}{p}.
\]

---

## 2. Theorem — single Goldbach representation (proved)

**Setup.** Suppose the only primes \(p,q\in[1,N]\) with \(p+q=k\) and \(p\neq q\) form one unordered pair \(\{p,q\}\) (and no other \(j\) makes \(v_k(j)\neq 0\) beyond \(\pm\) at \(p,q\)).  
Then (up to ordering) \(v_k=e_p-e_q\), \(\|v_k\|_2^2=2\), and
\begin{align*}
v_k^\top\tilde Q_N v_k
&=\frac1p+\frac1q-\frac{2}{\sqrt{pq}}
=\frac{(\sqrt{q}-\sqrt{p})^2}{pq}\;\ge\;0.
\end{align*}
Therefore
\[
R_k=\frac{(\sqrt{q}-\sqrt{p})^2}{2\,pq}\;\ge\;0\;>\;-\frac12.
\]

**Remark.** This is the clean algebraic cancel — same spirit as Phi-renorm: exact square, no Hardy.

---

## 3. Multi-representation — structure

Let
\[
\mathcal{R}(k)=\{p\in\mathbb{P}:2\le p\le k/2,\;k-p\in\mathbb{P}\}
\]
be the Goldbach partition set (representatives \(p\le k-p\)).  
The vector \(v_k\) is supported on primes in \([1,N]\cap\big(\mathcal{R}(k)\cup(k-\mathcal{R}(k))\big)\) with signs \(+\) on the left summand and \(-\) on the right (and cancellation to \(0\) if a site is both — only possible for \(k=2p\)).

**Twin / multi-pair form.** Index partitions \(p_a\in\mathcal{R}(k)\), \(q_a=k-p_a\). Schematically (when all \(p_a,q_a\) distinct and \(\le N\)):
\[
v=\sum_a(e_{p_a}-e_{q_a}),
\]
and
\begin{align*}
v^\top\tilde Q v
&=\sum_a\Big(\frac1{p_a}+\frac1{q_a}-\frac2{\sqrt{p_a q_a}}\Big)
+\sum_{a\neq b}\Big(
\frac{s_{ab}}{\sqrt{p_a p_b}}
+\frac{s'_{ab}}{\sqrt{q_a q_b}}
-\frac{s''_{ab}}{\sqrt{p_a q_b}}
-\frac{s'''_{ab}}{\sqrt{q_a p_b}}
\Big),
\end{align*}
with signs \(s,\ldots\in\{\pm1\}\) from the indicator algebra.

Diagonal / same-pair blocks are \(\ge 0\) by §2.  
**Cross terms** can push \(R_k\) slightly negative (numeric: worst \(\approx -0.09\) for \(N\le 400\)).

### Target lemma (to prove)

**Lemma (Cross-term control).** There exists an absolute \(c_0<1/2\) such that for all even \(k\le N\),
\[
v_k^\top\tilde Q_N v_k \;\ge\; -c_0\,\|v_k\|_2^2.
\]
In particular Bridge\* holds with room \(1/2-c_0\).

**Numeric evidence:** \(c_0\approx 0.10\) suffices up to \(N=400\) (`scripts/bridge_floor_verify.py`).

**Attack on the lemma:**
1. Bound cross sums by Cauchy–Schwarz in the form  
   \(\big|\sum_{a\neq b}(p_a p_b)^{-1/2}\big|\le \big(\sum_a p_a^{-1/2}\big)^2\) minus diagonal — then compare to \(\|v\|^2\sim \#\mathcal{R}(k)\).  
2. Use Goldbach–Vinogradov / average estimates for \(\sum_{p\in\mathcal{R}(k)}p^{-1/2}\).  
3. Or: write \(\tilde Q=D^{-1/2}QD^{-1/2}\) with \(D=\mathrm{diag}(i)\) and use known indefinite bounds on the *restriction* of \(Q\) to the prime support of \(v_k\) only (much smaller matrix).

---

## 4. SND cone (companion, easy half)

**Proposition (cone, expected).** If \(v\ge 0\), \(\|v\|_2=1\), then \(v^\top\tilde Q_N v\ge 0\).

**Reason:** \(\tilde Q_N(i,j)>0\) all entries; quadratic form on the positive orthant is positive.  
(Strict proof: \(\tilde Q_N=B^\top B\) style after correct factorization of \(1/\gcd\), conjugated by \(D^{-1/2}\), or Gershgorin / positivity of Gram of vectors \(g_d^{1/2}d^{-1/2}1_{d\mid\cdot}\) with care about signs of \(g(d)\).)  
Numeric: nonnegative Rayleigh \(\approx 0^+\) (`bridge_floor_verify` / prior audit).

---

## 5. What this does *not* finish

| Claim | Status |
| --- | --- |
| Bridge\* single-pair | **Proved** (§2) |
| Bridge\* multi-pair | Lemma needed (§3) |
| Full \(\lambda_{\min}(\tilde Q)>-1/2\) | **False** — abandoned |
| NS via H_N, \(\lambda_{\min}(H_N)\ge-3/14\) | **Separate** — need your matrix definition from Claude’s SND file |
| Frame/Riesz gap in SND Thm 1 | **Separate** — Claude flag #3; grab other version |
| Clay large-data | **Not** this note |

---

## 6. Interface to Triple Lock (corrected)

Replace “Bridge: \(\lambda_{\min}(Q_N)>-1/2\)” with:

> **Bridge\*:** \(R_k>-1/2\) for all Goldbach \(v_k\), and \(v^\top\tilde Q v\ge 0\) on the SND cone.

Then re-prove equivalence arrows **only** between SND(cone), GNC(\(v_k\)), and Bridge\* — after §2.1 identity fix in the Unified PDF.

---

## 7. Next concrete steps

1. You: drop `SND_FORMAL_PROOFS.tex` + the file containing **−3/14** / \(H_N(i,j)=\ldots\).  
2. Me: finish Lemma §3 (cross-term control) + wire H_N into NS track.  
3. Joint: one corrected Unified note (Bridge\* language, no false full-spectrum claim).
