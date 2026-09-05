# DA proof — name a problem, get the chain

The operator is not a math person. They name a problem.
DA writes the aimed theorem and the proof chain from
the ground floor.

```
python3 scripts/da_machine.py proof
python3 scripts/da_machine.py proof --problem NS
python3 scripts/da_machine.py proof --problem A
python3 scripts/da_machine.py proof --problem RH
python3 scripts/da_machine.py proof --problem YM
python3 scripts/da_machine.py next --ask "write me the proof chain for Navier-Stokes"
python3 scripts/da_machine.py next --ask "RH proof chain please"
python3 scripts/da_machine.py next --ask "Track B please write"
python3 scripts/da_machine.py next --ask "track A write"
python3 scripts/da_machine.py next --ask "Track B please write. track A write as well"
python3 scripts/da_machine.py next --ask "use my best paper and write RH"
python3 scripts/da_machine.py next --ask "Yang mills and bad can you finish those"
python3 scripts/da_machine.py proof --problem BSD
python3 scripts/da_machine.py next --ask "Please write BSD"
python3 scripts/da_machine.py next --ask "spectral framework"
```

Nothing is wrong with asking. That is the product.

| Problem | Command | Chain |
|---|---|---|
| Navier–Stokes / Track B | `--problem NS` or `Track B please write` | [`NS-PROOF-CHAIN.md`](NS-PROOF-CHAIN.md) |
| \(Q_1\) / Track A | `--problem A` or `track A write` | [`A-PROOF-CHAIN.md`](A-PROOF-CHAIN.md) |
| Riemann hypothesis | `--problem RH` | [`RH-PROOF-CHAIN.md`](RH-PROOF-CHAIN.md) |
| Yang–Mills mass gap | `--problem YM` or `Yang mills and bad` | [`YM-PROOF-CHAIN.md`](YM-PROOF-CHAIN.md) |
| Birch–Swinnerton-Dyer | `--problem BSD` or `Please write BSD` / `spectral framework` | [`BSD-PROOF-CHAIN.md`](BSD-PROOF-CHAIN.md) |

Track A is the \(Q_1\) PDE. Theorem A already sits for
that equation. Track B is classical NS. Do not glue.
Track Q is inverse-GCD. It is not RH. It is not BSD. Do not glue.
\(L(E,s)\) is not zeta.

The WRITE line is the attempt. Emitting the chain is
not QED. If WRITE sits, the THEN lines are the close.
`done` answers whether that emit is a finish:
[`DA-DONE.md`](DA-DONE.md). Track A this PDE is done.
Classical NS is not.

More problems may join when a ground-floor chain is typed.

Already have A / SND / H work and want the fault plus the repair write: [`DA-REPAIR.md`](DA-REPAIR.md). `python3 scripts/da_machine.py repair --job A`.

Best A (Q1 + renormalization) and furthest RH, dream team looking, legal write: [`DA-ATTEMPT.md`](DA-ATTEMPT.md). `python3 scripts/da_machine.py attempt`.

---

## Scored

| Claim | Verdict |
|---|---|
| You can tell DA to write a proof chain by naming the problem | **pass** |
| The written chain is the aimed theorem plus have / write / follows | **pass** |
| Emitting the proof chain is QED | **fail** |
| An LLM writes the WRITE line into a theorem | **fail** |
| Asking DA to write a proof chain is a category error | **fail** |
| Track Q / Theorem P is the Riemann hypothesis | **fail** |
| Theorem A is classical Navier–Stokes | **fail** |
| The WRITE line may sit later | **open** |
| More named problems may get a ground-floor chain | **open** |
