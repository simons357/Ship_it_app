# Lemma★ — older attempt (annotated archive)

**Date:** 2026-09-10  
**Role:** archive. **Not** the working claim. **Not** a theorem. **NS not solved.**

Working foundation: [`LEMMA_STAR_CANONICAL.md`](./LEMMA_STAR_CANONICAL.md), [`LEMMA_STAR_EXACT_FORMULAS.md`](./LEMMA_STAR_EXACT_FORMULAS.md).

This note records four failures in older writings so they are not reused as if they sat. It does not reconstruct a missing desktop file as a proof.

---

## Section 4 does not prove its advertised theorem

An older proof attempt opened a remainder involving \(\|\nabla u\|_\infty^2 X\), then ran incomplete estimates, then replaced the claim with a different conditional statement. The “proved” label cannot apply to that opening line.

That Section 4 file is **not mounted** on this branch (not in `docs/math/`, not in the five-lane export). Do not import a DA / SND pile to recover it. The operator correction is the record: advertised theorem, incomplete estimates, swapped conclusion. Archive, do not cite.

Historical formula lock that remains useful as identities (not as a close): [`LEMMA_STAR_SHAPE_FORM.md`](./LEMMA_STAR_SHAPE_FORM.md). Status board that still mixed a dead \(a^4\) bound into an open gap: [`../../five-lane-export/PROOF_LemmaStar_STATUS.md`](../../five-lane-export/PROOF_LemmaStar_STATUS.md) — that row is now **DEAD BY SCALING**.

---

## The “missing inequality” is algebraically false

Older PRODUCT-BLOCK text (five-lane Attack 3 target; DA-NS-1 on other branches) treated
\[
\lvert T_c(u)\rvert\le C\|u\|_2 X^{3/2}
\]
as the missing estimate, and sometimes as **equivalent** to \(\sup\mathcal R_\star<\infty\).

Under \(u=av\): \(T_c\sim a^3\), \(\|u\|_2\sim a\), \(X\sim a^2\), so the right side is \(a^4\). For any \(v\) with \(T_c(v)\ne 0\), send \(a\to 0\). The inequality fails. That route is discarded by algebra. HH→L can still diagnose channels. It cannot rescue an \(a^3\le C a^4\) bound.

Do not confuse this with Attack-2 \(|T_c|\le C_* X^{3/2}\Lambda\), which scales as \(a^3/a^3\).

---

## “Equivalent to global regularity” is not written

The quotient argument gives **one direction**: boxed ★ \(\Rightarrow\) no finite-time blowup of \(\Lambda\) in this packaging \(\Rightarrow\) global regularity on \(\mathbb{T}^3\) in this packaging.

No converse in these files shows that global regularity would force the uniform inequality on every smooth field. Older wording that ★ “is” the leftover in the sense of **equivalence** overstates the skeleton. Keep the implication. Drop the biconditional.

---

## Positive part vs testing all fields

Older kill notes said compression \(T_c<0\) gives \(\mathcal R_\star=0\) and is “not a stretching counterexample.” That is true of the **coded** quotient with \((T_c)_+\). It is false as a reason to ignore the field. \(T_c\) is odd; \(\mathcal D_s,E,Y\) are even. Reverse the field and the same shape stretches. Universal testing of \((T_c)_+^2\) is universal testing of \(T_c^2\).

---

## What to keep from the older stack

- Spectral identities, two-shell \(\mathcal D_s\), signed \(T_c\), \(\Lambda'\), \(\mathcal R_\star(av)=\mathcal R_\star(v)\).
- K=0 dead. Uniform pre-Young \(C\) dead. Attack-2 \(C_*\) is a different door.
- Kill criterion: \(\mathcal R_\star\to\infty\), or \(\mathcal D_s=0\) with \(T_c>0\).
- Finite samples are not \(C_{\mathrm{geom}}\).

What not to keep: the \(a^4\) missing inequality as a live target; ★ \(\Leftrightarrow\) GR; Section 4 as proved; unaligned \(z_\beta\) as if it recovered \(K_{\alpha,\beta}\).

**NS not solved.**
