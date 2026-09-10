# Five-lane Lemma★ pack locator

**FOUND: yes.**  
**NS is NOT solved.** Lemma★ remains **OPEN**. Bound on \(C_{\mathrm{geom}}\) / \(\sup\mathcal{R}_\star\) **OPEN**. Kill lane **LIVE**.

---

## Git / PR

| Item | Value |
|------|-------|
| Branch | `cursor/ns-five-lane-lemma-star-1390` |
| Tip commit | `8b6cd097ae5228d4287f166690d79ae49da61347` (CANONICAL alias + locator); SoT `45372d27679d9aea576f5ab6d3792f558ac2766f` |
| Tip subject | Add LEMMA_STAR_CANONICAL alias pointer; refresh locator tip |
| Remote | `origin/cursor/ns-five-lane-lemma-star-1390` |
| GitHub PR | **https://github.com/simons357/Ship_it_app/pull/48** |
| PR title | Five-lane Lemma★ drill: K=0 dead, ★ survives numeric |
| PR state | OPEN (`head` = five-lane branch, `base` = `main`) |
| Cursor agent (this locator run) | https://cursor.com/agents/bc-5228010a-ce68-5643-9d8a-512aaef18c73 |
| Related Cursor agent (PR footer) | https://cursor.com/agents/bc-01a00412-6516-7002-95f2-051faf8ba0eb |

---

## Absolute SoT / code pointers (on disk now)

| Role | Absolute path |
|------|----------------|
| **Canonical defs (Lemma★ shape form)** | `/workspace/docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md` |
| **Canonical filename alias** | `/workspace/docs/math/ns_attacks/LEMMA_STAR_CANONICAL.md` → shape form |
| **Exact triad / spectral formulas** | `/workspace/docs/math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md` |
| **Status board** | `/workspace/docs/math/ns_attacks/PROOF_LemmaStar_STATUS.md` |
| **Code lock (moments / \(T_c\) / \(\mathcal R_\star\))** | `/workspace/scripts/ns_attacks/stokes_moments.py` |
| **Attack 3 doc (HH input; not strict HH→L)** | `/workspace/docs/math/ns_attacks/ATTACK_3_BONY_HH_L.md` |
| **Attack 3 script** | `/workspace/scripts/ns_attacks/attack3_bony_hh_l.py` |
| **Near-shell + HH search** | `/workspace/scripts/ns_attacks/lemma_star_near_shell_search.py` |
| **Unit tests** | `/workspace/tests/test_ns_attacks_lemma_star.py` |
| **Five-lane runner** | `/workspace/scripts/ns_attacks/run_all_five.py` |
| **This locator** | `/workspace/docs/math/ns_attacks/FIVE_LANE_PACK_LOCATOR.md` |

All key SoT files under `/workspace/docs/math/ns_attacks/` are present on the five-lane branch tip (no checkout/copy from remote required).

---

## Absolute defs extract (from `LEMMA_STAR_SHAPE_FORM.md` + `stokes_moments.py`)

**Full Lemma★** (absolute SoT — definitions + claim; closing bound **OPEN**; not viscosity-primary; \(K_{\alpha,\beta}\) is **not** this):

\[
A=-P\Delta,\quad B(v,v)=P[(v\cdot\nabla)v],
\]
\[
E=\|v\|_2^2,\quad
X=\|A^{1/2}v\|_2^2,\quad
Y=\|Av\|_2^2,\quad
Z=\|A^{3/2}v\|_2^2,\quad
\Lambda=Y/X,
\]
\[
D_s=Z-Y^2/X=\|(A-\Lambda)A^{1/2}v\|_2^2,\qquad
T_c=-\langle B(v,v),A(A-\Lambda)v\rangle.
\]
Equivalent triad form: \(T_c=M-\Lambda N=\sum_k\lambda_k(\lambda_k-\Lambda)T_k\) — [`LEMMA_STAR_EXACT_FORMULAS.md`](./LEMMA_STAR_EXACT_FORMULAS.md).
\[
\boxed{
\exists\,C_{\mathrm{geom}}<\infty\quad
\forall\,v\in C^\infty_{\mathrm{div},0}(\mathbb{T}^3)\setminus\{0\}:\quad
\bigl(T_c(v)_+\bigr)^2
\le
C_{\mathrm{geom}}\,D_s(v)\,\|v\|_2^2\,Y(v).
}
\]
Equiv. (\(D_s>0\)): \(\sup (T_c)_+^2/(D_s\|v\|_2^2 Y)<\infty\). For \(D_s=0\): one shell and \(T_c=0\) — **vacuous, not a kill**.

