# Grok conclusions — RETIRED (FALSE)

**Date:** 2026-09-10  
**Audience:** Jonathan R. Simons / Domain Architect NS review  
**Rule:** Truth only. **NS NOT SOLVED.** No SFE. No “almost proved.”

These older Grok conclusions are **FALSE** and **RETIRED**. Do not cite them as status.

---

## 1. “The kill lane is closed” — **FALSE / RETIRED**

**Claim (retired):** Numeric search failed to find a counterexample ⇒ the kill lane is closed.

**Why false:** Failure to find a numerical counterexample does **not** close that lane.

**Correct status:**

| Direction | Status |
|-----------|--------|
| Falsification (\( \mathcal R_\star\to\infty \) or live \(D_s=0\) & \(T_c>0\)) | **LIVE** |
| Proof (uniform bound on \(\mathcal R_\star\)) | **LIVE** |

Both directions remain open. **Attack 9A (AP packet) did not kill ★** (\(D_s\) grew faster) and does **not** close the kill lane — refuse “AP packet closed kill lane.” Next falsification family: **Attack 9B** exact-shell + closing → \(K_{\alpha,\beta}\) ([`ATTACK-9B-EXACT-SHELL-CLOSING.md`](./ATTACK-9B-EXACT-SHELL-CLOSING.md)). Proof still requires a triadic / HH→L reason that is **not written**.

**DA encoding:** `domain_architect/lemma_star.py` → kill lane status = `LIVE`; refuses “kill lane closed” and “AP packet closed kill lane.”
---

## 2. “Amplitude or frequency makes the ratio smaller” — **FALSE / RETIRED** (for exact \(\mathcal R_\star\))

**Claim (retired):** Increasing amplitude or frequency makes “the ratio” smaller.

**Scope error:** That remark concerns an **older, non-optimized budget ratio** (e.g. post-Young / non-shape quotients that still carry amplitude scaling). It does **not** apply to the correct shape quotient \(\mathcal R_\star\).

**Correct lock-in:** \(\mathcal R_\star\) is **exactly invariant** under amplitude and under uniform Fourier dilation:

\[
\mathcal R_\star(av)=\mathcal R_\star(v),
\qquad
\mathcal R_\star\bigl(v(n\cdot)\bigr)=\mathcal R_\star(v).
\]

Exact formula (attestation required before any numeric comparison):

\[
\mathcal R_\star(v)=\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,\|v\|_2^2\,Y(v)}.
\]

**Do not compare** legacy reported values \(0.065\), \(0.073\), \(1.93\times10^{-3}\) unless **each** was computed with that exact \(\mathcal R_\star\). Without per-value attestation, those numbers are **not comparable**.

**DA encoding:** `domain_architect/rstar_quantities.py` → amplitude / dilation invariance checks; comparison warning without exact-formula attestation.

---

## Related

- [`LEMMA-STAR-EXACT-FORMULAS.md`](./LEMMA-STAR-EXACT-FORMULAS.md) — exact \(T_c\), \(D_s\), \(\mathcal R_\star\)
- [`ATTACK-8-RECORD.md`](./ATTACK-8-RECORD.md) — revised Attack 8 is the correct attack record
- [`LEMMA-STAR-SIDE-ARCHIVE.md`](./LEMMA-STAR-SIDE-ARCHIVE.md) — LP-shell / Route N / Q6 / \(M=256\) floor (not ★ evidence)
- PRs: [#48](https://github.com/simons357/Ship_it_app/pull/48) five-lane · [#50](https://github.com/simons357/Ship_it_app/pull/50)–[#52](https://github.com/simons357/Ship_it_app/pull/52) R_★ encoding
