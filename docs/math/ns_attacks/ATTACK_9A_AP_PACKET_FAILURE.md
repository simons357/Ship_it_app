# ATTACK 9A — AP / coherent packet fan: failure reason (not a kill)

**Date:** 2026-09-10  
**Branch:** `cursor/ns-five-lane-lemma-star-1390`  
**Status:** **FAILED to kill ★.** Kill lane remains **LIVE**. **NS not solved.**

## What was tried

**Status docs:** LIVE lock [`PROOF_LemmaStar_LIVE_LOCK.md`](./PROOF_LemmaStar_LIVE_LOCK.md); annotated proof-attempt archive [`PROOF_LemmaStar_STATUS.md`](./PROOF_LemmaStar_STATUS.md) (does **not** green ★; unconditional ★ **OPEN**).
Attack 9 / 9A maximized the complete shape quotient
\[
\mathcal{R}_\star(v)=\frac{(T_c(v)_+)^2}{\mathcal{D}_s(v)\,\|v\|_2^2\,Y(v)}
\]
over conjugate-closed AP / coherent packets \(P,Q,R\) with \(R=P+Q\), increasing packet cardinality \(m\) (amplitudes, phases, divergence-free polarizations).

Runtime (\(m=1..8\)): \(\gamma\approx-1.39\) (`DECAYING_gamma_lt_0`). Controls PASS. Details: [`ATTACK_9_PACKET_FAN.md`](./ATTACK_9_PACKET_FAN.md).

## Why it did not kill Lemma★

AP packet growth **did** increase total signed \(T_c\). That alone is not a kill.

The denominator factor \(\mathcal{D}_s\|v\|_2^2 Y\) grew **faster** than \((T_c)_+^2\). In this family, widening the packet injects spectral mass across more Stokes eigenvalues \(\lambda_k=|k|^2\). Lattice geometry amplifies small eigenvalue differences through
\[
\mathcal{D}_s=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2.
\]
So \(\mathcal{D}_s\) is **not** \(O(1)\) (nor \(O(1)\) after normalizing by \(\|v\|_2^2 Y\)) as \(m\) grows.

**False assumption (now retired for this family):**
\[
\mathcal{D}_s\,\|v\|_2^2\,Y=O(1)\quad\text{in packet size \(m\)}.
\]
That scaling was **FALSE** for the AP / coherent fan. Consequently \(\mathcal{R}_\star\) **decayed** (\(\gamma<0\)) instead of diverging.

## Caveat (carries to 9B)

Merely making a packet “narrow” does **not** automatically keep \(\mathcal{D}_s=O(1)\). Any finite shell thickness on the integer lattice can still inflate \(\mathcal{D}_s\) via the \((\lambda_k-\Lambda)^2\) weights.

## Verdict

| Claim | Verdict |
|-------|---------|
| Attack 9A killed Lemma★ | **FALSE** |
| Sustained \(\gamma>0\) counterexample on this fan | **FALSE** |
| Kill lane closed | **FALSE** — numeric non-kill ≠ closed |
| Next clean test | Exact-shell coherent fan + controlled closing packet — **Attack 9B** |

**NS not solved.** Lemma★ **OPEN**. Kill lane **LIVE**.

## Next

[`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md) — boxed \(K_{\alpha,\beta}\), \(\varepsilon\to0\) analysis, script `attack9b_exact_shell_K.py`.
