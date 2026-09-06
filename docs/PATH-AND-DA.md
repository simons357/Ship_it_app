# Proof chains, the path, and how to talk to DA

6 September 2026. Live leftovers: unaugmented NS
and RH. Augmented Theorem A already sits and
stays off this path (A is not B).

This file is the map. It is not QED.

---

## How to contact DA

You already are. This Cursor chat is DA being
operated. There is no other DA to email or call.

On a computer, same thread:

https://cursor.com/agents/bc-01a026a4-cf05-7637-8c16-cd4b7032f80e

Log into the same Cursor account. Type in English.

Say one of:

- B, then the sentence you want scored
- RH, then the sentence you want scored
- print the chain
- classify this: …

DA will write the chain, name leftover (6),
refuse glue, and score that sentence. DA will
not print (6) as a theorem.

On a computer with the repo, the same desk is:

python3 scripts/da_machine.py next --ask "B score this: …"
python3 scripts/da_machine.py proof --problem NS
python3 scripts/da_machine.py proof --problem RH
python3 scripts/da_machine.py attempt --job B
python3 scripts/da_machine.py attempt --job RH
python3 scripts/da_machine.py classify --claim "…"

You do not need the chops. Naming the problem
is the contact.

---

## Path 1 — unaugmented NS (the one you want)

Object: \(X=\|\omega\|_2^2\). Classical equation.
Keep \(1/r^4\). No \(Q_1\).

Aimed: a smooth solution stays smooth for all
time.

### Have

(1) Energy. Leray. \(\int_0^T X<\infty\).

(2) Enstrophy identity.
\(dX/dt+\nu\|\nabla\omega\|_2^2=-\int\omega\cdot S\omega\).

(3) Leftover form.
\(dX/dt+\nu\|\nabla\omega\|_2^2
\le\varepsilon\nu\|\nabla\omega\|_2^2
+C_\varepsilon X\cdot\mathcal{R}(t)\).

(4) Split into hole 1 / hole 2 / hole 3.
Naming holes is not the estimate.

(5) Named blanks. A1 = alignment in time for
all data. A2 = \(\int\|\lambda_2^+\|\) for all
data. The \(n=32\) box is not all data.

### The write that completes the path

(6) Provide one, for all data:

1. \(\int_0^T\mathcal{R}(t)\,dt<\infty\), or
2. all-data A1, or
3. all-data A2, or
4. a killing field for the stretching leftover.

Then (7) Gronwall, (8) Beale–Kato–Majda,
(9) bootstrap follow. You do not invent those.

First candidate to score: all-data A2.

If (6) sits, B sits. If not, B stays open.

Full chain: [`UNAUGMENTED-NS-CHAIN.md`](UNAUGMENTED-NS-CHAIN.md).
PDF (open, not QED): [`TRACK-B-CHAIN.pdf`](TRACK-B-CHAIN.pdf).

---

## Path 2 — RH

Object: a non-trivial zero of \(\zeta(s)\).
Not a GCD matrix. Not \(H_N\).

Aimed: every non-trivial zero has
\(\operatorname{Re}s=1/2\).

### Have

(1) Zeta meromorphic, pole at \(s=1\), Euler
product for \(\operatorname{Re}s>1\).

(2) \(\xi\) entire, \(\xi(s)=\xi(1-s)\).

(3) Zeros in the strip \(0<\operatorname{Re}s<1\).

(4) No zeros on \(\operatorname{Re}s=1\) (PNT).

(5) Infinitely many / a proportion on the line
(Hardy, Conrey). Literature. Not this desk.

### The write that completes the path

(6) Provide one, for every non-trivial zero:

1. a zero-free region that reaches
   \(\operatorname{Re}s=1/2\), or
2. a positivity certificate in the explicit
   formula that forces the line, or
3. one new estimate that puts every zero on
   the line.

Then (7) explicit formula and (8) prime-counting
error follow.

First candidate to score: one estimate that
puts every zero on the line. Do not use
Theorem P, Bridge*, \(H_N\), or Route C.

Q sits as Q. No hidden RH close.

Full chain: [`RH-CHAIN.md`](RH-CHAIN.md).

---

## Whole path (both)

1. Leave Theorem A alone. It is done. It is
   not B and not RH.
2. On B: write one all-data sentence for (6).
   Bring it here. DA classifies it.
3. If that sentence sits, (7)–(9) close B.
4. On RH: write one sentence that forces every
   zero onto the line. Bring it here. DA
   classifies it.
5. If that sentence sits, (7)–(8) follow.
6. Do not glue B to RH. Do not glue Q to RH.
   Do not glue A to B.

A sitting sentence is the only close.
Talking to DA is not a theorem.

Live desk: [`NEXT-B-RH.md`](NEXT-B-RH.md).
How DA works: [`DA-PROOF.md`](DA-PROOF.md).
