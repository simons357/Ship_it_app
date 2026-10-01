# \(\alpha_+\) depletion ⇒ (A) — C10 through the C6 hinge

**Date:** 2026-10-01  
**Branch:** `cursor/alpha-plus-depletion-0cc5` (from `cursor/tj-candidates-9083` / [PR #102](https://github.com/simons357/Ship_it_app/pull/102))  
**Face:** unaugmented shell budget; axisymmetric-with-swirl where labeled.  
**Honesty lock:** [`UNAUG-PROOF-CHAIN.md`](./UNAUG-PROOF-CHAIN.md) · candidates [`TJ-SAME-SCALE-CANDIDATES.md`](./TJ-SAME-SCALE-CANDIDATES.md) §5–§6.  
**Probe:** `python3 scripts/ns_attacks/alpha_plus_depletion_probes.py`

**Claim line:** NS / Clay B **not** solved. Absolute unaugmented \(\alpha_+\) control **OPEN / not seated**. Best seated material is **CONDITIONAL**.

**Do not revive:** C1–C5; Sobolev \(\alpha_+ Z\) vs \(P_j\) (\(\sim\lambda^{1/2}\)); CZ/Biot–Savart *pointwise* \(|\alpha|\lesssim|\omega|\); Φ-as-depletion; BKM \(\|\omega\|_\infty\) shortcut; naive energy-only HH \(\sim\lambda^{3/2}\).

**Forbidden in bounds:** \(\dot e_j\), \(\dot Z\), \(\dot Z_j\), \(\Lambda'\).

---

## 0. Target

**(A)** on the shell face (\(D_j=\|\nabla\Delta_j\omega\|_2^2\), \(0<\theta<1\)):

\[
(T_{j\leftarrow j})_+
\le
\theta\nu D_j
+
R_{\mathrm{allowed}},
\]

with \(R_{\mathrm{allowed}}\) from energy \(\mathcal{E}\), shell enstrophies \(\{Z_k\}\), maybe a direction factor — **not** time derivatives of the budget.

**C10 through C6:** control \((\alpha_{\mathrm{loc},j})_+\) (or an integrable substitute) so the main stretch enters that RHS, without Bernstein cubic wall and without BKM-as-shortcut.

---

## 1. What already sits (proved / EXACT / STANDARD)

Seated on the TJJ / AXISYM face (sources: `docs/TJJ-ESTIMATE.md`, `docs/AXISYM-SHELL.md` on `cursor/tjj-estimate-chain-e5c5`; recorded on PR #102).

| Tag | Statement | Status |
| --- | --- | --- |
| **TJJ-Trans** | \(\int(u_{\mathrm{loc}}\cdot\nabla)\Delta_j\omega\cdot\Delta_j\omega=0\) | **EXACT** |
| **TJJ-α** | main stretch \(=\int\alpha_{\mathrm{loc},j}\,\lvert\Delta_j\omega\rvert^2\) | **EXACT** |
| **one-sided** | \(\int\alpha\,\lvert\omega_j\rvert^2\le\|(\alpha)_+\|_\infty Z_j\) | **EXACT** (not a bound on \(\alpha_+\)) |
| **TJJ-template** | \(T_{j\leftarrow j}\le\varepsilon\nu D_j+\|a_+\|_\infty Z_j+C_\varepsilon\nu^{-1}\|u_{\mathrm{loc}}\|_\infty^2 Z_j+C\|\nabla u_{\mathrm{loc}}\|_\infty\sum_{\lvert k-j\rvert\le 1}Z_k\) | **STANDARD**; last two remainders **not** allowed \(R\) |
| **TJJ-E-false** | energy-linear \(R\) dies on \(u^\lambda\) (\(\sim\lambda^{1/2}\)) | **EXACT kill** |
| **AS-ρ** | \(\int\rho_j^{\mathrm{rate}}<\infty\) ⇒ \(Z_j\) finite *(axisym-conditional packaging)* | **CONDITIONAL** (rate \(\neq\) (A)) |

**Lemma α-hinge (EXACT).**  
\[
(T_{j\leftarrow j})_+
\le
\int(\alpha_{\mathrm{loc},j})_+\,\lvert\Delta_j\omega\rvert^2
+
\lvert T_{j\leftarrow j}^{\mathrm{comm}}\rvert.
\]
So depletion of the positive stretch is necessary for (A) on the main piece; commutators are a separate remainder.

**Lemma C10-implication (EXACT, tautological).**  
If
\[
\int(\alpha_{\mathrm{loc},j})_+\,\lvert\Delta_j\omega\rvert^2
+
\lvert T_{j\leftarrow j}^{\mathrm{comm}}\rvert
\le
\theta\nu D_j+R_{\mathrm{allowed}},
\]
then (A) holds. Filling the hypothesis is the whole problem.

---

## 2. Attacks this pass (geometric / conditional / integrable substitute)

### 2.1 CZ–Sobolev integrable substitute (no \(\|a_+\|_\infty\))

**Lemma α-CZ (STANDARD sketch; 3D).**  
Calderón–Zygmund: \(\|S(u)\|_{L^p}\lesssim_p\|\omega\|_{L^p}\) for \(1<p<\infty\). Hence
\[
\int(\alpha)_+\,\lvert\omega\rvert^2
\le
\|S\|_{L^3}\,\|\omega\|_{L^3}^2
\lesssim
\|\omega\|_{L^3}^3.
\]
Gagliardo–Nirenberg / Sobolev (\(\dot H^{1/2}\hookrightarrow L^3\)):
\[
\|\omega\|_{L^3}
\lesssim
\|\omega\|_2^{1/2}\|\nabla\omega\|_2^{1/2}
=
Z^{1/4}D^{1/4},
\]
so
\[
\int(\alpha)_+\,\lvert\omega\rvert^2
\lesssim
Z^{3/4}D^{3/4}.
\]
Young (\(p=4/3,q=4\)):
\[
Z^{3/4}D^{3/4}
\le
\varepsilon D+C_\varepsilon Z^3.
\]

**What this achieves.** Avoids \(\|(\alpha)_+\|_\infty\) and the Bernstein-on-\(u\) route for the *main stretch*. This is a genuine integrable substitute for Door-3’s \(L^\infty\) print.

**What it does not achieve.** Remainder \(C_\varepsilon Z^3\) is the classical enstrophy cubic wall. It is **not** an allowed \(R\) that closes (A) globally (Gronwall can blow). On concentration \(u^\lambda\),
\[
\frac{Z^{3/4}D^{3/4}}{\nu D}\sim\lambda^{1/2}\to\infty
\]
— same escape rate as Sobolev \(\alpha Z/(\nu P)\). **Killed as absolute unaugmented close.** Survives only as a conditional smallness / local-time criterion (not claimed as new).

Shell-localized form (same powers on \(Z_j,D_j\)) inherits the same \(\lambda^{1/2}\) ledger.

### 2.2 Conditional packaging \([\alpha_\theta]\) — Door-3 as a theorem hypothesis

**Hypothesis \([\alpha_\theta]\) (explicit).**  
There exist \(\theta\in(0,1)\) and an allowed remainder \(R\) such that for a.e. \(t\in[0,T]\),
\[
\int(\alpha_{\mathrm{loc},j})_+(t)\,\lvert\Delta_j\omega(t)\rvert^2
\le
\theta\nu D_j(t)+R\bigl(\mathcal{E}(t),\{Z_k(t)\},\mathrm{direction}\bigr).
\]

**Theorem α-cond (CONDITIONAL; stretch piece).**  
Under \([\alpha_\theta]\), the main-stretch contribution enters the RHS of (A).  
**Still open under \([\alpha_\theta]\):** placing \(T^{\mathrm{comm}}\) into allowed \(R\) without Bernstein cubic / \(\|u_{\mathrm{loc}}\|_\infty\).

**Label:** this is the honest C6 hinge. It is **not** an unaugmented absolute bound. Publishing \([\alpha_\theta]\) as a criterion is allowed; selling it as depletion proved from NS dynamics is **refuse**.

**BKM-adjacent twin (do not smuggle).**  
\(\int_0^T\|(\alpha_{\mathrm{loc},j})_+\|_\infty\,dt<\infty\) plus \(\int_0^T\|\nabla u_{\mathrm{loc}}\|_\infty\,dt<\infty\) makes the *template* Gronwall-finite. That twin is regularity-adjacent (controls a piece of \(\|\nabla u\|_\infty\)). **Refused** as a shortcut that “weakens” BKM; record only as named conditional.

### 2.3 Geometric direction hypothesis \([G_\delta]\) (Constantin–Fefferman style)

**Hypothesis \([G_\delta]\).**  
On the set where \(\lvert\omega\rvert\) is large, the direction \(\xi=\omega/\lvert\omega\rvert\) is Lipschitz with small constant \(\delta\) (or the CF geometric condition: vortex lines nearly aligned so stretching is depleted). Classically, such hypotheses yield bounds of the schematic form
\[
\int(\alpha)_+\,\lvert\omega\rvert^2
\le
C\delta\,\|\omega\|_\infty Z
\quad\text{or a depleted Young form.}
\]

**Status here:** **ABSENT as a seated theorem on this face.** No CF depletion is proved in-repo for the shell local block.  
**Conditional packaging only:** if a geometric theorem supplying
\[
\int(\alpha_{\mathrm{loc},j})_+\,\lvert\omega_j\rvert^2
\le
\theta\nu D_j+R_{\mathrm{allowed}}
\]
were imported and line-matched, it would fill \([\alpha_\theta]\). That import is **not done** in this note. Do not claim CF ⇒ (A) for unaugmented NS from this page.

### 2.4 Axisymmetric \(\alpha\) split *(axisym-conditional)*

On the axisymmetric-with-swirl class, write \(u=u_{\mathrm{mer}}+u_{\mathrm{swirl}}\) and
\[
\alpha_{\mathrm{loc},j}
=
\xi_j\cdot S(u_{\mathrm{loc}})\,\xi_j
=
\alpha^{\mathrm{mm}}+\alpha^{\mathrm{ss}}+\alpha^{\mathrm{cross}}
\]
by bilinearity of \(S\) (identity-level; same spirit as TJJ-AS-split for \(T\)).

| Claim | Verdict |
| --- | --- |
| Pure swirl \(\Rightarrow T_{j\leftarrow j}=0\) (hence stretch vanishes) | **EXACT** (TJJ-pure); subclass only |
| \(\alpha^{\mathrm{ss}}\) controlled by Φ-renorm / \(1/r^4\) rewrite | **FAIL as depletion** — Φ is algebra on the swirl *source* pairing, not a bound on \(\alpha_+\) or \(T^{\mathrm{mm}}\) |
| Meridional \(\alpha^{\mathrm{mm}}\) free by 2D regularity | **FALSE** on mixed fields (meridional piece of a mixed field is not a no-swirl solution) |
| SO(2) ⇒ \(\alpha_+\) small | **FALSE** as class bound; restriction on triads ≠ stretch depletion |

**Axisym-conditional remainder:** fill \([\alpha_\theta]\) for mixed swirl+meridional, or bound \(T^{\mathrm{mm}}\) geometrically (C11). Neither is seated.

---

## 3. Already-dead shortcuts (not revived)

| Shortcut | Status |
| --- | --- |
| \(\alpha_+ Z\le\theta\nu P_j+C\mathcal{E}Z\) (Sobolev, no geometry) | **KILLED** (\(\sim\lambda^{1/2}\)) |
| Pointwise CZ \(\lvert\alpha\rvert\lesssim\lvert\omega\rvert\Rightarrow L^\infty\) from \(L^2\) | **KILLED** |
| Φ-renorm ⇒ depletion ⇒ (A) | **KILLED** as standalone |
| BKM \(\|\omega\|_\infty\) ⇒ (A) free | **REFUSED** (stronger / circular for this chain) |
| Occupancy / alignment samples | **REFUSED** |
| \(\dot e_j/\dot Z/\Lambda'\) | **REFUSED** |
| CZ–Sobolev \(Z^{3/4}D^{3/4}\) as absolute (A) | **KILLED this pass** (cubic wall + \(\lambda^{1/2}\)) |

---

## 4. Light probes (ledger only; ≠ theorems)

Command: `python3 scripts/ns_attacks/alpha_plus_depletion_probes.py`  
Artifacts: `/opt/cursor/artifacts/alpha-plus-depletion/` · `results/alpha-plus-depletion/`

| Probe | Outcome | Implication |
| --- | --- | --- |
| Concentration \(\alpha Z/(\nu P)\sim\lambda^{1/2}\) | growth \(16\) over \(\lambda=4\to1024\) | absolute Sobolev still dead |
| CZ substitute \(Z^{3/4}D^{3/4}/(\nu D)\sim\lambda^{1/2}\) | same growth \(16\) | integrable substitute ≠ absolute (A) |
| Cubic Young remainder \(Z^3/D\sim\lambda^{2}\) | \(\to\infty\) | cubic wall live |
| Axisym-compatible concentration (same powers) | identical ledger | axisym does not repair scaling |
| Forbidden-slot checklist | all refused | C3 lock intact |
| Conditional \([\alpha_\theta]\) draft | packages; does not prove hyp. | **CONDITIONAL** seated as packaging only |

---

## 5. Scoreboard — proved vs open

| Item | Status |
| --- | --- |
| TJJ-Trans / TJJ-α / one-sided / template identities | **PROVED** (seated) |
| C10-implication (hyp ⇒ (A)) | **PROVED** (tautology) |
| Lemma α-CZ (integrable substitute → \(\varepsilon D+C_\varepsilon Z^3\)) | **STANDARD sketch seated**; **not** a close |
| Absolute \(\|(\alpha_{\mathrm{loc},j})_+\|_\infty\) from energy/\(\{Z_k\}\)/\(P_j\) | **OPEN / false on concentration** |
| Absolute CZ substitute ⇒ (A) with allowed \(R\) | **KILLED** (cubic + \(\lambda^{1/2}\)) |
| Geometric CF depletion on the shell block | **OPEN / ABSENT** in-repo |
| Hypothesis \([\alpha_\theta]\) ⇒ stretch enters (A) | **CONDITIONAL PROVED** (packaging) |
| Dynamics ⇒ \([\alpha_\theta]\) | **OPEN / EMPTY** |
| Commutators into \(R_{\mathrm{allowed}}\) | **OPEN** (Bernstein wall) |
| Axisym mixed \(\alpha^{\mathrm{mm}}\) / \(T^{\mathrm{mm}}\) | **OPEN** *(axisym-conditional)* |
| \(T_{j\leftarrow j}\) controlled; NS / Clay B | **OPEN**; **not claimed** |

---

## 6. Blunt verdict

**OPEN** (absolute unaugmented).  
**CONDITIONAL** best statement:

> Under the explicit hypothesis \([\alpha_\theta]\) (positive local stretch dominated by \(\theta\nu D_j+R_{\mathrm{allowed}}\)), the main-stretch piece of \(T_{j\leftarrow j}\) enters (A). The CZ integrable substitute replaces \(\|a_+\|_\infty\) by \(\varepsilon D+C_\varepsilon Z^3\) but hits the classical cubic wall and the same \(\lambda^{1/2}\) concentration escape — so it does **not** close unaugmented (A). Geometric CF-style depletion and axisym mixed-\(\alpha\) control remain **unproved**. Commutators remain open.

**C10 through C6:** hinge clarified; absolute door still empty. No Clay claim.
