import React, { useState, useMemo, useRef, useEffect } from "react";

const W = 700;
const H = 340;
const PAD = { top: 24, right: 24, bottom: 44, left: 52 };
const PLOT_W = W - PAD.left - PAD.right;
const PLOT_H = H - PAD.top - PAD.bottom;

// Domain: η from 0 to 0.5, λ_min from -0.6 to 0.6
const ETA_MIN = 0, ETA_MAX = 0.5;
const LAM_MIN = -0.6, LAM_MAX = 0.6;

function etaToX(eta) {
  return PAD.left + ((eta - ETA_MIN) / (ETA_MAX - ETA_MIN)) * PLOT_W;
}
function lamToY(lam) {
  return PAD.top + ((LAM_MAX - lam) / (LAM_MAX - LAM_MIN)) * PLOT_H;
}
function xToEta(x) {
  return ETA_MIN + ((x - PAD.left) / PLOT_W) * (ETA_MAX - ETA_MIN);
}

const STEPS = 200;

function buildCurves({ lambdaGap, kappa, alpha, N, a0Spread }) {
  const C_N = 1 + 1 / Math.max(lambdaGap, 0.001);

  const spectralFloor = []; // λ_min vs η after Q6 damping
  const rawFloor = [];      // λ_min vs η without Q6
  const sndBoundary = [];   // SND threshold line: λ = λ_gap - C_N * η

  for (let i = 0; i <= STEPS; i++) {
    const eta = ETA_MIN + (i / STEPS) * (ETA_MAX - ETA_MIN);

    // Raw ℓ¹ deviation (no Q6): worst case = a0Spread * eta
    const l1Raw = Math.min(eta * 1.1, a0Spread + eta * 0.8);

    // Q6-damped ℓ¹ deviation
    const dampFactor = 1 - Math.min(0.95, kappa * Math.pow(Math.max(0, l1Raw - eta / (N * 2)), alpha) * 0.5);
    const l1Damped = l1Raw * dampFactor;

    const lamRaw    = lambdaGap - C_N * l1Raw;
    const lamDamped = lambdaGap - C_N * l1Damped;
    const lamSND    = lambdaGap - C_N * eta; // theoretical SND boundary

    spectralFloor.push({ eta, lam: lamDamped });
    rawFloor.push({ eta, lam: lamRaw });
    sndBoundary.push({ eta, lam: lamSND });
  }

  // Find intersections: where spectralFloor crosses hard floor (-0.5) and SND boundary
  const hardFloorY = -0.5;
  let q6HardCross = null;
  let rawHardCross = null;
  let q6SndCross = null;

  for (let i = 1; i <= STEPS; i++) {
    const prev = spectralFloor[i - 1];
    const curr = spectralFloor[i];
    if (!q6HardCross && prev.lam >= hardFloorY && curr.lam < hardFloorY) {
      const t = (hardFloorY - prev.lam) / (curr.lam - prev.lam);
      q6HardCross = { eta: prev.eta + t * (curr.eta - prev.eta), lam: hardFloorY };
    }
    const prevS = sndBoundary[i - 1];
    const currS = sndBoundary[i];
    const d_prev = prev.lam - prevS.lam;
    const d_curr = curr.lam - currS.lam;
    if (!q6SndCross && d_prev >= 0 && d_curr < 0) {
      const t = d_prev / (d_prev - d_curr);
      q6SndCross = { eta: prev.eta + t * (curr.eta - prev.eta), lam: prev.lam + t * (curr.lam - prev.lam) };
    }

    const rp = rawFloor[i - 1];
    const rc = rawFloor[i];
    if (!rawHardCross && rp.lam >= hardFloorY && rc.lam < hardFloorY) {
      const t = (hardFloorY - rp.lam) / (rc.lam - rp.lam);
      rawHardCross = { eta: rp.eta + t * (rc.eta - rp.eta), lam: hardFloorY };
    }
  }

  return { spectralFloor, rawFloor, sndBoundary, q6HardCross, rawHardCross, q6SndCross, C_N };
}

