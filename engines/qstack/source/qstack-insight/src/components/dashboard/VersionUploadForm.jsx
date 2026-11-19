import React, { useState } from "react";
import { base44 } from "@/api/base44Client";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Upload, Loader2, FileText, X } from "lucide-react";

const PAPERS = [
  "NS/Clay Paper",
  "SFE / Geometry of Flow",
  "Exoplanet / Prime Resonance",
  "ℝ³ Extension Program",
];

export default function VersionUploadForm({ onSaved, onCancel }) {
  const [form, setForm] = useState({
    paper_name: "NS/Clay Paper",
    version_label: "",
    status: "Draft",
    change_summary: "",
    notes: "",
  });
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e) => {
    const f = e.target.files[0];
    if (f) setFile(f);
  };

  const handleSubmit = async () => {
    if (!form.version_label) return;
    setUploading(true);

    let file_url = null;
    let file_name = null;
    let file_type = "other";

    if (file) {
      const { file_url: url } = await base44.integrations.Core.UploadFile({ file });
      file_url = url;
      file_name = file.name;
      if (file.name.endsWith(".tex")) file_type = "tex";
      else if (file.name.endsWith(".pdf")) file_type = "pdf";
    }

    await base44.entities.PaperVersion.create({
      ...form,
      file_url,
      file_name,
      file_type,
    });

    setUploading(false);
    onSaved();
  };

  return (
    <div className="space-y-4 p-5 bg-muted/30 rounded-lg border border-border">
      <div className="flex items-center justify-between">
        <h4 className="font-serif text-lg">Upload New Version</h4>
        <Button variant="ghost" size="icon" onClick={onCancel} className="w-8 h-8">
          <X className="w-4 h-4" />
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="space-y-1">
          <label className="text-xs uppercase tracking-widest text-muted-foreground">Paper</label>
          <Select
            value={form.paper_name}
            onValueChange={(v) => setForm({ ...form, paper_name: v })}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {PAPERS.map((p) => (
                <SelectItem key={p} value={p}>{p}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-1">
          <label className="text-xs uppercase tracking-widest text-muted-foreground">Version Label</label>
          <Input
            placeholder="e.g. v1.0, v2-theoremH"
            value={form.version_label}
            onChange={(e) => setForm({ ...form, version_label: e.target.value })}
          />
        </div>

        <div className="space-y-1">
          <label className="text-xs uppercase tracking-widest text-muted-foreground">Status</label>
          <Select
            value={form.status}
            onValueChange={(v) => setForm({ ...form, status: v })}
          >
            <SelectTrigger>
              <SelectValue />
            </SelectTrigger>
            <SelectContent>
              {["Draft", "Review", "Submitted", "Accepted", "Rejected"].map((s) => (
                <SelectItem key={s} value={s}>{s}</SelectItem>
              ))}
            </SelectContent>
          </Select>
        </div>

        <div className="space-y-1">
          <label className="text-xs uppercase tracking-widest text-muted-foreground">File (.tex or .pdf)</label>
          <label className="flex items-center gap-2 cursor-pointer px-3 py-2 border border-border rounded-md bg-background hover:bg-muted/50 transition-colors">
            <Upload className="w-4 h-4 text-muted-foreground" />
            <span className="text-sm text-muted-foreground truncate">
              {file ? file.name : "Choose file…"}
            </span>
            <input
              type="file"
              accept=".tex,.pdf"
              className="hidden"
              onChange={handleFileChange}
            />
          </label>
        </div>
      </div>

      <div className="space-y-1">
        <label className="text-xs uppercase tracking-widest text-muted-foreground">Change Summary</label>
        <Textarea
          placeholder="What changed in this version? e.g. Integrated Theorem H proof into Section 7, fixed LaTeX compilation errors…"
          value={form.change_summary}
          onChange={(e) => setForm({ ...form, change_summary: e.target.value })}
          className="h-20"
        />
      </div>

      <div className="space-y-1">
        <label className="text-xs uppercase tracking-widest text-muted-foreground">Notes</label>
        <Input
          placeholder="Any additional notes…"
          value={form.notes}
          onChange={(e) => setForm({ ...form, notes: e.target.value })}
        />
      </div>

      <div className="flex gap-2 pt-2">
        <Button onClick={handleSubmit} disabled={uploading || !form.version_label} className="flex-1 gap-2">
          {uploading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Upload className="w-4 h-4" />}
          {uploading ? "Uploading…" : "Save Version"}
        </Button>
        <Button variant="outline" onClick={onCancel} className="flex-1">Cancel</Button>
      </div>
    </div>
  );
}
