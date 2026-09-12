# Uniform \(\mathcal{R}_\star\) attack — analytic reduction + numeric status

**Date:** 2026-09-12  
**Branch:** `cursor/uniform-rstar-attack-0cc5` (HH push via `cursor/uniform-rstar-hh-push-3c58`; dilation via `cursor/uniform-rstar-dilation-00ef`)  
**Honesty lock:** Lemma★ / DA-NS-1 remains a **HYPOTHESIS**. Clay Statement B is **not solved**. Numerics ≠ proof.  
**Live target:** PRODUCT-BLOCK = \(\sup_v\mathcal{R}_\star(v)<\infty\) with a geometry-only constant.  
**Research policy (locked):** [`RESEARCH-POLICY.md`](./RESEARCH-POLICY.md) — main path = analytic structure / efficient mathematical expression of truth; **not** an HPC/supercomputer arms race; light probes only as sanity checks. Still **OPEN**; no Clay claim.  
**Credit / show-work:** [`CREDIT-BODY-OF-WORK.md`](./CREDIT-BODY-OF-WORK.md) · [`../campaign/TWO-YEARS-MAP.md`](../campaign/TWO-YEARS-MAP.md).  
**Publisher/X gate:** [`GATED-PUBLISH-CHECKLIST.md`](./GATED-PUBLISH-CHECKLIST.md) — **INACTIVE**.

> i dont want to get in the ring with a supercomputer. i would not survive. but i can say do whatever is the logical and most efficient way to express the truth mathematically.

**Lead route:** \(T_c\) structure + Λ-relative HH channel reduction (§2). Numerics (§3) are subordinate.

**Close-attempt progress (2026-09-12):** [`UNIFORM-RSTAR-PROGRESS.md`](./UNIFORM-RSTAR-PROGRESS.md) — Lemmas A–M: dilation ledger; HH mass; elementary Λ-HL/LL **killed**; Cauchy-only \(\sup Q\) **strategically blocked** (face family); geometric HL/LL and HH **OPEN**; no \(\mathcal{R}_\star\) kill; still **OPEN**.

---

## 1. What is being attacked

Shape quotient (amplitude- and dilation-invariant):

\[
\mathcal{R}_\star(v)=\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,E\,Y}
\qquad(D_s E Y>0).
\]

Uniform bound \(\Leftrightarrow\) finite geometric \(C_{\mathrm{geom}}\) in
\((T_c)_+^2\le C_{\mathrm{geom}}\,D_s\,E\,Y\).

**Discarded (do not revive):** universal \(|T_c|\le C\|v\|_2 X^{3/2}\). Under \(v\mapsto a v\), LHS \(\sim a^3\), RHS \(\sim a^4\). Archive only.

---

## 2. Analytic reduction (conditional close)

Write the nonlinear triad through a Λ-relative Bony **input** split. Fix \(\theta>0\) (default \(\theta=1\)) and declare mode \(k\) **high** iff \(\lambda_k\ge\theta\Lambda\). Parent pairs \((p,q)\) contributing to \(\widehat B_k\) are classified HH / HL / LL accordingly. Then

\[
T_c=T_c^{\mathrm{HH}}+T_c^{\mathrm{HL}}+T_c^{\mathrm{LL}}.
\]

**Conditional reduction (honest):**

1. **HL / LL (not filed as classical).** On HL and LL channels, at least one parent is low relative to \(\Lambda\). The *intended* bound is
   \[
   \bigl(T_c^{\mathrm{HL}}+T_c^{\mathrm{LL}}\bigr)_+^2
   \le
   C_{\mathrm{HL/LL}}\,D_s\,E\,Y
   \]
   (or a Young form feeding the same Gronwall). **Correction (close attempt):** elementary Sobolev / paraproduct estimates lose dilation-invariant control (field-dependent \(\Lambda\) powers). HL/LL is **OPEN**, not “classical bookkeeping done.” See [`UNIFORM-RSTAR-PROGRESS.md`](./UNIFORM-RSTAR-PROGRESS.md).

2. **HH is also unbound.** The high×high piece is
   \[
   \bigl(T_c^{\mathrm{HH}}\bigr)_+^2
   \le
   C_{\mathrm{HH}}\,D_s\,E\,Y.
   \]
   Ordinary Agmon / energy-only Sobolev products do **not** deliver this for all \(v\). Historical diagnostic label “HH→L”: **input** channel, not a proved high→low output map. Together with open HL/LL, this is the live PRODUCT-BLOCK core.

3. **Therefore:** if (1) and (2) both hold with geometric constants, then
   \[
   \sup_v\mathcal{R}_\star(v)<\infty
   \]
   and the energy-budget form of Lemma★ closes → Gronwall on \(\Lambda(t)\) → continuation (Statement B packaging).  
   **Conversely:** without both channel bounds, the reduction does **not** close PRODUCT-BLOCK.

