import React, { useState } from "react";
import { motion } from "framer-motion";
import { Mail, Check, Clock, AlertCircle, Plus, Trash2, Edit } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";

const defaultEndorsers = [
  {
    id: 1,
    name: "George Seregin",
    affiliation: "Oxford University",
    email: "seregin@maths.ox.ac.uk",
    field: "math.AP",
    status: "pending",
    notes: "Theorem B: Φ-renormalization — hook for engagement",
    dateAdded: "2026-04-18",
    lastContact: null,
  },
  {
    id: 2,
    name: "James Robinson",
    affiliation: "University of Warwick",
    email: "j.c.robinson@warwick.ac.uk",
    field: "math.AP",
    status: "pending",
    notes: "Global regularity expertise",
    dateAdded: "2026-04-18",
    lastContact: null,
  },
  {
    id: 3,
    name: "Vladimír Šverák",
    affiliation: "University of Minnesota",
    email: "sverak@umn.edu",
    field: "math.AP",
    status: "pending",
    notes: "Navier–Stokes regularity — natural fit",
    dateAdded: "2026-04-18",
    lastContact: null,
  },
];

const statusConfig = {
  pending: { icon: Clock, color: "text-accent", bg: "bg-accent/10", label: "Pending" },
  contacted: { icon: Mail, color: "text-primary", bg: "bg-primary/10", label: "Contacted" },
  endorsed: { icon: Check, color: "text-chart-1", bg: "bg-chart-1/10", label: "Endorsed" },
  declined: { icon: AlertCircle, color: "text-destructive", bg: "bg-destructive/10", label: "Declined" },
};

export default function EndorsementTracker() {
  const [endorsers, setEndorsers] = useState(defaultEndorsers);
  const [showForm, setShowForm] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [formData, setFormData] = useState({
    name: "",
    affiliation: "",
    email: "",
    field: "math.AP",
    notes: "",
  });

  const handleAddEndorser = () => {
    if (formData.name && formData.email) {
      if (editingId) {
        setEndorsers((prev) =>
          prev.map((e) =>
            e.id === editingId ? { ...e, ...formData } : e
          )
        );
        setEditingId(null);
      } else {
        setEndorsers((prev) => [
          ...prev,
          {
            id: Math.max(...prev.map((e) => e.id), 0) + 1,
            ...formData,
            status: "pending",
            dateAdded: new Date().toISOString().split("T")[0],
            lastContact: null,
          },
        ]);
      }
      setFormData({ name: "", affiliation: "", email: "", field: "math.AP", notes: "" });
      setShowForm(false);
    }
  };

  const updateStatus = (id, newStatus) => {
    setEndorsers((prev) =>
      prev.map((e) =>
        e.id === id
          ? { ...e, status: newStatus, lastContact: new Date().toISOString().split("T")[0] }
          : e
      )
    );
  };

  const deleteEndorser = (id) => {
    setEndorsers((prev) => prev.filter((e) => e.id !== id));
  };

  const endorsed = endorsers.filter((e) => e.status === "endorsed").length;

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="font-serif text-xl mb-1">arXiv Endorsement CRM</h3>
          <p className="text-sm text-muted-foreground">
            Track outreach to potential arXiv math.AP endorsers
          </p>
        </div>
        <div className="text-right">
          <div className="font-serif text-3xl text-accent">{endorsed}/{endorsers.length}</div>
          <div className="text-xs text-muted-foreground">Endorsed</div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {["pending", "contacted", "endorsed"].map((s) => {
          const count = endorsers.filter((e) => e.status === s).length;
          const Icon = statusConfig[s].icon;
          return (
            <div key={s} className="p-4 bg-card border border-border rounded-lg">
              <div className="flex items-center gap-2 mb-2">
                <Icon className={`w-4 h-4 ${statusConfig[s].color}`} />
                <span className="text-sm font-medium capitalize">{s}</span>
              </div>
              <div className="font-serif text-2xl">{count}</div>
            </div>
          );
        })}
      </div>

      <div className="space-y-3">
        {endorsers.map((e, idx) => {
          const statusCfg = statusConfig[e.status];
          const StatusIcon = statusCfg.icon;

          return (
            <motion.div
              key={e.id}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.05 }}
              className="p-4 bg-card border border-border rounded-lg hover:border-accent/40 transition-colors"
            >
              <div className="flex items-start gap-4">
                <div className={`w-10 h-10 rounded-full ${statusCfg.bg} flex items-center justify-center shrink-0`}>
                  <StatusIcon className={`w-5 h-5 ${statusCfg.color}`} />
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap mb-1">
                    <h4 className="font-serif text-base">{e.name}</h4>
                    <span className="text-xs bg-muted px-2 py-0.5 rounded">
                      {e.affiliation}
                    </span>
                  </div>

                  <p className="text-sm text-muted-foreground mb-2">{e.email}</p>

                  {e.notes && (
                    <p className="text-sm italic text-muted-foreground mb-2">"{e.notes}"</p>
                  )}

                  <div className="flex items-center gap-2 text-xs text-muted-foreground">
                    <span>Added: {e.dateAdded}</span>
                    {e.lastContact && <span>· Last: {e.lastContact}</span>}
                  </div>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <select
                    value={e.status}
                    onChange={(evt) => updateStatus(e.id, evt.target.value)}
                    className="text-xs border border-border rounded px-2 py-1 bg-background"
                  >
                    <option value="pending">Pending</option>
                    <option value="contacted">Contacted</option>
                    <option value="endorsed">Endorsed</option>
                    <option value="declined">Declined</option>
                  </select>

                  <Button
                    variant="ghost"
                    size="icon"
                    className="w-8 h-8 text-muted-foreground hover:text-foreground"
                    onClick={() => deleteEndorser(e.id)}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      <div className="pt-4 border-t border-border">
        {!showForm ? (
          <Button
            onClick={() => {
              setShowForm(true);
              setEditingId(null);
              setFormData({ name: "", affiliation: "", email: "", field: "math.AP", notes: "" });
            }}
            className="gap-2"
          >
            <Plus className="w-4 h-4" /> Add Endorser
          </Button>
        ) : (
          <div className="space-y-3 p-4 bg-muted/30 rounded-lg">
            <Input
              placeholder="Name"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            />
            <Input
              placeholder="Affiliation"
              value={formData.affiliation}
              onChange={(e) => setFormData({ ...formData, affiliation: e.target.value })}
            />
            <Input
              placeholder="Email"
              type="email"
              value={formData.email}
              onChange={(e) => setFormData({ ...formData, email: e.target.value })}
            />
            <Textarea
              placeholder="Notes (e.g., research interests, contact strategy)"
              value={formData.notes}
              onChange={(e) => setFormData({ ...formData, notes: e.target.value })}
              className="h-20"
            />
            <div className="flex gap-2">
              <Button onClick={handleAddEndorser} className="flex-1">
                {editingId ? "Save" : "Add"}
              </Button>
              <Button
                variant="outline"
                onClick={() => {
                  setShowForm(false);
                  setEditingId(null);
                }}
                className="flex-1"
              >
                Cancel
              </Button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
