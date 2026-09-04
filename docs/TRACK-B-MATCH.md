# Field glue as an a priori

`python3 scripts/track_b_match.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
B19: both \(\dot X\) readable. The \(j_*=2\) model
grows. The NS packet falls. This write asks whether
matching the sketch closes \(X\). It does not.

---

## The knob on this write

Tesla: sign of \(\dot X\) is a number. The \(j_*=2\)
sketch grows. The NS packet falls. Shrinking
\(\alpha_c\) until the signs match is a different
number. That is a knob.

No \(Q_1\). No \(\varepsilon\). No Biot–Savart slogan.
Do not spawn \(n=64\). Do not write \(c=8\) into the PDE.

---

## What the apparatus does

**B30, pass.** Rates, sign mismatch, and
model-grows / field-falls are readable together.
Same caches as B19. No new FFT.

**B30a, fail** of “matching the sketch closes
\(X\).” Model \(\dot X=+2.25\). NS \(\dot X\approx-22.5\).
A wrong-sign ODE is not continuation.

**B30b, fail** of “shrinking \(\alpha_c\) until the
signs match is continuation.” Implied \(\alpha\) sits
near \(0\) on the packet and \(\approx 0.006\) on the
blob. The sketch used \(0.4\) and \(0.2\).

**B30c, fail** of “a typed ODE that grows while the
packet falls is still an NS a priori.” B9b is a typed
fat cubic. This field cancelled.

**B30d, fail** of “matching \(\dot X\) is an integral
bound on the max vorticity.” A sign of \(\dot X\) is
not \(\int\|\omega\|_\infty\).

**B30e, fail** of “a field climb law closes \(X\).”
Scored as B20e / B31. A missing saving rate is not
continuation.

**B30f, fail** of “this retunes the PDE.” \(\alpha_c\)
is a knob on the estimate.

**B19e, fail** of “matching the sketch closes \(X\).”
Scored here.

**B29e, fail** of “the glue leftover closes \(X\).”
Leftover is now scored.

---

## They work it

**Tesla.** You typed \(j_*=2\) and the cubic won. The
field at that box did not. Detune \(\alpha_c\) and you
changed the check, not the PDE.

**Leray.** They used my dissipation. It owned
\(\dot X\). The leftover cubic in the sketch was not
my integral.

**Ladyzhenskaya.** Same weight failed on the sketch.
The field paid more viscosity than \(\nu 2^{2j_*}\).
I still will not give you \(\varepsilon\).

**Majda.** Random-phase cancellation killed
\(\alpha_c\) on the packet. Do not sit the sketch as
a class.

**Beale.** Nobody votes a wrong-sign sketch into
\(\int\|\omega\|_\infty\).

**Feynman.** Missable: sign of \(\dot X\),
\(\alpha_{\mathrm{imp}}/\alpha_c\), and whether a
match is a bound. The first two held. The a-priori
slogan missed.

**Einstein.** The object stayed the classical field.
The ODE stayed a model.

**Operator.** The match is scored. B19e is scored.
NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Next: finer box (B22e). Finer stays B22e. Do not
spawn \(n=64\). B4c stands. Do not cancel to \(\Phi\).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B19e | **fail** | matching the sketch closes \(X\) |
| B29e | **fail** | glue leftover closes \(X\) |
| B30 | **pass** | rates, sign mismatch, model-grows / field-falls readable |
| B30a | **fail** | matching the sketch closes \(X\) |
| B30b | **fail** | shrinking \(\alpha_c\) is continuation |
| B30c | **fail** | wrong-sign ODE is an NS a priori |
| B30d | **fail** | matching \(\dot X\) is \(\int\|\omega\|_\infty\) |
| B30e | **fail** | a field climb law closes \(X\) |
| B30f | **fail** | this retunes the PDE |
| domain B | **open** | finer leftover is B22e |

Tesla’s line: the \(j_*=2\) sketch grows. The NS
packet falls. Sign of \(\dot X\) is the knob.