function toPolyline(pts) {
  return pts
    .filter(p => p.lam >= LAM_MIN - 0.05 && p.lam <= LAM_MAX + 0.05)
    .map(p => `${etaToX(p.eta).toFixed(1)},${lamToY(p.lam).toFixed(1)}`)
    .join(" ");
}

function CrossMarker({ x, y, color, label, sublabel }) {
  return (
    <g>
      <line x1={x - 7} y1={y - 7} x2={x + 7} y2={y + 7} stroke={color} strokeWidth={2} />
      <line x1={x + 7} y1={y - 7} x2={x - 7} y2={y + 7} stroke={color} strokeWidth={2} />
      <circle cx={x} cy={y} r={9} fill="none" stroke={color} strokeWidth={1} opacity={0.5} />
      {label && (
        <g>
          <rect x={x + 11} y={y - 16} width={label.length * 5.8 + 8} height={sublabel ? 28 : 16} rx={3}
            fill="#0a0c12" stroke={color} strokeWidth={0.5} opacity={0.95} />
          <text x={x + 15} y={y - 4} fill={color} fontSize={8} fontFamily="monospace" fontWeight="bold">{label}</text>
          {sublabel && <text x={x + 15} y={y + 8} fill={color} fontSize={7} fontFamily="monospace" opacity={0.7}>{sublabel}</text>}
        </g>
      )}
    </g>
  );
}

