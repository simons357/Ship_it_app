# DA-GATE — RMS / core / tail / summation-by-parts

**24 September 2026.** Gate filed. Every boxed identity below was
rechecked in sympy. This is an identity gate, not a close.

**Classical unaugmented 3-D Navier–Stokes stays open.**
DA-NS-2 stays **OPEN**. The tail estimate stays **OPEN**.

Machine: [`scripts/da_gate_rms_sbp.py`](../scripts/da_gate_rms_sbp.py).
Lock: [`data/da_gate_rms_core_tail_sbp_2026-09-24.json`](../data/da_gate_rms_core_tail_sbp_2026-09-24.json).
Ledger: [`docs/CENTERED-MASTER-LEDGER.md`](../docs/CENTERED-MASTER-LEDGER.md)
(separate PR; not overwritten).

Convention for this packet: **frozen epoch** \(\lambda_e=\kappa_e^2\).
Do not mix with the live-\(\Lambda\) form.

---

## Status

| Item | Bucket |
|---|---|
| Chebyshev tail bound | **PROVED** |
| Core-radius bound; factor of two exact | **PROVED** |
| \(\nabla R=(5\kappa^2,5\kappa^2,0)\), \(\partial_\Lambda R=-2\kappa\) | **PROVED** |
| \(\lvert R-2\kappa^3\rvert\le 5\kappa^3 Lr+O((Lr)^2)\) | **PROVED** (live core) |
| Frozen-core extra \(2\kappa_e\lvert\Lambda-\lambda_e\rvert\) | **PROVED** if frozen |
| Replacing a signed sum by a sum of absolute values | **FORBIDDEN** |
| Weight \(\lvert m\rvert\) flux; \(Q_a=\tfrac12(d/dt)_{\rm NL}\lVert u\rVert_{\dot H^{1/2}}^2\) | **PROVED** |
| \(M^{\rm het}=\sum AHQ\), \(N^{\rm het}=\sum AQ\) | **PROVED** |
| SBP identity for \(\Phi_e\) | **PROVED** (identity only) |
| \(\Phi_e/Y\) controlled by \(r^2\) | **OPEN** |
| Tail leakage vs \(\nu\mathcal D_s\) on the tail | **OPEN** — the broad missing estimate |
| DA-NS-2 | **OPEN** |

---

## Convention flag

Two writings of the core remainder. Pick one. Do not mix.

- **Live \(\Lambda\).** Written at the live barycenter. No moving term.
  Then \(2\kappa(t)^3 Q_a\) no longer telescopes.
- **Frozen \(\lambda_e\).** Core centered at \(\kappa_e=\sqrt{\lambda_e}\).
  Picks up the extra \(2\kappa_e\lvert\Lambda-\lambda_e\rvert\).
  This is the convention of the SBP identity below.

---

## Steps that check out

1. Chebyshev tail bound — **PROVED**.
2. Core-radius bound — **PROVED**. The factor of two is now exact.
3. Gradient of \(R\) at the live core \((i,j,o)=(\kappa,\kappa,\kappa)\),
   \(\Lambda=\kappa^2\):

\[
\nabla_{(i,j,o)}R=(5\kappa^2,5\kappa^2,0),
\qquad
\partial_\Lambda R=-2\kappa.
\]

Hence

\[
\lvert R-2\kappa^3\rvert\le 5\kappa^3 Lr+O((Lr)^2).
\]

   Under the frozen convention the core is at \(\kappa_e\) and the
   remainder picks up \(2\kappa_e\lvert\Lambda-\lambda_e\rvert\).
4. Replacing a signed sum by a sum of absolute values is the
   forbidden step.

On the tail: small \(X\)-mass and small \(Y\)-mass can still hold
essentially all of \(\mathcal D_s\). Tail leakage competes directly
with \(\nu\mathcal D_s\) restricted to the tail. That is the broad
missing estimate again.

---

## Two existing identities — PROVED

Weight \(\lvert m\rvert\) has flux \(2o(i-j)\) on heterochiral triads
and zero on homochiral ones. With Heavy’s normalization this makes
the charge

\[
\boxed{
Q_{a,\Gamma}
=
\tfrac12\Bigl(\frac{d}{dt}\Bigr)_{\rm NL}
\lVert u\rVert_{\dot H^{1/2}}^2.
}
\]

