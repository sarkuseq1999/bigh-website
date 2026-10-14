"use client";

import Image from "next/image";
import type { CSSProperties } from "react";
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

/**
 * Switzer's advance widths at the name's weight (650) and tracking (-0.045em), in ems, measured in
 * the browser on October 14, 2026. The opening was set for "Nuri" and "Cell" (1.76 and 1.60 ems);
 * a longer name ("Green Bee" 4.46) has to be set smaller to fit. Measured, not read from the page,
 * so the name is the right size from the first paint, with nothing moving once the page loads.
 */
// prettier-ignore
const EMS: Record<string, number> = {
  " ": 0.145, A: 0.655, B: 0.603, C: 0.649, D: 0.663, E: 0.541, F: 0.534, G: 0.669, H: 0.662,
  I: 0.231, J: 0.515, K: 0.622, L: 0.499, M: 0.842, N: 0.662, O: 0.712, P: 0.578, Q: 0.712,
  R: 0.598, S: 0.579, T: 0.584, U: 0.644, V: 0.655, W: 1.01, X: 0.627, Y: 0.589, Z: 0.577,
  a: 0.539, b: 0.546, c: 0.514, d: 0.546, e: 0.539, f: 0.266, g: 0.546, h: 0.544, i: 0.206,
  j: 0.206, k: 0.52, l: 0.206, m: 0.836, n: 0.544, o: 0.539, p: 0.546, q: 0.546, r: 0.356,
  s: 0.492, t: 0.298, u: 0.538, v: 0.517, w: 0.821, x: 0.509, y: 0.518, z: 0.481,
};
const ems = (text: string) => [...text].reduce((sum, c) => sum + (EMS[c] ?? 0.6), 0);

/** NuriCell's halves and bottle column, in name-sizes: the opening as approved (scale 1). */
const NURI = { half: 1.762, stand: 1.66 };

/**
 * How a name of these halves is set: its scale against NuriCell's size (the columns are equal, so
 * the longer half decides), the bottle's column in name-sizes (wider for a long name, so the
 * bottle keeps its presence beside smaller letters: 2.6 for "Green Bee", chosen on the page on
 * October 14 over 1.66, which left a small bottle), and on a phone the size that fits the column
 * (84.6vw, with 3% to spare): the longer half for a two-word name, which stacks its halves, the
 * whole word for one that stays one word. NuriCell's own name needs none of it (null; the small
 * tolerance keeps it so whatever the sum's last digit).
 */
export function nameFit(first: string, second: string, spaced: boolean) {
  const half = Math.max(ems(first), ems(second));
  if (half <= NURI.half + 0.005) return null;
  const stand = NURI.stand + (half - NURI.half) * 0.348;
  const scale = (2 * NURI.half + NURI.stand) / ((2 * half + stand) * 1.03);
  const line = spaced ? half : ems(first) + ems(second);
  return { scale, stand, phone: 84.6 / (line * 1.03) };
}

// Chapter 1: the giant name parts round the real bottle, centred on the letters, on bare paper (Mo,
// October 10: no eyebrow over the name, no ink pool under the bottle). Phones stack the name over
// the bottle. Under it (Mo, October 12-13, after Timeline's and Seed's buy boxes): under "Nuri" the
// headline and the purpose, which carries the same ink line as the highlights; under "Cell", the
// highlights either side of one ink line, a "One bottle" card with the supply and the About page's
// promise, a wide Add to cart and the refund line.
export function Opening({ product }: { product: ProductPage }) {
  const copy = useCopy();
  const [first, second] = product.nameHalves ?? splitName(product.name);
  // A two-word name ("Green Bee Propolis") stacks its halves on a phone; one word ("NuriCell")
  // stays one word.
  const spaced = product.name.startsWith(`${first} `);
  const fit = nameFit(first, second, spaced);
  return (
    <section
      id={anchorId("overview")}
      className={styles.opening}
      data-chapter="overview"
      aria-labelledby="product-name"
      data-name-fit={fit ? "long" : undefined}
      data-spaced={spaced || undefined}
      style={
        fit
          ? ({
              ["--name-scale" as string]: fit.scale.toFixed(4),
              ["--stand-ratio" as string]: fit.stand.toFixed(3),
              ["--phone-name" as string]: `${fit.phone.toFixed(2)}vw`,
            } as CSSProperties)
          : undefined
      }
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