**Alias:** \(\mathcal{D}_s\equiv D_s=Z-\Lambda Y\) (same object). Code `Tc = M - Λ N` matches the inner-product \(T_c\).

Centered spectral dissipation (expanded):
\[
D_s=Z-\Lambda Y=Z-Y^2/X
=\sum_k\lambda_k(\lambda_k-\Lambda)^2|v_k|^2.
\]

Nonlinear centered transfer (expanded):
\[
T_c=M-\Lambda N=\sum_k\lambda_k(\lambda_k-\Lambda)T_k.
\]

Sign check / viscosity packaging (\(\theta\), \(\nu\), \(C_0\)):
\[
\Lambda'=\frac{2}{X}\bigl(T_c-\nu D_s\bigr),
\]
\[
T_c\le\theta\nu D_s+C_0(\theta)\nu^{-1}\|u\|_2^2\,Y,\qquad
C_{\mathrm{geom}}=4\theta\,C_0(\theta).
\]

Canonical shape★ quotient:
\[
\mathcal{R}_\star(v)
=\frac{(T_c(v)_+)^2}{D_s(v)\,\|v\|_2^2\,Y(v)}.
\]

Code aliases in `stokes_moments.py`:
- `E` \(=\|v\|_2^2\), `Tc` \(=T_c\), `Ds` \(=D_s\) (alias \(\mathcal{D}_s\))
- **`ratio_R_star_shape`** \(=\mathcal{R}_\star\) (**canonical**)
- `ratio_R_star` — alias → same as `ratio_R_star_shape`
- **`ratio_star`** — **legacy / different**: \(T_c/(E X\Lambda)\) post-Young (scales as \(1/a\)); **not** \(\mathcal R_\star\)

**Near-shell lock:** \(K_{\alpha,\beta}\) is a restricted limiting-family probe only — **not** the full lemma.

## Precision corrections (user-confirmed SoT lock)

1. **Full Lemma★** is the boxed shape inequality / \(\sup\mathcal{R}_\star<\infty\) in `LEMMA_STAR_SHAPE_FORM.md` — **not** \(K_{\alpha,\beta}\). Bound on \(C_{\mathrm{geom}}\) / \(\sup\mathcal{R}_\star\) is **OPEN** (exact reduction + open closing estimate; not a GR proof).
2. **Attack 3 is NOT strictly HH→L.** It filters high-frequency **inputs** (Bony HH/HL/LL) without restricting **output** to low frequencies. Historical “HH→L” naming = HH-channel product gap, not a proved high→low output map. See `ATTACK_3_BONY_HH_L.md`.
3. **Canonical quotient** is `ratio_R_star_shape`. Legacy `ratio_star` means something different (post-Young).
4. **Attack 9C** is **SoT-only until implemented** — snapshot \(0.11\to0.031\) **lacks** supporting fixed-gap sweep script/data in PR #48.
5. **Boxed \(K\)** (restricted near-shell probe only):
   \[
   K_{\alpha,\beta}=\sup_{Aw=\alpha w}\frac{\beta\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\|w\|_2^4}.
   \]
6. **Attack 9B CRITICAL:** reported \(\max K\approx0.641\) at \((\alpha,\beta)=(4,8)\) has \(\beta>\alpha\) → transfer to a **higher** shell — **NOT** HH→L. Genuine HH→L subfamily requires \(\beta<\alpha\) (sample max \(\approx0.0123\) at \((5,2)\)). Always report \(\beta>\alpha\) and \(\beta<\alpha\) maxima separately. Sample \(K\) bound does **not** prove ★.
7. **Triad formulas:** `LEMMA_STAR_EXACT_FORMULAS.md` (\(T_c=M-\Lambda N=\sum\lambda_k(\lambda_k-\Lambda)T_k\)).

