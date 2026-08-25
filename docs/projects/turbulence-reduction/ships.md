# Application: ships — Global Shipping (ACTIVE)

**Program:** [`turbulence-reduction`](README.md)  
**Status:** ACTIVE  
**Customer:** Maersk-class liner and similar (container, tanker, bulker)  
**Cycle:** `available-turbulence` → `ship_package`  
**Full geometry spec:** [`docs/domain-architect/SHIP-RIBLET-PACKAGE.md`](../../domain-architect/SHIP-RIBLET-PACKAGE.md)  
**Not a tank certificate. Not 3D Navier–Stokes. Clay is NOT CLAIMED.**  
**DA does not file patents. Public literature only.**

This is the live study. Aircraft (drones included), submarines, and
hypersonic stay QUEUED.

## Ground rules applied here

Numbers below are labelled **laboratory**, **numerical**, **projected**,
or **hypothesis**. None is a noon-report fuel certificate. Literature
percentages are **not added**. A resonant / phononic / viscoelastic
overlay is **not** the primary certified mechanism. Closest realistic
product: trapezoidal riblets in a fouling-release carrier.

## Public state of the art (what it actually shows)

| Source | What it shows | Label |
|---|---|---|
| Bechert et al., *J. Fluid Mech.* **338**:59–87 (1997) | Oil-channel trapezoid \(s^+\approx 17\), \(h/s=0.5\): about **8.2%** Cf. Thin blades **9.9%**, not durable. | laboratory |
| Walsh-class sawtooth (earlier tunnels) | typically about **5–8%** Cf | laboratory |
| Bressy et al., *Biofouling* (2018) | Intersleek-class **embossed** riblets ~**6%** vs smooth in Taylor–Couette. Static immersion **increased** biofilm. Fouling is the limiter. | laboratory |
| MicroTau, AIAA SciTech (2023) conference note | Vendor 12-month Sydney immersion of antifoul-stamped riblets. **Not** a DA hull Cf. | field trial (vendor) |
| Liu et al., *ACS Omega* (2023) flexible MSGR | **16.8%** drag cut at **0.5 m/s**. Wrong speed and Re for a cargo hull. | laboratory (not ship-Re) |
| Ocean Eng. review **121591** (2025) | Underwater biomimetic survey: fabrication, durability, and limited effectiveness still the gap. | review |
| Hussein et al., *New J. Phys.* (2023) phononic subsurface | Locally resonant metamaterial can attenuate wall-bounded disturbances in DNS. Stabilization / transition delay, not a hull film. | numerical |
| Lin et al., AIAA (2026) resonant phononic material | Channel DNS: about **1.3%** class drag change near a damping threshold. Sensitive to damping. | numerical |
| IMO CII in force 1 Jan 2023 (Uzun et al. 2023) | Fouling raises frictional resistance and makes CII/EEXI harder. Coatings matter because slime and hard fouling raise power. | regulation / literature |
| International / AkzoNobel Intersleek 1100SR product literature | Manufacturer claim: **up to 9% fuel** vs *conventional antifouling*, plus ~1.2% speed-loss over a docking cycle. **Not a riblet Cf.** Smooth FR vs SPC, not grooved vs smooth FR. | vendor / marketing |
| AkzoNobel International whitepaper, Sea Asia 2025 | Three LNG ships, Intersleek 1100SR, 60-month ISO 19030-style review; CII within agreed limits. **Smooth FR in service**, not an embossed-riblet hull. | vendor case study |
| Koley, Wang & Katz, *J. Fluid Mech.* (2024) | Turbulent BL over a compliant surface: deformation scaling and critical-layer coupling. Not a marine Cf envelope. | laboratory |
| Wang, Koley & Katz, *J. Fluid Mech.* (2025) | High-Re viscoelastic wall: flow–deformation coupling. Historical compliant-wall Cf is **mixed** (reduction, nil, or increase). This paper is FSI, not a hull product. | laboratory |

