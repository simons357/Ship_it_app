# SFE ↔ Black Hole — spellbook (no prejudice)

**Date:** 2026-08-28  
**Rule:** Spells report structure. Correlation is a lead, not a proof.

---

## The overlay you saw

Same day: black-hole story + SFE “laid right over.”  
The archived stack already names the mapping:

| Black hole (caricature) | SFE / spectral stack |
|-------------------------|----------------------|
| Event horizon | Phase boundary \(E_0 = -1/2\) (folklore) |
| Maximum concentration | Phase II: BEC into one mode |
| Exterior \(g_{tt} = 1 - r_h/r\) | Harmonic weights \(n^{-1/2}\), row degrees of \(\widetilde Q\) |
| Ringdown QNM ratios | HB Experiment 01 (held-out null in repo) |
| Prime lattice pressure | Interaction \(\sum N_i N_j / \gcd(i,j) = Q_N\) |

**Two different “horizons” in the math (do not merge blindly):**

1. **Bridge\* / SFE phase line:** \(-1/2\) (restricted Rayleigh; full \(\lambda_{\min}\) goes below it)
2. **Route C spectral constant:** \(-1/(2\pi)\) for \(\lambda_{\min}/\log N\) (numeric, not proved)

---

## Spells (code)

| Spell | Command | What it hunts |
|-------|---------|---------------|
| Overlay | `python3 scripts/sfe_bh_overlay_spells.py 500 1000` | Pearson cross-correlation: \(\lambda_{\min}\) mode vs BH templates |
| Phase flow | `python3 scripts/sfe_phase_flow_spell.py 800 25` | \(\lambda_{\min}/\log N\) and concentration vs \(N\) |
| Route C | `python3 scripts/route_c_gap_a_verify.py 500 1000` | Spectral limit vs false \(v_{\mathrm{alt}}\) target |
| Ringdown | `python3 hb_ringdown_test.py ...` | Real GW data vs node families (separate track) |

---

## Discrete SFE Hamiltonian spell (math meat)

Archived second-quantized form:
\[
\hat H_{\mathrm{SFE}}
= \sum_n n^{-1/2}\hat N_n
+ \frac{g}{2}\sum_{i,j}\frac{\hat N_i\hat N_j}{\gcd(i,j)}
- \sum_n J_n(\hat{a}_n+\hat{a}_n^\dagger).
\]

**Classical / mean-field spell on sites \(n=1..N\):**
\[
H_{\mathrm{disc}} = \mathrm{diag}(n^{-1/2}) + g\cdot Q^{\mathrm{raw}}_{ij},\quad Q^{\mathrm{raw}}_{ij}=1/\gcd(i,j).
\]
Ground state \(\psi_*\) = smallest eigenvector of \(H_{\mathrm{disc}}\).

Compare \(\|\psi_*\|^2\) profile to:
- \(\lambda_{\min}\) mode of \(\widetilde Q\)
- Schwarzschild exterior templates on \(r_n=n/N\)

If profiles align with **harmonic** \(n^{-1/2}\) more than with \(g_{tt}\), the overlay is mostly the critical line \(s=\tfrac12\), not gravity.

---

## Leads from running spells (N=500, 1000 — 2026-08-28)

Artifacts: `/opt/cursor/artifacts/sfe_bh_overlay_spells.json`, `route_c_gap_a_verify_500_1000.txt`, `sfe_phase_flow_spell_1000.txt`

### Overlays matched (Pearson |r| > 0.85)

| N | SFE profile | BH template | r | Verdict |
|---|-------------|-------------|---|---------|
| 500 | harmonic_free / alternating | inv_r_sqrt | **+1.000** | **Artifact** — both are \(n^{-1/2}\) on \(r=n/N\) |
| 500 | λ_min mode | inv_r_sqrt | +0.902 | Lead — gcd-smoothed harmonic, not gravity |
| 500 | row_degree | inv_r_sqrt | +0.964 | Lead — degree field tracks harmonic shell |
| 1000 | harmonic_free / alternating | inv_r_sqrt | **+1.000** | **Artifact** (same) |
| 1000 | λ_min mode | inv_r_sqrt | +0.912 | Lead |
| 1000 | row_degree | inv_r_sqrt | +0.964 | Lead |

