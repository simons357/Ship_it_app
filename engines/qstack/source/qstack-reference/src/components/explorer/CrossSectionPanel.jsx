import React from "react";

const AXIS_DESCRIPTIONS = {
  x: "Cut along X — slices the simplex ring radially, revealing individual shell columns and their entanglement links.",
  y: "Cut along Y — horizontal slice through all structures. Reveals the spectral surface at a given energy level.",
  z: "Cut along Z — vertical slice through the cascade and zero garden. Shows depth of turbulent structure.",
};

const PRESETS = [
  { label: "Energy midpoint", axis: "y", value: 0, desc: "Slice at λ = 0" },
  { label: "Hard floor", axis: "y", value: -3.5, desc: "At the λ = −½ boundary" },
  { label: "Inertial range", axis: "z", value: 2, desc: "Through cascade inertial shells" },
  { label: "Zero spine", axis: "x", value: -8, desc: "Along the critical line Re = ½" },
  { label: "Simplex equator", axis: "x", value: 0, desc: "Through simplex center" },
];

export default function CrossSectionPanel({ crossSection, setCrossSection, params }) {
  const { axis, value } = crossSection;

  // What's revealed at current slice
  const revealed = getRevealedStructures(axis, value, params);

  return (
    <div className="p-4 space-y-5">
      <div className="text-[9px] text-gray-600 uppercase tracking-widest border-b border-gray-800 pb-2">
        Cross Section Tool
      </div>

      {/* Axis selector */}
      <div>
        <div className="text-[9px] text-gray-600 mb-2">Cut Axis</div>
        <div className="grid grid-cols-3 gap-1">
          {["x", "y", "z"].map(a => (
            <button key={a} onClick={() => setCrossSection(cs => ({ ...cs, axis: a }))}
              className={`py-2 text-xs font-mono rounded border transition-colors font-bold ${
                axis === a ? "border-cyan-700 bg-cyan-900/20 text-cyan-300" : "border-gray-800 text-gray-600 hover:border-gray-700 hover:text-gray-400"
              }`}>
              {a.toUpperCase()}
            </button>
          ))}
        </div>
        <div className="text-[9px] text-gray-600 mt-2 leading-relaxed">{AXIS_DESCRIPTIONS[axis]}</div>
      </div>

      {/* Position slider */}
      <div>
        <div className="flex justify-between items-center mb-2">
          <span className="text-[9px] text-gray-500">Position along {axis.toUpperCase()}</span>
          <span className="text-sm font-bold font-mono text-white">{value.toFixed(2)}</span>
        </div>
        <input type="range" min={-8} max={8} step={0.1} value={value}
          onChange={e => setCrossSection(cs => ({ ...cs, value: parseFloat(e.target.value) }))}
          className="w-full cursor-pointer" style={{ accentColor: "#22d3ee" }} />
        <div className="flex justify-between text-[8px] text-gray-800 mt-0.5 font-mono">
          <span>−8</span><span>0</span><span>+8</span>
        </div>

        {/* Reset */}
        <button onClick={() => setCrossSection(cs => ({ ...cs, value: 0 }))}
          className="mt-2 w-full text-[9px] py-1.5 rounded border border-gray-800 text-gray-600 hover:border-gray-700 hover:text-gray-400 transition-colors">
          Reset (no cut)
        </button>
      </div>

      {/* Presets */}
      <div>
        <div className="text-[9px] text-gray-600 uppercase tracking-widest mb-2">Named Cross Sections</div>
        <div className="space-y-1.5">
          {PRESETS.map(p => (
            <button key={p.label}
              onClick={() => setCrossSection({ axis: p.axis, value: p.value })}
              className={`w-full text-left px-3 py-2 rounded border text-[10px] transition-all ${
                axis === p.axis && Math.abs(value - p.value) < 0.2
                  ? "border-cyan-800 bg-cyan-900/20 text-cyan-300"
                  : "border-gray-800 text-gray-500 hover:border-gray-700 hover:text-gray-300"
              }`}>
              <div className="font-bold">{p.label}</div>
              <div className="text-[8px] text-gray-700 mt-0.5">{p.axis.toUpperCase()} = {p.value} — {p.desc}</div>
            </button>
          ))}
        </div>
      </div>

      {/* Revealed structures */}
      <div className="border border-gray-800 rounded-lg p-3 space-y-2">
        <div className="text-[9px] text-gray-600 uppercase tracking-widest">Revealed at this slice</div>
        {revealed.length === 0 ? (
          <div className="text-[9px] text-gray-700">No active cut — showing full structures.</div>
        ) : (
          revealed.map((r, i) => (
            <div key={i} className="flex items-start gap-2 text-[9px] font-mono">
              <div className="w-1.5 h-1.5 rounded-full mt-0.5 flex-shrink-0" style={{ backgroundColor: r.color }} />
              <div>
                <div style={{ color: r.color }}>{r.structure}</div>
                <div className="text-gray-700 text-[8px]">{r.desc}</div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Slice info */}
      {value !== 0 && (
        <div className="bg-[#0a0c12] border border-gray-800 rounded-lg p-3 text-[9px] font-mono space-y-1">
          <div className="text-gray-600 mb-1">Slice plane equation:</div>
          <div className="text-white">{axis} = {value.toFixed(2)}</div>
          <div className="text-gray-700">Everything with {axis} &gt; {value.toFixed(2)} is clipped</div>
          <div className="text-gray-700">Use with Measure tool to probe the cut face</div>
        </div>
      )}
    </div>
  );
}

function getRevealedStructures(axis, value, params) {
  if (value === 0) return [];
  const results = [];

  if (axis === "y") {
    if (value < -3 && value > -4) {
      results.push({ structure: "Hard floor λ = −½", color: "#ef4444", desc: "The eigenvalue boundary — spectral collapse threshold" });
    }
    if (value > -2 && value < 2) {
      results.push({ structure: "Simplex mid-ring", color: "#22d3ee", desc: "Shell energy levels near ℓ¹ = 0 axis" });
      results.push({ structure: "Spectral surface cross", color: "#a78bfa", desc: `λ_min ≈ ${(params.lambdaGap - 0.3).toFixed(3)} at this height` });
    }
    if (value > 2) {
      results.push({ structure: "SND tube top", color: "#34d399", desc: "ℓ¹-ball cap — upper SND boundary" });
    }
  }
  if (axis === "x") {
    if (Math.abs(value + 8) < 2) {
      results.push({ structure: "Critical line Re = ½", color: "#ec4899", desc: "Riemann zeros revealed here" });
    }
    if (Math.abs(value) < 3) {
      results.push({ structure: "Simplex ring interior", color: "#22d3ee", desc: "μ reference point and deviation tube" });
      results.push({ structure: "Entanglement links", color: "#6366f1", desc: "Cross-section of simplex→spectral connections" });
    }
  }
  if (axis === "z") {
    if (value > 3 && value < 7) {
      results.push({ structure: "Energy cascade", color: "#f59e0b", desc: `Inertial range shells — E ~ k^{-5/3}` });
    }
    if (Math.abs(value + 3) < 2) {
      results.push({ structure: "Zero garden plane", color: "#ec4899", desc: "Plane containing ζ zeros at Im(t) = 14–80" });
    }
  }

  return results;
}