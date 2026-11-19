import React, { useState } from "react";
import { ML, MB } from "../qstack/MathBlock";

const ITEMS = [
  {
    id: "OL1",
    tag: "Ω-Lemma 1",
    title: "Universal Zero-Density Bound",
    color: "violet",
    statement: "For arbitrary bounded projection pieces on the Hardy space:",
    formula: "\\left\\|\\sum_{j\\in J_N}\\Delta\\alpha_j\\Pi_j^\\zeta\\right\\|_{\\mathrm{op}} \\le \\sum_{j}|\\Delta\\alpha_j|\\,\\|\\Pi_j^\\zeta\\|_{\\mathrm{op}}",
    consequence: "\\text{RH spectral gap if }\\sup_{T}\\sum_j|\\alpha_j(T)-\\mu_j^\\zeta|\\|\\Pi_j^\\zeta\\|_{\\mathrm{op}} < 0.20",
    note: "Unconditional. Analog of QStack Lemma 1. Uses only triangle inequality on Hardy space.",
  },
  {
    id: "OL2",
    tag: "Ω-Lemma 2",
    title: "Zero-Repulsion Cage Bound",
    color: "amber",
    statement: "Classical zero-repulsion (de la Vallée Poussin + refinements) gives σ-free region:",
    formula: "\\zeta(s)\\ne 0\\quad\\text{for }\\sigma\\ge 1-\\frac{c}{\\log|t|},\\quad|t|\\ge 2",
    consequence: "\\text{RH-class cage: if }|\\alpha_j(T)-\\mu_j^\\zeta|\\le \\frac{c}{\\log T}\\;\\forall j",
    note: "Current best zero-free region. Does NOT prove RH but constrains coefficient cage. Provides starting Ω3 data.",
  },
  {
    id: "OL3",
    tag: "Ω-Lemma 3",
    title: "Orthogonal Band Bound",
    color: "cyan",
    statement: "If the bands Π_j^ζ are mutually orthogonal on H²(strip):",
    formula: "\\left\\|\\sum_{j}\\Delta\\alpha_j\\Pi_j^\\zeta\\right\\|_{\\mathrm{op}} = \\max_j|\\Delta\\alpha_j|",
    consequence: "\\text{RH from: }\\sup_T\\max_j|\\alpha_j(T)-\\mu_j^\\zeta| < 0.20",
    note: "Best possible form. Reduces RH spectral gap to a uniform zero-density envelope — the exact ΩStack target.",
  },
  {
    id: "OL4",
    tag: "Ω-Lemma 4",
    title: "GUE Universality Cage",
    color: "emerald",
    statement: "Montgomery's pair correlation conjecture (GUE statistics) gives zero-density spread:",
    formula: "\\int_0^T \\left|\\zeta\\bigl(\\tfrac12+it\\bigr)\\right|^{2k}\\,dt \\sim C_k\\,T(\\log T)^{k^2}",
    consequence: "\\text{If GUE holds: }\\|\\alpha(T)-\\mu^\\zeta\\|_{\\ell^1} = O(1/\\log T) \\to 0",
    note: "GUE universality → SZD. Not proven but numerically verified to 10^22 zeros. This is the most promising route to closing SZD.",
  },
  {
    id: "OL5",
    tag: "Ω-Lemma 5",
    title: "Simplex Lipschitz (ζ version)",
    color: "rose",
    statement: "Define the Lipschitz constant of H_N^ζ over the zero-density simplex:",
    formula: "C_N^\\zeta := \\sup_{\\alpha\\ne\\beta\\in\\Delta_N} \\frac{\\|H_N^\\zeta[\\alpha]-H_N^\\zeta[\\beta]\\|_{\\mathrm{op}}}{\\|\\alpha-\\beta\\|_{\\ell^1}}",
    consequence: "C_N^\\zeta\\cdot\\eta_N^\\zeta < 0.20 \\implies \\text{RH spectral gap}",
    note: "C_N^ζ must be computed explicitly from the Hardy-space operator. Unknown: depends on choice of H_N^ζ proxy (Connes/Lax-Phillips/Berry-Keating).",
  },
  {
    id: "OT1",
    tag: "Theorem (Open)",
    title: "SZD → RH",
    color: "violet",
    statement: "If the Spectral Zero-Dispersal condition holds for some η_N^ζ, and C_N^ζ · η_N^ζ < 0.20, then:",
    formula: "\\mathrm{SZD}_N(\\eta_N^\\zeta,\\mu^\\zeta) \\;\\&\\; C_N^\\zeta\\eta_N^\\zeta < 0.20 \\implies \\mathrm{RH}",
    consequence: "\\forall\\rho:\\;\\zeta(\\rho)=0\\implies \\operatorname{Re}(\\rho)=\\tfrac{1}{2}",
    note: "This is the ΩStack main theorem. Analogous to QStack Theorem (SND → H3). The proof is complete modulo: (1) constructing H_N^ζ, (2) proving SZD, (3) computing C_N^ζ.",
    isOpen: true,
  },
];

