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
