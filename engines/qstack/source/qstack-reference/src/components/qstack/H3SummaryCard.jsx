import React, { useState } from "react";
import { ML, MB } from "./MathBlock";

const BASE_BOUNDS = [
  { id: "L1", label: "Triangle Bound", formula: "\\sum_j |\\Delta\\gamma_j|\\,\\|\\Pi_j\\|_{\\mathrm{op}}", value: 0.31, method: "L1 crude" },
  { id: "L2", label: "Positive Cage", formula: "\\left\\|\\sum_j \\rho_j\\Pi_j\\right\\|_{\\mathrm{op}}", value: 0.24, method: "L2 positive" },
  { id: "L3", label: "Orthogonal Proj.", formula: "\\max_j|\\Delta\\gamma_j|", value: 0.17, method: "L3 orthogonal" },
  { id: "L5", label: "Simplex Lipschitz", formula: "C_N\\|a(t)-\\mu\\|_{\\ell^1}", value: 0.19, method: "L5 simplex" },
];

const STATUS_COLORS = {
  met: { bar: "bg-emerald-500", text: "text-emerald-400", border: "border-emerald-700/50", bg: "bg-emerald-950/20", badge: "bg-emerald-900/40 text-emerald-400 border-emerald-700" },
  near: { bar: "bg-amber-400", text: "text-amber-400", border: "border-amber-700/50", bg: "bg-amber-950/20", badge: "bg-amber-900/40 text-amber-400 border-amber-700" },
  fail: { bar: "bg-rose-500", text: "text-rose-400", border: "border-rose-700/50", bg: "bg-rose-950/20", badge: "bg-rose-900/40 text-rose-400 border-rose-700" },
};

function getStatus(value, threshold) {
  if (value < threshold) return value > threshold * 0.85 ? "near" : "met";
  return "fail";
}

function DeltaSlider({ bound, onValueChange }) {
  const status = getStatus(bound.value, bound.threshold);
  const c = STATUS_COLORS[status];
  const pct = Math.min((bound.value / Math.max(bound.threshold * 1.6, 0.01)) * 100, 100);

  return (
    <div className={`rounded-lg border p-4 ${c.border} ${c.bg} transition-all`}>
      <div className="flex items-start justify-between mb-3">
        <div>
          <div className="text-xs text-gray-500 font-mono uppercase tracking-widest">{bound.id}</div>
          <div className="text-sm text-gray-200 font-semibold mt-0.5">{bound.label}</div>
        </div>
        <div className={`text-xs px-2 py-0.5 rounded-full border font-mono ${c.badge}`}>
          {status === "met" ? "✓ STABLE" : status === "near" ? "⚠ NEAR" : "✗ FAIL"}
        </div>
      </div>

      <div className="mb-3 overflow-x-auto">
        <ML>{bound.formula}</ML>
      </div>

      {/* Progress bar */}
      <div className="relative h-2 bg-gray-800 rounded-full mb-2">
        {/* Threshold marker */}
        <div
          className="absolute top-0 bottom-0 w-0.5 bg-white/30 z-10"
          style={{ left: `${(bound.threshold / (bound.threshold * 1.6)) * 100}%` }}
        />
        {/* Value bar */}
        <div
          className={`h-full rounded-full transition-all duration-500 ${c.bar}`}
          style={{ width: `${pct}%` }}
        />
      </div>

      <div className="flex justify-between text-[10px] font-mono text-gray-600">
        <span>0</span>
        <span className="text-white/40">δ₀ = {bound.threshold}</span>
        <span>{(bound.threshold * 1.6).toFixed(2)}</span>
      </div>

      {/* Editable value */}
      <div className="mt-3 flex items-center gap-3">
        <input
          type="range"
          min={0}
          max={bound.threshold * 1.6}
          step={0.01}
          value={bound.value}
          onChange={(e) => onValueChange(bound.id, parseFloat(e.target.value))}
          className="flex-1 accent-cyan-400 cursor-pointer"
        />
        <span className={`text-sm font-bold font-mono w-12 text-right ${c.text}`}>
          {bound.value.toFixed(2)}
        </span>
      </div>
    </div>
  );
}

