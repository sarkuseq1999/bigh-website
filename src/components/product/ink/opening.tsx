"use client";

import Image from "next/image";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { AddToCart } from "../add-to-cart";
import type { ProductPage } from "../product-types";
import { anchorId, splitName } from "../template-chapters-model";
import { keepTogether } from "./ink-chapter";
import styles from "./product-ink.module.css";

// The promise from the About page ("What you can count on"), shown as a badge: its catalogs end it
// with a full stop, which a badge drops.
const PROMISE = "45 days to decide.";
const REFUND = "Not right for you? Send it back for a refund.";

const seal = (
  <svg viewBox="0 0 20 20" width="15" height="15" aria-hidden="true" focusable="false">
    <circle cx="10" cy="10" r="8.2" fill="none" stroke="currentColor" strokeWidth="1.6" />
    <path
      d="M6.2 10.3l2.5 2.5 5-5.4"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
    />
  </svg>
);

// Chapter 1: the giant name parts round the real bottle, centred on the letters, on bare paper (Mo,
// October 10: no eyebrow over the name, no ink pool under the bottle). Phones stack the name over
// the bottle. Under it (Mo, October 12, after Timeline's and Seed's buy boxes): the words under
// "Nuri" with the formulator's credit and painted face; under "Cell", the highlights either side of
// one ink line, a "One bottle" card with the supply and the About page's promise, a wide Add to
// cart and the refund line.
export function Opening({ product }: { product: ProductPage }) {
  const copy = useCopy();
  const [first, second] = product.nameHalves ?? splitName(product.name);
  const lead = product.people[0];
  const face = lead?.painting;
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
            {product.credit && lead ? (
              <div className={styles.credit}>
                {face ? (
                  <span className={styles.creditFace} aria-hidden="true">
                    <Image
                      src={face.src}
                      alt=""
                      width={face.width}
                      height={face.height}
                      sizes="140px"
                    />
                  </span>
                ) : null}
                <p>
                  <span className={styles.creditName}>{copy(product.credit)}</span>
                  <span className={styles.creditTitle}>{copy(lead.title)}</span>
                </p>
              </div>
            ) : null}
          </div>
          <div className={styles.openingBuy}>
            <ul className={styles.highlights}>
              {product.highlights.map((item) => (
                <li key={item}>{copy(item)}</li>
              ))}
            </ul>
            <div className={styles.bottleCard}>
              {product.ink?.supply ? (
                <Image
                  className={styles.bottleCardPicture}
                  src={product.ink.supply.src}
                  alt=""
                  width={product.ink.supply.width}
                  height={product.ink.supply.height}
                  sizes="96px"
                />
              ) : null}
              <p className={styles.bottleCardName}>{copy("One bottle")}</p>
              <p className={styles.bottleCardSupply}>
                {keepTogether(copy(product.serving.supply))}
              </p>
              <p className={styles.bottleCardDaily}>
                {copy("{count} a day", { count: product.serving.capsules })}
              </p>
              <p className={styles.promise}>
                {seal}
                {copy(PROMISE).replace(/[.。]$/, "")}
              </p>
            </div>
            <AddToCart wide />
            <p className={styles.refund}>{copy(REFUND)}</p>
          </div>
        </div>
      </div>
    </section>
  );
}
