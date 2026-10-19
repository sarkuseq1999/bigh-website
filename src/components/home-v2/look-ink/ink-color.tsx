"use client";

import { createContext, useContext, type ReactNode } from "react";

// A touch of colour: "green spring" (Mo, October 16, 2026). The homepage was "a little too black
// and white"; of three tests and then two live versions she chose C, green spring, with the
// buttons kept in ink. The homepage's paintings carry a thin watercolour: blue in the far hills,
// sage green near, pink blossoms, a red crown on the crane, the gold leaf untouched. Each tinted
// painting is the same picture with its ink treated as a coloured pigment
// (reference/home-v2/ink/recolor/recolor.py), saved beside the original in
// /images/home-v2/ink/spring/ under the same name. Only the homepage provides the colour: the
// footer's crane at rest and the bottles' ink pools stay grey on every other page.
export type InkColor = "ink" | "spring";

const DIR = "/images/home-v2/ink/";
const TINTED = new Set([
  "landscape.webp",
  "crane-painted.webp",
  "crane-flight-a2-twice.webp",
  "crane-flight-a2-twice-600.webp",
  "crane-rest-v2.webp",
  "mito.webp",
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

/** The painting to show for a picture's path: its tinted twin where the page is in colour. */
export function useTint(): (src: string) => string {
  const color = useContext(ColorContext);
  return (src) => {
    if (color === "ink" || !src.startsWith(DIR)) return src;
    const name = src.slice(DIR.length);
    return TINTED.has(name) ? `${DIR}${color}/${name}` : src;
  };
}
