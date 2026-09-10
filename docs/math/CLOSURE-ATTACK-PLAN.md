# Closure attack plan — stop the open/open/open loop

**Date:** 2026-08-25  
**Rule:** Prefer *close* or *kill*. Only keep “open” if the attack fails and we record *why*.

DA ranking (impact × closability): multi-rep Bridge\* ≫ Paper1 A–C packaging ≫ signed-floor theorems ≫ Route C Gap A ≫ classical Phi ≫ noncircular SND.

---

## CLOSED this session

### 1. Bridge\* multi-representative (was “Open Problem”)

| | |
|--|--|
| **Where** | `04_q6_inverse_gcd.tex` §Open Problem; `BRIDGE-STAR-PROOF.md` |
| **Problem** | Pair case proved; even multi-rep \(v_k=\sum(e_{p_j}-e_{q_j})\) left open |
| **Fix** | Expand \(\langle\widetilde Qv,v\rangle\); cross terms between disjoint pairs factor nonnegative; reduce to pair Bridge\* |
| **Status** | **PROVED** (algebraic). Numeric check even \(k\le200\). |

---

## NEXT CLOSE (ready to write as theorems)

### 2. Positive-GCD Paper1 — Theorems A / B / C / C′  **[CLOSED]**

| | |
|--|--|
| **Operator** | \(Q_{ij}=\gcd(i,j)/\sqrt{ij}\) (not inverse-GCD) |
| **A** | Pair \(R(e_a-e_b)>0\) — **proved** |
| **B** | Zero-diag pair \(R\ge-1\) — **proved** |
| **C** | \(Q_N\succ 0\) all \(N\) — **proved** (\(Q=D^{-1/2}GD^{-1/2}\), \(G=(\gcd)\) PD) |
| **C′** | Zero-diag full spectrum \(>-1/2\): **KILLED** (\(\lambda_{\min}(\widehat Q_5)\approx-0.79\)) |
| **File** | `docs/papers/submit/07_positive_gcd_paper1_abc.tex` |
| **Script** | `scripts/positive_gcd_floor_verify.py` |

### 3. Inverse-GCD signed-floor package  **[CLOSED in Q6]**

| | |
|--|--|
| **Where** | `04_q6_inverse_gcd.tex` Prop (full-spectrum Bridge is false) |
| **Status** | \(\exists N\) with \(\lambda_{\min}(Q_N),\lambda_{\min}(\widetilde Q_N)<-1/2\) — **proved** (numeric) |

### 4. \(H_N\) small-\(N\) universal bound  **[KILLED in tests]**

| | |
|--|--|
| **Claim** | \(\lambda_{\min}(H_N)\ge-3/14\) for all \(N\) |
| **Status** | **False** at \(N=4\) (`tests/test_bridge_star_h_n.py`) |

---

## HARD (honest open — don’t fake close)

| Gap | Why stuck | What would close it |
|-----|-----------|---------------------|
| Noncircular large-data SND / \(M\) independent of \(X\) | Needs new a-priori; circularity of Thm H | New estimate or abandon NS route |
| Route C Gap B (uniform \(\lambda_2-\lambda_{\min}\)) | Real analysis | Independent spectral gap proof |
| Route C Gap A′ (spectral limit) | \(\lambda_{\min}/\log N\to -1/(2\pi)\) numeric only | Trial vector + rigorous limit |
| Classical Phi without \(Q_1\) | \(1/r^4\) remainder | Different cancellation or accept augmentation |
| Full \(\widetilde Q\) spectrum \(>-1/2\) | **Already false** | Kill theorem only |
| **Route N PDE bridge** (GCD form → vortex-stretch / shell-transfer) | No map from arithmetic \(B_{M,j}\) to NS nonlinearity | New PDE theorem — not packaging |

---

## LEAD — Lemma★ / centered Stokes drift (five-lane numeric)  **[2026-09-10]**

