# DA packet — P2 torus algebra / MIN-CYCLE

**Date:** 28 September 2026
**Gate:** P2 / MIN-CYCLE
**Status:** torus lemma standard; finite compatibility exact;
one-cycle local law complete (exact + quadratic + quartic);
MIN-CYCLE gated; scale-rate **OPEN**

This packet records Jonathan's accepted corrections to the
P2 reachability / TREE / LOOP statement. It does **not**
close Navier–Stokes. It does **not** claim the torus lemma
as a Gate-C discovery.

Working page: [`docs/P2-TORUS-AND-MIN-CYCLE.md`](../docs/P2-TORUS-AND-MIN-CYCLE.md)
Machine: [`results/p2_torus_min_cycle.json`](../results/p2_torus_min_cycle.json)

```bash
PYTHONPATH=scripts python3 -m unittest \
  tests.test_torus_p2 tests.test_one_cycle_loss tests.test_min_cycle -q
PYTHONPATH=scripts python3 scripts/run_p2_torus_min_cycle.py
```

## Locked boxes

\[
b\in\operatorname{im}T_M
\iff
c^Tb\equiv0\pmod{2\pi}
\quad\forall c\in\ker_{\mathbb Z}(M^T)
\]

\[
r_{\mathrm{cyc}}=m-\operatorname{rank}M
\qquad
\text{TREE}\iff r_{\mathrm{cyc}}=0
\qquad
\text{one-cycle: }r_{\mathrm{cyc}}:0\to 1
\]

\[
w_i\sin\varepsilon_i=\lambda c_i
\qquad
\text{(enumerate branches; do not take the first root)}
\]

\[
1-\rho_{\max}
=
\frac{\delta^2}{2WS}
-
\frac{Q\delta^4}{24WS^4}
+O(\delta^6)
\quad(\lvert\delta\rvert\le\pi/2)
\]

\[
c_i=0\Rightarrow\varepsilon_i=0
\qquad
\varepsilon_i^{(2)}=\frac{c_i\delta}{w_i S}
\]

\[
\text{NA-2B = exact cancellation/assembly unit test}
\]

\[
\text{finite-size incompatibility}\;\not\Rightarrow\;\text{scale-decaying defect}
\]

\[
0.15\text{ is a convention, not a derived exponent}
\]

## Acceptance added on this packet

Algebraic TREE→LOOP control is now the MIN-CYCLE positive
control. Unique primitive \(c\) from \(\ker_{\mathbb Z}M^T\).
Not a picture of triangles.

The one-cycle local law is complete: exact branch-enumerated
stationarity, quadratic \(\delta^2/(2WS)\), quartic correction,
off-cycle \(\varepsilon_i=0\), and channel-by-channel
\(\varepsilon_i^{(2)}\). For \(\lvert\delta\rvert>\pi/2\) the
expansions are stamped OUTSIDE PREREGISTERED SMALL-HOLONOMY
REGIME. Scale-rate stays OPEN.

## Explicitly not claimed

- NS solved / DA-NS-2 closed
- Scale-rate exponent
- Optimizer performance from NA-2B
- Novelty of the torus lemma
