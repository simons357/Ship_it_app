# Proof chain — Goldbach-shaped multi-rep

Slot **Q**. Inverse-GCD on \(\widetilde Q\).
Not Goldbach’s conjecture. Not RH. Not SND. Not Track B.

```
python3 scripts/da_machine.py q
python3 scripts/da_machine.py next --ask "gold box"
python3 scripts/da_machine.py next --ask "Yes Goldbach. Please write"
```

Parent: Theorem P in [`SPECTRAL-FLOOR-EXPLORATION.md`](SPECTRAL-FLOOR-EXPLORATION.md).
Q6 floor: [`Q6-FLOOR-CHAIN.md`](Q6-FLOOR-CHAIN.md).

---

## Theorem (sits)

Let \(k\ge 4\) be even and

\[
v_k=\sum_{\substack{p+q=k\\ p\le q\\ p,q\ \mathrm{prime}}}(e_p-e_q).
\]

If \(v_k\neq 0\), then

\[
R(v_k)=\frac{v_k^\top\widetilde Q\,v_k}{\|v_k\|_2^2}\ge-\frac29>-\frac12.
\]

This is a corollary of Theorem P on odd primes. It is not
every even integer as a sum of two primes.

---

## Proof

**(1)** **Theorem P.** On any finite set of primes,
\(\widetilde Q\big|_P=uu^\top+D\) with \(u_p=p^{-1/2}\)
and \(D_{pp}=1/p^2-1/p\). \(uu^\top\ge 0\), so every
prime-supported \(v\) has \(R(v)\ge\min D=-1/4\) at \(p=2\).
*[have]*

**(2)** **Support.** Each term \(e_p-e_q\) is supported
on primes. So \(\operatorname{supp}(v_k)\subset P\).
Already \(R(v_k)\ge-1/4\) when \(v_k\neq 0\).
*[have]*

**(3)** **No 2.** The only even prime is 2. A pair that
uses 2 is \(2+(k-2)=k\). Then \(k-2\) is even. The only
even prime is 2, so \(k=4\) and the pair is \((2,2)\):
\(e_2-e_2=0\). For \(k>4\), \(k-2\ge 4\) is even and not
prime. Hence a nonzero \(v_k\) has \(v_k(2)=0\).
*[have]*

**(4)** **Odd-prime split.** Restrict \(D\) to primes
\(p\ge 3\):

\[
\min_{p\ge 3}\Big(\frac1{p^2}-\frac1p\Big)=\frac19-\frac13=-\frac29.
\]

So \(v_k^\top\widetilde Q\,v_k\ge-\frac29\|v_k\|_2^2\).
*[have; the write]*

**(5)** **Then.** The matrix leftover “multi-rep stays
above \(-1/2\)” sits. Emit is that corollary, not a new
axiom.
*[follows from (1)–(4)]*

**(6)** **Not this write.** \(R(v_k)\ge R(e_3-e_5)\approx-0.183\)
for every even \(k\). Numeric through \(N=200\). The pairing
and the odd-prime \(D\) do not prove it.
*[open]*

**(7)** **Not this object.** Every even integer \(>2\) is
\(p+q\). If there is no pair, \(v_k=0\) and there is no
Rayleigh. GNC stays withdrawn.
*[fail]*

---

## The other far leftover

Same numeric shape, different matrix:
\(\lambda_{\min}(H_N)\ge-1/4\). Through \(N=200\), worst
\(H_4\approx-0.225\). The pairing that proves \(-1\) does
not prove \(-1/4\). That is the remaining Q floor write.

---

Machine: [`DA-Q.md`](DA-Q.md)
