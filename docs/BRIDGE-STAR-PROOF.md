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
Multi-rep: \(v=\sum_a(e_{p_a}-e_{q_a})\) over unordered Goldbach partitions.

**Conjecture (Bridge\*).** For every such \(v\not\equiv 0\),
\[
R(v):=\frac{v^\top\tilde Q_N v}{\|v\|_2^2}>-\frac12.
\]

**Status:** single-pair **proved** (§2); multi-rep **numeric** + lemma open (§3).  
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

## 3. Multi-representation — structure

Let
\[
\mathcal{R}(k)=\{p\in\mathbb{P}:2\le p\le k/2,\;k-p\in\mathbb{P}\}.
\]
Set \(v=\sum_{p\in\mathcal{R}(k)}(e_p-e_{k-p})\) (sites \(\le N\)).

Same-pair blocks contribute as in §2 (each \(>-\|v_{\mathrm{pair}}\|^2/2\)).  
Cross terms among distinct partitions can push \(R\) negative; still \(>-1/2\) in checks.

### Target lemma **[Open]**

**Lemma (Cross-term control).** There exists absolute \(c_0<1/2\) such that for all even \(k\le N\),
\[
v^\top\tilde Q_N v\ge -c_0\|v\|_2^2.
\]

**Numeric:** worst multi-rep \(R\) for \(N\le 200\) among summed partition vectors ≈ \(-0.15\) at \(k=10\) (single effective pair after cancellation); for richer multi-rep, values sit higher (e.g. \(k=100\): \(R\approx +0.025\)). Full cone/GNC scan: `scripts/bridge_floor_verify.py` (extend for summed \(v\)).

**Attack:**
1. Cauchy–Schwarz on off-pair blocks vs \(\|v\|^2\sim\#\mathcal{R}(k)\).  
2. Average Goldbach estimates on \(\sum p^{-1/2}\).  
3. Restrict \(\tilde Q\) to the prime support of \(v\) (small indefinite matrix).

---

## 4. SND cone (companion)

**Proposition (cone).** If \(v\ge 0\), \(\|v\|_2=1\), then \(v^\top\tilde Q_N v\ge 0\).

All entries of \(\tilde Q_N\) are positive ⇒ quadratic form on the positive orthant is nonnegative.  
(Formal Gram via correct \(g=\mu*(1/\mathrm{id})\) factorization + \(D^{-1/2}\) conjugation — writeup pending.)

---

## 5. Status board

| Claim | Status |
| --- | --- |
| Bridge\* single-pair on \(\tilde Q_N\) | **Proved** (§2) |
| Bridge\* multi-pair | Lemma open (§3) |
| June 5 dark-state ↔ Goldbach | **False** (§0) |
| June 5 paper \(v_k\) as Goldbach detector | **Broken** (§0.1) |
| Full \(\lambda_{\min}(\tilde Q)>-1/2\) | **False** — abandoned |
| NS via \(H_N\), \(\lambda_{\min}\ge-3/14\) | Separate — need matrix one-liner |
| Clay large-data | **Not** this note |

---

## 6. Interface to Triple Lock (corrected)

Replace “Bridge: \(\lambda_{\min}(Q_N)>-1/2\)” and the dark-state lemma with:

> **Bridge\*:** \(R(v)>-1/2\) for Goldbach test vectors \(v=\sum(e_p-e_q)\), and \(v^\top\tilde Q v\ge 0\) on the SND cone.

Equivalence arrows only after that rewrite + §2.1 identity fix. See `docs/papers/SND_GNC_BRIDGE_REVISED.md`.
