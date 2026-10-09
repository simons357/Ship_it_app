# Gate D — interaction-sum speedup check

9 October 2026.
**Measured agreement. Modest speedup on the pair loop. Continuation not resumed. Not (17).**

Reference, left unchanged:
[`../scripts/ns_attacks/gate_d_full_trajectory.py`](../scripts/ns_attacks/gate_d_full_trajectory.py).

Copy:
[`../scripts/ns_attacks/gate_d_rhs_fast.py`](../scripts/ns_attacks/gate_d_rhs_fast.py).
Numbers: [`../scripts/ns_attacks/GATE-D-RHS-SPEEDUP.json`](../scripts/ns_attacks/GATE-D-RHS-SPEEDUP.json).

The field, viscosity, cutoff, and time step are the reference experiment:
\(n=1\), \(H=63\), \(\nu=1.2569258291022742\times 10^{-5}\), cutoff \(8H=504\),
\(\Delta t=2\,H^{-2.5}=6.348609607948723\times 10^{-5}\), energy normalized to 1.

---

## Agreement

| Check | Result |
|---|---|
| Initial derivative, relative \(L^2\) | \(1.96\times 10^{-16}\) |
| Initial signed excess \(T-\nu Y/4\) | \(15358.440780205932\) on both |
| Initial energy-identity residual | \(-4.2\times 10^{-11}\) reference, \(-7.8\times 10^{-11}\) copy |
| First accepted step, relative \(L^2\) | \(2.41\times 10^{-17}\) |
| First-step energy | \(0.9999356778913183\) on both |
| First-step signed transfer | \(20675.371288971586\) reference, differs by \(7\times 10^{-12}\) on the copy |
| First-step signed excess | \(15555.580670577521\), growth not turnover |
| Pair-row relative \(L^2\) on that state | \(5.2\times 10^{-16}\) |
| Hash overflow | 0 |

The initial field has 358 modes. The first accepted state has 66242 modes
(\(4.388\times 10^9\) ordered pairs).

---

## Speed

On the initial field the threaded copy is slower (0.24×): thread and merge
overhead dominates \(1.3\times 10^5\) pairs.

On 2048 rows of the first accepted state (\(1.357\times 10^8\) ordered pairs):

| Loop | Time |
|---|---|
| Reference pair loop | 35.05 s |
| Threaded copy, 4 threads | 23.10 s |
| Speedup | **1.52×** |

Scaling that rate by the full pair count is about 1130 s versus 750 s per
derivative. That scale is not a timed full sum. A faster evaluation does not
promise turnover. The continuation was not resumed, and the time step was
not refined.

---

## STATUS

AGREEMENT: YES, AT ROUNDOFF, ON THE FIXED EXPERIMENT.
SPEEDUP: 1.52× ON THE FIRST-ACCEPTED PAIR LOOP. NOT ON THE TINY INITIAL SUM.
REFERENCE SOLVER: UNCHANGED.
CONTINUATION: NOT RESUMED.
TURNOVER: NOT TESTED BY THIS SPEEDUP.
NS NOT SOLVED.
