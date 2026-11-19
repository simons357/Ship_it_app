import React from "react";
import { X, ArrowRight } from "lucide-react";
import { Button } from "@/components/ui/button";

const STATUS_COLORS = {
  Draft: "bg-muted text-muted-foreground",
  Review: "bg-accent/10 text-accent",
  Submitted: "bg-primary/10 text-primary",
  Accepted: "bg-chart-1/10 text-chart-1",
  Rejected: "bg-destructive/10 text-destructive",
};

function Field({ label, a, b }) {
  const changed = a !== b;
  return (
    <div className={`grid grid-cols-[1fr_auto_1fr] gap-4 items-start py-3 border-b border-border ${changed ? "bg-accent/5 -mx-4 px-4 rounded" : ""}`}>
      <div>
        <div className="text-[10px] uppercase tracking-widest text-muted-foreground mb-1">{label} (A)</div>
        <div className={`text-sm leading-relaxed ${changed ? "font-medium" : "text-muted-foreground"}`}>
          {a || <span className="italic text-muted-foreground">—</span>}
        </div>
      </div>
      <ArrowRight className={`w-4 h-4 mt-5 ${changed ? "text-accent" : "text-muted-foreground/30"}`} />
      <div>
        <div className="text-[10px] uppercase tracking-widest text-muted-foreground mb-1">{label} (B)</div>
        <div className={`text-sm leading-relaxed ${changed ? "font-medium text-accent" : "text-muted-foreground"}`}>
          {b || <span className="italic text-muted-foreground">—</span>}
        </div>
      </div>
    </div>
  );
}

export default function VersionDiff({ versionA, versionB, onClose }) {
  if (!versionA || !versionB) return null;

  return (
    <div className="fixed inset-0 bg-background/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-card border border-border rounded-lg w-full max-w-2xl max-h-[80vh] overflow-y-auto shadow-xl">
        <div className="flex items-center justify-between p-5 border-b border-border sticky top-0 bg-card">
          <div>
            <h3 className="font-serif text-xl">Version Comparison</h3>
            <p className="text-sm text-muted-foreground mt-0.5">
              {versionA.version_label} → {versionB.version_label}
            </p>
          </div>
          <Button variant="ghost" size="icon" onClick={onClose}>
            <X className="w-5 h-5" />
          </Button>
        </div>

        <div className="p-5 space-y-0">
          <Field label="Status" a={versionA.status} b={versionB.status} />
          <Field label="Paper" a={versionA.paper_name} b={versionB.paper_name} />
          <Field label="File" a={versionA.file_name || "—"} b={versionB.file_name || "—"} />
          <Field label="Change Summary" a={versionA.change_summary} b={versionB.change_summary} />
          <Field label="Notes" a={versionA.notes} b={versionB.notes} />

          <div className="grid grid-cols-[1fr_auto_1fr] gap-4 items-start py-3">
            <div>
              <div className="text-[10px] uppercase tracking-widest text-muted-foreground mb-1">Date (A)</div>
              <div className="text-sm text-muted-foreground">
                {new Date(versionA.created_date).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}
              </div>
            </div>
            <ArrowRight className="w-4 h-4 mt-5 text-muted-foreground/30" />
            <div>
              <div className="text-[10px] uppercase tracking-widest text-muted-foreground mb-1">Date (B)</div>
              <div className="text-sm text-muted-foreground">
                {new Date(versionB.created_date).toLocaleDateString("en-US", { month: "short", day: "numeric", year: "numeric" })}
              </div>
            </div>
          </div>
        </div>

        <div className="p-5 border-t border-border flex gap-3">
          {versionA.file_url && (
            <a href={versionA.file_url} target="_blank" rel="noopener noreferrer" className="flex-1">
              <Button variant="outline" className="w-full">Open {versionA.version_label}</Button>
            </a>
          )}
          {versionB.file_url && (
            <a href={versionB.file_url} target="_blank" rel="noopener noreferrer" className="flex-1">
              <Button variant="outline" className="w-full">Open {versionB.version_label}</Button>
            </a>
          )}
        </div>
      </div>
    </div>
  );
}
