# DA sixteen: four families, each member, the 16th

`python3 scripts/da_machine.py sixteen`

This is **not** the Cosmo app export. The official table is
[`docs/COSMO-SIXTEEN.md`](COSMO-SIXTEEN.md). This is the
reconstruction you asked for: the same four-way split that
produced “about sixteen” —
**gauge / gravity-gauge / teleological / harmonic** — four
each. Do not glue the two catalogs. The Cosmo 16th is
\(\sum m_\nu\). The 16th here is \(R\).

## The sixteen

| # | Family | Name | Role |
|---|---|---|---|
| 1 | gauge | `log_alpha_em` | EM coupling |
| 2 | gauge | `log_alpha_s` | strong coupling |
| 3 | gauge | `sin2_theta_w` | weak mixing |
| 4 | gauge | `log_weak_ratio` | weak / EM scale |
| 5 | gravity-gauge | `log_hierarchy` | Planck leftover |
| 6 | gravity-gauge | `log_cc_ratio` | vacuum leftover |
| 7 | gravity-gauge | `log_qcd_ratio` | QCD leftover |
| 8 | gravity-gauge | `theta_qcd` | CP leftover (target 0) |
| 9 | harmonic | `A_mean` | amplitude |
| 10 | harmonic | `f_mean` | frequency |
| 11 | harmonic | `phi_scale` | \(\varphi\) |
| 12 | harmonic | `delta_spread` | phase |
| 13 | teleological | `S_coh` | coherence |
| 14 | teleological | `kappa_att` | attractor |
| 15 | teleological | `grad_coh` | gradient |
| **16** | teleological | **`R`** | **realization (output)** |

`p_cut` is on the old 15-input list and **not** in this 4×4.
`theta_qcd` fills the leftover gravity-gauge slot. `R` is
the 16th because it is what the other fifteen are supposed
to produce, not another knob.

## Each one, lock-\(R\)

Fix that one at the star value, draw the rest. Compare to
baseline (nothing fixed). \(n=400\). **Fits** means lock-\(R\)
rises by more than \(0.02\).

From `results/da_sixteen.json` (baseline \(R=0.051\)):

| # | Name | \(\Delta\) lock-\(R\) | Fits? |
|---|---|---:|---|
| 6 | `log_cc_ratio` | +0.080 | yes |
| 5 | `log_hierarchy` | +0.045 | yes |
| 13 | `S_coh` | +0.034 | yes |
| 12 | `delta_spread` | +0.020 | yes |
| 15 | `grad_coh` | +0.011 | no |
| 14 | `kappa_att` | +0.006 | no |
| 8 | `theta_qcd` | +0.006 | no |
| 7 | `log_qcd_ratio` | +0.004 | no |
| 1–4, 9–11 | couplings / \(A,f,\varphi\) | \(\le 0.002\) | no |
| 16 | `R` | — | **target, not a knob** |

Same core as the combo machine. \(\lvert\nabla C\rvert\) is
close and enters the old best \(k=5\) set, but it does not
clear the singleton cut here.

## Family lock

Lock all four members of one family (except \(R\)):

| Family | lock \(R\) | couplings collapse? |
|---|---:|---|
| gravity-gauge | 0.277 | no |
| teleological | 0.118 | no |
| harmonic | 0.079 | no |
| gauge | 0.053 | yes, by construction |

Gauge “wins” coupling RMS only because we pasted the
observed couplings in. That is circular. Gravity-gauge is
the only family that actually moves the score.

Locking the four singletons that fit (`log_cc_ratio`,
`log_hierarchy`, `S_coh`, `delta_spread`) gives lock
\(R=0.51\). Coupling RMS stays \(0.133\), identical to
baseline. **Fits \(R\) is not \(F\).**

Leave-one-out of those four: dropping vacuum hurts most
(\(0.51\to 0.22\)), then Planck (\(0.28\)), then \(S_c\)
(\(0.32\)), then \(\delta\) (\(0.37\)).

## Candidate \(F\) (the next drill)

Affine map, train / holdout, from the oscillator +
teleology knobs to the four couplings. Holdout \(\chi^2\)
is \(0.073\); predicting the observed anchors is \(0.072\).
Verdict: **fail**. Same fail from just \(\{\delta,S_c\}\).

On this reconstructed vector the knobs and the couplings
are independent draws. A producing-map cannot appear. The
check is still fail-able, and it failed.

## How we know it is possible without knowing the names

That is the clue, and it is only a clue:

If a continuous map \(F:\mathbb{R}^n\to\mathbb{R}^k\) is
generic and \(n>k\), the equation \(F(x)=\text{data}\) is
typically solvable. Sixteen claimed slots, four couplings
(or six if you count Planck and \(\Lambda\)): \(16>4\) and
\(15\) knobs \(>6\). That is why “a list of about sixteen”
can be *possible* before anyone writes the names.

It is **not** why *this* sixteen works. This sixteen has
names, and the checker says: four of them move \(R\), the
couplings do not come out of the oscillators, and there is
still no \(F\).

## How far this drill got

1. Count 16 is possible by dimension — clue, not a pass.
2. 4×4 names reconstructed. Official Cosmo 16 is a different catalog.
3. Four singletons raise lock-\(R\). The 16th here is \(R\).
4. Those four do not collapse the four couplings.
5. Affine \(F\) from oscillators / teleology fails holdout.
6. Cosmo names are in. **Blocked** on a public producing-map.

Five-finger recursion on the realization line, and a
general fate for each of the 16 as a candidate type, is
[`docs/DA-FINGERS.md`](DA-FINGERS.md). Official Cosmo
isolation is [`docs/COSMO-SIXTEEN.md`](COSMO-SIXTEEN.md).
Keep this table as the score catalog. Do not replace it
with the app’s 16/16 slogan.