export default function SpectralIntersectionGraph() {
  const [lambdaGap, setLambdaGap] = useState(0.30);
  const [kappa,     setKappa]     = useState(0.80);
  const [alpha,     setAlpha]     = useState(1.0);
  const [N,         setN]         = useState(12);
  const [a0Spread,  setA0Spread]  = useState(0.40);
  const [hoverEta,  setHoverEta]  = useState(null);
  const svgRef = useRef(null);

  const { spectralFloor, rawFloor, sndBoundary, q6HardCross, rawHardCross, q6SndCross, C_N } =
    useMemo(() => buildCurves({ lambdaGap, kappa, alpha, N, a0Spread }),
    [lambdaGap, kappa, alpha, N, a0Spread]);

  // Hover probe
  const hoverData = useMemo(() => {
    if (hoverEta === null) return null;
    const idx = Math.round((hoverEta / ETA_MAX) * STEPS);
    const clamped = Math.max(0, Math.min(STEPS, idx));
    return {
      eta: spectralFloor[clamped]?.eta,
      lamQ6: spectralFloor[clamped]?.lam,
      lamRaw: rawFloor[clamped]?.lam,
      lamSND: sndBoundary[clamped]?.lam,
    };
  }, [hoverEta, spectralFloor, rawFloor, sndBoundary]);

  function handleMouseMove(e) {
    const rect = svgRef.current?.getBoundingClientRect();
    if (!rect) return;
    const svgX = ((e.clientX - rect.left) / rect.width) * W;
    const eta = xToEta(svgX);
    if (eta >= ETA_MIN && eta <= ETA_MAX) setHoverEta(eta);
    else setHoverEta(null);
  }

  // Safe region: where Q6 floor > hard floor AND > SND boundary
  const safeRegionPts = spectralFloor
    .filter(p => p.lam > -0.5 && p.lam > (sndBoundary.find(s => Math.abs(s.eta - p.eta) < 0.001)?.lam ?? -99))
    .map(p => `${etaToX(p.eta).toFixed(1)},${lamToY(p.lam).toFixed(1)}`);

  const hardFloorY = lamToY(-0.5);
  const zeroY = lamToY(0);

  return (
    <div className="space-y-5 max-w-5xl mx-auto">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
          <span className="text-xs font-mono uppercase tracking-widest text-gray-400">Spectral Intersection Graph</span>
        </div>
        <h2 className="text-lg font-bold text-white">Q6 Spectral Floor  ×  SND Threshold — Boundary Map</h2>
        <p className="text-xs text-gray-500 mt-1">
          Hover the graph to probe exact values. Intersection markers show where boundaries cross.
        </p>
      </div>

      {/* Main SVG graph */}
      <div className="bg-[#080a10] border border-gray-800 rounded-xl overflow-hidden">
        <svg
          ref={svgRef}
          viewBox={`0 0 ${W} ${H}`}
          className="w-full"
          style={{ height: 340, cursor: "crosshair" }}
          onMouseMove={handleMouseMove}
          onMouseLeave={() => setHoverEta(null)}
        >
          {/* Background zones */}
          {/* Danger zone: below hard floor */}
          <rect x={PAD.left} y={hardFloorY} width={PLOT_W} height={PAD.top + PLOT_H - hardFloorY}
            fill="#ef4444" opacity={0.04} />
          {/* Safe zone: above λ=0 */}
          <rect x={PAD.left} y={PAD.top} width={PLOT_W} height={zeroY - PAD.top}
            fill="#22d3ee" opacity={0.02} />

          {/* Grid lines */}
          {[-0.5, -0.25, 0, 0.25, 0.5].map(v => (
            <g key={v}>
              <line x1={PAD.left} y1={lamToY(v)} x2={W - PAD.right} y2={lamToY(v)}
                stroke={v === -0.5 ? "#ef4444" : v === 0 ? "#334155" : "#1a1f2e"}
                strokeWidth={v === -0.5 ? 1.5 : 1}
                strokeDasharray={v === -0.5 ? "6,3" : v === 0 ? "4,2" : "none"} />
              <text x={PAD.left - 6} y={lamToY(v) + 3} textAnchor="end"
                fill={v === -0.5 ? "#ef4444" : "#374151"} fontSize={8} fontFamily="monospace">
                {v.toFixed(2)}
              </text>
            </g>
          ))}
          {[0.1, 0.2, 0.3, 0.4].map(v => (
            <g key={v}>
              <line x1={etaToX(v)} y1={PAD.top} x2={etaToX(v)} y2={PAD.top + PLOT_H}
                stroke="#1a1f2e" strokeWidth={1} />
              <text x={etaToX(v)} y={PAD.top + PLOT_H + 14} textAnchor="middle"
                fill="#374151" fontSize={8} fontFamily="monospace">{v.toFixed(1)}</text>
            </g>
          ))}

          {/* Axis labels */}
          <text x={PAD.left + PLOT_W / 2} y={H - 4} textAnchor="middle"
            fill="#4b5563" fontSize={9} fontFamily="monospace">η  (SND ℓ¹ threshold)</text>
          <text x={10} y={PAD.top + PLOT_H / 2} textAnchor="middle"
            fill="#4b5563" fontSize={9} fontFamily="monospace"
            transform={`rotate(-90, 10, ${PAD.top + PLOT_H / 2})`}>λ_min</text>

          {/* Hard floor label */}
          <text x={PAD.left + 6} y={hardFloorY - 5} fill="#ef4444" fontSize={8} fontFamily="monospace" opacity={0.8}>
            Hard Floor = −½
          </text>
          <text x={PAD.left + 6} y={zeroY - 5} fill="#22d3ee" fontSize={8} fontFamily="monospace" opacity={0.4}>
            λ = 0
          </text>

          {/* Curves */}
          {/* Raw (no Q6) — dashed gray */}
          <polyline points={toPolyline(rawFloor)}
            fill="none" stroke="#374151" strokeWidth={1.5} strokeDasharray="5,3" opacity={0.7} />

          {/* SND theoretical boundary */}
          <polyline points={toPolyline(sndBoundary)}
            fill="none" stroke="#f59e0b" strokeWidth={1.5} strokeDasharray="4,2" opacity={0.85} />

          {/* Q6 spectral floor — main */}
          <polyline points={toPolyline(spectralFloor)}
            fill="none" stroke="#22d3ee" strokeWidth={2.5} />

          {/* Intersection markers */}
          {rawHardCross && (
            <CrossMarker
              x={etaToX(rawHardCross.eta)} y={lamToY(rawHardCross.lam)}
              color="#ef4444"
              label={`η=${rawHardCross.eta.toFixed(3)}`}
              sublabel="raw floor breach"
            />
          )}
          {q6HardCross && (
            <CrossMarker
              x={etaToX(q6HardCross.eta)} y={lamToY(q6HardCross.lam)}
              color="#f97316"
              label={`η=${q6HardCross.eta.toFixed(3)}`}
              sublabel="Q6 floor breach"
            />
          )}
          {q6SndCross && (
            <CrossMarker
              x={etaToX(q6SndCross.eta)} y={lamToY(q6SndCross.lam)}
              color="#a78bfa"
              label={`η=${q6SndCross.eta.toFixed(3)}`}
              sublabel="Q6 ∩ SND boundary"
            />
          )}

          {/* Hover probe */}
          {hoverData && hoverEta !== null && (
            <g>
              <line x1={etaToX(hoverEta)} y1={PAD.top} x2={etaToX(hoverEta)} y2={PAD.top + PLOT_H}
                stroke="#ffffff" strokeWidth={0.5} opacity={0.2} />
              {/* Q6 dot */}
              <circle cx={etaToX(hoverEta)} cy={lamToY(hoverData.lamQ6)} r={4}
                fill="#22d3ee" stroke="#0a0c12" strokeWidth={1.5} />
              {/* SND dot */}
              <circle cx={etaToX(hoverEta)} cy={lamToY(hoverData.lamSND)} r={4}
                fill="#f59e0b" stroke="#0a0c12" strokeWidth={1.5} />
              {/* Raw dot */}
              <circle cx={etaToX(hoverEta)} cy={lamToY(hoverData.lamRaw)} r={3}
                fill="#374151" stroke="#0a0c12" strokeWidth={1} />

              {/* Tooltip */}
              <g transform={`translate(${Math.min(etaToX(hoverEta) + 10, W - 160)}, ${PAD.top + 8})`}>
                <rect x={0} y={0} width={148} height={72} rx={4}
                  fill="#080a10" stroke="#374151" strokeWidth={0.8} />
                <text x={8} y={14} fill="#6b7280" fontSize={8} fontFamily="monospace">
                  η = {hoverData.eta?.toFixed(4)}
                </text>
                <text x={8} y={28} fill="#22d3ee" fontSize={8} fontFamily="monospace">
                  λ_Q6   = {hoverData.lamQ6?.toFixed(4)}
                </text>
                <text x={8} y={42} fill="#f59e0b" fontSize={8} fontFamily="monospace">
                  λ_SND  = {hoverData.lamSND?.toFixed(4)}
                </text>
                <text x={8} y={56} fill="#374151" fontSize={8} fontFamily="monospace">
                  λ_raw  = {hoverData.lamRaw?.toFixed(4)}
                </text>
                <text x={8} y={68} fill={hoverData.lamQ6 > hoverData.lamSND ? "#22d3ee" : "#ef4444"}
                  fontSize={7} fontFamily="monospace">
                  {hoverData.lamQ6 > hoverData.lamSND ? "Q6 above SND ✓" : "Q6 below SND ✗"}
                </text>
              </g>
            </g>
          )}

          {/* Border */}
          <rect x={PAD.left} y={PAD.top} width={PLOT_W} height={PLOT_H}
            fill="none" stroke="#1e293b" strokeWidth={1} />
        </svg>

        {/* Legend */}
        <div className="flex flex-wrap gap-5 px-5 py-3 border-t border-gray-800 text-[10px] font-mono text-gray-500">
          <span className="flex items-center gap-2">
            <span className="w-6 h-0.5 bg-cyan-400 inline-block" />
            Q6 spectral floor (λ_min after damping)
          </span>
          <span className="flex items-center gap-2">
            <span className="w-6 border-t border-dashed border-amber-400 inline-block" />
            SND theoretical boundary (λ_gap − C_N·η)
          </span>
          <span className="flex items-center gap-2">
            <span className="w-6 border-t border-dashed border-gray-600 inline-block" />
            Raw floor (no Q6)
          </span>
          <span className="flex items-center gap-2">
            <span className="text-violet-400">✕</span> Q6 ∩ SND intersection
          </span>
          <span className="flex items-center gap-2">
            <span className="text-orange-400">✕</span> Q6 hard floor breach
          </span>
          <span className="flex items-center gap-2">
            <span className="text-red-500">✕</span> Raw hard floor breach
          </span>
        </div>
      </div>

      {/* Intersection summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
        <div className="bg-[#0a0c12] border border-violet-900/40 rounded-lg px-4 py-3">
          <div className="text-[9px] text-gray-600 uppercase tracking-widest mb-1">Q6 ∩ SND Boundary</div>
          {q6SndCross
            ? <div className="text-sm font-bold font-mono text-violet-300">η = {q6SndCross.eta.toFixed(4)}</div>
            : <div className="text-sm font-bold font-mono text-gray-600">no intersection</div>}
          <div className="text-[9px] text-gray-600 mt-1">Q6 stays above SND curve left of this point</div>
        </div>
        <div className="bg-[#0a0c12] border border-orange-900/40 rounded-lg px-4 py-3">
          <div className="text-[9px] text-gray-600 uppercase tracking-widest mb-1">Q6 Hard Floor Breach</div>
          {q6HardCross
            ? <div className="text-sm font-bold font-mono text-orange-300">η = {q6HardCross.eta.toFixed(4)}</div>
            : <div className="text-sm font-bold font-mono text-emerald-400">never breached ✓</div>}
          <div className="text-[9px] text-gray-600 mt-1">λ_min = −½ threshold crossing</div>
        </div>
        <div className="bg-[#0a0c12] border border-red-900/40 rounded-lg px-4 py-3">
          <div className="text-[9px] text-gray-600 uppercase tracking-widest mb-1">Raw Floor Breach (no Q6)</div>
          {rawHardCross
            ? <div className="text-sm font-bold font-mono text-red-400">η = {rawHardCross.eta.toFixed(4)}</div>
            : <div className="text-sm font-bold font-mono text-gray-600">no breach</div>}
          <div className="text-[9px] text-gray-600 mt-1">Shows Q6 margin gain vs uncontrolled</div>
        </div>
      </div>

      {/* Controls */}
      <div className="bg-[#0a0c12] border border-gray-800 rounded-xl p-5">
        <div className="text-[10px] text-gray-600 uppercase tracking-widest mb-4">Parameters — drag to see boundaries shift in real time</div>
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
          {[
            { label: "λ_gap  (headroom at μ)", val: lambdaGap, set: setLambdaGap, min: 0.05, max: 1.0,  step: 0.01, color: "accent-violet-400",
              desc: "Eigenvalue gap at reference point. Larger = more room before hard floor." },
            { label: "κ  (Q6 damping strength)", val: kappa, set: setKappa, min: 0.1, max: 3.0, step: 0.05, color: "accent-cyan-400",
              desc: "Higher κ pushes Q6 floor up — intersection moves right." },
            { label: "α  (activation exponent)", val: alpha, set: setAlpha, min: 0.5, max: 3.0, step: 0.1, color: "accent-cyan-400",
              desc: "Nonlinearity of Q6 response. α>1 = harder kick for large deviations." },
            { label: "N  shells", val: N, set: setN, min: 4, max: 20, step: 1, color: "accent-amber-400",
              desc: `C_N = ${C_N.toFixed(3)}. More shells = steeper SND curve = tighter constraint.` },
            { label: "a₀ spread (initial dev)", val: a0Spread, set: setA0Spread, min: 0.05, max: 1.0, step: 0.01, color: "accent-gray-400",
              desc: "Worst-case raw ℓ¹ deviation. Shifts raw floor curve up/down." },
          ].map(p => (
            <div key={p.label}>
              <div className="flex justify-between mb-1">
                <span className="text-[10px] text-gray-400 font-mono">{p.label}</span>
                <span className="text-xs font-bold font-mono text-white">{typeof p.val === 'number' && p.step < 1 ? p.val.toFixed(2) : p.val}</span>
              </div>
              <input type="range" min={p.min} max={p.max} step={p.step} value={p.val}
                onChange={e => p.set(parseFloat(e.target.value))}
                className={`w-full cursor-pointer ${p.color}`} />
              <div className="text-[8px] text-gray-700 mt-1">{p.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}