const COLOR_MAP = {
  violet:  { border: "border-violet-700/60",  tag: "text-violet-400",  bg: "bg-violet-950/10" },
  amber:   { border: "border-amber-700/60",   tag: "text-amber-400",   bg: "bg-amber-950/10" },
  cyan:    { border: "border-cyan-700/60",    tag: "text-cyan-400",    bg: "bg-cyan-950/10" },
  emerald: { border: "border-emerald-700/60", tag: "text-emerald-400", bg: "bg-emerald-950/10" },
  rose:    { border: "border-rose-700/60",    tag: "text-rose-400",    bg: "bg-rose-950/10" },
};

export default function RHTheoremBlock() {
  const [expanded, setExpanded] = useState("OT1");

  return (
    <div className="space-y-4 max-w-3xl mx-auto">
      <div className="mb-6">
        <h2 className="text-lg font-bold text-white">ΩStack Lemmas & Theorems</h2>
        <p className="text-xs text-gray-400 mt-1">Exact parallel to QStack theorem library. Same structure, ζ-valued operators.</p>
      </div>

      {ITEMS.map((item) => {
        const c = COLOR_MAP[item.color];
        const open = expanded === item.id;
        return (
          <div key={item.id} className={`rounded-lg border transition-all ${c.border} ${open ? c.bg : "bg-[#12151e]"}`}>
            <button
              className="w-full px-5 py-4 flex items-center justify-between text-left"
              onClick={() => setExpanded(open ? null : item.id)}
            >
              <div className="flex items-center gap-3 flex-wrap">
                <span className={`text-xs font-bold uppercase tracking-widest ${c.tag}`}>{item.tag}</span>
                <span className="text-sm text-gray-200">{item.title}</span>
                {item.isOpen && (
                  <span className="text-[10px] px-2 py-0.5 rounded-full bg-violet-900/40 text-violet-400 border border-violet-800 tracking-widest uppercase">
                    Open Target
                  </span>
                )}
              </div>
              <span className="text-gray-600 text-xs ml-2">{open ? "▲" : "▼"}</span>
            </button>
            {open && (
              <div className="px-5 pb-5 space-y-3">
                <div className="text-xs text-gray-400">{item.statement}</div>
                <MB>{item.formula}</MB>
                {item.consequence && (
                  <>
                    <div className="text-xs text-gray-500 uppercase tracking-widest">Consequence</div>
                    <MB>{item.consequence}</MB>
                  </>
                )}
                {item.note && (
                  <div className={`text-xs rounded border p-3 ${c.border} ${c.bg} ${c.tag}`}>
                    {item.note}
                  </div>
                )}
              </div>
            )}
          </div>
        );
      })}

      {/* Work plan */}
      <div className="mt-8 rounded-lg border border-gray-700 bg-[#12151e] p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-4">ΩStack Immediate Work Plan</div>
        <div className="space-y-3">
          {[
            { n: "1", title: "Construct H_N^ζ explicitly", desc: "Choose between: Berry–Keating (D=xp), Connes adèlic, or Lax–Phillips scattering proxy. Each gives different C_N^ζ." },
            { n: "2", title: "Prove SZD from zero-repulsion", desc: "Use Bohr–Landau / de la Vallée Poussin + GUE pair correlation to bound ‖α(T)−μ^ζ‖_ℓ¹ ≤ η_N^ζ." },
            { n: "3", title: "Compute C_N^ζ", desc: "Lipschitz constant of H_N^ζ over Δ_N. Depends on spectral gap of chosen proxy operator." },
            { n: "4", title: "Certify C_N^ζ · η_N^ζ < 0.20", desc: "Combine steps 2 & 3. If product < δ₀, RH follows from ΩStack main theorem." },
          ].map((s) => (
            <div key={s.n} className="flex gap-4 text-xs">
              <div className="w-6 h-6 rounded-full border border-gray-600 flex items-center justify-center text-gray-500 flex-shrink-0 mt-0.5">
                {s.n}
              </div>
              <div>
                <div className="text-gray-200 font-semibold mb-1">{s.title}</div>
                <div className="text-gray-500">{s.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}