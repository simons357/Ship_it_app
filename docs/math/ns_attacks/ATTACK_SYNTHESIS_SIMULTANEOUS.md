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
| **9A Packet fan** | `attack9_packet_fan.py` | **Did not kill ★** — \(\gamma\approx-1.39\) | \(\mathcal D_s\) grew faster than \(T_c\); \(D_s\|v\|_2^2 Y=O(1)\) **false** for AP family |
| **9B Exact-shell \(K_{\alpha,\beta}\)** | `attack9b_exact_shell_K.py` | **LIVE** — \(\max K\approx0.641\) at \((4,8)\) | \(\mathcal R_\star\to K\); controls PASS; not a kill; kill lane still LIVE |
| **9C Fixed-gap spheres** | SoT-only (no probe script yet) | **Did not kill ★** — \(\mathcal R_\star\) \(0.11\to 0.031\) | \(\mathcal D_s\) from **gap**; closures \(O(m)\); does **not** track \(m^{1/2}\); natural same-shell **NOT** a kill |
| **9D \(\Theta(m^2)\) locked phase** | stub / spec | **LIVE falsifier** (not run) | Designed \(\Theta(m^2)\)-closure subset with locked phases |

## Attack 9A — failure (truth)

AP packet increased \(T_c\), but \(\mathcal D_s\) increased faster. Assumption \(\mathcal D_s\|v\|_2^2 Y=O(1)\) in packet size was **FALSE**. **9A did not kill Lemma★.**  
Docs: [`ATTACK_9A_AP_PACKET_FAILURE.md`](./ATTACK_9A_AP_PACKET_FAILURE.md), [`ATTACK_9_PACKET_FAN.md`](./ATTACK_9_PACKET_FAN.md).  
Artifacts: `/opt/cursor/artifacts/attack9_packet_fan/`

## Attack 9B — exact-shell closing

\[
K_{\alpha,\beta}=\sup_{Aw=\alpha w}\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}.
\]
Base packet = many same-shell modes; \(\mathcal D_s\) only from small closing component; \(\varepsilon\) cancels in limiting \(\mathcal R_\star\to K\).  
Caveat: “narrow” ≠ \(\mathcal D_s=O(1)\).  
Doc: [`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./ATTACK_9B_EXACT_SHELL_CLOSING.md).  
Artifacts: `/opt/cursor/artifacts/attack9b_exact_shell/`

### Runtime 2026-09-10 (seed 1390, kmax≤10 shells)

| Metric | Value |
|--------|-------|
| Pairs probed | 24 |
| \(\max K_{\alpha,\beta}\) seen | \(\approx 0.641\) at \((\alpha,\beta)=(4,8)\) |
| Controls | **PASS** (amp inv.; exact-shell \(\mathcal D_s\approx0\)) |
| \(\varepsilon\to0\) limit vs \(K\) | **PASS** on pairs with \(K>0\) |
| Verdict | Finite sample max — **not** a kill of ★; kill lane **LIVE** |

Other notable \(K\): \((1,2)\approx0.578\), \((2,4)\approx0.296\), \((5,10)\approx0.298\), \((13,26)\approx0.234\). Many \((\alpha,\beta)\) have \(K=0\) (kinematic: \(\Pi_\beta B(w,w)=0\) on the tested fan).

## Attack 9C — fixed-gap spheres (not a kill)

Fixed-gap spheres \(n\) and \(n+d\): \(\mathcal D_s\) from the **gap** (not packet width); natural closures only \(O(m)\); \(\mathcal R_\star\) **falls** with \(n\) (\(0.11\to 0.031\)) and does **not** track \(m^{1/2}\). **Natural same-shell ensemble is NOT a kill.**  
Doc: [`ATTACK_9C_FIXED_GAP_SPHERES.md`](./ATTACK_9C_FIXED_GAP_SPHERES.md).  
**Probe:** SoT-only until implemented (no `scripts/ns_attacks/attack9c_*.py` yet).

## Attack 9D — next falsifier (stub)

Designed \(\Theta(m^2)\)-closure subset with **locked phases**. Spec only.  
Doc: [`ATTACK_9D_THETA_M2_LOCKED_PHASE.md`](./ATTACK_9D_THETA_M2_LOCKED_PHASE.md).

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
PYTHONPATH=scripts python3 scripts/ns_attacks/attack9b_exact_shell_K.py \
  --outdir /opt/cursor/artifacts/attack9b_exact_shell
PYTHONPATH=scripts python3 -m pytest tests/test_ns_attacks_lemma_star.py -q
```
