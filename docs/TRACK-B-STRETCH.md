# Stretching budget on CONC packets

`python3 scripts/track_b_stretch.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.
B14 read unweighted \(|\cos\alpha_3|\) on a subsample.
This write integrates who pays \((\omega\cdot S\omega)_+\),
then lets the packet run.

---

## The knob on this write

Weight the strain alignment by the cubic’s actual
source. Same classical 3-shell CONC packets. No
\(Q_1\). No \(\varepsilon\). No Biot–Savart slogan.

Tesla: the cubic’s payers are a number. If time
empties the aligned cap, you can miss that. It did
not.

---

## What the apparatus does

**B15, pass.** On \(E_c=\{|\omega|\ge\tfrac12\|\omega\|_{\mathrm{rms}}\}\),
the positive stretching

\[
(\omega\cdot S\omega)_+
\]

is a readable budget. Stretch-weighted
\(|\cos\alpha_3|\) is defined. \(E_c\) at this
threshold already holds most of the torus production.

**B15a, pass.** Stretch-weighted \(|\cos\alpha_3|\)
sits near \(0.81\). Unweighted mean sits near
\(0.50\). Gap \(\gtrsim 0.15\). Constantin–Fefferman
as a **budget**: the cubic pays more where vorticity
meets extension. That is not depletion of the field.

**B15b, pass.** A majority (\(\sim 65\%\)) of
\((\omega\cdot S\omega)_+\) on \(E_c\) comes from
\(|\cos\alpha_3|>0.8\). The depleted cap
\(|\cos\alpha_3|<0.25\) pays \(\sim 3\%\). The aligned
set is a directional minority and a production
majority. Median \(|\cos\alpha_3|\) is still
\(\sim 1/2\).

**B15c, fail** of “a short viscous run depletes
median \(|\cos\alpha_3|\) to \(\le 0.25\).” Median
stays near \(1/2\). Viscosity ate \(X\)
(\(2.5\to\sim 1.43\)). It did not rotate the sphere.

**B15d, fail** of “a short run drops the aligned
share of \((\omega\cdot S\omega)_+\) below \(1/2\).”
\(\mathrm{frac}_{hi}\) stays \(\sim 0.65\). Euler is
frozen. The payers did not leave.

**B15e, fail** of “an aligned stretching budget
closes \(X\).” Scored as B26. A weighted
\(|\cos\alpha_3|\) is not an a priori. Time did
not empty the cap. A share is not continuation.

**B15f, fail** of “this retunes the PDE.” The
equation is untouched. The share is a knob on the
estimate.

---

## They work it

**Constantin.** Unweighted, the direction is random.
Weighted, the cubic sits on the extensional cap.
That is the “if” earning rent. Peter, did time
collect it?

**Fefferman.** No. Eight steps, viscous and Euler.
Median still one half. The majority share still
sits on \(|\cos\alpha_3|>0.8\). Do not call a
weighted budget a depleted field.

**Tesla.** Two knobs. Weight, then time. Weight
moved the number (\(0.50\to 0.81\)). Time did not
(\(0.65\) stayed \(0.65\)).

**Feynman.** Missable numbers: the gap \(0.81-0.50\),
the share \(0.65\) versus \(1/2\), and whether
median fell through \(0.25\). All readable. The
third missed.

**Ladyzhenskaya.** Viscosity paid \(X\). It did not
hand you alignment. I still will not give you
\(\varepsilon\).

**Majda.** CONC is still a spectrum. The budget
being aligned does not make the packet a geometric
class.

**Beale.** A \(65\%\) share on a short packet is not
\(\|\omega\|_\infty\in L^1\).

**Einstein.** The object stayed the classical field.

**Operator.** The budget is scored. B15e is scored.
Next: enstrophy balance (B16e). Finer stays B22e.
Do not spawn \(n=64\). B4c stands. Do not cancel
to \(\Phi\).

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B15 | **pass** | stretching budget on \(E_c\) readable |
| B15a | **pass** | CF weights the budget (\(\sim 0.81\) vs \(\sim 0.50\)) |
| B15b | **pass** | majority of \(+\)stretch from \(\lvert\cos\alpha_3\rvert>0.8\) |
| B15c | **fail** | short run depletes median \(\lvert\cos\alpha_3\rvert\) |
| B15d | **fail** | short run empties the aligned budget |
| B15e | **fail** | budget closes \(X\) |
| B15f | **fail** | this retunes the PDE |
| domain B | **open** | enstrophy-balance leftover is B16e |

Tesla’s line: the cubic’s payers are a number. Time
did not empty them.
