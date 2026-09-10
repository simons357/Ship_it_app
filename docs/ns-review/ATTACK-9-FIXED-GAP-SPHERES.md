# Attack 9 — Fixed-gap spheres (natural same-shell ensemble)

**Date:** 2026-09-10  
**Name (locked):** **Attack 9 — Fixed-gap spheres**  
**Prior:** Attack 9A (AP packet) = **negative for kill** — [`ATTACK-9-COHERENT-PACKET-FAN.md`](./ATTACK-9-COHERENT-PACKET-FAN.md)  
**Sibling family:** Attack 9B exact-shell + closing → \(K_{\alpha,\beta}\) — [`ATTACK-9B-EXACT-SHELL-CLOSING.md`](./ATTACK-9B-EXACT-SHELL-CLOSING.md)  
**Depends on:** exact \(\mathcal R_\star\) ([`LEMMA-STAR-EXACT-FORMULAS.md`](./LEMMA-STAR-EXACT-FORMULAS.md))  
**Status:** **USER LOCK-IN — negative for kill** (natural same-shell ensemble). Kill lane still **LIVE**. **NS NOT SOLVED.** No SFE. No “almost proved.” ★ **not** proved.

---

## Result (lock exactly)

Fixed-gap spheres \(n\) and \(n+d\):

| Lock | Content |
|------|---------|
| Geometry | Support on two shells separated by a **fixed gap** \(d\) (spheres at \(n\) and \(n+d\)) |
| \(D_s\) source | From the **gap** (not from packet width / AP widening) |
| Closures | Only \(O(m)\) |
| \(\mathcal R_\star\) vs \(n\) | **Falls** with \(n\): **\(0.11\to 0.031\)** for **this family** |
| Scaling | Does **not** track \(m^{1/2}\) |
| Kill decision | **Natural same-shell ensemble is not a kill** |

**Hard refusal:** Refuse “same-shell ensemble kills ★.” Finite fixed-gap / natural same-shell samples ≠ \(\mathcal R_\star\to\infty\).

**Do not** revive AP widening as the next clean test (9A already negative; \(D_s\) grew faster there).

---

## Exact \(\mathcal R_\star\) attestation (required)

The numbers **\(0.11\to 0.031\)** are attested as **this family's** \(\mathcal R_\star\) under the **exact** shape quotient only:

\[
\mathcal R_\star(v)=\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,\|v\|_2^2\,Y(v)}.
\]

- Positive part: \(T_c_+=\max(T_c,0)\).
- Complete signed \(T_c\) (never abs; never HH→L-only proxy for the kill decision).
- Amplitude / uniform Fourier dilation invariances hold for this quotient.
- **Do not** compare these values to unattested legacy numbers \(0.065\), \(0.073\), \(1.93\times10^{-3}\).

Falling \(\mathcal R_\star\) with \(n\) is evidence that this natural ensemble **fails** the kill route — it is **not** a uniform bound and **not** a proof of ★.

---

## Relation to Attack 9A / 9B

| Family | Role | Status |
|--------|------|--------|
| **9A** AP coherent packet/fan | Widening AP packet | **Negative for kill** (\(D_s\) grew faster) |
| **Fixed-gap spheres** (this doc) | Natural same-shell / fixed-gap ensemble; \(D_s\) from gap; closures \(O(m)\) | **Negative for kill** (\(\mathcal R_\star\) falls \(0.11\to 0.031\); not \(m^{1/2}\)) |
| **9B** Exact-shell + closing → \(K_{\alpha,\beta}\) | Structured next family (\(v_\varepsilon=w_\alpha+\varepsilon z_\beta\)) | Protocol / quantity lock — still structured next family |
| **9C** Designed \(\Theta(m^2)\)-closure subset | Remaining packet falsifier | **LIVE** falsification lane (below) |

Kill lane remains **LIVE** (falsification **and** proof). R_★ amplitude/dilation invariant. NS not solved. No SFE.

---

## Remaining packet falsifier — Attack 9C

**Name (locked):** **Attack 9C — Designed \(\Theta(m^2)\)-closure subset with locked phases**

Natural same-shell / fixed-gap ensembles did **not** kill ★. The remaining structured packet falsifier is a **designed** subset with:

1. **\(\Theta(m^2)\) closures** (not merely \(O(m)\)), and  
2. **Locked phases** (coherent phase design, not a natural ensemble average).

| Outcome (when run) | Meaning |
|--------------------|---------|
| Sustained \(\mathcal R_\star\to\infty\) under exact formula | Falsification lane advancing (★ dead if true) |
| Flat / decaying / \(D_s\) wins again | Another negative — kill lane still LIVE |
| Finite 9C samples of any kind | **≠** kill lane closed; **≠** Lemma★ proved |

**Do not** claim ★ proved from 9A / fixed-gap / 9B / 9C negatives.

Code / inventory: `domain_architect/kab_quantity.py` (`ATTACK_9_FIXED_GAP_STATUS`, `ATTACK_9C_STATUS`, `refuse_same_shell_ensemble_kills_star`).

---

## Hard refusals

- Refuse “same-shell ensemble kills ★.”
- Refuse “natural same-shell / fixed-gap closed the kill lane.”
- Refuse “AP packet closed kill lane” (9A).
- Refuse “kill lane closed” from any finite Attack 9 family.
- Refuse greening ★ / “almost proved” / “numerics prove ★.”
- Refuse reviving AP widening as the next clean test.
- Refuse comparing \(0.11\to 0.031\) to unattested legacy R numbers.

---

## Jonathan action

**None.** Encoding lock only. Remaining falsifier = **Attack 9C** (designed \(\Theta(m^2)\)-closure subset, locked phases). Attack 9B \(K_{\alpha,\beta}\) remains the structured exact-shell + closing family.
