# Track A lemmas — \(Q_1\)-augmented NS

`python3 scripts/da_machine.py tracka`

Augmented system only. Theorem A is for **this PDE**.
Uniform \(H^1\) as \(\varepsilon\to 0\) stays **open**.
A does not imply B. Olga stays on A.

Chain: [`AUGMENTED-NS-PROOF-CHAIN.md`](AUGMENTED-NS-PROOF-CHAIN.md)  
Checker: `python3 scripts/da_machine.py check --domain A`

---

## Scored

| id | Statement | Verdict |
|---|---|---|
| A1 | energy identity | **pass** |
| A2 | Galerkin global | **pass** |
| A3 | weak limit is a weak solution | **pass** |
| A4 | unique \(H^1\) at \(\varepsilon>0\), \(\beta\ge 1/2\) | **pass** |
| A5 | \(C^\infty\) bootstrap | **pass** |
| A_theorem | Theorem A for this PDE | **pass** |
| A_E1–E5 | Taylor–Green consistency | **pass** on the short window |
| A_uniform_H1 | Lemma 4 stays uniform as \(\varepsilon\to 0\) | **open** |
| A_implies_B | Theorem A is classical regularity | **fail** |
| A_phi_estimate | \(\Phi\) is the estimate variable | **fail** |
| A_export_olga | export Ladyzhenskaya onto classical NS | **fail** |

---

## Live leftover on A

The \(H^1\) constant of Lemma 4 depends on \(\varepsilon\) and
blows up as \(\varepsilon\to 0\). That gap is the only open
row. A uniform bound, or a named no-go, would move it.
Neither sits.

That write stays on A. It is not a B residual and it is not
leftover-close B42.

---

## What this is not

Not classical NS. Not \(\Phi\). Not inverse-GCD. Not a
retune of `nodes.json`.
