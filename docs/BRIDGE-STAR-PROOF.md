# Bridge\* — proof draft (corrected)

**Operator (locked):**
\[
\tilde Q_N(i,j)=\frac{1}{\gcd(i,j)\sqrt{ij}},\qquad 1\le i,j\le N.
\]

**Diagonal:** \(\tilde Q_N(p,p)=1/p^2\) (not \(1/p\)).  
**Off-diagonal for distinct primes:** \(\tilde Q_N(p,q)=1/\sqrt{pq}\).

**Working Goldbach test vector** (this note):
\[
v_{p,q}:=e_p-e_q\qquad (p+q=k,\ p\neq q\text{ primes}).
\]
Multi-rep: \(v_k=\sum_{p\in\mathcal{R}(k)}(e_p-e_{k-p})\) over unordered Goldbach partitions.

**Bridge\*.** For every such \(v\not\equiv 0\),
\[
R(v):=\frac{v^\top\tilde Q_N v}{\|v\|_2^2}>-\frac12.
\]

**Status:** single-pair **proved** (§2); multi-rep **proved** (§3).  
**Not claimed:** full \(\lambda_{\min}(\tilde Q_N)>-1/2\) (false).

---

## 0. June 5 definitions that fail (from pasted Unified text)

### 0.1 Paper \(v_k\) vanishes on Goldbach pairs

June 5:
\[
v_k(j)=1_{\mathbb{P}}(j)-1_{\mathbb{P}}(k-j).
\]
If \(p+q=k\) with both prime, then
\[
v_k(p)=1-1=0,\qquad v_k(q)=1-1=0.
\]
So every Goldbach representation is **zeroed out**. Nonzero mass sits only on “half-Goldbach” sites (one side prime, other not). That vector does **not** detect Goldbach pairs.

### 0.2 Dark-state lemma is false as stated

June 5 claims: even \(k\) is Goldbach iff \(v_k\) is not a dark state of \(H_N=Q_N\), via
“\(Q_N(p,q)=1\Rightarrow\langle v,Qv\rangle>0\)”.

For the correct test vector \(v=e_p-e_q\) on **raw** \(Q_N\):
\[
\langle v,Q_N v\rangle=\frac1p+\frac1q-2<0
\]
(e.g. \((3,7)\mapsto -1.52\)). Cross term \(-2\) dominates diagonals \(1/p,1/q\). The claimed sign is wrong; “dark \(\Leftrightarrow\) no Goldbach” does not hold.

**This note** therefore uses \(v_{p,q}=e_p-e_q\) on \(\tilde Q_N\), and Bridge\* as a restricted Rayleigh floor — not the June 5 dark-state iff.

---

## 1. Expansion (single pair)

\[
v^\top\tilde Q_N v
=\tilde Q_N(p,p)+\tilde Q_N(q,q)-2\tilde Q_N(p,q)
=\frac1{p^2}+\frac1{q^2}-\frac{2}{\sqrt{pq}}.
\]
\[
\|v\|_2^2=2,\qquad
R=\frac12\Big(\frac1{p^2}+\frac1{q^2}\Big)-\frac1{\sqrt{pq}}.
\]

(Previous draft wrongly used diagonal \(1/p\) and claimed \(R=(\sqrt q-\sqrt p)^2/(2pq)\ge 0\). That identity is **false** for \(\tilde Q_N\). Numeric: \(R(3,7)\approx -0.152\).)

---

## 2. Theorem — single Goldbach pair **[Proved]**

**Theorem.** For distinct primes \(p,q\),
\[
R(e_p-e_q)=\frac12\Big(\frac1{p^2}+\frac1{q^2}\Big)-\frac1{\sqrt{pq}}\;>\;-\frac12.
\]

**Proof.**
\[
R+\frac12
=\frac12+\frac1{2p^2}+\frac1{2q^2}-\frac1{\sqrt{pq}}
>\frac12-\frac1{\sqrt{pq}}.
\]
Distinct primes ⇒ \(pq\ge 2\cdot 3=6\), hence
\[
\frac1{\sqrt{pq}}\le\frac1{\sqrt6}<\frac12
\]
(\(\sqrt6>2\)). Therefore \(R+1/2>0\). ∎

**Sharpish small case:** \((p,q)=(2,3)\) gives \(R\approx -0.228>-1/2\).

---

## 3. Multi-representation **[Proved]**

Let
\[
\mathcal{R}(k)=\{p\in\mathbb{P}:2\le p<k/2,\;k-p\in\mathbb{P}\}.
\]
Set \(v_k=\sum_{p\in\mathcal{R}(k)}(e_p-e_{k-p})\) (sites \(\le N\)).

### Lemma (cross-term factorization) **[Proved]**

For distinct primes \(p\neq q\), \(r\neq s\),
\[
\widetilde Q(p,r)-\widetilde Q(p,s)-\widetilde Q(q,r)+\widetilde Q(q,s)
=\bigl(p^{-1/2}-q^{-1/2}\bigr)\bigl(r^{-1/2}-s^{-1/2}\bigr).
\]
If \(p<q\) and \(r<s\), the cross term is **strictly positive**.

### Theorem (multi-rep Bridge\*) **[Proved]**

Write \(v_k=\sum_a v_a\) with disjoint pair vectors \(v_a=e_{p_a}-e_{q_a}\), \(p_a<q_a\). Then
\[
v_k^\top\widetilde Q v_k
=\sum_a v_a^\top\widetilde Q v_a
+2\sum_{a<b}v_a^\top\widetilde Q v_b
\ge\sum_a \|v_a\|_2^2 R(v_a),
\]
so \(R(v_k)\ge\min_a R(v_a)>-1/2\) by §2.

**Numeric:** worst multi-rep \(R\) through \(N=200\) coincides with a single-pair case (\(\approx -0.183\) at \(k=8\), pair \((3,5)\)). Richer multi-rep sit higher because of positive crosses.

Formal write-up: `docs/papers/submit/04_q6_inverse_gcd.tex` Theorem (multi-representation).

---

## 4. SND cone (companion)

**Proposition (cone).** If \(v\ge 0\), \(\|v\|_2=1\), then \(v^\top\tilde Q_N v\ge 0\).

All entries of \(\tilde Q_N\) are positive ⇒ quadratic form on the positive orthant is nonnegative.

---

## 5. Status board

| Claim | Status |
| --- | --- |
| Bridge\* single-pair on \(\tilde Q_N\) | **Proved** (§2) |
| Bridge\* multi-pair | **Proved** (§3) |
| June 5 dark-state ↔ Goldbach | **False** (§0) |
| June 5 paper \(v_k\) as Goldbach detector | **Broken** (§0.1) |
| Full \(\lambda_{\min}(\tilde Q)>-1/2\) | **False** — abandoned |
| NS via \(H_N\), \(\lambda_{\min}\ge-3/14\) | Separate — false at small \(N\) |
| Large-data SND / noncircular \(M\) | **Hard** — not this note |

---

## 6. Interface to Triple Lock (corrected)

Replace “Bridge: \(\lambda_{\min}(Q_N)>-1/2\)” and the dark-state lemma with:

> **Bridge\*:** \(R(v)>-1/2\) for Goldbach test vectors \(v=\sum(e_p-e_q)\), and \(v^\top\tilde Q v\ge 0\) on the SND cone.

See `docs/papers/SND_GNC_BRIDGE_REVISED.md` and `docs/math/CLOSURE-ATTACK-PLAN.md`.
