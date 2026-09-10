# Attack 9C — Fixed-gap spheres \(n\) and \(n+d\) (natural same-shell ensemble)

**Date:** 2026-09-10  
**Name (locked):** **Attack 9C — Fixed-gap spheres**  
**Prior:** Attack 9B (exact-shell \(K_{\alpha,\beta}\)) — finite sample \(\max K\approx0.641\), not a kill — [`ATTACK-9B-EXACT-SHELL-CLOSING.md`](./ATTACK-9B-EXACT-SHELL-CLOSING.md)  
**Also prior:** Attack 9A (AP packet) = **negative for kill** — [`ATTACK-9-COHERENT-PACKET-FAN.md`](./ATTACK-9-COHERENT-PACKET-FAN.md)  
**Depends on:** exact \(\mathcal R_\star\) ([`LEMMA-STAR-EXACT-FORMULAS.md`](./LEMMA-STAR-EXACT-FORMULAS.md))  
**Status:** **USER LOCK-IN — negative for kill** (natural same-shell ensemble). Kill lane still **LIVE**. **NS NOT SOLVED.** No SFE. No “almost proved.” ★ **not** proved.  
**Canonical five-lane twin:** [`../math/ns_attacks/ATTACK_9C_FIXED_GAP_SPHERES.md`](../math/ns_attacks/ATTACK_9C_FIXED_GAP_SPHERES.md)  
**Legacy alias:** [`ATTACK-9-FIXED-GAP-SPHERES.md`](./ATTACK-9-FIXED-GAP-SPHERES.md) (same SoT; kept for old links)

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

## SoT Attack 9 order

| Family | Role | Status |
|--------|------|--------|
| **9A** AP coherent packet/fan | Widening AP packet | **Negative for kill** (\(D_s\) grew faster) |
| **9B** Exact-shell + closing → \(K_{\alpha,\beta}\) | Structured exact-shell family | **LIVE**; finite sample \(\max K\approx0.641\) **not** a kill |
| **9C** Fixed-gap spheres (this doc) | Natural same-shell; \(D_s\) from gap; closures \(O(m)\) | **Negative for kill** (\(\mathcal R_\star\) falls \(0.11\to 0.031\); not \(m^{1/2}\)) |
| **9D** Designed \(\Theta(m^2)\)-closure subset | Remaining packet falsifier | **LIVE** falsification lane — [`ATTACK-9D-THETA-M2-LOCKED-PHASE.md`](./ATTACK-9D-THETA-M2-LOCKED-PHASE.md) |

**Rename note:** Earlier DA docs called \(\Theta(m^2)\) “9C” — **renamed to 9D**. This fixed-gap family is **Attack 9C** in user SoT.

Kill lane remains **LIVE**. R_★ amplitude/dilation invariant. NS not solved. No SFE.

---

## Probe / script status

**SoT-only until implemented.** No dedicated probe script yet under `scripts/ns_attacks/` for fixed-gap spheres (contrast `attack9b_exact_shell_K.py` for 9B). Numbers \(0.11\to 0.031\) are locked as user/runtime truth into this Source of Truth.

---

## Hard refusals

- Refuse “same-shell ensemble kills ★.”
- Refuse “natural same-shell / fixed-gap closed the kill lane.”
- Refuse “AP packet closed kill lane” (9A).
- Refuse “9B killed ★.”
- Refuse “kill lane closed” from any finite Attack 9 family.
- Refuse greening ★ / “almost proved” / “numerics prove ★.”
- Refuse reviving AP widening as the next clean test.
- Refuse comparing \(0.11\to 0.031\) to unattested legacy R numbers.

---

## Jonathan action

**None.** Encoding lock only. Remaining falsifier = **Attack 9D** (designed \(\Theta(m^2)\)-closure subset, locked phases).

**NS NOT SOLVED.**
