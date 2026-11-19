import React, { useState } from "react";
import { MB, ML } from "../qstack/MathBlock";

const NS_SHELLS = Array.from({ length: 12 }, (_, j) => ({
  j: j + 1,
  label: `P_${j + 1}`,
  freq: `2^${j} ≤ |k| < 2^${j + 1}`,
  freqVal: Math.pow(2, j),
  energy: Math.exp(-0.4 * j) * (1 + 0.3 * Math.sin(j * 1.3)),
  role: j === 0 ? "Mean flow" : j < 3 ? "Large scale" : j < 7 ? "Inertial range" : j < 10 ? "Dissipation" : "UV cutoff",
  color: j < 3 ? "#22d3ee" : j < 7 ? "#a78bfa" : j < 10 ? "#f59e0b" : "#ef4444",
  dominant: j === 5,
}));

const RH_SHELLS = Array.from({ length: 10 }, (_, j) => {
  const T0 = 14.135;
  const Tj = T0 + j * 8;
  const zeros = [14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327, 48.005, 49.774];
  const inBand = zeros.filter((z) => z >= Tj && z < Tj + 8);
  return {
    j: j + 1,
    label: `Π_${j + 1}^ζ`,
    band: `Im ∈ [${Tj.toFixed(1)}, ${(Tj + 8).toFixed(1)})`,
    Tj,
    zeros: inBand,
    density: inBand.length / 10,
    color: inBand.length > 1 ? "#a78bfa" : inBand.length === 1 ? "#22d3ee" : "#334155",
    dominant: inBand.length > 1,
  };
});

const ANALOGIES = [
  { ns: "Frequency band 2^j ≤ |k| < 2^{j+1}", rh: "Height band Im(ρ) ∈ [T_j, T_{j+1})" },
  { ns: "Shell energy E_j = ‖P_j u‖²_L²", rh: "Zero density α_j(T) = #{ρ in band}/N(T)" },
  { ns: "Inertial range (j = 4–7)", rh: "GUE-distributed region (Im > 20)" },
  { ns: "Dominant shell j*", rh: "Dominant zero-density band j*" },
  { ns: "Energy cascade P_j → P_{j+1}", rh: "Zero spacing staircase N(T) ~ T log T" },
  { ns: "UV cutoff shell (j = N)", rh: "Truncation height T_N" },
  { ns: "Q6 damps j* when E_{j*} > E_c", rh: "Ω6 repels zeros when α_{j*} > α_c" },
];

function NSShellDiagram({ highlight, setHighlight }) {
  const maxE = Math.max(...NS_SHELLS.map((s) => s.energy));
  return (
    <div className="space-y-2">
      <div className="text-xs text-cyan-500 uppercase tracking-widest mb-3 font-mono">QStack — Frequency Shells</div>
      <div className="text-[10px] text-gray-600 font-mono mb-2">← IR (large scale) · · · UV (small scale) →</div>
      {NS_SHELLS.map((s) => {
        const pct = Math.round((s.energy / maxE) * 100);
        const isHL = highlight === s.j;
        return (
          <div
            key={s.j}
            className={`flex items-center gap-3 cursor-pointer rounded px-2 py-1 transition-all ${isHL ? "bg-white/5" : "hover:bg-white/3"}`}
            onMouseEnter={() => setHighlight(s.j)}
            onMouseLeave={() => setHighlight(null)}
          >
            <div className="w-16 text-right text-[10px] font-mono" style={{ color: s.color }}>
              {s.label}
            </div>
            <div className="flex-1 h-4 bg-gray-900 rounded relative">
              <div
                className="h-full rounded transition-all duration-300"
                style={{ width: `${pct}%`, backgroundColor: s.color, opacity: isHL ? 1 : 0.7, boxShadow: isHL ? `0 0 8px ${s.color}88` : "none" }}
              />
              {s.dominant && (
                <div className="absolute right-1 top-0.5 text-[8px] text-amber-400 font-mono">j*</div>
              )}
            </div>
            <div className="w-28 text-[9px] text-gray-600 font-mono truncate">{s.freq}</div>
            <div className="w-20 text-[9px] font-mono truncate" style={{ color: s.color }}>{s.role}</div>
          </div>
        );
      })}
      {/* Frequency axis */}
      <div className="flex justify-between text-[9px] text-gray-700 font-mono mt-1 px-20">
        <span>2⁰</span><span>2³</span><span>2⁶</span><span>2⁹</span><span>2¹²</span>
      </div>
    </div>
  );
}

