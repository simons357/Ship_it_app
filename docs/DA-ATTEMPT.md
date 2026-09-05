# DA attempt — your best A and RH, dream team looks, legal write

`python3 scripts/da_machine.py attempt`  
`python3 scripts/da_machine.py attempt --job A`  
`python3 scripts/da_machine.py attempt --job RH`  
`python3 scripts/da_machine.py attempt --job SND`  
`python3 scripts/da_machine.py attempt --job H`  
`python3 scripts/da_machine.py next --ask "what do I need to close SND"`  
`python3 scripts/da_machine.py next --ask "Einstein and Tesla figure out H"`

You asked for the most recent \(Q_1\) work with the
renormalization, and the RH attempt you got furthest
with. DA prints both. The field papers say what they
would do, how, and what they cannot. DA then does the
legal write: correct the errors, restate what already
sits, refuse the glue.

A council does not complete a missing line by agreeing.

Trying every combination on a supercomputer or quantum
device is the same refuse: [`DA-BRUTE.md`](DA-BRUTE.md).

Advice from the published big-picture account in each
area: [`DA-PICTURE.md`](DA-PICTURE.md). A treatise names
the next write. Seeing the whole is not the estimate.

---

## A — \(Q_1\) plus the \(\varepsilon\to 0\) renormalization

**Furthest.** Theorem A **pass** for this PDE
(\(\varepsilon>0\), \(\beta\ge 1/2\)). That close is real.
The latest extra write is the renormalization: send the
extra dissipation to zero (A6: the \(Q_1\) integral
falls) and hope \(H^1\) stays. On the scored box it does
not (A7 fail, A9 fail). `A_uniform_H1` is **open**.

**This PDE.** The chain is already complete.

**The renormalization.** Not complete.

**Classical NS.** Not complete. That is a separate
Track B argument, not a slide.

**Do (augmented).** Stop re-proving Theorem A. Write
\(\|u\|_{H^1}\le C\) with \(C\) independent of
\(\varepsilon\), or a named no-go. Classify it. Run
`tracka`. Do not \(\Phi\). Do not slide onto B. If that
bound sits, classical NS is still a separate leftover.

**Dream team (papers).** Ladyzhenskaya, Málek–Nečas–Růžička,
Temam, Tao, Fefferman, Constantin. Olga already closed
this PDE. She cannot pass \(\varepsilon\to 0\). Tao treats
a regularized cousin as a different equation. Fefferman
sends classical leftover to B.

Catalog: [`TRACK-A-LEMMAS.md`](TRACK-A-LEMMAS.md)  
Gap: [`TRACK-A-GAP.md`](TRACK-A-GAP.md)  
Repair: [`DA-REPAIR.md`](DA-REPAIR.md)

---

## RH — furthest attempt was inverse-GCD

**Furthest.** Classical RH through (5) sits (zeta, \(\xi\),
strip, PNT, Hardy + proportion). The furthest *original*
write on this desk was the inverse-GCD package:
Bridge\(^*\), Theorem P, and the renormalized
\(H_N=D^{-1/2}\widetilde Q D^{-1/2}\) with
\(H_N\ge-1\). Those are completed **Q** theorems. They
were glued to zeros. That glue is the error.
\(Q>-1/2\) and \(H\ge-3/14\) are false.

**RH through (5).** Complete (classical + literature).

**RH WRITE (6).** Not complete. Every non-trivial zero
on \(\operatorname{Re}s=1/2\) is not written.

**Q floors.** Complete as Q. Not as RH.

**Dream team (papers).** Riemann, Hadamard, de la Vallée
Poussin, Hardy, Conrey, Weil. Infinitely many on the
line is not all. A proportion is not RH. A GCD matrix
is not a zero.

Chain: [`RH-PROOF-CHAIN.md`](RH-PROOF-CHAIN.md)  
Floor: [`SPECTRAL-FLOOR-EXPLORATION.md`](SPECTRAL-FLOOR-EXPLORATION.md)

---

## SND — what has to sit

**Need to close.** CONC: all-data stretching bound on
\(\sigma\ge 1/2\). SPREAD: uniform SND-C (low paraproduct
as \(\rho\to 0\)). \(X\) still needs \(\int\mathcal{R}\).
SND sitting is not \(X\).

**Einstein.** Two regimes are two principles. Not one brand.

**Tesla.** Knob: \(\rho\). Script: bound on low Bony \(T\)
as \(\rho\to 0\). Detune \(\rho\). The script must still hold.

---

## H — what has to sit

**Need to close.** Fluids: uniform \(|\Pi_{j^*}|\) in SPREAD
(same write as SND-C). Arithmetic: \(H_N\ge-1\) already
sits. Sharp: \(H_N\ge-1/4\). Do not identify the two H’s.

**Einstein.** Fluids H and \(H_N\) are different additions.

**Tesla.** Fluids knob \(\rho\), script low \(T\). Arithmetic
knob \(N\), script \(\lambda_{\min}(H_N)\). \(-3/14\) is not
a resonator.

---

## Scored

| Claim | Verdict |
|---|---|
| DA can take A, RH, SND, and H and name what closes | **pass** |
| Field papers and program review say would / how / cannot | **pass** |
| DA does the legal corrections and restates what sits | **pass** |
| The \(Q_1\) chain at \(\varepsilon>0\) is already complete | **pass** |
| DA can print what has to sit to close SND and H | **pass** |
| The dream team completes RH WRITE | **fail** |
| The dream team completes `A_uniform_H1` or A\(\Rightarrow\)B | **fail** |
| Einstein and Tesla write SND-C or \(H_N\ge-1/4\) by sitting | **fail** |
| Theorem P or \(H_N\ge-1\) is RH | **fail** |
| Closing SND closes \(X\) | **fail** |
| Fluids H and \(H_N\) are one close | **fail** |
| Experts agreeing write the missing line | **fail** |
| `A_uniform_H1` may sit later | **open** |
| RH WRITE may sit later | **open** |
| Uniform SND-C in SPREAD may sit later | **open** |
| \(H_N\ge-1/4\) may sit later | **open** |
