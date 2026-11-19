import React, { useState } from "react";
import { MB } from "../qstack/MathBlock";

const SECTIONS = [
  {
    id: "leray",
    label: "Leray-Hopf",
    color: "text-gray-400",
    dot: "bg-gray-500",
    entries: [
      { tag: "Energy class", formula: "u \\in L^\\infty(0,T;L^2) \\cap L^2(0,T;\\dot{H}^1)" },
      { tag: "Energy inequality", formula: "\\|u(t)\\|^2_{L^2} + 2\\int_0^t\\|\\nabla u\\|^2_{L^2}\\,ds \\le \\|u_0\\|^2_{L^2}" },
      { tag: "NS equation", formula: "\\partial_t u + (u\\cdot\\nabla)u = -\\nabla p + \\nu\\Delta u,\\quad \\nabla\\cdot u=0" },
    ],
  },
  {
    id: "shells",
    label: "Shell Decomposition",
    color: "text-cyan-500",
    dot: "bg-cyan-500",
    entries: [
      { tag: "LP projection", formula: "u = \\sum_{j=0}^N P_j u,\\quad \\hat{P_j u} = \\hat{u}\\cdot\\mathbf{1}_{2^j\\le|k|<2^{j+1}}" },
      { tag: "Shell energy", formula: "E_j(t) = \\|P_j u(t)\\|^2_{L^2}" },
      { tag: "Simplex coord.", formula: "a_j(t) = \\frac{E_j(t)}{\\sum_k E_k(t)} \\in \\Delta_N" },
      { tag: "Reference μ", formula: "\\mu = (\\mu_0,\\ldots,\\mu_N) \\in \\Delta_N,\\quad \\sum_j\\mu_j=1" },
    ],
  },
  {
    id: "snd",
    label: "SND Condition",
    color: "text-amber-400",
    dot: "bg-amber-400",
    entries: [
      { tag: "SND def.", formula: "\\mathrm{SND}_N(\\eta,\\mu):\\;\\sup_{t\\ge0}\\|a(t)-\\mu\\|_{\\ell^1}\\le\\eta" },
      { tag: "ℓ¹ deviation", formula: "\\|a(t)-\\mu\\|_{\\ell^1} = \\sum_j|a_j(t)-\\mu_j|" },
      { tag: "Gronwall target", formula: "\\frac{d}{dt}f(t) \\le -\\kappa f(t) + C_{\\mathrm{NL}},\\quad f=\\|a-\\mu\\|_{\\ell^1}" },
    ],
  },
  {
    id: "q6",
    label: "Q6 Operator",
    color: "text-cyan-400",
    dot: "bg-cyan-400",
    entries: [
      { tag: "Q6 sum form", formula: "Q_6[u] = \\sum_j \\gamma_j[u]\\,\\Pi_j\\, u" },
      { tag: "Activation coeff.", formula: "\\gamma_j = \\kappa\\cdot\\max(0,\\,a_j - a_c)^\\alpha" },
      { tag: "Critical thresh.", formula: "a_c = \\mu_j + \\eta/N" },
      { tag: "Shell operator", formula: "\\Pi_j = P_j^*P_j,\\quad \\|\\Pi_j\\|_{\\mathrm{op}}=1" },
    ],
  },
  {
    id: "h3",
    label: "H3 Spectral Gap",
    color: "text-emerald-400",
    dot: "bg-emerald-400",
    entries: [
      { tag: "Residual operator", formula: "R_N(t) = H_N[u(t)] - H_N[\\mu]" },
      { tag: "H3 target", formula: "\\sup_{t\\ge0}\\|R_N(t)\\|_{\\mathrm{op}} < 0.20" },
      { tag: "Gap condition", formula: "\\inf_{t\\ge0}\\lambda_{\\min}(H_N(t)) > -\\tfrac{1}{2}" },
      { tag: "Lipschitz bound", formula: "\\|R_N(t)\\|_{\\mathrm{op}} \\le C_N\\|a(t)-\\mu\\|_{\\ell^1}" },
      { tag: "H3 from SND", formula: "C_N\\eta_N < 0.20 \\implies \\text{H3 holds}" },
    ],
  },
  {
    id: "lemmas",
    label: "Key Lemmas",
    color: "text-violet-400",
    dot: "bg-violet-400",
    entries: [
      { tag: "L1 · Triangle", formula: "\\|\\textstyle\\sum_j\\Delta\\gamma_j\\Pi_j\\|_{\\mathrm{op}} \\le \\sum_j|\\Delta\\gamma_j|\\|\\Pi_j\\|_{\\mathrm{op}}" },
      { tag: "L3 · Orthog.", formula: "\\|\\textstyle\\sum_j\\Delta\\gamma_j\\Pi_j\\|_{\\mathrm{op}} = \\max_j|\\Delta\\gamma_j| \\;(\\text{if }\\Pi_j\\perp)" },
      { tag: "L5 · Simplex Lip.", formula: "\\|H_N[a]-H_N[\\mu]\\|_{\\mathrm{op}} \\le C_N\\|a-\\mu\\|_{\\ell^1}" },
    ],
  },
  {
    id: "rh",
    label: "ΩStack / RH",
    color: "text-violet-500",
    dot: "bg-violet-500",
    entries: [
      { tag: "Zeta function", formula: "\\zeta(s) = \\sum_{n=1}^\\infty n^{-s},\\quad \\mathrm{Re}(s)>1" },
      { tag: "Zero-density shell", formula: "\\Pi_j^\\zeta = \\int_{T_j}^{T_{j+1}}|\\phi_t\\rangle\\langle\\phi_t|\\,dt" },
      { tag: "Zero simplex", formula: "\\alpha_j(T) = \\frac{\\#\\{\\rho\\in\\Pi_j^\\zeta\\}}{N(T)} \\in \\Delta_N^\\zeta" },
      { tag: "SZD condition", formula: "\\mathrm{SZD}_N(\\eta,\\mu^\\zeta):\\;\\sup_T\\|\\alpha(T)-\\mu^\\zeta\\|_{\\ell^1}\\le\\eta" },
      { tag: "RH gap target", formula: "\\sup_T\\|R_N^\\zeta(T)\\|_{\\mathrm{op}} < 0.20" },
    ],
  },
  {
    id: "bridge",
    label: "NS ↔ RH Bridge",
    color: "text-rose-400",
    dot: "bg-rose-400",
    entries: [
      { tag: "Simplex analogy", formula: "a_j[u(t)] \\longleftrightarrow \\alpha_j(T)" },
      { tag: "Deviation analogy", formula: "\\Delta\\gamma_j \\longleftrightarrow \\sigma_j(T)" },
      { tag: "Operator analogy", formula: "Q_6 \\longleftrightarrow \\Omega_6" },
      { tag: "Cage analogy", formula: "\\mathrm{SND}_N(\\eta,\\mu) \\longleftrightarrow \\mathrm{SZD}_N(\\eta,\\mu^\\zeta)" },
    ],
  },
];