### Confirmed originals (PR #48)

- `LEMMA_STAR_SHAPE_FORM.md`, `stokes_moments.py`, `attack3_bony_hh_l.py` from PR48 export
- `ATTACK_9B_EXACT_SHELL_CLOSING.md` is the original (not a Grok reconstruction)

### Export zip

`PR48_five_lane_export.zip` — **not found** under Downloads or `/opt/cursor/artifacts` in this environment. Cursor Origin URL for the pack also **not found**; use GitHub PR URL above.

---

## Attack 3 / HH statement (corrected)

**Target (diagnostic, not a kill criterion alone):** partition the bilinear driving \(T_c\) into Bony channels HH / HL / LL. The **HH input** channel blocks a clean product bound toward

\[
|T_c|\le C\|u\|_2 X^{3/2}
\]

(or the related survivor \(T_c\le\theta\nu\mathcal{D}_s+C_* X^{3/2}\Lambda\)).

**Lock:** Attack 3 is **not** a strict HH→L (high×high → low) map — no low-frequency **output** restriction. Channel splits can **identify** a mechanism; only the **complete signed** \(T_c\) enters the ★ kill criterion. For genuine HH→L as an **output** subfamily in exact-shell closing, use Attack 9B with \(\beta<\alpha\).

The analytic reason that signed triads cannot make \(\mathcal{R}_\star\) arbitrarily large **is NOT written**.

Pointers:
- `/workspace/docs/math/ns_attacks/ATTACK_3_BONY_HH_L.md`
- `/workspace/docs/math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md` (β split)
- `/workspace/docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md`
- `/workspace/docs/math/ns_attacks/PROOF_LemmaStar_STATUS.md`
- `/workspace/scripts/ns_attacks/attack3_bony_hh_l.py`
- Runtime: `/workspace/results/ns_five_lane_2026-09-10/attack3.json`
- 9B β-split notes: `/workspace/results/ns_five_lane_2026-09-10/attack9b_exact_shell/NOTES_BETA_SPLIT.md`

---

## Artifact directories

### Workspace results
- `/workspace/results/ns_five_lane_2026-09-10/` (attacks 1–5 + 9B + HEADLINE + SYNTHESIS)
- `/workspace/results/ns_five_lane_2026-09-10/attack9b_exact_shell/`
- `/workspace/results/ns_five_lane_shape_star/`

### `/opt/cursor/artifacts/`
- `/opt/cursor/artifacts/ns_five_lane_2026-09-10/`
- `/opt/cursor/artifacts/ns_five_lane_shape_star/`
- `/opt/cursor/artifacts/lemma_star_formula_lock/`
- `/opt/cursor/artifacts/attack9_packet_fan/`
- `/opt/cursor/artifacts/attack9b_exact_shell/` (includes `NOTES_BETA_SPLIT.md`, β-split HEADLINE)
- `/opt/cursor/artifacts/NS-BRUTE-FORCE-EXTRACTION-LEDGER.md`
- `/opt/cursor/artifacts/pr48_proposed_body.md`
- `/opt/cursor/artifacts/pr48_update.log`

