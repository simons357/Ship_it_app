# Enstrophy balance as an a priori

`python3 scripts/track_b_net.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
B16: \(\dot X=2P-2D\). Viscosity owns the net on
random 3-CONC packets. \(P_+\) is not a net cubic.
This write asks whether that reading closes \(X\).
It does not.

---

## The knob on this write

Tesla: net production is a number. If viscosity owns
an ensemble, you can miss that. It did. A decaying
packet is not a bound for classical \(X\).

No \(Q_1\). No \(\varepsilon\). No Biot–Savart slogan.
Do not spawn \(n=64\).

---

## What the apparatus does

**B27, pass.** Identity, visc-owned net, and cancelled
\(P_+\) are readable together. Same caches as B16.
No new FFT.

**B27a, fail** of “viscosity owning this ensemble
closes \(X\).” \(\dot X<0\) on random phase is a
reading. Leray’s dissipation did the work here.
That is not continuation.

**B27b, fail** of “cancellation is an a priori for
every 3-CONC field.” B16d already missed. A coherent
field can have \(P\approx(\omega\cdot S\omega)_+\).

**B27c, fail** of “a decaying \(L^2\) packet is
continuation.” B23 already refused DNS-never-blew-up.
So does a cancelled net.

**B27d, fail** of “the identity is an integral bound
on the max vorticity.” \(\dot X=2P-2D\) is \(L^2\).
A fat-packet ratio \(\|\omega\|_\infty/\|\omega\|_2\sim 0.2\)
is not \(\int\|\omega\|_\infty\).

**B27e, fail** of “the coherent leftover closes
\(X\).” Scored as B17e / B28. A one-sided leftover
is not continuation.

**B27f, fail** of “this retunes the PDE.” The net is
a knob on the estimate.

**B16e, fail** of “the enstrophy balance closes
\(X\).” Scored here.

**B26e, fail** of “the enstrophy leftover closes
\(X\).” Leftover is now scored.

---

## They work it

**Tesla.** Share moved (\(0.50\to 0.81\)). Net sat
at \(\sim 10^{-3}\). Do not sit a cancelled cubic
as a bound.

**Leray.** You used my dissipation. You did not ask
my \(\int X\) to do \(L^\infty\). Jean, that is a
reading of an ensemble. It is not my theorem
extended.

**Majda.** Random phase is not a vortex. Do not
promote cancellation to a geometric class.

**Beale.** Nobody votes \(\|\omega\|_2\) into
\(\int\|\omega\|_\infty\). The packet is fat. That
is why the ratio is small.

**Ladyzhenskaya.** Viscosity paid. I still will not
give you \(\varepsilon\).

**Feynman.** Missable: \(\lvert P\rvert/D\), the
cancel ratio, and whether decay is a bound. The
first two held. The a-priori slogan missed.

**Einstein.** The object stayed the classical field.
A balance is not a closed estimate.

**Operator.** The net is scored. B16e is scored.
The blob is scored (B17e). Field occupation is not
an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Next: finer box (B22e).
Finer stays B22e. Do not spawn \(n=64\).
B4c stands. Do not cancel to \(\Phi\).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B16e | **fail** | balance closes \(X\) |
| B26e | **fail** | enstrophy leftover closes \(X\) |
| B27 | **pass** | identity, visc-owned net, cancelled \(P_+\) readable |
| B27a | **fail** | visc owning this ensemble closes \(X\) |
| B27b | **fail** | cancellation is all-data |
| B27c | **fail** | decaying \(L^2\) packet is continuation |
| B27d | **fail** | identity is \(\int\|\omega\|_\infty\) |
| B27e | **fail** | coherent leftover closes \(X\) |
| B27f | **fail** | this retunes the PDE |
| domain B | **open** | finer leftover is B22e |

Tesla’s line: net production is a number. Viscosity
owned this ensemble. That is not continuation.
