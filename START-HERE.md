# START HERE — ChatGPT audit package for the unaugmented Navier–Stokes pathway

This folder is a **review packet**, not a new proof and not a merge of later work into the research.

**Ordinary 3D Navier–Stokes is not claimed solved. Clay Statement B is not claimed.**

Read this page first. Then read the original files. Do not treat this guide as a substitute for those files.

---

## 0. What this package is

| Item | Value |
|---|---|
| Repository | `https://github.com/simons357/Ship_it_app` |
| Primary research snapshot | branch `cursor/unaugmented-r4-vorticity-f80e` |
| Snapshot commit | `a5a97019eb6b890607538ea43496a1abf7551948` (2026-09-24) |
| Packaging branch | `cursor/ns-audit-package-ac6d` |
| Existing research PR | https://github.com/simons357/Ship_it_app/pull/24 |
| Packaging rule | Original research paths and contents are unchanged. This guide, the manifest, and `_chatgpt_audit/` are packaging only. |

The live tree at the root **is** the 24 Sep unaugmented snapshot: documents, mathematical scripts, tests, data, results, and unchanged supporting files.

Later Ring/SND papers and later honesty cards that were **not** on that snapshot are filed under `_chatgpt_audit/source-snapshots/<branch>/…` with **their original paths preserved under that prefix**. They are not copied over the snapshot.

Hashes: `AUDIT-MANIFEST.sha256`. Provenance: `_chatgpt_audit/SOURCE-MAP.md` and `AUDIT-PROVENANCE.json`.

Download: `NS-Audit-Package.zip` (single archive, 11.65 MB; no split). Same file is attached as a walkthrough artifact.

If ZIP download fails, use the numbered plain-text dumps (each under 5 MB):

- `_chatgpt_audit/plain-text/NS-Audit-Text-01.txt` — START-HERE, centered, energy/K, remainder, Ring/SND, unaugmented chain, and their scripts/tests/results
- `_chatgpt_audit/plain-text/NS-Audit-Text-02.txt` — remaining original text files
- `_chatgpt_audit/plain-text/NS-Audit-Text-BINARIES.txt` — PDF/image/binary index only


## Unsiloed ChatGPT feed (use this, not the 4.5 MB dump)

The 4.5 MB `NS-Audit-Text-01.txt` still mixes the pathway with hundreds of supporting files. That is the silo problem.

Give ChatGPT this short linear pack instead:

- `_chatgpt_audit/plain-text/CHATGPT-WHAT-YOU-HAVE.txt` — inventory: what exists vs what to read (~244 KB argument)
- `_chatgpt_audit/plain-text/CHATGPT-PATHWAY-INDEX.txt`
- `_chatgpt_audit/plain-text/CHATGPT-PATHWAY-A.txt` — locks, centered, energy/K, CS remainder
- `_chatgpt_audit/plain-text/CHATGPT-PATHWAY-B.txt` — Ring / SND
- `_chatgpt_audit/plain-text/CHATGPT-PATHWAY-C.txt` — unaugmented chain + honesty cards

Those five files are the argument plus the inventory. The big dumps are the archive. Do not start a review from `NS-Audit-Text-01.txt`.



---

## 1. Classical NSE versus any augmented model

Keep these as **different PDEs**. Do not weld them.

### Classical / unaugmented (this review)

\[
\partial_t u+(u\cdot\nabla)u=-\nabla p+\nu\Delta u,\qquad \nabla\cdot u=0
\]

on \(\mathbb{T}^3\) or \(\mathbb{R}^3\). Only viscosity \(\nu\Delta u\). No extra field, no force, no \(Q\)-operator, no \(K(t)\) inserted into the PDE.

Primary faces:

- `docs/UNAUGMENTED-NS-CHAIN.md`
- `docs/UNAUGMENTED-R4-VORTICITY-PLAN.md` (keep the axis weight \(1/r^4\); do not cancel it as the main path)
- `docs/NS-PROOF-CHAIN.md`

### Augmented / other PDE (out of scope for a classical close)

Track A is \(Q_1\)-augmented NS, \(\varepsilon>0\). That is **Theorem A / another equation**.

- `docs/AUGMENTED-NS-PROOF-CHAIN.md`
- `docs/A-CHAIN.md`
- `docs/A-PROOF-CHAIN.md`
- `scripts/augmented_ns_verify.py`

