# Attack 9B artifacts note

`/opt/cursor/artifacts/attack9b_exact_shell/` was **missing** at encode start.

## Locked SoT (user / five-lane seed 1390)
Source: `results/ns_five_lane_2026-09-10/attack9b_exact_shell/HEADLINE.md`
- max K ≈ **0.641** at (α,β)=(**4**,**8**)
- controls_all_pass: True
- eps_limit_all_pass: True
- Verdict: finite sample **NOT** a kill; kill lane **LIVE**; NS not solved

Copied as `HEADLINE_LOCKED_seed1390.md` in this directory.

## Smoke re-runs in this environment
- Reduced settings → max K≈0.494 (not authoritative)
- Full defaults seed 1390 → max K≈0.656 at (4,8); eps_limit PASS; `controls_all_pass=False` on this host (do **not** overwrite SoT; locked HEADLINE remains truth)

Kill lane LIVE. NS not solved.
