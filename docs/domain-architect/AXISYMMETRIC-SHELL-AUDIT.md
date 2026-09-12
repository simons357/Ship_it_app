# Axisymmetric-with-swirl shell estimate — binding audit filter

**Status:** Jonathan Simons locked this audit as the filter for **one**
program on 2026-09-12.  
**Class / quantity / remainder / assumed.** Unaugmented axisymmetric
Navier–Stokes with swirl; the quantity is a dyadic shell block \(Z_j\)
(Door 1 budget); the only remainder after the budget is the intra-shell
transfer \(T_{j\leftarrow j}\); extra hypotheses are written in brackets
in the open. This is **not** a close. Clay is **NOT CLAIMED**. DA-VC-01
stays **FAIL**.

This file is the **binding filter** for the axisymmetric (with swirl)
shell estimate only. It is not a hull \(C_f\) certificate, not the
turbulence-reduction program, not leftover-split strain
\(\int\|u^r/r\|_\infty\,dt\), and not Paper2 T2 / Route J.

Estimate note that must obey this filter:
[`docs/papers/swirl/AXISYMMETRIC-SHELL-ESTIMATE.md`](../papers/swirl/AXISYMMETRIC-SHELL-ESTIMATE.md).

Operator contract: [`DA-MODE.md`](DA-MODE.md).  
Decisions: [`DECISIONS.md`](DECISIONS.md) (2026-09-12 lock).  
OPEN board: [`OPEN-BOARD.md`](OPEN-BOARD.md).  
Leftover-split (different remainder): [`LEFTOVER-REPAIR.md`](LEFTOVER-REPAIR.md).

---

## Standing orders for anything written next

