# Grok Heavy — Lemma★ / five-lane / same-shell pack

**Read this file first.** Everything else in `docs/ns-recovery/` is indexed from here.

**Date packed:** 10 September 2026  
**This branch:** `cursor/centered-ns-recovery-b5c1` · PR https://github.com/simons357/Ship_it_app/pull/45  
**Live five-lane authoring branch:** `cursor/ns-five-lane-lemma-star-1390` · PR https://github.com/simons357/Ship_it_app/pull/48  
**Authoring agent (not fetchable from this environment):** https://cursor.com/agents/bc-01a00412-6516-7002-95f2-051faf8ba0eb  
**This recovery agent:** https://cursor.com/agents/bc-01a07930-4f88-7811-8d60-3383fff0b5c1

Human: Jonathan Simons (`winchester.anesthesia@gmail.com` / `simonsmedical@icloud.com`), Prime Field Technologies LLC.

---

## Honesty lock (do not weaken)

- **Navier–Stokes is not solved.**
- **Lemma★ is OPEN.** Uniform \(\sup \mathcal R_\star < \infty\) is not proved.
- **Kill lane is LIVE.** Failure to find a numerical counterexample does **not** close falsification.
- Numerics \(\neq\) proof. Do **not** green ★ from bounded samples.
- Do **not** glue SND \(J/X\), Theorem H, Phi-renorm, Triple Lock, Route N / Q6 / LP-shell floors, or Domain Architect “five fingers” into this book.
- Do **not** invent missing formulas. Do **not** abs-value the triad sum.
- Kill / ★ decisions use **complete signed** \(T_c\) only — never an HH→L-only proxy.
- Proving the boxed shape inequality with geometric \(C_{\mathrm{geom}}\) \(\equiv\) Clay B **in this packaging**. That weld is **WITHHELD** until PRODUCT-BLOCK / HH→L closes.

**Two different “fives” (do not mix):**

| Name | What it is |
|---|---|
| **Five lanes** (this pack) | Attacks 1–5 on Lemma★ / Stokes moments / HH→L / kill drill |
| **Five fingers** | Domain Architect role router (`P,H,\psi,\lambda;\Phi`). Organizational software, **not** this math |

---

## What you are being asked to do

Live work, in order:

1. **Attack 9D (retargeted):** growing input **and** output supports, full complex polarizations, frequency factors retained. Uniform 9B target \(\|\Pi_\beta B\|_2\le C\alpha\beta^{-1/2}\|w\|_2^2\). Fixed-output \(\Theta(m^2)\) is **excluded** (\(K\le 16s\)). Spec: `docs/math/ns_attacks/ATTACK_9D_THETA_M2_LOCKED_PHASE.md`. Exclusion: `docs/math/ns_attacks/ATTACK_9B_COUNTING_CS_EXCLUSION.md`.
2. **Lemma★ proof:** write the triadic reason that stretching cannot outrun spectral spread. HH→L is the dangerous channel. That reason is **not written**.
3. **Optional other track:** H1 on the cylinder — **not started**. Do not start it unless the packet line is shelved.

Natural same-shell (9C), AP fan (9A), and finite 9B \(K_{\alpha,\beta}\) samples are **not kills**. Do not re-run them as if they were the remaining job.

---

## Canonical formulas (locked)

Source of lock: `five-lane-pack/docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md`  
Same formulas: `five-lane-pack/docs/ns-review/LEMMA-STAR-EXACT-FORMULAS.md`  
Code: `five-lane-pack/scripts/ns_attacks/stokes_moments.py`

Torus \(\mathbb T^3=(\mathbb R/2\pi\mathbb Z)^3\). Stokes \(A=-P\Delta\), \(\lambda_k=|k|^2\), \((Av)_k=\lambda_k v_k\). Divergence-free, \(v_{-k}=\overline{v_k}\).

\[
\|v\|_2^2=\sum|v_k|^2,\quad
X=\sum\lambda_k|v_k|^2,\quad
Y=\sum\lambda_k^2|v_k|^2,\quad
Z=\sum\lambda_k^3|v_k|^2,\quad
\Lambda=Y/X.
\]