**Proven in public literature:** riblets can cut *clean* laboratory Cf by roughly 5–10% (geometry- and Re-dependent); durable trapezoids sit near **8%** in oil; embossed FR riblets sit near **6%** in Couette; fouling can erase that. Smooth commercial FR coatings are a real, licensed hull product; their fuel claims are vs conventional AF, not vs a grooved sister coating.

**Not proven:** an 8–12% *net* Cf at cargo \(Re_L\sim 10^9\); a phononic or viscoelastic overlay that adds to riblets on a ship; manufacturer “9% fuel” as a riblet number; plasma as a Maersk film.

Do **not** add 8% riblet + 1% phononic + 9% Intersleek fuel + 16% coupon. Those are different plants, different Re, and different quantities.

Plasma actuators appear in public flow-control reviews. They are **not**
a scalable Maersk hull product (power, seawater, fouling of electrodes).

## Realistic performance expectations

| Quantity | DA store | Label | Confidence |
|---|---|---|---|
| Desired commercial Cf cut | **8–12%** net turbulent skin friction | desired / licensing | stretch. **12% not contained** |
| Durable clean-lab ceiling | Bechert trapezoid **~8.2%** | laboratory | high *in oil channel* |
| Marine Couette on FR riblets | **~6%** vs smooth FR | laboratory | medium; fouling reduces net |
| In-service net Cf after slime | **unknown**; usually **lower** than clean lab | unknown | Bressy: more biofilm at rest |
| Fuel / energy | **4–8%** total fuel **if** 6–10% clean Cf is real and not eaten by fouling | **hypothesis** | frictional split 70–90% of calm-water \(R_T\) for slow full-form ships, ~50–65% for faster containers (standard / Wärtsilä-class split). Not a DA measurement. Not a Maersk noon report. |
| CO₂ | scales with fuel **if** the fuel cut is real | projected from the hypothesis | not awarded |
| Phononic / viscoelastic add-on | **no DA Cf envelope** at ship \(Re\) | unproven | public DNS is order-**1%** class in channels, not marine field |

Honest first product aim: a **desired 6–8% clean-hull Cf** cut (lab
ceiling about 8%). Treat **8–12% net at full scale** as a commercial
stretch, not a measured result.

## Preferred technical approach

**Selected (primary):** longitudinal **trapezoidal riblets** embossed into
a **fouling-release** fluoropolymer or silicone already used on commercial
hulls.

| Parameter | Freeze |
|---|---|
| Section | trapezoidal (not thin blades) |
| \(s^+\) | **15–17** |
| \(h/s\) | **0.5** |
| Physical \(s\) | about **50–90 µm** at cargo \(u_\tau\) (seawater \(\nu\approx 1.2\times 10^{-6}\,\mathrm{m}^2/\mathrm{s}\), \(C_f\sim 0.002\)) |
| 15 kn | \(s\approx 70\)–\(90\,\mu\mathrm{m}\) |
| 22 kn | \(s\approx 50\)–\(70\,\mu\mathrm{m}\) |
| Alignment | local streamline; yaw is a known Cf increase |

**Established alternative:** molded riblet film sheets (3M-class). Failure
mode: misalignment and yaw.

**Not selected for the hull product**

- Thin blades (Bechert 9.9% laboratory, not durable).
- Discrete suction (aerospace HLFC; pumps and seawater fouling).
- Locally resonant / phononic overlay (50–300 µm): **separate experiment**
  vs a riblet-only control. No DA envelope.
- Kramer-class viscoelastic / compliant wall: mixed replication.
- Plasma: not a hull film.
- Superhydrophobic slip: not field-durable in seawater.

One geometry will not be optimal at every hull station. The band is a
first freeze, not a CFD map.

## Key engineering constraints and risks

