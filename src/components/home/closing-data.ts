// Homepage closing invitation. Mo accepted this working copy on September 21, 2026
// (BRAND-CHEATSHEET.md): the last content block before the footer, bringing visitors back to the
// cellular-health message with a clear route to NuriCell or the full range.
export const closing = {
  title: "Start with your cells.",
  text: "Discover NuriCell, our flagship formula focused on mitochondrial health, or explore the full BiGH range.",
  primary: "Discover NuriCell",
  secondary: "Explore all products",
};

// The three looks offered on September 24 (`?closing=1|2|3` on the demo). "space" returns to the
// hero's deep space with a new picture, a constellation of many cells (GPT Image 2.5, in the hero's
// style: reference/closing-section/originals/close-constellation.png), so the page ends where it
// began without repeating the hero's cell; "light" stands the NuriCell bottle in the
// science section's warm gold light; "field" is a plain statement over a living field of cells.
export type ClosingDesign = "space" | "light" | "field";
export const closingDesigns: Record<string, ClosingDesign> = { 1: "space", 2: "light", 3: "field" };
export const defaultClosing: ClosingDesign = "space";

export const closingImages = {
  space: "/images/closing/space-cells.webp",
  bottle: { src: "/images/stories/v2/bottle-nuricell.webp", width: 493, height: 900 },
};
