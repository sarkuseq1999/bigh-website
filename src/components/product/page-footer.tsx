"use client";

import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import type { ProductPage } from "./product-types";
import styles from "./page-footer.module.css";

export function PageFooter({ product }: { product: ProductPage }) {
  const copy = useCopy();
  return (
    <footer className={styles.footer}>
      <div className={styles.inner}>
        <p className={styles.tagline}>{copy("Stay sharp. Live fully.")}</p>
        <div className={styles.notes}>
          <p>{copy(product.notes.science)}</p>
          <p>{copy(product.caution)}</p>
          <p>{copy(product.notes.fda)}</p>
        </div>
      </div>
      <div className={styles.bottom}>
        <span>
          © {new Date().getFullYear()} {copy("BiGH. Be in Good Health.")}
        </span>
        <span>{copy("Product page design preview")}</span>
        <Link href="/">{copy("Back to the homepage")}</Link>
      </div>
    </footer>
  );
}