function RHShellDiagram({ highlight, setHighlight }) {
  return (
    <div className="space-y-2">
      <div className="text-xs text-violet-500 uppercase tracking-widest mb-3 font-mono">ΩStack — Zero-Density Shells</div>
      <div className="text-[10px] text-gray-600 font-mono mb-2">↑ low Im(t) · · · high Im(t) ↓</div>
      {RH_SHELLS.map((s) => {
        const pct = Math.round((s.density / 0.3) * 100);
        const isHL = highlight === s.j + 100;
        return (
          <div
            key={s.j}
            className={`flex items-center gap-3 cursor-pointer rounded px-2 py-1 transition-all ${isHL ? "bg-white/5" : "hover:bg-white/3"}`}
            onMouseEnter={() => setHighlight(s.j + 100)}
            onMouseLeave={() => setHighlight(null)}
          >
            <div className="w-16 text-right text-[10px] font-mono" style={{ color: s.color }}>
              {s.label}
            </div>
            <div className="flex-1 h-4 bg-gray-900 rounded relative">
              {s.zeros.map((z, i) => (
                <div
                  key={i}
                  className="absolute top-0.5 w-1.5 h-3 rounded-sm"
                  style={{
                    left: `${((z - s.Tj) / 8) * 100}%`,
                    backgroundColor: s.color,
                    boxShadow: isHL ? `0 0 6px ${s.color}` : "none",
                  }}
                />
              ))}
              {s.dominant && (
                <div className="absolute right-1 top-0.5 text-[8px] text-violet-400 font-mono">j*</div>
              )}
            </div>
            <div className="w-28 text-[9px] text-gray-600 font-mono truncate">{s.band}</div>
            <div className="w-20 text-[9px] font-mono" style={{ color: s.color }}>
              {s.zeros.length} zero{s.zeros.length !== 1 ? "s" : ""}
            </div>
          </div>
        );
      })}
      <div className="flex justify-between text-[9px] text-gray-700 font-mono mt-1 px-20">
        <span>Im=14</span><span>Im=30</span><span>Im=50</span><span>Im=66</span><span>Im=82</span>
      </div>
    </div>
  );
}

function CriticalStripMap() {
  const W = 500, H = 280;
  const reToX = (re) => ((re - 0.1) / 0.8) * W;
  const imToY = (im) => H - ((im - 12) / 72) * H;
  const zeros = [14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327, 48.005, 49.774,
    52.970, 56.446, 59.347, 60.832, 65.113, 67.080, 69.546, 72.067, 75.705, 77.145];

  return (
    <div className="bg-[#080a10] border border-gray-800 rounded-lg p-4">
      <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">Critical Strip — Zero Map (first 20 non-trivial zeros)</div>
      <div className="relative overflow-hidden rounded" style={{ width: "100%", paddingBottom: "56%" }}>
        <svg viewBox={`0 0 ${W} ${H}`} className="absolute inset-0 w-full h-full">
          {/* Strip boundary */}
          <rect x={reToX(0)} y={0} width={reToX(1) - reToX(0)} height={H} fill="rgba(255,255,255,0.01)" />
          <line x1={reToX(0)} y1={0} x2={reToX(0)} y2={H} stroke="#374151" strokeWidth={1} />
          <line x1={reToX(1)} y1={0} x2={reToX(1)} y2={H} stroke="#374151" strokeWidth={1} />

          {/* Critical line */}
          <line x1={reToX(0.5)} y1={0} x2={reToX(0.5)} y2={H} stroke="#22d3ee" strokeWidth={1.5} strokeDasharray="6,3" />

          {/* Shell bands */}
          {RH_SHELLS.map((s, i) => {
            const y1 = imToY(s.Tj + 8);
            const y2 = imToY(s.Tj);
            return (
              <rect key={i} x={reToX(0)} y={y1} width={reToX(1) - reToX(0)} height={Math.max(0, y2 - y1)}
                fill={i % 2 === 0 ? "rgba(167,139,250,0.04)" : "rgba(34,211,238,0.03)"}
              />
            );
          })}

          {/* Shell labels */}
          {RH_SHELLS.map((s, i) => {
            const y = imToY(s.Tj + 4);
            return (
              <text key={i} x={reToX(0.12)} y={y} fill="#4b5563" fontSize={7} fontFamily="monospace">
                Π_{i + 1}
              </text>
            );
          })}

          {/* Known zeros on critical line */}
          {zeros.filter((z) => z > 12 && z < 80).map((z, i) => {
            const x = reToX(0.5);
            const y = imToY(z);
            return (
              <g key={i}>
                <line x1={reToX(0)} y1={y} x2={reToX(1)} y2={y} stroke="#1e293b" strokeWidth={0.5} />
                <circle cx={x} cy={y} r={4} fill="#a78bfa" opacity={0.9} />
                <circle cx={x} cy={y} r={7} fill="none" stroke="#a78bfa" strokeWidth={0.5} opacity={0.3} />
                <text x={x + 10} y={y + 3} fill="#6b7280" fontSize={7} fontFamily="monospace">{z.toFixed(3)}</text>
              </g>
            );
          })}

          {/* Labels */}
          <text x={reToX(0.5)} y={H - 4} textAnchor="middle" fill="#22d3ee" fontSize={8} opacity={0.7}>Re(s) = ½</text>
          <text x={reToX(0) + 3} y={12} fill="#374151" fontSize={7}>Re=0</text>
          <text x={reToX(1) - 20} y={12} fill="#374151" fontSize={7}>Re=1</text>
        </svg>
      </div>
      <div className="flex gap-4 mt-2 text-[10px] text-gray-600">
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded-full bg-violet-400 inline-block" /> Known zero (on Re=½)</span>
        <span className="flex items-center gap-1"><span className="w-2 h-1 bg-cyan-400 inline-block opacity-50" /> Critical line</span>
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-violet-900/40 inline-block border border-violet-800" /> Π_j^ζ band</span>
      </div>
    </div>
  );
}

