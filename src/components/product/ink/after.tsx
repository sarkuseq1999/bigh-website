"use client";

import Image from "next/image";
import { shadow } from "@/components/home-v2/look-ink/assets";
import base from "@/components/ink/ink.module.css";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct, ProductSummary } from "../product-types";
import { summaries } from "../products/summaries";
import styles from "./product-ink.module.css";

// After Buy, full width on paper: the questions on hairlines with round toggles, the other bottles
// small in pale pools (each links to its page), then the caution and FDA notes, before the shared
// footer.
export function After({ product }: { product: InkProduct }) {
  const copy = useCopy();
  // Every related product has a page (summaries, not the catalog: the catalog would bring every
  // product's whole page into this page's script).
  const related = product.related
    .map((slug) => summaries.find((summary) => summary.slug === slug))
    .filter((summary): summary is ProductSummary => Boolean(summary));
  return (
    <>
      {product.faq.length > 0 ? (
        <section id="questions" className={styles.after} aria-labelledby="questions-title">
          <div className={base.wrap}>
            <h2 id="questions-title" className={`${base.display} ${styles.heading}`}>
              {copy("Questions")}
            </h2>
            <ul className={styles.faq}>
              {product.faq.map((item) => (
                <li key={item.question}>
                  <details className={styles.question}>
                    <summary className={`${styles.summary} ${styles.faqSummary}`}>
                      <span className={styles.studyTitle}>{copy(item.question)}</span>
                      <span className={styles.toggle} aria-hidden="true">
                        +
                      </span>
                    </summary>
                    <p className={styles.answer}>{copy(item.answer)}</p>
                  </details>
                </li>
              ))}
            </ul>
          </div>
        </section>
      ) : null}
      {related.length > 0 ? (
        <section id="more" className={styles.after} aria-labelledby="more-title">
          <div className={base.wrap}>
            <h2 id="more-title" className={`${base.display} ${styles.heading}`}>
              {copy("More from BiGH")}
            </h2>
            <ul className={styles.more}>
              {related.map((summary) => (
                <li key={summary.slug}>
                  <Link href={`/products/${summary.slug}`} className={styles.moreLink}>
                    <span className={styles.moreStand} aria-hidden="true">
                      <Image
                        className={`${base.ink} ${styles.morePool}`}
                        src={shadow.src}
                        alt=""
                        width={shadow.width}
                        height={shadow.height}
                        sizes="180px"
                      />
                      <Image
                        className={styles.moreBottle}
                        src={summary.bottle.src}
                        alt=""
                        width={summary.bottle.width}
                        height={summary.bottle.height}
                        sizes="160px"
                      />
                    </span>
                    <span className={styles.moreName}>{summary.name}</span>
                    <span className={styles.meta}>{copy(summary.focus)}</span>
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        </section>
      ) : null}
      <div className={`${base.wrap} ${styles.notes}`} data-notes="">
        <p>{copy(product.caution)}</p>
        <p>{copy(product.notes.fda)}</p>
      </div>
    </>
  );
}
