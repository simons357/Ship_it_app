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

**Operator.** The holes are named. Regularity stays open.
Do not spawn \(n=64\). B4c stands. Do not cancel to
\(\Phi\).

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
| domain B | **open** | regularity stays open |

Tesla’s line: name the holes. A script that must move.
Reading is not a bound.
