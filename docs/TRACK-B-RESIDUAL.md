# Residual tool — the holes in \(\mathcal{R}\)

`python3 scripts/track_b_residual.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
Leftover knobs are scored. The leftover is a closed
estimate for \(X\). This write is an apparatus on that
blank: split the unknown into three named holes and
read them on the working box.

No \(Q_1\). No \(\varepsilon\). Do not spawn \(n=64\).

---

## The missing piece

\[
\frac{d}{dt}X+\nu\|\nabla\omega\|_2^2
\le \varepsilon\nu\|\nabla\omega\|_2^2
+C_\varepsilon X\cdot\mathcal{R}(t).
\]

\(\mathcal{R}\) must be integrable. It is not known to be.
The stretching leftover is the only term that can beat
viscosity. Split it:

\[
\int\omega\cdot S\omega
=
\underbrace{\text{hole 1}}_{\text{aligned }P_+\text{ on }E_c}
+
\underbrace{\text{hole 2}}_{\text{unaligned }P_+\text{ on }E_c}
+
\underbrace{\text{hole 3}}_{\text{off }E_c}.
\]

Tesla: name the holes. Detune a share. The script must
move. Reading is not a bound.

---

## What the apparatus does

Same caches as B15 / B16. \(n=32\). No new FFT.

**B37, pass.** The three holes are readable together.
Hole 1 (aligned cap of \(P_+\)) is the majority.
Weighted \(|\cos\alpha_3|\) exceeds the unweighted mean
(CF still weights). Net \(\lvert P\rvert/D\) is small and
\(\dot X<0\) on this ensemble (visc still owns the net).
Hole 1 + hole 2 \(=1\) on \(E_c\).

**B37a, fail** of “naming the holes is a closed estimate.”
A synthetic split is an apparatus. \(\mathcal{R}\) is still
the unknown.

**B37b, fail** of “readable holes make \(\mathcal{R}\)
integrable.” Readability is not integrability. Hole 2 is
the live cubic. Hole 1 is still an if. Hole 3 is not
all-data Hardy.

**B37c, fail** of “the synthetic \(\mathcal{R}\) is an NS
a priori.” A skeleton with blanks is not a type.

**B37d, fail** of “the residual tool is
\(\int\|\omega\|_\infty\).” Named holes are not the max.

**B37e, fail** of “the residual tool decides regularity.”
No. Domain B stays open.

**B37f, fail** of “this retunes the PDE.” Knob on the
check.

**B38, pass.** Miller \(\lambda_2^+\) is a different cut
from hole 2 on the same eigh. Hole 2 is \(\sim 35\%\) of
\(P_+\) on \(E_c\). The \(\lambda_2^+\) share is \(\sim 50\%\).
The \(e_2\)-aligned share is \(\sim 9\%\). Hole 1\((t)\) on
the B15 cache stays a majority while visc eats \(X\).
No new FFT. No \(n=64\).

**B38a, fail** of “the Miller cut is a closed estimate.”
The identity is not an a priori. A strain model with the
same identity blows.

**B38b, fail** of “a different cut makes \(\mathcal{R}\)
integrable.” A gap of \(0.15\) on this ensemble is not
\(\int\|\lambda_2^+\|_{L^q}<\infty\).

**B38c, fail** of “reading \(\lambda_2^+\) is an NS a priori.”
Keeping an eigenvalue is a knob on the check.

**B38d, fail** of “the Miller cut is \(\int\|\omega\|_\infty\).”

**B38e, fail** of “the Miller cut decides regularity.”
No. Domain B stays open.

**B38f, fail** of “this retunes the PDE.” Knob on the
check.

**B39, pass.** Miller identity \(\int\omega\cdot S\omega=-4\int\det S\)
holds to machine precision. \(\det_+\) is the same cut as
\(\lambda_2^+\) (gap \(\lt 0.05\)). The next rename is empty.
Sit down.

**B39a, fail** of “identity plus empty rename is a closed
estimate.”

**B39b, fail** of “an empty rename makes \(\mathcal{R}\)
integrable.” A1 and A2 are still the blanks.

**B39c, fail** of “reading \(\det S\) is an NS a priori.”

**B39d, fail** of “the empty rename is \(\int\|\omega\|_\infty\).”

**B39e, fail** of “sitting down decides regularity.”
No. Domain B stays open.

**B39f, fail** of “this retunes the PDE.” Knob on the
check.

---

## They work it

**Tesla.** You asked for another tool. Here it is: three
numbers you can miss. They moved. They did not write
\(\mathcal{R}\).

**Feynman.** Missable: hole 1 majority, weighted greater
than unweighted, \(\lvert P\rvert/D\) small. All held.
The a-priori slogan missed.

**Fefferman.** Hole 1 is still an if. Do not glue it to
Biot–Savart.

**Leray.** I own the net on these packets. I did not hand
you all data.

**Miller.** \(\lambda_2^+\) is not hole 2. \(\det_+\) is
\(\lambda_2^+\). Do not cash the rewrite.

**Operator.** The holes are named. The Miller cut is a
different cut. The next rename is empty. Sit down.
Regularity stays open. Do not spawn \(n=64\). B4c
stands. Do not cancel to \(\Phi\).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B37 | **pass** | three holes of \(\mathcal{R}\) readable on \(n=32\) |
| B37a | **fail** | naming the holes is a closed estimate |
| B37b | **fail** | readable holes make \(\mathcal{R}\) integrable |
| B37c | **fail** | synthetic \(\mathcal{R}\) is an NS a priori |
| B37d | **fail** | residual tool is \(\int\|\omega\|_\infty\) |
| B37e | **fail** | residual tool decides regularity |
| B37f | **fail** | this retunes the PDE |
| B38 | **pass** | \(\lambda_2^+\) is a different cut from hole 2 |
| B38a | **fail** | the Miller cut is a closed estimate |
| B38b | **fail** | a different cut makes \(\mathcal{R}\) integrable |
| B38c | **fail** | reading \(\lambda_2^+\) is an NS a priori |
| B38d | **fail** | Miller cut is \(\int\|\omega\|_\infty\) |
| B38e | **fail** | Miller cut decides regularity |
| B38f | **fail** | this retunes the PDE |
| B39 | **pass** | identity holds; \(\det_+\) is \(\lambda_2^+\) |
| B39a | **fail** | empty rename is a closed estimate |
| B39b | **fail** | empty rename makes \(\mathcal{R}\) integrable |
| B39c | **fail** | reading \(\det S\) is an NS a priori |
| B39d | **fail** | empty rename is \(\int\|\omega\|_\infty\) |
| B39e | **fail** | sitting down decides regularity |
| B39f | **fail** | this retunes the PDE |
| domain B | **open** | regularity stays open |

Tesla’s line: name the holes. The Miller cut moved.
The next rename is empty. Sit down.
