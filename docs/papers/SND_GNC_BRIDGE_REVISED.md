# A Universal Non-Concentration Principle: SND ≡ GNC ≡ Bridge\*
### (Corrected working draft — not a Clay claim)

**Jonathan Robert Simons, CRNA, MMed**  
Prime Field Technologies LLC | Savannah, Georgia  
simonsmedicalinnovations@gmail.com  
**Base text:** June 5, 2026 Unified PDF · **This revision:** 2026-08-02 (operator + floor correction)

---

## Status declaration

This draft keeps the **structural** idea of the June 5 paper: one non-concentration condition, three domain readings.  
It **corrects** arithmetic identities and the spectral-floor statement that do not survive computation.

| Label | Meaning in this revision |
| --- | --- |
| **[Proved]** | Argument below is complete for the stated claim |
| **[Conditional]** | Follows if a named hypothesis holds |
| **[Open]** | Not proved |
| **[Withdrawn]** | June 5 claim that fails for the named matrix |

**No Millennium Prize is claimed unconditionally.**

---

## Abstract (revised)

Let \(Q_N\) be the \(N\times N\) matrix \(Q_N(i,j)=1/\gcd(i,j)\), and let
\[
\tilde Q_N(i,j)=\frac{1}{\gcd(i,j)\sqrt{ij}}
\]
be its diagonally normalized form. We study three non-concentration readings:

1. **SND** — shell fractions \(\rho(t)=\max_j a_j(t)\le\rho_0\) for NS on \(\mathbb{T}^3\);
2. **GNC** — Goldbach difference vectors \(v_k\) stay away from the dark set of \(\tilde Q_N\);
3. **Bridge\*** — restricted spectral floor: \(v_k^\top\tilde Q_N v_k > -\tfrac12\|v_k\|^2\) for all even \(k\le N\) with \(v_k\not\equiv 0\), and \(v^\top\tilde Q_N v\ge 0\) for \(v\ge 0\).

**[Withdrawn]** Full-spectrum Bridge \(\lambda_{\min}(Q_N)>-1/2\) (and the same for \(\tilde Q_N\)): false for the named matrices (counterexamples for small \(N\)).

**[Proved]** Single Goldbach-pair case of Bridge\* on \(\tilde Q_N\) with \(v=e_p-e_q\) (§4.1).  
**[Withdrawn]** June 5 dark-state ↔ Goldbach lemma; June 5 \(v_k=\chi-\chi\circ(k-\cdot)\) as Goldbach detector (§3.2).  
**[Open]** Multi-representation cross-term lemma for Bridge\*; frame/Riesz form of SND arithmetic steps in companion NS files; Route C gaps for RH.

Threshold \(\kappa_*=6/\pi^2=\zeta(2)^{-1}\) remains the squarefree density; it is **not** identified with \(\lambda_{\min}(Q_N)\) in this revision.

---

## 1. Introduction (unchanged intent, corrected finish line)

Three Clay problems live in three vocabularies. The structural question is still:

> Can a spectral distribution on the prime lattice concentrate into a null set?

June 5 named the finish line as \(\lambda_{\min}(Q_N)>-1/2\).  
**Computation shows that inequality fails** for \(Q_N\) and for \(\tilde Q_N\) as full-spectrum statements.  
The finish line in this revision is **Bridge\*** (restricted Rayleigh), plus whatever normalized \(H_N\) the NS track actually proves \(\lambda_{\min}(H_N)\ge -3/14\) for (companion file — paste matrix definition when locked).

---

## 2. Operators

### 2.1 Definition

\[
Q_N(i,j)=\frac{1}{\gcd(i,j)},\qquad
\tilde Q_N(i,j)=\frac{1}{\gcd(i,j)\sqrt{ij}}.
\]

### 2.2 Correct factorization of \(Q_N\) **[Proved]**

June 5 claimed
\[
\frac{1}{\gcd(i,j)}=\sum_{d\mid\gcd}\frac{\mu(d)\varphi(d)}{d^2},
\]
which is **false** (\(n=2\): RHS \(=3/4\), LHS \(=1/2\)).

**Correct:** define \(g=\mu*(1/\mathrm{id})\) in the Dirichlet sense,
\[
\frac{1}{n}=\sum_{d\mid n}g(d),\qquad
g(n)=\sum_{d\mid n}\frac{\mu(d)}{n/d}.
\]
Then
\[
Q_N(i,j)=\sum_{d\ge 1}g(d)\,1_{d\mid i}\,1_{d\mid j}.
\]

