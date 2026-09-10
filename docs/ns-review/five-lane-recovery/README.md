# Five-lane / Lemma★ recovery inventory

**Date:** 2026-09-10  
**Recovery branch:** `cursor/da-five-lane-recovery-0cc5`  
**Rule:** Truth only. **NS is NOT solved.** Lemma★ is **OPEN**. This pack recovers sources; it does not prove ★.

## Verdict (unblockers)

| Need | Found? | Where |
|------|--------|-------|
| Absolute defs of \(T_c,X,Y,Z,\Lambda,\theta,\nu\) | **YES** | `docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md` (+ code `scripts/ns_attacks/stokes_moments.py`) |
| Exact HH→L map / statement | **PARTIAL — diagnostic statement recovered; no proved map** | `docs/math/ns_attacks/ATTACK_3_BONY_HH_L.md`, `scripts/ns_attacks/attack3_bony_hh_l.py` |
| Whole PR #48 / five-lane folder | **YES** | GitHub PR + branch export below |

Also mirrored under `/opt/cursor/artifacts/five-lane-recovery/`.

---

## PR #48 (canonical five-lane pack)

| Field | Value |
|-------|-------|
| **GitHub** | https://github.com/simons357/Ship_it_app/pull/48 |
| **Title** | Five-lane Lemma★ drill: K=0 dead, ★ survives numeric |
| **State** | OPEN |
| **Head** | `cursor/ns-five-lane-lemma-star-1390` |
| **Base** | `main` |
| **Cursor agent (author)** | https://cursor.com/agents/bc-6378e748-26ec-5035-bfac-1ef1b5071390 (“Five-lane NS drill”) |
| **Related agents** | https://cursor.com/agents/bc-62c77e5e-d650-5242-9b79-9978ad920060 (Lock Lemma★ shape form); https://cursor.com/agents/bc-cd9306da-3fa3-5fce-a57a-d0e6613c31f8 (Attack 9 packet fan) |
| **Cursor Origin `codebase/.../pull/48` URL** | **NOT FOUND** in repo, transcripts, artifacts, or agent metadata (searched). Closest Cursor links are agent URLs above and a stale PR-footer agent `bc-01a00412-6516-7002-95f2-051faf8ba0eb` (Tao SND-H panel, not five-lane). |

Metadata dump: `/opt/cursor/artifacts/five-lane-recovery/pr48-meta.json`  
Full file list from branch: `/opt/cursor/artifacts/five-lane-recovery/pr48-files-list.txt`

### Original PR summary body (from agent transcript)

Simultaneous five-lane drill on Lemma★ / centered spectral drift \(T_c\).

- **K=0 dead** — amplitude scaling blows \(T_c/\mathcal{D}_s\)
- **Lemma★ survives numeric kill** — no blowing family for \(C_0\) ratio; not a proof
- Bony HH→L still the analytic bottleneck
- Survivor form: \(T_c \le \theta\nu(Z-\Lambda Y)+C_* X^{3/2}\Lambda\)

---

## Absolute definitions (five-lane pack)

Source of truth: recovered copy at  
`docs/ns-review/five-lane-recovery/docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md`  
(live on branch `origin/cursor/ns-five-lane-lemma-star-1390`).

On \(\mathbb{T}^3\), Stokes \(A=-P\Delta\), \(\lambda_k=|k|^2\):

\[
\|v\|_2^2=\sum|v_k|^2,\quad
X=\|A^{1/2}v\|_2^2=\sum\lambda_k|v_k|^2,\quad
Y=\|Av\|_2^2=\sum\lambda_k^2|v_k|^2,\quad
Z=\|A^{3/2}v\|_2^2=\sum\lambda_k^3|v_k|^2,
\]
\[
\Lambda=Y/X.
\]

Centered dissipation:
\[
\mathcal{D}_s=Z-\Lambda Y=Z-Y^2/X=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2.
\]

Nonlinear transfer / centered stretch:
\[
N=-\langle B,Av\rangle,\quad M=-\langle AB,Av\rangle,\quad
T_c=M-\Lambda N=\sum_k\lambda_k(\lambda_k-\Lambda)T_k.
\]

