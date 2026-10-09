# Gate D — Resource-Weighted Turnover Lemma

8 October 2026 (corrections from 9 Oct review).
**VALID TARGET — not a proved lemma. Not (17).**

Parent deficit:
[`GATE-C-HALF-DERIVATIVE-2026-10-08.md`](GATE-C-HALF-DERIVATIVE-2026-10-08.md).

Adversarial protocol:
[`GATE-D-TURNOVER-ADVERSARIAL-TEST-2026-10-08.md`](GATE-D-TURNOVER-ADVERSARIAL-TEST-2026-10-08.md).

Review: [`GATE-D-REVIEW-2026-10-09.md`](GATE-D-REVIEW-2026-10-09.md).

Program: [`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).

Sources recovered:
[`sources/NS_ORBIT_R4_SMALL_DATA_2026-09-20.md`](sources/NS_ORBIT_R4_SMALL_DATA_2026-09-20.md),
[`sources/NS_EPISODE_BALANCE_NOTE_2026-09-20.md`](sources/NS_EPISODE_BALANCE_NOTE_2026-09-20.md),
Signed-Gate packet under `handoff/gate-d-signed-packet-2026-10-08/`.

---

## Deficit and scale bridge

\[
\boxed{\text{We need a dynamical mechanism worth one half derivative.}}
\]

**Bridge.** Onset \(O(\rho^{-2})\) is an **amplitude** statement; the
obstruction is a **frequency** statement \(H^{1/2}\). Connect them.

### Sharp coherent packet (Gate C), \(E=1\)

\[
X\sim H^2,\qquad
Y\sim H^4,\qquad
\mathcal T_{\mathrm{sc}}\sim H^{9/2},
\qquad
\frac{\mathcal T_{\mathrm{sc}}}{X}\sim H^{5/2}.
\]

Viscosity alone: \(\tau_\nu\sim H^{-2}\) gives
\(H^{5/2}\cdot H^{-2}=H^{1/2}\) — still short by a half derivative.

Bernstein / concentration: \(\|\nabla u\|_\infty\sim H^{5/2}\) ⇒
\[
\boxed{\tau_{\mathrm{nl}}\sim H^{-5/2}.}
\]
Dimensional match (not a proof):
\[
H^{5/2}\times H^{-5/2}\sim 1.
\]

**Correction (9 Oct):** an effective-window estimate
\(\lvert I\rvert\lesssim H^{-5/2}\) is a **duration diagnostic only**.
It is **not** equivalent to the resource-weighted lemma
\(B_I\le C\mathcal R_I\) with \(\sum\mathcal R_I\) controlled.
Duration match alone does not close recurrence.

---

## Target theorem (not stamped)

\[
\boxed{\textbf{Resource-Weighted Turnover Lemma}}
\]

Find a nonnegative resource \(\mathcal R_I\) such that the two obligations
\[
B_I=\int_I d(t)\,dt\le C\mathcal R_I,
\qquad
\sum_I\mathcal R_I\le C_{\mathrm{data},\nu,T}
\]
hold with constants uniform in the Galerkin cutoff. Critical \(H^{-5/2}\)
turnover is a duration scale. It can match the static \(H^{1/2}\) loss on
one window. It does not by itself pay for repetition. The resource must
pay for repeated episodes without reusing the same budget.

Preferred working form (resource-weighted; duration not interchangeable):
\[
\int_I
\frac{[\mathcal T_{\mathrm{sc}}-\nu Y/4]_+}{X}\,dt
\le C\,\mathcal R_I
\]
with \(\sum_I\mathcal R_I\) controlled. Record
\(H^{5/2}\lvert I\rvert\) as a separate diagnostic — never as a
substitute for \(\mathcal R_I\).

Budget consequence **if** both obligations hold, with the same uniformity
in the Galerkin cutoff:
\[
\sum_I B_I
\le C\,C_{\mathrm{data},\nu,T}
\]
⇒ control of \(\mathcal S_{K,N}(T)\).

---

## Mathematical gap (open)

No large-packet (Gate-C / six-box scale) resource has yet been shown to
pay for **repeated** episodes. The small-\(\ell^1\) Orbit-R4 prototype
\(\int UW\,dt\le U_0^2/(2(\nu-U_0))\) remains restricted-class only.

Next decisive test: a completed, corrected episode followed through
regeneration. Fast turnover alone cannot settle recurrence. The resource
must pay for repeated episodes without reusing the same budget.
Solver setup corrections do not supply that episode. Status:
implementation corrected; dynamical evidence pending.

---

## Prototype already in the archive

In the small Fourier-\(\ell^1\) class (`NS_ORBIT_R4_SMALL_DATA_2026-09-20`,
**Source-backed**), the quartic remainder satisfies
\[
\lvert R_4\rvert\lesssim UWX,
\]
while dynamics supplies an integrated bound on \(UW\). Resource:
\[
\mathcal R\sim\int UW\,dt
\]
— summable on that class. That is the pattern to imitate for all-high
scalene episodes — **not yet established** for the six-box packet.

---

## Exact episode identity (archive)

From `NS_EPISODE_BALANCE_NOTE_2026-09-20` (**Source-backed**).
For an episode \((a,b)\) with \(D(a)=0\), \(D>0\) inside, \(X>0\):
\[
B_I
=
\int_a^b(b-s)
\left[
\frac{Q_\Sigma}{X}
+\frac{V}{X}
+\frac{M}{X}
-\frac{DX'}{X^2}
\right]ds.
\]

**Correction (9 Oct) — restore the initial boundary term.**
If an episode starts at initial time with \(d(a)>0\), add
\[
(b-a)\,d(a)
\]
to the first-time-moment integral. Do not omit it. Adversarial first
episodes from the signed packet typically begin with \(D(0)>0\), so this
term is live.

---

## Program stack (what Gate D is now)

\[
\boxed{
\text{static deficit}
\to H^{1/2}
\to
\text{critical turnover }H^{-5/2}
\to
\textbf{find the resource that pays for recurrence}.
}
\]

---

## Adversarial packet (decisive test)

Still use the coherent Gate-C six-box packet — Gaussian not substituted.
Do **not** ask only \(\lvert I_H\rvert\stackrel{?}{\lesssim}H^{-5/2}\).
Score the family by the measured ratio
\[
\boxed{
\frac{B_{I_H}}{\mathcal R_{I_H}}
}
\]
and whether \(\sum\mathcal R_I\) stays globally finite.
Coarse “\(O(1)\) versus \(o(1)\)” slogans are insufficient (9 Oct).

Also record \(H^{5/2}\lvert I_H\rvert\) as a **duration diagnostic only**.

Pipeline:
\[
\text{coherent Gate-C packet}
\to
\text{exact }D(0),D'(0)
\to
B_{I_H}/\mathcal R_{I_H}\text{ with }B_I=\int d.
\]

Core question:
\[
\boxed{\textbf{Does nonlinear turnover supply exactly the missing half derivative?}}
\]
— and what resource pays when it must happen again.

---

## Execution status (9 Oct)

| Item | Status |
|---|---|
| Sources (Orbit R4, episode balance, Signed-Gate) | **Recovered — blocker closed** |
| Static author sweep | Filed (exponents only; not episode cost) |
| Prior top-\(M\) Euler “episodes” | **Demoted** — not full-trajectory evidence |
| Solver setup ( \(B_I=\int d\), Orszag, fixed \(K\) ) | **Corrected** — not Gate D evidence |
| Six-box corrected episode through regeneration | **Unrun** |
| Next decisive test | Completed corrected episode, then regeneration, without reusing the same resource |

See [`GATE-D-REVIEW-2026-10-09.md`](GATE-D-REVIEW-2026-10-09.md),
[`GATE-D-FULL-TRAJECTORY-SOLVER.md`](GATE-D-FULL-TRAJECTORY-SOLVER.md).

---

## Not the next target

Shell-count; Young reshuffles; generic instantaneous phase;
52/70/100 families; random-phase fishing; Ring / swirl-as-substitute;
B41→NSE; Gaussian as substitute for six-box.

---

## STATUS

GATE D: VALID TARGET; LEMMA NOT STAMPED.
NEED: \(B_I=\int d\le C\mathcal R_I\) AND \(\sum\mathcal R_I\le C_{\mathrm{data},\nu,T}\),
CONSTANTS UNIFORM IN THE GALERKIN CUTOFF.
SCORE: \(B_I/\mathcal R_I\).
DURATION ≢ RESOURCE. FAST TURNOVER DOES NOT PAY FOR RECURRENCE.
IMPLEMENTATION CORRECTED; DYNAMICAL EVIDENCE PENDING.
NEXT TEST: COMPLETED CORRECTED EPISODE THROUGH REGENERATION.
(17) NOT CLAIMED.
NS NOT SOLVED.
