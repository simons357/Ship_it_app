# Field glue

`python3 scripts/track_b_field_glue.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
B9 typed two columns. This write asks the field.

---

## The knob on this write

While CONC the sketch says

\[
\dot X=\alpha_c(j_*)X^3-\nu\,2^{2j_*}X,
\]

with \(\alpha_c(j_*)=0.4\cdot 2^{2-j_*}\) for \(j_*\ge 2\).
NS says \(\dot X=2\int\omega\cdot S\omega-2\nu\|\nabla\omega\|_2^2\).

Same box as B13 / B9b: \(n=32\), \(X=2.5\), \(\nu=0.1\),
typed \(j_*=2\) on the packet. The blob uses typed
\(j_*=3\). \(j_{\mathrm{bar}}\) is reported, not
substituted. Substituting it is climbing (B11).

Tesla: sign of \(\dot X\) is a number. \(\alpha_c\) versus
\(2P/X^3\) is a different number. Turn the typed \(j_*\).
If the sketch grows and the field falls, you do not have
an a priori.

No \(Q_1\). No \(\varepsilon\). No retune of \(\alpha_c\)
into the PDE.

---

## What the apparatus does

**B19, pass.** Both rates readable. Packet \(\sigma=1\),
blob \(\sigma\approx 0.85\). Still CONC.

**B19a, fail** of “the \(j_*=2\) model has the same sign
of \(\dot X\) as the NS packet.” Model \(\dot X=+2.25\).
NS \(\dot X\approx-22.5\). The sketch points up. The
field points down.

**B19b, fail** of “the working-box packet is the B9b
blowup.” Eight steps: model \(X\) grows \(2.5\to 2.67\).
NS \(X\) falls \(2.5\to 1.43\).

**B19c, fail** of “\(\alpha_c\) is the field cubic.”
Implied \(\alpha=2P/X^3\) sits near \(0\) on the packet
(cancellation) and \(\approx 0.006\) on the blob. The
sketch used \(0.4\) and \(0.2\).

**B19d, fail** of “\(\nu 2^{2j_*}X\) is \(2\nu\|\nabla\omega\|_2^2\)
on the \(j_*=2\) packet.” \(2D/(\gamma X)\approx 5.6\).
Bernstein-scale \(\gamma\) under-counts a fat packet.
\(j_{\mathrm{bar}}\) sits near \(3\). That is a scale
reading, not a climb law.

**B19e, fail** of “matching the sketch closes \(X\).”
Scored as B30. A wrong-sign sketch is not
continuation. Shrinking \(\alpha_c\) is a knob.

**B19f, fail** of “this retunes the PDE.” \(\alpha_c\)
is a knob on the estimate.

**B9d, fail** of “the glued model is a closed a priori.”
A sketch that points the wrong way on the packet it
named is not an a priori.

---

## They work it

**Tesla.** You typed \(j_*=2\) and the cubic won. The
field at that box did not. Detune the typed scale. Do
not call \(j_{\mathrm{bar}}\approx 3\) a free upgrade.
That is another write.

**Ladyzhenskaya.** Same weight failed on the sketch.
The field paid more viscosity than \(\nu 2^{2j_*}\).
I still will not give you \(\varepsilon\).

**Leray.** They used my dissipation. It owned \(\dot X\).
The leftover cubic in the sketch was not my integral.

**Majda.** Random-phase cancellation killed \(\alpha_c\)
on the packet. The blob’s one-sided \(P\) is still not
\(0.2\,X^3\).

**Kato.** High \(j_*\) short was a scale on the ODE.
This packet did not sit at the typed \(j_*\) the ODE
used. Do not glue that into a climb.

**Beale.** Nobody votes a wrong-sign sketch into
\(X\in L^\infty\).

**Feynman.** Missable: sign of \(\dot X\),
\(\alpha_{\mathrm{imp}}/\alpha_c\), and \(2D/(\gamma X)\).
All readable. The a-priori slogan missed.

**Einstein.** The object stayed the classical field.
The ODE stayed a model.

**Operator.** Field glue is scored. B9d is scored.
B19e is scored. NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Next: finer box (B22e). Finer is B22e.
B4c stands. Do not cancel to \(\Phi\).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B9d | **fail** | glued model is an NS a priori |
| B19 | **pass** | both \(\dot X\) readable |
| B19a | **fail** | \(j_*=2\) model sign matches NS |
| B19b | **fail** | NS packet is the B9b blowup |
| B19c | **fail** | \(\alpha_c\) is the field cubic |
| B19d | **fail** | \(\nu 2^{2j_*}X\) is NS visc |
| B19e | **fail** | matching the sketch closes \(X\) |
| B19f | **fail** | this retunes the PDE |
| domain B | **open** | finer leftover is B22e |

Tesla’s line: the \(j_*=2\) sketch grows. The NS packet
falls. Sign of \(\dot X\) is the knob.
