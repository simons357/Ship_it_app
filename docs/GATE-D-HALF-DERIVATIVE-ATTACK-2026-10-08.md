# Gate D — Resource-Weighted Turnover Lemma

8 October 2026.
**ACTIVE shot — refined. Not (17).**

Parent deficit:
[`GATE-C-HALF-DERIVATIVE-2026-10-08.md`](GATE-C-HALF-DERIVATIVE-2026-10-08.md).

Adversarial protocol:
[`GATE-D-TURNOVER-ADVERSARIAL-TEST-2026-10-08.md`](GATE-D-TURNOVER-ADVERSARIAL-TEST-2026-10-08.md).

Program: [`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).

Archive pointers (may be absent as binaries here):
`NS_EPISODE_BALANCE_NOTE_2026-09…`, `NS_ORBIT_R4_SMALL_DATA_2026-09…`
(**Source-backed** from author notes).

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

Need:
\[
\boxed{\text{effective dangerous-window duration of order }H^{-5/2}}
\]
(or an equivalent \(H^{-1/2}\) height drop).

Bernstein / concentration: \(\|\nabla u\|_\infty\sim H^{5/2}\) ⇒
\[
\boxed{\tau_{\mathrm{nl}}\sim H^{-5/2}.}
\]
Dimensional match (not a proof):
\[
H^{5/2}\times H^{-5/2}\sim 1.
\]

---

## Target theorem

\[
\boxed{\textbf{Resource-Weighted Turnover Lemma}}
\]

Find a nonnegative resource \(\mathcal R_I\) such that
\[
B_I\le C\,\mathcal R_I,
\qquad
\sum_I\mathcal R_I
\le C(u_0,\nu,K,T).
\]
Then critical \(H^{-5/2}\) turnover can remove the static \(H^{1/2}\)
loss, while the resource pays for **repetition**.

Equivalent episode forms (weaker → stronger for practice):
\[
|I|\lesssim H^{-5/2}
\quad\text{(near worst-case height \(H^{5/2}\))}
\]
or
\[
\int_I
\frac{[\mathcal T_{\mathrm{sc}}-\nu Y/4]_+}{X}\,dt
\le C\,\mathcal R_I
\]
with \(\sum_I\mathcal R_I\) controlled. The resource-weighted form is
preferred: not every episode needs a hard duration bound.

Budget consequence:
\[
\sum_I B_I
\le C(u_0,\nu,K,T)
\quad\text{(uniformly in Galerkin \(N\))}
\]
⇒ control of \(\mathcal S_{K,N}(T)\).

---

## Prototype already in the archive

In the small Fourier-\(\ell^1\) class (`NS_ORBIT_R4_SMALL_DATA_2026-09…`,
**Source-backed**), the quartic remainder satisfies
\[
\lvert R_4\rvert\lesssim UWX,
\]
while dynamics supplies an integrated bound on \(UW\). Resource:
\[
\mathcal R\sim\int UW\,dt
\]
— summable. That is the pattern to imitate for all-high scalene
episodes.

---

## Exact episode identity (archive)

From `NS_EPISODE_BALANCE_NOTE_2026-09…` (**Source-backed**):
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
Finite trajectories: block viscosity can contribute a large negative
moment and terminate episodes even while quartic feeding stays positive.

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

Still use the coherent Gate-C packet — but do **not** ask only
\(\lvert I_H\rvert\stackrel{?}{\lesssim}H^{-5/2}\). Measure
\[
\boxed{
B_{I_H}
\quad\text{and}\quad
\frac{B_{I_H}}{\text{candidate resource consumed on }I_H}
}
\]
as \(H\to\infty\).

| Reading | Meaning |
|---|---|
| \(B_{I_H}\sim O(1)\) | Consistent with critical turnover — not enough alone for infinitely many episodes |
| \(B_{I_H}\to 0\) | Extra dynamical gain — excellent |
| \(B_{I_H}\sim O(1)\) consuming \(O(1)\) of a globally finite resource | Works — only finitely much total episode cost accumulates |
| \(B_{I_H}\sim O(1)\) consuming \(o(1)\) resource | **Gate D in trouble** |

Pipeline:
\[
\text{coherent Gate-C packet}
\to
\text{exact }D(0),D'(0)
\to
B_{I_H}\text{ vs resource on }I_H.
\]

Core question:
\[
\boxed{\textbf{Does nonlinear turnover supply exactly the missing half derivative?}}
\]
— and what resource pays when it must happen again.

---

## Not the next target

Shell-count; Young reshuffles; generic instantaneous phase;
52/70/100 families; random-phase fishing; Ring / swirl-as-substitute;
B41→NSE.

---

## STATUS

GATE D: ACTIVE — RESOURCE-WEIGHTED TURNOVER LEMMA (**RECORDED, NOT STAMPED**).
NEED: \(B_I\le C\mathcal R_I\) WITH \(\sum\mathcal R_I\) CONTROLLED.
CRITICAL SCALE: \(\tau_{\mathrm{nl}}\sim H^{-5/2}\).
ADVERSARIAL EXECUTION: **BLOCKED ON SOURCES** —
[`GATE-D-EXECUTION-BLOCKER.md`](GATE-D-EXECUTION-BLOCKER.md).
(17) NOT CLAIMED.
NS NOT SOLVED.
