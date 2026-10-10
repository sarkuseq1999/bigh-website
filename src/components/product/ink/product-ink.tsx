"use client";

import { InkPage } from "@/components/ink/ink-page";
import type { InkProduct } from "../product-types";
import { Inside } from "./inside";
import { Opening } from "./opening";
import styles from "./product-ink.module.css";
import { Research } from "./research";
import { Why } from "./why";

// The product page in Ink & Gold (NuriCell first, October 9, 2026; spec
// docs/superpowers/specs/2026-10-09-nuricell-ink-design.md; mockups
// reference/ink-pages/mockups/nuricell-ink/). The shared theme (paper, menu bar, crane footer,
// bloom); its own layout: seven chapters, each one painting beside its words, the lantern's light
// coming on in "Why it matters". Every word of the product's data stays.
export function ProductInkPage({ product }: { product: InkProduct }) {
  return (
    <InkPage current="products" className={styles.page}>
      {(motion) => (
        <div data-product-ink={product.slug}>
          <Opening product={product} />
          <Why product={product} motion={motion} />
          <Inside product={product} />
          {product.studies.length > 0 ? <Research product={product} /> : null}
        </div>
      )}
    </InkPage>
  );
}
