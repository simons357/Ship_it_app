import { sections } from "./data";

const colorMap = {
  cyan: "text-cyan-400 border-cyan-500 bg-cyan-500/10",
  violet: "text-violet-400 border-violet-500 bg-violet-500/10",
  amber: "text-amber-400 border-amber-500 bg-amber-500/10",
  emerald: "text-emerald-400 border-emerald-500 bg-emerald-500/10",
  rose: "text-rose-400 border-rose-500 bg-rose-500/10",
  sky: "text-sky-400 border-sky-500 bg-sky-500/10",
  orange: "text-orange-400 border-orange-500 bg-orange-500/10",
};

const dotColor = {
  cyan: "bg-cyan-400",
  violet: "bg-violet-400",
  amber: "bg-amber-400",
  emerald: "bg-emerald-400",
  rose: "bg-rose-400",
  sky: "bg-sky-400",
  orange: "bg-orange-400",
};

export default function Sidebar({ sections, activeSection, activeStep, onSectionClick }) {
  return (
    <div className="w-72 flex-shrink-0 bg-slate-900/80 border-r border-slate-800 flex flex-col overflow-hidden">
      <div className="p-5 border-b border-slate-800">
        <div className="text-xs text-slate-500 tracking-widest uppercase mb-1">Navier–Stokes</div>
        <div className="text-lg font-bold text-slate-100 leading-tight">Regularity Proof<br/>Navigator</div>
      </div>
      <div className="flex-1 overflow-y-auto py-3">
        {sections.map((section, sIdx) => {
          const isActive = sIdx === activeSection;
          const colors = colorMap[section.color] || colorMap.cyan;
          const dot = dotColor[section.color] || dotColor.cyan;
          return (
            <div key={section.id} className="mb-1">
              <button
                onClick={() => onSectionClick(sIdx)}
                className={`w-full text-left px-4 py-3 flex items-start gap-3 transition-all hover:bg-slate-800/60 ${isActive ? "bg-slate-800/80" : ""}`}
              >
                <div className={`flex-shrink-0 w-8 h-8 rounded-lg border flex items-center justify-center text-sm font-bold mt-0.5 ${colors}`}>
                  {section.icon}
                </div>
                <div className="flex-1 min-w-0">
                  <div className={`text-xs font-semibold leading-tight ${isActive ? "text-slate-100" : "text-slate-400"}`}>
                    {section.title}
                  </div>
                  <div className="flex gap-1 mt-2 flex-wrap">
                    {section.steps.map((_, stepIdx) => (
                      <div
                        key={stepIdx}
                        className={`h-1.5 w-4 rounded-full transition-all ${
                          isActive && stepIdx <= activeStep
                            ? dot
                            : "bg-slate-700"
                        }`}
                      />
                    ))}
                  </div>
                </div>
              </button>
            </div>
          );
        })}
      </div>
      <div className="p-4 border-t border-slate-800 text-xs text-slate-600">
        QStack · H3 Framework
      </div>
    </div>
  );
}