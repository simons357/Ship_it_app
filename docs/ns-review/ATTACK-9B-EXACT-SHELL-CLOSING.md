# Attack 9B — Exact-shell + closing packet

**Date:** 2026-09-10  
**Name (locked):** **Attack 9B — Exact-shell + closing packet**  
**Prior:** Attack 9A (AP packet) = **negative for kill** — [`ATTACK-9-COHERENT-PACKET-FAN.md`](./ATTACK-9-COHERENT-PACKET-FAN.md)  
**Depends on:** exact \(\mathcal R_\star\) ([`LEMMA-STAR-EXACT-FORMULAS.md`](./LEMMA-STAR-EXACT-FORMULAS.md))  
**Status:** Protocol / quantity lock — **not a proof**. **NS NOT SOLVED.** No SFE. Kill lane **LIVE**.

---

## Why 9B (after 9A)

Attack 9A widened an AP packet: \(T_c\) rose, but spectral variance drove \(D_s\) up **faster**. The assumption \(D_s\|v\|_2^2 Y=O(1)\) in packet size was **FALSE** for that family.

9B changes geometry:

- Put the **base packet on one exact eigenvalue shell** (many same-shell modes).
- Generate \(D_s\) only through a **small closing component** on a second shell.
- Read the kill/survive decision through a scale-free shell-to-shell quantity \(K_{\alpha,\beta}\).

---

## Family

\[
v_\varepsilon = w_\alpha + \varepsilon z_\beta,
\qquad
A w_\alpha=\alpha w_\alpha,
\quad
A z_\beta=\beta z_\beta.
\]

Choose the closing direction parallel to the projected bilinear self-interaction of the base shell:
\[
z_\beta \parallel \Pi_\beta B(w_\alpha,w_\alpha).
\]

Here \(B(u,v)=\mathbb P[(u\cdot\nabla)v]\) (or the symmetrized convention used in the exact-\(T_c\) bookkeeping), and \(\Pi_\beta\) projects onto the \(\beta\)-eigenspace of \(A=-\mathbb P\Delta\).

---

## Boxed quantity \(K_{\alpha,\beta}\)

\[
\boxed{
K_{\alpha,\beta}
=
\sup_{A w=\alpha w}
\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}
}
\]

| Feature | Lock |
|---------|------|
| Base packet | Many **same-shell** modes (\(Aw=\alpha w\)) |
| \(D_s\) source | Only the small closing component \(\varepsilon z_\beta\) (pure \(w_\alpha\) has \(D_s=0\)) |
| \(\varepsilon\)-dependence | Cancels in the **limiting** quotient as \(\varepsilon\to 0\) (with \(z_\beta\) normalized) |
| Role | Leading geometric intensity of same-shell → \(\beta\) stretching vs \(\alpha\)-scale |

Code stub: `domain_architect/kab_quantity.py`.

---

## Controls

| Control | Requirement |
|---------|-------------|
| Exact shell | Support of \(w_\alpha\) lies in \(\{|k|^2=\alpha\}\); pure \(w_\alpha\) ⇒ \(D_s=0\) |
| Closing alignment | \(z_\beta \parallel \Pi_\beta B(w_\alpha,w_\alpha)\); \(\beta\neq\alpha\) |
| Complete \(T_c\) | Signed, full triad sum — never abs; never HH→L-only for kill |
| Exact \(\mathcal R_\star\) | \(\mathcal R_\star=(T_c_+)^2/(D_s\|v\|_2^2 Y)\); amplitude + dilation invariant |
| \(\varepsilon\)-cancel | Report the limiting quotient (ε-free), not a single finite-ε spike |
| Attestation | No comparison to legacy \(0.065\) / \(0.073\) / \(1.93\times10^{-3}\) without exact formula |
| Kill lane | Remains **LIVE**; 9A/9B negatives do **not** close it |

---

## Caveat — narrow ≠ \(O(1)\) \(D_s\) on the lattice

A merely “narrow” packet does **not** automatically keep \(D_s=O(1)\). On \(\mathbb Z^3\), small eigenvalue gaps are amplified by the variance form
\[
D_s=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2.
\]
Nearby shells with tiny \(\lambda_k-\Lambda\) still contribute after the \(\lambda_k(\lambda_k-\Lambda)^2\) weight. So “almost one shell” in Fourier index space is not the same as exact-shell \(D_s=0\).

**Next clean test order (mandatory):**

1. **Exact-shell coherent fan** (pure same-shell base; \(D_s=0\) until closing is added)
2. Then **controlled finite shell thickness** (measure how \(D_s\) opens)
3. **NOT** another widening AP packet

---

## Decisive reading

| Outcome | Meaning |
|---------|---------|
| \(K_{\alpha,\beta}\) unbounded over shells / fans | Falsification route advancing (still need \(\mathcal R_\star\to\infty\) with exact formula) |
| \(K_{\alpha,\beta}\) uniformly bounded on tested exact shells | Evidence only — **≠** proof of ★ |
| Finite 9B samples of any kind | **≠** kill lane closed; **≠** Lemma★ proved |

**NS NOT SOLVED.** No SFE glue.

---

## Hard refusals

- Refuse “AP packet closed kill lane.”
- Refuse “kill lane closed” from 9A or 9B.
- Refuse greening ★ / “almost proved” / “numerics prove ★.”
- Refuse treating “narrow packet” as automatic \(D_s=O(1)\).
- Refuse another widening AP packet as the next clean test.

---

## Jonathan action

**None.** Quantity + protocol lock only.
