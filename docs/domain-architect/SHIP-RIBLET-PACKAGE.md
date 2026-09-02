# Ship-hull riblet package (Maersk-class)

**Status:** Domain Architect product spec, August 2026  
**Program:** [`docs/projects/turbulence-reduction/`](../projects/turbulence-reduction/README.md) · application **ships** (ACTIVE)  
**Cycle:** `available-turbulence` → `ship_package`  
**Not 3D Navier–Stokes. Not a tank certificate. Clay is NOT CLAIMED.**  
**DA does not file patents.**

## Understanding (locked)

| Ask | DA store |
|---|---|
| Primary customer | Large cargo / container ships (Maersk-class and similar) |
| Desired Cf cut | **8–12%** net turbulent skin friction, **desired**, not realized |
| Fuel translation | **4–8%** total fuel, hypothesis from the standard resistance split |
| Established mechanism | Longitudinal **trapezoidal riblets** in a **fouling-release** carrier |
| Resonant / phononic layer | Catalogued, **not selected**. No established Cf envelope at ship \(Re\) |
| Discrete suction | Aerospace HLFC. **Not** the hull film product |
| Analog 15% | Still the lumped DA setpoint \(x\to 0.85\). Separate from the ship commercial band |

Stay inside established fluid mechanics: Bechert / Walsh riblets, marine fouling-release coatings, the usual frictional vs residual split. Do not invent a burst-frequency coating as a proven Cf mechanism.

Public 2023–2026 notes (conservative): vendor antifoul-stamped riblet immersions exist (MicroTau AIAA SciTech 2023) but are **not** a DA hull Cf. Flexible “gradient riblet” coupons have reported **16.8%** at **0.5 m/s** (ACS Omega 2023) — wrong Re for cargo. Phononic-subsurface DNS (Hussein et al. 2023; Lin et al. 2026) is **order-1% class in channels**, not a marine field coating, and is **not added** to the riblet envelope. Compliant-wall JFM (2024–2025) is laboratory FSI; historical Kramer-class Cf is mixed. IMO CII (in force 1 Jan 2023) makes fouling control material to ratings; a riblet that slimes worse than the incumbent FR can hurt CII. Intersleek-class “up to 9% fuel vs conventional AF” is a **vendor smoothness/fouling claim**, not a grooved-riblet Cf, and is **not added** to Bechert.

## First-order riblet geometry

Literature (Bechert et al., *J. Fluid Mech.* **338**:59–87, 1997, oil channel):

- Optimal spacing \(s^+\approx 17\). Durable **trapezoid**: about **8.2%** Cf cut at \(h/s=0.5\).
- Thin **blades**: **9.9%**. Not field-durable. Not selected.
- Walsh-class sawtooth is typically ~5–8% in earlier tunnels.

Marine overlay (Bressy et al., *Biofouling* 2018): Intersleek-class **embossed riblets** about **6%** vs smooth in Taylor–Couette. Static immersion **increased** biofilm on the riblets. Fouling is the limiter.

DA first-order size, seawater \(\nu\approx 1.2\times 10^{-6}\,\mathrm{m}^2/\mathrm{s}\), \(C_f\approx 0.002\), \(u_\tau=U\sqrt{C_f/2}\), \(s=s^+\,\nu/u_\tau\):

| Station | Speed | \(s\) at \(s^+=16\)–\(17\) | \(h\) at \(h/s=0.5\) |
|---|---|---|---|
| Slow steamer | 15 kn | about 70–90 µm | about 35–45 µm |
| Container cruise | 22 kn | about 50–70 µm | about 25–35 µm |

Use **\(s^+=15\)–\(17\)**, **\(h/s=0.5\)**, trapezoidal section, embossed into an existing fouling-release chemistry. One geometry will not be optimal at every hull station; the band is the first freeze, not a CFD map.

