import React, { useState } from "react";
import { motion } from "framer-motion";
import { ChevronDown, Check, Clock, AlertCircle, Zap } from "lucide-react";

const projects = [
  {
    id: 1,
    name: "NS/Clay Paper",
    status: "in-progress",
    progress: 85,
    startDate: "2026-01-01",
    targetDate: "2026-04-30",
    milestones: [
      { name: "Compile in Overleaf", date: "2026-04-18", done: false },
      { name: "Integrate Theorem H proof", date: "2026-04-18", done: false },
      { name: "Write endorser email", date: "2026-04-18", done: false },
      { name: "Submit to arXiv", date: "2026-04-25", done: false },
    ],
    team: "Jonathan Robert Simons",
    color: "bg-accent",
  },
  {
    id: 2,
    name: "SFE / Geometry of Flow",
    status: "ready",
    progress: 0,
    startDate: "2026-04-18",
    targetDate: "2026-05-15",
    milestones: [
      { name: "Write 15-page draft", date: "2026-04-25", done: false },
      { name: "Include MasterMap diagram", date: "2026-05-01", done: false },
      { name: "Polish for submission", date: "2026-05-10", done: false },
    ],
    team: "Jonathan Robert Simons",
    color: "bg-primary",
  },
  {
    id: 3,
    name: "Exoplanet / Prime Resonance",
    status: "ready",
    progress: 60,
    startDate: "2026-02-01",
    targetDate: "2026-05-30",
    milestones: [
      { name: "Data analysis done", date: "2026-04-01", done: true },
      { name: "Polish draft", date: "2026-04-25", done: false },
      { name: "Submit to MNRAS", date: "2026-05-15", done: false },
    ],
    team: "Jonathan Robert Simons",
    color: "bg-chart-2",
  },
  {
    id: 4,
    name: "ℝ³ Extension Program",
    status: "planning",
    progress: 5,
    startDate: "2026-05-01",
    targetDate: "2026-12-31",
    milestones: [
      { name: "Study Bahouri–Gérard profiles", date: "2026-05-15", done: false },
      { name: "Formalize proof strategy", date: "2026-06-30", done: false },
      { name: "Lemma bank development", date: "2026-09-30", done: false },
    ],
    team: "Research Program",
    color: "bg-destructive",
  },
  {
    id: 5,
    name: "Theorem H Write-up",
    status: "done",
    progress: 100,
    startDate: "2026-04-17",
    targetDate: "2026-04-18",
    milestones: [
      { name: "Complete proof", date: "2026-04-18", done: true },
      { name: "Ready for LaTeX", date: "2026-04-18", done: true },
    ],
    team: "Jonathan Robert Simons + AI",
    color: "bg-chart-1",
  },
];

const statusColors = {
  done: "bg-chart-1 text-chart-1",
  "in-progress": "bg-accent text-accent",
  ready: "bg-primary text-primary",
  planning: "bg-muted text-muted-foreground",
};

const statusLabels = {
  done: "Complete",
  "in-progress": "In Progress",
  ready: "Ready to Start",
  planning: "Planning",
};

