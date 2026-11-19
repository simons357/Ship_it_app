import React, { useState, useEffect } from "react";
import { base44 } from "@/api/base44Client";
import { motion } from "framer-motion";
import { Plus, FileText, Download, GitCompare, Trash2, Tag } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import VersionUploadForm from "./VersionUploadForm";
import VersionDiff from "./VersionDiff";

const STATUS_COLORS = {
  Draft: "bg-muted text-muted-foreground border-border",
  Review: "bg-accent/10 text-accent border-accent/30",
  Submitted: "bg-primary/10 text-primary border-primary/30",
  Accepted: "bg-chart-1/10 text-chart-1 border-chart-1/30",
  Rejected: "bg-destructive/10 text-destructive border-destructive/30",
};

const FILE_ICONS = {
  tex: "TEX",
  pdf: "PDF",
  other: "FILE",
};

export default function VersionHistory() {
  const [versions, setVersions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [filterPaper, setFilterPaper] = useState("all");
  const [compareA, setCompareA] = useState(null);
  const [compareB, setCompareB] = useState(null);
  const [showDiff, setShowDiff] = useState(false);
  const [selectingCompare, setSelectingCompare] = useState(false);

  const loadVersions = async () => {
    setLoading(true);
    const data = await base44.entities.PaperVersion.list("-created_date");
    setVersions(data);
    setLoading(false);
  };

  useEffect(() => {
    loadVersions();
  }, []);

  const handleDelete = async (id) => {
    await base44.entities.PaperVersion.delete(id);
    setVersions((prev) => prev.filter((v) => v.id !== id));
  };

  const handleStatusChange = async (id, status) => {
    await base44.entities.PaperVersion.update(id, { status });
    setVersions((prev) => prev.map((v) => v.id === id ? { ...v, status } : v));
  };

  const handleCompareSelect = (version) => {
    if (!compareA) {
      setCompareA(version);
    } else if (!compareB && version.id !== compareA.id) {
      setCompareB(version);
      setShowDiff(true);
      setSelectingCompare(false);
    }
  };

  const startCompare = () => {
    setCompareA(null);
    setCompareB(null);
    setSelectingCompare(true);
  };

  const papers = ["all", ...new Set(versions.map((v) => v.paper_name))];
  const filtered = filterPaper === "all" ? versions : versions.filter((v) => v.paper_name === filterPaper);

  return (
    <div className="space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h3 className="font-serif text-xl">Document Version History</h3>
          <p className="text-sm text-muted-foreground mt-1">
            {versions.length} version{versions.length !== 1 ? "s" : ""} across {papers.length - 1} paper{papers.length - 1 !== 1 ? "s" : ""}
          </p>
        </div>
        <div className="flex items-center gap-2 flex-wrap">
          {selectingCompare && (
            <div className="text-xs text-accent font-medium animate-pulse">
              Select {!compareA ? "Version A" : "Version B"} from the list below…
            </div>
          )}
          <Button
            variant="outline"
            size="sm"
            onClick={selectingCompare ? () => setSelectingCompare(false) : startCompare}
            className="gap-2"
          >
            <GitCompare className="w-4 h-4" />
            {selectingCompare ? "Cancel" : "Compare"}
          </Button>
          <Button
            size="sm"
            onClick={() => setShowForm(!showForm)}
            className="gap-2"
          >
            <Plus className="w-4 h-4" />
            New Version
          </Button>
        </div>
      </div>

      {showForm && (
        <VersionUploadForm
          onSaved={() => { setShowForm(false); loadVersions(); }}
          onCancel={() => setShowForm(false)}
        />
      )}

      {versions.length > 1 && (
        <div className="flex items-center gap-2">
          <span className="text-xs text-muted-foreground uppercase tracking-widest">Filter</span>
          <Select value={filterPaper} onValueChange={setFilterPaper}>
            <SelectTrigger className="w-48 h-8 text-sm">
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Papers</SelectItem>
              {papers.filter((p) => p !== "all").map((p) => (
                <SelectItem key={p} value={p}>{p}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>
      )}

      {loading ? (
        <div className="flex items-center justify-center py-12 text-muted-foreground text-sm">
          Loading versions…
        </div>
      ) : filtered.length === 0 ? (
        <div className="flex flex-col items-center justify-center py-16 gap-4 text-center">
          <FileText className="w-10 h-10 text-muted-foreground/40" />
          <div>
            <p className="font-serif text-lg">No versions yet</p>
            <p className="text-sm text-muted-foreground mt-1">Upload your first .tex or .pdf to start tracking.</p>
          </div>
          <Button onClick={() => setShowForm(true)} className="gap-2">
            <Plus className="w-4 h-4" /> Upload First Version
          </Button>
        </div>
      ) : (
        <div className="space-y-3">
          {filtered.map((version, idx) => {
            const isSelectedA = compareA?.id === version.id;
            const isSelectedB = compareB?.id === version.id;
            return (
              <motion.div
                key={version.id}
                initial={{ opacity: 0, y: 8 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: idx * 0.04 }}
                onClick={selectingCompare ? () => handleCompareSelect(version) : undefined}
                className={`group relative p-5 bg-card border rounded-lg transition-all ${
                  selectingCompare ? "cursor-pointer hover:border-accent" : ""
                } ${isSelectedA ? "border-accent ring-1 ring-accent" : isSelectedB ? "border-primary ring-1 ring-primary" : "border-border hover:border-accent/40"}`}
              >
                {(isSelectedA || isSelectedB) && (
                  <div className={`absolute -top-2 -right-2 text-[10px] font-mono uppercase tracking-widest px-2 py-0.5 rounded-full ${isSelectedA ? "bg-accent text-accent-foreground" : "bg-primary text-primary-foreground"}`}>
                    {isSelectedA ? "A" : "B"}
                  </div>
                )}

                <div className="flex items-start gap-4">
                  <div className="w-12 h-12 rounded-lg bg-muted flex items-center justify-center shrink-0 font-mono text-[10px] font-medium text-muted-foreground">
                    {FILE_ICONS[version.file_type] || "FILE"}
                  </div>

                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap mb-1">
                      <span className="font-serif text-base">{version.paper_name}</span>
                      <span className="font-mono text-xs text-muted-foreground">{version.version_label}</span>
                      <span className={`text-[10px] font-mono uppercase tracking-wider px-2 py-0.5 rounded-full border ${STATUS_COLORS[version.status]}`}>
                        {version.status}
                      </span>
                    </div>

                    {version.file_name && (
                      <p className="text-xs text-muted-foreground mb-2 font-mono">{version.file_name}</p>
                    )}

                    {version.change_summary && (
                      <p className="text-sm text-muted-foreground leading-relaxed mb-2">{version.change_summary}</p>
                    )}

                    <div className="text-xs text-muted-foreground">
                      {new Date(version.created_date).toLocaleDateString("en-US", {
                        month: "long", day: "numeric", year: "numeric", hour: "2-digit", minute: "2-digit"
                      })}
                    </div>
                  </div>

                  <div className="flex items-center gap-1 shrink-0 opacity-0 group-hover:opacity-100 transition-opacity">
                    <Select
                      value={version.status}
                      onValueChange={(s) => handleStatusChange(version.id, s)}
                    >
                      <SelectTrigger className="h-7 text-xs w-28">
                        <Tag className="w-3 h-3 mr-1" />
                        <SelectValue />
                      </SelectTrigger>
                      <SelectContent>
                        {["Draft", "Review", "Submitted", "Accepted", "Rejected"].map((s) => (
                          <SelectItem key={s} value={s}>{s}</SelectItem>
                        ))}
                      </SelectContent>
                    </Select>

                    {version.file_url && (
                      <a href={version.file_url} target="_blank" rel="noopener noreferrer">
                        <Button variant="ghost" size="icon" className="w-8 h-8">
                          <Download className="w-4 h-4" />
                        </Button>
                      </a>
                    )}

                    <Button
                      variant="ghost"
                      size="icon"
                      className="w-8 h-8 text-muted-foreground hover:text-destructive"
                      onClick={(e) => { e.stopPropagation(); handleDelete(version.id); }}
                    >
                      <Trash2 className="w-4 h-4" />
                    </Button>
                  </div>
                </div>
              </motion.div>
            );
          })}
        </div>
      )}

      {showDiff && compareA && compareB && (
        <VersionDiff
          versionA={compareA}
          versionB={compareB}
          onClose={() => {
            setShowDiff(false);
            setCompareA(null);
            setCompareB(null);
          }}
        />
      )}
    </div>
  );
}
