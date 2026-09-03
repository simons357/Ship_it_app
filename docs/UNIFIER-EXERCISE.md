# Unifier-program exercise (not a unifier)

Domain Architect is **not** a unifier. This is the exercise you asked for: define success as a number, put that number in as the variable we are hunting, and see which of ~16 coordinates actually move it.

SFE / HB stay shelved as claims (`docs/SHELF.md`). They are only used here as a source of knob names.

---

## Cosmos list

I do not have the DA Cosmos 3-D 16-list. It is not in this repo, not in the HB Experiment files, and Zenodo/HTML for your stack is 403 from here. “1616” I read as “16, 16 or so.”

Until that list is in the repo, the 16 coordinates are **reconstructed**:

| # | Name | Role |
|---|---|---|
| 1–8 | \(A_{\mathrm{mean}}, f_{\mathrm{mean}}, \varphi, \delta, p_{\mathrm{cut}}, S_c, |\nabla C|, \kappa\) | Public SFE / coherence knobs |
| 9–15 | \(\log\alpha_{\mathrm{em}}, \log\alpha_s, \sin^2\theta_W, \log(M_{\mathrm{Pl}}/v), \log(\Lambda_{\mathrm{QCD}}/v), \log(\rho_\Lambda^{1/4}/v), \log(m_W/v)\) | Four-force / leftover-scale anchors |
| 16 | \(R\) | **Realization / success** (output, not a free knob) |

If you drop the actual Cosmos names, I will replace this table and re-run.

The follow-up 4×4 drill (gauge / gravity-gauge / teleological / harmonic) is in [`docs/DA-SIXTEEN.md`](DA-SIXTEEN.md). The 16th is \(R\). Five-finger recursion on the same line: [`docs/DA-FINGERS.md`](DA-FINGERS.md).

---

## Mathematical definition of success

A program with state \(x\) is a **unifier at tolerance \(\varepsilon\)** when one map \(F\) sends \(x\) to all four interaction strengths at one scale \(\mu_*\),

\[
\chi^2_{\mathrm{ext}}(x)=\sum_{i\in\{\mathrm{em},s,W,\mathrm{N},\Lambda,\mathrm{QCD}\}}\bigl(x_i-x_i^{\mathrm{obs}}\bigr)^2\le\varepsilon^2.
\]

Gravity and the vacuum energy stay in the sum. If you omit them, every gauge-only fit looks like a unifier.

Internal HB-language bookkeeping (quiet coherence):

\[
\chi^2_{\mathrm{int}}(x)=\|x_{\mathrm{SFE}}-x_{\mathrm{quiet}}\|_2^2.
\]

**Realization** (the variable we hunt):

\[
R(x)=\exp\bigl(-\tfrac12\chi^2_{\mathrm{ext}}\bigr)\,\exp\bigl(-\tfrac12\chi^2_{\mathrm{int}}\bigr)\in(0,1].
\]

\(R=1\) is “looks like success on this score.” It is not “the forces are unified.” There is still no map \(F\) from the SFE knobs to the couplings. Without that map, the SFE knobs cannot produce the observed \(\alpha_i\); they can only look tidy.

---

## What the numbers did

`python3 scripts/unifier_exercise.py --n 4000`  
Output: `results/unifier_exercise.json`

On 4000 random states around the anchors, permutation importance (fraction of \(\mathbb{E}|\Delta R|\) when that coordinate is shuffled) is dominated by the **external leftovers**, not by the SFE oscillator knobs.

Ranking from the 4000-draw run (`results/unifier_exercise.json`):

1. \(\log(\rho_\Lambda^{1/4}/v)\) — 0.28  
2. \(\log(M_{\mathrm{Pl}}/v)\) — 0.23  
3. \(S_c\) (coherence entropy) — 0.18  
4. \(\delta\) (phase disorder) — 0.11  
5. \(|\nabla C|\) — 0.08  

Prime amplitudes, frequencies, and the three gauge logs are at the bottom (\(\le 0.01\)). Sampling widths matter: hierarchy and the cosmological constant were given more room because that is where the real residuals live. Even so, the SFE oscillator knobs do not move the four-force score.  

The quiet+observed target state has \(R\approx 1\) **by construction** (we sat it on the anchors). That only shows the score is well-defined. It does not show a unifier program.

So: as an exercise, the method works. As a unifier, it does not. The score tells you what you already know if you have looked at unification for five minutes — the cosmological constant and the Planck hierarchy are the variables that kill \(R\). Prime amplitudes and phase offsets do not move the four-force residuals unless you write a map that puts them in. That map is the missing Cosmos object.

---

## Combinatorial search (which ones are involved)

Cardinality is unknown, so every subset of size \(1\ldots 5\) was locked at the target while the complement stayed random.

\[
\mathrm{lock}\,R=\mathbb{E}[R\mid x_S=x_S^\star]
\]

All \(\binom{15}{k}\) for \(k\le 5\), 256 draws. `scripts/unifier_combo.py`.

| \(k\) | Best set | lock \(R\) |
|---:|---|---:|
| 0 | all random | 0.066 |
| 1 | vacuum energy | 0.139 |
| 2 | vacuum + Planck | 0.248 |
| 3 | those two + \(S_c\) | 0.411 |
| 4 | those three + \(\delta\) | 0.577 |
| 5 | those four + \(\lvert\nabla C\rvert\) | 0.703 |

Core in every best set of size \(\ge 2\): \(\log(\rho_\Lambda^{1/4}/v)\) and \(\log(M_{\mathrm{Pl}}/v)\).  
23 sets reach lock \(R\ge 0.5\). None of size \(\le 5\) reach 0.8. Gauge logs and the SFE oscillator knobs never enter a best set.

Domain Architect does not replace this search or the missing map \(F\). When \(F\) exists, point the same lock-\(R\) scan at predicted couplings.

```
python3 scripts/unifier_combo.py --n 256 --kmax 5 --out results/unifier_combo.json
```

---

## What would make a later run actually about Cosmos

Send the 16 names and the formula that turns them into \((\alpha_s,\alpha_w,\alpha_{\mathrm{em}},G_N)\). Then \(R\) is computed from *predicted* couplings, not from treating the couplings as free coordinates. Until then this is a sensitivity drill on a reconstructed vector.
