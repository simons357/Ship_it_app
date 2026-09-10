# Proof attempt — Lemma★ and what actually closes

> **Working foundation (controlling):** `LEMMA_STAR_CANONICAL.md` + `LEMMA_STAR_EXACT_FORMULAS.md` + shape SoT [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md) / [`docs/ns-review/LEMMA-STAR-ACTUAL-SHAPE.md`](../../../docs/ns-review/LEMMA-STAR-ACTUAL-SHAPE.md).  
> **LIVE kill/proof-lane lock (Attack 8 / 9A–9D):** [`PROOF_LemmaStar_LIVE_LOCK.md`](./PROOF_LemmaStar_LIVE_LOCK.md) — prefer this for current Attack 9 status.  
> **Five-lane recovered discussion:** `FIVE_LANE_RECOVERY.md` (PR #48; original five lane names **not** fully recovered — do not substitute 9A–9D).  
> **This file:** annotated **archive** of an older attempt. Keep for history; do not treat unmarked claims as current SoT.  
> **Honesty lock:** Unconditional Lemma★ / `sup R_★` / finite `C_geom` for **all** `v` is **OPEN**. **NS not solved.** Do **not** green ★.

**Unconditional Lemma★ is not proved. NS not solved.**

**Reframe (controlling):** ★ is a **shape** statement. After \(u=av\) and optimizing size, \(\nu\) cancels; ★ is a uniform bound on
\[
\mathcal R_\star(v)=\frac{\bigl(T_c(v)_+\bigr)^2}{D_s\,E\,Y}.
\]
**One direction supported:** ★ ⇒ global regularity (quotient / HANDOFF ODE).  
**Not supported here:** converse — GR does **not** automatically force the uniform inequality over every smooth field. Do **not** say “equivalent to global regularity.”

**Audit lock (10 Sep 2026):**
- Proposed universal \(|T_c(u)|\le C\|u\|_2 X^{3/2}\) is **algebraically false** (scales \(a^3\) vs \(a^4\) under \(u=av\)) — discard that route.
- \(T_c(-v)=-T_c(v)\) with \(D_s,E,Y\) fixed ⇒ universal bound on \((T_c)_+^2\) ⇔ universal bound on \(T_c^2\).
- §4 below does **not** establish its opening advertised theorem — incomplete estimates; “proved” label withdrawn for that opening claim.
- Near-shell: \(\lim\mathcal R_\star=K_{\alpha,\beta}(w)\) only for aligned, sign-selected \(z_\beta\); arbitrary \(z_\beta\) depends on projection against \(B(w,w)\).

**Date:** 7 Sep 2026 (audit annotations 10 Sep 2026)

---

## 0. Notation (proved algebra)

Mean-zero divergence-free \(u\) on \(\mathbb T^3\), \(A=-P\Delta\), \(B(u,u)=P((u\cdot\nabla)u)\),

\[
X=\|A^{1/2}u\|_2^2,\quad
Y=\|Au\|_2^2,\quad
Z=\|A^{3/2}u\|_2^2,\quad
\Lambda=Y/X,\quad
E=\|u\|_2^2,
\]

\[
w(A)=A-\Lambda,\qquad
Z-\Lambda Y=\|A^{1/2}(A-\Lambda)u\|_2^2\ge0,
\]

\[
\mathcal N=-\langle B(u,u),Au\rangle,\qquad
\mathcal M=-\langle AB(u,u),Au\rangle,\qquad
\mathfrak T_c=\mathcal M-\Lambda\mathcal N.
\]

**Identity (proved).**
\[
\mathfrak T_c=-\langle B(u,u),\,A(A-\Lambda)u\rangle,
\qquad
\Lambda'=\frac{2}{X}\mathfrak T_c-\frac{2\nu}{X}(Z-\Lambda Y).
\]
Also \(X\le E\Lambda\) (Cauchy–Schwarz / Plancherel), and \(\Lambda\ge1\) on \(\mathbb T^3\) (lowest lattice frequency).

---

## 1. Theorem (Lemma★ ⇒ global regularity) — **proved (one direction)**

Assume there exist \(\theta_0\in(0,1)\) and \(C_0<\infty\) such that for every smooth mean-zero divergence-free \(u\),

\[
\tag{★}
\mathfrak T_c
\le
\theta_0\nu\,(Z-\Lambda Y)
+C_0\nu^{-1} E\,X\Lambda.
\]

Then on any strong-solution interval, with \(E(t)\le E(0)\) (energy inequality),

\[
\Lambda'
\le
-\frac{2\nu(1-\theta_0)}{X}(Z-\Lambda Y)
+2C_0\nu^{-1} E\Lambda
\le
2C_0\nu^{-1} E(0)\,\Lambda.
\]

Hence
\[
\Lambda(t)\le\Lambda(0)\exp\bigl(2C_0\nu^{-1} E(0)\,t\bigr),
\qquad
X(t)\le E(0)\Lambda(t)<\infty
\quad\text{for all finite }t.
\]

Standard continuation: a smooth solution cannot blow up in finite time.  
**Therefore a proof of unconditional (★) implies global regularity for smooth data on \(\mathbb T^3\).**

**Not proved here:** the converse (GR ⇒ ★ as a uniform inequality over every field). These files supply no such argument. Do not write “★ ≡ GR.”

**Consequence:** the next sections attempt (★) only under extra hypotheses, or prove weaker statements that do not imply Clay.

---

## 2. Theorem (pure viscous absorption is false) — **proved**

**Claim.** There is no \(\theta\in[0,1)\) such that
\[
\mathfrak T_c\le\theta\nu(Z-\Lambda Y)
\]
holds for all smooth divergence-free fields.

**Proof.** Fix the triad support
\[
k_1=(1,0,0),\quad k_2=(2,1,0),\quad k_3=(-3,-1,0)
\]
and a phase choice with \(\mathfrak T_c(u_\*)>0\) and \(Z-\Lambda Y>0\) (explicit Fourier computation; see `attack2_triad_probe.py`, field `amps=(1,1,1j)`).  
For \(u=B u_\*\) (\(B>0\)):

\[
\mathfrak T_c(Bu_\*)=B^3\mathfrak T_c(u_\*),
\qquad
Z-\Lambda Y\big|_{Bu_\*}=B^2(Z-\Lambda Y)(u_\*).
\]

Ratio \(\mathfrak T_c/(Z-\Lambda Y)=B\cdot\mathfrak T_c(u_\*)/\mathrm{Var}(u_*)\to\infty\) as \(B\to\infty\).  
No fixed \(\theta\) works. \(\square\)

(Numerical: \(B=20\) already forces ratio \(\approx3.8\).)

---

## 3. Theorem (Young reduction) — **proved**

For every \(\varepsilon>0\),

\[
\tag{Y}
|\mathfrak T_c|
\le
\varepsilon\,(Z-\Lambda Y)
+\frac{1}{4\varepsilon}\,\|A^{1/2}B(u,u)\|_2^2.
\]

**Proof.** Plancherel:
\[
\mathfrak T_c=-\Re\sum_k\widehat{B}(k)\cdot|k|^2 w(k)\overline{\hat u(k)}.
\]
Pointwise Young with \(a=|k|w|\hat u|\), \(b=|k||\widehat{B}|\):
\[
|k|^2|w||\widehat{B}||\hat u|
\le\varepsilon\,|k|^2 w^2|\hat u|^2+\frac{1}{4\varepsilon}|k|^2|\widehat{B}|^2.
\]
Sum and take real parts. \(\square\)

**Gap to (★):** one still needs
\[
\|A^{1/2}B(u,u)\|_2^2
\le
C\,E\,X\Lambda
\]
(or \(\le C\nu^{2}E X\Lambda\) after choosing \(\varepsilon=\theta\nu\)).  
That bound is **not proved here**; controlling \(\|A^{1/2}B\|_2\sim\|\nabla B(u,u)\|_2\) at energy level is the supercritical step.

---

## 4. Attempt (BKM-conditional DA-NS-1) — **not proved as advertised**

**Audit:** the opening claim below is **not** established by this section. The sketch starts from a remainder involving \(\|\nabla u\|_\infty^2 X\), then runs into incomplete spectral estimates, and is eventually replaced by a **different** conditional statement under hypothesis (H\(_\infty\)). The “proved” label on the opening theorem is **withdrawn**.

**Opening claim (advertised, not proved here).** Absolute \(C_*<\infty\) such that
\[
\mathfrak T_c
\le
\theta\nu\,(Z-\Lambda Y)
+\frac{C_*}{\theta\nu}\,\|\nabla u\|_{L^\infty}^2\,X
\qquad\text{for all }\theta\in(0,1).
\]
In DA-NS-1 form with remainder \(K(t)X\Lambda\), one may take
\[
K(t)=\frac{C_*}{\theta\nu}\,\frac{\|\nabla u(t)\|_{L^\infty}^2}{\Lambda(t)},
\]
which is **not** known to lie in \(L^1(0,T)\) from Leray data alone (same difficulty as BKM).

**Incomplete sketch (archive):**

\[
|\mathfrak T_c|
=|\langle(u\cdot\nabla)u,\,A(A-\Lambda)u\rangle|
\le\|u\|_{L^\infty}\|\nabla u\|_{L^2}\|A(A-\Lambda)u\|_{L^2}.
\]

Agmon on \(\mathbb T^3\): \(\|u\|_{L^\infty}\le C_A\|u\|_{L^2}^{1/2}\|u\|_{H^2}^{1/2}\).  
We avoid Agmon and use \(\|u\|_{L^\infty}\le C\|\nabla u\|_{L^\infty}^{1/2}\|u\|_{L^\infty}^{?}\) — cleaner route:

Standard Calderón estimate / product:
\[
|\langle B(u,u),\phi\rangle|
\le C\|\nabla u\|_{L^\infty}\|u\|_{L^2}\|\phi\|_{L^2}
\]
for divergence-free fields (integrate by parts / use \(\nabla\cdot u=0\)). Take \(\phi=A(A-\Lambda)u\):

\[
|\mathfrak T_c|
\le C\|\nabla u\|_{L^\infty}\,E^{1/2}\,\|A(A-\Lambda)u\|_2.
\]

Now
\[
\|A(A-\Lambda)u\|_2^2
=\sum_k|k|^4 w(k)^2|\hat u(k)|^2
=\sum_k|k|^2(\Lambda+w(k))\,|k|^2? 
\]
Since \(|k|^2=\Lambda+w\),
\[
|k|^4 w^2=( \Lambda+w)^2 w^2,
\]
\[
\|A(A-\Lambda)u\|_2^2
=\sum(\Lambda+w)^2 w^2|\hat u|^2
\le 2\sum(\Lambda^2 w^2+w^4)|\hat u|^2.
\]

Relate to variance \(V:=Z-\Lambda Y=\sum|k|^2 w^2|\hat u|^2\).  
Use \(|k|^2\ge1\) and Hölder on the spectral measure:

**Elementary bound used:** by Cauchy–Schwarz in the form
\[
\sum |k|^4 w^2|\hat u|^2
=\sum \big(|k|w|\hat u|\big)\big(|k|^3 w|\hat u|\big)
\le
\Bigl(\sum|k|^2 w^2|\hat u|^2\Bigr)^{1/2}
\Bigl(\sum|k|^6 w^2|\hat u|^2\Bigr)^{1/2},
\]
which reintroduces a higher moment — **not closed**.

**Closed path:** write
\[
\sum|k|^4 w^2|\hat u|^2
=\sum|k|^2(\Lambda+w)w^2|\hat u|\cdot|k|^0?
=\Lambda V+\sum|k|^2 w^3|\hat u|^2.
\]
Estimate \(\sum|k|^2 w^3|\hat u|^2\le\|w\|_{L^\infty(\mu)}\,V\), and
\[
|w(k)|\le|k|^2+\Lambda\le 2\sup|k|^2,
\]
again diameter-dependent — **not** Lemma★.

**Substitute a cruder but closed estimate:**  
\[
\|A(A-\Lambda)u\|_2
\le\|A^{1/2}\|_{L^2\to L^2\text{ on }(A-\Lambda)u\text{ weighted}}
\le
\|A u\|_2^{1/2}\|A^{1/2}(A-\Lambda)u\|_2^{?}.
\]

Use instead the vorticity form and the classical inequality
\[
\bigl|\langle B(u,u),Au\rangle\bigr|\le C\|\nabla u\|_{L^\infty}X,
\]
and similarly for \(\mathcal M\), whence
\[
|\mathfrak T_c|\le C\|\nabla u\|_{L^\infty}(Y+\Lambda X)=2C\|\nabla u\|_{L^\infty}X\Lambda.
\]
Then
\[
\mathfrak T_c
\le
\theta\nu V
+\frac{C^2}{\theta\nu}\|\nabla u\|_{L^\infty}^2\frac{(X\Lambda)^2}{V}
\]
is useless when \(V\) is small.

**Clean conditional statement (proved under the following estimate as hypothesis):**

**Hypothesis (H\(_\infty\)).** \(\lvert\mathfrak T_c\rvert\le C_\infty\|\nabla u\|_{L^\infty}X\Lambda\).  
(This is the natural scaling-homogeneous bound; verified on our triad probes up to \(O(1)\) constants when \(\|\nabla u\|_\infty\sim\sqrt{\Lambda}\sqrt{X}\) order.)

Then for any \(\theta\in(0,1)\),
\[
\mathfrak T_c
\le
\theta\nu V
+C_\infty\|\nabla u\|_{L^\infty}X\Lambda,
\]
so DA-NS-1 holds with \(K=C_\infty\|\nabla u\|_{L^\infty}\), and \(\int K<\infty\) whenever the BKM integral is finite — **conditional regularity**, classical.

---

## 5. Theorem (sharp scaling remainder identity on rays) — **proved**

Along any fixed-shape ray \(u=B u_\*\) with \(\mathfrak T_c(u_*)>0\),
\[
\frac{\mathfrak T_c(Bu_*)}{X(Bu_*)^{3/2}\Lambda(Bu_*)}
=\frac{\mathfrak T_c(u_*)}{X(u_*)^{3/2}\Lambda(u_*)}
=:C[u_*].
\]
So the **sharp** remainder class \(C_* X^{3/2}\Lambda\) is exactly amplitude-critical.  
On the reference triad above, \(C[u_*]\approx0.0357\).

**Open:** whether \(\sup C[u]<\infty\) over all shapes (equivalently Lemma★ via \(X\le E\Lambda\Rightarrow X^{3/2}\Lambda\le E X\Lambda\cdot\sqrt{\Lambda}/\sqrt{?}?\):

From \(X\le E\Lambda\), \(\sqrt{X}\le\sqrt{E}\sqrt{\Lambda}\),
\[
X^{3/2}\Lambda=X\cdot\sqrt{X}\cdot\Lambda
\le X\cdot\sqrt{E}\sqrt{\Lambda}\cdot\Lambda
=E^{1/2}X\Lambda^{3/2}.
\]
Vs \(E X\Lambda\): need \(E^{1/2}\Lambda^{3/2}\le C E\Lambda\) i.e. \(\Lambda^{1/2}\le C E^{1/2}\), **false** for large \(\Lambda\) at fixed \(E\).  

So **\(X^{3/2}\Lambda\) is NOT dominated by \(E X\Lambda\) uniformly** when \(\Lambda\gg E\).  
Earlier we claimed \(X^{3/2}\|u\|_2\le E X\Lambda\) using \(\sqrt{X}\le\sqrt{E}\sqrt{\Lambda}\) and \(\sqrt{\Lambda}\le\Lambda\):
\[
\|u\|_2 X^{3/2}=E^{1/2}X\sqrt{X}\le E^{1/2}X\cdot E^{1/2}\sqrt{\Lambda}=E X\sqrt{\Lambda}\le E X\Lambda
\]
(for \(\Lambda\ge1\)). That controls the Ladyzhenskaya-type remainder \(\|u\|_2 X^{3/2}\), **not** bare \(X^{3/2}\Lambda\).

**Discarded route (algebra):** the older “missing” inequality
\[
\tag{missing — FALSE}
|T_c(u)|\le C\|u\|_2\,X(u)^{3/2}
\]
is **not** a universal estimate. Under \(u=av\): LHS \(\sim a^3\), RHS \(\sim a^4\). For any field with \(T_c(v)\ne0\), \(a\to0\) contradicts it. Discard by scaling; do not pursue as the gap.

The live shape target is uniform \(\mathcal R_\star\) (see canonical), not (missing).

---

## 6. Where a proof of discarded (missing) would have gone — **archive only**

**Former target (now discarded by §5 audit):**
\[
\bigl|\langle B(u,u),A(A-\Lambda)u\rangle\bigr|
\le
C\|u\|_2\,\|A^{1/2}u\|_2^{3}.
\]

**Attempt.** Ladyzhenskaya: \(\|u\|_{L^4}\le C_L E^{1/8}X^{3/8}\) on \(\mathbb T^3\) (up to absolute constants).  
\[
\|B(u,u)\|_{\dot H^{-1}}
\le C\|u\otimes u\|_{L^2}
\le C\|u\|_{L^4}^2
\le C'E^{1/4}X^{3/4}.
\]
If one had
\[
|\mathfrak T_c|\le\|B\|_{\dot H^{-1}}\|A(A-\Lambda)u\|_{\dot H^{1}},
\]
then \(\|A(A-\Lambda)u\|_{\dot H^1}=\|A^{3/2}(A-\Lambda)u\|_2\), which is **larger** than \(\sqrt{V}\) and not \(\le C X\) — **gap**.

If one had
\[
|\mathfrak T_c|\le\|B\|_{\dot H^{-1}}\|A(A-\Lambda)u\|_{\dot H^{1}}\cdot ?
\]
wrong critical index.

**Correct needed pairing:** \(\psi=A(A-\Lambda)u\) lives naturally in a space of order \(\dot H^{0}\) relative to \(A^{1/2}(A-\Lambda)u\in L^2\), demanding \(B\in L^2\), hence
\[
\|B\|_2\le C\|u\|_{L^\infty}X^{1/2},
\]
and \(\|u\|_{L^\infty}\) is **not** \(\le C E^{1/2}X^{1/2}\) in 3D (false; that would be 2D-like).  
3D Agmon: \(\|u\|_{L^\infty}\le C E^{1/4}X^{1/4}\|Au\|_2^{1/2}=C E^{1/4}X^{1/4}Y^{1/4}\), introducing \(Y=\Lambda X\):
\[
\|B\|_2\le C E^{1/4}X^{1/4}(\Lambda X)^{1/4}X^{1/2}=C E^{1/4}X^{3/4}\Lambda^{1/4},
\]
\[
|\mathfrak T_c|\le\|B\|_2\|A(A-\Lambda)u\|_2.
\]
Still need \(\|A(A-\Lambda)u\|_2\le C\sqrt{\Lambda V}\) or \(\le C X^{3/4}\Lambda^{3/4}\) etc. — **not closed without further structure**.

**Status:** gap is the 3D product estimate closing on centered \(\psi=A(A-\Lambda)u\) using only \(E,X,\Lambda,V\). This is where the problem sits; no fake fill-in.

---

## 7. What is proved vs open (summary)

| Statement | Status |
|---|---|
| Spectral identities for \(\Lambda',\mathfrak T_c\) | **proved** |
| (★) ⇒ global regularity on \(\mathbb T^3\) | **proved** (one direction only) |
| GR ⇒ ★ (converse) | **not established** in these files |
| \(K=0\) form impossible | **proved** (scaling) |
| Young reduction (Y) | **proved** |
| Universal \(\lvert T_c\rvert\le C\|u\|_2 X^{3/2}\) | **FALSE** (discard) |
| §4 opening BKM-\(\|\nabla u\|_\infty^2 X\) theorem | **not proved** (incomplete) |
| Unconditional Lemma★ / \(\sup\mathcal R_\star<\infty\) | **open** |
| Numerics on probes | **evidence only** |

---

## 8. Honest bottom line

**Working target:** bound \(\mathcal R_\star=(T_c)_+^2/(D_s E Y)\) uniformly, or exhibit a family with \(\mathcal R_\star\to\infty\). One large finite value only raises \(C_{\mathrm{geom}}\); it does not kill ★.

What remains usable from this archive:

1. ★ ⇒ GR (one direction), via the HANDOFF ODE for \(\Lambda\).  
2. Pure variance absorption is **false**.  
3. Discarded (missing) \(X^{3/2}\) product as universal estimate.

What is **not** proved: unconditional (★). Claiming it would be claiming NS is solved — refused.

Foundation: `LEMMA_STAR_CANONICAL.md`, `LEMMA_STAR_EXACT_FORMULAS.md`.


---

## Relation to LIVE SoT / Attack 9B–9D (routing, 10 Sep 2026)

| Topic | Where |
|---|---|
| Canonical shape ★ / \(\mathcal R_\star\) | [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md), [`LEMMA-STAR-ACTUAL-SHAPE.md`](../../../docs/ns-review/LEMMA-STAR-ACTUAL-SHAPE.md) |
| LIVE kill criteria + Attack 9 table | [`PROOF_LemmaStar_LIVE_LOCK.md`](./PROOF_LemmaStar_LIVE_LOCK.md) |
| Attack 9B near-shell \(K_{\alpha,\beta}\) | [`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md) — restricted family; finite sample ≠ proof |
| Attack 9C / 9D | [`ATTACK_9C_FIXED_GAP_SPHERES.md`](./ATTACK_9C_FIXED_GAP_SPHERES.md), [`ATTACK_9D_THETA_M2_LOCKED_PHASE.md`](./ATTACK_9D_THETA_M2_LOCKED_PHASE.md) |
| PRODUCT-BLOCK / discarded \(\lvert T_c\rvert\le C\|u\|_2 X^{3/2}\) | **FALSE by scaling** (this archive §5); live gap is uniform \(\mathcal R_\star\) / HH→L structure — see LIVE lock |

**Do not** read any “proved” label in §§1–5 as unconditional ★. Only ★ ⇒ GR (one direction), K=0 impossible, and Young reduction are claimed proved here; unconditional ★ remains **open**.
