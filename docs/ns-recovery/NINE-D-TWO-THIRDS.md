# Three-shear floor \(K=2/3\) — scored on this book

**Date:** 13 September 2026  
**Other book:** [`docs/ATTACK-9D-TWO-THIRDS.md`](https://github.com/simons357/Ship_it_app/blob/cursor/unaugmented-r4-vorticity-f80e/docs/ATTACK-9D-TWO-THIRDS.md) on [PR #24](https://github.com/simons357/Ship_it_app/pull/24).  
**This book** checked the same field on [`scripts/ns_lemma_star_core.py`](../../scripts/ns_lemma_star_core.py).

**This is the write-up example, not the bound.**  
A random-search maximum is a weaker object.  
**NS is not solved.** Unrestricted ★ stays dead on \(v_n\). Soft X silent.

---

## The field (one line)

\[
w=(\sin y,\sin z,\sin x).
\]

Real, mean-zero, divergence-free. Exact shell \(\alpha=1\): six axis modes

\[
\widehat w(0,1,0)=\bigl(-\tfrac i2,0,0\bigr),\quad
\widehat w(0,0,1)=\bigl(0,-\tfrac i2,0\bigr),\quad
\widehat w(1,0,0)=\bigl(0,0,-\tfrac i2\bigr),
\]

and conjugates. Energy \(E=3/2\).

Output shell \(\beta=2\): twelve keys, permutations of \((\pm1,\pm1,0)\).  
At \(k=(1,1,0)\) the only live ordered pair is \(p=(0,1,0)\), \(q=(1,0,0)\).  
\(\widehat B_k=(0,0,-i/4)\), so \(|\widehat B_k|^2=1/16\). Cyclic axes give the same size on every output.

\[
\|\Pi_2 B(w,w)\|_2^2=12\cdot\frac1{16}=\frac34,
\qquad
K_{1,2}(w)=\frac{2\cdot(3/4)}{(3/2)^2}=\frac23.
\]

This book’s evaluator reproduces \(2/3\) to machine precision
(`scripts/three_shear_k_two_thirds.py`). Twelve outputs, each \(1/16\).
That is a check, not a second claim.

---

## Floor, not ceiling

\[
\sup K\ge\frac23.
\]

\(2/3\approx 0.667\) clears aligned 9B \(0.641\) and grow-\(s\) \(0.456\).
It sits well under \(16/9\approx 1.778\).

One explicit value proves the floor of the supremum. It does **not**
prove the ceiling. \(2/3\) is **not** \(C_0\).

Exact-shell \(K\le 16/9\) stays **CLAIMED**. Moving that to supported
still needs the closed-form derivation, or a sweep that shows nothing
gets near \(16/9\). Neither sits. Specialist review is still pending.

This book’s aligned 9B row at \((1,2)\) was \(K\approx 0.578\) on a
**different** field. That sweep did not name this interaction.

---

## Status

| Item | This book |
|---|---|
| \(K_{1,2}(w)=2/3\) on this field | **Yes.** Hand + locked core. |
| \(\sup K\ge 2/3\) | **Yes.** Floor. Write-up example. |
| \(2/3\) as \(C_0\) or as \(16/9\) | **No.** |
| Exact-shell \(K\le 16/9\) | **CLAIMED.** Unchanged. |
| Unrestricted ★ | **Still dead** on \(v_n\). |
| Ordinary NS | **Open.** |

JSON: [`results/three_shear_k_two_thirds.json`](../../results/three_shear_k_two_thirds.json)

**NS not solved.**
