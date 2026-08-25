# Turbulence reduction (program)

**Status:** Domain Architect *program*, August 2026  
**Not a single plant. Not 3D Navier–Stokes. Clay is NOT CLAIMED.**

This is the proper setup: one **project**, four **applications**. DA
decomposes the project into application slots. Each slot gets its own
operating regime, stack, and envelope. Do **not** copy the ship riblet
envelope onto a missile, a submarine, or a drone.

```
turbulence-reduction          ← project
├── ships        ACTIVE       Maersk-class cargo / container hull
├── missiles     QUEUED       high-speed external flow
├── submarines   QUEUED
└── drones       QUEUED
```

| Slot | Status | Cycle / spec |
|---|---|---|
| **ships** | ACTIVE | `available-turbulence` · [`ships.md`](ships.md) |
| **missiles** | QUEUED | [`missiles.md`](missiles.md) |
| **submarines** | QUEUED | [`submarines.md`](submarines.md) |
| **drones** | QUEUED | [`drones.md`](drones.md) |

Correspondence across slots is **analogy**, not a declared \(T\).

## Run the program

```
python -m domain_architect cycle turbulence-reduction
python -m domain_architect cycle available-turbulence
```

Desktop Cycle tab: **Turbulence reduction (4 apps)**.

Ships is the live study (desired 8–12% Cf; durable trapezoids contain 8%,
not 12%). Missiles, submarines, and drones are empty slots until their
own DA studies run.

## What this does not do

- It does not treat “decrease turbulence” as a setpoint (A13 still refuses).
- It does not award a ship envelope to another platform.
- It does not certify a phononic / resonant film.
- It does not file patents.
- It does not close NS-open.
