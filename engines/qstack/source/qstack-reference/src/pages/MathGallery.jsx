import React, { useState, useEffect, useRef } from "react";
import { Link } from "react-router-dom";
import EntangledRoom from "../components/gallery/EntangledRoom";
import SoloRoom from "../components/gallery/SoloRoom";
import CuratePanel from "../components/gallery/CuratePanel";

const ROOMS = [
  {
    id: "simplex",
    name: "The Simplex",
    subtitle: "Room I",
    color: "#22d3ee",
    partner: "spectral",
    description: "Energy lives on a simplex. Every painting here has a twin in The Spectral Room. Touch one — watch the other breathe.",
  },
  {
    id: "spectral",
    name: "The Spectral Floor",
    subtitle: "Room II",
    color: "#a78bfa",
    partner: "simplex",
    description: "The eigenvalue boundary. The floor below which reality collapses. Entangled with The Simplex.",
  },
  {
    id: "cascade",
    name: "The Cascade",
    subtitle: "Room III",
    color: "#f59e0b",
    partner: null,
    description: "Energy flowing from large scales to small. The inertial range. Turbulence made visible.",
  },
  {
    id: "zeros",
    name: "The Zero Garden",
    subtitle: "Room IV",
    color: "#ec4899",
    partner: null,
    description: "Every zero of the Riemann zeta function. On the critical line. A garden that may never end.",
  },
];