1. First sentence: class, quantity, remainder, what is assumed.
2. Remainder is \(T_{j\leftarrow j}\) (axisymmetric if that is the class).
3. Smallness is a printed ratio or an explicit integral of \(\|\omega\|_\infty\), not a story.
4. No object from the discard list appears in the identity, the Young step, or the claim.
5. If the identity is not closed in the time series, do not quote the sign of \(\Lambda'\).

---

## How to read KEEP / DISCARD / PARK

**KEEP** = may enter the current estimate.

**DISCARD** = must not be used in the estimate, the identity, or the
claim sentence. If a paragraph needs a discard item to move, the
paragraph is **OUT**. Including as “motivation” inside the proof.

**PARK** = may live in another stack, not this one.

---

## KEEP — Method

- Write the exact identity first. Name the one term that can grow the quantity. Never bound that term by a copy of the time derivative you are estimating.
- State extra hypotheses in brackets, in the open, the way [SND] was stated. A conditional theorem is a theorem. A hidden hypothesis is not.
- Prefer a restricted class with real geometry (axisymmetric with swirl) over a modified PDE that is no longer Clay NS.
- Measure before closing: signed triads, cancellation \(C\), \(|T_c|/D_s\), shell block \(T_{j\leftarrow j}/Z_j\), occupancy, alignment \(\alpha\). If a number can come out the other way, it is allowed in.
- Unaugmented normalization. Do not add a field to help the estimate.
- Galerkin / truncation theorems with every constant named, scope in the first sentence.
- Energy conservation of the pairing as a check (\(10^{-16}\) residual). If the stepper and the diagnostic disagree, the identity is not closed.

## KEEP — Objects that earned their place today

- \(\Lambda'=2(T_c-\nu D_s)/X\) as bookkeeping, not as the final left-hand side.
- Closed-triad rewrite \(\tau=(\omega(p)-\omega(r))J_p+(\omega(q)-\omega(r))J_q\).
- Shift by a lattice constant \(\omega_*\), not by \(\Lambda\).
- Door 1: shell budget. The only remainder is \(T_{j\leftarrow j}\).
- Door 3 as a criterion to test: vorticity-direction alignment \(\alpha\), kept separate from triad-phase occupancy.
- 2-D fact: adversary \(|T_c|/D_s\sim 0.017\), occupancy \(\sim 0.15\).
- 3-D fact: random-phase ratio still \(O(10^{-2})\), HHH occupancy 1 on the orbits that were run, \(\alpha\approx 0.5\).
- Swirl geometry as the class that removes free helical HHH.

## KEEP — Habits

- Send work with the gap visible.
- Refuse “visibility of cancellation = uniform smallness.”
- Separate modified equations from classical NS.

---

## DISCARD — do not use in this program

- SFE, coherence viscosity, Q1–Q6 as constitutive laws of Clay NS. Those are other PDEs. A close of another PDE is not a close of NS.
- Any bound of the bad term by \(\Lambda'\), \(\dot Z_j\), or a new symbol of the same size.
- [SND] in its large form (“assume the dangerous interactions are not dangerous”) as if it were a smallness you measured.
- GCD spectral attractor, E8 cathedral, prime-harmonic lock, Borromean coherence as mechanisms that force \(T_{j\leftarrow j}\) small.
- Base 44 / gematria / letter-number maps as estimates. They do not bound a flux.
- Q6-Kabbalah, Lightning Flash, syncretic narrative inside the proof. Opinion stack only.
- Importing 2-D \(\rho=0.02\) into 3-D, or occupancy 1 into CFM.
- FFT-aliased orbits used as if \(\dot\Lambda=2(T_c-\nu D_s)\) held.
- “Clay is solved,” “unconditional 3-D regularity,” or any sentence that drops the class and the measured \(\rho_j\).
- Treating a Tao-positive reply as certification of a proof.
- Coherence-floor / extra memory / prime gates added to NS and then described as the Millennium problem.

---

## PARK — other stacks, not this estimate

| Parked object | Where it lives (do not delete; do not revive as this remainder) |
|---|---|
| Harmonic Blueprint / SFE as a standalone field model | [`docs/archive/`](../archive/README.md); [`docs/archive/sfe-hb/`](../archive/sfe-hb/) |
| Apps (Prime Breath, GCD Shells viz, Swirl publishing, FIELD MAPPER) | not lemmas; not this remainder |
| Base 44 as an optional partition experiment | relabel existing triads; keep the label only if \(\rho_j\) drops. Until that test is run, parked. Packet: [`docs/packets/BASE44-RECOVERY-REPORT-FOR-GROK-2026-08-25.md`](../packets/BASE44-RECOVERY-REPORT-FOR-GROK-2026-08-25.md) |
| Defense / TITAN-X / HarborSafe | different problem |
| RH / Goldbach / “Three in One” | different problems. GAP1 Step F stays on the OPEN board as arithmetic, not this flux |
| Turbulence-reduction (ships ACTIVE; aircraft including drones, submarines, hypersonic QUEUED) | [`docs/projects/turbulence-reduction/`](../projects/turbulence-reduction/README.md). Analog 15% intensity is a **separate** lumped setpoint. Do not copy the ship envelope onto this estimate |
| Leftover-split strain \(\int\|u^r/r\|_\infty\,dt\) | [`LEFTOVER-REPAIR.md`](LEFTOVER-REPAIR.md). Same class, **different** remainder. Do not set \(\sigma_{\mathrm{strain}}=T_{j\leftarrow j}\) |
| Ring SND / Paper2 simplex / Route J / T2 Gronwall | [`docs/papers/ring/`](../papers/ring/README.md), [`docs/papers/ns-snd/`](../papers/ns-snd/). Route J stays separate from SND / GNC / Bridge Triple Lock. `03_t2_shell_flux_gronwall.tex` is **MISSING**; do not invent it |
| Missing bytes (`SND_GNC_BRIDGE_EXTRACTED.txt`, `SYNTHESIS-AXISYMMETRIC-SND-BRIDGE.md`, July 23 claim ledger, `Paper2_NS_Regularity_SND_FIXED.tex`) | hunt receipts only. Do not invent a close |

---

## What this filter does not do

- It does not prove classical unaugmented Navier–Stokes.
- It does not award unconditional 3-D regularity.
- It does not treat swirl geometry “removes free helical HHH” as a measured 3-D CFM close. That is a **class** statement.
- It does not overwrite DA-VC-01 as PASS.
- It does not stamp `TRANSFORMABLE` / SPE without a real \(T\).
- It does not rewrite Maersk / ship riblet docs to satisfy this audit.
- It does not import archived SFE / HB into live `domain_architect/*.py`.