export default function FormulaReference() {
  const [open, setOpen]         = useState(false);
  const [expanded, setExpanded] = useState(new Set(["h3", "snd"]));
  const [search, setSearch]     = useState("");

  const toggle = (id) => setExpanded(prev => {
    const next = new Set(prev);
    next.has(id) ? next.delete(id) : next.add(id);
    return next;
  });

  const q = search.toLowerCase();
  const filtered = SECTIONS.map(sec => ({
    ...sec,
    entries: q
      ? sec.entries.filter(e => e.tag.toLowerCase().includes(q) || sec.label.toLowerCase().includes(q))
      : sec.entries,
  })).filter(sec => sec.entries.length > 0);

  return (
    <>
      {/* Toggle button — fixed bottom-right */}
      <button
        onClick={() => setOpen(o => !o)}
        className={`fixed bottom-6 right-6 z-50 flex items-center gap-2 px-3 py-2 rounded-lg border text-xs font-mono uppercase tracking-widest shadow-xl transition-all ${
          open
            ? "bg-gray-900 border-gray-600 text-gray-300"
            : "bg-[#10131a] border-gray-700 text-gray-400 hover:border-gray-500 hover:text-gray-200"
        }`}
        title="Formula Reference"
      >
        <span className="text-base leading-none">∑</span>
        <span className="hidden sm:inline">{open ? "Close" : "Formulas"}</span>
      </button>

      {/* Sidebar panel */}
      <div className={`fixed top-0 right-0 h-full z-40 flex flex-col bg-[#0d0f14] border-l border-gray-800 shadow-2xl transition-all duration-300 ${
        open ? "w-80 sm:w-96" : "w-0 overflow-hidden"
      }`}>
        {open && (
          <>
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-gray-800 flex-shrink-0">
              <div>
                <div className="text-[9px] text-gray-600 uppercase tracking-widest">QStack · ΩStack</div>
                <div className="text-sm font-bold text-white mt-0.5">Formula Reference</div>
              </div>
              <button onClick={() => setOpen(false)} className="text-gray-600 hover:text-gray-300 text-lg leading-none">✕</button>
            </div>

            {/* Search */}
            <div className="px-4 py-2 border-b border-gray-800 flex-shrink-0">
              <input
                value={search}
                onChange={e => setSearch(e.target.value)}
                placeholder="Search formulas…"
                className="w-full bg-[#080a10] border border-gray-800 rounded px-3 py-1.5 text-xs text-gray-300 placeholder-gray-700 font-mono focus:outline-none focus:border-gray-600"
              />
            </div>

            {/* Section toggles */}
            <div className="px-4 py-2 border-b border-gray-800 flex-shrink-0 flex flex-wrap gap-1">
              {SECTIONS.map(sec => (
                <button key={sec.id} onClick={() => toggle(sec.id)}
                  className={`flex items-center gap-1 px-2 py-0.5 rounded text-[9px] font-mono border transition-colors ${
                    expanded.has(sec.id)
                      ? "border-gray-600 bg-white/5 text-gray-300"
                      : "border-gray-800 text-gray-600 hover:border-gray-700"
                  }`}>
                  <span className={`w-1.5 h-1.5 rounded-full ${sec.dot}`} />
                  {sec.label}
                </button>
              ))}
            </div>

            {/* Formula list */}
            <div className="flex-1 overflow-y-auto px-2 py-2 space-y-1">
              {filtered.map(sec => (
                <div key={sec.id}>
                  <button
                    onClick={() => toggle(sec.id)}
                    className="w-full flex items-center gap-2 px-2 py-1.5 rounded hover:bg-white/3 transition-colors text-left"
                  >
                    <span className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${sec.dot}`} />
                    <span className={`text-[10px] font-mono uppercase tracking-widest flex-1 ${sec.color}`}>{sec.label}</span>
                    <span className="text-gray-700 text-[9px]">{expanded.has(sec.id) ? "▲" : "▼"}</span>
                    <span className="text-gray-700 text-[9px]">{sec.entries.length}</span>
                  </button>

                  {expanded.has(sec.id) && (
                    <div className="ml-3 space-y-2 mb-2">
                      {sec.entries.map((e, i) => (
                        <div key={i} className="bg-[#080a10] border border-gray-800/60 rounded p-2">
                          <div className="text-[8px] text-gray-600 uppercase tracking-widest mb-1.5 font-mono">{e.tag}</div>
                          <div className="overflow-x-auto">
                            <MB>{e.formula}</MB>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}

              {filtered.length === 0 && (
                <div className="text-center text-gray-700 text-xs font-mono mt-8">No formulas match "{search}"</div>
              )}
            </div>

            {/* Footer */}
            <div className="px-4 py-2 border-t border-gray-800 flex-shrink-0 text-[8px] text-gray-700 font-mono">
              {SECTIONS.reduce((a, s) => a + s.entries.length, 0)} formulas · {SECTIONS.length} sections
            </div>
          </>
        )}
      </div>

      {/* Backdrop on mobile */}
      {open && (
        <div className="fixed inset-0 z-30 bg-black/40 sm:hidden" onClick={() => setOpen(false)} />
      )}
    </>
  );
}