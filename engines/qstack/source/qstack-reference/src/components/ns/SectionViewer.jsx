import { motion, AnimatePresence } from "framer-motion";
import MathBlock from "./MathBlock";
import { ChevronLeft, ChevronRight } from "lucide-react";

const tagColorMap = {
  cyan: "bg-cyan-500/20 text-cyan-300 border border-cyan-500/30",
  violet: "bg-violet-500/20 text-violet-300 border border-violet-500/30",
  amber: "bg-amber-500/20 text-amber-300 border border-amber-500/30",
  emerald: "bg-emerald-500/20 text-emerald-300 border border-emerald-500/30",
  rose: "bg-rose-500/20 text-rose-300 border border-rose-500/30",
  sky: "bg-sky-500/20 text-sky-300 border border-sky-500/30",
  orange: "bg-orange-500/20 text-orange-300 border border-orange-500/30",
  red: "bg-red-500/20 text-red-300 border border-red-500/30",
  green: "bg-green-500/20 text-green-300 border border-green-500/30",
};

const sectionBorderMap = {
  cyan: "border-cyan-500/40",
  violet: "border-violet-500/40",
  amber: "border-amber-500/40",
  emerald: "border-emerald-500/40",
  rose: "border-rose-500/40",
  sky: "border-sky-500/40",
  orange: "border-orange-500/40",
};

const operatorColors = {
  blue: "bg-blue-500/15 border-blue-500/30 text-blue-300",
  purple: "bg-purple-500/15 border-purple-500/30 text-purple-300",
  green: "bg-emerald-500/15 border-emerald-500/30 text-emerald-300",
  orange: "bg-orange-500/15 border-orange-500/30 text-orange-300",
};

