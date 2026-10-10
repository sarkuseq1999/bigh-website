"use client";

import type { CSSProperties } from "react";
import { useCopy } from "@/i18n/use-copy";
import { PageFooter } from "./page-footer";
import type { ProductPage } from "./product-types";
import { SiteHeader } from "./site-header";
import { TemplateChapters } from "./template-chapters";
import styles from "./product-page.module.css";

// The product page: the Chapters template Mo chose on September 25, 2026, opening with "Big name"
// and set in Switzer (both picked September 28, 2026). One template serves every product.

export type TemplateProps = { product: ProductPage };

export function ProductPageView({ product }: { product: ProductPage }) {
  const copy = useCopy();

  // Each product lends the template its own colours.
  const colours = {
    "--tint": product.tint,
    "--product-ink": product.inkColor,
    "--accent": product.accent,
  } as CSSProperties;

  return (
    <div className={styles.page} style={colours}>
      <a href="#main-content" className={styles.skip}>
        {copy("Skip to content")}
      </a>
      <SiteHeader tone="light" />
      <main id="main-content">
        <TemplateChapters product={product} />
      </main>
      <PageFooter product={product} />
    </div>
  );
}
