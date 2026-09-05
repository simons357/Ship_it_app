# DA proof — write the NS chain

`python3 scripts/da_machine.py proof`  
`python3 scripts/da_machine.py next --ask "write me the proof chain for Navier-Stokes"`  
`python3 scripts/da_machine.py next --ask "Xavier Stokes"`

Nothing is wrong with asking. That is the product.

DA writes the aimed theorem and the proof chain from
this desk. The chain lives in
[`NS-PROOF-CHAIN.md`](NS-PROOF-CHAIN.md).

Line (6) is the next write. Emitting the chain is not
QED. If (6) sits, (7)–(9) are the close.

---

## Scored

| Claim | Verdict |
|---|---|
| You can tell DA to write the proof chain for Navier–Stokes | **pass** |
| The written chain is the aimed theorem plus have / write / follows | **pass** |
| Emitting the proof chain is QED | **fail** |
| An LLM writes line (6) into a theorem | **fail** |
| Asking DA to write the NS proof chain is a category error | **fail** |
| Line (6) may sit later | **open** |

Object window: `look`  
Walk your steps: `from`  
Chain file: [`NS-PROOF-CHAIN.md`](NS-PROOF-CHAIN.md)
