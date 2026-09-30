# SFE “black hole” matplotlib paste — archive snapshot

Toy 2D numpy / matplotlib animation titled **SFE Black Hole Simulator: Coherence Collapse**.

This folder is **not ChatVault**. It is **not** a black hole. It is **not** general relativity. It is **not** Navier–Stokes. It does **not** prove anything. Domain Architect / SFE / DA does not prove NS. Do not glue this to ChatVault search, E8 ranking, or Millennium claims.

## Already in the repo?

**Not on `main`.** A sanitized copy of the same kernel is already on draft PR 31 (`cursor/sfe-rewrite-domain-architect-9d6b`) at `docs/archive/nav-42-cbfd-2026-04/sfe_black_hole_simulator_paste.py`. This dedicated branch exists so the toy is not mixed into ChatVault (PR 33) or the Domain Architect rewrite.

Sibling 1D slider toy (same sine-sum-independent-of-space bug, more knobs): `docs/archive/sfe-hb/equation_explorer_simons_field.py` on that same PR 31 branch. Neither toy is better physics. This 2D clip is the animation Jonathan pasted.

## What it actually computes

`Phi` in the loop **does not depend on `(x, y)`**. It is a scalar function of `t` and a list of primes:

```
Phi += A * sin(2 * pi * p * t / phi_mod + delta)   # p in [2, 3, 5, 7]
```

The only spatial structure is then

```
Gamma = |Phi| / (r + 1e-5)
Phi[Gamma >= epsilon] = 0
```

with `r = sqrt(x^2 + y^2)` and `epsilon = 0.5`. That zeros a **disk** whose radius tracks `|Phi(t)| / epsilon`. The imshow is a uniform field with a circular hole. Comments in the paste (`Coherence pressure Γ (mimics black hole attractor)`, `Simulate phase collapse`) are slogans. They do not make a Schwarzschild spacetime, an event horizon, or an NS collapse criterion.

This `Phi` is **not** swirl `Φ = u_θ / r`, **not** DA output `Φ`, **not** Newtonian `Φ_g`.

## Files

| File | Role |
|---|---|
| `sfe_field_paste.py` | Snapshot of the chat paste (`plt.show()`, mutable default). Do not run headless. |
| `sfe_field_headless.py` | Same kernel; Agg backend; writes PNG / mp4 / gif. |
| `requirements.txt` | numpy, matplotlib, pillow (local to this toy). |

## Run (headless)

```bash
pip install -r docs/archive/sfe-black-hole-sim/requirements.txt
python docs/archive/sfe-black-hole-sim/sfe_field_headless.py --outdir /opt/cursor/artifacts
```

Desktop with a display: `python docs/archive/sfe-black-hole-sim/sfe_field_paste.py` (will block on `plt.show()`).

```bash
python -m unittest tests.test_sfe_black_hole_sim
```
