"use client";

import Image from "next/image";
import { contactShadow, shadow } from "@/components/home-v2/look-ink/assets";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { AddToCart } from "../add-to-cart";
import type { ProductPage } from "../product-types";
import { splitName } from "../template-chapters-hero";
import { anchorId } from "../template-chapters-kit";
import styles from "./product-ink.module.css";

// Chapter 1: the giant name parts round the real bottle, which stands in the kit's ink pool (the
// Ink Pool Rule), on paper. Phones stack the name over the bottle. The bottle photo never
// multiplies; only its pools do.
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
        <p className={`${base.label} ${styles.eyebrow}`}>{copy(product.eyebrow)}</p>
        <h1 id="product-name" className={styles.name}>
          <span className={styles.first}>{first}</span>
          <span className={styles.stand} aria-hidden="true">
            <Image
              className={`${base.ink} ${styles.pool}`}
              src={shadow.src}
              alt=""
              width={shadow.width}
              height={shadow.height}
              sizes="(max-width: 959px) 50vw, 300px"
              loading="eager"
            />
            <Image
              className={`${base.ink} ${styles.contact}`}
              src={contactShadow.src}
              alt=""
              width={contactShadow.width}
              height={contactShadow.height}
              sizes="(max-width: 959px) 44vw, 260px"
              loading="eager"
            />
            <Image
              className={styles.bottle}
              src={product.bottle.src}
              alt=""
              width={product.bottle.width}
              height={product.bottle.height}
              sizes="(max-width: 959px) 60vw, 440px"
              preload
              fetchPriority="high"
            />
          </span>
          <span className={styles.second}>{second}</span>
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
            <p className={base.caption}>{copy(product.serving.supply)}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