The June 5 object
\[
H_N^{\mathrm{(old)}}=\sum_{d=1}^N\frac{\mu(d)\varphi(d)}{d^2}\,P_d^{(N)}
\]
is a **different** operator (diagonal in the standard basis if \(P_d\) are coordinate projections onto multiples of \(d\)). It must not be silently identified with \(Q_N\).

### 2.3 Full-spectrum floor **[Withdrawn]**

| Claim (June 5) | Status |
| --- | --- |
| \(\lambda_{\min}(Q_N)>-1/2\) for all \(N\le 5000\) | **False** — e.g. \(\lambda_{\min}(Q_{20})\approx -3.32\) |
| \(\lambda_{\min}(Q_N)\to 6/\pi^2-1/2>0\) | **False** for raw \(Q_N\) (floor \(\to-\infty\)) |
| Same for \(\tilde Q_N\) as full spectrum | **False** — \(\lambda_{\min}(\tilde Q_{20})<-1/2\), keeps falling |

Verifier: `scripts/bridge_floor_verify.py`.

### 2.4 Vacuum constant

\(\sum_d\mu(d)/d^2=1/\zeta(2)=6/\pi^2\).  
\(\sum_d\mu(d)\varphi(d)/d^2\) is a **different** series. June 5 §2.2 mixed them; this revision does not.

---

## 3. The three conditions (revised)

### 3.1 SND (NS) — unchanged definition

Shell fractions \(a_j(t)=E_j(t)/\sum E_k(t)\), \(\rho(t)=\max_j a_j(t)\).  
**SND:** \(\rho(t)\le\rho_0<1\).

**Theorem (NS under SND) [Conditional]** — as in companions (Ring Lemma, Phi-renorm, Theorem H).  
Not re-proved here. Subject to Claude/drive gaps: frame lower bound; \(X(t)\le M\) from data; CF small-angle vs threshold.

### 3.2 GNC (Goldbach) — vector fix

**June 5 vector [Withdrawn as Goldbach detector]:**
\[
v_k^{\mathrm{(old)}}(j)=1_{\mathbb{P}}(j)-1_{\mathbb{P}}(k-j).
\]
If \(p+q=k\) both prime, then \(v_k^{\mathrm{(old)}}(p)=v_k^{\mathrm{(old)}}(q)=0\). Every Goldbach pair is erased; the vector only sees half-Goldbach sites.

**June 5 dark-state lemma [Withdrawn]:** “Goldbach iff not dark” via \(Q_N(p,q)=1\Rightarrow\langle v,Qv\rangle>0\).  
For \(v=e_p-e_q\) on raw \(Q_N\): \(\langle v,Q_N v\rangle=1/p+1/q-2<0\). Sign is wrong; the iff fails.

**Working test vectors (this revision):**
\[
v_{p,q}:=e_p-e_q,\qquad
v_k:=\sum_{\substack{p\le k/2\\p,\,k-p\in\mathbb{P}}}(e_p-e_{k-p}).
\]

**GNC\* / Bridge\* on this class:** \(v^\top\tilde Q_N v > -\tfrac12\|v\|^2\).

> Stronger June 5 GNC with threshold \(\kappa_*=6/\pi^2\) on a mixed \(H_N\) is **not** used until \(H_N\) is defined and checked.

### 3.3 Bridge\* (restricted floor) **[Partially proved]**

**Definition (Bridge\*).**  
(i) For every Goldbach test vector \(v_k\) as above with \(v_k\not\equiv 0\),
\[
R(v_k):=\frac{v_k^\top\tilde Q_N v_k}{\|v_k\|^2}>-\frac12.
\]
(ii) For every \(v\ge 0\), \(\|v\|_2=1\), \(v^\top\tilde Q_N v\ge 0\) (SND cone).

---

## 4. Partial proof of Bridge\*

### 4.1 Single Goldbach representation **[Proved]**

Diagonal of \(\tilde Q_N\): \(\tilde Q_N(p,p)=1/p^2\). For distinct primes \(p,q\),
\[
R(e_p-e_q)=\frac12\Big(\frac1{p^2}+\frac1{q^2}\Big)-\frac1{\sqrt{pq}}.
\]
Then
\[
R+\frac12>\frac12-\frac1{\sqrt{pq}}\ge\frac12-\frac1{\sqrt6}>0
\]
since \(pq\ge 6\). Hence \(R>-1/2\).

