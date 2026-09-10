# ATTACK SYNTHESIS — Lemma★ lanes (truth lock)

**Date:** 2026-09-10  
**Branch:** `cursor/ns-five-lane-lemma-star-1390`  
**Rule:** Truth only. **Navier–Stokes is NOT solved. No Millennium claim.**  
**Kill lane:** **LIVE.** Proof lane: **LIVE.**  
**Correct record:** [`ATTACK_8_CORRECT_RECORD.md`](./ATTACK_8_CORRECT_RECORD.md)

## Retired false claims

1. **“The kill lane is closed”** — **FALSE.** Numeric non-find ≠ closed falsification.
2. **“Amplitude or frequency makes the ratio smaller”** — **FALSE for \(\mathcal R_\star\).** Exact invariance under amplitude and uniform Fourier dilation. Older budgets (post-Young) are a different object.

## Lemma★ (canonical: shape form)

Full lock: [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md).

\[
\mathcal R_\star(v)
=
\frac{(T_c(v)_+)^2}{\mathcal D_s(v)\,\|v\|_2^2\,Y(v)}.
\]

When \(T_c\ge0\), \((T_c)_+^2=T_c^2\). Kill cares about stretching \(T_c>0\).  
**Hygiene:** do not compare \(0.065\), \(0.073\), \(1.93\times10^{-3}\) unless each used this exact formula.

## Lane board

| Lane | Script / doc | Runtime verdict | Key notes |
|------|----------------|-----------------|-----------|
| 1 Covariance | `attack1_covariance.py` | Numeric support only | Homogeneity checks; **not** a proof |
| 2 Triad / K=0 / C* | `attack2_triad_k0_cstar.py` | **K=0 DEAD** | Viscosity-only absorption dies with amplitude |
| 3 Bony HH→L | `attack3_bony_hh_l.py` | HH channel live bottleneck | Diagnostic only; kill uses **total** \(T_c\) |
| 4 Stokes | `attack4_stokes.py` | Identities OK | Remainder still needed |
| 5 Route2 kill | `attack5_route2_kill.py` | Sample list ≠ constant | Kill lane still **LIVE** |
| **8 Correct record** | `ATTACK_8_CORRECT_RECORD.md` | **CORRECT RECORD** | Invariants; lanes LIVE; archive split |
| **9 Packet fan** | `attack9_packet_fan.py` | **LIVE** — \(\gamma\approx-1.39\) (decaying on this fan) | Controls PASS; not a kill; kill lane still LIVE |

## Attack 9 decisive rule

- Sustained \(\gamma>0\) → counterexample route  
- Flat → next analytic target: square-summation / orthogonality  
- This run (\(m=1..8\)): \(\gamma\approx-1.389\), verdict `DECAYING_gamma_lt_0` — **not** a counterexample; **not** lane closure

Artifacts: `/opt/cursor/artifacts/attack9_packet_fan/`

## Exact inequality still to attack

Close **either** boxed shape ★, or a pre-Young geometric bound that Young-lifts — with a proof controlling signed triads. Numerics ≠ proof. **NS not solved.**

## Archive — NOT Lemma★

Route N / Q6 / LP-shell / shell floor \(M\le256\):  
[`ARCHIVE_ROUTE_N_Q6_SHELL/`](./ARCHIVE_ROUTE_N_Q6_SHELL/), [`../ARCHIVE_NOT_LEMMA_STAR.md`](../ARCHIVE_NOT_LEMMA_STAR.md).

Route N ledger remains linked and labeled **NOT Lemma★** (`docs/math/NS-BRUTE-FORCE-EXTRACTION-LEDGER.md`). Do not weld to ★.

## Reproduce

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/attack9_packet_fan.py \
  --m-min 1 --m-max 8 --outdir /opt/cursor/artifacts/attack9_packet_fan
PYTHONPATH=scripts python3 -m pytest tests/test_ns_attacks_lemma_star.py -q
```
