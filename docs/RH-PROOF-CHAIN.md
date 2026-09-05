# Proof chain — Riemann hypothesis

Aimed at: every non-trivial zero of zeta has real part \(1/2\).

The operator names the problem. They do not need the chops.

```
python3 scripts/da_machine.py proof --problem RH
python3 scripts/da_machine.py next --ask "RH proof chain please"
```

Track Q on this desk is inverse-GCD. Theorem P is not RH.
Do not glue.

---

## Theorem (aimed)

Every non-trivial zero of the Riemann zeta function
has real part equal to \(1/2\).

---

## Proof

**(1)** **Zeta.** Riemann zeta is meromorphic, simple
pole at \(s=1\), Euler product for \(\operatorname{Re}s>1\).
*[have]*

**(2)** **xi.** The completed \(\xi\)-function is entire
of order 1 and satisfies \(\xi(s)=\xi(1-s)\).
*[have]*

**(3)** **Strip.** Every non-trivial zero lies in
\(0<\operatorname{Re}s<1\).
*[have]*

**(4)** **Prime number theorem.** No zeros on
\(\operatorname{Re}s=1\) (Hadamard / de la Vallée Poussin).
*[have]*

**(5)** **The line.** Infinitely many zeros on
\(\operatorname{Re}s=1/2\) (Hardy). A positive proportion
sit on the line (Conrey and later). Literature, not a
theorem of this desk.
*[have]*

**(6)** **Write.** Every non-trivial zero has
\(\operatorname{Re}s=1/2\).
*[the next write]*

**(7)** **Explicit formula.** If (6) sits, the
von Mangoldt explicit formula has all oscillatory
terms on the critical line.
*[follows from (6)]*

**(8)** **Error term.** The prime-counting error is then
of the classical Riemann order (up to logs).
*[follows from (6)]*

If (6) sits, (7)–(8) are the classical consequences.

---

## Candidates for (6)

Classify one:

- a zero-free region that reaches \(\operatorname{Re}s=1/2\)
- a positivity certificate in the explicit formula that forces the line
- one new estimate that puts every zero on \(\operatorname{Re}s=1/2\)

Do not use Theorem P, Bridge*, or a full \(Q\)-floor.
Those are inverse-GCD. Different object.

Machine: [`DA-PROOF.md`](DA-PROOF.md)  
NS chain: [`NS-PROOF-CHAIN.md`](NS-PROOF-CHAIN.md)
