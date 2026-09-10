# ATTACK 9 — Coherent Packet / Fan Test

**Date:** 2026-09-10  
**Branch:** `cursor/ns-five-lane-lemma-star-1390`  
**Status:** **LIVE kill attempt** (numerics). Lemma★ **OPEN**. **NS not solved.**

## Goal

Maximize the complete shape quotient
\[
\mathcal{R}_\star(v)=\frac{(T_c(v)_+)^2}{\mathcal{D}_s(v)\,\|v\|_2^2\,Y(v)}
\]
over conjugate-closed packets \(P,Q,R\) with \(R=P+Q\), increasing packet cardinality \(m\), optimizing amplitudes, phases, and divergence-free polarizations.

## Decisive output

Fit
\[
\mathcal{R}_\star(v_m)\sim m^\gamma.
\]

| Outcome | Meaning |
|---------|---------|
| Sustained \(\gamma>0\) | **Counterexample route** still open (kill lane progressing) |
| Flat \(\gamma\approx 0\) | Next analytic target: square-summation / orthogonality preventing coherent triad accumulation |
| \(\gamma<0\) | Decay under this packet family — not a kill; try other fans |

## Required controls

| Control | Expectation |
|---------|-------------|
| \(\mathcal R_\star(av)=\mathcal R_\star(v)\) | Exact (amplitude) |
| \(\mathcal R_\star(v(n\cdot))=\mathcal R_\star(v)\) | Exact (uniform Fourier dilation) |
| \(\sum_k\mathscr{T}_k=0\) | Energy identity |
| Direct triad \(\Leftrightarrow\) dealiased FFT | Agree on total \(T_c\) |
| Report **total** \(T_c\) | Not HH→L-only favorable portion |

## Script

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/attack9_packet_fan.py \
  --m-min 1 --m-max 8 --outdir /opt/cursor/artifacts/attack9_packet_fan
```

Artifacts: `/opt/cursor/artifacts/attack9_packet_fan/` (`attack9.json`, `HEADLINE.md`, `R_star_vs_m.png`).

## Runtime 2026-09-10 (m=1..8, seed 1390)

| Metric | Value |
|--------|-------|
| \(\gamma\) (OLS log–log) | \(\approx -1.389\) |
| \(R^2\) | \(\approx 0.818\) |
| Verdict | `DECAYING_gamma_lt_0` — this fan does **not** open a sustained \(\gamma>0\) counterexample route |
| Controls | **PASS** (amp inv., dilation inv., \(\sum T_k=0\), triad=FFT total \(T_c\)) |
| \(\max_m\mathcal R_\star\) on this run | \(\approx 0.103\) at \(m=1\) |

Decay under this coherent fan is **not** a kill of ★ and **not** closure of the kill lane. Next analytic target if other fans stay flat/decaying: square-summation / orthogonality preventing coherent triad accumulation. Kill lane remains **LIVE**.

## Relation to Attack 8

[`ATTACK_8_CORRECT_RECORD.md`](./ATTACK_8_CORRECT_RECORD.md) locks that the kill lane is **LIVE** and that \(\mathcal R_\star\) is amplitude/dilation invariant. Attack 9 is the next falsification probe under that record.

## Archive warning

Do not weld Route N / Q6 / LP-shell floor numerics into this attack. Those live under [`ARCHIVE_ROUTE_N_Q6_SHELL/`](./ARCHIVE_ROUTE_N_Q6_SHELL/).

**NS not solved.**
