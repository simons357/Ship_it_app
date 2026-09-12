# Attack 9B — original computation

10 September 2026. Recovered from PR 48
(`cursor/ns-five-lane-lemma-star-1390`).
**LIVE kill attempt. ★ open. NS not solved.**
Finite sample. Not a proof. Not a kill.

Phone: stay in this chat.

---

## Family

\[
v_\varepsilon=w_\alpha+\varepsilon z_\beta,\qquad
Aw_\alpha=\alpha w_\alpha,\qquad
Az_\beta=\beta z_\beta,
\qquad
z_\beta\parallel\Pi_\beta B(w_\alpha,w_\alpha).
\]

Exact shell at \(\varepsilon=0\): \(\mathcal D_s=0\), typically
\(T_c=0\). Vacuous. Not a kill. \(\mathcal D_s\) comes from
the small closer when \(\varepsilon>0\).

Boxed:
\[
K_{\alpha,\beta}
=
\sup_{Aw=\alpha w}
\frac{\beta\,\|\Pi_\beta B(w,w)\|_2^2}{\alpha^2\,\|w\|_2^4}.
\]

If \(\sup K=\infty\), then \(\sup\mathcal R_\star=\infty\)
along \(\varepsilon\to 0\) → ★ dead. A finite max is not
that. \(\varepsilon\) and \((\alpha-\beta)\) cancel in the
limit **when** \(z_\beta\) is aligned with
\(\Pi_\beta B(w,w)\) and the sign is chosen so
\((T_c)_+>0\):
\(\mathcal R_\star(v_\varepsilon)\to K_{\alpha,\beta}(w)\).
For arbitrary \(z_\beta\), the limit is the squared
projection against \(B(w,w)\), not necessarily \(K\).

---

## Original run (seed 1390)

| What | Path |
|---|---|
| JSON | `results/ns_five_lane_2026-09-10/attack9b_exact_shell/attack9b.json` |
| Headline | `results/ns_five_lane_2026-09-10/attack9b_exact_shell/HEADLINE.md` |
| Script | `scripts/ns_attacks/attack9b_exact_shell_K.py` |
| SoT | `docs/math/ns_attacks/ATTACK_9B_EXACT_SHELL_CLOSING.md` |

`max K \approx 0.641` at \((\alpha,\beta)=(4,8)\).
Controls PASS. \(\varepsilon\)-limit PASS.
`kill_lane: LIVE`. `lemma_star: OPEN`.

Plots rebuilt from that JSON:
`K_by_ab_pair.png`, `R_star_eps_limit.png`.
β-split notes from PR 48: `BETA_SPLIT_CONFIRM.md`.
Pack snapshot: [`../../FIVE-LANE-PACK.md`](../../FIVE-LANE-PACK.md).
Do not cash \(0.641\) as \(C_0\).

The other VM wrote `/opt/cursor/artifacts/attack9b_exact_shell/`.
The JSON is the `results/` tree above.

---

## After 9B, already scored here

- **9A** AP: \(\mathcal D_s\) wins. `attack9_packet.py`.
- **9C** fixed-gap spheres: this branch’s Attack 11.
  Closures \(O(m)\). \(\mathcal R_\star\) falls \(0.11\to 0.031\).
  Not a kill.
- **9D** designed \(\Theta(m^2)\) locked phase: Freiman-AP,
  already dead. Do not rebuild.
- **Screenshot 9D** (\(\Theta(m^2)\) onto a fixed output set):
  counting error. Excluded. \(K\le 16s\).
  [`../LEMMA-STAR-9B-COUNTING.md`](../LEMMA-STAR-9B-COUNTING.md).

Growing output support is still a 9B test. Keep
\(|k|\). Do not cash a finite \(\sqrt{K}\) as \(C_0\).
Campaign: [`../LEMMA-STAR-9B-GROWING.md`](../LEMMA-STAR-9B-GROWING.md).

Five-lane lanes 1–5: [`COMPUTE.md`](COMPUTE.md).
Packets: [`../LEMMA-STAR-PACKET.md`](../LEMMA-STAR-PACKET.md).

Re-run (optional; does not replace the JSON):

```bash
PYTHONPATH=scripts python3 scripts/ns_attacks/attack9b_exact_shell_K.py \
  --outdir results/attack9b_rerun --seed 1390
```
