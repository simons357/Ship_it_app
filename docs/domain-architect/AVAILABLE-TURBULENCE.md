# Available-tech turbulence stack (15% desired)

**Status:** a Domain Architect lab cycle, August 2026  
**Not 3D Navier–Stokes. Not a tank certificate. Clay is NOT CLAIMED.**

The slogan “decrease turbulence” is still **not** a recognized setpoint.
A13 refuses it. This cycle keeps the intensity analog’s desired state
\(x\to 0.85\) (**15% below** the industry-standard no-actuation intensity)
and **synthesizes a hardware stack from technology that already exists**.

## Plug-in

| Slot | What DA stores | Gate |
|---|---|---|
| **Desired** | \(x\to 0.85\), 15% below industry \(x=1\) | recognized setpoint |
| **Analog realized** | same lumped plant as `turbulence-intensity`, treated vs \(u=0\) | `COMPUTATIONAL` |
| **Hardware realized** | **no** | `empirical[unverified]` |

`realized_or_desired` is **`desired`**. The analog can realize 15% on the
lumped plant. The hardware does not get that stamp from DA.

## Default stack

Selected because it is field-available, not because DA ran CFD:

1. **Sawtooth riblets** — passive near-wall **constraint**. Literature
   skin-friction envelope about 4–10%. Catalog mechanism `riblet_geometry`.
2. **Discrete wall suction** — active wall **forcing** (porous panel +
   pump). Literature envelope about 8–20%. Catalog mechanism
   `discrete_suction`.

Not selected: LEBU blades (parasitic drag), superhydrophobic slip (not
field-ready), Kramer-class compliant wall (replication mixed), locally
resonant polymer film (licensing overlay, no DA envelope).

Literature highs are **not added**. The selected-high envelope (suction
20%) **can contain** the 15% target. A separate **commercial band**
8–12% sits inside that envelope; it is a licensing target, not a tank
number. That is an envelope check, not a proof and not a flight number.

Application context (not CFD): aircraft cruise boundary layer, Mach
about 0.75–0.85, altitude about 30 000–40 000 ft, panel \(Re_\tau\)
about 1 000–5 000. Secondary notes only: ship hull, submarine hull,
internal duct.

## Grok hybrid overlay vs what DA kept

An external licensing sketch asked for a **hybrid riblet + locally
resonant film** at **8–12%**, with a hoped-for first-cycle lab band of
9–14% and a provisional-patent package.

| Piece | DA |
|---|---|
| Cruise regime + riblet \(s^+\), \(h^+\) | **kept** as application context / geometry |
| Embossed / molded riblet film | **kept** as how the riblet is applied |
| Discrete suction | **kept and selected** (available; envelope can contain 15%) |
| Locally resonant / phononic film | **catalogued, not selected** |
| Piezo / plasma assist | **not selected** |
| 9–14% first-cycle lab | **refused** (not a DA measurement) |
| Provisional patent / claim outlines | **attorney-owned**; DA does not file |

DA desired remains **15%** (`x → 0.85`). The 8–12% figure is the
commercial band, not a replacement setpoint. A13 still refuses slogans
such as “8–12% drag reduction” unless written as \(x\to x^\star\).

Empirical gates DA does not award: wall-resolved LES of the selected
riblet geometry, down-select, modular panels, direct drag measurement,
durability.

## Run it

```
python -m domain_architect cycle available-turbulence
python -m domain_architect synthesize --target "decrease turbulence"
python -m domain_architect synthesize --target "x → 0.85" --constraint "|u| ≤ 6"
python -m domain_architect synthesize --target "x → 0.85" --constraint "|u| ≤ 6" --constraint "hardware already available"
```

Desktop Cycle tab: **Available 15% stack**. Desktop Synthesize tab: the same
button fills \(x\to 0.85\) plus `hardware already available` and assembles
the stack. Bare \(x\to 0.85\) without that constraint is still the analog
PD loop.

Sibling analog: [`TURBULENCE-INTENSITY.md`](TURBULENCE-INTENSITY.md).

## What this does not do

- It does not decrease turbulence in a DNS or a tank.
- It does not add 8% + 10% and call the sum a theorem.
- It does not close NS-open.
- It does not revive an archived coating dump as the plant.
- It does not certify a phononic / locally resonant film.
- It does not award a 9–14% laboratory result.
- It does not file a provisional patent.
- It does not make “decrease turbulence” a legal inverse-design target.
