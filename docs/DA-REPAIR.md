# DA repair — take the work you already put in

`python3 scripts/da_machine.py repair`  
`python3 scripts/da_machine.py repair --job A`  
`python3 scripts/da_machine.py repair --job SND`  
`python3 scripts/da_machine.py repair --job H`  
`python3 scripts/da_machine.py next --ask "what's wrong with the augmented one"`

What has to sit to close A / RH / SND / H, Einstein and Tesla reviewing: [`DA-ATTEMPT.md`](DA-ATTEMPT.md). `python3 scripts/da_machine.py attempt --job SND`.

You already did the work. You have heard “closed” on
the augmented system about a half-dozen times. DA
names the fault and the repair write.

---

## A — augmented / \(Q_1\)

**Have.** Theorem A **pass** for this PDE
(\(\varepsilon>0\), \(\beta\ge 1/2\)). Energy, Galerkin,
unique \(H^1\), \(C^\infty\). That close is real. That is
what you heard.

**Fault.** The extra term leaves as \(\varepsilon\to 0\).
Lemma 4’s constant blows up. `A_uniform_H1` is **open**.
`A_implies_B` **fails**. Calling A classical NS is the
fake close.

**Repair.** Write a bound on \(\|u\|_{H^1}\) that stays
finite as \(\varepsilon\to 0\), or a named no-go. That
write stays on A. Do not export Olga onto B.

**To close.** This PDE: already closed. Classical NS:
uniform \(H^1\), then a **separate** Track B argument.
Not a slide.

Catalog: [`TRACK-A-LEMMAS.md`](TRACK-A-LEMMAS.md)  
Gap: [`TRACK-A-GAP.md`](TRACK-A-GAP.md)

---

## SND

**Have.** August CONC (\(\inf J/X\ge c_*\)) and June
SPREAD (\(\rho\le\rho_0<1\)) were both called SND.

**Fault.** One word for opposites. Bridge* glued to SND.
\(\Phi\) put in front of H. SIMPLEX used GCD arithmetic.

**Repair.** Two names: CONC (\(\sigma\ge 1/2\)) and
SPREAD (\(\sigma<1/2\)). Cut \(\Phi\) and \(Q\). Do
not reattach Bridge*. Do not quote displayed
SND-C as proved. Rebuild from the exact
shell equation:
[`SND-H-REVIEW.md`](SND-H-REVIEW.md).

**To close.** A two-regime a priori. Neither side is
yet an all-data bound on \(X\).

---

## H — two objects

**Have.** Fluids Theorem H was written as
SND-C in SPREAD (Bony \(T+T^*+R\)).
That displayed estimate is **not
established** even with \(X\le M\):
[`SND-H-REVIEW.md`](SND-H-REVIEW.md).
\(F_j\) bound sits; \(D^+\rho\) is a
ceiling, not a floor:
[`SND-H-REPAIR.md`](SND-H-REPAIR.md).
Arithmetic Theorem H-floor:
\(\lambda_{\min}(H_N)\ge-1\), proved.

**Fault.** Fluids: proof drops the viscous
tail \(S_j\); invalid 3-D embeddings;
incomplete Bony split; Theorem F too
strong; \(\Phi\)-glue. Arithmetic:
\(-3/14\) false; \(Q>-1/2\) false.

**Repair.** Fluids: keep the original
extract as an extract. Rebuild the
needed bound from the exact shell
equation. The \(F_j\) input sits; the
propagation argument is unwritten:
[`SND-H-REPAIR.md`](SND-H-REPAIR.md).
Do not remove \(M\) from the
same quadratic estimate. Do not claim
a universal SND floor from \(t=0\).
Arithmetic: keep \(H_N\ge-1\); to sharpen,
prove \(H_N\ge-1/4\). Do not revive
\(-3/14\).

**To close.** Fluids: a rebuilt estimate
tested on shears, amplitude, and equal
shells; still not a bound on \(X\).
Arithmetic: \(-1\) already sits; \(-1/4\)
is the remaining floor.

Plan: [`UNAUGMENTED-R4-VORTICITY-PLAN.md`](UNAUGMENTED-R4-VORTICITY-PLAN.md)  
Floor: [`SPECTRAL-FLOOR-EXPLORATION.md`](SPECTRAL-FLOOR-EXPLORATION.md)

---

## Scored

| Claim | Verdict |
|---|---|
| DA can take the operator's A / SND / H work and name the fault | **pass** |
| DA can name the repair write for each job | **pass** |
| Repairing A is exporting Olga onto classical NS | **fail** |
| Calling both statements SND is the repair | **fail** |
| Repair H by reviving \(Q>-1/2\) or \(H\ge-3/14\) | **fail** |
| Hearing Theorem A closed means classical NS is done | **fail** |
| `A_uniform_H1` may sit later | **open** |
| Uniform SND-C in SPREAD may sit later | **fail** as displayed. \(F_j\) bound sits; propagation unwritten: [`SND-H-REVIEW.md`](SND-H-REVIEW.md), [`SND-H-REPAIR.md`](SND-H-REPAIR.md). |
| \(H_N\ge-1/4\) may sit later | **open** |
