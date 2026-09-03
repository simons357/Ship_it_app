# Domain Architect machine (the experiment)

You do not have to know the chops. Domain Architect sets the math of the **process**. Ordinary AI is the generator. Scripts are the checker. You are the operator.

This is not “DA unifies the forces.” That stay is still shelved. This is: how far can an operator who is not a specialist go with ordinary AI, if every claim is forced into a slot and a fail-able check.

That is the valuable datum. It is also the shape of “use AI to work on problems,” not “AI said it is solved.”

---

## What DA decided (the setup)

A **domain** is a pair \((X,V)\):

- \(X\) — one mathematical object (one PDE, one matrix, or one score)
- \(V\) — a verdict map from a proposal to \(\{\mathrm{pass},\mathrm{fail},\mathrm{open}\}\)

A **proposal** is a finite string the AI is allowed to emit: a lemma, a numerical check, a subset of knobs, a forbidden-move report. Not a vibe.

A **run** is \((d,p,v)\): domain, proposal, verdict. The log is the experiment.

Meta-success is **not** a solved PDE. It is

\[
S_{\mathrm{meta}}=\bigl(N_{\mathrm{scored}},\,N_{\mathrm{fail}},\,N_{\mathrm{pass}},\,N_{\mathrm{open}}\bigr)
\]

plus a list of any open item that later got a stronger lemma. If the AI cannot be scored, the machine failed, not the operator.

---

## Slots DA will accept

| Slot | Object \(X\) | What the AI may propose | Checker \(V\) |
|---|---|---|---|
| **A** | \(Q_1\) NS, \(\varepsilon>0\) | Energy identity, short Galerkin run | `augmented_ns_verify.py`, E1–E5 |
| **B** | Classical NS, keep \(1/r^4\) | LP / Bony / Ring / tube lemmas | No regularity pass exists. \(V\) may only **fail** a forbidden close or mark **open** |
| **Q** | Inverse-GCD | Bridge*, Theorem P, \(H_N\ge-1\) | `spectral_floor_explore.py` |
| **U** | Realization score \(R\) | Which knobs lock \(R\) | `unifier_exercise.py`, `unifier_combo.py` |

Glue is refused: A does not imply B, Q does not imply fluids, U does not unify the forces.

SFE, HB, prize packaging, and “I solved NS/RH” are not slots. They bounce.

---

## Forbidden closes (auto-fail)

The checker fails the proposal, without discussion, if it asserts any of:

- classical 3D NS is globally regular
- \(\lambda_{\min}(Q_N)>-1/2\) or \(\lambda_{\min}(\widetilde Q_N)>-1/2\) for all \(N\)
- Biot–Savart forces \(\cos\alpha_3\to 0\) for all data
- bounded \(\|\omega\|_2\) implies Beale–Kato–Majda
- \(\int\mathcal{E}\,dt<\infty\) kills cubic enstrophy blowup
- SFE / UHF / DHFA implies a fluids or coupling map
- Track A \(\Rightarrow\) Track B, or Bridge* \(\Rightarrow\) SND

Open is allowed. Fail is allowed. A fake pass is not.

---

## How you run it (no chops)

```
python3 scripts/da_machine.py status
python3 scripts/da_machine.py check
python3 scripts/da_machine.py classify --claim "the prime block of Q-tilde sits above -1/4"
python3 scripts/da_machine.py log --domain Q --claim "Theorem P" --verdict pass --note "script certificate"
```

`status` shows the slots. `check` runs every checker that exists. `classify` is DA assigning a slot and a pre-verdict from the claim text. `cosmos` drills the ~16 Cosmo knobs (`docs/DA-COSMOS-DRILL.md`). `sixteen` identifies a 4×4 list, runs each slot, and names the 16th (`docs/DA-SIXTEEN.md`). `fingers` does five-finger DA on the realization line and recurses (`docs/DA-FINGERS.md`). `fate` gives each of the 16 a category and a general fate, then breaks the pieces (`docs/DA-SIXTEEN-FATE.md`). `how` lists the only legal reasons a typed catalog can say “possible” and emit a finite \(X\) (`docs/DA-HOW-IT-KNEW.md`). `flush` ranks combinations by Born weight (`docs/DA-FLUSH.md`). `wave` adds superposition / entanglement / collapse / falsification rules without touching A/B/Q (`docs/DA-WAVE.md`). `game` runs Shapley on the score versus the unifier-claim game (`docs/DA-GAME.md`). `screen` runs published unification claims through gauge3 vs nature4 (`docs/DA-SCREEN.md`). `gq` starts at gravity + quantum and names what is coupled (`docs/DA-GRAVITY-QUANTUM.md`). `separate` runs each pair, published claim, and slot alone (`docs/DA-SEPARATE.md`). `log` writes one run into `results/da_machine_log.json`.

You point ordinary AI at one slot. It proposes. You run `classify` and `check`. The log is the record of how far this process got.

---

## What would count as the machine working

- The AI’s sentence lands in exactly one slot.
- A script returns pass or fail in finite time.
- A fail is recorded, not rewritten into a pass.
- An open item stays open until a real lemma or a real counterexample.

That is already a result about AI-for-problems, whether or not any PDE closes.