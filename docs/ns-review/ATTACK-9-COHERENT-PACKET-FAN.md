# Attack 9 — Coherent Packet / Fan Test

**Date:** 2026-09-10  
**Name (locked):** **Attack 9 — Coherent Packet/Fan Test**  
**Depends on:** exact \(\mathcal R_\star\) ([`LEMMA-STAR-EXACT-FORMULAS.md`](./LEMMA-STAR-EXACT-FORMULAS.md)), Attack 8 record ([`ATTACK-8-RECORD.md`](./ATTACK-8-RECORD.md))  
**Status:** **Attack 9A (AP packet) recorded — negative for kill.** Attack **9C** fixed-gap spheres / natural same-shell = **not a kill** ([`ATTACK-9C-FIXED-GAP-SPHERES.md`](./ATTACK-9C-FIXED-GAP-SPHERES.md)). Attack **9B** finite sample max K≈0.641 = **not a kill** ([`ATTACK-9B-EXACT-SHELL-CLOSING.md`](./ATTACK-9B-EXACT-SHELL-CLOSING.md)). Remaining falsifier = **9D** Θ(m²) ([`ATTACK-9D-THETA-M2-LOCKED-PHASE.md`](./ATTACK-9D-THETA-M2-LOCKED-PHASE.md)). Kill lane still **LIVE**. **NS NOT SOLVED.** No SFE. No “almost proved.”

---

## Attack 9A (AP packet) — result lock

**Verdict:** Attack 9A = **negative for kill** (does **not** kill Lemma★; also **not** a proof of ★).

| Observation | Lock |
|-------------|------|
| AP packet effect on \(T_c\) | Increased \(T_c\) |
| Spectral variance / \(D_s\) | Widening the packet increased \(D_s\) **faster** than \(T_c\) growth helped the quotient |
| Earlier assumption | \(D_s\|v\|_2^2 Y = O(1)\) in packet size was **FALSE** for that AP family |
| Kill decision | **Did not kill ★** |
| Proof claim | **None** — finite negative kill attempt ≠ uniform bound |

**Hard refusal:** Refuse “AP packet closed kill lane.” Failure of 9A does **not** close falsification or proof. Kill lane remains **LIVE** (both directions).

---

## Objective (family protocol)

Maximize the **complete** shape quotient
\[
\mathcal R_\star(v)=\frac{\bigl(T_c(v)_+\bigr)^2}{D_s(v)\,\|v\|_2^2\,Y(v)}
\]
over conjugate-closed Fourier packets \(P,Q,R\) with
\[
R=P+Q,
\]
while controlling packet geometry (cardinality, shell thickness) and optimizing **all** amplitudes, phases, and divergence-free polarizations.

---

## Setup (historical 9A AP packet)

1. Choose conjugate-closed mode packets \(P,Q,R\subset\mathbb Z^3\setminus\{0\}\) with \(R=P+Q\) (triad support).
2. Build a divergence-free field \(v_m\) supported on those packets (cardinality parameter \(m\)).
3. Optimize amplitudes, phases, and polarizations (\(k\cdot v_k=0\), \(v_{-k}=\overline{v_k}\)).
4. Evaluate **complete** signed \(T_c\) (never abs; never HH→L-only proxy for the kill decision).
5. Form exact \(\mathcal R_\star(v_m)\) and record against \(m\).

Stub (controls + refusals only): `scripts/attack9_packet_fan_stub.py` (if present).

**9A lesson:** Widening an arithmetic-progression (AP) packet is the wrong geometry for a kill attempt when \(D_s\) tracks spectral variance faster than \(T_c\) accumulates.

---

## Required controls

| Control | Requirement |
|---------|-------------|
| Amplitude invariance | \(\mathcal R_\star(av)=\mathcal R_\star(v)\) |
| Uniform Fourier dilation | \(\mathcal R_\star(v(n\cdot))=\mathcal R_\star(v)\) |
| Triad cancellation identity | \(\sum_k \mathscr T_k = 0\) |
| Evaluation agreement | Direct triad summation **agrees** with dealiased FFT evaluation |
| Complete \(T_c\) | Report **total** \(T_c\), not only the favorable HH→L portion |
| Growth fit | Fit \(\mathcal R_\star(v_m)\) against packet size \(m\) (9A); for 9B use \(K_{\alpha,\beta}\) |

