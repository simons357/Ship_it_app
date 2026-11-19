import React from "react";

const LAYER_DESCRIPTIONS = {
  simplex:     "Energy fractions a_j living on Δ_N. The 3D bars show each shell's weight.",
  spectral:    "The λ_min surface — how the spectral gap varies with η. The red floor is λ = −½.",
  cascade:     "Kolmogorov energy cascade from IR to UV. Height = energy, color = regime.",
  zeros:       "Non-trivial zeros of ζ(s) on the critical line Re(s) = ½.",
  snd:         "The SND ℓ¹ tube — the region Δ_N must stay within for H3 to hold.",
  connections: "Entanglement links — how each simplex shell maps to the spectral surface.",
};

const LAYER_COLORS = {
  simplex:     "#22d3ee",
  spectral:    "#a78bfa",
  cascade:     "#f59e0b",
  zeros:       "#ec4899",
  snd:         "#34d399",
  connections: "#6366f1",
};

export default function LayerPanel({ layers, toggleLayer, params, setParams }) {
  return (
    <div className="p-4 space-y-5">
      <div className="text-[9px] text-gray-600 uppercase tracking-widest border-b border-gray-800 pb-2">
        Layers & Parameters
      </div>

      {/* Layer toggles */}
      <div className="space-y-2">
        {Object.entries(layers).map(([key, layer]) => (
          <div key={key} className={`rounded-lg border transition-all ${layer.on ? "border-gray-700 bg-gray-900/30" : "border-gray-900 bg-transparent"}`}>
            <div className="flex items-center gap-3 px-3 py-2.5 cursor-pointer" onClick={() => toggleLayer(key)}>
              {/* Toggle */}
              <div className={`w-7 h-4 rounded-full relative transition-colors flex-shrink-0 ${layer.on ? "bg-opacity-80" : "bg-gray-800"}`}
                style={{ backgroundColor: layer.on ? LAYER_COLORS[key] + "88" : undefined }}>
                <div className={`absolute top-0.5 w-3 h-3 rounded-full transition-all ${layer.on ? "left-3.5 bg-white" : "left-0.5 bg-gray-600"}`} />
              </div>
              <div className="flex-1 min-w-0">
                <div className="text-[10px] font-bold truncate" style={{ color: layer.on ? LAYER_COLORS[key] : "#4b5563" }}>
                  {layer.label}
                </div>
              </div>
              <div className="w-2 h-2 rounded-full flex-shrink-0" style={{ backgroundColor: layer.on ? LAYER_COLORS[key] : "#1f2937" }} />
            </div>
            {layer.on && (
              <div className="px-3 pb-2.5 text-[9px] text-gray-600 leading-relaxed border-t border-gray-800/40 pt-1.5">
                {LAYER_DESCRIPTIONS[key]}
              </div>
            )}
          </div>
        ))}
      </div>

      {/* Relationship summary */}
      <div className="border border-gray-800 rounded-lg p-3 space-y-2">
        <div className="text-[9px] text-gray-600 uppercase tracking-widest">Active Connections</div>
        {[
          { from: "simplex", to: "spectral", desc: "a_j → λ_min via Lipschitz", active: layers.simplex.on && layers.spectral.on },
          { from: "simplex", to: "snd", desc: "a_j ∈ SND ℓ¹-tube", active: layers.simplex.on && layers.snd.on },
          { from: "cascade", to: "simplex", desc: "energy cascade feeds a_j", active: layers.cascade.on && layers.simplex.on },
          { from: "zeros", to: "spectral", desc: "ΩStack ↔ H3 analogy", active: layers.zeros.on && layers.spectral.on },
        ].map((rel, i) => (
          <div key={i} className={`flex items-center gap-2 text-[9px] font-mono ${rel.active ? "opacity-100" : "opacity-25"}`}>
            <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ backgroundColor: LAYER_COLORS[rel.from] }} />
            <span style={{ color: LAYER_COLORS[rel.from] }}>{rel.from}</span>
            <span className="text-gray-700">→</span>
            <span style={{ color: LAYER_COLORS[rel.to] }}>{rel.to}</span>
            <span className="text-gray-700 truncate text-[8px]">{rel.desc}</span>
          </div>
        ))}
      </div>

      {/* Parameters */}
      <div className="space-y-4 border border-gray-800 rounded-lg p-3">
        <div className="text-[9px] text-gray-600 uppercase tracking-widest">Global Parameters</div>
        {[
          { key: "eta", label: "η (SND radius)", min: 0.01, max: 0.5, step: 0.01, color: "#f59e0b" },
          { key: "kappa", label: "κ (Q6 strength)", min: 0.1, max: 3.0, step: 0.05, color: "#22d3ee" },
          { key: "lambdaGap", label: "λ_gap (headroom)", min: 0.05, max: 1.0, step: 0.05, color: "#a78bfa" },
        ].map(p => (
          <div key={p.key}>
            <div className="flex justify-between items-center mb-1">
              <span className="text-[9px] font-mono" style={{ color: p.color }}>{p.label}</span>
              <span className="text-[10px] font-bold font-mono text-white">{params[p.key].toFixed(2)}</span>
            </div>
            <input type="range" min={p.min} max={p.max} step={p.step} value={params[p.key]}
              onChange={e => setParams(prev => ({ ...prev, [p.key]: parseFloat(e.target.value) }))}
              className="w-full cursor-pointer" style={{ accentColor: p.color }} />
          </div>
        ))}

        <div>
          <div className="flex justify-between mb-1">
            <span className="text-[9px] font-mono text-gray-400">N (shells)</span>
            <span className="text-[10px] font-bold font-mono text-white">{params.N}</span>
          </div>
          <div className="flex gap-1">
            {[8, 10, 12, 14].map(n => (
              <button key={n} onClick={() => setParams(p => ({ ...p, N: n }))}
                className={`flex-1 text-[9px] py-1 rounded border font-mono transition-colors ${params.N === n ? "border-cyan-700 bg-cyan-900/20 text-cyan-300" : "border-gray-800 text-gray-600 hover:border-gray-700"}`}>
                {n}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}