# Official CosmoEvolution 3D sixteen

`python3 scripts/da_machine.py cosmos`

The Cosmo app is live at
[https://cosmoevolution3d.base44.app](https://cosmoevolution3d.base44.app)
(host is **Base44**, not “bass44”). Ingested 2026-09-03 from the
app’s own **Topology vs Gauge** table.

This **replaces the missing-names block**. It does **not** replace
the reconstructed 4×4 in [`DA-SIXTEEN.md`](DA-SIXTEEN.md). Those
are two catalogs. The reconstructed 16th is \(R\). The Cosmo 16th
is \(\sum m_\nu\). Do not glue them.

The app’s UI says gauge predicts 0/16 and DA predicts 16/16.
**That is not a DA pass.** The core equation is private / trade
secret. Sitting at a measured value is not \(F\).

---

## The sixteen (app’s table)

| # | Parameter | Measured | App DA claim | App match |
|---|---|---|---|---|
| 1 | Koide ratio (charged leptons) | 0.666661(7) | exactly \(2/3\) | exact |
| 2 | \(\tau\) mass | 1776.86 MeV | Koide from \(e,\mu\): 1776.97 | exact 0.006% |
| 3 | Fermion generations | 3 | topological invariant | exact |
| 4 | Charge quantization \(\lvert e\rvert=\lvert p\rvert\) | \(1\pm10^{-21}\) | winding conservation | exact |
| 5 | \(\alpha^{-1}\) | 137.036… | “U(1) eigenvalue ≈137” | good 0.03% |
| 6 | \(\sin^2\theta_W\) | 0.23122 | “\(3/8\) at unification → 0.231” | good |
| 7 | \(m_\mu/m_e\) | 206.768 | recursive Koide | good |
| 8 | Higgs VEV \(v\) | 246.22 GeV | “domain ground-state ≈246” | good ~1% |
| 9 | Higgs mass | 125.10 GeV | “first excitation ≈125” | good ~1% |
| 10 | CKM \(\theta_{12}\) | 13.04° | “interface winding ≈13°” | approx ~3% |
| 11 | \(\alpha_s(M_Z)\) | 0.1181 | “SU(3) spectral flow ≈0.118” | approx |
| 12 | \(m_p/m_e\) | 1836.15 | “baryon eigenvalue ≈1836” | approx |
| 13 | \(\Lambda\) | \(1.1\times10^{-52}\,\mathrm{m}^{-2}\) | “domain web tension” | order of magnitude |
| 14 | \(G\) | \(6.674\times10^{-11}\) | “Planck spectral gap” | order of magnitude |
| 15 | \(\ell_P\) | \(1.616\times10^{-35}\,\mathrm{m}\) | “domain foam cell” | order of magnitude |
| 16 | \(\sum m_\nu\) | \(<0.12\,\mathrm{eV}\) | “≈0.06 eV” | predicted, untested |

App disclaimer, in the app: research and educational only; not
established physics.

---

## Same five questions, each slot alone

kind / nature / score / produce / next. **Produce fails for
everyone** because \(F\) is not public.

| # | Kind | Nature leftover? | Produce? | Honest note |
|---|---|---|---|---|
| 1 | 1981 Koide formula | no | **fail** | predates DA; spectral-zeta “has not been completed” (app papers) |
| 2 | same Koide, as \(m_\tau\) | no | **fail** | not a second prediction |
| 3 | SM counting fact | no | **fail** | “topological invariant” is a slogan without \(F\) |
| 4 | already in SM / Dirac | no | **fail** | winding slogan |
| 5 | EM coupling | **yes** | **fail** | sits at 137 |
| 6 | weak mixing | **yes** | **fail** | \(3/8\to0.231\) is standard GUT running; manifold test already failed |
| 7 | same Koide | no | **fail** | do not triple-count |
| 8 | EW scale | **yes** (the scale) | **fail** | sits at 246 |
| 9 | Higgs mass | no | **fail** | sits at 125 |
| 10 | flavor angle | no | **fail** | sits at 13° |
| 11 | strong coupling | **yes** | **fail** | sits at 0.118 |
| 12 | baryon/lepton ratio | no | **fail** | sits at 1836 |
| 13 | vacuum leftover | **yes** | **fail** | order of magnitude |
| 14 | gravity leftover | **yes** | **fail** | order of magnitude |
| 15 | rewrite of \(G\) | no (duplicate) | **fail** | \(\ell_P=\sqrt{\hbar G/c^3}\) |
| 16 | neutrino sum | no | **fail** as \(F\); **open** as a number | only forward claim; cannot check the derivation |

16 UI slots collapse to **13 clusters** (Koide×3, \(G\equiv\ell_P\)).

---

## Honesty already inside the app (use it; do not flatten it)

**Manifold sweep** (key finding 07): 10 standard geometries, **0**
match \(\cos\theta_W\approx0.878\). Highest \(\lambda_1/\lambda_2\)
is Bolza 0.717. Quote from the app: “The DA prediction fails for
every known exact-spectrum topology.” A rectangular torus tuned to
0.882 is a **fit**, not a prediction (the app calls this the
tuning trap).

**Koide** (key finding 01): strongest empirical pattern they
advertise. It is also a 1981 formula. The genus-2 / Bolza story is
not a completed derivation.

**Gauge non-convergence** (key finding 02): SM couplings miss;
MSSM needs undiscovered superpartners. The app treats the miss as
evidence *for* topological unification. Our screen: that is still
only **gauge3**, not **nature4**. SM fail and MSSM-class open as
gauge3 were already on the published-claim list.

**55-parameter split** (key finding 03): 1 gauge, 19 harmonic, 2
anomaly→H, 26 unresolved, 7 both. Counts only. Full names were not
extracted from the minified bundle. Do not invent them.

**Unification verdict** (key finding 06): Scenario B
(topological) “strengthening.” That is the app’s slogan.
Collapse still needs a public \(F\) and \(\chi^2_{\mathrm{ext}}\le\varepsilon^2\).

---

## Screen (same two levels; do not glue)

| Level | Verdict | Why |
|---|---|---|
| gauge3 | **fail** | App does not claim a 3-meet; a miss is not a topology |
| nature4 | **fail** | No public \(F\) to \((g_s,g_w,g_{\mathrm{em}},G_N)\) with \(\Lambda\) in |
| 16/16 UI | **fail** | Private equation, sitting, double-counts, manifold fail |
| collapse | **no** | P3 still fail |

\(G\) and \(\Lambda\) on this table are the **same leftovers**
the reconstructed score already hit. Naming them in Cosmo does
not produce them.

---

## Overlap with the reconstructed 4×4

In both: \(\alpha\), \(\sin^2\theta_W\), \(\alpha_s\), \(v\) as
scale, \(G\)/Planck, \(\Lambda\).

Cosmo only: Koide cluster, generations, charge, \(m_H\),
\(m_p/m_e\), \(\ell_P\), \(\sum m_\nu\).

Reconstruction only: \(\theta_{\mathrm{QCD}}\), \(S_c\), \(\delta\),
oscillators, \(R\).

---

## What this unblocks, and what it does not

Unblocked: the names. X3 is no longer “we do not have the
screen.” The official 16 is this table.

Still blocked: a **public** producing-map from a named topology
to \((g_s,g_w,g_{\mathrm{em}},G_N,\Lambda)\). Until that exists,
Cosmo is a catalog plus slogans plus one untested neutrino
number, and one already-failed manifold test.

Tracks A, B, Q are untouched. SFE / HB stay shelved.
