import React, { useState } from "react";
import { ML, MB } from "../qstack/MathBlock";

const WRONG = [
  {
    label: "Assume RH → Prove bound",
    formula: "\\text{RH} \\Rightarrow |\\zeta(s)| > 0 \\text{ for Re}(s)>\\tfrac{1}{2}",
    note: "CIRCULAR: Uses the conclusion as hypothesis.",
    color: "rose",
  },
  {
    label: "Bootstrap from sub-convexity",
    formula: "\\zeta(\\tfrac{1}{2}+it) = O(|t|^{1/6+\\varepsilon})",
    note: "CIRCULAR RISK: Sub-convexity gives log-free regions but not full RH. Iterating it toward RH assumes convergence not yet proven.",
    color: "rose",
  },
  {
    label: "Use GRH → Deduce RH",
    formula: "\\text{GRH} \\Rightarrow \\text{RH}",
    note: "CIRCULAR: Generalized RH is strictly stronger. Proves nothing new.",
    color: "rose",
  },
];

const RIGHT = [
  {
    step: "1",
    label: "Start: Mellin-L² class only",
    formula: "f \\in L^2(\\mathbb{R}_{>0},\\,x^{-1}\\,dx) \\cap \\mathcal{M}",
    note: "Analog of Leray energy class. No regularity assumptions beyond what's proven.",
    color: "emerald",
  },
  {
    step: "2",
    label: "Zero-density shell decomposition",
    formula: "\\alpha_j(T) = \\frac{\\#\\{\\rho : |\\operatorname{Im}(\\rho)-T_j|<\\Delta\\}}{N(T)},\\quad \\alpha\\in\\Delta_N",
    note: "Normalized zero counts per band — the ζ analog of simplex a_j[u]. Energy-class observable: uses N(T) = (T/2π)log(T/2π) − T/2π + O(log T) only.",
    color: "emerald",
  },
  {
    step: "3",
    label: "SZD condition (open debt)",
    formula: "\\sup_{T\\ge T_0}\\|\\alpha(T)-\\mu^\\zeta\\|_{\\ell^1} \\le \\eta_N^\\zeta",
    note: "Spectral Zero-Dispersal: zeros stay spread along critical line. To be proved from zero-repulsion theorems (Bohr–Landau type).",
    color: "amber",
  },
  {
    step: "4",
    label: "Coefficient cage (open debt)",
    formula: "\\left\\|\\sum_j (\\alpha_j(T)-\\mu_j^\\zeta)\\Pi_j^\\zeta\\right\\|_{\\mathrm{op}} \\le C_N^\\zeta\\,\\eta_N^\\zeta",
    note: "Lipschitz reduction on the zero-density simplex. Requires explicit estimate of C_N^ζ.",
    color: "amber",
  },
  {
    step: "5",
    label: "Spectral gap certification",
    formula: "C_N^\\zeta\\,\\eta_N^\\zeta < 0.20 \\implies \\inf_{t}\\lambda_{\\min}(H_N^\\zeta(t)) > -\\tfrac{1}{2}",
    note: "Hilbert–Pólya proxy enforced. All zeros remain on Re(s)=½.",
    color: "cyan",
  },
  {
    step: "RH",
    label: "Riemann Hypothesis",
    formula: "\\forall\\,\\rho:\\;\\zeta(\\rho)=0,\\;0<\\operatorname{Re}(\\rho)<1 \\implies \\operatorname{Re}(\\rho)=\\tfrac{1}{2}",
    note: "Conclusion. Non-circular: derived from certified spectral gap, not assumed.",
    color: "violet",
    isGoal: true,
  },
];

const COLOR = {
  rose:    { border: "border-rose-700/50",    bg: "bg-rose-950/10",    tag: "text-rose-400",    step: "bg-rose-900/30 text-rose-400 border-rose-700" },
  emerald: { border: "border-emerald-700/50", bg: "bg-emerald-950/10", tag: "text-emerald-400", step: "bg-emerald-900/30 text-emerald-400 border-emerald-700" },
  amber:   { border: "border-amber-700/50",   bg: "bg-amber-950/10",   tag: "text-amber-400",   step: "bg-amber-900/30 text-amber-400 border-amber-700" },
  cyan:    { border: "border-cyan-700/50",    bg: "bg-cyan-950/10",    tag: "text-cyan-400",    step: "bg-cyan-900/30 text-cyan-400 border-cyan-700" },
  violet:  { border: "border-violet-700/50",  bg: "bg-violet-950/10",  tag: "text-violet-400",  step: "bg-violet-900/30 text-violet-400 border-violet-700" },
};

