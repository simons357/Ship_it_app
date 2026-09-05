# Proof chain — Riemann hypothesis

Aimed at: every non-trivial zero of zeta has real part \(1/2\).

The operator names the problem. They do not need the chops.

```
python3 scripts/da_machine.py proof --problem RH
python3 scripts/da_machine.py next --ask "RH proof chain please"
python3 scripts/da_machine.py next --ask "use my best paper and write RH"
```

Your best paper on this desk is the August inverse-GCD
package (Zenodo 22045478) plus the spectral-floor
retraction. That paper is **Q**. It is not line (6).
Theorem P is not RH. Do not glue.

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

Do not use Theorem P, Bridge*, or a full \(Q\)-floor
as line (6). Those are inverse-GCD. Different object.

---

## From your best paper (Q, not RH)

August inverse-GCD (Zenodo 22045478) plus
[`SPECTRAL-FLOOR-EXPLORATION.md`](SPECTRAL-FLOOR-EXPLORATION.md).

**Sits as Q.**

- Bridge\(^*\): \(R(e_p-e_q)>-1/2\) on \(\widetilde Q\)
- Theorem P: prime-supported \(\widetilde Q\big|_P\ge-1/4\)
- \(H_N=D^{-1/2}\widetilde Q D^{-1/2}\), \(\lambda_{\min}(H_N)\ge-1\)
- \(v\ge 0\Rightarrow v^\top\widetilde Q v\ge 0\)

**Withdrawn.**

- \(\lambda_{\min}(Q_N)>-1/2\) (\(Q_{10}\approx-1.90\))
- \(\lambda_{\min}(H_N)\ge-3/14\) (\(H_4\approx-0.225\))

These are completed Q theorems. They do not put every
non-trivial zero on \(\operatorname{Re}s=1/2\). A GCD
matrix is not a zero. Keep them on Q. Write (6) as RH.

Machine: [`DA-PROOF.md`](DA-PROOF.md)  
NS chain: [`NS-PROOF-CHAIN.md`](NS-PROOF-CHAIN.md)
