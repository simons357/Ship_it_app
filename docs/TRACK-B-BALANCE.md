# Enstrophy balance

`python3 scripts/track_b_balance.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
Geometry weighted \((\omega\cdot S\omega)_+\). Fluids
look at the net.

---

## The knob on this write

The classical identity

\[
\dot X=2\int_{\mathbb{T}^3}\omega\cdot S\omega
-2\nu\|\nabla\omega\|_2^2.
\]

Same B13-scale 3-CONC packets (\(n=32\), \(j_*=2\),
\(X=2.5\), \(\nu=0.1\)). No \(Q_1\). No \(\varepsilon\).
No BKM-from-\(L^2\).

Tesla: net production is a number. The share of a
leftover is not the cubic.

---

## What the apparatus does

**B16, pass.** A tiny IF-RK2 step matches
\(\dot X=2P-2D\) at relative residual \(\sim 2\cdot 10^{-4}\).
That is the fluids identity. Geometry started from a
share. This is the balance.

**B16a, pass.** On these packets,
\(\lvert\int\omega\cdot S\omega\rvert\ll\nu\|\nabla\omega\|_2^2\)
and \(\dot X<0\). Leray’s dissipation owns the net.
Same ensemble the stretching budget was read on.

**B16b, fail** of “the aligned \((\omega\cdot S\omega)_+\)
budget is a large net cubic.” Plus and minus stretch
cancel at \(\sim 10^{-3}\). One-sided \(P_+\) is still
\(\sim 0.2\%\) of dissipation. The \(65\%\) share is
\(65\%\) of a leftover that nets near zero.

**B16c, fail** of “an \(L^2\) packet bound is BKM.”
\(\|\omega\|_\infty/\|\omega\|_2\) sits near \(0.2\) on a
fat packet. Beale–Kato–Majda ask for
\(\int\|\omega\|_\infty\). Do not improve them into
\(L^2\).

**B16d, fail** of “random-phase cancellation is an a
priori for every 3-CONC field.” This ensemble is random
phase. A coherent vortex can have
\(P\approx(\omega\cdot S\omega)_+\). Fluids did not
promote a packet to a class.

**B16e, open.** Viscosity owned this ensemble. That is
not continuation. The tube (B5b) is still a different
weight.

**B16f, fail** of “this retunes the PDE.” The equation
is untouched. Cancellation is a knob on the estimate.

---

## They work it

**Leray.** You used my dissipation. You did not ask my
\(\int X\) to do \(L^\infty\). Good. On these packets
the cubic cancels and viscosity owns the net. Jean,
that is a reading of an ensemble. It is not my theorem
extended.

**Majda.** Random phase is not a vortex. The stretching
mechanism is still the mechanism. Do not sit
cancellation as a geometric class. Charlie, Peter —
your \(65\%\) was real as a share of \(P_+\). The net
is a different integral.

**Beale.** And nobody here turns \(\|\omega\|_2\) into
our criterion. The ratio \(\|\omega\|_\infty/\|\omega\|_2\)
is small because the packet is fat. That is not
\(\int\|\omega\|_\infty<\infty\).

**Kato.** The identity held. The slogan “B15 closes the
cubic” did not. Tosio is satisfied when the check can
fail. It failed the slogan. It passed the identity.

**Caffarelli.** A decaying random packet is not a
singular set. Partial regularity stays a wall.

**Ladyzhenskaya.** Viscosity paid. I still will not
give you \(\varepsilon\). The tube is a different
weight: \(1/r^4\) against \(1/r^2\). That is B5b. These
Cartesian packets did not answer it.

**Constantin.** We weighted the plus pile. Fluids asked
for the signed integral. Both numbers stand. Do not
glue them.

**Fefferman.** Do not call cancellation depletion.
Depletion would empty the cap. Cancellation is plus
against minus.

**Tesla.** Two knobs. Share, then net. Share moved
(\(0.50\to 0.81\)). Net sat at \(\sim 10^{-3}\). You can
miss the second number if you stop at the first.

**Feynman.** Missable: \(\lvert P\rvert/D\),
\(\lvert P\rvert/(P_++P_-)\), and
\(\|\omega\|_\infty/\|\omega\|_2\). All readable. The
cubic slogan missed.

**Einstein.** The object stayed the classical field.

**Operator.** Fluids looked. The budget is not the
balance. Next is the tube that was already open (B5b).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B16 | **pass** | enstrophy identity on a packet |
| B16a | **pass** | viscosity owns the net on this ensemble |
| B16b | **fail** | aligned \(P_+\) is a large net cubic |
| B16c | **fail** | \(L^2\) packet is BKM |
| B16d | **fail** | random-phase \(\Rightarrow\) all CONC |
| B16e | **open** | balance closes \(X\) |
| B16f | **fail** | this retunes the PDE |
| domain B | **open** | B5b (tube geometry) |

Tesla’s line: net production is a number. The share of
a leftover is not the cubic.