\[
\mathcal D_s=Z-\Lambda Y=Z-Y^2/X=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2\ge0.
\]

Two-shell closed form:
\[
\mathcal D_s=\frac{\alpha\beta(\alpha-\beta)^2\,e_\alpha e_\beta}{\alpha e_\alpha+\beta e_\beta}.
\]

Signed triad (**never** abs-value the sum):

\[
T_k=\sum_{p+q=k}\mathrm{Im}\bigl[(q\cdot v_p)(v_q\cdot\overline{v_k})\bigr],
\quad
N=\sum\lambda_k T_k,\quad
M=\sum\lambda_k^2 T_k,
\]
\[
T_c=M-\Lambda N=\sum_k\lambda_k(\lambda_k-\Lambda)T_k.
\]

Sign check: \(\Lambda'=2(T_c-\nu\mathcal D_s)/X\).

**Lemma★ is a shape statement, not a viscosity statement.** Size \(u=av\) cancels \(\nu\). Canonical quotient:

\[
\mathcal R_\star(v)=\frac{(T_c(v)_+)^2}{\mathcal D_s(v)\,\|v\|_2^2\,Y(v)},
\qquad
T_c_+=\max(T_c,0).
\]

Boxed ★:
\[
\bigl(T_c(v)_+\bigr)^2\le C_{\mathrm{geom}}\,\mathcal D_s(v)\,\|v\|_2^2\,Y(v).
\]

Exact invariance: \(\mathcal R_\star(av)=\mathcal R_\star(v)\) and \(\mathcal R_\star(v(n\cdot))=\mathcal R_\star(v)\). Claims that amplitude or frequency make “the ratio” smaller concern **older budgets**, not \(\mathcal R_\star\).

Derived Young packaging (not primary):
\[
T_c\le\theta\nu\mathcal D_s+C_0\nu^{-1}\|v\|_2^2 Y,
\quad
C_0(\theta)=C_{\mathrm{geom}}/(4\theta).
\]

Energy-budget / DA-NS-1 form (PR #49):
\[
T_c\le\theta\nu(Z-\Lambda Y)+C_0\nu^{-1}\|u\|_2^2 X\Lambda.
\]

PRODUCT-BLOCK still open: need something like \(|T_c|\le C\|u\|_2 X^{3/2}\) (or pre-Young \(|T_c|\le C\|u\|_2 X\Lambda\)). Ordinary 3D product/Agmon from energy **insufficient**. HH→L is the channel that blocks it.

### Ratio hygiene (do not mix)

| Symbol in JSON / old notes | What it actually is |
|---|---|
| `ratio_R_star_shape` | Canonical \(\mathcal R_\star\) (amp-invariant) |
| `ratio_star` in Attacks 1–2 JSON | **Post-Young** \(T_c/(E Y)\) or similar — **falls as \(1/B\)** — **not** \(\mathcal R_\star\) |
| `ratio_preyoung` / \(R_{\mathrm{pre}}\) | \(T_c/(\|v\|_2 X\Lambda)\) |
| `ratio_cstar` / \(C_*\) | \(T_c/(X^{3/2}\Lambda)\) |
| `ratio_k0` | \(T_c/\mathcal D_s\) — blows with amplitude; K=0 **DEAD** |
| Reported \(0.065\), \(0.073\), \(1.93\times10^{-3}\) | **Do not compare** unless each used this exact \(\mathcal R_\star\) |
| 9C \(0.11\to 0.031\) | User-reported on natural same-shell; **not recomputed** in the JSON below |

The shape-star Attack 5 `best_R_star_shape` tag `sep_1_p8` has **\(T_c<0\)** (\(\approx-591\)). Under the locked \((T_c)_+\) form that field has \(\mathcal R_\star=0\). The quoted \(\max\mathcal R_\star\approx0.0227\) used \(T_c^2\), not \((T_c)_+^2\). Compression is **not** a stretching kill.

---

## Five-lane computation (the run you asked for)

**Date:** 10 September 2026 · seed / branch tag `1390`  
**Harness:** `five-lane-pack/scripts/ns_attacks/run_all_five.py`  
**Original artifacts on PR #48:** `results/ns_five_lane_2026-09-10/` and `results/ns_five_lane_shape_star/`  
**Original paths (restored from PR #48 onto this branch):** `results/ns_five_lane_2026-09-10/` and `results/ns_five_lane_shape_star/`  
**Nested copy:** `five-lane-pack/results/`

Headline (`SYNTHESIS_RUNTIME.json`):

```json
{
  "attack1": "SURVIVE_numeric_NOT_proof",
  "attack2": "K0_DEAD_Cstar_SURVIVES_numeric",
  "attack3": "HH_CHANNEL_LIVE_BOTTLENECK_no_closure",
  "attack4": "STOKES_IDENTITIES_OK_absorption_needs_remainder",
  "attack5": "SURVIVE_numeric_gap_remains",
  "LemmaStar_C0_killed": false,
  "ns_solved": false
}
```

| Lane | Script | Verdict | Key numbers (this run) |
|---|---|---|---|
| 1 Covariance | `attack1_covariance.py` | SURVIVE numeric, not proof | Phase diam \(\lvert R_{\mathrm{pre}}\rvert\approx0.155\); post-Young falls with \(B\) |
| 2 Triad / K=0 / \(C_*\) | `attack2_triad_k0_cstar.py` | **K=0 DEAD** | \(\lvert T_c\rvert/\mathcal D_s\sim B\) (\(0.0035\to349\) on triad); \(C_*\approx0.004058\) amp-invariant on that triad |
| 3 Bony HH→L | `attack3_bony_hh_l.py` | HH live bottleneck, **no closure** | Pure high triad: all \(T_c\) in HH; random HH frac p90 \(\approx0.51\) |
| 4 Stokes identities | `attack4_stokes.py` | Identities OK | \(\mathcal D_s\ge0\); viscous-only absorption insufficient |
| 5 Route-2 kill | `attack5_route2_kill.py` | SURVIVE numeric, gap remains | First pass \(n=978\), \(\max\lvert R_{\mathrm{pre}}\rvert\approx5.088\), \(\max\lvert C_*\rvert\approx0.04065\). Shape re-run \(n=1242\), \(\max T_c^2/(D_s E Y)\approx0.0227\) (see hygiene); almost-shell max \(\sim3.6\cdot10^{-6}\); pure-shell kills \(0\) |
| 9A AP packet | `attack9_packet_fan.py` | **Did not kill ★** | \(\gamma\approx-1.39\); \(\mathcal D_s\) grew faster than \(T_c\) |
| 9B exact-shell \(K_{\alpha,\beta}\) | `attack9b_exact_shell_K.py` | Finite sample, **not a kill** | \(\max K\approx0.641\) at \((\alpha,\beta)=(4,8)\); controls PASS |
| 9C fixed-gap spheres | SoT / combinatorial probe | **Did not kill ★** | Closures \(O(m)\) not \(O(m^2)\); reported \(\mathcal R_\star\) \(0.11\to0.031\) |
| 9D \(\Theta(m^2)\) locked phase | **stub** | **LIVE falsifier** | Not implemented |

JSON files (complete run records):

- `five-lane-pack/results/ns_five_lane_2026-09-10/SYNTHESIS_RUNTIME.json`
- `five-lane-pack/results/ns_five_lane_2026-09-10/attack{1,2,3,4,5}.json`
- `five-lane-pack/results/ns_five_lane_2026-09-10/attack9b_exact_shell/attack9b.json`
- `five-lane-pack/results/ns_five_lane_shape_star/attack{1,5}.json`

Reproduce (from pack; does **not** prove ★):

```bash
cd docs/ns-recovery/five-lane-pack
PYTHONPATH=scripts python3 scripts/ns_attacks/run_all_five.py --outdir /tmp/ns_five_lane --serial
PYTHONPATH=scripts python3 -m pytest tests/test_ns_attacks_lemma_star.py -q
```

Same-shell combinatorial probe (this branch, independently checked):

```bash
python3 scripts/same_shell_packet_probe.py
python3 -m pytest tests/test_same_shell_packet.py -q
```

---

## Same-shell packet SoT (locked 10 Sep 2026)

Canonical: [`SOT.md`](SOT.md). Longer notes do not override it.

Packet = full lattice spheres \(S_n\cup S_{n+d}\), **not** an AP. \(\mathcal D_s\) from the **gap** \(d\), not width.

Mixed closures type \((n,n,n+d)\) only **\(O(m)\)**, not \(O(m^2)\):

| \(n\) | \(d\) | keys \(m\) | mixed closures |
|---:|---:|---:|---:|
| 9 | 1 | 54 | **48** |
| 89 | 1 | 264 | **288** |

\(d=2\): zero mixed landings on \(\{9,17,25,41,49,89\}\).  
Natural ensemble is **not a kill**. Remaining packet falsifier = **9D**.

---

## File map

### Start here

| File | Role |
|---|---|
| **This file** | Grok Heavy entry |
| [`SOT.md`](SOT.md) | Packet source of truth |
| [`five-lane-pack/HIT.md`](five-lane-pack/HIT.md) | Pack index / PR pointers |
| [`five-lane-pack/docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md`](five-lane-pack/docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md) | **Canonical exact formulas** |
| [`five-lane-pack/docs/math/ns_attacks/PROOF_LemmaStar_STATUS.md`](five-lane-pack/docs/math/ns_attacks/PROOF_LemmaStar_STATUS.md) | Status board |
| [`five-lane-pack/docs/math/ns_attacks/ATTACK_SYNTHESIS_SIMULTANEOUS.md`](five-lane-pack/docs/math/ns_attacks/ATTACK_SYNTHESIS_SIMULTANEOUS.md) | Lane board |
| [`five-lane-pack/docs/math/ns_attacks/ATTACK_8_CORRECT_RECORD.md`](five-lane-pack/docs/math/ns_attacks/ATTACK_8_CORRECT_RECORD.md) | Kill lane LIVE; ratio invariants |

### Attacks 1–5 + 9

| File | Role |
|---|---|
| `five-lane-pack/docs/math/ns_attacks/ATTACK_1_COVARIANCE.md` | Amplitude / phase survival |
| `five-lane-pack/docs/math/ns_attacks/ATTACK_2_TRIAD_K0_CSTAR.md` | K=0 dead |
| `five-lane-pack/docs/math/ns_attacks/ATTACK_3_BONY_HH_L.md` | HH→L diagnostic |
| `five-lane-pack/docs/math/ns_attacks/ATTACK_4_STOKES.md` | Moment identities |
| `five-lane-pack/docs/math/ns_attacks/ATTACK_5_ROUTE2.md` | Kill drill |
| `five-lane-pack/docs/math/ns_attacks/ATTACK_9A_AP_PACKET_FAILURE.md` | AP fan non-kill |
| `five-lane-pack/docs/math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md` | \(K_{\alpha,\beta}\) |
| `five-lane-pack/docs/math/ns_attacks/ATTACK_9C_FIXED_GAP_SPHERES.md` | Natural ensemble non-kill |
| `five-lane-pack/docs/math/ns_attacks/ATTACK_9D_THETA_M2_LOCKED_PHASE.md` | **Next falsifier (spec)** |
| `five-lane-pack/docs/math/ns_attacks/ATTACK_9_PACKET_FAN.md` | 9A runtime |

### Code + tests + JSON

| Path | Role |
|---|---|
| `five-lane-pack/scripts/ns_attacks/stokes_moments.py` | \(X,Y,Z,\Lambda,T_c,\mathcal D_s,\mathcal R_\star\) |
| `five-lane-pack/scripts/ns_attacks/attack{1,2,3,4,5}_*.py` | Five lanes |
| `five-lane-pack/scripts/ns_attacks/attack9_packet_fan.py` | 9A |
| `five-lane-pack/scripts/ns_attacks/attack9b_exact_shell_K.py` | 9B |
| `five-lane-pack/scripts/ns_attacks/run_all_five.py` | Simultaneous launcher |
| `five-lane-pack/rstar_quantities.py` | DA copy of spectral moments (PR #52) |
| `five-lane-pack/tests/test_ns_attacks_lemma_star.py` | Formula lock tests |
| `scripts/same_shell_packet_probe.py` | Combinatorial 9C keys/closures |
| `tests/test_same_shell_packet.py` | Locks 48 / 288 / \(d=2\) zeros |
| `results/same_shell_packet.json` | Probe dump |

### DA packaging (do not green)

| File | Role |
|---|---|
| `five-lane-pack/docs/ns-review/LEMMA-STAR-DA-NS-1.md` | Energy-budget Clay packaging; PRODUCT-BLOCK open |
| `five-lane-pack/docs/ns-review/LEMMA-STAR-EXACT-FORMULAS.md` | PR #52 Fourier lock |
| `five-lane-pack/docs/math/ns_attacks/DA-SHAPE-TEXTURE-LINK.md` | Shape vs texture |

### Recovery history (do not treat as the live math)

| File | Role |
|---|---|
| [`CENTERED-SPECTRAL-DRIFT-MASTER-REPORT.md`](CENTERED-SPECTRAL-DRIFT-MASTER-REPORT.md) | 7 Sep search; Stokes paste was missing **until** PR #48 |
| [`SAME-SHELL-PACKET-NOTE.md`](SAME-SHELL-PACKET-NOTE.md) | Expanded 9C note |

### Related live PRs (do not merge books)

| PR | Title |
|---|---|
| [#48](https://github.com/simons357/Ship_it_app/pull/48) | Five-lane Lemma★ drill |
| [#49](https://github.com/simons357/Ship_it_app/pull/49) | Lemma★ / DA-NS-1 energy-budget |
| [#50](https://github.com/simons357/Ship_it_app/pull/50) | DA sync to five-lane (HH→L gap) |
| [#51](https://github.com/simons357/Ship_it_app/pull/51) | ★ is \(\mathcal R_\star\) shape statement |
| [#52](https://github.com/simons357/Ship_it_app/pull/52) | Exact Fourier formulas |

**Not found (do not invent):** `Hyp-ST`, `Hyp-Lat`, `Lat-Emb`, `LAST-KEY-LEMMA-STAR`, `NS_H_SND_NoCancellation_Reconstruction`, `centered_spectral_drift_note`.

---

## Kill / survive rules (copy these)

| Outcome | Verdict |
|---|---|
| Some shapes make \(\mathcal R_\star\) arbitrarily large | no finite \(C_{\mathrm{geom}}\) → **★ dead** |
| \(\mathcal D_s=0\) and \(T_c>0\) | **★ dead** on that field |
| Pure single shell, \(T_c=0=\mathcal D_s\) | vacuous — not a kill |
| Bounded samples of \(\mathcal R_\star\) | those shapes did not kill it — **not a proof** |
| 9A AP / 9C natural same-shell | **not kills** |
| 9B finite \(\max K\approx0.641\) | **not a kill**; kill lane still LIVE |
| 9D \(\mathcal R_\star\to\infty\) on designed locked-phase family | **★ dead** |
| 9D bounded/decaying on that family | those shapes did not kill ★ — still not a proof |

**K=0** form \(T_c\le\theta\nu\mathcal D_s\): **DEAD** (Attack 2 amplitude scaling).

---

## What a proof would have to be

Reason from how **signed** triads add that stretching cannot get large unless spectrum also spreads or phases cancel. HH→L is the channel that could refuse that. **That reason is not written.** Until it is mathematics, do not claim global regularity.

**NS not solved.**
