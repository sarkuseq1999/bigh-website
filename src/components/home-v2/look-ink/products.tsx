"use client";

import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { useState, type FocusEvent, type ReactNode } from "react";
import { ProductAction } from "@/components/home/product-action";
import { useCopy } from "@/i18n/use-copy";
import { Sentences } from "../chrome";
import { products, productsIntro, type HomeProduct } from "../content";
import { useHomeDialogs } from "../dialogs";
import { contactShadow, shadow } from "./assets";
import base from "./look-ink.module.css";
import styles from "./products.module.css";

// "Find your starting point." A showroom, not a shelf: the chosen bottle (the approved
// photographs, never generated) stands large on the stage in its gathered ink pool, on the brush
// line that is its ground, with its words beside it at display size; NuriCell is chosen first.
// Under the stage the five stand small in a quiet picker row (on one column it comes straight
// after the big bottle, so what you tap and what changes share the window; it comes before the
// words in the page's order too, so choosing comes before discovering). Pointing at one (or
// reaching it with the keyboard) previews it on the stage; choosing it (click, tap, Enter) keeps
// it. The big bottle and the Discover button go to the shown product's page (ProductAction), so
// every product page stays one click away.
export function Products() {
  const copy = useCopy();
  const dialogs = useHomeDialogs();
  const [chosen, setChosen] = useState(0);
  const [preview, setPreview] = useState<number | null>(null);
  const shown = preview ?? chosen;
  const product = products[shown];

  const leave = (event: FocusEvent<HTMLDivElement>) => {
    if (!event.currentTarget.contains(event.relatedTarget as Node | null)) setPreview(null);
  };

  return (
    <section
      id="products"
      className={styles.products}
      aria-labelledby="products-title"
      data-brush="products"
    >
      <div className={`${base.wrap} ${styles.inner}`}>
        <header className={styles.head}>
          <h2 id="products-title" className={base.display}>
            {copy(productsIntro.headline)}
          </h2>
          <div className={styles.lede}>
            <p
              className={`${base.station} ${styles.station}`}
              data-station=""
              data-side="right"
              data-brush="st-products"
            >
              {copy(productsIntro.title)}
            </p>
            <p className={`${base.body} ${styles.intro}`}>{copy(productsIntro.text)}</p>
          </div>
        </header>

        <div className={styles.show} data-brush="stage">
          {/* The brush line comes down here, between the bottle and its words (brush-route.ts),
              and turns under the bottle as its ground. */}
          <span className={styles.spine} aria-hidden="true" data-brush="product-spine" />
          <ProductAction
            name={product.name}
            onOpen={() => dialogs.openProduct(product.index)}
            className={styles.stand}
          >
            {/* Keyed by the shown bottle, so its ink gathers again each time it changes. */}
            <Image
              key={`pool-${shown}`}
              className={`${base.ink} ${styles.pool}`}
              src={shadow.src}
              alt=""
              width={shadow.width}
              height={shadow.height}
              sizes="(max-width: 720px) 46vw, 330px"
            />
            <Image
              className={`${base.ink} ${styles.contact}`}
              src={contactShadow.src}
              alt=""
              width={contactShadow.width}
              height={contactShadow.height}
              sizes="(max-width: 720px) 40vw, 280px"
            />
            {products.map((item, i) => (
              <Image
                key={item.name}
                className={styles.big}
                data-shown={i === shown}
                src={item.image}
                alt={i === shown ? copy("{name} bottle", { name: item.name }) : ""}
                width={item.size.width}
                height={item.size.height}
                sizes="(max-width: 720px) 70vw, (max-width: 899px) 46vw, 490px"
                loading="eager"
              />
            ))}
          </ProductAction>
        </div>

        <div
          className={styles.picker}
          role="group"
          aria-label={copy("BiGH products")}
          data-brush="bottles"
          onMouseLeave={() => setPreview(null)}
          onBlur={leave}
        >
          {products.map((item, i) => (
            <button
              key={item.name}
              type="button"
              className={styles.pick}
              aria-pressed={chosen === i}
              aria-controls="ink-product-panel"
              data-shown={shown === i}
              onMouseEnter={() => setPreview(i)}
              onFocus={() => setPreview(i)}
              onClick={() => setChosen(i)}
            >
              <span className={styles.mini}>
                <Image
                  className={`${base.ink} ${styles.miniPool}`}
                  src={shadow.src}
                  alt=""
                  width={shadow.width}
                  height={shadow.height}
                  sizes="100px"
                />
                <Image
                  className={`${base.ink} ${styles.miniContact}`}
                  src={contactShadow.src}
                  alt=""
                  width={contactShadow.width}
                  height={contactShadow.height}
                  sizes="80px"
                />
                <Image
                  className={styles.miniBottle}
                  src={item.image}
                  alt=""
                  width={item.size.width}
                  height={item.size.height}
                  sizes="(max-width: 720px) 34vw, 140px"
                  loading="eager"
                />
              </span>
              <span className={styles.name}>{copy(item.name)}</span>
            </button>
          ))}
        </div>

        {/* The shown product's words over five invisible copies (one per product), so the stage
            keeps the tallest one's height and nothing under it moves while you preview. */}
        <div className={styles.words}>
          <div id="ink-product-panel" aria-live="polite">
            <Words product={product} keyed={shown}>
              <ProductAction
                name={product.name}
                onOpen={() => dialogs.openProduct(product.index)}
                className={base.pill}
              >
                {copy("Discover {name}", { name: product.name })}{" "}
                <ArrowRight size={18} aria-hidden="true" />
              </ProductAction>
            </Words>
          </div>
          {products.map((item) => (
            <div key={item.name} className={styles.ghost} aria-hidden="true" inert>
              <Words product={item}>
                <span className={base.pill}>
                  {copy("Discover {name}", { name: item.name })}{" "}
                  <ArrowRight size={18} aria-hidden="true" />
                </span>
              </Words>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

/** One product's words: headline, focus, highlights, description, credit and its action. Keyed
 *  by the shown product, the words settle in each time it changes. */
function Words({
  product,
  keyed,
  children,
}: {
  product: HomeProduct;
  keyed?: number;
  children: ReactNode;
}) {
  const copy = useCopy();
  return (
    <>
      <div key={`head-${keyed}`} className={styles.panelHead}>
        <h3 className={styles.headline}>
          <Sentences text={copy(product.headline)} />
        </h3>
        <p className={styles.focus}>{copy(product.focus)}</p>
        <ul className={styles.highlights}>
          {product.highlights.map((highlight) => (
            <li key={highlight}>{copy(highlight)}</li>
          ))}
        </ul>
      </div>
      <div key={`body-${keyed}`} className={styles.panelBody}>
        <p className={base.body}>{copy(product.description)}</p>
        <p className={styles.credit}>{copy(product.credit)}</p>
        {children}
      </div>
    </>
  );
}
