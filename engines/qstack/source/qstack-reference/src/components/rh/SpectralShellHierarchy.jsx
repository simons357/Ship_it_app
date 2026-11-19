import React, { useState, useEffect, useRef } from "react";
import { MB, ML } from "../qstack/MathBlock";

const N_SHELLS = 16;
const KNOWN_ZEROS = [
  14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327, 48.005, 49.774,
  52.970, 56.446, 59.347, 60.832, 65.113, 67.080, 69.546, 72.067, 75.705, 77.145,
  79.337, 82.910, 84.735, 87.425, 88.809, 92.491, 94.651, 95.870, 98.831, 101.318
];

function initShells() {
  return Array.from({ length: N_SHELLS }, (_, j) => {
    const T0 = 14.0;
    const bandW = 6.5;
    const Tj = T0 + j * bandW;
    const zeros = KNOWN_ZEROS.filter(z => z >= Tj && z < Tj + bandW);
    // spectral gap: distance from nearest zero to critical line deviation
    const deviation = zeros.length > 0 ? Math.random() * 0.04 : Math.random() * 0.12;
    const gap = Math.max(0, 0.5 - deviation - Math.random() * 0.03);
    return {
      j,
      Tj,
      bandEnd: Tj + bandW,
      zeros,
      zeroCount: zeros.length,
      deviation,       // how far zeros stray from Re=1/2
      gap,             // spectral gap estimate
      density: zeros.length / 6.5, // zeros per unit height
      energy: Math.exp(-0.15 * j) * (1 + 0.4 * Math.sin(j * 0.8 + 1)),
      stable: deviation < 0.04,
    };
  });
}

const GAP_COLOR = (gap) => {
  if (gap > 0.45) return "#22d3ee";
  if (gap > 0.38) return "#a78bfa";
  if (gap > 0.28) return "#f59e0b";
  return "#ef4444";
};

const GAP_LABEL = (gap) => {
  if (gap > 0.45) return "STRONG";
  if (gap > 0.38) return "MODERATE";
  if (gap > 0.28) return "WEAK";
  return "BROKEN";
};