**Status of the reduction itself:** the *logic* “HL/LL bound + HH bound ⇒ uniform \(\mathcal{R}_\star\)” is the intended attack map. **Neither** half is proved. HL/LL is **not** classical on present estimates; HH remains **OPEN**. Sufficient form: \(\|A^{1/2}B\|_2^2\le C E Y\). Do not green DA-NS-1.

**Efficient mathematical target (policy):** express HH control as a clean geometric inequality on the high×high triad sum — not as a larger Fourier box. See [`RESEARCH-POLICY.md`](./RESEARCH-POLICY.md).

---

## 3. Numeric attack (stress tests, not proofs)

**Subordinate to analysis.** Light probes / kill searches only — not a supercomputer campaign. Finite max ≠ \(\sup\); numerics ≠ proof.

Executable probe (self-contained core, no external Stokes eigenbasis):

```bash
python3 scripts/ns_attacks/uniform_rstar_identities.py   # Lemmas A–D checks + light kill sanity
python3 scripts/ns_attacks/uniform_rstar_dilation.py     # Lemmas G–J: dilation / dichotomy / Λ-route kill
python3 scripts/ns_attacks/uniform_rstar_hh_push.py      # Lemmas K–M: HH mass / face Q-block / HH→L
python3 scripts/ns_attacks/uniform_rstar_attack.py
python3 scripts/ns_attacks/uniform_rstar_attack.py --quick
```

What it does:

| Lane | Purpose |
| --- | --- |
| Λ-relative HH/HL/LL split of \(T_c\) | Channel diagnostic; check channel-sum \(\approx T_c\) |
| Two-shell maximizers | Finite-sample ceilings of \(\mathcal{R}_\star\) |
| Near-shell / eps-shell packets | Near-degenerate \(D_s\) stress |
| Triad packets | Classical stretching support |
| Random bands / HH-heavy amp | Broadband + high-amp high-shell |
| Amplitude false-product check | Reconfirm \(X^{3/2}\) universal dies; \(\mathcal{R}_\star\) flat in \(a\) |

**Kill lane:** a smooth family with \(\mathcal{R}_\star(v_n)\to\infty\) would kill the packaging. Absence of such a family in finite samples leaves kill lane **LIVE** and proof lane **OPEN**.

Artifacts: `/opt/cursor/artifacts/uniform-rstar-attack/`.

### 3.1 Latest finite-sample ceiling (this branch)

From `python3 scripts/ns_attacks/uniform_rstar_attack.py` (seed 20260912):

| Quantity | Value |
| --- | --- |
| max \(\mathcal{R}_\star\) (default seed, full pass) | \(\approx 1.86\times 10^{-2}\) (`triad_packet_max`) |
| max \(\mathcal{R}_\star\) (quick pass, same seed) | \(\approx 4.49\times 10^{-2}\) (RNG path differs) |
| Observed ceiling across passes | \(\approx 4.5\times 10^{-2}\) on tested families |
| Kill family found? | **No** |
| Channel-sum error \(\lvert\sum_{\mathrm{ch}}T_c^{\mathrm{ch}}-T_c\rvert\) | \(\lesssim 10^{-14}\) |
| False-product \(\lvert T_c\rvert/(\|v\|_2 X^{3/2})\) max/min under \(a\in[1/4,8]\) | \(32\) (\(=1/a\) scaling) while \(\mathcal{R}_\star\) flat |
| PRODUCT-BLOCK | **still OPEN** |

These ceilings are tiny on the sampled families; that does **not** prove \(\sup\mathcal{R}_\star<\infty\).

---

## 4. Honesty / DA status

| Item | Status |
| --- | --- |
| PRODUCT-BLOCK / uniform \(\mathcal{R}_\star\) | **OPEN** |
| Lemma★ / DA-NS-1 | **HYPOTHESIS** |
| HH-channel bound | **GAP (live)** |
| HL/LL geometric bound | **OPEN** (elementary unmatched-Λ route **killed**; see PROGRESS Lemmas G–J) |
| Cauchy-sufficient \(\sup Q<\infty\) | **STRATEGICALLY BLOCKED** (face family; Conjecture \(Q\to\infty\)) |
| Kill family found | Record from latest probe run (default expectation: **no**) |
| Clay Statement B | **NOT SOLVED** |
| False \(X^{3/2}\) universal | **DISCARDED** |
| Publisher / X “clean proof” | **Gate CLOSED** — [`GATED-PUBLISH-CHECKLIST.md`](./GATED-PUBLISH-CHECKLIST.md) |
| Numerics = proof? | **No** |

Domain Architect: packaging symbols typically Level-0 on mainline CLI; do not treat DA output as greening PRODUCT-BLOCK. See [`DA-AUDIT.md`](./DA-AUDIT.md).

---

## 5. One-line status

**Uniform \(\mathcal{R}_\star\) still OPEN. Elementary Λ-HL/LL killed; Cauchy-only \(\sup Q\) blocked by face family; geometric HL/LL and HH unbound. No \(\mathcal{R}_\star\) kill. NS / Clay B not solved. Publisher gate CLOSED. Numerics ≠ proof.**
