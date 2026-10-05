"use client";

import { useEffect, useState } from "react";

// Review only (October 5, 2026): a small chip in the corner to flip between today's menu bar and
// the three options. Hidden with `?rec=1` (recordings). Not part of any design.
const options = [
  { key: undefined, label: "Today" },
  { key: "a", label: "A" },
  { key: "b", label: "B" },
  { key: "c", label: "C" },
] as const;

export function NavSwitcher({ current }: { current?: string }) {
  const [hidden, setHidden] = useState(false);
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === "h" && event.altKey) setHidden((value) => !value);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);
  if (hidden) return null;
  const active = options.some((option) => option.key === current) ? current : undefined;
  return (
    <nav
      aria-label="Menu bar options (review)"
      style={{
        position: "fixed",
        left: 16,
        bottom: 16,
        zIndex: 90,
        display: "flex",
        gap: 4,
        padding: 4,
        borderRadius: 999,
        background: "rgba(12, 11, 10, 0.86)",
        color: "#f8f3ea",
        font: "500 14px/1 var(--font-brand), Arial, sans-serif",
      }}
    >
      <span style={{ alignSelf: "center", padding: "0 8px 0 10px", opacity: 0.7 }}>Menu bar</span>
      {options.map((option) => {
        const on = option.key === active;
        return (
          <a
            key={option.label}
            href={option.key ? `?nav=${option.key}` : "?"}
            aria-current={on ? "true" : undefined}
            style={{
              display: "inline-flex",
              alignItems: "center",
              minHeight: 36,
              padding: "0 14px",
              borderRadius: 999,
              background: on ? "#f8f3ea" : "transparent",
              color: on ? "#0c0b0a" : "inherit",
            }}
          >
            {option.label}
          </a>
        );
      })}
    </nav>
  );
}
