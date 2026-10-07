# Priority 2 — Exact-family signed efficiency (numerical)

**Date:** 7 October 2026  
**Evidence label:** **NUMERICAL** finite search — not a proof.  
**Script:** `scripts/ns_attacks/signed_efficiency_probe.py`  
**Output:** `scripts/ns_attacks/SIGNED-EFFICIENCY-PROBE.json`

---

## Question

On the exact 32-shape family (unit dilations of the listed
\((5,b,25)\) and \((9,b,25)\) shapes), how large can the
**signed** combined transfer be relative to (i) the absolute
shape-sum and (ii) a proposed weighted-budget proxy built from
\(\rho+3\rho'\), under reality + divergence-free constraints?

Handoff next step: optimize signed transfer vs proposed budget with
one consistent real DF Fourier field; label finite searches numerical.

---

## Experimental design

### Exact family (not the compact toy)

Shapes at dilation \(n=1\):

- 17 shapes \((5,b,25)\) for the listed original thirds;
- 15 shapes \((9,b,25)\) for the active added thirds.

### Two probes (both numerical)

1. **Shell-phase coherent search.** One shared phase per shell
   label; trigonometric proxy
   \(T_\sigma=\cos(\phi_a+\phi_b+\phi_c)\) on the exact 32 triples.
   Measures whether common signs among nonzero contributions can
   force ratio \(R=|\sum T|/\sum|T|\) to 1 on the *true* shape list
   (not a synthetic 32).

2. **Representative-triad DF field.** For each shape, take the first
   lattice witness triad \((p,q,r)\) with
   \(|p|^2=a\), \(|q|^2=b\), \(|r|^2=c\). Build a real,
   divergence-free Fourier field on the union of those modes
   (Hermitian reality; \(k\cdot\hat u_k=0\)). Coordinate-ascent on
   phases (and a short polarization sweep) maximizing
   \(|\sum_\sigma T_\sigma|\) with the same polarized transfer
   functional used in `phase_cancellation_probe.py`.

### Proposed-budget proxy (numerical face, not the paper’s full high-pass)

With field energy \(E=\sum|\hat u_k|^2\) and dissipation proxy
\(Y=\sum |k|^2|\hat u_k|^2\),

\[
B_{\mathrm{proxy}} := (\rho+3\rho')\,\sqrt{E}\,Y,
\qquad
\eta_{\mathrm{eff}} := \frac{|\sum T_\sigma|}{B_{\mathrm{proxy}}}.
\]

Also report the absolute-efficiency
\(|\sum T|/\sum|T|\) (phase-coherence ratio).

**Caveat:** \(B_{\mathrm{proxy}}\) is a dimensional proxy using the
filed weighted face; it is **not** a re-derivation of the paper’s
time-integrated high-pass inequality. Crossing \(\eta_{\mathrm{eff}}>1\)
would be a numerical stress test of the proxy, not a disproof of the
restricted-family theorem.

---

## Why not a full-lattice 550-mode search

Active shells of the unit-dilation 32-family carry ~1100 lattice
points (~550 Hermitian mode pairs). Full \(T_{abc}\) over all
mode triples is too heavy for this turn’s finite search budget.
Representative triads + shell-phase probes are the feasible
exact-list tests; results are labeled accordingly.

---

## Non-claims

- Does not prove a signed multi-shape lemma.
- Does not establish criterion (17).
- Does not close swirl.
- Does not certify optimality of \(\rho+3\rho'\).

---

## Results (**Rerun here**, 7 Oct 2026)

Artifact log: `/opt/cursor/artifacts/signed_efficiency_probe.log`  
JSON: `scripts/ns_attacks/SIGNED-EFFICIENCY-PROBE.json`

| Probe | Headline |
|---|---|
| Shell-phase on exact 32 triples | Worst-case coherence ratio **1.0** (all 32 contributions same sign) |
| Shell-phase random baseline | mean ≈ 0.19–0.30 regime (see JSON) |
| Representative-triad DF search | Coherence ratio **1.0**; \(\eta_{\mathrm{eff}}\approx 0.039\) vs \(B_{\mathrm{proxy}}=(\rho+3\rho')\sqrt{E}\,Y\) |
| Representative DF random baseline | \(\eta_{\mathrm{eff}}\) mean ≈ 0.003, max ≈ 0.013; coherence mean ≈ 0.19 |

**Reading (numerical only):**

- On the exact 32-list, common-sign assembly is attainable (ratio 1),
  matching the narrowed phase conclusion: \(R=1\) ≠ geometric-bound
  saturation.
- Against the proxy budget with \(\rho+3\rho'\), the representative-triad
  DF search stayed an order of magnitude below 1
  (\(\eta_{\mathrm{eff}}\approx 0.039\)). This does **not** prove the
  paper high-pass inequality; it only shows that this finite search
  did not stress the proxy face.
- Optimistic random-phase cancellation is real in baselines but
  does not survive coherent shared-phase search.

---

## STATUS

PRIORITY 2 NUMERICAL PROBE: COMPLETE (finite search).
ANALYTIC SIGNED MULTI-SHAPE LEMMA: OPEN.
(17) / CLAY / SWIRL: NOT CLAIMED.
NS NOT SOLVED.