export default function H3SummaryCard() {
  const [delta0, setDelta0] = useState(0.20);
  const [boundValues, setBoundValues] = useState(Object.fromEntries(BASE_BOUNDS.map(b => [b.id, b.value])));

  const bounds = BASE_BOUNDS.map(b => ({ ...b, threshold: delta0, value: boundValues[b.id] }));

  const handleValueChange = (id, newVal) => {
    setBoundValues((prev) => ({ ...prev, [id]: newVal }));
  };

  const allMet = bounds.every((b) => b.value < b.threshold);
  const bestBound = bounds.reduce((best, b) => b.value < best.value ? b : best, bounds[0]);

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      <div className="mb-6">
        <div className="flex items-center gap-3 mb-2">
          <div className={`w-2 h-2 rounded-full ${allMet ? "bg-emerald-400 animate-pulse" : "bg-rose-500"}`} />
          <span className={`text-xs tracking-widest uppercase font-mono ${allMet ? "text-emerald-400" : "text-rose-400"}`}>
            {allMet ? "H3 Stability Condition — MET" : "H3 Stability Condition — NOT YET MET"}
          </span>
        </div>
        <h2 className="text-lg font-bold text-white">H3 Energy-Observable Path</h2>
        <p className="text-xs text-gray-400 mt-1">
          Live delta bounds. Drag sliders to simulate coefficient evolution. Green = stable spectral gap.
        </p>
      </div>

      {/* Spectral gap slider */}
      <div className="bg-[#0a0c12] border border-gray-800 rounded-lg p-4">
        <div className="flex items-center justify-between mb-2">
          <div>
            <div className="text-[10px] text-gray-500 uppercase tracking-widest font-mono">Spectral Gap Threshold — δ₀</div>
            <div className="text-[10px] text-gray-600 mt-0.5">
              H3 requires <span className="text-white/60 font-mono">‖R_N(t)‖_op &lt; δ₀</span>. Drag to see which bounds survive.
            </div>
          </div>
          <div className="text-right">
            <div className={`text-2xl font-bold font-mono ${allMet ? "text-emerald-400" : "text-rose-400"}`}>
              δ₀ = {delta0.toFixed(3)}
            </div>
            <div className="text-[9px] text-gray-600 mt-0.5">
              {bounds.filter(b => b.value < b.threshold).length} / {bounds.length} bounds certified
            </div>
          </div>
        </div>
        <div className="flex items-center gap-4 mt-3">
          <span className="text-[9px] font-mono text-gray-700">0.05</span>
          <input
            type="range"
            min={0.05}
            max={0.60}
            step={0.005}
            value={delta0}
            onChange={e => setDelta0(parseFloat(e.target.value))}
            className="flex-1 accent-emerald-400 cursor-pointer"
          />
          <span className="text-[9px] font-mono text-gray-700">0.60</span>
        </div>
        {/* Mini bar showing which bounds pass */}
        <div className="flex gap-1 mt-3">
          {bounds.map(b => {
            const ok = b.value < b.threshold;
            return (
              <div key={b.id} className="flex-1 text-center">
                <div className={`h-1.5 rounded-full transition-all duration-300 ${ok ? "bg-emerald-500" : "bg-rose-600"}`} />
                <div className={`text-[8px] font-mono mt-1 ${ok ? "text-emerald-600" : "text-rose-600"}`}>{b.id}</div>
              </div>
            );
          })}
        </div>
        <div className="mt-2 text-[9px] text-gray-700 font-mono">
          Classical conjecture: δ₀ = 0.20 · &nbsp;
          <button onClick={() => setDelta0(0.20)} className="text-gray-500 hover:text-gray-300 underline underline-offset-2 transition-colors">reset to 0.20</button>
        </div>
      </div>

      {/* Master status banner */}
      <div className={`rounded-xl border p-5 ${allMet ? "border-emerald-700/60 bg-emerald-950/20" : "border-rose-700/40 bg-rose-950/10"}`}>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className={`text-2xl font-bold font-mono ${allMet ? "text-emerald-300" : "text-rose-400"}`}>
              {allMet ? "λ_min(H_N) > −½ · · · CERTIFIED" : "λ_min(H_N) ≤ −½ · · · UNCERTIFIED"}
            </div>
            <div className="text-xs text-gray-500 mt-1">
              Best bound via <span className="text-gray-300">{bestBound.label}</span>:&nbsp;
              <span className={bestBound.value < bestBound.threshold ? "text-emerald-400" : "text-rose-400"}>
                {bestBound.value.toFixed(2)} / {bestBound.threshold}
              </span>
            </div>
          </div>
          <div className="text-right">
            <MB>{`\\|R_N(t)\\|_{\\mathrm{op}} < ${delta0.toFixed(3)}`}</MB>
          </div>
        </div>
      </div>

      {/* Route recap */}
      <div className="grid grid-cols-4 gap-2 text-center text-[10px] font-mono">
        {[
          { label: "Leray Energy", sub: "L²∩L²Ḣ¹", color: "text-gray-400" },
          { label: "Shell Simplex", sub: "a(t)∈Δ_N", color: "text-amber-400" },
          { label: "Coeff. Cage", sub: "SND via Q6", color: "text-cyan-400" },
          { label: "H3 Goal", sub: "‖R_N‖<0.20", color: allMet ? "text-emerald-400" : "text-rose-400" },
        ].map((step, i) => (
          <React.Fragment key={step.label}>
            <div className={`rounded border border-gray-800 bg-[#12151e] p-3 ${step.color}`}>
              <div className="font-semibold">{step.label}</div>
              <div className="text-gray-600 mt-0.5">{step.sub}</div>
            </div>
            {i < 3 && (
              <div className="hidden" />
            )}
          </React.Fragment>
        ))}
      </div>
      <div className="flex justify-between px-1 text-gray-700 text-xs font-mono">
        <span>→</span><span>→</span><span>→</span>
      </div>

      {/* Per-bound cards */}
      <div className="space-y-3">
        {bounds.map((b) => (
          <DeltaSlider key={b.id} bound={b} onValueChange={handleValueChange} />
        ))}
      </div>

      {/* Proof hierarchy */}
      <div className="rounded-lg border border-gray-700 bg-[#12151e] p-5">
        <div className="text-xs text-gray-500 uppercase tracking-widest mb-4">Proof Hierarchy</div>
        <MB>{`\\mathrm{SND} \\Rightarrow \\|a(t)-\\mu\\|_{\\ell^1}\\le\\eta_N \\Rightarrow C_N\\eta_N < ${delta0.toFixed(3)} \\Rightarrow \\inf_{t\\ge0}\\lambda_{\\min}(H_N(t))>-\\tfrac{1}{2}`}</MB>
        <div className="mt-3 text-xs text-gray-600">
          Middle implication complete via Simplex Lipschitz Lemma. Remaining debt: SND → ℓ¹-tube.
        </div>
      </div>
    </div>
  );
}