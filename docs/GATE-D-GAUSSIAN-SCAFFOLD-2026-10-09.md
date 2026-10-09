# Gate D Gaussian scaffold — smoke only

9 October 2026.
**Replacement scaffold. Not the recovered historical driver. Not a Gate D episode. Not a substitute for the six-box adversary.**

Files: `scripts/ns_attacks/gate_d_gaussian_scaffold/`.
Source SHA256 of `gaussian_gate_d.py`: `a591e95657eadbe9f1027939ec08f696e5fbba3de67d2cdf1f15060123c15534`.

The separate \(s=4\) Gaussian run stays where it was filed
([`GATE-D-GAUSSIAN-EXTENSION-2026-10-09.md`](GATE-D-GAUSSIAN-EXTENSION-2026-10-09.md)).
This scaffold is not that run.

---

## What the smoke does

`gaussian_gate_d.py` samples the curl of
\(A=e^{-r^2/2}(xy,\,xz,\,x+yz)\)
on the periodic cube \([-L/2,L/2)^3\), projects it, and steps unforced
3-D NSE with viscosity \(1/c\) by a 2/3-dealiased integrating-factor RK4.
The pointwise curl formula matches that vector potential before
periodization. After sampling, projection, and the 2/3 mask, the field
is not the \(\mathbb R^3\) datum in the 8 October packet audit.

The supplied smoke is \(n=12\), \(L=12\), \(c=200\), \(0\le s\le 0.02\),
\(\Delta s=0.01\). Rerun here reproduced `smoke.jsonl` entry for entry.
At \(s=0\): energy \(5.1207283333063645\), \(X=32.611124080320636\),
\(Y=120.67914364422008\), production \(0.19602790351705981\),
maximum Fourier divergence about \(10^{-18}\).
Through \(s=0.02\), energy, \(X\), \(Y\), and production all decline slightly.
\(n\) is grid points per axis, not the Gate D cutoff.

`T_sc`, `D`, and `G` are recorded as null. The code sets
`T_sc_implemented` and `D_implemented` to false. No downward crossing
can be read from this output. This audit cannot supply the missing
definitions
([`GATE-D-DIAGNOSTIC-BLOCKED-2026-10-09.md`](GATE-D-DIAGNOSTIC-BLOCKED-2026-10-09.md)).

---

## What this does not do

It does not complete a numerically converged turnover episode.
It does not decide whether dangerous transfer regenerates.
It does not fund repeated episodes from a finite shared resource.
It does not prove a cutoff-independent bound.
It is not DA-preregistered, and the frozen experiment has not run.

Gate B stays in independent review. Primary effort remains Gate D.
No global regularity result has been established.

## STATUS

SCAFFOLD SMOKE: REPRODUCED. NOT AN EPISODE. \(T_{\mathrm{sc}}\), \(D\), AND \(G\): NULL.
AUDIT CANNOT SUPPLY THE DEFINITIONS. DIAGNOSTIC IMPLEMENTATION: BLOCKED.
NOT THE SIX-BOX ADVERSARY. NOT THE \(s=4\) GAUSSIAN RUN.
NS NOT SOLVED.
