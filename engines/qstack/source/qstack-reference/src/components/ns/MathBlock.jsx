import { useEffect, useRef } from "react";

export default function MathBlock({ formula, display = true, className = "" }) {
  const ref = useRef(null);

  useEffect(() => {
    if (!ref.current || !formula) return;
    import("katex").then((katex) => {
      try {
        katex.default.render(formula, ref.current, {
          displayMode: display,
          throwOnError: false,
          trust: true,
          macros: {
            "\\R": "\\mathbb{R}",
          },
        });
      } catch (e) {
        ref.current.textContent = formula;
      }
    });
  }, [formula, display]);

  return (
    <div
      ref={ref}
      className={`katex-block ${display ? "overflow-x-auto py-1" : "inline"} ${className}`}
    />
  );
}