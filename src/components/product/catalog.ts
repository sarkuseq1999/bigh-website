import type { ProductPage, ProductSummary } from "./product-types";
import advancedOpc from "./products/advanced-opc";
import greenBeePropolis from "./products/green-bee-propolis";
import natureCalm from "./products/nature-calm";
import nuricell from "./products/nuricell";
import { summaries } from "./products/summaries";
import turmerific from "./products/turmerific";

export { summaries };

// Every product's page lives in its own file under products/ (September 28, 2026), so a session
// building one product edits only that file. A product whose file is still empty has no page.
const pages: Record<string, ProductPage> = Object.fromEntries(
  [nuricell, greenBeePropolis, advancedOpc, turmerific, natureCalm]
    .filter((page): page is ProductPage => page !== null)
    .map((page) => [page.slug, page]),
);

export const productSlugs = Object.keys(pages);

export function getProduct(slug: string): ProductPage | undefined {
  return pages[slug];
}

export function getSummary(slug: string): ProductSummary | undefined {
  return summaries.find((summary) => summary.slug === slug);
}

/** Product name → its page, for every product that has one (the homepage links these). */
export function productPageLinks(): Record<string, string> {
  return Object.fromEntries(productSlugs.map((slug) => [pages[slug].name, `/products/${slug}`]));
}