The charge is the flux of the critical \(\dot H^{1/2}\) norm. This
may be the dossier’s cross-radius helicity primitive. That
identification is **not confirmed** here; the 7 Sep dossier is not
in this tree.

Also

\[
\boxed{M^{\rm het}=\sum AHQ},
\qquad
\boxed{N^{\rm het}=\sum AQ}.
\]

---

## Summation-by-parts — PROVED as an identity

Take the weight

\[
\boxed{
\phi_e(m)
=
\tfrac12(m-\kappa_e)^2(m^2+2\kappa_e m+2\kappa_e^2)\ge0
}
\]

and the capacity \(\Phi_e=\sum_k\phi_e(\lvert k\rvert)\lvert a_k\rvert^2\).
Then, exactly and over all triads, under the frozen convention,

\[
\boxed{
\mathfrak T_c
=
\Bigl(\frac{d}{dt}\Bigr)_{\rm NL}\Phi_e
+
2\kappa_e^3 Q_a
-
(\Lambda-\lambda_e)N.
}
\]

The constant \(\phi_e\)-shift \(\kappa_e^4\) has vanishing nonlinear
derivative by energy conservation.

The narrow-homochiral and heterochiral-radial parts together are the
time derivative of one nonnegative capacity that vanishes to second
order at the shell. The order-\(r\) multiplier variation lands on
\(\Phi_e'\), not on \(\sum\lvert Q\rvert\). That is the bridge,
stamped as an identity only.

---

## What it costs — all OPEN

- \(\phi_e(0)=\kappa_e^4\), and \(\phi_e\) grows like \(m^4/2\) at
  high \(k\). So \(\Phi_e/Y\) is **not** controlled by \(r^2\).
  Low-mode energy enters as \(\kappa^4 E\), which is always at
  least \(Y\).
- Integrating \(\Phi_e'/Y\) by parts returns \(\Phi_e Y'/Y^2\),
  absorbable only if \(\Phi_e/Y\) is small. Tail leakage reappears
  exactly here, as the weight of \(\phi_e\) away from the shell.
- The viscous part has the good sign. Epoch resets add a jump ledger.
- The charge (the \(\dot H^{1/2}\) flux) and \(-(\Lambda-\lambda_e)N\)
  are still the residual.

---

## \(\Phi_e/Y\) diagnostic

Split \(\Phi_e/Y\) into core, low tail, and high tail along
Taylor–Green, frozen \(\lambda_e=\Lambda(0)\).

```bash
PYTHONPATH=scripts python3 scripts/da_gate_rms_sbp.py --n 16 --t 4.5 --dt 0.5
```

On the \(n=16\), \(\nu=0.02\) Taylor–Green run already in this tree,
frozen \(\lambda_e=\Lambda(0)=3\): \(\Phi_e/Y=0\) at \(t=0\) (exact
shell), then rises to \(0.31\) by \(t=4.5\), and that mass sits in
the high tail. \(\kappa^4 E/Y\) falls from \(1\) to \(0.15\).
\(\mathcal D_s\) grows from \(0\) to about \(51\). This is evidence
that the returned term is **not** small on this run. It is not the
missing tail estimate.

| \(t\) | \(\Phi_e/Y\) | core | low | high | \(\kappa^4 E/Y\) | \(\mathcal D_s\) |
|---:|---:|---:|---:|---:|---:|---:|
| 0.0 | 0 | 0 | 0 | 0 | 1.00 | 0 |
| 0.5 | 0.023 | 0 | 0 | 0.023 | 0.92 | 0.80 |
| 1.0 | 0.080 | 0 | 0 | 0.080 | 0.72 | 4.03 |
| 1.5 | 0.148 | 0 | 0 | 0.148 | 0.52 | 11.5 |
| 2.0 | 0.206 | 0 | 0 | 0.206 | 0.38 | 22.6 |
| 2.5 | 0.247 | 0 | 0 | 0.247 | 0.28 | 34.0 |
| 3.0 | 0.274 | 0 | 0 | 0.274 | 0.22 | 43.0 |
| 3.5 | 0.291 | 0 | 0 | 0.291 | 0.19 | 48.6 |
| 4.0 | 0.303 | 0 | 0 | 0.303 | 0.16 | 51.0 |
| 4.5 | 0.312 | 0 | 0 | 0.312 | 0.15 | 51.0 |

\(N=64\) and \(N=96\) data are **not in this tree**. A table on
those grids is a later measurement, not a substitute for the missing
tail estimate.

---

**NS not solved.**