Sign check: \(\Lambda'=2/X\,(T_c-\nu\mathcal{D}_s)\).

Canonical shape★:
\[
\mathcal{R}_\star=\frac{(T_c)_+^2}{\mathcal{D}_s\,\|v\|_2^2\,Y}.
\]

Viscosity packaging (derived):
\[
T_c\le\theta\nu\mathcal{D}_s+C_0\nu^{-1}\|v\|_2^2\,Y
=\theta\nu\mathcal{D}_s+C_0\nu^{-1}\|v\|_2^2\,X\Lambda,
\]
with \(C_0(\theta)=C_{\mathrm{geom}}/(4\theta)\). Here \(\theta\in(0,1)\) is the Young absorption fraction; \(\nu\) is viscosity.

Code aliases: `E`, `Tc`, `Ds`, `Lambda`, **`ratio_R_star_shape`** (canonical \(\mathcal{R}_\star\); alias `ratio_R_star`). Legacy **`ratio_star`** is different — do not compare. Bookkeeping: [`../FIVE-LANE-BOOKKEEPING.md`](../FIVE-LANE-BOOKKEEPING.md).

---

## HH→L statement (recovered) — not strictly HH→L

From `ATTACK_3_BONY_HH_L.md` (precision-updated):

> Partition the bilinear form driving \(\mathfrak T_c\) into parent-wavevector channels HH / HL / LL (Bony-style). Prior analytic note: **HH→L is the channel that blocks a clean product bound toward**
> \[
> |\mathfrak T_c|\le C\|u\|_2 X^{3/2}.
> \]

**Precision:** Attack 3 filters high-frequency **inputs**; it does **not** restrict output to low → **not strictly HH→L**.

Live 2026-09-10 result: HH is the sole channel on a pure high triad; random HH frac p90 \(\approx0.51\). **No closure.** Diagnostic only — kill decisions use **complete signed** \(T_c\), not HH→L-only.

**Honest gap:** There is **no proved analytic HH→L → L map** in the pack. What exists is (1) the bottleneck statement above, (2) the Galerkin channel splitter `attack3_bony_hh_l.py`, (3) synthesis notes that HH→L remains the PRODUCT-BLOCK gap.

**9B note:** runtime \(\max K\approx0.641\) at \((\alpha,\beta)=(4,8)\) has \(\beta>\alpha\) → **not** HH→L (higher-shell transfer).

---

## Exported tree (this recovery)

Under `docs/ns-review/five-lane-recovery/`:

| Path | Role |
|------|------|
| `docs/math/ns_attacks/*` | Attack 1–5, 8, 9A–9D, synthesis, Lemma★ shape lock, status |
| `docs/math/ARCHIVE_NOT_LEMMA_STAR.md` | Archive separation |
| `scripts/ns_attacks/*` | Galerkin probes + `run_all_five.py` + `stokes_moments.py` |
| `tests/test_ns_attacks_lemma_star.py` | Formula / identity tests |
| `results/ns_five_lane_2026-09-10/` | HEADLINE + attack JSON/PNG + 9B |
| `results/ns_five_lane_shape_star/` | Shape★ SUMMARY + logs |
| `EXTRACTS-DEFS-AND-HH-TO-L.md` | Short paste of defs + HH→L |
| `HITS.md` | Every search hit (paths/URLs) |

---

## Related Git hits (not the five-lane Galerkin pack itself)

| Hit | Path / URL |
|-----|------------|
| DA sync to PR #48 | branch `cursor/da-lemma-star-five-lane-0cc5` → PR https://github.com/simons357/Ship_it_app/pull/50 |
| Lemma★ DA-NS-1 packaging | `cursor/da-lemma-star-0cc5` → PR #49 |
| Exact \(R_\star\) formulas in DA | `cursor/da-rstar-exact-formulas-0cc5` → PR #52 |
| Shape statement in DA | `cursor/da-rstar-shape-0cc5` → PR #51 |
| Workspace docs (current tips) | `docs/ns-review/LEMMA-STAR-*.md`, `domain_architect/lemma_star.py` |
| Artifacts already on disk | `/opt/cursor/artifacts/da-lemma-star*`, `lemma-star-*.log`, `ns_five_lane_*` (when present) |
| Centered-drift **absence** report | `docs/ns-recovery/CENTERED-SPECTRAL-DRIFT-MASTER-REPORT.md` on PR #48 (older “lost in transit” note; **superseded for defs** by `LEMMA_STAR_SHAPE_FORM.md`) |

---

## Search misses (honest)

| Target | Result |
|--------|--------|
| `Hyp-ST`, `Hyp-Lat`, `Lat-Emb` | **Not found** anywhere searched |
| `LAST-KEY-LEMMA-STAR` | **Not found** |
| `/Users/jonathansimons/...` mounts | **Not present** on this VM |
| `/home/ubuntu/Downloads`, `Desktop` | **Empty / absent** |
| `/opt/cursor/logs` five-lane logs | **Empty directory** |
| `https://cursor.com/codebase/.../pull/48` Origin URL | **Not found** |

---

## Jonathan action

1. Open **https://github.com/simons357/Ship_it_app/pull/48** (or checkout `cursor/ns-five-lane-lemma-star-1390`) — this is the live five-lane pack.  
2. For absolute defs / HH→L bottleneck, start at `docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md` and `ATTACK_3_BONY_HH_L.md` (also copied here).  
3. If you still need a Cursor **Origin** `codebase/.../pull/48` link: it was not recoverable from agents/transcripts; use agent https://cursor.com/agents/bc-6378e748-26ec-5035-bfac-1ef1b5071390 or ask Cursor UI “Open in Cursor” from PR #48.  
4. Do **not** treat numeric survive as proof. Kill lane LIVE. **NS not solved.**