export default function ProjectGantt() {
  const [expanded, setExpanded] = useState({});
  const [selected, setSelected] = useState(null);

  const toggleExpand = (id) => {
    setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
  };

  const getDateWidth = (start, end, date) => {
    const startTime = new Date(start).getTime();
    const endTime = new Date(end).getTime();
    const dateTime = new Date(date).getTime();
    const totalWidth = endTime - startTime;
    const offset = dateTime - startTime;
    return (offset / totalWidth) * 100;
  };

  const maxDate = new Date("2026-12-31");
  const minDate = new Date("2026-01-01");
  const totalDays = (maxDate - minDate) / (1000 * 60 * 60 * 24);

  return (
    <div className="space-y-6">
      <div className="grid gap-4">
        {projects.map((project, idx) => (
          <motion.div
            key={project.id}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3, delay: idx * 0.05 }}
            className="bg-card border border-border rounded-lg overflow-hidden hover:border-accent/40 transition-colors"
          >
            <button
              onClick={() => {
                toggleExpand(project.id);
                setSelected(project.id);
              }}
              className="w-full p-5 text-left hover:bg-muted/30 transition-colors flex items-center justify-between"
            >
              <div className="flex items-center gap-4 flex-1 min-w-0">
                <div className={`w-10 h-10 rounded-full ${project.color} bg-opacity-20 flex items-center justify-center shrink-0`}>
                  {project.status === "done" ? (
                    <Check className={`w-5 h-5 ${project.color.replace("bg-", "text-")}`} />
                  ) : project.status === "in-progress" ? (
                    <Zap className={`w-5 h-5 ${project.color.replace("bg-", "text-")}`} />
                  ) : (
                    <Clock className={`w-5 h-5 ${project.color.replace("bg-", "text-")}`} />
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className="font-serif text-lg leading-tight">{project.name}</h3>
                  <div className="flex items-center gap-3 mt-2">
                    <div className="flex-1 bg-muted rounded-full h-2 max-w-xs overflow-hidden">
                      <div
                        className={`h-full ${project.color} transition-all`}
                        style={{ width: `${project.progress}%` }}
                      />
                    </div>
                    <span className="text-xs font-mono text-muted-foreground">{project.progress}%</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-3 ml-4 shrink-0">
                <div className={`px-2 py-1 rounded-full text-[10px] font-mono uppercase tracking-wider ${statusColors[project.status]}`}>
                  {statusLabels[project.status]}
                </div>
                <ChevronDown
                  className={`w-5 h-5 text-muted-foreground transition-transform ${
                    expanded[project.id] ? "rotate-180" : ""
                  }`}
                />
              </div>
            </button>

            {expanded[project.id] && (
              <motion.div
                initial={{ height: 0, opacity: 0 }}
                animate={{ height: "auto", opacity: 1 }}
                transition={{ duration: 0.3 }}
                className="border-t border-border px-5 py-5 space-y-6 bg-muted/20"
              >
                <div>
                  <div className="text-xs uppercase tracking-widest text-muted-foreground mb-3">Timeline</div>
                  <div className="relative h-16 bg-background rounded-lg border border-border p-2">
                    <div className="absolute inset-0 flex items-center px-2">
                      {project.milestones.map((m, i) => (
                        <div
                          key={i}
                          className="absolute flex flex-col items-center"
                          style={{
                            left: `${getDateWidth(project.startDate, project.targetDate, m.date)}%`,
                          }}
                        >
                          <div
                            className={`w-3 h-3 rounded-full ${
                              m.done
                                ? "bg-chart-1 shadow-lg shadow-chart-1/50"
                                : "bg-muted-foreground border border-border"
                            }`}
                          />
                          <div className="text-[9px] text-muted-foreground mt-1 whitespace-nowrap">
                            {new Date(m.date).toLocaleDateString("en-US", {
                              month: "short",
                              day: "numeric",
                            })}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div>
                  <div className="text-xs uppercase tracking-widest text-muted-foreground mb-3">Milestones</div>
                  <div className="space-y-2">
                    {project.milestones.map((m, i) => (
                      <div key={i} className="flex items-center gap-3 p-2 rounded-lg hover:bg-background/50 transition-colors">
                        <div
                          className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                            m.done
                              ? "bg-chart-1 border-chart-1"
                              : "border-border"
                          }`}
                        >
                          {m.done && <Check className="w-3 h-3 text-background" strokeWidth={3} />}
                        </div>
                        <div className="flex-1">
                          <p className={`text-sm ${m.done ? "line-through text-muted-foreground" : ""}`}>
                            {m.name}
                          </p>
                        </div>
                        <span className="text-xs text-muted-foreground font-mono">
                          {new Date(m.date).toLocaleDateString("en-US", {
                            month: "short",
                            day: "numeric",
                          })}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="pt-3 border-t border-border">
                  <div className="text-xs uppercase tracking-widest text-muted-foreground mb-2">Owner</div>
                  <div className="text-sm">{project.team}</div>
                </div>
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
}