- **Fouling.** Grooves can fill. Bressy: more biofilm at rest on riblets
  than on smooth FR. Net Cf can go **negative** vs a well-maintained
  smooth FR hull.
- **Dry-dock cycle.** Survive blasting, fender abrasion, handling, UV.
  Life must match a coating interval. DA does not award a year-count.
- **Application / retrofit.** Shipyard-compatible emboss or film on a
  curved, large hull. Alignment tolerance is an engineering risk, not a
  DA certificate.
- **Reynolds number.** Tunnel and Couette are not \(Re_L\sim 10^9\).
- **Yaw / cross-flow** on a real hull.
- **12% net Cf** is outside the durable riblet literature.
- **CII / EEXI.** Public literature (2023 onward) says fouling control
  is already material to ratings. A riblet that fouls worse than the
  incumbent FR coating can **hurt** CII. That must be tested, not assumed.
- **Safety / environment.** Stay on an already-approved FR chemistry
  path. Do not invent a new biocide story.

## Development / validation path

**DA status of any 6–12 month calendar: requested plan, not a schedule
certificate.**

1. Freeze trapezoid \(s^+=15\)–\(17\), \(h/s=0.5\); two physical \(s\) from
   cargo \(u_\tau\).
2. Manufacture coupons in an **existing approved FR** system.
3. Clean Cf vs a **smooth FR control** (Taylor–Couette or oil-film / drag
   balance). Same chemistry, grooved vs smooth.
4. Static plus dynamic seawater fouling; re-test Cf. Confirm grooves do
   not fill.
5. Wall-resolved LES of the trapezoid at \(Re_\tau\sim 10^3\)–\(2\times 10^3\)
   (not ship \(Re_L\)).
6. One towing-tank campaign at the highest reachable Re, same control.
7. Abrasion, UV, handling, dry-dock coupons.
8. Data room for a coatings partner. **No ISO 19030 claim** in this first
   cycle. In-service fuel is last and is not a substitute for Cf.
9. If a partner still wants a phononic / viscoelastic overlay: run it
   **separately** against the riblet-only control. Do not mix the
   envelopes.

Human review required before any customer claim, licensing number, or
regulatory filing.

## Licensing / customer fit

**Customer:** Maersk-class and similar large cargo operators. Fuel cost
and CO₂ are the buying reasons. Ease of retrofit at a scheduled docking
is a constraint.

**What DA can honestly offer:** a fouling-release trapezoidal riblet film
sized in wall units to cargo-ship shear, aimed at a **desired** 6–8%
clean-hull Cf cut. 8–12% net at full scale is a **licensing target**, not
a measured hull result.

DA does **not** file patents. Attorney-owned idea list only: method of
embossing trapezoidal \(s^+=15\)–\(17\) into a named FR chemistry; a
shipyard process that preserves local streamline alignment. **Do not**
claim an unproven phononic burst-frequency mechanism as the invention.

Licensing one-pager still owed from **empirical** work, not from this
document: coupon Cf, fouling, application spec, durability, cost/payback,
field-of-use (marine hull vs aerospace).

## What must still be proven

- Clean-hull trapezoid Cf vs smooth FR at a relevant \(Re_\tau\).
- Net Cf after a realistic fouling interval.
- That grooves survive a docking cycle.
- Application tolerance on a curved hull (yaw).
- That a fuel/CO₂ cut actually appears in ISO 19030 / noon reports
  **after** the Cf is real. The 4–8% fuel band is a split hypothesis
  until then.
- Any phononic or viscoelastic overlay, **separately**, at ship-relevant
  conditions. Public channel DNS of order 1% does not prove a marine
  hybrid.
- I do not know the in-service Cf of this product. It has not been built
  and tested as specified.

## Run it

```
python -m domain_architect cycle available-turbulence
python -m domain_architect cycle turbulence-reduction
```

Payload: `prediction.ship_package`. Hybrid ask is stored as
`ship_package.hybrid_request` with `overlay_selected: false`.