### Not found / not mounted
- `/Users/jonathansimons/Downloads/` — **not mounted** in this environment
- `PR48_five_lane_export.zip` — **not found** under Downloads or `/opt/cursor/artifacts`
- Cursor Origin URL for five-lane pack — **not found** (use GitHub PR #48)
- `LAST-KEY-LEMMA-STAR*` — **no hits**
- `Hyp-ST*`, `Hyp-Lat*`, `Lat-Emb*` as standalone docs — **no hits** (HH-channel content lives under Attack 3 / Lemma★ SoT above)
- `/home/ubuntu` / `/tmp/cursor` copies of five-lane packs — **no extra copies** beyond workspace + `/opt/cursor/artifacts`

---

## Full inventory (absolute paths)

### Docs — SoT pack (`/workspace/docs/math/ns_attacks/`)
- `/workspace/docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md`
- `/workspace/docs/math/ns_attacks/LEMMA_STAR_CANONICAL.md` (alias → shape form)
- `/workspace/docs/math/ns_attacks/LEMMA_STAR_EXACT_FORMULAS.md`
- `/workspace/docs/math/ns_attacks/PROOF_LemmaStar_STATUS.md`
- `/workspace/docs/math/ns_attacks/ATTACK_SYNTHESIS_SIMULTANEOUS.md`
- `/workspace/docs/math/ns_attacks/ATTACK_1_COVARIANCE.md`
- `/workspace/docs/math/ns_attacks/ATTACK_2_TRIAD_K0_CSTAR.md`
- `/workspace/docs/math/ns_attacks/ATTACK_3_BONY_HH_L.md`
- `/workspace/docs/math/ns_attacks/ATTACK_4_STOKES.md`
- `/workspace/docs/math/ns_attacks/ATTACK_5_ROUTE2.md`
- `/workspace/docs/math/ns_attacks/ATTACK_8_CORRECT_RECORD.md`
- `/workspace/docs/math/ns_attacks/ATTACK_9_PACKET_FAN.md`
- `/workspace/docs/math/ns_attacks/ATTACK_9A_AP_PACKET_FAILURE.md`
- `/workspace/docs/math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md`
- `/workspace/docs/math/ns_attacks/ATTACK_9C_FIXED_GAP_SPHERES.md`
- `/workspace/docs/math/ns_attacks/ATTACK_9D_THETA_M2_LOCKED_PHASE.md`
- `/workspace/docs/math/ns_attacks/DA-SHAPE-TEXTURE-LINK.md`
- `/workspace/docs/math/ns_attacks/ARCHIVE_ROUTE_N_Q6_SHELL/README.md`
- `/workspace/docs/math/ns_attacks/FIVE_LANE_PACK_LOCATOR.md` (this file)

### Related math docs (archive / ledger, not canonical ★)
- `/workspace/docs/math/ARCHIVE_NOT_LEMMA_STAR.md`
- `/workspace/docs/math/NS-BRUTE-FORCE-EXTRACTION-LEDGER.md`
- `/workspace/docs/math/NS-EXTRACTION-LEDGER.md`
- `/workspace/docs/math/CLOSURE-ATTACK-PLAN.md`
- `/workspace/docs/math/COOL-CHECK.md`

### Scripts
- `/workspace/scripts/ns_attacks/stokes_moments.py`
- `/workspace/scripts/ns_attacks/run_all_five.py`
- `/workspace/scripts/ns_attacks/attack1_covariance.py`
- `/workspace/scripts/ns_attacks/attack2_triad_k0_cstar.py`
- `/workspace/scripts/ns_attacks/attack3_bony_hh_l.py`
- `/workspace/scripts/ns_attacks/attack4_stokes.py`
- `/workspace/scripts/ns_attacks/attack5_route2_kill.py`
- `/workspace/scripts/ns_attacks/attack9_packet_fan.py`
- `/workspace/scripts/ns_attacks/attack9b_exact_shell_K.py`
- `/workspace/scripts/ns_attacks/lemma_star_near_shell_search.py`
- `/workspace/scripts/ns_attacks/__init__.py`

### Tests / results
- `/workspace/tests/test_ns_attacks_lemma_star.py`
- `/workspace/results/ns_five_lane_2026-09-10/` (full tree)
- `/workspace/results/ns_five_lane_shape_star/`

### Git refs
- Branch: `cursor/ns-five-lane-lemma-star-1390`
- Remote: `refs/remotes/origin/cursor/ns-five-lane-lemma-star-1390`

---

## ManagePullRequest note

`ManagePullRequest` is **not available** in this agent toolset (read-only `gh` only). PR #48 already exists and is OPEN at the URL above; locator commit should land on the same head branch so the PR picks it up automatically after push.
