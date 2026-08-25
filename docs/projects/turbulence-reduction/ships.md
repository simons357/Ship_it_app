# Application: ships (ACTIVE)

**Program:** [`turbulence-reduction`](README.md)  
**Status:** ACTIVE  
**Customer:** Maersk-class liner and similar (container, tanker, bulker)  
**Cycle:** `available-turbulence`  
**Full spec:** [`docs/domain-architect/SHIP-RIBLET-PACKAGE.md`](../../domain-architect/SHIP-RIBLET-PACKAGE.md)  
**Not a tank certificate. Clay is NOT CLAIMED. DA does not file patents.**

This is the live study. The other three slots wait.

## Public state of the art (conservative)

| Source | What it actually shows | Label |
|---|---|---|
| Bechert et al., *J. Fluid Mech.* **338**:59–87 (1997) | Oil-channel trapezoid \(s^+\approx 17\), \(h/s=0.5\): about **8.2%** Cf cut. Thin blades 9.9%, not durable. | laboratory |
| Bressy et al., *Biofouling* (2018) | Intersleek-class **embossed** riblets ~**6%** vs smooth in Taylor–Couette. Static immersion **increased** biofilm. Fouling is the limiter. | laboratory |
| MicroTau, AIAA SciTech (2023) conference note | Vendor 12-month Sydney immersion of antifoul-stamped riblets; **not** a DA hull Cf number. | field trial (vendor) |
| Kim et al., *Ocean Eng.* **310**:118783 (2024) | Numerical riblets on a **SUBOFF** hull. Different plant (submarine). Not a cargo Cf. | numerical |

Do **not** add those percentages. A 16% lab coupon at 0.5 m/s is not a
Maersk envelope.

## Realistic expectation (this slot only)

| Quantity | DA store | Confidence |
|---|---|---|
| Desired commercial Cf cut | **8–12%**, desired | stretch; 12% **not contained** |
| Durable literature ceiling | Bechert trapezoid **~8.2%** | laboratory, clean oil channel |
| Marine Couette | **~6%** on FR riblets | laboratory; fouling reduces net |
| Fuel translation | **4–8%** total fuel | **hypothesis** from the frictional split, not a DA measurement |
| Hardware gate | `empirical[unverified]` | needs coupon Cf + fouling, then a tank |

## Preferred technical approach

Longitudinal **trapezoidal riblets** in a **fouling-release** carrier.
Geometry freeze: \(s^+=15\)–\(17\), \(h/s=0.5\). Physical spacing at
cargo \(u_\tau\) is tens of micrometres (see the ship package). Thin
blades, hull suction, and a locally resonant / phononic / viscoelastic
overlay are **not selected**.

## Constraints and risks

Seawater durability, biofouling in the grooves, dry-dock interval,
application/retrofit on a large hull, and loss of net Cf once slime
builds. Ease of coating is a customer constraint, not a DA certificate.

## Validation path

Coupon Cf and fouling first. Then a coatings-partner towing tank.
In-service fuel is last and is not a substitute for Cf.

## Licensing / customer fit

Maersk-class and similar. 8–12% is a **licensing target**, not a
measured hull result. DA does not file patents.

## Still to prove

Clean-hull trapezoid Cf at ship \(Re\); net Cf after a realistic fouling
interval; that the fuel split actually appears in noon reports.