**YES as Theorem A. NO as ordinary NS.** See `docs/YES-NO-OPEN.md`.

### Φ-renorm / swirl algebra (identity, not a close)

The identity \(\frac{1}{r^4}\partial_z(\Gamma^2)=\partial_z(\Phi^2)\) is algebra. It does not remove work; it moves the estimate onto \(\|\Phi\|_\infty\). The unaugmented plan **keeps** \(1/r^4\).

Original swirl papers (labeled snapshot, not on the r4 root):

- `_chatgpt_audit/source-snapshots/ns-learning-pack-9d6b/docs/papers/` is for Ring/SND. Swirl Φ-renorm faces on later mainline notes are not this close.

---

## 2. Read this order (priority arguments)

Do not start leftover H1 from these pages. Do not restore unrestricted Lemma★. Do not treat numerics as a theorem.

### A. Status locks (read before any estimate)

1. `docs/YES-NO-OPEN.md` — binding tape: YES / NO / OPEN. Wins if a later sentence contradicts it.
2. `docs/ISSUES-SHEET.md` — named leftovers for collaborators.
3. `docs/LATEST.md` — desk pointer.
4. `docs/ESTIMATE-AUDIT.md` — filter for what may be used as an estimate.
5. `docs/LEMMA-STAR-CORRECTIONS.md` — corrections to ★ packaging.

### B. Centered argument

| File | Role |
|---|---|
| `docs/CENTERED-LEDGER.md` | Incoming ledger, scored 24 Sep. §1 identities sit. DA-NS-2 is a target, not a theorem. |
| `docs/CENTERED-DRIFT.md` | Target: frequency / spectral-center drift. |
| `docs/RESET.md` | Chart reset of frozen variance \(W_K\). Remainder does not jump. |
| `docs/WIDTH.md` | Relative width. \(r\sim\kappa^{-1}\) is not a payment. |
| `docs/SBP.md` | SBP / \(\Phi_e\). |
| `docs/PRESS.md` | Lemma A sits; Lemma B OPEN. |
| `docs/SIGN-GATE.md`, `docs/SIGN-RUN.md` | First-variation sign gate. Persistence OPEN. |
| `docs/FOURIER-TRIANGLE.md`, `docs/TRIANGLE-LIFT.md` | Triangle geometry for \(T_c\). |
| `docs/DA-NS-2.md` | Y-cousin / barycenter sibling. Not this close. |
| `scripts/centered_ledger.py`, `scripts/centered_drift.py`, `scripts/centered_barycenter.py` | Machines. |
| `tests/test_centered_ledger.py`, `tests/test_centered_barycenter.py` | Locks. |
| `results/centered_ledger.json` | Printed score. |

Later centered recovery (labeled; do not overwrite the snapshot):

- `_chatgpt_audit/source-snapshots/centered-ns-recovery-b5c1/docs/ns-recovery/`
- `_chatgpt_audit/source-snapshots/centered-master-ledger-62ec/docs/CENTERED-MASTER-LEDGER.md`

### C. Energy / \(K\) estimates

| File | Role |
|---|---|
| `docs/ENERGY-K.md` | Energy-class remainder ladder. Only \(K\sim\sqrt{E}\) and \(K_Y\sim\sqrt{E}\) are amplitude-legal. Both die on \(v_n\). |
| `scripts/energy_k.py` | Closed forms and amplitude doors. Writes `results/energy_k.json`. |
| `tests/test_energy_k.py` | Arithmetic + status-string locks. |
| `results/energy_k.json` | Recorded run. |
| `docs/L-DOOR.md`, `docs/MN-CANCEL.md`, `docs/PATHWISE.md`, `docs/INTERVAL.md` | Adjacent doors. Instantaneous \(M-\Lambda N\) cancel dies (\(N=0\) on \(v_n\)). |

Claimed on this face: homogeneity is exact; unique amplitude-legal power is \(p=1/2\); the three energy-class doors die on the growing-layer family. **Not a close. Catalog B open stays 1.**

### D. Remainder estimates