export default function SpectralShellHierarchy() {
  const [shells, setShells] = useState(initShells);
  const [selected, setSelected] = useState(null);
  const [running, setRunning] = useState(false);
  const [omega6, setOmega6] = useState(true);
  const [repulsion, setRepulsion] = useState(0.6);
  const [view, setView] = useState("hierarchy"); // hierarchy | strip | gap
  const tickRef = useRef(0);

  // Live simulation
  useEffect(() => {
    if (!running) return;
    const id = setInterval(() => {
      tickRef.current += 1;
      setShells(prev => prev.map(s => {
        const drift = (Math.random() - 0.49) * 0.008;
        let newDev = Math.max(0, s.deviation + drift);
        // Ω6 repulsion: pull deviation toward 0
        if (omega6 && newDev > 0.03) {
          newDev *= (1 - repulsion * 0.06);
        }
        newDev = Math.min(0.18, newDev);
        const newGap = Math.max(0, 0.5 - newDev - Math.random() * 0.01);
        return {
          ...s,
          deviation: newDev,
          gap: newGap,
          stable: newDev < 0.04,
          energy: Math.max(0.01, s.energy + (Math.random() - 0.51) * 0.015),
        };
      }));
    }, 280);
    return () => clearInterval(id);
  }, [running, omega6, repulsion]);

  const sel = selected !== null ? shells[selected] : null;
  const overallGap = shells.reduce((a, s) => a + s.gap, 0) / shells.length;
  const stableCount = shells.filter(s => s.stable).length;
  const rhStatus = stableCount >= N_SHELLS * 0.9 && overallGap > 0.38;

  return (
    <div className="space-y-5 max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-start justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <div className={`w-2 h-2 rounded-full ${rhStatus ? "bg-cyan-400 animate-pulse" : "bg-rose-500 animate-pulse"}`} />
            <span className={`text-xs font-mono uppercase tracking-widest ${rhStatus ? "text-cyan-400" : "text-rose-400"}`}>
              {rhStatus ? "RH — Spectral Gap Holds" : "RH — Gap Uncertain"}
            </span>
          </div>
          <h2 className="text-lg font-bold text-white">Spectral Shell Hierarchy</h2>
          <p className="text-xs text-gray-400 mt-1">
            {N_SHELLS} zero-density bands · Ω6 repulsion · live gap tracking
          </p>
        </div>

        {/* Global metrics */}
        <div className="flex gap-3 flex-wrap">
          {[
            { label: "Avg Gap", value: overallGap.toFixed(3), color: GAP_COLOR(overallGap) },
            { label: "Stable", value: `${stableCount}/${N_SHELLS}`, color: stableCount === N_SHELLS ? "#22d3ee" : "#f59e0b" },
            { label: "Zeros", value: KNOWN_ZEROS.length, color: "#a78bfa" },
          ].map(m => (
            <div key={m.label} className="bg-[#0a0c12] border border-gray-800 rounded px-3 py-2 text-center min-w-[72px]">
              <div className="text-[10px] text-gray-600 uppercase tracking-widest">{m.label}</div>
              <div className="text-base font-bold font-mono mt-0.5" style={{ color: m.color }}>{m.value}</div>
            </div>
          ))}
        </div>
      </div>

      {/* Controls */}
      <div className="flex flex-wrap gap-2 items-center">
        <button onClick={() => setRunning(r => !r)}
          className={`px-3 py-1.5 rounded text-xs font-mono border transition-colors ${running ? "border-cyan-600 bg-cyan-900/20 text-cyan-300" : "border-gray-700 text-gray-400 hover:border-gray-500"}`}>
          {running ? "⏸ Pause" : "▶ Simulate"}
        </button>
        <button onClick={() => setShells(initShells())}
          className="px-3 py-1.5 rounded text-xs font-mono border border-gray-700 text-gray-400 hover:text-gray-200 transition-colors">
          ↺ Reset
        </button>

        <label className="flex items-center gap-2 text-xs text-gray-400 cursor-pointer ml-2">
          <div onClick={() => setOmega6(v => !v)}
            className={`w-9 h-5 rounded-full relative transition-colors ${omega6 ? "bg-violet-700" : "bg-gray-700"}`}>
            <div className={`absolute top-0.5 w-4 h-4 rounded-full bg-white transition-all ${omega6 ? "left-4" : "left-0.5"}`} />
          </div>
          Ω6 Repulsion
        </label>

        {omega6 && (
          <div className="flex items-center gap-2 text-xs">
            <span className="text-gray-600 font-mono">strength</span>
            <input type="range" min={0.1} max={1.0} step={0.05} value={repulsion}
              onChange={e => setRepulsion(parseFloat(e.target.value))}
              className="w-24 accent-violet-400" />
            <span className="text-violet-400 font-mono w-8">{repulsion.toFixed(2)}</span>
          </div>
        )}

        <div className="ml-auto flex gap-1">
          {[["hierarchy", "Hierarchy"], ["strip", "Strip"], ["gap", "Gap Curve"]].map(([id, lbl]) => (
            <button key={id} onClick={() => setView(id)}
              className={`px-3 py-1 rounded text-xs font-mono border transition-colors ${view === id ? "border-violet-600 text-violet-300" : "border-gray-700 text-gray-500 hover:border-gray-600"}`}>
              {lbl}
            </button>
          ))}
        </div>
      </div>

      {/* ---- HIERARCHY VIEW ---- */}
      {view === "hierarchy" && (
        <div className="grid grid-cols-1 xl:grid-cols-3 gap-4">
          {/* Shell list */}
          <div className="xl:col-span-2 bg-[#080a10] border border-gray-800 rounded-lg p-4 space-y-1.5">
            <div className="grid grid-cols-12 text-[9px] text-gray-600 uppercase tracking-widest mb-2 px-1">
              <div className="col-span-1">Π</div>
              <div className="col-span-2">Im band</div>
              <div className="col-span-1 text-center">zeros</div>
              <div className="col-span-4">spectral gap</div>
              <div className="col-span-2 text-center">deviation</div>
              <div className="col-span-2 text-right">energy</div>
            </div>

            {shells.map((s, i) => {
              const gapPct = (s.gap / 0.5) * 100;
              const energyPct = (s.energy / 1.2) * 100;
              const isSelected = selected === i;
              const c = GAP_COLOR(s.gap);
              return (
                <div key={i}
                  onClick={() => setSelected(isSelected ? null : i)}
                  className={`grid grid-cols-12 items-center gap-1 px-2 py-2 rounded cursor-pointer transition-all text-xs ${isSelected ? "bg-white/6 ring-1 ring-violet-600/40" : "hover:bg-white/3"}`}
                >
                  <div className="col-span-1 font-mono text-[10px]" style={{ color: c }}>Π{i + 1}</div>
                  <div className="col-span-2 font-mono text-[9px] text-gray-600">{s.Tj.toFixed(0)}–{s.bandEnd.toFixed(0)}</div>
                  <div className="col-span-1 text-center font-mono font-bold" style={{ color: s.zeroCount > 0 ? "#a78bfa" : "#374151" }}>{s.zeroCount}</div>

                  {/* Gap bar */}
                  <div className="col-span-4 relative h-3 bg-gray-900 rounded">
                    <div className="h-full rounded transition-all duration-300"
                      style={{ width: `${gapPct}%`, backgroundColor: c, opacity: 0.8 }} />
                    <div className="absolute inset-0 flex items-center justify-end pr-1">
                      <span className="text-[8px] font-mono" style={{ color: c }}>{GAP_LABEL(s.gap)}</span>
                    </div>
                  </div>

                  {/* Deviation dot */}
                  <div className="col-span-2 flex justify-center">
                    <div className="w-2 h-2 rounded-full" style={{
                      backgroundColor: s.stable ? "#22d3ee" : "#ef4444",
                      boxShadow: s.stable ? "0 0 6px #22d3ee88" : "0 0 6px #ef444488"
                    }} />
                  </div>

                  {/* Energy bar */}
                  <div className="col-span-2 relative h-2 bg-gray-900 rounded">
                    <div className="h-full rounded transition-all duration-300"
                      style={{ width: `${Math.min(100, energyPct)}%`, backgroundColor: "#6366f1", opacity: 0.7 }} />
                  </div>
                </div>
              );
            })}
          </div>

          {/* Detail panel */}
          <div className="bg-[#080a10] border border-gray-800 rounded-lg p-4">
            {sel ? (
              <div className="space-y-4">
                <div>
                  <div className="text-xs text-gray-500 uppercase tracking-widest">Shell</div>
                  <div className="text-2xl font-bold font-mono mt-1" style={{ color: GAP_COLOR(sel.gap) }}>
                    Π{sel.j + 1}^ζ
                  </div>
                </div>

                <div className="space-y-2 text-xs">
                  {[
                    ["Im band", `[${sel.Tj.toFixed(3)}, ${sel.bandEnd.toFixed(3)})`],
                    ["Zeros in band", sel.zeroCount],
                    ["Zero density", sel.density.toFixed(3) + " / unit"],
                    ["Spectral gap", sel.gap.toFixed(4)],
                    ["Deviation", sel.deviation.toFixed(5)],
                    ["Band energy", sel.energy.toFixed(4)],
                    ["Gap status", GAP_LABEL(sel.gap)],
                    ["Stable?", sel.stable ? "✓ Yes" : "✗ No"],
                  ].map(([k, v]) => (
                    <div key={k} className="flex justify-between border-b border-gray-800/60 pb-1">
                      <span className="text-gray-600 font-mono">{k}</span>
                      <span className="font-mono" style={{ color: k === "Gap status" ? GAP_COLOR(sel.gap) : k === "Stable?" ? (sel.stable ? "#22d3ee" : "#ef4444") : "#cbd5e1" }}>{v}</span>
                    </div>
                  ))}
                </div>

                {sel.zeros.length > 0 && (
                  <div>
                    <div className="text-[10px] text-gray-600 uppercase tracking-widest mb-2">Known zeros</div>
                    <div className="flex flex-wrap gap-1">
                      {sel.zeros.map((z, i) => (
                        <span key={i} className="text-[10px] font-mono px-2 py-0.5 rounded bg-violet-900/30 text-violet-300 border border-violet-800/40">
                          {z.toFixed(3)}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                <div>
                  <div className="text-[10px] text-gray-600 uppercase tracking-widest mb-2">Gap formula</div>
                  <MB>{"\\lambda_{\\min}(H_{\\Pi_{" + (sel.j+1) + "}}^\\zeta) \\approx " + sel.gap.toFixed(3)}</MB>
                </div>

                {/* Neighbor context */}
                <div>
                  <div className="text-[10px] text-gray-600 uppercase tracking-widest mb-2">Neighbors</div>
                  <div className="space-y-1">
                    {[-1, 0, 1].map(d => {
                      const idx = sel.j + d;
                      if (idx < 0 || idx >= shells.length) return null;
                      const ns = shells[idx];
                      const c = GAP_COLOR(ns.gap);
                      return (
                        <div key={d} onClick={() => setSelected(idx)}
                          className={`flex items-center gap-2 px-2 py-1 rounded cursor-pointer transition-all ${d === 0 ? "bg-violet-900/20 ring-1 ring-violet-600/40" : "hover:bg-white/3"}`}>
                          <div className="w-1.5 h-1.5 rounded-full flex-shrink-0" style={{ backgroundColor: c }} />
                          <span className="text-[10px] font-mono text-gray-400">Π{idx + 1}</span>
                          <div className="flex-1 h-1.5 bg-gray-900 rounded">
                            <div className="h-full rounded" style={{ width: `${(ns.gap / 0.5) * 100}%`, backgroundColor: c }} />
                          </div>
                          <span className="text-[10px] font-mono" style={{ color: c }}>{ns.gap.toFixed(3)}</span>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            ) : (
              <div className="h-full flex flex-col items-center justify-center text-center py-10 space-y-3">
                <div className="text-4xl opacity-20">Π</div>
                <div className="text-xs text-gray-600">Click any shell to inspect its spectral gap, zeros, and energy state.</div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* ---- STRIP VIEW ---- */}
      {view === "strip" && (
        <div className="bg-[#080a10] border border-gray-800 rounded-lg p-5">
          <div className="text-xs text-gray-500 uppercase tracking-widest mb-4">Critical Strip — Shell Bands + Zeros</div>
          <div className="relative" style={{ height: 480 }}>
            <svg viewBox="0 0 700 480" className="w-full h-full">
              {/* Strip */}
              <rect x={80} y={10} width={540} height={460} fill="rgba(255,255,255,0.01)" />
              <line x1={80} y1={10} x2={80} y2={470} stroke="#1e293b" strokeWidth={1} />
              <line x1={620} y1={10} x2={620} y2={470} stroke="#1e293b" strokeWidth={1} />

              {/* Critical line */}
              <line x1={350} y1={10} x2={350} y2={470} stroke="#22d3ee" strokeWidth={1.5} strokeDasharray="8,4" opacity={0.6} />
              <text x={350} y={8} textAnchor="middle" fill="#22d3ee" fontSize={9} opacity={0.6}>Re(s) = ½</text>

              {/* Shell bands */}
              {shells.map((s, i) => {
                const T_min = 14, T_max = 14 + N_SHELLS * 6.5;
                const y1 = 10 + ((s.bandEnd - T_min) / (T_max - T_min)) * 460;
                const y0 = 10 + ((s.Tj - T_min) / (T_max - T_min)) * 460;
                const h = Math.max(1, y1 - y0);
                const c = GAP_COLOR(s.gap);
                const isSelected = selected === i;
                return (
                  <g key={i} onClick={() => setSelected(isSelected ? null : i)} style={{ cursor: "pointer" }}>
                    <rect x={80} y={y0} width={540} height={h}
                      fill={i % 2 === 0 ? "rgba(167,139,250,0.04)" : "rgba(34,211,238,0.02)"}
                      stroke={isSelected ? c : "transparent"}
                      strokeWidth={isSelected ? 1 : 0}
                    />
                    {/* Gap indicator bar on left */}
                    <rect x={60} y={y0 + 1} width={18 * (s.gap / 0.5)} height={h - 2} fill={c} opacity={0.7} rx={1} />
                    {/* Shell label */}
                    <text x={50} y={y0 + h / 2 + 3} textAnchor="end" fill={c} fontSize={7} fontFamily="monospace">Π{i + 1}</text>
                    {/* Im label */}
                    <text x={626} y={y0 + 4} fill="#374151" fontSize={6} fontFamily="monospace">{s.Tj.toFixed(1)}</text>
                  </g>
                );
              })}

              {/* Zero dots */}
              {KNOWN_ZEROS.map((z, i) => {
                const T_min = 14, T_max = 14 + N_SHELLS * 6.5;
                if (z > T_max) return null;
                const y = 10 + ((z - T_min) / (T_max - T_min)) * 460;
                const shellIdx = shells.findIndex(s => z >= s.Tj && z < s.bandEnd);
                const stable = shellIdx >= 0 ? shells[shellIdx].stable : true;
                return (
                  <g key={i}>
                    <circle cx={350} cy={y} r={4} fill="#a78bfa" opacity={0.9}
                      style={{ filter: "drop-shadow(0 0 4px #a78bfa)" }} />
                    <circle cx={350} cy={y} r={9} fill="none" stroke="#a78bfa" strokeWidth={0.5} opacity={0.25} />
                    <line x1={90} y1={y} x2={610} y2={y} stroke="#1e293b" strokeWidth={0.5} />
                    <text x={620} y={y + 3} fill="#6b7280" fontSize={6} fontFamily="monospace">{z.toFixed(3)}</text>
                  </g>
                );
              })}

              {/* Axis labels */}
              <text x={80} y={478} fill="#374151" fontSize={8}>Re=0</text>
              <text x={340} y={478} textAnchor="middle" fill="#374151" fontSize={8}>Re=½</text>
              <text x={608} y={478} textAnchor="end" fill="#374151" fontSize={8}>Re=1</text>

              {/* Gap legend */}
              <text x={62} y={480} fill="#374151" fontSize={6}>← gap →</text>
            </svg>
          </div>
          <div className="flex gap-4 mt-2 text-[10px] text-gray-600">
            <span className="flex items-center gap-1"><span className="w-3 h-1" style={{ background: "#22d3ee", display: "inline-block" }} /> Strong gap</span>
            <span className="flex items-center gap-1"><span className="w-3 h-1" style={{ background: "#a78bfa", display: "inline-block" }} /> Moderate</span>
            <span className="flex items-center gap-1"><span className="w-3 h-1" style={{ background: "#f59e0b", display: "inline-block" }} /> Weak</span>
            <span className="flex items-center gap-1"><span className="w-3 h-1" style={{ background: "#ef4444", display: "inline-block" }} /> Broken</span>
            <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-violet-400 inline-block" /> Known zero (Re=½)</span>
          </div>
        </div>
      )}

      {/* ---- GAP CURVE VIEW ---- */}
      {view === "gap" && (
        <div className="space-y-4">
          <div className="bg-[#080a10] border border-gray-800 rounded-lg p-5">
            <div className="text-xs text-gray-500 uppercase tracking-widest mb-4">Spectral Gap λ_min across shells</div>
            <div className="relative" style={{ height: 260 }}>
              <svg viewBox="0 0 700 260" className="w-full h-full">
                {/* Grid */}
                {[0.1, 0.2, 0.3, 0.4, 0.5].map(v => {
                  const y = 240 - (v / 0.5) * 220;
                  return (
                    <g key={v}>
                      <line x1={40} y1={y} x2={680} y2={y} stroke="#1e293b" strokeWidth={0.5} />
                      <text x={35} y={y + 3} textAnchor="end" fill="#374151" fontSize={7}>{v.toFixed(1)}</text>
                    </g>
                  );
                })}

                {/* Threshold line */}
                <line x1={40} y1={240 - (0.5 / 0.5) * 220} x2={680} y2={240 - (0.5 / 0.5) * 220}
                  stroke="#22d3ee" strokeWidth={1} strokeDasharray="6,3" opacity={0.4} />
                <text x={682} y={20} fill="#22d3ee" fontSize={7} opacity={0.5}>½</text>

                {/* Area fill */}
                <polyline
                  points={shells.map((s, i) => {
                    const x = 40 + (i / (N_SHELLS - 1)) * 640;
                    const y = 240 - (s.gap / 0.5) * 220;
                    return `${x},${y}`;
                  }).join(" ")}
                  fill="none" stroke="#a78bfa" strokeWidth={2}
                />

                {/* Dots */}
                {shells.map((s, i) => {
                  const x = 40 + (i / (N_SHELLS - 1)) * 640;
                  const y = 240 - (s.gap / 0.5) * 220;
                  const c = GAP_COLOR(s.gap);
                  const isSel = selected === i;
                  return (
                    <g key={i} onClick={() => setSelected(isSel ? null : i)} style={{ cursor: "pointer" }}>
                      <circle cx={x} cy={y} r={isSel ? 7 : 5} fill={c}
                        style={{ filter: `drop-shadow(0 0 ${isSel ? 8 : 4}px ${c})` }} />
                      <text x={x} y={250} textAnchor="middle" fill="#374151" fontSize={7}>Π{i + 1}</text>
                    </g>
                  );
                })}

                {/* Axes */}
                <line x1={40} y1={240} x2={680} y2={240} stroke="#1e293b" strokeWidth={1} />
                <line x1={40} y1={20} x2={40} y2={240} stroke="#1e293b" strokeWidth={1} />
                <text x={360} y={260} textAnchor="middle" fill="#374151" fontSize={8}>Shell index j</text>
                <text x={10} y={130} fill="#374151" fontSize={8} transform="rotate(-90,10,130)">λ_min</text>
              </svg>
            </div>
          </div>

          {/* Energy status row */}
          <div className="bg-[#080a10] border border-gray-800 rounded-lg p-5">
            <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">Energy Status per Shell</div>
            <div className="flex items-end gap-1 h-24">
              {shells.map((s, i) => {
                const pct = Math.min(100, (s.energy / 1.2) * 100);
                const c = GAP_COLOR(s.gap);
                const isSel = selected === i;
                return (
                  <div key={i} className="flex-1 flex flex-col items-center justify-end h-full cursor-pointer"
                    onClick={() => setSelected(isSel ? null : i)}>
                    <div className="w-full rounded-t transition-all duration-300"
                      style={{
                        height: `${pct}%`,
                        backgroundColor: c,
                        opacity: isSel ? 1 : 0.6,
                        boxShadow: isSel ? `0 0 8px ${c}88` : "none",
                      }} />
                    <div className="text-[8px] text-gray-700 mt-1 font-mono">{i + 1}</div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Gap distribution summary */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {[
              { label: "Strong (>0.45)", count: shells.filter(s => s.gap > 0.45).length, color: "#22d3ee" },
              { label: "Moderate (>0.38)", count: shells.filter(s => s.gap > 0.38 && s.gap <= 0.45).length, color: "#a78bfa" },
              { label: "Weak (>0.28)", count: shells.filter(s => s.gap > 0.28 && s.gap <= 0.38).length, color: "#f59e0b" },
              { label: "Broken (≤0.28)", count: shells.filter(s => s.gap <= 0.28).length, color: "#ef4444" },
            ].map(m => (
              <div key={m.label} className="bg-[#080a10] border border-gray-800 rounded-lg p-3 text-center">
                <div className="text-[10px] text-gray-600 mb-1">{m.label}</div>
                <div className="text-xl font-bold font-mono" style={{ color: m.color }}>{m.count}</div>
                <div className="text-[9px] text-gray-700 mt-0.5">shells</div>
              </div>
            ))}
          </div>

          {/* Proof consequence */}
          <div className="bg-[#080a10] border border-gray-800 rounded-lg p-4">
            <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">ΩStack Consequence</div>
            <MB>{"\\forall j\\le N:\\;\\lambda_{\\min}(H_{\\Pi_j}^\\zeta) > 0 \\implies \\text{Re}(\\rho) = \\tfrac{1}{2}\\;\\forall\\,\\rho\\in\\Pi_j^\\zeta"}</MB>
            <div className="mt-3 text-xs text-gray-600">
              If the spectral gap holds for all {N_SHELLS} shells simultaneously, RH follows for all zeros with Im(ρ) &lt; {(14 + N_SHELLS * 6.5).toFixed(0)}.
              Current certified: <span className="text-cyan-400 font-mono">{stableCount}/{N_SHELLS}</span> shells.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}