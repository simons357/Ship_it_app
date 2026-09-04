# Climb law from the field

`python3 scripts/track_b_climb_law.py`  
`python3 scripts/da_machine.py trackb`

Dated 4 September 2026. The PDE is not being tuned.

---

## The knob on this write

\(c\) the **packet** makes. Not a \(c\) we type.

Read the vorticity RHS on a 3-shell CONC field. Form
the enstrophy barycenter \(j_{\mathrm{bar}}\) and its
instantaneous drift. That is \(\mathrm{d}j_{\mathrm{bar}}/\mathrm{d}t\).
Tesla: ask the field. If it does not move toward the
saving rate, do not write \(c=8\) into the estimate.

B11c sat at a prescribed \(c=8\). This write asks
whether the classical field produces that.

---

## What the apparatus does

On a packet, shells of \(\omega\) carry masses \(X_j\).

\[
j_{\mathrm{bar}}=\frac{\sum j\,X_j}{X},\qquad
c=\frac{\mathrm{d}}{\mathrm{d}t}j_{\mathrm{bar}}
\]

from \(\partial_t\omega=-(u\cdot\nabla)\omega+(\omega\cdot\nabla)u+\nu\Delta\omega\).

**B12, pass.** \(j_{\mathrm{bar}}\) sits next to \(j_*\).
\(\sigma=1\) on a 3-shell field.

**B12a, pass.** \(c\) is a finite number from the RHS.
The apparatus reads.

**B12b, fail** of “random CONC at \(t=0\) produces
\(c\ge 8\).” None do. Euler drift is \(\sim 10^{-4}\)
even at \(X=40\). Viscous drift is about \(-1.4\).

**B12c, fail** of “viscosity is a ladder.” High shells
damp faster. \(j_{\mathrm{bar}}\) falls.

**B12d, fail** of “a short evolution produces a
saving climb.” Broken out as B13. Short missed.
Longer missed. DNS is not an a priori (B13f).

**B12e, fail** of “the \(t=0\) drift is a climb law
for classical \(X\).” A reading is not a law. The
path did not write one either.

---

## They work it

**Tesla.** You typed \(c=8\) and the model sat. I asked
the field. It went the other way. That is a knob.

**Ladyzhenskaya.** Viscosity eats the thin shells first.
It is not a hoist. I still will not give you
\(\varepsilon\).

**Feynman.** Missable numbers: \(\max c\) versus 8, and
whether every viscous packet is negative. You can get
both wrong.

**Leray.** Energy is still \(E\). This drift is not
\(\int X\).

**Majda.** They stayed CONC. The clock was not the
cheat.

**Beale.** A falling barycenter is not a criterion
in \(L^\infty\).

**Einstein.** The object stayed the classical field.
You read it. You did not retune it.

**Operator.** The field did not hand us the saving
climb at \(t=0\). Short and longer runs are scored.
DNS is not an a priori. Finer is B22e.

---

## Score

| id | Verdict | What it is |
|---|---|---|
| B12 | **pass** | \(j_{\mathrm{bar}}\) is readable |
| B12a | **pass** | \(c\) from the RHS |
| B12b | **fail** | \(t=0\) packets produce \(c\ge 8\) |
| B12c | **fail** | viscosity forces an upward climb |
| B12d | **fail** | a short evolution produces a saving climb |
| B12e | **fail** | \(t=0\) drift is an NS a priori |
| domain B | **open** | finer (\(n>32\)) is a box knob (B22e) |

Tesla’s line: ask the field. Do not type the answer.
