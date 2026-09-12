# Lemma★ — 9B growing-\(s\) campaign

12 September 2026. Live lane after the counting lock.
**Not a proof of ★. NS not solved.**

Phone: stay in this chat.

---

## What this is

The displayed bound
\(\|\Pi_\beta B(w,w)\|_2\le C\alpha\beta^{-1/2}\|w\|_2^2\)
is the 9B uniform target. \(B=B(w,w)\) is the same
exact-shell bilinear as the HH→L fan.
Not a new field. Linear pol only.
Live 9D (full complex pol, growing supports)
is the remaining packet falsifier:
[`LEMMA-STAR-LIVE.md`](LEMMA-STAR-LIVE.md).

Fixed \(s\) cannot unbound \(K\) (\(K\le 16s\)).
Growing input support \(m\) and occupied output
support \(s\) is the remaining test.
There is **no seated exponent** tying \((m,s)\)
to \((\alpha,\beta)\). Finding that scaling is
this campaign, not a 9D lemma.

Probe: `python3 scripts/ns_attacks/attack9b_growing_s.py`

JSON: `results/attack9b_growing_s/attack9b_growing_s.json`

Counting lock:
[`LEMMA-STAR-9B-COUNTING.md`](LEMMA-STAR-9B-COUNTING.md).

---

## What ran

Two layers.

1. **Combinatorial room** (no field), \(|k|_\infty\le 20\).
   36895 \((\alpha,\beta)\) pairs with sums.
   Pairs-per-output \(\le m\): 0 failures.
2. **Fields**, seed 1390. 774 samples. Random,
   locked-phase, plane-restricted, high-rep
   greedy, phase-optimized. Then a focused
   full-shell optimize on the census extremes.

---

## Combinatorial room (not \(K\))

| What | Number |
|---|---|
| max \(s_{\mathrm{geom}}\) | 480 |
| max representations on one \(k\) | 24 at \((\alpha,\beta)=(650,900)\), \(m=216\) |
| max \(\mathrm{max\_rep}/m\) | \(1/2\) at the tiny pair \((3,4)\) |
| max \(s_{\mathrm{geom}}/m\) | \(\approx 2.89\) |
| max \(s_{\mathrm{geom}}/m^2\) | \(1/3\) |
| CS ceiling \(16s_{\mathrm{geom}}\) | 7680 |

On the large shells, \(s_{\mathrm{geom}}\) grows
and representations stay \(O(1)\) (typically 2–8,
once 24). The ratio \(1/2\) is a small-shell
artifact, not a growing law.

The CS ceiling grows because \(s\) grows. That is
room, not \(K\). Census is \(|k|_\infty\le 20\),
not a theorem for all shells.

---

## Fields (not \(C_0\))

| What | Number |
|---|---|
| max \(K\) | \(\approx 0.631\) at \((4,8)\), \(s=12\), \(m=6\) |
| max \(\sqrt{K}\) | \(\approx 0.794\) |
| max occupied \(s\) | 36 |
| max \(m\) | 30 |
| max \(K/(16s)\) | \(\approx 0.0078\) |
| sample log-log slope \(K\) vs \(s\) | \(\approx -0.35\) |
| sample log-log slope \(K\) vs \(m\) | \(\approx -0.79\) |
| focused extremes max \(K\) | \(\approx 0.148\) at \((3,4)\) |

Did **not** beat the original exact-shell
\(\max K\approx 0.641\) at the same \((4,8)\).
Larger \(m\) and \(s\) printed **smaller** \(K\).
Efficiency against the CS budget stays below one
percent. High-rep full shells did not lift \(K\).

A sample slope is **not** a seated exponent.
A finite max is not \(C_0\).
A growing ceiling is **not** a kill.
Do not merge \(\sqrt{K}\) with Attack 12
\(\mathcal R_\star\sim\beta/\alpha\).

---

## Extrapolation (flagged)

If representations stay \(O(1)\) while \(m\)
grows, equal-amp pair mass on one output is
\(O(1/m)\) and the CS ceiling is not the live
constraint. That **matches** these samples.
It is **not** a proof that \(\sup K<\infty\).
A new family with \(\mathrm{max\_rep}\sim m\)
on many outputs would reopen the kill.

---

## Honesty

- NS not solved.
- Lemma★ OPEN.
- Kill lane LIVE.
- This is not 9D. Do not rebuild Freiman-AP.
- Do not glue this to H1 or the \(T_{j\leftarrow j}\) door.
