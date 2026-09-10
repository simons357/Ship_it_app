# Attack 9B — β vs α shell-transfer split

CRITICAL precision correction (user-confirmed):

- Global max K ≈ 0.6410131735094131 at (α,β)=(4, 8) has **β>α** → transfer to a **higher** shell. This is **NOT** HH→L.
- Genuine HH→L subfamily requires **β<α**. Sample max among β<α: K ≈ 0.012320184062780926 at (5, 2).
- Higher-shell (β>α) sample max: K ≈ 0.6410131735094131 at (4, 8).

Kill lane LIVE. NS not solved.

## Re-run confirmation (SoT rewrite)

Same `--seed 1390 --kmax 6`: argmax pairs unchanged.
- β>α ≈0.656 at (4,8) (optimizer scatter vs locked ≈0.641)
- β<α ≈0.0126 at (5,2) (vs locked ≈0.0123)
See `/opt/cursor/artifacts/attack9b_sot_rewrite/BETA_SPLIT_CONFIRM.md`.
