"use client";

import { createContext, useContext, type ReactNode } from "react";
import styles from "./ink-color.module.css";

// A touch of colour (Mo, October 14-15, 2026: the homepage is "a little too black and white";
// of three tests she liked B and C and asked to try both). Review only: `?color=b` lays a thin
// watercolour over the paintings in the coastal-fog palette, `?color=c` in the green-spring one,
// and no parameter shows today's ink. The tinted paintings are the same pictures with their ink
// treated as a coloured pigment (made outside the repo by recolor.py; the gold leaf is untouched);
// they live beside the originals in /images/home-v2/ink/<coast|spring>/ under the same names.
export type InkColor = "ink" | "coast" | "spring";

const DIR = "/images/home-v2/ink/";
const TINTED = new Set([
  "landscape.webp",
  "crane-painted.webp",
  "crane-flight-a2-twice.webp",
  "crane-flight-a2-twice-600.webp",
  "crane-rest-v2.webp",
  "mito.webp",
  "mito-closeup.webp",
  "mito-aged.webp",
  "mito-radicals.webp",
  "halo.webp",
  "inkstone-v2.webp",
  "pool.webp",
  "pool-foot.webp",
  "story-morning-v2.webp",
  "story-reading-v2.webp",
  "story-source-v2.webp",
  "purpose-land.webp",
  "purpose-cranes.webp",
]);

const ColorContext = createContext<InkColor>("ink");

export function InkColorProvider({ color, children }: { color: InkColor; children: ReactNode }) {
  return <ColorContext.Provider value={color}>{children}</ColorContext.Provider>;
}

export function useInkColor(): InkColor {
  return useContext(ColorContext);
}

/** The painting to show for a picture's path: its tinted twin while a colour is chosen. */
export function useTint(): (src: string) => string {
  const color = useContext(ColorContext);
  return (src) => {
    if (color === "ink" || !src.startsWith(DIR)) return src;
    const name = src.slice(DIR.length);
    return TINTED.has(name) ? `${DIR}${color}/${name}` : src;
  };
}

const CHOICES: { color: InkColor; letter: string; name: string; href: string }[] = [
  { color: "ink", letter: "Now", name: "Ink", href: "?" },
  { color: "coast", letter: "B", name: "Coastal fog", href: "?color=b" },
  { color: "spring", letter: "C", name: "Green spring", href: "?color=c" },
];

/** The review switch, bottom right: each choice reloads the page in that colour. */
export function ColorSwitch() {
  const color = useContext(ColorContext);
  return (
    <nav className={styles.switch} aria-label="Colour test">
      {CHOICES.map((choice) => (
        <a
          key={choice.color}
          className={styles.choice}
          href={choice.href}
          aria-current={choice.color === color ? "page" : undefined}
        >
          <b>{choice.letter}</b>
          <span>{choice.name}</span>
        </a>
      ))}
    </nav>
  );
}