function FrequencySpaceMap() {
  const W = 500, H = 160;
  return (
    <div className="bg-[#080a10] border border-gray-800 rounded-lg p-4">
      <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">Fourier Space — NS Shell Geometry</div>
      <div className="relative overflow-hidden rounded" style={{ width: "100%", paddingBottom: "32%" }}>
        <svg viewBox={`0 0 ${W} ${H}`} className="absolute inset-0 w-full h-full">
          {NS_SHELLS.map((s, i) => {
            const x0 = (i / 12) * W;
            const x1 = ((i + 1) / 12) * W;
            const barH = (s.energy / 1.0) * (H - 40);
            const y = H - 20 - barH;
            return (
              <g key={i}>
                <rect x={x0 + 1} y={y} width={x1 - x0 - 2} height={barH}
                  fill={s.color} opacity={s.dominant ? 1 : 0.6}
                  style={{ filter: s.dominant ? `drop-shadow(0 0 6px ${s.color})` : "none" }}
                />
                <text x={(x0 + x1) / 2} y={H - 6} textAnchor="middle" fill="#4b5563" fontSize={7} fontFamily="monospace">
                  {i + 1}
                </text>
                {s.dominant && (
                  <text x={(x0 + x1) / 2} y={y - 4} textAnchor="middle" fill="#f59e0b" fontSize={8} fontFamily="monospace">j*</text>
                )}
              </g>
            );
          })}
          {/* Axis */}
          <line x1={0} y1={H - 20} x2={W} y2={H - 20} stroke="#1e293b" strokeWidth={1} />
          <text x={2} y={H - 22} fill="#374151" fontSize={7}>E_j</text>
          <text x={W - 60} y={H - 8} fill="#374151" fontSize={7}>shell j →</text>
        </svg>
      </div>
      <div className="flex gap-4 mt-2 text-[10px] text-gray-600">
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-cyan-400 inline-block" /> Large scale</span>
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-violet-400 inline-block" /> Inertial</span>
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-amber-400 inline-block" /> Dissipation</span>
        <span className="flex items-center gap-1"><span className="w-2 h-2 rounded bg-red-500 inline-block" /> UV cutoff</span>
      </div>
    </div>
  );
}