DA helpers: `domain_architect/rstar_quantities.py` (`check_rstar_invariances`, `warn_rstar_comparison_without_attestation`); Attack 9B: `domain_architect/kab_quantity.py`.

---

## Decisive output (9A framing)

Fit
\[
\mathcal R_\star(v_m)\sim m^\gamma.
\]

| Outcome | Decision |
|---------|----------|
| Sustained \(\gamma>0\) | **Counterexample route** (falsification lane advancing) |
| Flat / decaying / \(D_s\) wins (9A) | **Not a kill** — reposition family geometry |

**9A realized outcome:** \(D_s\) grew faster → **negative for kill**. Neither outcome proves Lemma★. Kill lane stays **LIVE** until either a true \(\mathcal R_\star\to\infty\) family or a uniform bound is established.

---

## Fixed-gap spheres — natural same-shell = not a kill

**USER LOCK-IN:** Fixed-gap spheres \(n\) and \(n+d\): \(D_s\) from the **gap** (not width); closures only \(O(m)\); \(\mathcal R_\star\) **falls** with \(n\) (**\(0.11\to 0.031\)**, exact quotient attested for this family) and does **not** track \(m^{1/2}\).

**Verdict:** **Natural same-shell ensemble is not a kill.**

Full lock: [`ATTACK-9-FIXED-GAP-SPHERES.md`](./ATTACK-9-FIXED-GAP-SPHERES.md).

---

## Next structured family — Attack 9B (exact-shell + closing packet)

**Do not** run another widening AP packet. **Do not** claim natural same-shell kills ★.

Name: **Attack 9B — Exact-shell + closing packet.** Full lock:  
[`ATTACK-9B-EXACT-SHELL-CLOSING.md`](./ATTACK-9B-EXACT-SHELL-CLOSING.md).

Family:
\[
v_\varepsilon = w_\alpha + \varepsilon z_\beta,\qquad A w_\alpha=\alpha w_\alpha,\quad A z_\beta=\beta z_\beta,
\]
with
\[
z_\beta \parallel \Pi_\beta B(w_\alpha,w_\alpha).
\]

Relevant quantity:
\[
\boxed{
K_{\alpha,\beta}
=
\sup_{A w=\alpha w}
\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}
}
\]

- Base packet: many **same-shell** modes  
- \(D_s\) generated only by the small closing component  
- \(\varepsilon\)-dependence cancels in the limiting quotient  

### Caveat (important)

A merely “narrow” packet does **not** automatically keep \(D_s=O(1)\). On the lattice, small eigenvalue differences are amplified by
\[
D_s=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2.
\]

**Next clean test order:**

1. **Exact-shell coherent fan** / \(K_{\alpha,\beta}\) (9B)
2. Then **controlled finite shell thickness**
3. **Attack 9C** — designed \(\Theta(m^2)\)-closure subset with locked phases ([`ATTACK-9-FIXED-GAP-SPHERES.md`](./ATTACK-9-FIXED-GAP-SPHERES.md))
4. **NOT** another widening AP packet

---

## Remaining packet falsifier — Attack 9C

Natural same-shell / fixed-gap did **not** kill ★. Remaining falsifier:

**Attack 9C — Designed \(\Theta(m^2)\)-closure subset with locked phases.**

Kill lane stays **LIVE** via that designed-closure route (and via proof). See fixed-gap doc.

---

## Hard refusals

- Refuse “kill lane closed” from finite Attack 9 / 9A / fixed-gap / 9B / 9C samples.
- Refuse “AP packet closed kill lane” (9A negative ≠ lane closed).
- Refuse “same-shell ensemble kills ★” (fixed-gap / natural same-shell = not a kill).
- Refuse greening Lemma★ / “almost proved” / “numerics prove ★” from any finite \(m\) sweep.
- Refuse comparing Attack 9 \(\mathcal R_\star\) values to unattested legacy numbers (\(0.065\), \(0.073\), \(1.93\times10^{-3}\)).
- Refuse claiming ★ from LP-shell / Route N / Q6 / \(M=256\) side material ([`LEMMA-STAR-SIDE-ARCHIVE.md`](./LEMMA-STAR-SIDE-ARCHIVE.md)).

---

## Jonathan action

**None.** Encoding lock only. Fixed-gap / natural same-shell = not a kill. Remaining falsifier = **Attack 9C** (designed \(\Theta(m^2)\)-closure, locked phases). 9B \(K_{\alpha,\beta}\) remains structured next family — not another AP widen.
