"use client";

import Image from "next/image";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { AddToCart } from "../add-to-cart";
import type { ProductPage } from "../product-types";
import { anchorId, splitName } from "../template-chapters-model";
import { keepTogether } from "./ink-chapter";
import styles from "./product-ink.module.css";

// Chapter 1: the giant name parts round the real bottle, centred on the letters, on bare paper (Mo,
// October 10: no eyebrow over the name, no ink pool under the bottle). Phones stack the name over
// the bottle.
export function Opening({ product }: { product: ProductPage }) {
  const copy = useCopy();
  const [first, second] = product.nameHalves ?? splitName(product.name);
  return (
    <section
      id={anchorId("overview")}
      className={styles.opening}
      data-chapter="overview"
      aria-labelledby="product-name"
    >
      <div className={base.wrap}>
        {/* The name as one word for assistive tech: the two visible halves sit in separate grid
            cells, which Chrome reads as "Nuri Cell". */}
        <h1 id="product-name" className={styles.name}>
          <span className={base.visuallyHidden}>{product.name}</span>
          <span className={styles.first} aria-hidden="true">
            {first}
          </span>
          <span className={styles.stand} aria-hidden="true">
            {/* The largest picture on a phone or tablet (on a wide screen it is the menu bar's
                paper): loaded at once and first. Next 16's docs prefer loading="eager" with
                fetchPriority to `preload`, which they advise against when the largest picture
                changes with the window and alongside fetchPriority. */}
            <Image
              className={styles.bottle}
              src={product.bottle.src}
              alt=""
              width={product.bottle.width}
              height={product.bottle.height}
              sizes="(max-width: 959px) 64vw, 29vw"
              loading="eager"
              fetchPriority="high"
            />
          </span>
          <span className={styles.second} aria-hidden="true">
            {second}
          </span>
        </h1>
        <div className={styles.openingWords}>
          <div>
            <p className={styles.headline}>
              {product.headlineLines.map((line) => (
                <span key={line}>{copy(line)}</span>
              ))}
            </p>
            <p className={styles.text}>{copy(product.purpose)}</p>
          </div>
          <div className={styles.openingBuy}>
            <ul className={styles.highlights}>
              {product.highlights.map((item) => (
                <li key={item}>{copy(item)}</li>
              ))}
            </ul>
            <AddToCart />
            <p className={base.caption}>{keepTogether(copy(product.serving.supply))}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
