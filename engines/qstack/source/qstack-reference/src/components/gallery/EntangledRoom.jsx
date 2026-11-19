import React, { useEffect, useRef, useState } from "react";

// The two entangled paintings side by side — touch one, the other reacts instantly

export default function EntangledRoom({ room, partner, entanglementState, onExit }) {
  const [touched, setTouched] = useState(null); // "left" | "right" | null
  const [touchPos, setTouchPos] = useState({ x: 0.5, y: 0.5 });
  const leftRef = useRef(null);
  const rightRef = useRef(null);
  const { phase, pulse, drift, intensity } = entanglementState;

  // Paint both canvases every frame
  useEffect(() => {
    paintSimplexCanvas(leftRef.current, phase, pulse, drift, touched, touchPos, touched === "right");
    paintSpectralCanvas(rightRef.current, phase, pulse, drift, touched, touchPos, touched === "left");
  }, [phase, pulse, drift, touched, touchPos]);

  function handleMouse(side, e) {
    const canvas = side === "left" ? leftRef.current : rightRef.current;
    if (!canvas) return;
    const rect = canvas.getBoundingClientRect();
    const x = (e.clientX - rect.left) / rect.width;
    const y = (e.clientY - rect.top) / rect.height;
    setTouched(side);
    setTouchPos({ x, y });
  }

  return (
    <div className="min-h-screen bg-[#04050a] font-mono flex flex-col">
      {/* Room header */}
      <div className="flex items-center justify-between px-8 py-5 border-b border-gray-900">
        <button onClick={onExit}
          className="text-[10px] text-gray-600 hover:text-gray-300 tracking-widest uppercase transition-colors">
          ← Gallery
        </button>
        <div className="text-center">
          <div className="text-[9px] text-violet-500 tracking-[0.4em] uppercase">Entangled Exhibition</div>
          <div className="text-white text-sm font-bold mt-0.5">{room.name}  ×  {partner.name}</div>
        </div>
        <div className="flex items-center gap-2">
          <div className="w-1.5 h-1.5 rounded-full bg-violet-400 animate-pulse" />
          <span className="text-[9px] text-violet-500">Live entanglement active</span>
        </div>
      </div>

      {/* Entanglement explanation strip */}
      <div className="px-8 py-3 bg-[#07090f] border-b border-gray-900/60 text-center">
        <p className="text-[11px] text-gray-500 max-w-3xl mx-auto">
          Move your cursor over either painting. The other responds — not as a copy, but as its
          <span className="text-violet-400"> mathematical conjugate</span>. The simplex coordinate
          <span className="text-cyan-400"> a_j</span> and the spectral eigenvalue
          <span className="text-violet-400"> λ_min</span> are one object seen from two sides.
        </p>
      </div>

      {/* Twin paintings */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-2 gap-0">
        {/* Left — Simplex */}
        <div className="relative border-r border-gray-900"
          onMouseMove={e => handleMouse("left", e)}
          onMouseLeave={() => setTouched(null)}>
          <canvas
            ref={leftRef}
            width={700} height={500}
            className="w-full h-full"
            style={{ display: "block", minHeight: 400, cursor: "crosshair" }}
          />
          <PaintingLabel
            title="The Simplex"
            subtitle="Energy distribution a_j ∈ Δ_N"
            color={room.color}
            side="left"
            active={touched === "left"}
            reaction={touched === "right"}
          />
        </div>

        {/* Right — Spectral */}
        <div className="relative"
          onMouseMove={e => handleMouse("right", e)}
          onMouseLeave={() => setTouched(null)}>
          <canvas
            ref={rightRef}
            width={700} height={500}
            className="w-full h-full"
            style={{ display: "block", minHeight: 400, cursor: "crosshair" }}
          />
          <PaintingLabel
            title="The Spectral Floor"
            subtitle="λ_min(H_N[a]) — eigenvalue boundary"
            color={partner.color}
            side="right"
            active={touched === "right"}
            reaction={touched === "left"}
          />
        </div>
      </div>

      {/* Live readout */}
      <div className="px-8 py-4 border-t border-gray-900 grid grid-cols-2 md:grid-cols-4 gap-4 bg-[#06080e]">
        {[
          { label: "phase", val: phase.toFixed(3), color: "text-gray-400" },
          { label: "simplex pulse", val: pulse.toFixed(3), color: "text-cyan-400" },
          { label: "spectral drift", val: drift.toFixed(3), color: "text-violet-400" },
          { label: "entanglement", val: touched ? `from ${touched}` : "passive", color: "text-pink-400" },
        ].map(m => (
          <div key={m.label} className="text-center">
            <div className="text-[9px] text-gray-700 uppercase tracking-widest">{m.label}</div>
            <div className={`text-sm font-bold font-mono mt-0.5 ${m.color}`}>{m.val}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function PaintingLabel({ title, subtitle, color, side, active, reaction }) {
  return (
    <div className={`absolute bottom-0 ${side === "left" ? "left-0" : "right-0"} p-4`}>
      <div className={`inline-block bg-black/70 backdrop-blur-sm rounded-lg px-4 py-2 border transition-all duration-300
        ${active ? "border-opacity-100" : reaction ? "border-opacity-60" : "border-opacity-20"}
      `} style={{ borderColor: color }}>
        <div className="text-xs font-bold" style={{ color }}>{title}</div>
        <div className="text-[9px] text-gray-500 font-mono mt-0.5">{subtitle}</div>
        {reaction && (
          <div className="text-[8px] text-violet-400 mt-1 animate-pulse">⟵ reacting to twin</div>
        )}
        {active && (
          <div className="text-[8px] mt-1" style={{ color }}>● you are here</div>
        )}
      </div>
    </div>
  );
}

// ── Simplex painter ────────────────────────────────────────────────
function paintSimplexCanvas(canvas, phase, pulse, drift, touched, touchPos, isReacting) {
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height;
  ctx.clearRect(0, 0, W, H);

  // Deep space background
  const bg = ctx.createRadialGradient(W / 2, H / 2, 0, W / 2, H / 2, W * 0.8);
  bg.addColorStop(0, "#0a0f1e");
  bg.addColorStop(1, "#04050a");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, W, H);

  const N = 14;
  const tx = isReacting ? touchPos.x : (touched === "left" ? touchPos.x : 0.5);
  const ty = isReacting ? touchPos.y : (touched === "left" ? touchPos.y : 0.5);
  const reactStrength = isReacting ? 0.7 : (touched === "left" ? 1.0 : 0);

  // Shell bars
  for (let j = 0; j < N; j++) {
    const base = Math.exp(-0.35 * j);
    const perturbation = reactStrength * 0.4 * Math.exp(-3 * Math.pow(j / N - tx, 2)) * (1 - ty);
    const a = base * (0.7 + 0.25 * Math.sin(phase * (1 + j * 0.15) + j)) + perturbation;
    const barW = (W / N) - 4;
    const barH = a * H * 0.65;
    const x = (j / N) * W + 2;
    const y = H - barH - 30;

    // Glow
    const grd = ctx.createLinearGradient(x, y, x, H - 30);
    const cyan_a = 0.3 + pulse * 0.4 + perturbation * 0.5;
    grd.addColorStop(0, `rgba(34, 211, 238, ${cyan_a})`);
    grd.addColorStop(1, `rgba(6, 182, 212, ${cyan_a * 0.3})`);
    ctx.fillStyle = grd;
    ctx.beginPath();
    ctx.roundRect(x, y, barW, barH, 3);
    ctx.fill();

    // Top highlight
    ctx.fillStyle = `rgba(200, 245, 255, ${0.2 + pulse * 0.3})`;
    ctx.beginPath();
    ctx.roundRect(x + barW * 0.2, y, barW * 0.6, 3, 1);
    ctx.fill();
  }

  // Simplex floor line
  ctx.strokeStyle = `rgba(34, 211, 238, ${0.15 + pulse * 0.2})`;
  ctx.lineWidth = 1;
  ctx.setLineDash([6, 4]);
  ctx.beginPath();
  ctx.moveTo(0, H - 30);
  ctx.lineTo(W, H - 30);
  ctx.stroke();
  ctx.setLineDash([]);

  // Touch ripple
  if (touched === "left" && touchPos) {
    const rx = touchPos.x * W, ry = touchPos.y * H;
    for (let r = 0; r < 3; r++) {
      const rad = (r + 1) * 30 + (phase * 20 % 30);
      ctx.beginPath();
      ctx.arc(rx, ry, rad, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(34, 211, 238, ${0.3 - r * 0.08})`;
      ctx.lineWidth = 1;
      ctx.stroke();
    }
  }

  // Entanglement reaction ripple (from partner)
  if (isReacting) {
    const rx = touchPos.x * W, ry = touchPos.y * H;
    for (let r = 0; r < 3; r++) {
      const rad = (r + 1) * 25 + (phase * 15 % 25);
      ctx.beginPath();
      ctx.arc(rx, ry, rad, 0, Math.PI * 2);
      ctx.strokeStyle = `rgba(167, 139, 250, ${0.2 - r * 0.06})`;
      ctx.lineWidth = 0.8;
      ctx.stroke();
    }
  }

  // Labels
  ctx.fillStyle = "rgba(34, 211, 238, 0.4)";
  ctx.font = "bold 11px monospace";
  ctx.fillText("Δ_N", 16, 24);
  ctx.fillStyle = "rgba(100, 150, 180, 0.3)";
  ctx.font = "9px monospace";
  ctx.fillText("a_j = ‖P_j u‖² / Σ‖P_k u‖²", 16, 40);
}

// ── Spectral painter ───────────────────────────────────────────────
function paintSpectralCanvas(canvas, phase, pulse, drift, touched, touchPos, isReacting) {
  if (!canvas) return;
  const ctx = canvas.getContext("2d");
  const W = canvas.width, H = canvas.height;
  ctx.clearRect(0, 0, W, H);

  const bg = ctx.createRadialGradient(W / 2, H * 0.6, 0, W / 2, H * 0.6, W * 0.9);
  bg.addColorStop(0, "#0f0a1e");
  bg.addColorStop(1, "#04050a");
  ctx.fillStyle = bg;
  ctx.fillRect(0, 0, W, H);

  const tx = isReacting ? touchPos.x : (touched === "right" ? touchPos.x : 0.5);
  const ty = isReacting ? touchPos.y : (touched === "right" ? touchPos.y : 0.5);
  const reactStrength = isReacting ? 0.8 : (touched === "right" ? 1.0 : 0);

  const STEPS = 120;
  const lamGap = 0.32;
  const C_N = 1 + 1 / lamGap;

  // Build λ_min curve
  const pts = [];
  for (let i = 0; i <= STEPS; i++) {
    const eta = (i / STEPS) * 0.5;
    const perturbEta = reactStrength * 0.12 * Math.exp(-6 * Math.pow(i / STEPS - tx, 2));
    const l1Dev = eta * 0.8 + 0.05 * Math.sin(phase + i * 0.15) + perturbEta;
    const lam = lamGap - C_N * l1Dev;
    const x = (i / STEPS) * W;
    const y = H * 0.5 - lam * H * 0.55;
    pts.push([x, y]);
  }

  const hardFloorY = H * 0.5 + 0.5 * H * 0.55;

  // Danger zone fill
  ctx.beginPath();
  ctx.moveTo(0, hardFloorY);
  pts.forEach(([x, y]) => ctx.lineTo(x, Math.max(y, hardFloorY)));
  ctx.lineTo(W, H);
  ctx.lineTo(0, H);
  ctx.closePath();
  ctx.fillStyle = `rgba(239, 68, 68, ${0.04 + pulse * 0.03})`;
  ctx.fill();

  // Safe zone fill above curve
  ctx.beginPath();
  ctx.moveTo(0, pts[0][1]);
  pts.forEach(([x, y]) => ctx.lineTo(x, y));
  ctx.lineTo(W, 0);
  ctx.lineTo(0, 0);
  ctx.closePath();
  ctx.fillStyle = `rgba(167, 139, 250, ${0.04 + pulse * 0.02})`;
  ctx.fill();

  // Hard floor
  ctx.strokeStyle = `rgba(239, 68, 68, ${0.5 + pulse * 0.4})`;
  ctx.lineWidth = 1.5;
  ctx.setLineDash([8, 4]);
  ctx.beginPath();
  ctx.moveTo(0, hardFloorY);
  ctx.lineTo(W, hardFloorY);
  ctx.stroke();
  ctx.setLineDash([]);

  // λ=0 line
  ctx.strokeStyle = "rgba(55, 65, 81, 0.4)";
  ctx.lineWidth = 1;
  ctx.setLineDash([4, 3]);
  ctx.beginPath();
  ctx.moveTo(0, H * 0.5);
  ctx.lineTo(W, H * 0.5);
  ctx.stroke();
  ctx.setLineDash([]);

  // λ_min curve glow
  ctx.shadowBlur = 12;
  ctx.shadowColor = "rgba(167, 139, 250, 0.6)";
  ctx.strokeStyle = `rgba(167, 139, 250, ${0.7 + pulse * 0.25})`;
  ctx.lineWidth = 2.5;
  ctx.beginPath();
  pts.forEach(([x, y], i) => i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y));
  ctx.stroke();
  ctx.shadowBlur = 0;

  // Touch probe
  if ((touched === "right" || isReacting) && touchPos) {
    const px = tx * W;
    ctx.strokeStyle = `rgba(167, 139, 250, ${isReacting ? 0.3 : 0.5})`;
    ctx.lineWidth = 1;
    ctx.setLineDash([3, 3]);
    ctx.beginPath();
    ctx.moveTo(px, 0);
    ctx.lineTo(px, H);
    ctx.stroke();
    ctx.setLineDash([]);
  }

  // Hard floor label
  ctx.fillStyle = `rgba(239, 68, 68, ${0.5 + pulse * 0.3})`;
  ctx.font = "10px monospace";
  ctx.fillText("Hard Floor  λ = −½", 12, hardFloorY - 8);

  // Labels
  ctx.fillStyle = "rgba(167, 139, 250, 0.4)";
  ctx.font = "bold 11px monospace";
  ctx.fillText("λ_min(H_N[a])", 16, 24);
  ctx.fillStyle = "rgba(120, 100, 180, 0.3)";
  ctx.font = "9px monospace";
  ctx.fillText("spectral gap — must stay above −½", 16, 40);
}