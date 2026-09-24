# Fourier-triangle mechanism — reconstruction

20 September 2026.
**Identities, then the first missing
implication. Not a theorem. Not a
close. NS not solved.**

Unaugmented NS on
\(\mathbb{T}^3=(\mathbb{R}/2\pi\mathbb{Z})^3\).
No \(Q_1\). No \(\Phi\)-cancel. No
SND persistence. No Theorem H. No
Route A weld. Unrestricted
\(\sup\mathcal R_\star<\infty\) stays
**KILLED** by \(v_n\).

This page reconstructs the exact
Fourier-triangle geometry the desk
already locked, separates three kinds
of sentence, locates where that
geometry is lost when interactions
are **summed** and **evolved**, and
scores \(I_3\) / prime restrictions
**inside** that mechanism.

SoT identities:
[`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](https://github.com/simons357/Ship_it_app/blob/cursor/unaug-ns-unified-status-a7a2/docs/math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md)
on PR #104.
One-shell geometry:
[`ATTACK-9D-FULL-SUPPORT-BOUND.md`](https://github.com/simons357/Ship_it_app/blob/cursor/unaug-ns-unified-status-a7a2/docs/ATTACK-9D-FULL-SUPPORT-BOUND.md).
Gap-cancel / Need★:
[`NEED-STAR-HH-L-DUAL.md`](https://github.com/simons357/Ship_it_app/blob/cursor/unaug-ns-unified-status-a7a2/docs/NEED-STAR-HH-L-DUAL.md).
Cheap CS map:
[`LEMMA-STAR-REASON.md`](https://github.com/simons357/Ship_it_app/blob/cursor/unaug-ns-unified-status-a7a2/docs/LEMMA-STAR-REASON.md).
Time-dependent target:
[`CENTERED-DRIFT.md`](https://github.com/simons357/Ship_it_app/blob/cursor/unaug-ns-unified-status-a7a2/docs/CENTERED-DRIFT.md).

Three kinds of sentence, never mixed:

| Tag | Meaning |
|---|---|
| **EXACT** | Identity. Do not redo. |
| **NUMERICAL** | Printed sample. Not \(C_0\). Not \(16/9\). |
| **ILLUSTRATIVE** | Motion / picture. Not a bound. |

**CLAIMED** stays a fourth word, not
a proof. **DEAD** stays dead.

---

## 1. Shell placement (EXACT)

Mean-zero divergence-free field

\[
v(x)=\sum_{k\in\mathbb{Z}^3\setminus\{0\}}
v_k e^{ik\cdot x},
\qquad
k\cdot v_k=0,
\qquad
v_{-k}=\overline{v_k}.
\]

Stokes / Leray:

\[
A=-P\Delta,
\qquad
(Av)_k=\lambda_k v_k,
\qquad
\lambda_k=\lvert k\rvert^2,
\qquad
B(v,v)=P[(v\cdot\nabla)v].
\]

Eigenvalue shell \(\alpha\):
\(\{k:\lvert k\rvert^2=\alpha\}\).
Projector \(\Pi_\alpha\) is exact on
\(\mathbb{Z}^3\), not a Littlewood–Paley
annulus.

Linear moments:

\[
\begin{aligned}
E&=\|v\|_2^2=\sum_k\lvert v_k\rvert^2,\\
X&=\|A^{1/2}v\|_2^2=\sum_k\lambda_k\lvert v_k\rvert^2,\\
Y&=\|Av\|_2^2=\sum_k\lambda_k^2\lvert v_k\rvert^2,\\
Z&=\|A^{3/2}v\|_2^2=\sum_k\lambda_k^3\lvert v_k\rvert^2,\\
\Lambda&=Y/X.
\end{aligned}
\]

Spectral spread (one object):

\[
\mathcal D_s
=Z-\Lambda Y
=\|(A-\Lambda)A^{1/2}v\|_2^2
=\sum_k\lambda_k(\lambda_k-\Lambda)^2\lvert v_k\rvert^2
\ge 0.
\]

One shell \(\Rightarrow\mathcal D_s=0
\Rightarrow T_c=0\). Vacuous. Not a kill.

Two shells \(\alpha,\beta\) with
energies \(e_\alpha,e_\beta\):

\[
\mathcal D_s
=\frac{\alpha\beta(\alpha-\beta)^2 e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}.
\]

A **triangle** is an ordered triad
\((p,q,k)\) with \(p+q=k\). Each
ordered pair \((p,q)\) counted once;
\(k\) is determined.

---

## 2. Divergence-free polarizations and Leray (EXACT)

Transverse condition: \(p\cdot v_p=0\).
Leray on the output:

\[
P_k=I-\frac{k\otimes k}{\lvert k\rvert^2},
\qquad
\widehat{B}_k
=i\,P_k\sum_{p+q=k}(q\cdot v_p)\,v_q.
\]

Because \(p\cdot v_p=0\),

\[
q\cdot v_p=(k-p)\cdot v_p=k\cdot v_p,
\]

so

\[
\widehat{B}_k
=i\,P_k\sum_{p+q=k}(k\cdot v_p)\,v_q.
\]

Leray does not enlarge the vector.
If the raw convolution is already
\(\perp k\), \(P_k\) is idle
(three-shear write-up: “Leray does
not change it”).

On one input shell
\(\lvert p\rvert^2=\lvert q\rvert^2=\alpha\),
\(\lvert k\rvert^2=\beta\):

\[
k\cdot p=k\cdot q=\beta/2,
\qquad
\lvert k_\perp\rvert^2
=\beta\Bigl(1-\frac{\beta}{4\alpha}\Bigr).
\]

Write \(k=k_\parallel+k_\perp\),
\(k_\parallel=(\beta/(2\alpha))p\),
\(k_\perp\cdot p=0\), \(k_\perp\) real.
Then \(k\cdot v_p=k_\perp\cdot v_p\)
and the one-mode Cauchy–Schwarz

\[
\lvert k\cdot v_p\rvert
\le
\lvert k_\perp\rvert\,\lvert v_p\rvert
=
\sqrt{\beta\bigl(1-\beta/(4\alpha)\bigr)}\,\lvert v_p\rvert
\]

is EXACT. Equality iff
\(v_p=\lambda k_\perp\) for
\(\lambda\in\mathbb{C}\): a legal
transverse polarization (still
\(\perp p\)).

Constraint: \(\lvert p+q\rvert\le 2\sqrt{\alpha}\)
forces \(\beta\le 4\alpha\). If
\(\beta>4\alpha\), no pairs,
\(\Pi_\beta B=0\). Vacuous.

As \(\beta\to 4\alpha^-\),
\(\lvert k_\perp\rvert\to 0\). Collinear
pairs contribute \(k\cdot v_p=0\).
Nothing in the identity divides by
\(\lvert k_\perp\rvert\).

---

## 3. Equal-length cancellation (EXACT)

“Equal-length” on this desk means
**one input shell**:
\(\lvert p\rvert^2=\lvert q\rvert^2=\alpha\).

Two exact cancellations live here.

### 3a. Geometric kernel

The parallel piece of \(k\) is
invisible to \(v_p\)
(\(k_\parallel\parallel p\) and
\(v_p\perp p\)). Only \(k_\perp\)
stretches. When the triangle is
flat (\(\beta=4\alpha\)),
\(k_\perp=0\) and that triad
transfers nothing.

### 3b. Two-shell gap-cancel

On exactly two shells \(\alpha>\beta\),
energy \(T_\alpha+T_\beta=0\) and

\[
T_c
=(\alpha-\beta)\frac{\alpha\beta E}{X}\,T_\alpha
=-(\alpha-\beta)\frac{\alpha\beta E}{X}\,T_\beta.
\]

The gap \((\alpha-\beta)\) **cancels**
in \(\mathcal R_\star\). When
\(T_c>0\):

\[
\mathcal R_\star
=\frac{\alpha\beta E\,T_\beta^2}{X\,e_\alpha e_\beta Y}.
\]

This is EXACT on two shells. It is
not Need★. It is not a multi-shell
bound.

---

## 4. Unequal-length defect (EXACT as a hole)

When \(\lvert p\rvert\neq\lvert q\rvert\),
or when more than two shells are
occupied, 3a–3b do not apply.

- \(k\cdot v_p\) is no longer a pure
  \(k_\perp(\alpha,\beta)\) factor.
- Gap-cancel has no single
  \((\alpha-\beta)\) to cancel against
  \(\mathcal D_s\).
- The growing-layer family \(v_n\)
  that killed unrestricted \(\star\)
  is a **multi-shell** unequal-length
  object. One-shell \(K\le 16/9\),
  even if true, does not see it.

Unsigned modal CS, which does not
care about lengths,

\[
\lvert\widehat B_k\rvert
\le
\lvert k\rvert\sum_p\lvert v_p\rvert\lvert v_{k-p}\rvert
\le
\lvert k\rvert\,E,
\]

then

\[
\lvert T_k\rvert
\le
\sqrt{\lambda_k}\,E\,\lvert v_k\rvert.
\]

If the output occupies \(s\) keys on
a shell,

\[
K_{\alpha,\beta}\le 16s
\qquad(\beta\le 4\alpha).
\]

**Independent of phases and
polarizations.** That is the defect:
length geometry, Leray, and signs
have already been thrown away.
Occupancy \(s\) is what remains.

---

## 5. Phase-dependent signed transfer (EXACT)

Keep \(\mathrm{Im}\). Never replace
by absolute values.

\[
T_k(v)
=-\mathrm{Re}\bigl(\widehat B_k\cdot\overline{v_k}\bigr)
=\sum_{p+q=k}
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

Energy of the bilinear form:

\[
\sum_k T_k=0.
\]

Centered moments and drift:

\[
N=\sum_k\lambda_k T_k,
\qquad
M=\sum_k\lambda_k^2 T_k,
\]

\[
T_c
=-\langle B,A(A-\Lambda)v\rangle
=M-\Lambda N
=\sum_k\lambda_k(\lambda_k-\Lambda)T_k
\]

\[
=\sum_{p+q=k}
\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr].
\]

Code lock: `Tc = M - Lam * N`.

Phases enter **only** through that
\(\mathrm{Im}\) product. The same
triangle with reversed field sends
\(T_c\to -T_c\). Only
\((T_c)_+=\max(T_c,0)\) is fought
by viscosity.

HH→L channel (two high inputs on
\(\alpha\), output on lower
\(\beta\)): the weight
\(\lambda_k(\lambda_k-\Lambda)\) is
order \(\beta\cdot\alpha\) when
\(\Lambda\) sits near the high
shell. The unsigned vertex carries
\(\sqrt{\beta}\), not \(\sqrt{\alpha}\).
That is why the channel looks able
to stretch. The leftover on this
channel is the **signed** sum

\[
\mathcal S_\star
=T_\beta^{\mathrm{HH}\to\mathrm{L}}
=\sum_{\substack{p+q=k\\ \lvert p\rvert^2=\lvert q\rvert^2=\alpha\\ \lvert k\rvert^2=\beta}}
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr],
\]

not \(\lvert\widehat B_k\rvert\).

---

## 6. What is numerical, what is a picture

**NUMERICAL (do not cash as \(C_0\)
or as \(16/9\))**

| Sample | Value | Scope |
|---|---|---|
| Attack 2 fixed-triad \(C_*\) | \(\approx 0.004058\) | That shape only. \(K=0\) absorption **DEAD** (ratio grows with amplitude). |
| 9B aligned max \(K\) | \(\approx 0.641\) at \((4,8)\) | One-shell probe. |
| Grow-\(s\) max \(K\) | \(\approx 0.456\), \(s\le 192\) | Historical. Larger \(s\) did not raise \(K\) in that sweep. |
| HH→L fan \(\mathcal R_\star\) | \(\sim\beta/\alpha\), max \(\approx 0.71\) | Falls as the high shell climbs. |
| Three-shear \(K_{1,2}\) | \(2/3\) | **EXACT** for \(w=(\sin y,\sin z,\sin x)\). Floor of \(\sup K\), not the ceiling. |
| Random-phase same-shell \(\mathcal R_\star\) | \(O(10^{-7})\) | Phases can cancel. Not a bound. |
| Locked \(\mathcal N_\star\) on one closer | \(\approx 0.099\) | Sample of Need★’s ratio. Not \(\sup\mathcal N_\star<\infty\). |

**CLAIMED, frozen, not this page’s
job:** \(\|\Pi_\beta B\|_2\le(4/3)
(\alpha/\sqrt{\beta})\|w\|_2^2\), i.e.
\(K\le 16/9\), via a weighted count
\(\sum c_k^2\le 3(\sum a_p^2)^2\) plus
a complex polarization cancellation
producing the factor \(3/4\).
Specialist reproduction pending.
Single input shell only. Designed
\(\Theta(m^2)\) 9D is **DEAD**.

**ILLUSTRATIVE motion (not a bound)**

- A high-high pair on shell \(\alpha\)
  closing onto a lower shell
  \(\beta\) “looks like” stretching
  because the vertex is
  \(\sqrt{\beta}\) and the weight is
  \(\sim\alpha\beta\).
- Random phases look like they wash
  \(T_c\) out; locked phases look
  like they could add. The
  designed locked-phase
  \(\Theta(m^2)\) subset is
  Freiman-AP: \(\mathcal D_s\) wins.
  Picture, not a theorem.
- Enstrophy “cascading down the
  triangle” is language for
  \(\sum T_k=0\) plus a negative
  \(T_\beta\) on the low shell.
  The identity is the conservation.
  The cascade is the picture.

---

## 7. \(I_3\) and prime restrictions

The later tape does **not** name an
object \(I_3\). It names \(T_k\),
\(T_c\), \(\mathcal S_\star\), and
(in the Route B handoff)
\(\mathcal I_\Lambda\). To assess the
request without inventing a second
\(T_c\), set

\[
I_3(v)
:=\sum_{p+q=k}
\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr]
=\sum_k T_k
=0.
\]

That is the **unweighted** cubic
interaction. It is EXACTLY energy
conservation of \(B\). The object
that can move \(\Lambda\) is the
**weighted** cubic

\[
T_c
=\sum_{p+q=k}
\lambda_k(\lambda_k-\Lambda)\,
\mathrm{Im}(\cdots).
\]

So \(I_3=0\) sits and does **not**
control \(T_c\). The first interesting
restriction of \(I_3\) is already
spectral: the factor
\(\lambda_k(\lambda_k-\Lambda)\).
That is EXACT. It is not a prime
restriction.

A **prime restriction** on this
mechanism is an optional mask

\[
P_n=\mathbf 1_{\mathbb P}(n)
\]

on some integer label of the triad:
mode index, shell index \(\lambda_k\),
or \(\lvert k\rvert\). That is FRA
selector language
([`docs/domain-architect/01-EQUATION-INVENTORY.md`](domain-architect/01-EQUATION-INVENTORY.md)
FRA-8 / GRV-7). It is **not** forced
by Leray, by \(p\cdot v_p=0\), or by
the Im-sum.

What a prime mask would actually do
**inside** the triangle:

| Effect | Status |
|---|---|
| Thin the set of closing triads \(p+q=k\) | True as counting. Fewer lattice points. |
| Lower occupancy \(s\) in the crude bound \(K\le 16s\) | Possible, not proved, and not needed if the claimed \(16/9\) sits. |
| Produce equal-length \(k_\perp\) cancellation | **No.** That is \(\lvert p\rvert=\lvert q\rvert\), not primality. |
| Produce gap-cancel | **No.** That is two shells and \(T_\alpha+T_\beta=0\). |
| Control the \(\mathrm{Im}\) product | **No.** Primes do not lock phases. |
| Put \(T_c\) in a useful \(L^1_t\) class | **No.** Instantaneous support restriction is not a pathwise majorant. |
| Repair unrestricted \(\star\) | **No.** \(v_n\) is not a prime-shell object, and the box is already dead. |

Arithmetic cousins that must stay in
the other book (C-GLUE / ARITH-H):

- Inverse-GCD \(H_N\), Q6 floor
  \(\lambda_{\min}(\widetilde Q\big|_P)\ge-1/4\),
  Bridge* \(R(e_p-e_q)>-1/2\).
- Full-spectrum
  \(\lambda_{\min}(Q_N)>-1/2\) is
  **retired**.
- HB Experiment 01: held-out TEST
  did not reject H0 for prime
  neighbor ratios.

Do not feed those into \(\Pi_k B\)
or into \(T_c\). A prime mask on
Fourier support is a **different
PDE’s data**, or a diagnostic
restriction, not a mechanism NS
forces.

If \(I_3\) was meant as the Route B
interaction norm \(\mathcal I_\Lambda\)
in

\[
\lvert T_c\rvert
\stackrel{?}{\le}
\sqrt{\mathcal D_s\,\mathcal I_\Lambda},
\]

that object is **not yet defined as
an exact pairing** on this desk.
Defining it by tautology
\(\mathcal I_\Lambda=T_c^2/\mathcal D_s\)
makes \(\mathcal I_\Lambda/X\) the
original question in other units.
Prime restrictions do not supply the
majorant.

---

## 8. Where the geometry is lost

Two distinct losses. Do not glue them.

### Loss A — summation (snapshot)

Per triangle, the desk still has:

- shell placement \(\lambda_k=\lvert k\rvert^2\),
- \(v_p\perp p\), \(P_k\) on the output,
- \(k_\perp\) on equal-length inputs,
- signed \(\mathrm{Im}\) transfer.

When those triangles are **added**
with a cheap estimate
\(\lvert\widehat B_k\rvert\le\lvert k\rvert E\),
every one of those structures dies
at once. What remains is occupancy
\(s\): a count of active keys.

That is the Need★ hole on two shells
and the \(K\le 16s\) hole on one
shell. The claimed \(16/9\) is an
attempt to kill \(s\) **on one input
shell** by putting polarization
cancellation and a weighted incidence
count back into the sum. It is
CLAIMED, single-shell, and even if
true does not bound a multi-shell
field.

**First missing implication (sum):**

\[
\boxed{
\begin{aligned}
&\text{EXACT per-triangle geometry}\\
&\qquad\not\Rightarrow\\
&\text{a signed bound on }\sum_{\text{all triads}}
\text{ that still sees }k_\perp\text{ and }\mathrm{Im}.
\end{aligned}
}
\]

Cheap CS is not that implication.
Need★ would be that implication on
the two-shell HH→L channel, and it
is **unwritten**. The claimed
one-shell \(K\le 16/9\) would be
that implication on \(Aw=\alpha w\),
and it is **not seated**.

### Loss B — evolution (time)

The identities of §§1–5 are
**instantaneous**. They hold at each
\(t\) for the current Fourier
coefficients.

The NS / Galerkin moment ODEs give
the EXACT clock

\[
\Lambda'
=\frac{2}{X}(T_c-\nu\mathcal D_s).
\]

If a useful remainder

\[
T_c
\le
\theta\nu\mathcal D_s
+K(t)X,
\qquad
\theta<1,
\qquad
K\in L^1_{\mathrm{loc}}
\]

sat, then \(\Lambda'\le 2K\) and
\(X\le\|u\|_2^2\Lambda\) would stay
finite. That is the Route B target.

Phases, occupancies, and which
triangles are active **move**. A
bound on \(K_{\alpha,\beta}(w)\) for a
frozen exact-shell field does not
control \(K(t)\) along the orbit.
A prime mask frozen at \(t=0\) is
not preserved by \(B\).

**Second missing implication
(evolve)** — not the first, and not
to be attacked before Loss A is
named:

\[
\text{snapshot bound on }T_c(v(t))
\quad\not\Rightarrow\quad
\int_0^T K(t)\,dt<\infty.
\]

Tautological
\(K=(T_c-\theta\nu\mathcal D_s)_+/X\)
makes this sentence empty.

---

## 9. First missing implication to the time-dependent bound

The time-dependent bound is Route B:

\[
T_c(t)
\le
\theta\nu\mathcal D_s(t)
+K(t)X(t),
\qquad
K\text{ useful in }L^1_{\mathrm{loc}}.
\]

The seated chain, and the first
break:

```
EXACT triangle (shell, Leray, k_⊥, Im)
        |
        |  EXACT
        v
T_k , T_c = Σ λ_k(λ_k−Λ) T_k ,  Λ' = 2(T_c−ν D_s)/X
        |
        |  FIRST MISSING IMPLICATION
        |  signed sum that keeps geometry
        |  (Need★ / seated 16/9 / non-tautological I_Λ)
        v
snapshot: |T_c| ≤ √(D_s I_Λ)  with I_Λ not T_c²/D_s
        |
        |  SECOND (later): I_Λ/X integrable
        v
T_c ≤ θν D_s + K(t) X ,  K ∈ L¹
        |
        |  EXACT if that estimate sits
        v
Λ' ≤ 2K  ⇒  X ≤ ‖u‖₂² Λ  finite
```

Do not skip the first break by
quoting \(16/9\), a prime mask, or
a numerical \(K\approx 0.64\).

What would count as writing the
first implication, and only that:

1. A signed estimate of
   \(\sum_{p+q=k}\mathrm{Im}(\cdots)\)
   that still uses \(k_\perp\) and
   \(P_k\), on the class the estimate
   claims (two-shell, or one input
   shell, or general — name it),
   **or**
2. a named death that every such
   estimate reintroduces occupancy
   \(s\) or \(\|\nabla u\|_\infty\).

Until (1) or (2) exists, the
time-dependent bound is not a
write. It is a target hanging on
an unwritten snapshot inequality.

Prime restrictions do not fill (1).
They thin the sum. They do not
restore the signs.

---

## Lock

Shell \(\lambda_k=\lvert k\rvert^2\) EXACT.
\(v_p\perp p\), \(\widehat B_k=i P_k\sum(k\cdot v_p)v_q\) EXACT.
Equal-length \(k_\perp\) EXACT on one input shell.
Two-shell gap-cancel EXACT.
\(\sum T_k=0\) EXACT. \(T_c=\sum\lambda_k(\lambda_k-\Lambda)T_k\) EXACT.
\(\Lambda'=2(T_c-\nu\mathcal D_s)/X\) EXACT.
Keep \(\mathrm{Im}\). Cheap CS returns occupancy \(s\).
\(I_3:=\sum T_k=0\) is energy, not \(T_c\).
Prime masks are optional selectors, not this mechanism.
Claimed \(K\le 16/9\) frozen, one shell, not seated.
Unrestricted \(\star\) killed by \(v_n\).
Need★ unwritten.

First missing implication:
per-triangle geometry \(\not\Rightarrow\)
signed bound on the sum.

That implication is now a gate:
[`SIGNED-ASSEMBLY-GATE.md`](SIGNED-ASSEMBLY-GATE.md).
It sits before old Gate 5.
The assembly blank splits as
[`SAG-5-COMPATIBILITY.md`](SAG-5-COMPATIBILITY.md):
shared-input rank (5A) is not
the partner/output network (5B).
Do not stamp SAG-5 from rank
alone. No \(\lvert\sum S\rvert\to\sum\lvert S\rvert\).
No occupancy bound yet.
SAG-6
([`SAG-6-LATTICE-CIRCLE.md`](SAG-6-LATTICE-CIRCLE.md)):
bisector plane
\(=\bigsqcup_\alpha C_{\alpha,k}\).
One circle is sparse. The stack
admits \(\rho_k(N)=1\). Centered
prefactor factors out of one
\(k\). Not the missing power.
The old \(Q_a\) witness is
scalene, not this stack.
Static shared-output rescue
**KILLED**. Next Gate =
[`JOINT-EPOCH-BUDGET.md`](JOINT-EPOCH-BUDGET.md).
Master ledger:
[`CENTERED-MASTER-LEDGER.md`](CENTERED-MASTER-LEDGER.md).
Reset \(\Delta W\) EXACT from
\(W_K=\mathcal D_s+X(\Lambda-K)^2\).
Do not evolve a bound that was never
written. No A2. No prime glue.
NS not solved.