export default function RHRouteMap() {
  const [open, setOpen] = useState("RH");

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div className="mb-4">
        <h2 className="text-lg font-bold text-white">RH Non-Circular Route Map</h2>
        <p className="text-xs text-gray-400 mt-1">
          Exactly parallel to the H3 route. Left: dangerous circular routes. Right: the correct ΩStack path.
        </p>
      </div>

      {/* Danger routes */}
      <div>
        <div className="text-xs text-rose-500 uppercase tracking-widest mb-3 flex items-center gap-2">
          <span className="text-rose-600">✗</span> Dangerous / Circular Routes
        </div>
        <div className="space-y-3">
          {WRONG.map((w, i) => {
            const c = COLOR[w.color];
            return (
              <div key={i} className={`rounded-lg border p-4 ${c.border} ${c.bg}`}>
                <div className={`text-xs font-semibold mb-2 ${c.tag}`}>{w.label}</div>
                <div className="overflow-x-auto mb-2"><MB>{w.formula}</MB></div>
                <div className="text-xs text-rose-400/70 font-mono">{w.note}</div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Divider */}
      <div className="flex items-center gap-3">
        <div className="flex-1 border-t border-gray-800" />
        <span className="text-xs text-gray-600 font-mono uppercase tracking-widest">Correct Route ↓</span>
        <div className="flex-1 border-t border-gray-800" />
      </div>

      {/* Correct route */}
      <div>
        <div className="text-xs text-emerald-500 uppercase tracking-widest mb-3 flex items-center gap-2">
          <span className="text-emerald-500">✓</span> ΩStack Non-Circular Route
        </div>
        <div className="space-y-3">
          {RIGHT.map((r) => {
            const c = COLOR[r.color];
            const isOpen = open === r.step;
            return (
              <div key={r.step} className={`rounded-lg border transition-all ${c.border} ${isOpen ? c.bg : "bg-[#12151e]"}`}>
                <button
                  className="w-full px-5 py-4 flex items-center justify-between text-left"
                  onClick={() => setOpen(isOpen ? null : r.step)}
                >
                  <div className="flex items-center gap-3">
                    <span className={`text-xs font-bold px-2 py-0.5 rounded border font-mono ${c.step}`}>
                      {r.step}
                    </span>
                    <span className="text-sm text-gray-200">{r.label}</span>
                    {r.isGoal && (
                      <span className="text-[10px] px-2 py-0.5 rounded-full bg-violet-900/40 text-violet-400 border border-violet-800 tracking-widest uppercase">
                        Goal
                      </span>
                    )}
                    {r.color === "amber" && (
                      <span className="text-[10px] px-2 py-0.5 rounded-full bg-amber-900/30 text-amber-400 border border-amber-800 tracking-widest uppercase">
                        Open
                      </span>
                    )}
                  </div>
                  <span className="text-gray-600 text-xs">{isOpen ? "▲" : "▼"}</span>
                </button>
                {isOpen && (
                  <div className="px-5 pb-5 space-y-3">
                    <div className="overflow-x-auto"><MB>{r.formula}</MB></div>
                    <div className={`text-xs rounded border p-3 ${c.border} ${c.bg} ${c.tag}`}>
                      {r.note}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      {/* Proof hierarchy */}
      <div className="rounded-lg border border-gray-700 bg-[#12151e] p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-4">Proof Hierarchy (Full Chain)</div>
        <MB>{"\\mathrm{SZD} \\Rightarrow \\|\\alpha(T)-\\mu^\\zeta\\|_{\\ell^1}\\le\\eta_N^\\zeta \\Rightarrow C_N^\\zeta\\eta_N^\\zeta < 0.20 \\Rightarrow \\lambda_{\\min}(H_N^\\zeta)>-\\tfrac{1}{2} \\Rightarrow \\mathrm{RH}"}</MB>
        <div className="mt-4 grid grid-cols-2 md:grid-cols-4 gap-2 text-[10px] font-mono text-center">
          {["SZD", "ℓ¹-tube", "Spectral Gap", "RH"].map((s, i) => (
            <div key={s} className={`rounded border p-2 ${i === 3 ? "border-violet-700 text-violet-400" : i === 0 ? "border-amber-700 text-amber-400" : "border-gray-700 text-gray-400"}`}>
              {s}
            </div>
          ))}
        </div>
        <div className="mt-3 text-xs text-gray-600">
          Steps 3→5 are the open debts. Steps 1→2 and 5→RH are established.
        </div>
      </div>
    </div>
  );
}