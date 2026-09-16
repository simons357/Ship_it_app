# C10 chain — depletion ⇒ (A), written out

**Date:** 16 September 2026  
**Do not work on Theorem H. Do not extend 9D sweeps. NS / Clay B not claimed.**

## (A), verbatim

On the unaugmented shell face, with \(D_j=\|\nabla\Delta_j\omega\|_2^2\) and \(0<\theta<1\),

\[
\boxed{
(\mathrm{A})\qquad
(T_{j\leftarrow j})_+
\le
\theta\nu D_j
+
R_{\mathrm{allowed}}.
}
\]

**Allowed \(R\):** energy \(\mathcal{E}\), shell enstrophies \(\{Z_k\}\), maybe a direction factor.  
**Forbidden in \(R\):** \(\dot e_j\), \(\dot Z\), \(\dot Z_j\), \(\Lambda'\).

This is **not** absorption into \(\nu Z_j\). Closing (A) is not Clay B.

---

## Decision tree (this page)

```
C10
  → derive depletion from NS dynamics?
  → depletion ⇒ (A)?
  → noncircular?  (right-hand side not H¹ / L^∞ / BKM / (A) itself)
  → survives adversarial families?
```

**Result: NO.** The failed arrow is recorded below. Do **not** repair it by inserting a stronger assumption (\(\|\nabla u\|_\infty\le\Gamma\), geometric tail, occupancy, BKM). That would change the question, not fill the arrow.

| Gate | Answer |
| --- | --- |
| Derive depletion from NS dynamics? | **NO.** Empty. Occupancy samples refused. |
| Depletion ⇒ (A)? | Tautology if depletion means the \(a_+\) line; that line is (A) for the main stretch |
| Noncircular? | **NO** on the first new arrow: template remainders and \(\|a_+\|_\infty\) are BKM-adjacent or are (A) |
| Adversarial families? | Energy-linear (A) **dies** on \(u^\lambda\) and on amplitude. Shears / \(v_L\) are inert |

PR #102 “SURVIVES” means circular drafts were refused, not that an inequality was proved. C10 is **not** closer to done than BKM because it is phrased dynamically. “Does the dynamics produce depletion sufficient for (A)?” is not a weaker question than BKM. It is the same unresolved dynamical hope in different clothes.

**Fake-weaker hypotheses.** Controlling \(a_+=(\xi\cdot S(u_{\mathrm{loc}})\xi)_+\) in \(L^\infty\) already controls a piece of \(\|\nabla u_{\mathrm{loc}}\|_\infty\). Shell occupancy / geometric tail strong enough to make Bernstein sum \(\Gamma\) is already a spectral sufficient condition for BKM. Naming those as “depletion” does not make them weaker than the forbidden regularity control.

---

## Operating map

Three **independent** bets on the same unresolved dynamical question. None currently proves that the dynamics cooperate.

| Lane | Target | Status |
| --- | --- | --- |
| **C10** | (A) as boxed above | failed at \(a_+\) / template remainders; do not assume \(\Gamma\) to “fix” it |
| **Centered drift** | \(T_c\le\theta\nu D_s+K(t)X\), \(K\in L^1(0,T)\) | separate; C10 need not work for drift, drift need not work for C10 |
| **SND** | instrument: measure \(\rho\), peak migration, tail, shell pairings | demoted from engine; Theorem H withdrawn; (P) **false** on Family H ([PR #101](https://github.com/simons357/Ship_it_app/pull/101)) |
| **Exact-shell 9D** | \(K\le 16/9\) | **CLAIMED**, frozen; ≠ unrestricted ★ ≠ regularity |

Do not merge C10 with \(T_c\) unless an explicit inequality connects them. After a NO, do not push C10 into \(T_c=M-\Lambda N\).

Tag legend: **EXACT** · **STANDARD LEMMA** · **NEW CLAIM** · **NUMERICAL ONLY** · **EMPTY**

Sources (other branches; not re-proved here): `docs/TJJ-ESTIMATE.md`, `docs/AXISYM-SHELL.md` on `origin/cursor/tjj-estimate-chain-e5c5`; `TJ-SAME-SCALE-CANDIDATES.md`, `UNAUG-PROOF-CHAIN.md` on [PR #102](https://github.com/simons357/Ship_it_app/pull/102).

---

## 0. Two \(\rho_j\) (do not mix)

The AXISYM extra hypothesis \(\rho_j^{\mathrm{rate}}=(T_{j\leftarrow j})_+/Z_j\) with \(\int\rho_j^{\mathrm{rate}}<\infty\) is Theorem AS-ρ. It is **not** (A). C10 is about (A).

If (A) holds with \(R_{\mathrm{allowed}}\) integrable on \([0,T]\) in the energy inequality for \(Z_j\), then \(Z_j\) cannot blow up from the local block alone. Infrared/ultraviolet sums and continuation remain.

---

## 1. Definitions

Class for the seated TJJ identities: smooth, divergence-free, rapidly decreasing, **axisymmetric with swirl** on \(\mathbb{R}^3\), unaugmented NS, no extra field. Littlewood–Paley projectors \(\Delta_j\) from a fixed radial bump \(\varphi\).

\[
Z_j=\|\Delta_j\omega\|_2^2,\qquad
D_j=\|\nabla\Delta_j\omega\|_2^2,\qquad
u_{\mathrm{loc}}=(\Delta_{j-1}+\Delta_j+\Delta_{j+1})u.
\]

\[
T_j=\langle\Delta_j(\omega\cdot\nabla u-u\cdot\nabla\omega),\Delta_j\omega\rangle,
\qquad
T_{j\leftarrow j}=\langle\Delta_j B(u_{\mathrm{loc}}),\Delta_j\omega\rangle,
\]

with \(B(\omega,u)=\omega\cdot\nabla u-u\cdot\nabla\omega\).

On \(\{\Delta_j\omega\neq 0\}\),

\[
\xi_j=\frac{\Delta_j\omega}{\lvert\Delta_j\omega\rvert},\qquad
\alpha_{\mathrm{loc},j}=\xi_j\cdot S(u_{\mathrm{loc}})\,\xi_j,\qquad
(\alpha_{\mathrm{loc},j})_+=\max(\alpha_{\mathrm{loc},j},0).
\]

Here \(S=\tfrac12(\nabla u+(\nabla u)^\top)\). Write \(a_+=(\alpha_{\mathrm{loc},j})_+\) for the C10 hinge.

**Depletion**, as used in C10, is **not** occupancy or alignment samples. It means: the positive stretch \(a_+\) is small enough, or integrable enough, that the main local pairing enters the right-hand side of (A).

Centered spectral drift (separate lane; §7):

\[
\Lambda=Y/X,\qquad
D_s=Z-\Lambda Y,\qquad
T_c=M-\Lambda N.
\]

---

## 2. The chain, with no omitted inequality

```
hypotheses
    │
    ▼
AS-Id, AS-Split                         EXACT
    │
    ▼
TJJ-Trans, TJJ-α                        EXACT
    │
    ▼
TJJ-template                            STANDARD LEMMA + L^∞ remainders
    │
    ▼
a_+ estimate   ‖(α)_+‖_∞ Z_j ≤ θν D_j + R_allowed     EMPTY / NEW CLAIM
    │
    ▼
commutators into R_allowed              EMPTY (Bernstein cubic wall)
    │
    ▼
depletion                               tautological if a_+ estimate holds
    │
    ▼
(A)                                     follows; not seated unaugmented
```

### Step I — shell budget. EXACT

**Proposition AS-Id.**

\[
\tfrac12\dot Z_j+\nu D_j=T_j.
\]

Do **not** bound \(T_{j\leftarrow j}\) by \(\dot Z_j\). That is C3, refused.

### Step II — Door-1 split. EXACT

**Proposition AS-Split.**

\[
T_j=T_{j\leftarrow\mathrm{IR}}+T_{j\leftarrow j}+T_{j\leftarrow\mathrm{UV}}.
\]

Far-shell Young (Lemmas AS-IR, AS-UV) is **STANDARD LEMMA** on this axisymmetric face (Hölder + Bernstein; constants from \(\varphi\)). Those lemmas do not touch \(T_{j\leftarrow j}\). Cross-scale summability on the unaugmented 3D face is **not supplied** on the honesty card.

### Step III — local transport vanishes. EXACT

**Proposition TJJ-Trans.**

\[
\int (u_{\mathrm{loc}}\cdot\nabla)\Delta_j\omega\cdot\Delta_j\omega=0.
\]

Only the commutator \([\Delta_j,u_{\mathrm{loc}}\cdot\nabla]\) remains from transport.

### Step IV — main stretch is \(\alpha\). EXACT

**Proposition TJJ-α.**

\[
\int\bigl((\Delta_j\omega)\cdot\nabla u_{\mathrm{loc}}\bigr)\cdot\Delta_j\omega
=
\int\alpha_{\mathrm{loc},j}\,\lvert\Delta_j\omega\rvert^2.
\]

The antisymmetric part of \(\nabla u\) drops. Identity, not a bound.

Hence **EXACT**

\[
T_{j\leftarrow j}
=
\int\alpha_{\mathrm{loc},j}\,\lvert\Delta_j\omega\rvert^2
+
T_{j\leftarrow j}^{\mathrm{comm}}.
\]

One-sided stretch, **EXACT**:

\[
\int\alpha_{\mathrm{loc},j}\,\lvert\Delta_j\omega\rvert^2
\le
\|(\alpha_{\mathrm{loc},j})_+\|_\infty Z_j
=
\|a_+\|_\infty Z_j.
\]

This is the only seated \(a_+\) inequality. It is not an estimate of \(a_+\).

### Step V — template. STANDARD LEMMA, remainders not allowed

**Proposition TJJ-template** (sits on the TJJ page):

\[
T_{j\leftarrow j}
\le
\varepsilon\nu D_j
+
\|a_+\|_\infty Z_j
+
C_\varepsilon[\varphi]\,\nu^{-1}\|u_{\mathrm{loc}}\|_\infty^2 Z_j
+
C[\varphi]\,\|\nabla u_{\mathrm{loc}}\|_\infty\sum_{|k-j|\le 1}Z_k.
\]

The first remainder after \(\varepsilon\nu D_j\) is the C10 hinge. The last two are **not** \(R_{\mathrm{allowed}}\).

**Kato–Ponce / dyadic commutators.** Bounds of the shape

\[
\bigl\|[\Delta_j,u\cdot\nabla]v\bigr\|_2
\lesssim
\|\nabla u\|_\infty\,\|v\|_2
\]

exist in the literature (Kato–Ponce, *Comm. Pure Appl. Math.* 41 (1988); dyadic forms in Danchin and later Besov/Triebel notes). **STANDARD LEMMA, citation not line-matched in this note.** Any such bound inserts \(\|\nabla u\|_\infty\) or \(\|u_{\mathrm{loc}}\|_\infty\). That is the Beale–Kato–Majda quantity, or a quantity Bernstein converts into a cubic wall. It is **not** an unaugmented \(a_+\) estimate from energy and \(\{Z_k\}\).

### Step VI — \(a_+\) estimate. EMPTY / NEW CLAIM

Needed for (A) from the template, after folding \(\varepsilon<\theta\):

\[
\boxed{
\|a_+\|_\infty Z_j
+
\text{(commutator remainders)}
\le
(\theta-\varepsilon)\nu D_j
+
R_{\mathrm{allowed}}.
}
\]

**No seated proof of this line.** Equivalent integrable substitute

\[
\int a_+\,\lvert\Delta_j\omega\rvert^2
\le
\theta\nu D_j+R_{\mathrm{allowed}}
\]

is the same claim in integral form (Door-3 / C6). PR #102 hard-run: this draft **COLLAPSES_TO_C6**. Absolute \(\|a_+\|_\infty\) is not controlled by energy or by \(\{Z_k\}\) (\(W^{1,2}\not\subset L^\infty\) in 3D).

Bernstein on the remainders returns \(2^{cj}\) or \(2^{j/2}Z^{1/2}\). That is the cubic wall. Hard-run C6: \(\alpha_+ Z/(\mathcal{E} Z)\sim\lambda^{5/2}\to\infty\); commutator proxy over \(D\) grows like \(\lambda\).

### Step VII — depletion ⇒ (A). TAUTOLOGY + EMPTY

If Step VI holds, then (A) holds. That implication is **EXACT** and uninteresting.

The dynamical claim “the NS flow produces depletion sufficient for Step VI” is **EMPTY**. Occupancy \(\approx 1\) and alignment \(\approx 1/2\) on restricted disks are **NUMERICAL ONLY** and are refused as depletion (C4).

**Standalone geometric depletion not reducing to C6 / C11 / C8:** **ABSENT** (PR #102 hard-run).

---

## 3. Circularity test (one question per arrow)

| Arrow | Right-hand object | Equivalent / stronger / secretly dependent on \(H^1\), \(L^\infty\), BKM, or (A)? |
| --- | --- | --- |
| hypotheses → AS-Id | \(\dot Z_j\), \(T_j\) | No. Bookkeeping. |
| AS-Id → split | \(T_{j\leftarrow j}\) | No. Partition. |
| split → TJJ-α | \(a_+\) as a *name* | No. Identity. |
| TJJ-α → template | \(\|u_{\mathrm{loc}}\|_\infty\), \(\|\nabla u_{\mathrm{loc}}\|_\infty\) | **Yes, secretly.** These are BKM-adjacent. Not energy, not \(Z\). |
| template → \(a_+\) estimate | \(\|a_+\|_\infty Z_j\le(\theta-\varepsilon)\nu D_j+R_{\mathrm{allowed}}\) | **This is (A) for the main stretch.** Using BKM \(\|\nabla u\|_\infty\le\Gamma\) makes \(a_+\le\Gamma\) and reduces C10 to a spectral sufficient condition for BKM, not a producer of (A). |
| \(a_+\) estimate → depletion | “depletion” | Tautology. |
| depletion → (A) | (A) | Tautology if Step VI is assumed. |
| any draft using \(\dot Z_j\), \(\dot e_j\), \(\Lambda'\) | time derivative of the budget | **Circular.** C3. Refused. |

**Brutal answer:** nothing in the seated identities is circular. The *first new analytic arrow* (template remainders, or \(a_+\) control) is either empty or dependent on \(\|\nabla u\|_\infty\) / Bernstein, which is the regularity quantity (A) was supposed to help avoid. C10 is **not** genuinely interesting as an unaugmented mechanism until Step VI is filled by something that is not BKM and not \(\dot Z_j\).

Conditional on an **explicit** hypothesis \(\|(\alpha_{\mathrm{loc},j})_+\|_{L^1_t L^\infty_x}<\infty\) (or \(\|\nabla u\|_\infty\in L^1_t\)), C10 becomes a criterion downstream of BKM. Publishable as conditional. Not the missing estimate (A).

---

## 4. Adversarial families

Do not revive C1–C5. Tests below are against C10’s claimed implication, including the SND shear family and the TJJ concentration family.

### 4.1 High-tail shear (SND Test A)

Velocity in the \(x\)-direction, depends only on \(y\), so \((u\cdot\nabla)u=0\) and typically \(T_{j\leftarrow j}=0\). Then (A) holds trivially. \(a_+\) is not stressed. **Does not support C10.** Does not kill a vacuous (A).

### 4.2 Amplitude \(u=Aw\) (SND Test B)

Stretch and \(T_{j\leftarrow j}\) scale as \(A^3\); \(D_j\) scales as \(A^2\); \(\|a_+\|_\infty\) scales as \(A\); \(Z_j\) as \(A^2\). So \(\|a_+\|_\infty Z_j\sim A^3\) against \(\nu D_j\sim A^2\). An \(A\)-independent (A) **FAILS** unless \(a_+\) itself depletes like \(1/A\). C10 does not produce that depletion. Same cubic obstruction as the withdrawn SND quadratic flux bound.

### 4.3 Equal-enstrophy shells \(v_L\) (SND Test C)

Kills a uniform \(\rho(0)\) floor for SND. It does not by itself kill or prove (A). Local \(T_{j\leftarrow j}\) on a shear \(v_L\) is again typically zero. **Inert for C10.**

### 4.4 Concentration \(u^\lambda=\lambda^{3/2}\varphi(\lambda x)\) (TJJ-E-false)

**EXACT scaling** (Proposition TJJ-E-false): occupied shell \(j\sim\log_2\lambda\),

\[
Z\sim\lambda^2,\qquad D\sim\lambda^4,\qquad T_{j\leftarrow j}\sim\lambda^{9/2}.
\]

Hence

\[
\frac{(T_{j\leftarrow j})_+}{\theta\nu D_j+C\,\mathcal{E}\,Z_j}\sim\lambda^{1/2}\to\infty.
\]

So **(A) with energy-linear \(R\) is false** as a uniform statement. Main stretch \(\|a_+\|_\infty Z_j\) is sharp at the same order (strain \(\sim\lambda^{5/2}\)). C10 cannot close (A) on this family without extra depletion that this family does not have.

This is the cheap kill of “C10 as an unaugmented absolute bound.” It does not kill C10 as a *conditional* criterion that excludes concentrating data by assuming \(a_+\) or \(\|\nabla u\|_\infty\) bounded.

### 4.5 Pure swirl (C5)

\(T_{j\leftarrow j}=0\). Check, not a class bound. **BLOCKED** as an upgrade to mixed fields.

---

## 5. What PR #102 actually showed

| Draft | Tag | Result |
| --- | --- | --- |
| \((T)_+\le\lvert\dot Z_j\rvert+\nu D_j\) | circular | REFUSED (C3) |
| depletion from \(\mathrm{sign}(\Lambda')\) | circular | REFUSED |
| \(\lvert T\rvert\le C\lvert\dot e_j\rvert\) | circular | REFUSED |
| occupancy + alignment samples | NUMERICAL ONLY | REFUSED (C4) |
| \(\int a_+\,\lvert\omega_j\rvert^2\le\theta\nu P_j+R_{E,Z}\) | NEW CLAIM | COLLAPSES TO C6 (Door-3, not seated) |
| \(\lvert T^{\mathrm{mm}}\rvert\) under SO(2) | NEW CLAIM | COLLAPSES TO C11 (axisym bulk still open) |
| near-shell \(K_{\alpha\beta}\) cancel ⇒ \(\rho_j<\nu\) | NUMERICAL ONLY | COLLAPSES TO C8 (lab) |
| independent geometric depletion | NEW CLAIM | **ABSENT** |

So “C10 SURVIVES” = empty principal door. Not a candidate mechanism yet.

---

## 6. Dependency graph

```mermaid
flowchart TD
  hyp[smooth axisym-with-swirl NS] --> id["AS-Id  EXACT"]
  id --> split["AS-Split  EXACT"]
  split --> far["AS-IR / AS-UV  STANDARD LEMMA"]
  split --> trans["TJJ-Trans  EXACT"]
  trans --> alpha["TJJ-α  EXACT"]
  alpha --> tmpl["TJJ-template  STANDARD LEMMA"]
  tmpl --> aplus["a+ estimate  EMPTY"]
  tmpl --> comm["commutators in R_allowed  EMPTY / cubic wall"]
  aplus --> dep["depletion  tautology"]
  comm --> dep
  dep --> A["(A)  not seated"]
  far -.->|does not close local block| A
  bkm["‖∇u‖_∞ or BKM  hypothesis"] -.->|makes remainders legal; circular for unaugmented (A)| tmpl
  zdot["Ż_j / Λ'  forbidden"] -.->|C3 refuse| A
```

---

## 7. Centered spectral drift — do not merge

Target of the drift lane:

\[
T_c\le\theta\nu D_s+K(t)X,
\qquad
\int_0^T K(t)\,dt<\infty.
\]

\(T_c\) is a **global** centered pairing. \(T_{j\leftarrow j}\) is a **local** LP block. There is **no seated inequality** of the form

\[
(T_c)_+\le C\sum_j(T_{j\leftarrow j})_+
\quad\text{or}\quad
(T_{j\leftarrow j})_+\le C(T_c)_+.
\]

Single-shell fields have \(T_c=0\) and \(D_s=0\) (vacuous for the shape quotient) while a local block can still be nontrivial on a different partition. Concentration that kills energy-linear (A) is a different scaling question from uniform \(\mathcal{R}_\star\).

C10 depletion, even if it existed, would not automatically bound \(T_c\) without an **explicit** comparison written and proved. **Do not merge the lanes.**

Lemma★ / PRODUCT-BLOCK \(\sup_v\mathcal{R}_\star<\infty\) remains a separate OPEN node. Exact-shell 9D does not close it (firewall in [`EXACT-SHELL-9D-FREEZE.md`](./EXACT-SHELL-9D-FREEZE.md)).

---

## 8. Independence (do not merge)

C10 does **not** have to work for centered drift to work. Centered drift does **not** have to work for C10 to work. SND is an **instrument** until its dynamics earn something stronger: measure \(\rho\), peak migration, tail shape, and shell pairings, and ask whether those measurements expose a depletion mechanism. They have not.

A geometric-tail / BKM sufficient condition remains a useful **conditional** theorem. It is not a repair of the failed C10 arrow.

---

## 9. Lock

**Failed arrow:** template \(\to a_+\) estimate (Step VI). Not repaired by assuming \(\|\nabla u\|_\infty\), a geometric envelope, or occupancy.

**C10 is not a candidate mechanism.** It is not closer to done than BKM.  
Seated: identities through TJJ-α.  
Empty: dynamics \(\Rightarrow\) depletion \(\Rightarrow\) (A), noncircular.  
Killed as unaugmented absolute (A): energy-linear \(R\), by \(u^\lambda\) and by amplitude.  
Forbidden: \(\dot Z_j\), \(\Lambda'\), occupancy samples, Theorem H, 9D sweeps, merging with \(T_c\) without an inequality.

Until Step VI is filled **without** those, do not say C10 produces (A).
