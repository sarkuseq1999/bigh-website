// NuriCell's chapters, each painting in its own place (Mo picked B, October 19, 2026; mockups
// reference/ink-pages/mockups/nuricell-layout/): from 960px the lantern hangs on the right, the
// capsule sits in the middle of its four ingredients, the books run in from the page's edge, Dr.
// Liu stands on the right, the brushed sum goes across the page and the bottle stays on the left
// (nuricell.module.css). The other product pages keep the template's layout. Four of those
// paintings are drawn larger than the template draws them, so their pictures ask for more: the
// numbers here are the stylesheet's.
import type { InkProduct } from "../product-types";
import { pictureSizes } from "./ink-chapter";

export function isNuricell(product: Pick<InkProduct, "slug">) {
  return product.slug === "nuricell";
}

/** The window height the lantern and Dr. Liu leave free beside their words (the stylesheet's
 *  --picture-height: the window less these), not the template's 220px. */
const RESERVE = { why: 150, people: 190 } as const;

/** The `sizes` of a NuriCell painting the layout draws larger, or undefined (the template's). */
export function nuricellSizes(
  product: Pick<InkProduct, "slug">,
  chapter: "why" | "people" | "research" | "sum",
  art: { width: number; height: number },
) {
  if (!isNuricell(product)) return undefined;
  if (chapter === "why" || chapter === "people") return pictureSizes(art, RESERVE[chapter]);
  // The books: their column plus the gutter, at most 6/11 of (1300px less the 112px gap) + 132px.
  if (chapter === "research") return "(max-width: 959px) 88vw, 780px";
  // The brushed sum across the page, at most 940px.
  return "(max-width: 959px) 88vw, 940px";
}
