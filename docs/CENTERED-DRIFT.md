# Centered spectral drift — DA-NS-1 target

16 September 2026.
**Independent of C10. Independent of
SND persistence. Unrestricted \(\star\)
stays killed. Replacement leftover 4
stays OPEN. NS not solved.**

Not leftover 1. Do not start H1.
Do not weld the dead box.
Do not add \(K(t)\) to the PDE.
The \(K(t)\) below is a remainder
coefficient in an estimate, not a
forcing or a modified viscosity.

Handoff: [`NS-STATUS.md`](NS-STATUS.md).
Killed box:
[`LEMMA-STAR.md`](LEMMA-STAR.md),
[`LEMMA-STAR-GROWING-LAYER.md`](LEMMA-STAR-GROWING-LAYER.md).
Identities:
[`math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`](math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md).
Arithmetic: `python3 scripts/centered_drift.py`.

C10 did not seat (A). There is no
crossover inequality on this page.

B★
\([T_c]_+\le C X\Lambda^{1/2}\mathcal D_s^{1/2}\):
[`BSTAR.md`](BSTAR.md),
[`BSTAR-PROOF.md`](BSTAR-PROOF.md).
No universal \(C\). Imag
\(|k|^{-2}\) cutoff grows \(R_B\)
like \(\Lambda^{1/4}\). Not a
useful \(K\).
Triangle reconstruction:
[`FOURIER-TRIANGLE.md`](FOURIER-TRIANGLE.md).
First lift:
[`TRIANGLE-LIFT.md`](TRIANGLE-LIFT.md).
Energy-class ladder:
[`ENERGY-K.md`](ENERGY-K.md).
Pairing CS doors:
[`L-DOOR.md`](L-DOOR.md).
Instantaneous \(MN\):
[`MN-CANCEL.md`](MN-CANCEL.md).
First jet:
[`PATHWISE.md`](PATHWISE.md).
Short interval:
[`INTERVAL.md`](INTERVAL.md).
Incoming ledger:
[`CENTERED-LEDGER.md`](CENTERED-LEDGER.md).
Chart reset:
[`RESET.md`](RESET.md).
Relative width:
[`WIDTH.md`](WIDTH.md).
SBP / \(\Phi_e\):
[`SBP.md`](SBP.md).
Identities sit. The first
missing implication is this
page’s estimate.
\(K\sim\sqrt{E}\) is dead.
\(K_Y\sim\sqrt{E}\) and the
mid door die on \(v_n\) by
closed form.

---

## Target

Preserve centering.

\[
X=\|A^{1/2}u\|_2^2,\qquad
Y=\|Au\|_2^2,\qquad
Z=\|A^{3/2}u\|_2^2,\qquad
\Lambda=\frac{Y}{X},
\]

\[
T_c=M-\Lambda N
=-\langle B(u,u),A(A-\Lambda)u\rangle,
\qquad
\mathcal D_s=Z-\Lambda Y
=\|(A-\Lambda)A^{1/2}u\|_2^2\ge 0.
\]

**Drift estimate (OPEN).** There exist
\(\theta\in[0,1)\) and a coefficient
\(K\in L^1_{\mathrm{loc}}(0,T)\) such
that, along the classical solution,

\[
T_c
\le
\theta\nu\mathcal D_s
+K(t)X.
\]

A Y-remainder cousin is

\[
T_c
\le
\theta\nu\mathcal D_s
+K_Y(t)Y.
\]

Either form is useful only if the
coefficient is controlled by
quantities already known from the
energy inequality, or by a named
dynamical bound that does not assume
the desired \(H^1\) ceiling, \(L^\infty\),
or BKM.

---

## What is not this target

**Unrestricted Lemma★** used a
*uniform geometric* remainder

\[
T_c
\le
\theta\nu\mathcal D_s
+C_0\nu^{-1}\|u\|_2^2 X\Lambda.
\]

That box is **KILLED** by the
growing-layer family \(v_n\):
\(\mathcal R_\star(v_n)\to\infty\)
on the live evaluators. Instantaneous
admissible class, not a trajectory,
not a blowup.

Need★ cannot repair that box.
Do not restore \(\sup\mathcal R_\star<\infty\).

The \(K(t)X\) form is a different
sentence. \(v_n\) does not
automatically kill a *pathwise*
integrable remainder. It does kill
any remainder that is a uniform
function of energy-class norms of
the same scaling as
\(C_0\nu^{-1}\|u\|_2^2\Lambda\).

