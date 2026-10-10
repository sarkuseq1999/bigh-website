"use client";

import { ProductPagesProvider } from "@/components/home/product-action";
import { SiteDialogs } from "@/components/ink/dialogs";
import { InkPage } from "@/components/ink/ink-page";
import type { InkProduct } from "../product-types";
import { After } from "./after";
import { Buy } from "./buy";
import { Daily } from "./daily";
import { Inside } from "./inside";
import { Opening } from "./opening";
import { People } from "./people";
import styles from "./product-ink.module.css";
import { Research } from "./research";
import { Why } from "./why";

// The product page in Ink & Gold (NuriCell first, October 9, 2026; spec
// docs/superpowers/specs/2026-10-09-nuricell-ink-design.md; mockups
// reference/ink-pages/mockups/nuricell-ink/). The shared theme (paper, menu bar, crane footer,
// bloom); its own layout: seven chapters, each one painting beside its words, the lantern's light
// coming on in "Why it matters", then the questions, the other products and the notes. Every word
// of the product's data stays.
export function ProductInkPage({ product }: { product: InkProduct }) {
  return (
    <InkPage current="products" className={styles.page}>
      {(motion) => (
        <div data-product-ink={product.slug}>
          <Opening product={product} />
          <Why product={product} motion={motion} />
          <Inside product={product} />
          {product.studies.length > 0 ? <Research product={product} /> : null}
          {product.people.length > 0 ? <People product={product} /> : null}
          <Daily product={product} />
          <Buy product={product} />
          <After product={product} />
        </div>
      )}
    </InkPage>
  );
}

/** The ink page as the product route renders it: the shared header's sheets and the product links
 *  need the same providers as About (`pages`: product name → its page, read on the server). */
export function ProductInkRoute({
  product,
  pages,
}: {
  product: InkProduct;
  pages: Record<string, string>;
}) {
  return (
    <ProductPagesProvider pages={pages}>
      <SiteDialogs>
        <ProductInkPage product={product} />
      </SiteDialogs>
    </ProductPagesProvider>
  );
}