| File | Role |
|---|---|
| `docs/CS-REMAINDER.md` | Localized ABC evaluator. Not a proof. Largest printed FFT \(\mathcal R_\star(-v)=0.327\) at \(\lambda=8\) is **not** a kill. |
| `docs/ns-recovery/CS-REMAINDER-VS-DA-REJECT.md` | Comparison / reject notes. |
| `scripts/ns_attacks/cs_remainder_bump.py` | FFT / bump evaluator. |
| `scripts/ns_attacks/cs_remainder_exact_check.py` | Exact-core jobs (\(\lambda=2,3,4\) only). |
| `tests/test_cs_remainder_bump.py` | Locks. |
| `results/cs_remainder_bump/` | Printed tables. |

Principal named remainders on the unaugmented chain:

- Same-scale transfer \(T_{j\leftarrow j}\) — OPEN.
- \(A_{\mathrm{bad}}\) / H1 (Lemma I on the ball) — written, not a theorem.
- H2 (annulus flux) a priori from energy — OPEN.
- H3 (exterior Biot–Savart) a priori from energy — OPEN.
- G4 / useful \(K\) after energy-class death — OPEN.

### E. Ring Lemma / SND and dependencies

**Name hygiene (do not call both SND):**

- **Concentration.** \(J/X\ge c_*\). Dominant shell. Ring-Lemma regime.
- **Spread.** \(\max_j X_j/X\le\rho_0<1\). Viscosity / T2 regime.

| File | Role |
|---|---|
| `docs/SND-TO-REGULARITY.md` | Implication is **not** a bound on \(X\). Theorem G dead. Ring is REPAIR. Displayed Theorem H not established even with \(X\le M\). |
| `docs/SND-H-PLAIN.md` | Closing SND does not close NS. |
| `docs/SND-H-REVIEW.md` | Specialist H review: viscous tail, shear kill, valid \(F_j\). |
| `docs/SND-H-REPAIR.md` | Repaired \(F_j\) is a Dini ceiling, not a floor. Theorem H withdrawn. |
| `docs/SND-INSTRUMENT.md` | SND is an instrument, not a closer. |
| `docs/UNAUGMENTED-R4-VORTICITY-PLAN.md` §§8–10 | Dictionary for Ring / T2 / occupation. |
| `docs/C10-CHAIN.md` | Named local-block candidate beside leftover 5. Failed arrow recorded. |
| `docs/TRACK-B-BONY-T.md`, `docs/TRACK-B-CLIMB-LAW.md` | Bony \(T\) and climb-from-the-field. |
| `scripts/snd_h_review.py`, `scripts/snd_h_repair.py`, `scripts/snd_instrument.py` | Machines. |
| `tests/test_snd_to_regularity.py`, `tests/test_snd_h_review.py`, `tests/test_snd_h_repair.py` | Locks. |

Original Ring Lemma and Paper2 SND manuscripts (not rewritten; not on the r4 root):

- `_chatgpt_audit/source-snapshots/ns-learning-pack-9d6b/docs/papers/ring/RingLemma_Simons_June19_2026.tex`
- `_chatgpt_audit/source-snapshots/ns-learning-pack-9d6b/docs/papers/ring/RingLemma_Final.tex`
- `_chatgpt_audit/source-snapshots/ns-learning-pack-9d6b/docs/papers/ring/02_ring_lemma_snd_conditional.pdf`
- `_chatgpt_audit/source-snapshots/ns-learning-pack-9d6b/docs/papers/ring/README.md`
- `_chatgpt_audit/source-snapshots/ns-learning-pack-9d6b/docs/papers/ns-snd/NS_UNAUGMENTED_PROOF_CHAIN.md`
- `_chatgpt_audit/source-snapshots/ns-learning-pack-9d6b/docs/papers/ns-snd/README.md`
- `_chatgpt_audit/source-snapshots/ns-learning-pack-9d6b/docs/papers/ns-snd/FACES.md`
- `_chatgpt_audit/source-snapshots/ns-learning-pack-9d6b/docs/papers/ns-snd/NS_PAPER2_CONDITIONAL_AUDIT_AUG1_2026.md`

Later honesty cards (spectral-shift identity ≠ Lemma★ bound):

