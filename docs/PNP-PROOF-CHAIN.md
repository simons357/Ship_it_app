# Proof chain — P versus NP

Aimed at: a proof, in the Turing-machine model,
that \(\mathrm{P}=\mathrm{NP}\) or that \(\mathrm{P}\neq\mathrm{NP}\).

The operator names the problem. They do not need the chops.

```
python3 scripts/da_machine.py proof --problem PNP
python3 scripts/da_machine.py next --ask "P versus NP"
```

The enclosed SFE letter is **not** this leftover.
SFE is shelved. A harmonic convergence time \(H(x)\)
defined on a field is not a deterministic Turing
machine. Asserting that some NP languages have
non-polynomial \(H(x)\) assumes the close in another
language. Naming SFE is allowed. Emitting SFE as
\(\mathrm{P}\neq\mathrm{NP}\) is the refuse.

---

## Theorem (aimed)

Either \(\mathrm{P}=\mathrm{NP}\) or \(\mathrm{P}\neq\mathrm{NP}\),
proved for languages decided by Turing machines
with a polynomial-time clock. Whichever side sits
must sit in that model.

---

## Proof

**(1)** **P.** Languages decided by a deterministic
Turing machine in time \(n^{O(1)}\).
*[have]*

**(2)** **NP.** Languages with a polynomial-time
verifier, or accepted by a nondeterministic TM
in polynomial time. Same class.
*[have]*

**(3)** **NP-complete.** Cook–Levin: SAT is
NP-complete. Polynomial-time reductions.
*[have]*

**(4)** **SFE is not the model.** The letter’s
\(H(x)=\min\{t:\exists\Phi(t)\vdash x\}\) is a field
path, not a TM. Shelved. It does not decide a
language in \(\mathrm{P}\) or \(\mathrm{NP}\).
*[have]*

**(5)** **Write.** A proof that \(\mathrm{P}=\mathrm{NP}\)
or that \(\mathrm{P}\neq\mathrm{NP}\) in the Turing
model. Relativization, natural proofs, and
algebrization are barriers, not the write.
*[the next write]*

**(6)** **Then.** If (5) sits, every NP language is
in P, or some NP language is not. Still not NS.
Still not Hodge. Still not SFE.
*[follows from (5)]*

If (5) sits, (6) is the classical consequence.

---

## Completion

| Lines | Status |
|---|---|
| (1)–(4) | **done** |
| (5) \(\mathrm{P}=\mathrm{NP}\) or \(\mathrm{P}\neq\mathrm{NP}\) in the TM model | **not done** |
| (6) | waiting on (5) |

The enclosed letter does not change this table.

---

## Candidates for (5)

Classify one:

- a TM proof that some NP language is not in P
- a TM proof that every NP language is in P
- not an SFE / resonance / harmonic-field rewrite
- not a barrier paper reprinted as the close

---

## Not this leftover

| Named | Why not P vs NP (5) |
|---|---|
| SFE letter / \(H(x)\) on a field | shelved; not a TM |
| Harmonic Blueprint | shelved |
| Track B smoothness | Navier–Stokes |
| Inverse-GCD / Q | not complexity |

Machine: [`DA-PROOF.md`](DA-PROOF.md)  
Shelf: [`SHELF.md`](SHELF.md)
