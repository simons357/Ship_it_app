import React, { useState, useEffect } from "react";
import { base44 } from "@/api/base44Client";

const ROOMS = [
  { id: "simplex",  name: "The Simplex",       color: "#22d3ee" },
  { id: "spectral", name: "The Spectral Floor", color: "#a78bfa" },
  { id: "cascade",  name: "The Cascade",        color: "#f59e0b" },
  { id: "zeros",    name: "The Zero Garden",    color: "#ec4899" },
];

const TYPE_META = {
  artistic:    { label: "Artistic",    color: "#ec4899", bg: "bg-pink-900/20",   border: "border-pink-800/60",   dot: "bg-pink-400" },
  theoretical: { label: "Theoretical", color: "#22d3ee", bg: "bg-cyan-900/20",   border: "border-cyan-800/60",   dot: "bg-cyan-400" },
};

const ACCENT_COLORS = ["#22d3ee", "#a78bfa", "#f59e0b", "#ec4899", "#34d399", "#6366f1"];

export default function CuratePanel({ onClose }) {
  const [collections, setCollections] = useState([]);
  const [creating, setCreating]       = useState(false);
  const [editing, setEditing]         = useState(null); // collection id
  const [form, setForm]               = useState({ title: "", type: "artistic", description: "", rooms: [], color: "#22d3ee" });
  const [loading, setLoading]         = useState(true);

  useEffect(() => { loadCollections(); }, []);

  async function loadCollections() {
    setLoading(true);
    const data = await base44.entities.Collection.list("-created_date", 50);
    setCollections(data);
    setLoading(false);
  }

  function openNew() {
    setForm({ title: "", type: "artistic", description: "", rooms: [], color: "#22d3ee" });
    setEditing(null);
    setCreating(true);
  }

  function openEdit(col) {
    setForm({ title: col.title, type: col.type, description: col.description || "", rooms: col.rooms || [], color: col.color || "#22d3ee" });
    setEditing(col.id);
    setCreating(true);
  }

  async function saveCollection() {
    if (!form.title.trim()) return;
    if (editing) {
      await base44.entities.Collection.update(editing, form);
    } else {
      await base44.entities.Collection.create(form);
    }
    setCreating(false);
    setEditing(null);
    loadCollections();
  }

  async function deleteCollection(id) {
    await base44.entities.Collection.delete(id);
    loadCollections();
  }

  function toggleRoom(id) {
    setForm(f => ({
      ...f,
      rooms: f.rooms.includes(id) ? f.rooms.filter(r => r !== id) : [...f.rooms, id],
    }));
  }

  return (
    <div className="fixed inset-0 z-50 flex items-end md:items-center justify-center bg-black/70 backdrop-blur-sm" onClick={onClose}>
      <div
        className="bg-[#0a0c12] border border-gray-800 rounded-2xl w-full max-w-lg max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={e => e.stopPropagation()}
      >
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-800">
          <div>
            <div className="text-[9px] text-gray-600 uppercase tracking-widest mb-0.5">Curator's Studio</div>
            <h2 className="text-base font-bold text-white font-mono">My Collections</h2>
          </div>
          <button onClick={onClose} className="text-gray-600 hover:text-gray-300 text-xl leading-none">×</button>
        </div>

        <div className="p-6 space-y-5">
          {/* Create/Edit form */}
          {creating ? (
            <div className="space-y-4 bg-[#080a10] border border-gray-800 rounded-xl p-5">
              <div className="text-[10px] text-gray-500 uppercase tracking-widest">
                {editing ? "Edit Collection" : "New Collection"}
              </div>

              {/* Title */}
              <div>
                <label className="text-[9px] text-gray-600 uppercase tracking-widest block mb-1">Show Title</label>
                <input
                  className="w-full bg-[#0a0c12] border border-gray-800 rounded-lg px-3 py-2 text-sm text-white font-mono focus:border-gray-600 outline-none"
                  placeholder="e.g. Spectral Boundaries Vol. I"
                  value={form.title}
                  onChange={e => setForm(f => ({ ...f, title: e.target.value }))}
                />
              </div>

              {/* Type */}
              <div>
                <label className="text-[9px] text-gray-600 uppercase tracking-widest block mb-2">Classification</label>
                <div className="grid grid-cols-2 gap-2">
                  {["artistic", "theoretical"].map(t => {
                    const m = TYPE_META[t];
                    return (
                      <button key={t} onClick={() => setForm(f => ({ ...f, type: t }))}
                        className={`py-3 rounded-lg border text-xs font-mono font-bold uppercase tracking-widest transition-all ${
                          form.type === t ? `${m.bg} ${m.border}` : "border-gray-800 text-gray-600 hover:border-gray-700"
                        }`}
                        style={{ color: form.type === t ? m.color : undefined }}
                      >
                        <div className={`w-1.5 h-1.5 rounded-full ${m.dot} mx-auto mb-1`} />
                        {m.label}
                      </button>
                    );
                  })}
                </div>
              </div>

              {/* Rooms */}
              <div>
                <label className="text-[9px] text-gray-600 uppercase tracking-widest block mb-2">Rooms in this show</label>
                <div className="grid grid-cols-2 gap-2">
                  {ROOMS.map(r => (
                    <button key={r.id} onClick={() => toggleRoom(r.id)}
                      className={`px-3 py-2 rounded-lg border text-[10px] font-mono text-left transition-all ${
                        form.rooms.includes(r.id) ? "border-gray-600 bg-white/5" : "border-gray-800 text-gray-600 hover:border-gray-700"
                      }`}
                      style={{ color: form.rooms.includes(r.id) ? r.color : undefined }}
                    >
                      <div className="flex items-center gap-2">
                        <div className="w-1.5 h-1.5 rounded-full" style={{ backgroundColor: form.rooms.includes(r.id) ? r.color : "#374151" }} />
                        {r.name}
                      </div>
                    </button>
                  ))}
                </div>
              </div>

              {/* Color */}
              <div>
                <label className="text-[9px] text-gray-600 uppercase tracking-widest block mb-2">Accent Color</label>
                <div className="flex gap-2">
                  {ACCENT_COLORS.map(c => (
                    <button key={c} onClick={() => setForm(f => ({ ...f, color: c }))}
                      className="w-6 h-6 rounded-full border-2 transition-all"
                      style={{ backgroundColor: c, borderColor: form.color === c ? "white" : "transparent" }}
                    />
                  ))}
                </div>
              </div>

              {/* Description */}
              <div>
                <label className="text-[9px] text-gray-600 uppercase tracking-widest block mb-1">Curator Notes</label>
                <textarea
                  className="w-full bg-[#0a0c12] border border-gray-800 rounded-lg px-3 py-2 text-xs text-gray-300 font-mono focus:border-gray-600 outline-none resize-none"
                  rows={3}
                  placeholder="What does this show say? What's the thesis?"
                  value={form.description}
                  onChange={e => setForm(f => ({ ...f, description: e.target.value }))}
                />
              </div>

              {/* Actions */}
              <div className="flex gap-3 pt-1">
                <button onClick={saveCollection}
                  className="flex-1 py-2 rounded-lg text-xs font-mono font-bold uppercase tracking-widest transition-all"
                  style={{ backgroundColor: form.color + "22", color: form.color, border: `1px solid ${form.color}44` }}>
                  {editing ? "Save Changes" : "Create Show"}
                </button>
                <button onClick={() => { setCreating(false); setEditing(null); }}
                  className="px-4 py-2 rounded-lg border border-gray-800 text-gray-600 text-xs font-mono hover:border-gray-600 transition-colors">
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <button onClick={openNew}
              className="w-full py-3 border border-dashed border-gray-700 rounded-xl text-xs text-gray-500 font-mono hover:border-gray-500 hover:text-gray-300 transition-all tracking-widest uppercase">
              + New Show / Collection
            </button>
          )}

          {/* Collections list */}
          {loading ? (
            <div className="text-center py-8 text-xs text-gray-700 font-mono">loading…</div>
          ) : collections.length === 0 && !creating ? (
            <div className="text-center py-8 text-xs text-gray-700 font-mono">
              No collections yet. Create your first show above.
            </div>
          ) : (
            <div className="space-y-3">
              {collections.map(col => {
                const tm = TYPE_META[col.type] || TYPE_META.artistic;
                const roomNames = (col.rooms || []).map(rid => ROOMS.find(r => r.id === rid)?.name).filter(Boolean);
                return (
                  <div key={col.id}
                    className="bg-[#080a10] border border-gray-800 rounded-xl p-4 hover:border-gray-700 transition-all">
                    <div className="flex items-start justify-between gap-3">
                      <div className="flex-1 min-w-0">
                        <div className="flex items-center gap-2 mb-1">
                          <div className={`w-1.5 h-1.5 rounded-full flex-shrink-0 ${tm.dot}`} />
                          <span className="text-[8px] uppercase tracking-widest font-mono" style={{ color: tm.color }}>{tm.label}</span>
                        </div>
                        <div className="text-sm font-bold text-white font-mono truncate" style={{ color: col.color || "white" }}>
                          {col.title}
                        </div>
                        {col.description && (
                          <div className="text-[10px] text-gray-600 mt-1 leading-relaxed line-clamp-2">{col.description}</div>
                        )}
                        {roomNames.length > 0 && (
                          <div className="flex flex-wrap gap-1 mt-2">
                            {roomNames.map(n => (
                              <span key={n} className="text-[8px] px-1.5 py-0.5 rounded bg-gray-800 text-gray-500 font-mono">{n}</span>
                            ))}
                          </div>
                        )}
                      </div>
                      <div className="flex gap-1.5 flex-shrink-0">
                        <button onClick={() => openEdit(col)}
                          className="text-[9px] px-2 py-1 rounded border border-gray-800 text-gray-600 hover:border-gray-600 hover:text-gray-300 transition-colors font-mono">
                          Edit
                        </button>
                        <button onClick={() => deleteCollection(col.id)}
                          className="text-[9px] px-2 py-1 rounded border border-gray-800 text-gray-700 hover:border-rose-800 hover:text-rose-500 transition-colors font-mono">
                          ×
                        </button>
                      </div>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}