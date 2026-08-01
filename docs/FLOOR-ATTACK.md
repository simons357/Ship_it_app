# Floor attack — get Bridge where it can actually be solved

**Goal:** unconditional stability that makes Triple Lock fire.  
**Input papers:** `docs/papers/SND_GNC_BRIDGE_UNIFIED.pdf` · three-in-one · verifier `scripts/bridge_floor_verify.py`

---

## 0. What “solve” means here

Not “wish the old slogan true.”  
**Solve** = state a **true** spectral inequality, prove it, and keep the SND/GNC glue attached to **that** inequality.

---

## 1. Blockers in the June 5 Triple Lock text (must fix first)

### 1.1 False identity (§2.1)

Claimed:
\[
\frac{1}{\gcd(i,j)}=\sum_{d\mid\gcd(i,j)}\frac{\mu(d)\,\varphi(d)}{d^2}.
\]
**False.** Already at \(n=2\): RHS \(= 3/4\), LHS \(= 1/2\).

Correct Dirichlet factorization of \(1/n\):
\[
\frac{1}{n}=\sum_{d\mid n}g(d),\qquad
g(n)=\sum_{d\mid n}\frac{\mu(d)}{n/d}.
\]
Then
\[
Q_{ij}=\frac{1}{\gcd(i,j)}=\sum_d g(d)\,1_{d\mid i}\,1_{d\mid j}.
\]

### 1.2 Full-spectrum Bridge is false for the named matrices

| Operator | Claim in papers | Computation |
| --- | --- | --- |
| \(Q_{ij}=1/\gcd(i,j)\) | \(\lambda_{\min}>-1/2\) for all \(N\le 5000\) | \(\lambda_{\min}(Q_{100})\approx -14.9\) · falls ~\(-\Theta(N)\) |
| \(\tilde Q_{ij}=1/(\gcd\sqrt{ij})\) (three-in-one Route C) | \(\lambda_{\min}\to 6/\pi^2-1/2>0\) and \(>-1/2\) for \(N\le 5000\) | Already \(<-1/2\) by \(N=20\); keeps falling ~\(c\log N\), \(c\approx 0.16\) |

So the open problem **as written** is not an open proof — it is a **false statement** for those matrices. You cannot “finish the last inequality” until the inequality is corrected.

### 1.3 Asymptotic sketch mixes constants

§2.2 uses \(\sum \mu(d)\varphi(d)/d^2\) but quotes \(\zeta(2)^{-1}=\sum\mu(d)/d^2=6/\pi^2\). Those are different series. Vacuum constant must match the actual operator.

---

## 2. What still looks alive (the place to attack)

Run: `python3 scripts/bridge_floor_verify.py 200`

On **normalized** \(\tilde Q_{ij}=1/(\gcd(i,j)\sqrt{ij})\):

| Quantity | Behavior (checked to \(N=400\)) |
| --- | --- |
| Full \(\lambda_{\min}(\tilde Q)\) | \(<-1/2\) · **not** Bridge |
| Rayleigh of Goldbach \(v_k\) (signed ±1 on primes) | worst \(\approx -0.05\) to \(-0.09\) · **still \(>-1/2\)** |
| Nonnegative Rayleigh (SND-style \(v\ge 0\)) | \(>0\) |

So the **corrected conjecture** to try to prove is not full-spectrum Bridge, but a **restricted** floor:

### Corrected Bridge* (candidate)

**Conjecture (Bridge\*).** Let \(\tilde Q_N(i,j)=1/(\gcd(i,j)\sqrt{ij})\). Then for every even \(k\le N\),
\[
\frac{v_k^\top \tilde Q_N v_k}{\|v_k\|^2} \;>\; -\tfrac12
\]
whenever \(v_k(j)=1_{j\in\mathbb{P}}-1_{k-j\in\mathbb{P}}\) is not zero.

Optionally strengthen to \(\ge \kappa\) for an explicit \(\kappa\) (data suggest \(\kappa\) near \(0\) from below, **not** \(6/\pi^2\)).

**SND side:** prove nonnegative unit vectors satisfy \(v^\top\tilde Q v \ge 0\) (likely true; diagonal-dominant / Gram of positives on the cone).

Then rebuild Triple Lock as:
\[
\text{SND (cone)} \;\longleftrightarrow\; \text{GNC (}v_k\text{ class)} \;\longleftrightarrow\; \text{Bridge* (restricted floor)},
\]
not as equivalence to full \(\lambda_{\min}>-1/2\).

---

## 3. Attack plan (order of operations)

1. **Patch §2.1** — replace false Möbius line with correct \(g(d)\); freeze notation \(Q\) vs \(\tilde Q\).  
2. **Retire full-spectrum Bridge** for \(Q\) and \(\tilde Q\) (counterexamples via `bridge_floor_verify.py`).  
3. **Promote Bridge\*** — restricted Rayleigh on Goldbach class + cone for SND.  
4. **Prove Bridge\*** analytically, candidate tools:  
   - expand \(v_k^\top\tilde Q v_k\) over prime pairs \((p,q)\) with \(p+q=k\);  
   - large sieve / Bombieri–Vinogradov for average over \(k\) (Route B style);  
   - uniform bound for each \(k\) via bilinear forms \(\sum_{p+q=k} (pq)^{-1/2}\) minus cross terms.  
5. **Re-glue corollaries** only after (3)–(4): NS under SND, Goldbach under GNC+Bridge*, RH still needs Route C gaps on whatever operator Route C actually uses.  
6. **Do not** claim Clay until Bridge* (or a true full-spectrum inequality on a different operator) is proved and refereed.

---

## 4. Where the swirl paper fits

Phi-renorm algebraic cancel is **independent** and already clean — Track B credit path.  
It does **not** plug the Bridge hole. Keep it on a separate submission track.

---

## 5. One-line status

**Full-spectrum \(\lambda_{\min}(Q)>-1/2\) cannot be the finish line — numerics kill it.  
The solvable finish line is Bridge\* (restricted Rayleigh on \(\tilde Q\)) after fixing the §2.1 identity.**

---

## 6. Files

| Path | Role |
| --- | --- |
| `docs/papers/SND_GNC_BRIDGE_UNIFIED.pdf` | Triple Lock source |
| `docs/papers/THREE_IN_ONE_QUANTUM_MILLENNIUM.pdf` | three-in-one (names \(\tilde Q\)) |
| `scripts/bridge_floor_verify.py` | counterexample + GNC Rayleigh check |
| `docs/BRIDGE-FLOOR-AUDIT.md` | earlier audit |
| `docs/FLOOR-ATTACK.md` | this plan |
