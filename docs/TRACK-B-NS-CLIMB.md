# NS climb law

`python3 scripts/track_b_ns_climb.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
B11 typed \(c=\mathrm{d}j_*/\mathrm{d}t\). This write asks
the field.

---

## The knob on this write

The B11 model sits if \(c=8\) (B11c) and blows if \(c=1\)
(B11b). That \(c\) was prescribed. Tesla: \(c\) the field
makes, not a \(c\) we type.

Instantaneous

\[
c=\frac{\mathrm{d}j_{\mathrm{bar}}}{\mathrm{d}t}
\]

from the vorticity RHS (B12a). Mean \(c=\Delta j_{\mathrm{bar}}/T\)
on the B18 IF-RK2 paths.

Same box: \(n=32\), \(X=2.5\), \(\nu=0.1\), \(T=0.064\).
Packet typed \(j_*=2\). Blob typed \(j_*=3\).
\(j_{\mathrm{bar}}\) is reported, not substituted.
Substituting it is a static offset, then a fall.

No \(Q_1\). No \(\varepsilon\). Do not write \(c=8\) into
the PDE.

---

## What the apparatus does

**B20, pass.** \(c\) readable. Packet still CONC
(\(\sigma=1\)). Blob still CONC (\(\sigma\approx 0.85\)).

**B20a, fail** of “the signed-strain blob at \(t=0\)
produces \(c\ge 8\).” Viscous \(t=0\) \(c\approx-2\).
Euler \(\approx 0.024\). Coherence of swirl is not a
saving climb.

**B20b, fail** of “mean \(c\) on B18 paths reaches 8.”
Packet visc \(\approx-0.24\). Blob visc \(\approx-2.01\).
Euler means sit near \(0\).

**B20c, fail** of “viscosity on the blob is a ladder.”
\(j_{\mathrm{bar}}\) falls \(2.57\to 2.44\). Same
direction as the \(t=0\) RHS.

**B20d, fail** of “\(j_{\mathrm{bar}}>\text{typed }j_*\)
at \(t=0\) is a climb.” Packet \(j_{\mathrm{bar}}\approx 2.97\)
versus typed \(2\) is a static offset. Then \(j_{\mathrm{bar}}\)
falls. Do not call B19’s scale-reading a free B11c.

**B20e, fail** of “a field climb closes \(X\).”
Scored as B31. The field did not hand us \(c=8\).
A missing saving rate is not continuation.

**B20f, fail** of “this retunes the PDE.” \(c\) is a
knob on the estimate.

**B11d, fail** of “classical NS forces a saving \(c\).”
\(t=0\) packets already failed (B12b). Short visc run
already failed (B13a). Blob and B18 paths fail the same
way. The field did not hand us \(c=8\).

---

## They work it

**Tesla.** You typed \(c=8\) and the ODE sat. The field
at this box went the other way. Detune the apparatus
until the claim can fail. Do not type the saving rate
into the equation. Do not call \(j_{\mathrm{bar}}\approx 3\)
a climb.

**Ladyzhenskaya.** Same weight, both sides, at the scale
you are actually on. I still will not give you
\(\varepsilon\) so you can skip the climb the field
refused.

**Leray.** Viscosity pulled \(j_{\mathrm{bar}}\) down.
That is my dissipation, not a ladder.

**Majda.** The blob stayed CONC. Occupation of CONC is
not a cascade.

**Kato.** High \(j_*\) short was a scale on the ODE.
This packet did not climb there.

**Beale.** Nobody votes a falling barycenter into
\(X\in L^\infty\).

**Feynman.** Missable: \(t=0\) \(c\), \(\Delta j_{\mathrm{bar}}/T\),
and \(j_{\mathrm{bar}}-\text{typed }j_*\). All readable.
The saving-rate slogan missed.

**Einstein.** The object stayed the classical field.
A rate you typed is not a rate the metric produced.

**Operator.** NS climb law is scored. B11d is scored.
B20e is scored. Climb sketch is not an a priori (B21e). Next: DNS leftover (B23e). Finer is B22e.
Do not write \(c=8\) into the PDE. Do not spawn \(n=64\).
B4c stands. Do not cancel to \(\Phi\).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B11d | **fail** | NS forces a saving \(c\) |
| B20 | **pass** | \(c\) readable on blob and paths |
| B20a | **fail** | blob \(t=0\) produces \(c\ge 8\) |
| B20b | **fail** | B18-path mean \(c\ge 8\) |
| B20c | **fail** | visc on the blob is a ladder |
| B20d | **fail** | \(j_{\mathrm{bar}}>\text{typed }j_*\) is a climb |
| B20e | **fail** | field climb closes \(X\) |
| B20f | **fail** | this retunes the PDE |
| domain B | **open** | DNS leftover is B23e |

Tesla’s line: \(c\) the field makes. It did not give
you \(c=8\).
