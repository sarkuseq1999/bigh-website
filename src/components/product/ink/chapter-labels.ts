// The small line over a chapter's heading ("Why antioxidants matter" over "A balance worth
// keeping."). Mo found it strange on NuriCell three times (October 26, 2026) and it came off there;
// on November 16, 2026, shown before and after on the live pages, he said yes to taking it off
// Advanced OPC Formula, Turmerific and Nature Calm too. Green Bee Propolis keeps it: its labels are
// numbered ("01 | Why green propolis"), part of its own chapter system with the index row under its
// opening (propolis.module.css counts them). The buy chapter's line is the product's tagline and is
// not one of these.
import type { InkProduct } from "../product-types";

export function showsChapterLabels(product: Pick<InkProduct, "slug">) {
  return product.slug === "green-bee-propolis";
}
