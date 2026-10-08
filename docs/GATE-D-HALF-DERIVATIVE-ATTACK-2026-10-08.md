# Gate D — Turnover Lemma / height × duration

8 October 2026.
**ACTIVE shot — refined. Not (17).**

Parent deficit:
[`GATE-C-HALF-DERIVATIVE-2026-10-08.md`](GATE-C-HALF-DERIVATIVE-2026-10-08.md).

Program: [`PROGRAM-GATES-A-D.md`](PROGRAM-GATES-A-D.md).

Archive pointer (not in this workspace binary):
`NS_EPISODE_BALANCE_NOTE_2026-09…` — exact episode identity below
(**Source-backed** from author note).

---

## Deficit and scale bridge

\[
\boxed{\text{We need a dynamical mechanism worth one half derivative.}}
\]

**Important refinement.** The onset law’s \(O(\rho^{-2})\) window is an
**amplitude** statement. The obstruction we must erase is a
**frequency** statement \(H^{1/2}\). Gate D needs an explicit bridge
between those two scales.

### Sharp coherent packet (Gate C) after \(E=1\) normalization

Schematically
\[
X\sim H^2,\qquad
Y\sim H^4,\qquad
\mathcal T_{\mathrm{sc}}\sim H^{9/2}.
\]
Dangerous normalized height:
\[
\frac{\mathcal T_{\mathrm{sc}}}{X}\sim H^{5/2}.
\]

### Two time scales

Viscosity alone gives
\[
\tau_\nu\sim H^{-2}.
\]
Product with height:
\[
H^{5/2}\cdot H^{-2}=H^{1/2}.
\]
There is the missing half derivative again — viscosity is not enough.

So Gate D, sharpened:
\[
\boxed{\text{We need an effective dangerous-window duration of order }H^{-5/2}}
\]
— or an equivalent \(H^{-1/2}\) reduction in episode height.

### Dimensional match — nonlinear turnover

For an \(E=1\) field occupying \(O(H^3)\) modes in a band of size \(H\),
Bernstein-scale estimates naturally give
\[
\|\nabla u\|_\infty\sim H^{5/2}
\]
at the worst concentration scale. Nonlinear turnover time:
\[
\boxed{\tau_{\mathrm{nl}}\sim H^{-5/2}.}
\]
Exactly the scale required. Clean dimensional match (not a proof):
\[
\underbrace{H^{5/2}}_{\text{normalized dangerous height}}
\times
\underbrace{H^{-5/2}}_{\text{nonlinear turnover window}}
\sim 1.
\]

---

## Budget object

\[
\boxed{
\sum_I B_I
\le
C(u_0,\nu,K,T)
}
\]
uniformly in Galerkin cutoff \(N\). That would directly control
\[
\mathcal S_{K,N}(T)
=
\int_0^T
\frac{\bigl[\mathcal T_{\mathrm{sc}}(h_{K,N})-\nu Y_N/4\bigr]_+}{X_N}\,dt.
\]

---

## Gate D target — Turnover Lemma

For a positive all-high scalene episode \(I\) concentrated near frequency
\(H\), prove one of the following equivalent kinds of statements:

\[
|I|\lesssim H^{-5/2}
\]
when the normalized transfer is near its worst-case \(H^{5/2}\) size; or,
more robustly,
\[
\boxed{
\int_I
\frac{[\mathcal T_{\mathrm{sc}}-\nu Y/4]_+}{X}\,dt
\le C\,\mathcal R_I
}
\]
where the resources \(\mathcal R_I\) are summable over episodes.

The second form is better: we do **not** need every episode to carry a
hard duration bound.

---

## Exact episode identity (archive)

From `NS_EPISODE_BALANCE_NOTE_2026-09…` (**Source-backed**; retrieve full
note when available in-workspace):
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
Finite trajectories show block viscosity contributes a large negative
moment and can terminate episodes even while quartic feeding remains
positive. That is the laboratory hint that duration can compress while
instantaneous height looks dangerous.

---

## Onset clue (amplitude side)

Onset law: a dangerous-looking positive crossing can carry only
\(O(\rho^{-2})\) normalized cost on its first shrinking window.
Amplitude growth ≠ budget cost; dynamics compresses the window.
**Bridge still required** to the frequency form \(H^{-5/2}\) above.

---

## Adversarial test (next calculation)

Do **not** test Gate D on an arbitrary field. Use the same coherent
packet that proves the sharp static \(H^{1/2}\) obstruction.

Decisive question:

> Does the configuration that is worst possible **instantaneously**
> also remain dangerous **long enough** to make the time-integrated
> budget bad?

| Outcome | Meaning |
|---|---|
| Episode lasts only \(\sim H^{-5/2}\) | Static obstruction may neutralize itself dynamically |
| Persists \(\gtrsim H^{-2}\) at full height | Gate D in serious trouble |

Pipeline:
\[
\boxed{
\text{coherent Gate-C packet}
\longrightarrow
\text{exact }D(0),\,D'(0)
\longrightarrow
\text{turnover-scale episode law}
}
\]
Measure the scale of
\[
H^{5/2}\lvert I_H\rvert.
\]

The test is not merely “dynamics.” It is:
\[
\boxed{\textbf{Does nonlinear turnover supply exactly the missing half derivative?}}
\]

---

## Not the next target

Shell-count upgrades; Young reshuffles; generic instantaneous phase;
52/70/100 families; random-phase fishing; Ring without bridge;
swirl-as-substitute; B41→NSE.

---

## STATUS

GATE D: ACTIVE — TURNOVER LEMMA.
NEED: DANGEROUS-WINDOW DURATION \(\sim H^{-5/2}\) (OR HEIGHT DROP \(H^{-1/2}\)).
BRIDGE: AMPLITUDE ONSET \(O(\rho^{-2})\) ↔ FREQUENCY \(H^{1/2}\).
NEXT: COHERENT GATE-C PACKET → \(D(0),D'(0)\) → \(H^{5/2}\lvert I_H\rvert\).
(17) NOT CLAIMED.
NS NOT SOLVED.