- `_chatgpt_audit/source-snapshots/unaug-proof-chain-honesty-6df4/docs/ns-review/UNAUG-PROOF-CHAIN.md`
- `_chatgpt_audit/source-snapshots/unaug-generic-3d-chain-4e04/docs/ns-review/UNAUG-GENERIC-3D-PROOF-CHAIN.md`

Paper2 PDFs are **not** compiles of the TeX in the same folder. Diff them via `FACES.md`. GNC / Goldbach / Bridge glue is retired.

---

## 3. Claimed results versus known gaps

### Sitting (do not take back) — classical bookkeeping / criteria / identities

From `docs/YES-NO-OPEN.md` and the unaugmented chain:

- Energy identity / Leray class while smooth.
- Local existence (Fujita–Kato). Continuation is the question.
- Serrin / LPS and ESS as **criteria**, not a priori bounds.
- Enstrophy identity \(\tfrac12\dot E+\nu\|D^2u\|_2^2=S_{\mathrm{tot}}\). Cubic Young bound does **not** give \(\int E^2\).
- Lemma C (CF / BdVB): good-pair **if**. Not an H.
- Local enstrophy identity on a cylinder. Does not bound \(A_{\mathrm{bad}}\).
- Far-shell Young on the axisymmetric shell budget. Remainder \(T_{j\leftarrow j}\) still OPEN.
- Spectral-shift / barycenter identity \(\Lambda'=2(T_c-\nu D_s)/X\) as **bookkeeping**. Not a bound on \(T_c\).
- Two-shell product identity for \(T_c\). \(\alpha+\beta=\Lambda\) is empty on two positive shells.
- Frozen variance \(W_K=\mathcal D_s+X(\Lambda-K)^2\) exact and nonnegative.
- Growing-layer family \(v_n\) admissible; unrestricted \(\sup\mathcal R_\star<\infty\) **killed**.
- Energy-class \(K\sim\sqrt{E}\) / \(K_Y\sim\sqrt{E}\) / mid door **dead** on \(v_n\).
- Theorem A sits for the **augmented** PDE only.

### Corrections already locked (do not revive)

- Occupation-decays detector: **withdrawn**.
- Designed Attack 9D as a live closer: **NO**.
- Finite samples \(0.327\), \(0.641\), \(0.610\), grow-\(s\) \(0.456\), three-shear \(2/3\): **samples**, not a kill and not \(16/9\).
- Ring “sits”: **NO**. Direction bound is REPAIR.
- SND sitting \(\Rightarrow\) bound on \(X\): **NO**. Theorem G dead. Displayed Theorem H withdrawn.
- Unrestricted Lemma★ bound: **killed** by \(v_n\). Not a singular NSE solution. Replacement closure OPEN.
- Φ-cancel / \(Q_1\) / \(K(t)\) in the PDE: **not** the unaugmented path.
- Spectral-shift identity \(\Rightarrow\) Lemma★ ratio bound: **false**.
- \(\rho_j<\nu\) as shell-energy absorption into \(\nu Z_j\): **false**. That comparison lives in (A).
- Restricted-disk numerics \(\Rightarrow\) depletion / \(K_{\max}\to\infty\): **false**.
- `tests/test_lemma_star_statement.py` still looks for the old banner `**OPEN. Not a proof. NS not solved.**` in `docs/LEMMA-STAR-STATEMENT.md`. The page already records that the unrestricted box is **killed** by \(v_n\) and that only the replacement closure is OPEN. That mismatch is pre-existing on the snapshot. Do not “repair” either file for this package.

### Still OPEN on the unaugmented face

- Global regularity of classical 3D NSE.
- \(T_{j\leftarrow j}\) (principal same-scale remainder).
- H1 / \(A_{\mathrm{bad}}\) as a theorem (leftover 1).
- H2-from-energy and H3-from-energy.
- Useful remainder \(K\) after energy-class death (G4).
- Lemma B (press). Sign-gate persistence.
- DA-NS-2 / JGC epoch budget / SAG seating.
- Dynamic SND for general Leray–Hopf data.
- PRODUCT-BLOCK \(\sup_v\mathcal R_\star(v)<\infty\) as a replacement (old unrestricted form is dead).
- Axisymmetric-with-swirl global regularity; \(\|u^r/r\|_\infty\) barrier if anyone returns to Φ-renorm.

---

## 4. How to reproduce calculations

Python 3. The snapshot `requirements.txt` is:

```
numpy>=1.24
pandas>=2.0
```

Some later extras use only the standard library. Install once:

```bash
python3 -m pip install -r requirements.txt
```

### Priority locks (run these first)

```bash
python3 -m unittest \
  tests.test_energy_k \
  tests.test_centered_ledger \
  tests.test_centered_barycenter \
  tests.test_cs_remainder_bump \
  tests.test_snd_to_regularity \
  tests.test_snd_h_review \
  tests.test_snd_h_repair \
  tests.test_ns_lemma_star_core \
  tests.test_lemma_star_corrections \
  tests.test_lemma_star_statement \
  tests.test_track_b_lemmas \
  tests.test_track_b_bony_t \
  tests.test_track_b_climb_law
```

### Regenerating printed JSON (does not rewrite the markdown)

```bash
python3 scripts/energy_k.py
python3 scripts/centered_ledger.py
python3 scripts/centered_barycenter.py
python3 scripts/centered_drift.py
python3 scripts/snd_h_review.py
python3 scripts/snd_h_repair.py
python3 scripts/snd_instrument.py
python3 scripts/ns_attacks/cs_remainder_exact_check.py
```

Compare new JSON to the committed files under `results/`. A changed number is a measurement, not a theorem.

### Broader Track B / five-lane machines

```bash
python3 -m unittest tests.test_attack9b_exact_shell tests.test_attack9b_grow_s tests.test_attack9d_two_thirds
python3 scripts/ns_attacks/run_all_five.py
```

Five-lane printed record: `results/ns_five_lane_2026-09-10/`.

### What not to run as a closer

- `scripts/augmented_ns_verify.py` is Track A (other PDE).
- `hb_ringdown_test.py` is the closed HB Experiment 01 null. Do not retune `nodes.json`.
- Domain Architect `scripts/da_*.py` routers are honesty / classification machines, not NS estimates.
- Do not treat occupancy \(\approx 1\) or alignment \(\approx 1/2\) as depletion.

### Later extras (optional; separate trees)

```bash
# These tests expect their own snapshot layout. Run from the labeled snapshot
# only if you copy that subtree to a working root. Do not overlay onto this root.
```

---

## 5. File map

| Path | What it is |
|---|---|
| `docs/` | Working notes. Priority pages listed above. |
| `docs/math/ns_attacks/` | Canonical ★ formulas and older-attempt archive. |
| `docs/five-lane-export/` | Exported five-lane pack. |
| `scripts/`, `scripts/ns_attacks/` | Mathematical scripts. |
| `tests/` | Unit / lock tests (many assert phrases in the markdown). |
| `results/` | Committed numerical output. |
| `data/qnm_events.csv` | HB ringdown table only (supporting; not NS). |
| `jonathan-handoff/` | Duplicate five-lane handoff copy. |
| `apps/`, `assets/`, `tex/` | Unchanged supporting files. |
| `_chatgpt_audit/` | Packaging only: labeled snapshots from other branches. |

Excluded from this ZIP: `.git/`, credentials, `.env*`, virtualenvs, `node_modules/`, `__pycache__/`, build caches.

---

## 6. Reviewer instructions

1. Treat this as an **open proof chain**, not a submitted close.
2. Quote the original file when judging a claim. If this guide and a lock page disagree, the lock page wins (`docs/YES-NO-OPEN.md` first).
3. Separate: (i) exact identities, (ii) numerical samples, (iii) proposed closures.
4. If a step uses \(Q_1\), \(\Phi\)-cancel as the main path, \(K(t)\) in the PDE, GNC/Goldbach/Bridge, or SFE/HB, mark it **out of the classical face**.
5. Do not “repair” Theorem H, unrestricted ★, or SND\(\Rightarrow X\) in this packet. Those are recorded deaths.
6. The leftover to name, if you find one, is a **useful remainder** or a gap in a named OPEN row — not a new Clay claim.

---

## 7. One-line status

**Unaugmented 3D NSE: OPEN. Energy-class \(K\) dead on \(v_n\). Unrestricted ★ killed. Ring/SND do not bound \(X\). Centered identities sit; DA-NS-2 and \(T_{j\leftarrow j}\) remain. Augmented Track A is a different PDE.**