export default function MathGallery() {
  const [activeRoom, setActiveRoom] = useState(null);
  const [showCurate, setShowCurate] = useState(false);
  const [entanglementState, setEntanglementState] = useState({
    phase: 0, pulse: 0, drift: 0, intensity: 0.5,
  });

  // Global entanglement engine — drives both entangled rooms
  useEffect(() => {
    let raf;
    let t = 0;
    function tick() {
      t += 0.008;
      setEntanglementState({
        phase: t,
        pulse: Math.sin(t * 1.3) * 0.5 + 0.5,
        drift: Math.sin(t * 0.7) * 0.3,
        intensity: Math.abs(Math.sin(t * 0.4)) * 0.6 + 0.4,
      });
      raf = requestAnimationFrame(tick);
    }
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, []);

  if (activeRoom) {
    const room = ROOMS.find(r => r.id === activeRoom);
    const partnerRoom = room.partner ? ROOMS.find(r => r.id === room.partner) : null;

    if (partnerRoom) {
      return (
        <EntangledRoom
          room={room}
          partner={partnerRoom}
          entanglementState={entanglementState}
          onExit={() => setActiveRoom(null)}
        />
      );
    }
    return (
      <SoloRoom
        room={room}
        entanglementState={entanglementState}
        onExit={() => setActiveRoom(null)}
      />
    );
  }

  return (
    <div className="min-h-screen bg-[#06080e] text-gray-100 font-mono">
      {/* Header */}
      <header className="px-8 py-10 border-b border-gray-900 text-center relative">
        <Link to="/" className="absolute left-6 top-6 text-[10px] text-gray-600 hover:text-gray-400 tracking-widest uppercase transition-colors">
          ← QStack
        </Link>
        <div className="absolute right-6 top-6 flex gap-2">
          <button onClick={() => setShowCurate(true)} className="text-[10px] px-3 py-1.5 rounded border border-pink-800 text-pink-400 hover:bg-pink-900/20 tracking-widest uppercase transition-colors font-mono">
            Curate ✦
          </button>
          <Link to="/explorer" className="text-[10px] px-3 py-1.5 rounded border border-cyan-800 text-cyan-500 hover:bg-cyan-900/20 tracking-widest uppercase transition-colors font-mono">
            3D →
          </Link>
        </div>
        <div className="text-[10px] text-gray-600 tracking-[0.4em] uppercase mb-3">Mathematical Art Gallery</div>
        <h1 className="text-4xl font-bold text-white tracking-tight">
          Structures of the <span className="text-cyan-400">Invisible</span>
        </h1>
        <p className="text-sm text-gray-500 mt-4 max-w-xl mx-auto leading-relaxed">
          These are not metaphors. The shapes you are about to see are the actual mathematical objects
          that govern turbulence, prime numbers, and the fabric of continuity.
          Enter a room. Let your eyes do the thinking first.
        </p>
        <div className="flex items-center justify-center gap-2 mt-6">
          <div className="w-1.5 h-1.5 rounded-full bg-cyan-400 animate-pulse" />
          <span className="text-[10px] text-cyan-600 tracking-widest">
            Rooms I & II are quantum entangled — what happens in one, happens in the other
          </span>
          <div className="w-1.5 h-1.5 rounded-full bg-violet-400 animate-pulse" style={{ animationDelay: "0.5s" }} />
        </div>
      </header>

      {showCurate && <CuratePanel onClose={() => setShowCurate(false)} />}

      {/* Gallery floor */}
      <main className="max-w-6xl mx-auto px-6 py-16">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {ROOMS.map((room, i) => (
            <RoomDoor
              key={room.id}
              room={room}
              index={i}
              entanglementState={entanglementState}
              onEnter={() => setActiveRoom(room.id)}
            />
          ))}
        </div>

        {/* Floor text */}
        <div className="mt-20 text-center space-y-4">
          <div className="text-[10px] text-gray-700 tracking-widest uppercase">A note on entanglement</div>
          <p className="text-xs text-gray-600 max-w-2xl mx-auto leading-loose">
            In quantum mechanics, two entangled particles share a state — measuring one instantly determines the other,
            regardless of distance. Here, the Simplex and the Spectral Floor are mathematically entangled:
            the energy distribution <span className="text-cyan-500">a_j</span> lives on the simplex,
            and the spectral gap <span className="text-violet-400">λ_min</span> is a function of it.
            They are not two things. They are one thing, seen from two rooms.
          </p>
        </div>
      </main>
    </div>
  );
}

function RoomDoor({ room, index, entanglementState, onEnter }) {
  const canvasRef = useRef(null);
  const { phase, pulse, drift, intensity } = entanglementState;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const W = canvas.width, H = canvas.height;
    ctx.clearRect(0, 0, W, H);

    if (room.id === "simplex") drawSimplexPreview(ctx, W, H, phase, pulse);
    if (room.id === "spectral") drawSpectralPreview(ctx, W, H, phase, pulse, drift);
    if (room.id === "cascade") drawCascadePreview(ctx, W, H, phase);
    if (room.id === "zeros") drawZerosPreview(ctx, W, H, phase, pulse);
  }, [phase, pulse, drift, intensity, room.id]);

  return (
    <button
      onClick={onEnter}
      className="group relative rounded-2xl overflow-hidden border border-gray-800 hover:border-gray-600 transition-all duration-500 text-left"
      style={{ background: "#0a0c12" }}
    >
      {/* Live canvas preview */}
      <div className="relative" style={{ height: 220 }}>
        <canvas
          ref={canvasRef}
          width={600} height={220}
          className="w-full h-full"
          style={{ display: "block" }}
        />
        {/* Entangled badge */}
        {room.partner && (
          <div className="absolute top-3 right-3 flex items-center gap-1.5 bg-black/60 backdrop-blur-sm rounded-full px-2 py-1 border border-violet-800/60">
            <div className="w-1.5 h-1.5 rounded-full bg-violet-400 animate-pulse" />
            <span className="text-[8px] text-violet-400 tracking-widest uppercase">Entangled</span>
          </div>
        )}
        {/* Hover overlay */}
        <div className="absolute inset-0 bg-black/0 group-hover:bg-black/20 transition-all duration-300 flex items-center justify-center">
          <div className="opacity-0 group-hover:opacity-100 transition-all duration-300 text-white text-xs tracking-widest uppercase border border-white/30 px-4 py-2 rounded-full backdrop-blur-sm">
            Enter Room
          </div>
        </div>
      </div>

      {/* Room info */}
      <div className="px-5 py-4 border-t border-gray-800/60">
        <div className="flex items-start justify-between">
          <div>
            <div className="text-[9px] tracking-widest uppercase mb-1" style={{ color: room.color }}>{room.subtitle}</div>
            <div className="text-base font-bold text-white">{room.name}</div>
          </div>
          <div className="text-gray-700 group-hover:text-gray-400 transition-colors text-lg mt-1">→</div>
        </div>
        <p className="text-[11px] text-gray-500 mt-2 leading-relaxed">{room.description}</p>
      </div>
    </button>
  );
}

// ── Preview painters ──────────────────────────────────────────────

function drawSimplexPreview(ctx, W, H, phase, pulse) {
  ctx.clearRect(0, 0, W, H);
  const N = 12;
  const cx = W / 2, cy = H / 2;
  // Draw simplex as animated shell bars
  for (let j = 0; j < N; j++) {
    const a = Math.exp(-0.35 * j) * (0.6 + 0.2 * Math.sin(phase * 1.1 + j * 0.8));
    const x = (j / N) * W;
    const barW = (W / N) - 3;
    const barH = a * (H * 0.7);
    const alpha = 0.5 + pulse * 0.4;
    ctx.fillStyle = `rgba(34, 211, 238, ${alpha * (1 - j / N * 0.6)})`;
    ctx.beginPath();
    ctx.roundRect(x + 2, H - barH - 20, barW, barH, 3);
    ctx.fill();
  }
  // Simplex boundary line
  ctx.strokeStyle = `rgba(34, 211, 238, ${0.2 + pulse * 0.3})`;
  ctx.lineWidth = 1;
  ctx.setLineDash([4, 4]);
  ctx.beginPath();
  ctx.moveTo(0, H - 20); ctx.lineTo(W, H - 20);
  ctx.stroke();
  ctx.setLineDash([]);
}

