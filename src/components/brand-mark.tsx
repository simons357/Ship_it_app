export function BrandMark({
  className = "",
  size = "md",
}: {
  className?: string;
  size?: "sm" | "md" | "lg";
}) {
  const sizes = {
    sm: "text-xl tracking-tight",
    md: "text-2xl tracking-tight",
    lg: "text-5xl sm:text-7xl tracking-[-0.04em]",
  };

  return (
    <span
      className={`font-[family-name:var(--font-display)] font-semibold text-ink ${sizes[size]} ${className}`}
    >
      Ship<span className="text-sea"> it</span>
    </span>
  );
}
