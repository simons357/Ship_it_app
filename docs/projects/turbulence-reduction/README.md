# Turbulence reduction (program)

**Status:** Domain Architect *program*, August 2026  
**Not a single plant. Not 3D Navier–Stokes. Clay is NOT CLAIMED.**  
**DA does not file patents. Public literature only. No classified programs.**

This is the proper setup: one **project**, four **applications**. DA
decomposes the project into application slots. Each slot gets its own
operating regime, stack, and envelope. Do **not** copy the ship riblet
envelope onto aircraft, a submarine, or a hypersonic vehicle.

Drones sit **inside aircraft**, not as a fifth project.

```
turbulence-reduction                ← project
├── ships         ACTIVE            Maersk-class cargo / container hull
├── aircraft      QUEUED            cruise transport; drones / UAV included
├── submarines    QUEUED
└── hypersonic    QUEUED            high-Mach atmospheric flow (not a weapon design)
```

| Slot | Status | Cycle / spec |
|---|---|---|
| **ships** | ACTIVE | `available-turbulence` · [`ships.md`](ships.md) |
| **aircraft** | QUEUED | [`aircraft.md`](aircraft.md) (drones included) |
| **submarines** | QUEUED | [`submarines.md`](submarines.md) |
| **hypersonic** | QUEUED | [`hypersonic.md`](hypersonic.md) |

Correspondence across slots is **analogy**, not a declared \(T\).

Established mechanism on the live slot: **trapezoidal riblets** in a
fouling-release carrier. A resonant / phononic / viscoelastic overlay is
**catalogued, not selected**, and has **no DA Cf envelope**.

Commercial 8–12% Cf is a **desired** band on ships. Durable lab
trapezoids **contain 8%, not 12%**. That band is **not** awarded to the
queued slots.

## Run the program

```
python -m domain_architect cycle turbulence-reduction
python -m domain_architect cycle available-turbulence
```

Desktop Cycle tab: **Turbulence reduction (4 apps)**.

## What this does not do

- It does not treat “decrease turbulence” as a setpoint (A13 still refuses).
- It does not award a ship envelope to another platform.
- It does not certify a phononic / resonant / viscoelastic film.
- It does not file patents or claim classified access.
- It does not design weapons.
- It does not close NS-open.
