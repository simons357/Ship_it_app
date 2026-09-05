# Proof chain — Q6 spectral floor

Q6 hygiene: August inverse-GCD (Zenodo 22045478).
Slot **Q**. Not RH. Not SND. Not Track B.

```
python3 scripts/da_machine.py q
python3 scripts/da_machine.py next --ask "Q6. Spectral floor"
```

Long form: [`SPECTRAL-FLOOR-EXPLORATION.md`](SPECTRAL-FLOOR-EXPLORATION.md).

---

## Theorem (sits)

\(\lambda_{\min}(H_N)\ge-1\) for every \(N\ge 1\).
On primes, \(\lambda_{\min}(\widetilde Q\big|_P)\ge-1/4\).

---

## Proof

**(1)** **Three matrices.** \(Q_N=1/\gcd(i,j)\).
\(\widetilde Q_N(i,j)=1/(\gcd(i,j)\sqrt{ij})\).
\(H_N=D^{-1/2}\widetilde Q D^{-1/2}\),
\(D=\mathrm{diag}(\widetilde Q\mathbf 1)\).
Do not mix them.
*[have]*

**(2)** **Full \(Q\) floor is false.**
\(\lambda_{\min}(Q_{10})\approx-1.90\).
\(\lambda_{\min}(\widetilde Q_{20})\approx-0.505\).
Composites kill \(\widetilde Q\).
*[have]*

**(3)** **Bridge\(^*\).** On \(\widetilde Q\), \(v=e_p-e_q\):

\[
R(v)=\frac12\Big(\frac1{p^2}+\frac1{q^2}\Big)-\frac1{\sqrt{pq}}>-\frac12
\]

because \(pq\ge 6\). Two-line identity. Not \(\lambda_{\min}\).
*[have]*

**(4)** **Theorem P.** Prime block \(A=uu^\top+D\) with
\(u_p=p^{-1/2}\), \(D_{pp}=1/p^2-1/p\).
\(uu^\top\ge 0\) and \(\min D=-1/4\) at \(p=2\).
Hence \(\lambda_{\min}(\widetilde Q\big|_P)\ge-1/4\).
*[have]*

**(5)** **Theorem H-floor.**

\[
w^\top\widetilde Q w+w^\top Dw
=\frac12\sum_{i,j}\widetilde Q_{ij}(w_i+w_j)^2\ge 0.
\]

So \(w^\top\widetilde Q w\ge-w^\top Dw\), i.e.
\(\lambda_{\min}(H_N)\ge-1\) for every \(N\).
This is the unrestricted spectral floor that sits.
*[have]*

**(6)** **Write.** \(\lambda_{\min}(H_N)\ge-1/4\) for all \(N\).
Numeric through \(N=200\) (worst \(H_4\approx-0.225\)).
The pairing that proves \(-1\) does not prove \(-1/4\).
Do not revive \(-3/14\).
*[the next write]*

**(7)** **Then.** If (6) sits, the full-index floor is
sharp at \(-1/4\). Still not RH. Still not SND.
Still not Track B.
*[follows from (6)]*

**(8)** **Spectral-limit leftover.**
\(\lambda_{\min}(\widetilde Q_N)/\log N\) sits near \(-0.16\).
Compatible with a finite limit. Old Route C shape.
Not a floor at \(-1/2\). Gap 1 complete is stale.
*[open; not (6)]*

Goldbach-shaped \(R\ge-2/9\) is a corollary of (4) on
odd primes. Separate chain: [`GOLDBACH-CHAIN.md`](GOLDBACH-CHAIN.md).
Not (6). Not the integer conjecture. GNC stays withdrawn.

If (6) sits, the sharp floor follows. Emitting the
chain is not that close. Q6 is this paper, not
Montgomery–Dyson and not SND.

Machine: [`DA-Q.md`](DA-Q.md)
