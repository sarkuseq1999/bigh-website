// NuriCell's chapters, each painting in its own place (Mo picked B, October 19, 2026; mockups
// reference/ink-pages/mockups/nuricell-layout/): from 960px the lantern hangs on the right, the
// capsule sits in the middle of its four ingredients, the books run in from the page's edge, Dr.
// Liu stands on the right of the view west, one painting across the page (Mo picked A2, October 26,
// 2026), the redwood round stands right of its words (October 27, 2026) and the bottle stays on the
// left (nuricell.module.css). The other product pages keep the template's layout. Three of those
// paintings are drawn larger than the template draws them, so their pictures ask for more: the
// numbers here are the stylesheet's.
import type { InkProduct } from "../product-types";
import { pictureSizes } from "./ink-chapter";

export function isNuricell(product: Pick<InkProduct, "slug">) {
  return product.slug === "nuricell";
}

/** The window height the lantern leaves free beside its words (the stylesheet's --picture-height:
 *  the window less this), not the template's 220px. */
const RESERVE = 150;

/** The share of the window (vh) the lighthouse is drawn at over its words, taller than the
 *  template's 46. */
const OVER = 55;

/** Dr. Liu's phone framing: the column's full width up to 640px (nuricell.module.css). */
export const NURICELL_PEOPLE_PHONE_SIZES = "(max-width: 640px) 100vw, 640px";

/** The `sizes` of a NuriCell painting the layout draws larger, or undefined (the template's). */
export function nuricellSizes(
  product: Pick<InkProduct, "slug">,
  chapter: "why" | "people" | "research",
  art: { width: number; height: number },
) {
  if (!isNuricell(product)) return undefined;
  if (chapter === "why") return pictureSizes(art, RESERVE, OVER);
  // Dr. Liu's view west from 960px: as wide as the window (at most the window's height less the
  // bar, times 1.8, on a short wide screen).
  if (chapter === "people") return "100vw";
  // The books: their column plus the gutter, at most 6/11 of (1300px less the 112px gap) + 132px.
  return "(max-width: 959px) 88vw, 780px";
}