**Tautology warning.** Defining

\[
K(t)=\frac{(T_c-\theta\nu\mathcal D_s)_+}{X}
\]

makes the estimate an identity.
The content then collapses to
\(\int K<\infty\), which is the
original regularity question in
other units. That is not a proof.

---

## Identities (EXACT)

**Spectral Cauchy.** EXACT.
\[
X^2\le\|u\|_2^2\,Y
\qquad\Rightarrow\qquad
X\le\|u\|_2^2\Lambda.
\]

**Dissipative spread.** EXACT.
\[
\mathcal D_s=\sum_m a_m(a_m-\Lambda)^2 m_m\ge 0.
\]

**Log-center motion.** EXACT.
\[
(\log\Lambda)'
=\frac{2}{Y}\bigl(T_c-\nu\mathcal D_s\bigr).
\]

Work \(T_c-\theta\nu\mathcal D_s\).
Splitting \(M\) and \(\Lambda N\) by
coarse Sobolev estimates is how the
centering is lost. Do not do that
as the first move.

---

## Formal differential inequality

**STANDARD LEMMA** (algebra from the
identities; the estimate is not
granted).

Assume the X-remainder form with
\(\theta<1\). Then

\[
(\log\Lambda)'
\le
\frac{2}{Y}\bigl((\theta-1)\nu\mathcal D_s+K X\bigr)
\le
\frac{2KX}{Y}
=\frac{2K}{\Lambda},
\]

hence

\[
\Lambda'\le 2K.
\]

If \(K\in L^1(0,T)\), then
\(\Lambda(t)\le\Lambda(0)+2\int_0^t K\)
stays finite, and
\(X\le\|u\|_2^2\Lambda\) stays finite.

Assume instead the Y-remainder form.
Then

\[
(\log\Lambda)'
\le 2K_Y,
\]

so \(\log\Lambda\) stays finite if
\(K_Y\in L^1(0,T)\). That also
closes *if* the estimate sits with a
useful \(K_Y\).

Both implications are one direction.
They are not the estimate.

---

## Dependency graph

```
smooth NSE, A, spectral measure     EXACT defs
        |
        v
T_c = M − Λ N,  D_s = Z − Λ Y      EXACT
        |
        v
(log Λ)' = 2/Y (T_c − ν D_s)       EXACT
        |
        +---- X ≤ E Λ              EXACT
        |
        v
T_c ≤ θν D_s + K(t) X              NEW CLAIM; OPEN
        |
        v
Λ' ≤ 2K,  K ∈ L¹ ⇒ X bound         STANDARD; after the claim
        |
        x  not  x
        v
unrestricted ★ / uniform C_0       DEAD (v_n). Do not restore.
C10 a_+ sum                        NO seated inequality.
```

---

## Circularity test

Does the claim secretly assume
\(\|u\|_{H^1}\le C\),
\(\|\nabla u\|_\infty\le C\),
BKM, or a spectral tail already
known to imply regularity?

- If \(K\) is bounded by energy
  only: **false.** The unique
  amplitude-legal energy
  remainders die on \(v_n\).
  [`ENERGY-K.md`](ENERGY-K.md).
  The older \(a^4\) line
  \(\lvert T_c\rvert\le C\|u\|_2 X^{3/2}\)
  is a different death.
- If \(K\) is bounded by
  \(\|\nabla u\|_\infty\): **BKM.**
  Sufficient, not an attack on the
  dynamics.
- If \(K\) is defined as
  \((T_c-\theta\nu\mathcal D_s)_+/X\):
  **tautological.**
- A non-circular write must produce
  \(K\) from cancellation in
  \(T_c=M-\Lambda N\) itself
  (near-scale structure, or a
  monotone quantity), without
  embedding the unknown field into
  a supercritical norm.
  Instantaneous \(MN\) and
  above/below \(\Lambda\) are
  already dead as uniform
  \(\theta<1\).
  [`MN-CANCEL.md`](MN-CANCEL.md).

---

## Adversarial families

No new 9D sweeps.

1. **Growing-layer \(v_n\).** Kills
   every uniform \(C_0\) of ★
   scaling. Does not, by itself,
   kill a pathwise \(K(t)\) that is
   allowed to grow with \(n\) at a
   snapshot. It does forbid selling
   that snapshot family as a
   bounded remainder.
