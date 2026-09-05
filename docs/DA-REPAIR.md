# DA repair — take the work you already put in

`python3 scripts/da_machine.py repair`  
`python3 scripts/da_machine.py repair --job A`  
`python3 scripts/da_machine.py repair --job SND`  
`python3 scripts/da_machine.py repair --job H`  
`python3 scripts/da_machine.py next --ask "what's wrong with the augmented one"`

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
SPREAD (\(\sigma<1/2\)). Cut \(\Phi\) and \(Q\). Write
SND-C only in SPREAD: uniform low paraproduct as
\(\rho\to 0\). Do not reattach Bridge*.

**To close.** A two-regime a priori. Neither side is
yet an all-data bound on \(X\).

---

## H — two objects

**Have.** Fluids Theorem H = SND-C in SPREAD (Bony
\(T+T^*+R\)). Arithmetic Theorem H-floor:
\(\lambda_{\min}(H_N)\ge-1\), proved.

**Fault.** Fluids: Theorem F too strong; low Bony \(T\)
not uniform as \(\rho\to 0\); \(\Phi\)-glue. Arithmetic:
\(-3/14\) false; \(Q>-1/2\) false. Those were fake closes.

**Repair.** Fluids: delete B/C/I/\(\Phi\); write uniform
SND-C on \(\mathbb{T}^3\), SPREAD, no \(\varepsilon\).
Arithmetic: keep \(H_N\ge-1\); to sharpen, prove
\(H_N\ge-1/4\). Do not revive \(-3/14\).

**To close.** Fluids: uniform SND-C. Arithmetic:
\(-1\) already sits; \(-1/4\) is the remaining floor.

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
| Uniform SND-C in SPREAD may sit later | **open** |
| \(H_N\ge-1/4\) may sit later | **open** |
