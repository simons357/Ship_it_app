# C10 — depletion ⇒ (A): theorem-shaped target

> **NOT CLAY. NS NOT SOLVED. C10 OPEN.**
>
> This note is a **target statement only**. No proof is claimed. No regularity is claimed.
> Unaugmented classical 3D Navier–Stokes is kept distinct from any \(Q_1\)-augmented PDE.
>
> **Ledger stance (do not green):** July 23 CLAIM LEDGER — **NS-10 OPEN**, **NS-11 NOT CLAIMED**.
> Centered face — **DA-NS-2 OPEN**. Same-scale shell remainder \(T_{j\leftarrow j}\) — **OPEN**.

**Date:** 2026-10-02  
**Face:** Jonathan’s **unaugmented** NS shell program (axisymmetric restriction labeled where used).  
**Parent filter:** [`TJ-SAME-SCALE-CANDIDATES.md`](./TJ-SAME-SCALE-CANDIDATES.md) §5–§6 (hard-run + harder-run on PR #102).  
**Honesty lock:** [`UNAUG-PROOF-CHAIN.md`](./UNAUG-PROOF-CHAIN.md).

---

## 1. What C10 is

**C10** is the principal empty door on the unaugmented face: prove a **non-circular depletion** of the local positive stretch (or an honest integrable substitute) strong enough that the same-scale block enters the enstrophy–palinstrophy comparison **(A)**, thereby giving a path to control \(T_{j\leftarrow j}\) without recycling \(\dot e_j\), \(\dot Z\), or \(\Lambda'\). Hard-runs (2026-09-16, 2026-10-01) found **no** seated theorem; every non-circular sketch collapsed onto weakened feeders (C6 / C11 / C8). C10 **survives as the named write**, not as a proved inequality.

---

## 2. Precise target statement

**Setting.** Smooth, divergence-free, rapidly decreasing fields on the unaugmented classical NSE face. Shell quantities \(Z_j=\|\Delta_j\omega\|_2^2\), palinstrophy \(P_j\) as in the (A)-normalized comparison of the honesty lock, local velocity \(u_{\mathrm{loc}}=(\Delta_{j-1}+\Delta_j+\Delta_{j+1})u\), and

\[
\alpha_{\mathrm{loc},j}=\xi_j\cdot S(u_{\mathrm{loc}})\,\xi_j,\qquad
(\alpha_{\mathrm{loc},j})_+=\max(\alpha_{\mathrm{loc},j},0),
\]

on \(\{\Delta_j\omega\neq 0\}\), with \(\xi_j=\Delta_j\omega/\lvert\Delta_j\omega\rvert\) and \(S=\tfrac12(\nabla u+(\nabla u)^\top)\).

**(A) (program sense).** The enstrophy–palinstrophy route in which \(\rho_j<\nu\) (normalized by \(P_j\)) can enter the estimate — **not** absorption of same-scale transfer into the shell-energy viscous term \(\nu Z_j\).

**Target (C10 through the honest C6 hinge).** Exhibit a geometric, or explicitly labeled conditional, control of \((\alpha_{\mathrm{loc},j})_+\) (or an integrable substitute) such that the main local stretch satisfies, for some \(0<\theta<1\),

\[
\int (\alpha_{\mathrm{loc},j})_+\,\lvert\Delta_j\omega\rvert^2
\;\le\;
\theta\nu P_j
\;+\;
R_{\mathrm{allowed}},
\]

and deduce that this implies **(A)** for the same-scale contribution, **without** using \(\dot e_j\), \(\dot Z\), \(\dot Z_j\), or \(\Lambda'\) as controlling quantities, and **without** passing through the Bernstein cubic wall as the bound.

**Allowed \(R_{\mathrm{allowed}}\):** energy \(\mathcal{E}\), shell enstrophies \(\{Z_k\}\), and (if needed) an explicitly declared direction / geometric factor — not time derivatives of the budget, not spectral-shift rates, not BKM \(\|\omega\|_\infty\) sold as a weaker shortcut.

**Killed absolute pretenses (harder-run):** Sobolev control of \(\alpha_+\) by \(P_j\) alone is **false** (\(\alpha_+ Z/(\nu P)\sim\lambda^{1/2}\to\infty\)). Pointwise CZ / Biot–Savart “\(\lvert\alpha\rvert\lesssim\lvert\omega\rvert\)” does not close the door. Φ-renorm algebra is **not** standalone depletion.

---

## 3. What may be used

| May use | Role |
| --- | --- |
| **C6 hinge as Door-3 criterion** | Identities that main stretch \(=\alpha\) and local transport vanishes may be cited as **EXACT**; \(\alpha_+\) control remains the open criterion, not an absolute unaugmented bound |
| **EXACT shell / TJJ identities** | AS-Id, AS-Split, TJJ-Trans, TJJ-α (and seated Constantin / Miller–Chae algebra as algebra only) |
| **Named hypotheses, labeled** | Axisym-with-swirl, geometric \(\alpha\)-hypothesis, or other **explicit** conditionals — must stay labeled; conditional ≠ Clay |
| **Hard-run refuse checklists** | Use to reject circular drafts early |

---

## 4. What is forbidden

- Recycling \(\dot e_j\), \(\dot Z\), \(\dot Z_j\), or \(\Lambda'\) as the controlling bound for \(T_{j\leftarrow j}\) / (A)
- BKM \(\|\omega\|_\infty\) (or \(\|\nabla u\|_\infty\)) sold as a shortcut that “weakens” the question
- Claiming \(N_{\mathrm{eff}}\) closes Leray / classical regularity
- \(Q_1\) / Φ **weld** of augmented structure onto the unaugmented face
- SND persistence as **proved** (SND / C12 remains conditional texture only)
- Unrestricted ★ / uniform \(\sup\mathcal{R}_\star<\infty\) as proved (Lemma★ / DA-NS-1 stays HYPOTHESIS / PRODUCT-BLOCK **OPEN**)
- Numerics (occupancy ≈ 1, alignment ≈ ½, near-shell samples) ⇒ depletion / ⇒ theorem
- Energy-linear absolute (A) revived after C1 death
- Claiming NS / Clay Statement B solved

---

## 5. Why other survivors are not the write

| ID | One-liner |
| --- | --- |
| **C7** | SURVIVES as HH bottleneck laboratory; Agmon / energy-only HH products are dead — supports diagnostics, does not write depletion ⇒ (A) |
| **C8** | ★ / near-shell **lab only**; category gap vs shell-budget (A) — evidence, not the theorem |
| **C9** | WEAKENED to triad / \(\omega_*\) rewrite tool; non-feeder to C10 |
| **C11** | WEAKENED axisym \(T^{\mathrm{mm}}\) bulk target; Φ ≠ cancel; structure lane, not the principal depletion write |
| **C6** | WEAKENED to Door-3 / α-hypothesis **criterion**; absolute \(\alpha_+\) vs \(P_j\) false — the hinge inside C10, not a separate close |

---

## 6. Acceptance criteria (future proof attempt)

A future write counts as a **serious C10 attempt** only if it:

1. States **(A)** and the \(\alpha_+\) (or integrable-substitute) inequality with explicit \(\theta\), \(R_{\mathrm{allowed}}\), and function class.
2. Lists every **NEW CLAIM** vs **EXACT** / **STANDARD LEMMA**, with no omitted inequality between TJJ-α and (A).
3. Keeps the forbidden list empty (no \(\dot e_j/\dot Z/\Lambda'\), no BKM-as-shortcut, no \(Q_1\)/Φ weld, no unrestricted ★, no SND-as-proved).
4. Survives the harder-run killed pretenses (Sobolev-\(P_j\), CZ pointwise, Φ-as-depletion) or names a **labeled** conditional that changes the question honestly.
5. Does **not** claim Clay B, NS-11, DA-NS-2 close, or unaugmented regularity from the estimate alone without a separate continuation argument.
6. Distinguishes unaugmented classical NSE from any augmented Track / \(Q_1\) face throughout.

Failure modes already recorded: circular recycle; Bernstein cubic wall as the bound; “dynamics produce depletion” with empty arrow; selling lab ★ samples as shell (A).

---

## 7. Status

| Item | Status |
| --- | --- |
| This note | **OPEN** — theorem-shaped **target** only |
| Proof of depletion ⇒ (A) | **Not claimed** |
| \(T_{j\leftarrow j}\) | **OPEN** |
| NS-10 (July 23) | **OPEN** |
| NS-11 (July 23) | **NOT CLAIMED** |
| DA-NS-2 (centered) | **OPEN** |
| NS / Clay B | **NOT SOLVED / NOT CLAIMED** |

**One line:** C10 is the principal empty door — write depletion ⇒ (A) through honest \(\alpha_+\) / C6 Door-3 control, or keep it OPEN; do not fake a close.
