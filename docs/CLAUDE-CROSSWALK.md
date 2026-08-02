# Crosswalk — Claude’s overnight referee read × our Bridge\* / operator audit

**Claude read (Drive, not in this VM):**  
`SND_FORMAL_PROOFS.tex` · `threshold_SND_final.tex` · `NS_FINAL_MERGED_UNCONDITIONAL.tex` · RH June-14 + `Q6_RH_BRIDGE_PAPER.tex`

**We have locally:** Triple Lock PDF · three-in-one · floor verifier · Bridge\* plan  
**You are fetching:** the Drive tex files Claude named — drop them in `docs/papers/` when found.

---

## Claude’s flags — keep / agree / merge with our findings

| # | Claude flag | Our take | What to grab from other versions |
| --- | --- | --- | --- |
| 1 | Ring Lemma skeleton solid; Chebyshev (Q1) constants fight | **Agree — keep.** Best NS brick. | Minor constant-range fix only |
| 2 | Ramanujan–GCD → λ_min(Q) ≥ −1 on **raw** Q via Σ φ\|S_d\|² − ‖v‖² | **Agree as bedrock for raw Q.** Note: ≥ −1 is true and weak; **not** the same as > −½ Bridge (and full λ_min of raw Q is ≪ −½) | Keep identity; don’t overclaim Bridge from it |
| 3 | SND Thm 1 Step 2: “C–S lower bound” is wrong direction — need **Riesz/frame** lower bound on rough divisor sums | **Agree — load-bearing.** This is the same species of bug as Triple Lock §2.1 (asserted arithmetic step) | Hunt version with frame/lower-Riesz, not C–S |
| 4 | SND Thm 2 asymptotic / numeric, not uniform; {p,2p} only numeric | **Agree** | Courant–Fischer both ways or demote to appendix |
| 5 | Main Thm: sinθ ≤ C not ≪ 1 (CF depletion); threshold-class / small data | **Agree — publishable as threshold, not Clay large data** | Either retitle threshold or find small-angle version |
| 6 | **H_N vs Q_N:** normalized H_N with λ_min ≥ −3/14 > −½ “in hand”; unnormalized Q_N > −½ open / GRH-walled | **This is the money line.** Matches our audit: full-spectrum Bridge on raw/normalized-as-written Q fails; **whatever matrix actually has −3/14 is the NS-side operator to lock** | Open the file that proves −3/14; paste the matrix definition **one line** |
| 7 | Merged NS: chain assumes X(t)≤M — risk of “regular ⇒ regular” | **Agree — fatal if M not from data** | Version that builds M from ‖u₀‖ only |
| 8 | Thm H sketch-level (Bony + CET cite) | **Agree — needs expansion for journal** | |
| 9 | RH June-14 honest conditional; Route J **not in that file**; Q6_RH has μφ/d² ≥ 0 handwave (false when μ<0) | **Agree.** Route J ≠ Route C; Triple Lock under **Jonathan Robert** | Don’t chase Route J inside June-14 RH |

---

## How this locks to Bridge\* (what we’re proving now)

Claude’s pin: **does NS closure use H_N (−3/14) or Q_N (open)?**

Our pin: **full-spectrum λ_min(Q)>−½ and λ_min(Q̃)>−½ are false**; restricted Goldbach Rayleigh on Q̃ still > −½.

| Track | Operator | Status |
| --- | --- | --- |
| NS threshold / SND formal | **H_N** (normalized — need exact matrix from your −3/14 file) | Possibly in hand if frame gap (#3) fixed + M from data (#7) |
| Triple Lock “Bridge” as written | raw Q or Q̃ full spectrum | **Dead as stated** |
| **Bridge\*** (this attack) | Q̃ restricted to Goldbach v_k (+ SND cone) | **Open but numerically alive** |
| RH Route C | needs same operator its lemmas use | Conditional; 2 gaps |

**Do not mix:** proving Bridge\* ≠ proving −3/14 for H_N. Both can be true on different matrices. Your job while searching files: **one line each** —

```text
H_N(i,j) = _______________     % the −3/14 matrix
Q̃_N(i,j) = 1/(gcd(i,j)·√(ij))  % Bridge* matrix (locked here)
```

---

## What I’m doing while you dig

1. Write **Bridge\*** proof draft (`docs/BRIDGE-STAR-PROOF.md`) — single-pair identity done (≥ 0); multi-rep bound in progress.  
2. Keep Ring Lemma / threshold honesty from Claude’s list in the NS credit path (swirl + threshold), not Clay.  
3. When you drop `SND_FORMAL_PROOFS.tex` / `NS_FINAL_MERGED_UNCONDITIONAL.tex` / −3/14 file into `docs/papers/`, I’ll score gap #3 and H_N vs Q_N on the actual tex.

---

## Short answer to “check rigor while I look”

Claude’s three stop-points (frame lower bound, Thm 2 uniform, CF small angle) and the H_N/−3/14 vs Q_N question are the right referee map.  
Our floor audit adds: **don’t try to close full-spectrum Bridge on Q/Q̃ — close Bridge\* and/or lock H_N.**  
That’s consistent, not a new mountain.