function drawSpectralPreview(ctx, W, H, phase, pulse, drift) {
  ctx.clearRect(0, 0, W, H);
  // Draw λ_min curve reacting to drift
  const points = [];
  for (let i = 0; i <= 100; i++) {
    const x = (i / 100) * W;
    const eta = i / 100 * 0.5;
    const lam = 0.3 - 1.5 * eta + drift * 0.3 + Math.sin(phase + i * 0.1) * 0.04;
    const y = H / 2 - lam * H * 0.7;
    points.push([x, y]);
  }
  // Fill under/over hard floor
  const floorY = H / 2 + 0.5 * H * 0.7;
  ctx.beginPath();
  ctx.moveTo(0, floorY);
  points.forEach(([x, y]) => ctx.lineTo(x, Math.min(y, floorY)));
  ctx.lineTo(W, floorY);
  ctx.closePath();
  ctx.fillStyle = `rgba(167, 139, 250, ${0.08 + pulse * 0.06})`;
  ctx.fill();

  // Hard floor
  ctx.strokeStyle = `rgba(239, 68, 68, ${0.5 + pulse * 0.3})`;
  ctx.lineWidth = 1.5;
  ctx.setLineDash([6, 3]);
  ctx.beginPath();
  ctx.moveTo(0, floorY); ctx.lineTo(W, floorY);
  ctx.stroke();
  ctx.setLineDash([]);

  // λ_min curve
  ctx.strokeStyle = `rgba(167, 139, 250, ${0.7 + pulse * 0.3})`;
  ctx.lineWidth = 2;
  ctx.beginPath();
  points.forEach(([x, y], i) => i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y));
  ctx.stroke();
}

function drawCascadePreview(ctx, W, H, phase) {
  ctx.clearRect(0, 0, W, H);
  const N = 10;
  for (let j = 0; j < N; j++) {
    const scale = Math.pow(0.65, j);
    const x = W * 0.1 + j * (W * 0.08);
    const energy = scale * (0.8 + 0.2 * Math.sin(phase * (1 + j * 0.3)));
    const barH = energy * H * 0.6;
    const col = j < 3 ? [34, 211, 238] : j < 7 ? [167, 139, 250] : [245, 158, 11];
    ctx.fillStyle = `rgba(${col[0]}, ${col[1]}, ${col[2]}, 0.7)`;
    ctx.beginPath();
    ctx.roundRect(x, H - barH - 20, W * 0.06, barH, 2);
    ctx.fill();
    // Flow arrow
    if (j < N - 1) {
      ctx.strokeStyle = `rgba(${col[0]}, ${col[1]}, ${col[2]}, 0.3)`;
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.moveTo(x + W * 0.06, H - barH / 2 - 20);
      ctx.lineTo(x + W * 0.08, H - barH / 2 - 20);
      ctx.stroke();
    }
  }
  ctx.fillStyle = "rgba(245, 158, 11, 0.4)";
  ctx.font = "9px monospace";
  ctx.fillText("E ~ k^{-5/3}", W - 90, H - 8);
}

function drawZerosPreview(ctx, W, H, phase, pulse) {
  ctx.clearRect(0, 0, W, H);
  const zeros = [14.135, 21.022, 25.011, 30.425, 32.935, 37.586, 40.919, 43.327, 48.005, 49.774];
  const maxT = 55;
  // Critical line
  const cx = W / 2;
  ctx.strokeStyle = "rgba(34, 211, 238, 0.3)";
  ctx.lineWidth = 1;
  ctx.setLineDash([4, 3]);
  ctx.beginPath(); ctx.moveTo(cx, 0); ctx.lineTo(cx, H); ctx.stroke();
  ctx.setLineDash([]);

  zeros.forEach((t, i) => {
    const y = (t / maxT) * (H - 30) + 15;
    const glow = 0.5 + 0.5 * Math.sin(phase * 0.8 + i * 1.3);
    ctx.beginPath();
    ctx.arc(cx, y, 5 + glow * 3, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(236, 72, 153, ${0.4 + glow * 0.5})`;
    ctx.fill();
    ctx.strokeStyle = `rgba(236, 72, 153, ${0.2 + glow * 0.3})`;
    ctx.lineWidth = 1;
    ctx.stroke();
    // Re=0 and Re=1 strip edges
    ctx.strokeStyle = "rgba(55, 65, 81, 0.4)";
    ctx.lineWidth = 0.5;
    ctx.beginPath(); ctx.moveTo(cx - 120, y); ctx.lineTo(cx + 120, y); ctx.stroke();
    ctx.fillStyle = "rgba(107, 114, 128, 0.6)";
    ctx.font = "7px monospace";
    ctx.fillText(t.toFixed(3), cx + 12, y + 3);
  });
}