**8% Cf** sits at the durable lab ceiling. **12% Cf is not contained** by that literature. In-service net after slime is usually lower.

## Coating stack (concepts)

1. **Selected — embossed fouling-release.** Trapezoidal riblets in a commercial FR fluoropolymer or silicone already used on hulls. Application: shipyard-compatible emboss or molded film with local streamline alignment.
2. **Established alternative — molded film sheets.** 3M-class riblet film. Known failure: yaw and misalignment increase Cf.
3. **Not selected — phononic / locally resonant overlay (50–300 µm).** No DA skin-friction envelope at ship \(Re\). Kramer-class compliant walls have mixed replication. If someone wants it, it is a **separate experiment** against a riblet-only control. Not an archived coating dump.

Discrete suction is available aerospace hardware. It is not a scalable Maersk hull product (pumps, seawater, fouling of pores).

## Fuel translation (hypothesis)

For low-speed bulkers/tankers, frictional resistance is often **70–90%** of calm-water \(R_T\); for faster container ships, closer to **50–65%** (standard split; Wärtsilä encyclopedia). Then:

- 8% Cf × 0.75 friction fraction ≈ **6%** calm-water resistance.
- 6% Cf × 0.6 ≈ **3.6%**.

A **4–8% fuel** band is consistent **only if** a 6–10% clean-hull Cf cut is actually achieved and fouling does not eat it. DA does not award that.

## Validation (what must be physically tested)

Tunnel \(Re\) is not ship \(Re_L\sim 10^9\). Do not pretend otherwise.

1. Wall-resolved LES of the trapezoid at \(Re_\tau\sim 10^3\)–\(2\times 10^3\).
2. Coupon Cf vs a **smooth FR control** (Taylor–Couette or oil-film / drag balance).
3. Towing-tank panels at the highest reachable \(Re\).
4. Static + dynamic seawater fouling; confirm grooves do not fill.
5. Yaw / cross-flow; misaligned riblets can increase Cf.
6. Abrasion, UV, handling, dry-dock.
7. Any phononic overlay **separately** vs riblet-only.
8. ISO 19030 in-service is **later**, not this first cycle.

## Requested 6–12 month roadmap

**DA status: requested plan, not a schedule certificate.**

1. Freeze trapezoid \(s^+=15\)–\(17\), \(h/s=0.5\); pick two physical \(s\) from cargo \(u_\tau\).
2. Manufacture coupons in an existing approved FR system.
3. Clean Cf vs smooth FR.
4. Fouling exposure and re-test.
5. One towing-tank campaign.
6. Data room for a coatings partner. No ISO 19030 claim yet.

## Patent / licensing (attorney-owned)

DA does **not** file. High-level idea list only:

- Method of embossing trapezoidal \(s^+=15\)–\(17\) riblets into a named fouling-release chemistry.
- Shipyard process that preserves local streamline alignment.
- **Do not** claim an unproven phononic burst-frequency mechanism as the invention.

Licensing one-pager contents owed (empirical, not self-awarded): coupon Cf, fouling, application spec, durability, cost/payback, field-of-use (marine hull vs aerospace).

## Maersk / coatings-partner note

Domain Architect can offer a fouling-release trapezoidal riblet film sized in wall units to cargo-ship shear, aimed at a **desired** 6–8% clean-hull Cf cut (lab ceiling about 8%). An **8–12% net Cf** target at full scale is a commercial stretch, not a measured result. A resonant overlay is a separate experiment, not part of the field-ready stack. Next evidence: coupon Cf and fouling, then a partner towing-tank.

## Run it

```
python -m domain_architect cycle available-turbulence
python -m domain_architect cycle turbulence-reduction
```

Payload key: `prediction.ship_package`. Program parent: [`docs/projects/turbulence-reduction/`](../projects/turbulence-reduction/README.md). Sibling: [`AVAILABLE-TURBULENCE.md`](AVAILABLE-TURBULENCE.md).