export default function SectionViewer({
  section, step, stepIndex, totalSteps,
  globalStep, globalTotal,
  onNext, onPrev, canNext, canPrev,
}) {
  const borderColor = sectionBorderMap[section.color] || "border-slate-700";
  const tagColor = tagColorMap[step.tagColor] || tagColorMap.cyan;

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      {/* Top bar */}
      <div className="flex items-center justify-between px-8 py-4 border-b border-slate-800 bg-slate-900/40">
        <div className="flex items-center gap-3">
          <span className="text-slate-500 text-sm">{section.title}</span>
          <span className="text-slate-700">›</span>
          <span className="text-slate-300 text-sm font-medium">{step.title}</span>
        </div>
        <div className="flex items-center gap-2 text-xs text-slate-500">
          <span>{stepIndex + 1} / {totalSteps}</span>
          <span className="text-slate-700 mx-1">·</span>
          <span>Step {globalStep + 1} of {globalTotal}</span>
        </div>
      </div>

      {/* Global progress bar */}
      <div className="h-0.5 bg-slate-800">
        <div
          className="h-full bg-gradient-to-r from-slate-500 to-slate-300 transition-all duration-500"
          style={{ width: `${((globalStep + 1) / globalTotal) * 100}%` }}
        />
      </div>

      {/* Main content */}
      <div className="flex-1 overflow-y-auto">
        <AnimatePresence mode="wait">
          <motion.div
            key={`${section.id}-${stepIndex}`}
            initial={{ opacity: 0, y: 16 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -16 }}
            transition={{ duration: 0.25 }}
            className="max-w-3xl mx-auto px-8 py-10"
          >
            {/* Tag */}
            <div className="flex items-center gap-3 mb-6">
              <span className={`text-xs font-mono px-3 py-1 rounded-full ${tagColor}`}>
                {step.tag}
              </span>
              {step.wrongRoute && (
                <span className="text-xs text-slate-600 font-mono">non-circular route</span>
              )}
            </div>

            {/* Title */}
            <h1 className="text-3xl font-bold text-slate-100 leading-tight mb-3">
              {step.title}
            </h1>

            {/* Summary */}
            <p className="text-slate-400 text-base leading-relaxed mb-8 border-l-2 pl-4 border-slate-700 italic">
              {step.summary}
            </p>

            {/* Body */}
            <p className="text-slate-300 text-sm leading-relaxed mb-8">
              {step.body}
            </p>

            {/* Wrong / Right route */}
            {step.wrongRoute && (
              <div className="grid grid-cols-1 gap-3 mb-8">
                <div className="flex items-start gap-3 p-4 rounded-lg bg-red-500/8 border border-red-500/20">
                  <span className="text-red-400 text-xs font-mono mt-0.5 flex-shrink-0">✗ WRONG</span>
                  <div className="text-red-300/70 text-sm font-mono">{step.wrongRoute}</div>
                </div>
                <div className="flex items-start gap-3 p-4 rounded-lg bg-green-500/8 border border-green-500/20">
                  <span className="text-green-400 text-xs font-mono mt-0.5 flex-shrink-0">✓ CORRECT</span>
                  <div className="text-green-300/70 text-sm font-mono">{step.rightRoute}</div>
                </div>
              </div>
            )}

            {/* Main formula */}
            {step.formula && (
              <div className={`p-6 rounded-xl bg-slate-900 border ${borderColor} mb-6`}>
                <MathBlock formula={step.formula} />
              </div>
            )}

            {/* Sub formulas for Q6 */}
            {step.subFormula && (
              <div className={`p-5 rounded-xl bg-slate-900/60 border border-slate-700/50 mb-4`}>
                <div className="text-xs text-slate-500 font-mono mb-3">with</div>
                <MathBlock formula={step.subFormula} />
              </div>
            )}
            {step.normFormula && (
              <div className={`p-5 rounded-xl bg-slate-900/60 border border-slate-700/50 mb-6`}>
                <div className="text-xs text-slate-500 font-mono mb-3">where</div>
                <MathBlock formula={step.normFormula} />
              </div>
            )}

            {/* Criterion */}
            {step.criterion && (
              <div className="p-5 rounded-xl bg-slate-800/60 border border-slate-600/40 mb-6">
                <div className="text-xs text-slate-500 font-mono uppercase tracking-wider mb-3">H3 follows if</div>
                <MathBlock formula={step.criterion} />
              </div>
            )}

            {/* Consequence */}
            {step.consequence && (
              <div className="p-5 rounded-xl bg-amber-500/8 border border-amber-500/25 mb-6">
                <div className="text-xs text-amber-500 font-mono uppercase tracking-wider mb-3">Consequence</div>
                <MathBlock formula={step.consequence} />
              </div>
            )}

            {/* Stronger formula */}
            {step.strongerFormula && (
              <div className="p-5 rounded-xl bg-emerald-500/8 border border-emerald-500/20 mb-6">
                <div className="text-xs text-emerald-500 font-mono uppercase tracking-wider mb-3">Stronger form</div>
                <MathBlock formula={step.strongerFormula} />
              </div>
            )}

            {/* Operator table */}
            {step.operators && (
              <div className="grid grid-cols-1 gap-3 mb-8">
                {step.operators.map((op) => (
                  <div key={op.name} className={`flex items-center gap-4 p-4 rounded-lg border ${operatorColors[op.color]}`}>
                    <div className="text-lg font-bold font-mono w-12 text-center">{op.name}</div>
                    <div className="text-sm">{op.role}</div>
                  </div>
                ))}
              </div>
            )}

            {/* Duality */}
            {step.duality && (
              <div className="grid grid-cols-2 gap-4 mb-8">
                {step.duality.map((d) => (
                  <div key={d.label} className="p-4 rounded-lg bg-slate-800/60 border border-slate-700/50">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-lg font-bold text-slate-200 font-mono">{d.label}</span>
                      <span className="text-xs text-slate-500 font-mono">{d.role}</span>
                    </div>
                    <p className="text-slate-400 text-xs leading-relaxed">{d.desc}</p>
                  </div>
                ))}
              </div>
            )}

            {/* Valid data list */}
            {step.validData && (
              <div className="mb-8">
                <div className="text-xs text-slate-500 font-mono uppercase tracking-wider mb-3">Valid energy-class quantities</div>
                <div className="grid grid-cols-2 gap-2">
                  {step.validData.map((d, i) => (
                    <div key={i} className="flex items-center gap-2 p-3 rounded-lg bg-green-500/8 border border-green-500/20">
                      <span className="text-green-400 text-xs">✓</span>
                      <span className="text-green-300/80 text-xs font-mono">{d}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Note */}
            {step.note && (
              <div className="flex items-start gap-3 p-4 rounded-lg bg-slate-800/40 border border-slate-700/40">
                <span className="text-slate-500 text-xs mt-0.5 flex-shrink-0 font-mono">NOTE</span>
                <p className="text-slate-400 text-xs leading-relaxed font-mono">{step.note}</p>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>

      {/* Navigation footer */}
      <div className="px-8 py-5 border-t border-slate-800 bg-slate-900/40 flex items-center justify-between">
        <button
          onClick={onPrev}
          disabled={!canPrev}
          className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-300 text-sm font-medium hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed transition-all"
        >
          <ChevronLeft className="w-4 h-4" />
          Previous
        </button>

        {/* Step dots */}
        <div className="flex items-center gap-2">
          {Array.from({ length: totalSteps }).map((_, i) => (
            <div
              key={i}
              className={`rounded-full transition-all duration-300 ${
                i === stepIndex
                  ? "w-6 h-2 bg-slate-300"
                  : i < stepIndex
                  ? "w-2 h-2 bg-slate-500"
                  : "w-2 h-2 bg-slate-700"
              }`}
            />
          ))}
        </div>

        <button
          onClick={onNext}
          disabled={!canNext}
          className="flex items-center gap-2 px-5 py-2.5 rounded-lg bg-slate-100 text-slate-900 text-sm font-bold hover:bg-white disabled:opacity-30 disabled:cursor-not-allowed transition-all"
        >
          Next
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}