2. **Amplitude \(u=Av\).**
   \(T_c\sim A^3\), \(X\sim A^2\),
   \(\mathcal D_s\sim A^2\).
   The remainder \(K X\) must scale
   at least like \(A^3\) unless
   centering cancels the leading
   term. Energy-linear \(K\) fails.
3. **Single shell.** \(T_c=0\) and
   \(\mathcal D_s=0\). Holds as
   \(0\le 0\). Does not test the
   claim.
4. **Shears.** Nonlinear term
   vanishes. \(T_c=0\). Same
   \(0\le 0\).
5. **C10 quantities.** No seated
   \(T_c\le C\sum a_+ Z_j\). Do not
   write one from language.

---

## Verdict

| Claim | Status |
|---|---|
| Spectral identities | **PROVED** (exact). |
| Formal DI: estimate \(\Rightarrow\) \(\Lambda'\le 2K\) | **PROVED** as algebra. |
| Drift estimate with useful \(K\) | **OPEN.** Pathwise, not energy-class. |
| Energy-class \(K\sim\sqrt{E}\) / \(K_Y\sim\sqrt{E}\) / mid | **DEAD** on \(v_n\). [`ENERGY-K.md`](ENERGY-K.md). |
| Tight CS / LE door | **DEAD.** Tight is ★. LE dies on \(v_n\). [`L-DOOR.md`](L-DOOR.md). |
| LX door \(\|L\|_2\le C X\) | **NO** as a seated \(C\). Not a boxed kill. |
| Instantaneous \(MN\) / above-below \(\Lambda\) | **DEAD** as a uniform \(\theta<1\). \(N=0\) on \(v_n\). [`MN-CANCEL.md`](MN-CANCEL.md). |
| Signed vertices \(R_{\mathrm{sign}}\) | **NO** as a useful \(K\). Saturates \(\sim 0.31\). |
| \(t=0\) jet of \(N,T_c\) | **NO** as a useful \(K\). Stokes keeps \(N=0\). Euler generates \(N\). \(T_c\) grows. Not a G4 death. [`PATHWISE.md`](PATHWISE.md). |
| Short Stokes / NSE interval | **NO** as a useful \(K\). Stokes keeps \(N=0\). NSE keeps \(R_{mn}=1\). Large-amp \(K_{1/2}\) grows. Not a G4 death. [`INTERVAL.md`](INTERVAL.md). |
| Incoming DA-NS-2 as a theorem | **NO.** Y-cousin target. Tautological \(K\) forbidden. [`CENTERED-LEDGER.md`](CENTERED-LEDGER.md). |
| Two-shell \(\alpha+\beta=\Lambda\) zero | **NO** as a two-shell zero. \(\Lambda\) is a convex combination. [`CENTERED-LEDGER.md`](CENTERED-LEDGER.md). |
| Chart reset of \(W_K\) as a useful \(K\) | **NO.** Jump is exact. \(K_{\min,\theta}\) is chart-invariant. Not a G4 death. [`RESET.md`](RESET.md). |
| \(r\sim\kappa^{-1/2}\) crossover as a useful \(K\) | **NO.** Equivalence of three writings. \(r\) is scale-invariant; the threshold is not. BROAD is not a payment. No primitive for \(S_\Gamma\). [`WIDTH.md`](WIDTH.md). |
| SBP / \(\Phi_e\) as a useful \(K\) | **NO.** Elementary rewrite if the \(\dot H^{1/2}\) flux holds. Moves the tail. \(\Phi_e/Y\) is not controlled by \(r^2\). Residual still charge and moving \(N\). [`SBP.md`](SBP.md). |
| Y-remainder cousin (pathwise \(K_Y\)) | **OPEN.** Same circularity test. |
| Unrestricted \(\star\) | **DEAD.** |
| C10 \(\Rightarrow\) this estimate | **NO** without an inequality. C10 did not seat (A). |
| Theorem H as a bridge | **DEAD.** Do not work it. |

---

## What this does not do

It does not restore \(\star\).
It does not close leftover 1 or 5.
It does not run a 9D sweep.
It does not merge with C10.
It does not put \(K(t)\) in the PDE.

NS not solved.

---

## Lock

T_c = M − Λ N. D_s = Z − Λ Y.
Keep the centering.
Target T_c ≤ θν D_s + K(t) X, θ<1,
K useful and in L¹_loc.
If that estimate sits, Lambda' <= 2K.
Unrestricted ★ stays killed.
C10 did not seat (A). No crossover.
NS not solved.
