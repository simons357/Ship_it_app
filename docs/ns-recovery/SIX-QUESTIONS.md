# Six questions — straight answers

**Date:** 12 September 2026  
**This book.** Anyone can read this without the backstory.  
**NS is not solved.** No singular Navier–Stokes solution is constructed.

---

## 1. Is the exact-shell 9D four-thirds coefficient proven?

**No. It is still a claim.** Specialist review has not happened.

The claimed statement is: if \(Aw=\alpha w\) and \(\beta>0\), then

\[
\|\Pi_\beta B(w,w)\|_2
\le
\frac43\frac{\alpha}{\sqrt{\beta}}\|w\|_2^2,
\]

equivalently \(K_{\alpha,\beta}(w)\le 16/9\). Optimality is not claimed.

This book does **not** stamp that coefficient. Score of the full writeup: [`ATTACK-9D-FULL-SUPPORT-SCORE.md`](ATTACK-9D-FULL-SUPPORT-SCORE.md). The claimed steps are a weighted lattice count (factor \(3\)) plus a polarization kernel (factor \(3/4\)). The elementary max of \((3/4)x^2(1-x/4)\) is \(16/9\) at \(x=8/3\); that calculus step is not the theorem. The audit checks a few shells and three count ratios \(\le 3\). Those are checks, not a lattice theorem and not a proof-assistant verification. Existing maxima \(0.641\) and \(0.456\) are not near \(16/9\). That does not unclaim the bound.

---

## 2. Are 0.641 and 0.456 the only samples?

**No.** Those two numbers are the **maxima of two different finite sweeps**. They are not a universal constant. They must not be merged into one “best \(K\)”.

| Object | What it is | Width | \(K\) |
|---|---|---|---|
| Three-shear write-up example | \(w=(\sin y,\sin z,\sin x)\), by hand | one field, \((\alpha,\beta)=(1,2)\) | **\(2/3\)** (floor of \(\sup K\), not a bound) |
| Aligned 9B (this book) | Optimized / aligned closer on exact shells | \(k_{\max}=6\), **24** \((\alpha,\beta)\) pairs | **0.641013** at \((4,8)\) |
| Natural 9D growing I/O (this book) | Random complex polarizations, growing supports | \(k_{\max}=5\), **1632** pairs (298 with \(K>0\)) | **0.469472** at \((1,2)\) |
| PR #24 grow-\(s\) | Random draw, seed 1390 | \(k_{\max}=8\), 2084 inputs, **39853** occupied rows | **0.45583** at \((16,32)\), \(s=4\) |

Those sweep maxima are **not** the write-up example. The named field \(w=(\sin y,\sin z,\sin x)\) gives \(K_{1,2}=2/3\) by hand. That is a floor, \(\sup K\ge 2/3\), not a bound and not \(C_0\). See [`NINE-D-TWO-THIRDS.md`](NINE-D-TWO-THIRDS.md). It clears \(0.641\) and \(0.456\). It does not prove \(16/9\).

---

## 3. Is there a plot or table for many shell pairs?

**Yes, a table and now plots. Not a proof.**

- Aligned 9B table of all 24 pairs: [`results/ns_five_lane_2026-09-10/attack9b_exact_shell/HEADLINE.md`](../../results/ns_five_lane_2026-09-10/attack9b_exact_shell/HEADLINE.md)
- Plot of those 24: [`results/ns_five_lane_2026-09-10/attack9b_exact_shell/K_by_ab_pair.png`](../../results/ns_five_lane_2026-09-10/attack9b_exact_shell/K_by_ab_pair.png)
- Natural 9D JSON of 1632 pairs: [`results/attack9d_growing_io/attack9d_growing_io.json`](../../results/attack9d_growing_io/attack9d_growing_io.json)
- Top 20 of that sweep: [`results/attack9d_growing_io/K_top20.png`](../../results/attack9d_growing_io/K_top20.png)
- PR #24 grow-\(s\) summary is committed on that PR; the raw per-row dump is **not** committed.

Every plotted \(K\) sits below the claimed \(16/9\approx 1.778\). That does not prove the bound.

---

## 4. Has anyone outside this circle checked the 9D algebra?

**No.**

Evaluator matches (this book’s core, PR #24 `stokes_moments`, the closure-review audit) are in-circle computational checks. They are not an independent specialist reading of the weighted sphere count or the polarization factor. The record still says specialist review pending.

---

## 5. If the 9D bound is true, does it feed a regularity argument?

**No as a regularity close.**

If \(K\le 16/9\) holds, occupancy \(s\) is gone on a single input shell. That is a written bound on exact-shell fields, not a sweep maximum. The three-shear field then sits under a named ceiling, not under a rumor.

A true \(4/3\) does not kill or repair unrestricted ★. That box is already dead by the multi-shell family \(v_n\). It does not give a continuation criterion and it does not restore ★ \(\Rightarrow\) global regularity. Ordinary NS stays open. It is an **exact-shell** bound on \(\|\Pi_\beta B(w,w)\|_2\). That is not unrestricted Lemma★.

- The growing-layer family \(v_n\) that killed unrestricted ★ is **not** exact-shell. 9D does not control it.
- Near-shell, \(\mathcal R_\star(w+\varepsilon z_\beta)\to K_{\alpha,\beta}(w)\) only for an aligned, sign-selected closer. That is a restricted family.
- The unaugmented regularity program used unrestricted ★ as closure. That closure is **dead**. Nobody has written a chain “9D \(\Rightarrow\) global regularity.”
- Soft X, SND, Theorem H stay silent. Do not glue them in.

Until a specialist signs the algebra, or a sweep shows nothing near \(16/9\), the word is still **CLAIMED**. Soft X silent.

---

## 6. What is the actual replacement closure, and has anyone started writing it?

**There is no written replacement theorem.** What exists is a framing page and one negative check.

Two *kinds* of replacement were named. Neither is a theorem:

1. **Restricted class** (same \(\mathcal R_\star\) ratio, fewer fields). Bounded eigenvalue aspect **fails** as a repair: \(v_n\) has aspect exactly 6, so any class with aspect \(\le R\) and \(R\ge 6\) still contains the diverging family. One-shell fields are vacuous (\(D_s=T_c=0\)). A two-shell or sparse-spectrum class has **not** been written.
2. **A different inequality** (extra factor in the denominator). On \(v_n\), \(\mathcal R_\star/\sqrt{X/E}\) does not climb. That is a diagnostic on one family. It is **not proved**, not checked elsewhere, and not known to close regularity.

A **time-integrated** version of the old ★ bound has **not** been started. The viscosity packaging already in the canonical page is the same instantaneous statement in other clothes; integrating a false uniform bound does not repair it.

Page: [`REPLACEMENT-CLOSURE.md`](REPLACEMENT-CLOSURE.md).  
Need★ cannot restore the old box unless its hypotheses change.

---

**NS not solved.** Do not send a Clay / regularity close.