| | |
|--|--|
| **Where** | `docs/math/ns_attacks/`; probes `scripts/ns_attacks/` |
| **Lemma★** | **Canonical shape form:** \(\mathfrak T_c(v)^2\le C_{\mathrm{geom}}\mathcal D_s(v)\,E(v)\,Y(v)\) with \(\mathcal R_\star=T_c^2/(\mathcal D_s E Y)\) — **OPEN** (viscosity packaging equivalent via \(u=av\)) |
| **K=0** | **KILLED** (ratio grows with amplitude) |
| **C\* survivor** | Numeric amp-invariance on triads; **not proved** |
| **Kill drill** | Max pre-Young \(\lvert R_{\mathrm{pre}}\rvert\approx5.09\); almost-shell \(\mathcal R_\star\) probe — **survives**, not a proof; sample list ≠ \(C_{\mathrm{geom}}\) |
| **Does not buy** | Clay / unconditional GR |
| **Status** | **LEAD / OPEN**; **NS NOT SOLVED**; see `LEMMA_STAR_SHAPE_FORM.md` |

---

## LEAD — Route N (shellwise convex bypass)  **[2026-09-08]**

| | |
|--|--|
| **Where** | `docs/math/NS-EXTRACTION-LEDGER.md`; probe `scripts/route_n_shell_floor_probe.py` |
| **Idea** | \(H_M[a]=\sum_j a_j B_{M,j}\); convexity \(\Rightarrow\lambda_{\min}(H_M[a])\ge\min_j\lambda_{\min}(B_{M,j})\) |
| **Convexity** | **TRUE** for Hermitian convex combinations (Rayleigh / min-max) |
| **Buys** | If uniform shellwise \(B_{M,j}\succeq(-1/2+\delta)I\), eliminates dynamic simplex / dominant-shell ratio / no-crossing **for the auxiliary operator only** |
| **Shellwise \(\widetilde Q\) principal blocks** | Probe through \(M=256\): \(\min_j\lambda_{\min}\approx-0.234>-1/2\) even when full \(\lambda_{\min}(\widetilde Q)<-1/2\) — **LEAD** |
| **Shellwise \(H_M\) principal blocks** | Probe: clears \(-1/2\) in checked range — **LEAD / not a theorem** |
| **Does not buy** | NS regularity; still need PDE bridge |
| **Status** | **LEAD** (convexity lemma + \(H\)-shell empirics); PDE gap remains **HARD**; do **not** claim Clay |

---

## KILLED this DA pass (Aug 27)

| Claim | Why killed | Evidence |
|-------|------------|----------|
| Route C Lemma A (\(\mu\varphi/d^2\)) | False at \(\gcd=2\) | `route_c_gap_a_verify.py` max entry error |
| \(R(v_{\mathrm{alt}})\to -1/(2\pi)\) | Ratio \(\to 4\)–\(6\times\) target, growing | N=500,1000 verifier |
| \(v_{\mathrm{alt}}^\top Q v\sim -\log N/(2\pi)\) | Same divergence | Same script |
| Zero-diag positive-GCD \(>-1/2\) | \(\lambda_{\min}(\widehat Q_5)\approx -0.79\) | `positive_gcd_floor_verify.py` |

**Reframe:** spectral target is \(\lambda_{\min}/\log N\to -1/(2\pi)\), not \(R(v_{\mathrm{alt}})\).  
**Proved auxiliary:** parity split Lemmas in `05_route_c_conditional.tex`.

---

## DA method (reuse)

1. Name the exact inequality / matrix / hypothesis.  
2. Ask: *algebraic identity?* *finite check?* *counterexample?* *needs analysis?*  
3. If algebraic or finite → close this week.  
4. If needs new PDE estimate → mark HARD; stop calling it “almost.”  
5. Update status table in the same commit as the proof.

---

## File map

| Artifact | Path |
|----------|------|
| Multi-rep proof | `docs/papers/submit/04_q6_inverse_gcd.tex` |
| Bridge\* digest | `docs/BRIDGE-STAR-PROOF.md` |
| This plan | `docs/math/CLOSURE-ATTACK-PLAN.md` |
| Cool Check kills | `docs/math/COOL-CHECK.md` |
| Route N ledger | `docs/math/NS-EXTRACTION-LEDGER.md` |
| Route N probe | `scripts/route_n_shell_floor_probe.py` |
