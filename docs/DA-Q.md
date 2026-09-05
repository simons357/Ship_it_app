# DA Q — inverse-GCD paper, floors, Q6, Q7

`python3 scripts/da_machine.py q`  
`python3 scripts/da_machine.py next --ask "look at my best gcd paper"`  
`python3 scripts/da_machine.py next --ask "can it find the electoral floor"`  
`python3 scripts/da_machine.py next --ask "what about Q6"`  
`python3 scripts/da_machine.py next --ask "where does Q7 fit"`  
`python3 scripts/da_machine.py next --ask "Q6. Spectral floor"`  
`python3 scripts/da_machine.py next --ask "gold box"`  
`python3 scripts/da_machine.py next --ask "theorem p"`

Floor chain: [`Q6-FLOOR-CHAIN.md`](Q6-FLOOR-CHAIN.md).

The best GCD paper on this desk is August inverse-GCD
(Zenodo 22045478), also called **Q6 hygiene**, plus the
retraction in [`SPECTRAL-FLOOR-EXPLORATION.md`](SPECTRAL-FLOOR-EXPLORATION.md).

Q is inverse-GCD. It is not RH. It is not Track B.

---

## Sitting floors (the ones DA can find)

| Statement | Verdict |
|---|---|
| Bridge\(^*\): \(R(e_p-e_q)>-1/2\) on \(\widetilde Q\) | **pass** |
| Theorem P: prime-supported \(\widetilde Q\big|_P\ge-1/4\) | **pass** |
| \(\lambda_{\min}(H_N)\ge-1\) (pairing) | **pass** |
| \(v\ge 0\Rightarrow v^\top\widetilde Q v\ge 0\) | **pass** |

## Withdrawn

| Statement | Verdict |
|---|---|
| \(\lambda_{\min}(Q_N)>-1/2\) | **fail** (\(Q_{10}\approx-1.90\)) |
| \(\lambda_{\min}(H_N)\ge-3/14\) | **fail** (\(H_4\approx-0.225\)) |
| Theorem P / \(H_N\) is RH | **fail** |
| \(Q_6\) with \(\gamma>3/2\) enforces SND | **fail** (May T³ glue) |
| GNC is a live Goldbach detector | **fail** (vanishes on an actual pair) |
| Route C Gap 1 complete | **fail** (stale) |

## Remaining Q writes

| Statement | Verdict |
|---|---|
| \(\lambda_{\min}(H_N)\ge-1/4\) | **open** |
| \(\lambda_{\min}(\widetilde Q_N)/\log N\) has a finite limit | **open** |
| Goldbach multi-rep Bridge\(^*\) | **open** (numeric, not a proof) |

---

## Electoral / spectral / actual floor

One object. The live unrestricted floor is
\(\lambda_{\min}(H_N)\ge-1\). The useful restricted floor
is Theorem P. DA can find those: they sit.

DA cannot find \(\lambda_{\min}(Q)>-1/2\). That floor is
false. Finding it would be reviving a counterexample.

The remaining floor write is \(\lambda_{\min}(H_N)\ge-1/4\).

---

## Gold box / the T-name

**Gold box = Goldbach.** The leftover you got far on.

For even \(k\),

\[
v_k=\sum_{p+q=k}(e_p-e_q).
\]

The scan through \(N=200\) stays near \(-0.183>-1/2\).
Worst pair is \((3,5)\). That is a reading. It is not
a theorem. It is not needed for Theorem P.

**The T-name that sits is Theorem P.**
\(\lambda_{\min}(\widetilde Q\big|_P)\ge-1/4\).
Rank-one split \(A=uu^\top+D\). Bridge\(^*\) is the
two-sparse case of the same matrix. This one closed.

**GNC stays withdrawn.** The Goldbach detector /
prime-indicator difference vanishes on an actual
Goldbach pair. Do not unshelve it. Do not glue
Goldbach to RH or SND.

Other T-names on this desk are not this pair:
T2 is fluids (Lemma 1 pass / Lemma 2 fail).
Titchmarsh is the RH treatise. T³ / triple lock
is withdrawn glue. Tao is a chair, not a close.

---

## Q6

Two uses of the same name. Do not glue them.

**Q6 the paper.** August 22045478. Hygiene. Bridge\(^*\)
and the withdrawal of the full floor. That is the best
GCD paper.

**Q6 the old slogan.** \(\lambda_{\min}/\log N\),
normalization \(Q\) vs \(\widetilde Q\) vs \(H\),
operator-to-Mertens. Montgomery–Dyson pair correlation
is a different equation. “Gap 1 complete” is stale.
“\(Q_6\) with \(\gamma>3/2\) enforces SND” is withdrawn.

---

## Q7

Not seated. No file. No theorem id. Do not mint Q7 to
look finished.

If the next inverse-GCD sentence is wanted, it already
has a name: sharp \(H_N\ge-1/4\), or the spectral-limit
without calling it Gap 1 complete. That is still Q.
It is not RH and not Navi Stokes.

---

## Scored

| Claim | Verdict |
|---|---|
| The best GCD paper is Q6 hygiene (22045478) | **pass** |
| DA can find the floors that sit | **pass** |
| The electoral / spectral floor is that Q object | **pass** |
| DA can find \(\lambda_{\min}(Q)>-1/2\) | **fail** |
| Q6 enforces SND | **fail** |
| Route C Gap 1 is complete | **fail** |
| Q7 is already a named theorem here | **fail** |
| The GCD paper closes RH or classical NS | **fail** |
| Sharp \(H_N\ge-1/4\) or the spectral-limit may sit later | **open** |
| The T-name we got to a close is Theorem P | **pass** |
| Goldbach multi-rep is a theorem | **fail** |
| GNC is the live Goldbach object | **fail** |
