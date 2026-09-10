# Original five-lane computation

10 September 2026 run, recovered from
PR 48 (`cursor/ns-five-lane-lemma-star-1390`).
**NS not solved. ★ not proved.** This is the
scored JSON, not a new search.

**Original five lanes (not 9A–9D).**
[`FIVE_LANES.md`](FIVE_LANES.md). Screenshots did not
name them. `run_all_five.py` did: covariance; triad /
K=0 / \(C_*\); Bony HH→L; Stokes; Route 2. Do not
substitute packet attacks 9A–9D.

Phone: stay in this chat.

---

## Where it sits

| What | Path |
|---|---|
| Headline | `results/ns_five_lane_2026-09-10/HEADLINE.md` |
| Merged runtime | `results/ns_five_lane_2026-09-10/SYNTHESIS_RUNTIME.json` |
| Lanes 1–5 JSON | `results/ns_five_lane_2026-09-10/attack{1–5}.json` |
| Later R★ drill | `results/ns_five_lane_shape_star/` |
| Attack 9B \(K_{\alpha,\beta}\) | `results/ns_five_lane_2026-09-10/attack9b_exact_shell/`; phone [`ATTACK_9B.md`](ATTACK_9B.md) |
| Scripts | `scripts/ns_attacks/run_all_five.py`, `attack1_covariance.py` … `attack5_route2_kill.py` |
| Lane notes | `docs/math/ns_attacks/ATTACK_{1–5}_*.md`, `ATTACK_SYNTHESIS_SIMULTANEOUS.md` |
| Defs | `docs/math/ns_attacks/LEMMA_STAR_SHAPE_FORM.md` (same lock as `docs/five-lane-export/LEMMA_STAR_SHAPE_FORM.md`) |

The other agent’s `/opt/cursor/artifacts/ns_five_lane_*` path
was that machine. The JSON is these `results/` trees.

Do not merge PR 48’s SND / Q6 / SFE pile.

Attack 8 **on this branch** is the three-key probe
(`scripts/ns_attacks/attack8_three_shell.py`). The five-lane
file `ATTACK_8_CORRECT_RECORD.md` is a status lock on PR 48.
Not copied (name collision).

---

## Headline (elapsed ~7 s)

`kill_lane: LIVE`. `lemma_star: OPEN`. `ns_solved: false`.
`LemmaStar_C0_killed: false`.

| Lane | Verdict |
|---|---|
| 1 covariance | `SURVIVE_numeric_NOT_proof` |
| 2 triad / K=0 / C* | `K0_DEAD_Cstar_SURVIVES_numeric` |
| 3 Bony HH→L | `HH_CHANNEL_LIVE_BOTTLENECK_no_closure` |
| 4 Stokes | `STOKES_IDENTITIES_OK_absorption_needs_remainder` |
| 5 Route 2 | `SURVIVE_numeric_gap_remains` |

Numbers from that run (samples, not \(C_0\)):

- Attack 1 phase diam \(\lvert R_{\mathrm{pre}}\rvert\approx 0.155\)
- Attack 2: \(\lvert T_c\rvert/\mathcal D_s\) grows with \(B\)
  (\(0.0035\to 349\) on the triad). K=0 dead.
- Attack 2 \(C_*\approx 0.004058\) amp-invariant on that triad.
  This is **not** \(C_{\star}\).
- Attack 5 (\(n=978\)): max \(\lvert R_{\mathrm{pre}}\rvert\approx 5.088\)
  on `sep_32_p0`; max \(\lvert C_*\rvert\approx 0.04065\)
- Later shape★ drill (\(n=1242\)): max \(\mathcal R_\star\approx 0.0227\)
  (`sep_1_p8`); almost-shell max \(\sim 3.6\cdot 10^{-6}\);
  pure-shell kills \(0\)

Do not cash \(0.0227\), \(0.155\), or \(0.04065\) as \(C_0\).
Uniform pre-Young \(C\) is dead on a later door (Attack 6).
Packet attacks 9–12 on this branch did not kill ★.

---

## Re-run (optional; does not replace the JSON)

```bash
python3 scripts/ns_attacks/run_all_five.py --outdir results/ns_five_lane_rerun --serial
```

`ProbeResult.ratio_box` is \(\mathcal R_\star\). Five-lane
scripts still say `ratio_R_star_shape`; that name is an
alias here. This branch’s `stokes_moments.py` was not
overwritten.

A new search is not the original computation.
