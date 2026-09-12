# Uniform \(\mathcal{R}_\star\) attack — analytic reduction + numeric status

**Date:** 2026-09-12  
**Branch:** `cursor/uniform-rstar-attack-0cc5`  
**Honesty lock:** Lemma★ / DA-NS-1 remains a **HYPOTHESIS**. Clay Statement B is **not solved**. Numerics ≠ proof.  
**Live target:** PRODUCT-BLOCK = \(\sup_v\mathcal{R}_\star(v)<\infty\) with a geometry-only constant.  
**Research policy (locked):** [`RESEARCH-POLICY.md`](./RESEARCH-POLICY.md) — main path = analytic structure / efficient mathematical expression of truth; **not** an HPC/supercomputer arms race; light probes only as sanity checks. Still **OPEN**; no Clay claim.

> i dont want to get in the ring with a supercomputer. i would not survive. but i can say do whatever is the logical and most efficient way to express the truth mathematically.

**Lead route:** \(T_c\) structure + Λ-relative HH channel reduction (§2). Numerics (§3) are subordinate.

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

1. **HL / LL classical (if available).** On HL and LL channels, at least one parent is low relative to \(\Lambda\). Standard 3D product / paraproduct estimates at the energy–enstrophy scale are expected to give
   \[
   \bigl(T_c^{\mathrm{HL}}+T_c^{\mathrm{LL}}\bigr)_+^2
   \le
   C_{\mathrm{HL/LL}}\,D_s\,E\,Y
   \]
   (or a Young form feeding the same Gronwall). This step is **classical-ish bookkeeping**, not the prize difficulty — but it must still be written carefully with the centered weight \(\lambda_k(\lambda_k-\Lambda)\). Status on this branch: **assumed as a lemma to prove**, not claimed closed in code.

2. **HH is the bottleneck.** The remaining piece is
   \[
   \bigl(T_c^{\mathrm{HH}}\bigr)_+^2
   \le
   C_{\mathrm{HH}}\,D_s\,E\,Y.
   \]
   Ordinary Agmon / energy-only Sobolev products do **not** deliver this for all \(v\). This is the live PRODUCT-BLOCK core (historical diagnostic label “HH→L”: **input** channel, not a proved high→low output map).

3. **Therefore:** if (1) and (2) both hold with geometric constants, then
   \[
   \sup_v\mathcal{R}_\star(v)<\infty
   \]
   and the energy-budget form of Lemma★ closes → Gronwall on \(\Lambda(t)\) → continuation (Statement B packaging).  
   **Conversely:** without HH control, the reduction does **not** close PRODUCT-BLOCK.

**Status of the reduction itself:** the *logic* “HL/LL classical + HH bound ⇒ uniform \(\mathcal{R}_\star\)” is the intended attack map. **Neither** half is proved as a theorem on this branch. HH remains **OPEN**. Do not green DA-NS-1.

---

## 3. Numeric attack (stress tests, not proofs)

**Subordinate to analysis.** Light probes / kill searches only — not a supercomputer campaign. Finite max ≠ \(\sup\); numerics ≠ proof.

Executable probe (self-contained core, no external Stokes eigenbasis):

```bash
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

---

## 4. Honesty / DA status

| Item | Status |
| --- | --- |
| PRODUCT-BLOCK / uniform \(\mathcal{R}_\star\) | **OPEN** |
| Lemma★ / DA-NS-1 | **HYPOTHESIS** |
| HH-channel bound | **GAP (live)** |
| HL/LL classical reduction | **Not filed as proved** (attack map only) |
| Kill family found | Record from latest probe run (default expectation: **no**) |
| Clay Statement B | **NOT SOLVED** |
| False \(X^{3/2}\) universal | **DISCARDED** |
| Numerics = proof? | **No** |

Domain Architect: packaging symbols typically Level-0 on mainline CLI; do not treat DA output as greening PRODUCT-BLOCK. See [`DA-AUDIT.md`](./DA-AUDIT.md).

---

## 5. One-line status

**Uniform \(\mathcal{R}_\star\) still OPEN. HH control would close the reduction if HL/LL are classical; HH unbound. NS / Clay B not solved. Numerics ≠ proof.**
