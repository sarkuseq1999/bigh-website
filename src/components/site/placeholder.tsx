import { clsx } from "clsx";

export function Placeholder({
  label,
  className,
}: {
  label: string;
  className?: string;
}) {
  return (
    <div
      role="img"
      aria-label={label}
      className={clsx(
        "flex items-center justify-center rounded-xl border border-line bg-paper-2 text-center",
        className,
      )}
    >
      <span className="font-mono text-xs tracking-widest text-ink-soft uppercase px-4">
        {label}
      </span>
    </div>
  );
}