**Not matched:** photon_sphere_bump (r ≈ 0.1–0.2), tortoise_decay (r ≈ 0.3). The overlay is **harmonic/critical-line**, not photon-sphere geometry.

### Doors opened (numeric, not proved)

| Door | N=500 | N=1000 | Notes |
|------|-------|--------|-------|
| Phase-II floor (\(\lambda_{\min} < -1/2\)) | ✓ (−0.981) | ✓ (−1.084) | Folklore "horizon" — operator below \(-1/2\) |
| Route C spectral limit \(\lambda_{\min}/\log N \to -1/(2\pi)\) | ratio **0.992** | ratio **0.986** | Strong numeric match; **not** a Clay proof |
| \(v^*\) ↔ \(v_{\mathrm{alt}}\) overlap | 0.954 | 0.955 | Ground mode ≈ alternating harmonic |
| Phase-flow ratio → 1 | 0.992 @ N=490 | 0.986 @ N=990 | Monotone drift toward \(-1/(2\pi)\) |
| SFE toy ground concentration | H=0.0022 | H=0.0011 | **More diffuse** than λ_min mode — gcd interaction spreads mass |
| Parity split \(v^T Q v\) | odd −8.13, even +3.80 | odd −10.11, even +4.67 | Even-d leakage partially cancels odd-d core |

### What's folklore (do not promote without proof)

- **Event horizon = \(-1/2\) phase line:** \(\lambda_{\min}(\widetilde Q) < -1/2\) at moderate N, but this is the Bridge\* restricted-Rayleigh floor, not Schwarzschild.
- **BH collapse = Phase II concentration:** Herfindahl \(H(v^*) \approx 0.002\) at N=1000 — **anti-collapsed** (spread across sites). Concentration **decreases** with N.
- **Gap A for \(v_{\mathrm{alt}}\):** \(R(v_{\mathrm{alt}})/(-1/2\pi) \approx 4.0\)–4.6 — **fails** the archived Route C Rayleigh claim. Only \(\lambda_{\min}/\log N\) tracks the target.
- **Lemma A (Möbius \(\mu\phi/d^2\)):** max entry error ≈ 0.148 — decomposition **false** off-diagonal.
- **SND shell caricature:** \(\rho_{\max} \approx 0.608 > 0.5\) at \(j^*=1\) — discrete enstrophy toy does **not** satisfy SND gate.
- **Perfect harmonic ↔ inv_r_sqrt:** expected algebra (\(1/\sqrt{n}\) vs \(\sqrt{r_h/r}\) with \(r=n/N\)), not evidence of black-hole physics.

### Bug fixes in this run

- `sfe_bh_overlay_spells.py`: replaced invalid `math.isprime` with local trial-division helper.
- `sfe_phase_flow_spell.py`: removed duplicate `eigh` call.

Unit tests: `tests/test_sfe_bh_spells.py` (10 tests, all pass).

1. **Coupled ODE spell:** T2 shell Gronwall \( \dot\rho \) vs \(\partial_N(\lambda_{\min}/\log N)\) — hunt shared constant.
2. **Anesthesia spell:** BIS proxy = \(|\langle\psi\rangle|^2\); map to inverse participation ratio of SFE ground state.
3. **Prime horizon spell:** concentration on largest prime \(\le N\) vs photon-sphere bump position.
4. **Möbius parity spell:** Route C \(T_+\) (even-\(d\)) as “exterior” leakage canceling odd-\(d\) core.

---

## Honesty fence

- NS / RH / Clay: **not** solved by overlay.
- Strong Pearson with \(1/\sqrt{r}\) is **expected** (harmonic critical line), not automatic BH validation.
- HB ringdown experiment in this repo: **null held** — do not reverse-causality into “BH proves Q6.”

Use spells to **generate leads**. Promote to theorem only after kill/close DA pass.
