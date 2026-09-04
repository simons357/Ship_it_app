# Geometry on CONC packets

`python3 scripts/track_b_geometry.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
Ring Lipschitz was already real (B3). This write asks
what else the strain eigenframe will give.

---

## The knob on this write

Read \(\xi=\omega/|\omega|\) against the strain
eigenvectors on \(E_c=\{|\omega|\ge c\|\omega\|_{\mathrm{rms}}\}\).
Same classical 3-shell CONC packets. No \(Q_1\).
No \(\varepsilon\). No Biot–Savart slogan.

Tesla: alignment is a number. If you cannot miss it,
it is a paragraph.

---

## What the apparatus does

**B14, pass.** On \(E_c\),

\[
\xi\cdot S\xi=\sum_{i=1}^3\lambda_i\cos^2\alpha_i.
\]

Eigenframe residual is roundoff (\(\sim 10^{-13}\)).
Geometry starts here. This is not depletion.

**B14a, fail** of “3-CONC \(\Rightarrow\) median
\(|\cos\alpha_3|\le 0.25\).” Median sits near \(1/2\):
random on the sphere, not depleted. CONC is a spectrum,
not an alignment.

**B14b, fail** of “Ring Lipschitz of \(\xi\) on \(E_c\)
forces \(\cos\alpha_3\to 0\).” B3 bounds
\(\|\nabla\xi\|_\infty\lesssim 2^{j_*}\). Direction slowly
varying is not direction aligned. Same slogan as B3b.

**B14c, pass.** Constantin–Fefferman as a conditional.
On \(E_c\), samples with \(|\cos\alpha_3|<0.25\) stretch
less, relative to \(|\lambda|_{\max}\), than samples with
\(|\cos\alpha_3|>0.8\) (roughly \(0.46\) versus \(0.65\)).
IF less aligned with extension, stretching is smaller.
Not all-data.

**B14d, fail** of “packet geometry closes \(X\).”
Lipschitz plus a conditional is not continuation.
See [`TRACK-B-ALIGN.md`](TRACK-B-ALIGN.md).

**B14e, fail** of “this retunes the PDE.” The equation
is untouched. Geometry is a knob on the estimate.

---

## They work it

**Constantin.** Three shells give Lipschitz direction
where vorticity is large. That is real. Peter, does it
force the “if”?

**Fefferman.** No. Median \(|\cos\alpha_3|\) on these
packets is about one half. The “if” is still an if.
When the if holds, stretching is smaller. That is the
theorem we wrote. Do not glue it to Biot–Savart.

**Tesla.** Then alignment is a knob. You can miss
\(0.25\). The packets miss it.

**Feynman.** Two missable numbers: median
\(|\cos\alpha_3|\) versus \(0.25\), and the stretch
ratio low versus high. Both readable. Neither closes
\(X\).

**Ladyzhenskaya.** I still will not give you
\(\varepsilon\). A conditional is not extra dissipation.

**Majda.** CONC stayed a spectrum. Do not promote it
to a geometric class.

**Beale.** A smaller stretching efficiency on a subset
of \(E_c\) is not \(\|\omega\|_\infty\in L^1\).

**Einstein.** The object stayed the classical field.

**Operator.** Geometry is scored. B14d is scored.
The budget is scored (B15e). The net is scored
(B16e). The blob is scored (B17e). Field occupation is not an a priori (B18e). Field glue is not an a priori (B19e). NS climb is not an a priori (B20e). Climb sketch is not an a priori (B21e). Next: regularity stays open. Alignment is a conditional, not
a close.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B14 | **pass** | strain identity on \(E_c\) |
| B14a | **fail** | 3-CONC \(\Rightarrow\) depleted \(\cos\alpha_3\) |
| B14b | **fail** | Ring Lipschitz \(\Rightarrow\) alignment |
| B14c | **pass** | CF conditional: small \(\lvert\cos\alpha_3\rvert\) stretches less |
| B14d | **fail** | geometry closes \(X\) |
| B14e | **fail** | this retunes the PDE |
| domain B | **open** | regularity stays open |

Tesla’s line: alignment is a number. If you cannot miss
it, it is a paragraph.
