import React from "react";
import "katex/dist/katex.min.css";
import { InlineMath, BlockMath } from "react-katex";

export function ML({ children }) {
  return (
    <span className="text-cyan-200">
      <InlineMath math={children} />
    </span>
  );
}

export function MB({ children, label }) {
  return (
    <div className="my-4 px-4 py-3 bg-[#0a0c12] border border-gray-800 rounded overflow-x-auto">
      {label && (
        <div className="text-xs text-gray-500 mb-2 uppercase tracking-widest">{label}</div>
      )}
      <div className="text-center text-gray-100">
        <BlockMath math={children} />
      </div>
    </div>
  );
}