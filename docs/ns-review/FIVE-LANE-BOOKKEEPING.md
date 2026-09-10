# Five-lane / Lemma★ — bookkeeping locks (USER precision)

**Date:** 2026-09-10  
**Branch:** `cursor/da-attack9b-precision-0cc5`  
**Base packs:** PR #48 (`cursor/ns-five-lane-lemma-star-1390`) recovered under [`five-lane-recovery/`](./five-lane-recovery/); Attack 9B SoT [`ATTACK_9B_EXACT_SHELL_CLOSING.md`](./five-lane-recovery/docs/math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md).  
**Rule:** Truth only. **NS is NOT solved.** Lemma★ **OPEN**. Kill lane **LIVE**.

These three locks are **canonical** for DA / five-lane Source of Truth. Do not silently reverse them in later notes.

---

## 1. Attack 3 — not strictly HH→L

| Lock | Content |
|------|---------|
| What Attack 3 does | Bony channel split on **high-frequency parent inputs** (HH / HL / LL by parent wavevector norms vs cutoff) |
| What it does **not** do | Restrict / project the **output** of \(B\) onto a low shell |
| Naming | **Not strictly HH→L** — diagnostic channel accounting only |
| Kill use | Kill decisions use **complete signed** \(T_c\), never an HH→L-only favorable slice |

Sources: [`ATTACK_3_BONY_HH_L.md`](./five-lane-recovery/docs/math/ns_attacks/ATTACK_3_BONY_HH_L.md), `scripts/ns_attacks/attack3_bony_hh_l.py`.

---

## 2. Quotient names — do not cross-compare

| Name (code) | Formula | Role |
|-------------|---------|------|
| **`ratio_R_star_shape`** (alias `ratio_R_star`) | \(\mathcal{R}_\star=(T_c)_+^2/(\mathcal{D}_s\|v\|_2^2 Y)\) | **Canonical** shape★ / kill quotient |
| **`ratio_star`** | \(T_c/(E\,X\,\Lambda)\) | **Legacy / different** post-Young packaging ratio — scales as \(1/B\) on a fixed shape |

**Lock:** Never compare numeric values of `ratio_star` to `ratio_R_star_shape` / \(\mathcal{R}_\star\). They are different objects — **do not compare**.

Source: [`LEMMA_STAR_SHAPE_FORM.md`](./five-lane-recovery/docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md), `scripts/ns_attacks/stokes_moments.py`.

---

## 3. Attack 9C — SoT-only until implemented

| Lock | Content |
|------|---------|
| Status | **SoT-only** until a dedicated probe script exists |
| Recorded observation | \(\mathcal{R}_\star\) falls with shell index: \(\approx 0.11\to 0.031\) on fixed-gap spheres; does **not** track \(m^{1/2}\) |
| PR #48 inventory | **No** sweep script and **no** sweep data artifact for 9C in PR #48 / recovered pack |
| Verdict | Natural same-shell / fixed-gap ensemble is **NOT** a kill; kill lane **LIVE** |

Source: [`ATTACK_9C_FIXED_GAP_SPHERES.md`](./five-lane-recovery/docs/math/ns_attacks/ATTACK_9C_FIXED_GAP_SPHERES.md).

---

## Packet naming (locked)

| ID | Name | Role |
|----|------|------|
| **9A** | AP / coherent packet fan | Fail — did **not** kill ★ |
| **9B** | Exact-shell + closing → \(K_{\alpha,\beta}\) | This family; finite sample \(\max K\approx0.641\) **≠** kill |
| **9C** | Fixed-gap spheres | Natural same-shell **not** a kill; SoT-only numbers |
| **9D** | \(\Theta(m^2)\) locked-phase closure | Remaining designed falsifier |

Older notes that called \(\Theta(m^2)\) “Attack 9C” are **superseded** by this naming.

---

## Confirmed sources

| Source | Location |
|--------|----------|
| Original Attack 9B | `ATTACK_9B_EXACT_SHELL_CLOSING.md` (PR #48 / recovery tree) |
| PR #48 export | [`five-lane-recovery/PR48_five_lane_export.zip`](./five-lane-recovery/PR48_five_lane_export.zip) (when present) + live branch `cursor/ns-five-lane-lemma-star-1390` |
| Shape lock | `LEMMA_STAR_SHAPE_FORM.md` |
| Moments / quotients | `stokes_moments.py` |
| Attack 3 probe | `attack3_bony_hh_l.py` |

## Jonathan action

**None.**
