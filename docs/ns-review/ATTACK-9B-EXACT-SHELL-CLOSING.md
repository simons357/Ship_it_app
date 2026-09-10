# Attack 9B — Exact-shell coherent fan + small closing packet

**Date:** 2026-09-10  
**Name (locked):** **Attack 9B — Exact-shell + closing packet**  
**Branch:** `cursor/da-attack9b-precision-0cc5`  
**Prior:** Attack 9A (AP packet) = **negative for kill** — [`ATTACK-9-COHERENT-PACKET-FAN.md`](./ATTACK-9-COHERENT-PACKET-FAN.md)  
**Also:** Attack **9C** fixed-gap = **not a kill** (SoT-only) — [`ATTACK-9C-FIXED-GAP-SPHERES.md`](./ATTACK-9C-FIXED-GAP-SPHERES.md)  
**Depends on:** exact \(\mathcal R_\star\) ([`LEMMA-STAR-EXACT-FORMULAS.md`](./LEMMA-STAR-EXACT-FORMULAS.md)); bookkeeping [`FIVE-LANE-BOOKKEEPING.md`](./FIVE-LANE-BOOKKEEPING.md)  
**Status:** **LIVE kill attempt** (numerics). Finite sample **NOT** a kill. Lemma★ **OPEN**. **NS NOT SOLVED.** Kill lane **LIVE**.  
**Five-lane twin:** [`five-lane-recovery/docs/math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md`](./five-lane-recovery/docs/math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md)

## Naming (locked)

| ID | Meaning |
|----|---------|
| **9A** | AP packet — **fail** |
| **9B** | Exact-shell + closing → \(K_{\alpha,\beta}\) — **this note** |
| **9C** | Fixed-gap spheres — natural same-shell **not** a kill |
| **9D** | Designed \(\Theta(m^2)\)-closure, locked phases |

---

## Family

\[
v_\varepsilon = w_\alpha + \varepsilon z_\beta,
\qquad
A w_\alpha=\alpha w_\alpha,
\quad
A z_\beta=\beta z_\beta.
\]

\[
z_\beta \parallel \Pi_\beta B(w_\alpha,w_\alpha).
\]

Spectral variance \(\mathcal{D}_s\) opens **only** via the closing component. At \(\varepsilon=0\), exact single shell \(\Rightarrow\mathcal{D}_s=0\) (vacuous, not a kill).

---

## Boxed quantity \(K_{\alpha,\beta}\) (correct lock)

\[
\boxed{
K_{\alpha,\beta}
=
\sup_{A w=\alpha w}
\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}
}
\]

Code: `domain_architect/kab_quantity.py`. Quotient for \(\varepsilon\)-family: canonical **`ratio_R_star_shape`** — **not** legacy **`ratio_star`**.

---

## \(\varepsilon\to0\) asymptotics

Normalize \(\|w\|_2=1\), \(\|z\|_2=1\), \(z=\pm\Pi_\beta B(w,w)/\|\Pi_\beta B(w,w)\|_2\). Energies \(e_\alpha=1\), \(e_\beta=\varepsilon^2\).

\[
\mathcal{D}_s
=\frac{\alpha\beta(\alpha-\beta)^2 e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}
\sim\beta(\alpha-\beta)^2\varepsilon^2,
\qquad
Y\sim\alpha^2,\qquad\Lambda\to\alpha.
\]

\[
T_c(v_\varepsilon)\sim\beta(\beta-\alpha)\,\varepsilon\,\|\Pi_\beta B(w,w)\|_2
\]
(stretch orientation so \(T_c>0\)).

\[
\mathcal{R}_\star(v_\varepsilon)
=\frac{(T_c)_+^2}{\mathcal{D}_s\|v\|_2^2 Y}
\;\xrightarrow{\varepsilon\to0}\;
\frac{\beta\,\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2}
\]
for unit \(w\). \(\varepsilon\) and \((\alpha-\beta)\) cancel in the limit:
\[
\lim_{\varepsilon\to0}\mathcal{R}_\star(w+\varepsilon z_\beta(w))=K_{\alpha,\beta}(w)\le K_{\alpha,\beta}.
\]

---

## Precision — runtime max is **not** HH→L

| Metric | Value |
|--------|-------|
| \(\max K\) (seed 1390) | \(\approx 0.641\) at \((\alpha,\beta)=(4,8)\) |
| \(\beta>\alpha\)? | **Yes** → **higher-shell** transfer |
| HH→L? | **No** — genuine HH→L needs \(\beta<\alpha\) |
| Controls / \(\varepsilon\)-limit | **PASS** |
| Verdict | Finite sample — **not** a kill; kill lane **LIVE**; **NS not solved** |

Attack 3 filters high-frequency **inputs**; it does **not** restrict output to low → **not strictly HH→L**. Kill uses **total** signed \(T_c\).

---

## Required controls

| Control | Requirement |
|---------|-------------|
| Exact shell | Pure \(w_\alpha\) ⇒ \(D_s=0\) |
| Closing alignment | \(z_\beta \parallel \Pi_\beta B(w_\alpha,w_\alpha)\); \(\beta\neq\alpha\) |
| Complete \(T_c\) | Signed, full triad — never HH→L-only |
| Exact \(\mathcal R_\star\) | `ratio_R_star_shape` only |
| \(\varepsilon\)-cancel | Limiting quotient matches \(K\) |
| HH→L tag | Only when \(\beta<\alpha\) |
| Kill lane | **LIVE**; finite samples do **not** close it |

---

## Caveat — narrow ≠ \(O(1)\) \(D_s\)

\[
D_s=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2
\]
amplifies small lattice gaps. Exact shell first; then controlled thickness; then **9D** \(\Theta(m^2)\) — **not** another AP widen.

---

## Decisive reading

| Outcome | Meaning |
|---------|---------|
| Sample \(K\) unbounded | Counterexample route still open |
| Bounded sample max | Those shells did not kill ★ — **≠** proof |
| Max at \(\beta>\alpha\) | **Not** HH→L |
| Natural fixed-gap (9C) | **Not** a kill — SoT-only \(0.11\to0.031\) |

**NS NOT SOLVED.**

## Hard refusals

- Refuse “9B killed ★” / “kill lane closed” / “AP packet closed kill lane.”
- Refuse “same-shell ensemble kills ★.”
- Refuse calling \((4,8)\) max an HH→L witness.
- Refuse comparing `ratio_star` to `ratio_R_star_shape`.

## Jonathan action

**None.**