export default function ShellTopologyMap() {
  const [highlight, setHighlight] = useState(null);
  const [view, setView] = useState("side");

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      <div className="mb-4">
        <div className="flex items-center gap-3 mb-2">
          <div className="w-2 h-2 rounded-full bg-cyan-400" />
          <div className="w-2 h-2 rounded-full bg-violet-400" />
          <span className="text-xs text-gray-400 tracking-widest uppercase font-mono">Shell Topology</span>
        </div>
        <h2 className="text-lg font-bold text-white">All Shells — Where They Live</h2>
        <p className="text-xs text-gray-400 mt-1">
          QStack (cyan) = Fourier frequency bands in ℝ³. ΩStack (violet) = horizontal height bands in the critical strip ℂ.
        </p>
      </div>

      {/* View toggle */}
      <div className="flex gap-2">
        {[["side", "Side by Side"], ["maps", "Full Maps"], ["analogy", "Analogy Table"]].map(([id, label]) => (
          <button
            key={id}
            onClick={() => setView(id)}
            className={`px-3 py-1.5 rounded text-xs font-mono tracking-wider uppercase border transition-colors ${view === id ? "border-gray-400 text-gray-200" : "border-gray-700 text-gray-500 hover:border-gray-600"}`}
          >
            {label}
          </button>
        ))}
      </div>

      {view === "side" && (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          <div className="bg-[#0a0c12] border border-cyan-900/40 rounded-lg p-5">
            <NSShellDiagram highlight={highlight} setHighlight={setHighlight} />
          </div>
          <div className="bg-[#0a0c12] border border-violet-900/40 rounded-lg p-5">
            <RHShellDiagram highlight={highlight} setHighlight={setHighlight} />
          </div>
        </div>
      )}

      {view === "maps" && (
        <div className="space-y-6">
          <FrequencySpaceMap />
          <CriticalStripMap />
        </div>
      )}

      {view === "analogy" && (
        <div className="space-y-4">
          {/* Unified shell equation */}
          <div className="bg-[#0a0c12] border border-gray-800 rounded-lg p-5">
            <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">Unified Shell Decomposition</div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <div className="text-xs text-cyan-500 mb-2">QStack: Littlewood–Paley</div>
                <MB>{"u = \\sum_{j=0}^N P_j u,\\quad P_j u = \\mathcal{F}^{-1}[\\hat{u}\\cdot\\mathbf{1}_{2^j\\le|k|<2^{j+1}}]"}</MB>
              </div>
              <div>
                <div className="text-xs text-violet-500 mb-2">ΩStack: Horizontal Band</div>
                <MB>{"\\Pi_j^\\zeta = \\int_{T_j}^{T_{j+1}} |\\phi_t\\rangle\\langle\\phi_t|\\,dt,\\quad T_j = T_0 + j\\Delta"}</MB>
              </div>
            </div>
          </div>

          {/* Analogy table */}
          <div className="bg-[#0a0c12] border border-gray-800 rounded-lg overflow-hidden">
            <div className="grid grid-cols-3 text-[10px] font-bold uppercase tracking-widest border-b border-gray-700">
              <div className="px-4 py-2 text-gray-600">Concept</div>
              <div className="px-4 py-2 text-cyan-600 border-x border-gray-700">QStack (NS)</div>
              <div className="px-4 py-2 text-violet-600">ΩStack (RH)</div>
            </div>
            <div className="divide-y divide-gray-800/60">
              {ANALOGIES.map((row, i) => (
                <div key={i} className="grid grid-cols-3 text-xs hover:bg-white/2 transition-colors">
                  <div className="px-4 py-3 text-gray-500 font-mono text-[10px] border-r border-gray-800/60">{i + 1}</div>
                  <div className="px-4 py-3 text-cyan-400/80 font-mono text-[10px] border-r border-gray-800/60">{row.ns}</div>
                  <div className="px-4 py-3 text-violet-400/80 font-mono text-[10px]">{row.rh}</div>
                </div>
              ))}
            </div>
          </div>

          {/* Key structural difference */}
          <div className="bg-[#0a0c12] border border-amber-800/40 rounded-lg p-5">
            <div className="text-xs text-amber-500 uppercase tracking-widest mb-3">Key Structural Difference</div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-gray-400">
              <div>
                <div className="text-cyan-400 font-semibold mb-2">NS Shells — Spatial Frequency</div>
                <p>Live in <span className="text-cyan-400 font-mono">ℝ³</span> Fourier space. Each band has width factor 2 (dyadic). Energy flows <span className="font-mono">j → j+1</span> via nonlinear cascade. Shells are orthogonal in L².</p>
                <div className="mt-2 font-mono text-[10px] text-gray-600">|k| ∈ [2^j, 2^{"{j+1}"})</div>
              </div>
              <div>
                <div className="text-violet-400 font-semibold mb-2">RH Shells — Height Bands</div>
                <p>Live in <span className="text-violet-400 font-mono">ℂ</span> critical strip. Each band has fixed height Δ. Zeros distribute via <span className="font-mono">N(T) ~ T log T</span>. Bands are orthogonal in H²(strip).</p>
                <div className="mt-2 font-mono text-[10px] text-gray-600">Im(s) ∈ [T_j, T_j + Δ)</div>
              </div>
            </div>
          </div>

          {/* Simplex comparison */}
          <div className="bg-[#0a0c12] border border-gray-800 rounded-lg p-5">
            <div className="text-xs text-gray-500 uppercase tracking-widest mb-3">Simplex Structure (Both Systems)</div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <div className="text-xs text-cyan-500 mb-2">QStack simplex</div>
                <MB>{"a_j[u] = \\frac{\\|P_j u\\|^2_{L^2}}{\\sum_k\\|P_k u\\|^2_{L^2}} \\in \\Delta_N"}</MB>
              </div>
              <div>
                <div className="text-xs text-violet-500 mb-2">ΩStack simplex</div>
                <MB>{"\\alpha_j(T) = \\frac{\\#\\{\\rho\\in\\Pi_j^\\zeta\\}}{N(T)} \\in \\Delta_N^\\zeta"}</MB>
              </div>
            </div>
            <div className="mt-4 text-xs text-gray-600">
              Both simplex coordinates sum to 1. Both must stay in an ℓ¹-tube of radius η around the reference μ for stability to hold.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}