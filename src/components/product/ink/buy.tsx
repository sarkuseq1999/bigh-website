"use client";

import Image from "next/image";
import { contactShadow } from "@/components/home-v2/look-ink/assets";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { AddToCart } from "../add-to-cart";
import type { InkProduct } from "../product-types";
import { InkChapter, titleId } from "./ink-chapter";
import styles from "./product-ink.module.css";

const EYEBROW_ID = `${titleId("buy")}-eyebrow`;

// Chapter 7: the real bottle standing on one bold brush stroke (Mo, round 6). The stroke and the
// contact shadow multiply onto the paper; the bottle photo never does, so this figure is not a
// blend group (data-stand) and not sticky. The heading is the product's name, which the opening's
// region is named after too, so this region is named by the eyebrow and the heading together
// ("Our flagship formula NuriCell"): one landmark name each.
export function Buy({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const stroke = product.ink.buy.stroke;
  return (
    <InkChapter
      id="buy"
      labelledBy={`${EYEBROW_ID} ${titleId("buy")}`}
      picture={
        <figure className={styles.buyStand} data-picture="" data-stand="">
          <Image
            className={`${base.ink} ${styles.stroke}`}
            src={stroke.src}
            alt=""
            width={stroke.width}
            height={stroke.height}
            sizes="(max-width: 959px) 88vw, 560px"
            data-bloom="waiting"
          />
          <Image
            className={`${base.ink} ${styles.buyContact}`}
            src={contactShadow.src}
            alt=""
            width={contactShadow.width}
            height={contactShadow.height}
            sizes="200px"
          />
          <Image
            className={styles.buyBottle}
            src={product.bottle.src}
            alt={copy("{name} bottle", { name: product.name })}
            width={product.bottle.width}
            height={product.bottle.height}
            sizes="(max-width: 959px) 80vw, 470px"
          />
        </figure>
      }
    >
      <p id={EYEBROW_ID} className={`${base.label} ${styles.label}`}>
        {copy(product.eyebrow)}
      </p>
      <h2 id={titleId("buy")} className={`${base.display} ${styles.buyName}`}>
        {product.name}
      </h2>
      <p className={styles.focus}>{copy(product.focus)}</p>
      <dl className={styles.rows}>
        <div>
          <dt>{copy("How to take it")}</dt>
          <dd>{copy(product.serving.use)}</dd>
        </div>
        <div>
          <dt>{copy("In each bottle")}</dt>
          <dd>{copy(product.serving.supply)}</dd>
        </div>
      </dl>
      <AddToCart wide />
      {product.credit ? <p className={styles.small}>{copy(product.credit)}</p> : null}
    </InkChapter>
  );
}