(Note: \(R\) can be negative, e.g. \((2,3)\mapsto\approx-0.228\); the June 5 “exact square \(\ge 0\)” used the wrong diagonal \(1/p\).)

### 4.2 Multi-representation **[Open lemma]**

Cross terms among several partitions can make \(R\) negative (still \(>-1/2\) in checks through \(N\sim 200\)).  
**Lemma (needed):** \(R(v_k)\ge -c_0\) for some absolute \(c_0<1/2\). See `docs/BRIDGE-STAR-PROOF.md`.

### 4.3 Cone positivity **[Expected / numeric]**

All entries of \(\tilde Q_N\) are positive ⇒ Rayleigh on \(v\ge 0\) is nonnegative (formal Gram writeup pending correct \(g(d)\) factorization conjugated by \(D^{-1/2}\)).

---

## 5. Equivalence — what survives

June 5 Main Theorem claimed SND ⇔ GNC ⇔ full-spectrum Bridge on one \(Q_N\).  
**As written, that theorem is not kept** (Bridge clause false; \(Q_N\)/\(H_N\) identification broken).

**Revised structural claim [Open to re-prove after 4.2]:**
\[
\mathrm{SND(cone\ control)}\;\longleftrightarrow\;
\mathrm{GNC^*}\;\longleftrightarrow\;
\mathrm{Bridge^*}.
\]
Arrows must be rewritten without using \(\lambda_{\min}(Q_N)>-1/2\).

**Remark (still valid):** A structural equivalence, once proved for Bridge\*, does **not** by itself give unconditional Clay; it says one restricted inequality feeds three readings.

---

## 6. Corollaries (status reset)

| Corollary | Status |
| --- | --- |
| One proof of Bridge\* closes GNC\* + cone-SND reading | **[Conditional on §5 rewrite]** |
| SND ⇒ NS on \(\mathbb{T}^3\) | **[Conditional]** — companions; not Clay large-data until gaps closed |
| Bridge\* ⇒ RH | **[Not claimed]** — Route C was tied to full-spectrum floor |
| T2 ⇔ SND | Keep pointing at T2 DOI; not re-audited in this file |
| \(\kappa_*=6/\pi^2\) “universal floor of \(Q_N\)” | **[Withdrawn]** as \(\lambda_{\min}\) statement |

---

## 7. Single open problem (revised)

**Open A (Bridge\*).** Prove the multi-rep lemma: \(R_k>-1/2\) for all even \(k\le N\).  
**Open B (NS track).** Lock \(H_N(i,j)=\ldots\) with \(\lambda_{\min}\ge -3/14\); fix Riesz/frame step; derive \(M\) from data.  
**Open C (RH track).** Route C gaps — only after the RH operator matches Open A/B.

Abandoned as stated: “Prove \(\lambda_{\min}(Q_N)>-1/2\) for all \(N\).”

---

## 8. Summary table (revised)

| Condition | Domain | Status |
| --- | --- | --- |
| Full-spectrum \(\lambda_{\min}(Q_N)>-1/2\) | Operator | **Withdrawn** |
| Bridge\* (restricted) | Operator / Goldbach class | **Partial** (single-pair proved; \(R>-1/2\) not \(R\ge 0\)) |
| SND ⇒ NS | Fluids | Conditional |
| GNC\* on corrected \(v=e_p-e_q\) | Additive NT | Same as Bridge\* on that class |
| June 5 dark-state ↔ Goldbach | Additive NT | **Withdrawn** |
| SND ≡ GNC ≡ full Bridge | Meta | **Withdrawn** |
| SND(cone) ≡ GNC\* ≡ Bridge\* | Meta | To re-prove |
| Phi-renorm algebraic cancel | Fluids (swirl) | Standalone strong (companion) |

---

## 9. Closing

The June 5 paper’s **ambition** was right: one lattice, three readings.  
Its **finish line** was wrong for the matrix it named.  
This revision moves the work to a finish line that is **not yet proved**, but **not already false**.

---

## References (unchanged DOIs)

As in June 5 Unified PDF, plus internal:

- `docs/FLOOR-ATTACK.md`  
- `docs/BRIDGE-STAR-PROOF.md`  
- `docs/CLAUDE-CROSSWALK.md`  
- `scripts/bridge_floor_verify.py`
