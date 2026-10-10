"use client";

import dynamic from "next/dynamic";
import type { ProductPage } from "./product-types";

// Each product page uses one of two templates: the ink page (a product with `ink`, NuriCell first,
// October 9, 2026) or Chapters (the other four). A Server Component that imports both ships both
// to every product page, and Next does not code-split a Server Component's dynamic import of a
// Client Component (node_modules/next/dist/docs/01-app/02-guides/lazy-loading.md). So this Client
// Component loads each template with next/dynamic: its own chunks, fetched only by the pages that
// use it, still rendered on the server (ssr is on), so the page arrives whole without scripts.
const InkTemplate = dynamic(() => import("./ink/product-ink").then((m) => m.ProductInkRoute));
const ChaptersTemplate = dynamic(() => import("./product-page").then((m) => m.ProductPageView));

export function ProductTemplate({
  product,
  pages = {},
}: {
  product: ProductPage;
  /** Product name → its page (the ink page's header and links); read on the server. */
  pages?: Record<string, string>;
}) {
  if (product.ink) return <InkTemplate product={{ ...product, ink: product.ink }} pages={pages} />;
  return <ChaptersTemplate product={product} />;
}
