"use client";

import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { useState } from "react";
import { ProductAction } from "@/components/home/product-action";
import { useCopy } from "@/i18n/use-copy";
import { products, productsIntro } from "../content";
import { useHomeDialogs } from "../dialogs";
import { contactShadow, shadow } from "./assets";
import base from "./look-ink.module.css";
import styles from "./products.module.css";

// "Find your starting point." The five real bottles (the approved photographs, never generated)
// each stand in their own ink-wash pool, seated on its darkest core with a small contact shadow at
// the base, as the comps show; the brush line runs beneath the row, dividing it from the chosen
// product's words. Each bottle picture is the product's
// action (NuriCell opens its page, the rest the product preview); pointing at one, or choosing its
// name, shows its headline, words, credit and Discover button below.
export function Products() {
  const copy = useCopy();
  const dialogs = useHomeDialogs();
  const [active, setActive] = useState(0);
  const product = products[active];

  return (
    <section
      id="products"
      className={styles.products}
      aria-labelledby="products-title"
      data-brush="products"
    >
      <div className={`${base.wrap} ${styles.inner}`}>
        <header className={styles.head}>
          <p
            className={`${base.station} ${styles.station}`}
            data-station=""
            data-side="left"
            data-brush="st-products"
          >
            {copy(productsIntro.title)}
          </p>
          <h2 id="products-title" className={`${base.display} ${styles.title}`}>
            {copy(productsIntro.headline)}
          </h2>
          <p className={`${base.body} ${styles.intro}`}>{copy(productsIntro.text)}</p>
        </header>

        <div
          className={styles.row}
          role="group"
          aria-label={copy("BiGH products")}
          data-brush="bottles"
        >
          {products.map((item, i) => (
            <div key={item.name} className={styles.item} data-active={active === i}>
              <ProductAction
                name={item.name}
                onOpen={() => dialogs.openProduct(item.index)}
                className={styles.bottle}
              >
                <span
                  className={styles.stand}
                  onMouseEnter={() => setActive(i)}
                  onFocus={() => setActive(i)}
                >
                  <Image
                    className={`${base.ink} ${styles.shadow}`}
                    src={shadow.src}
                    alt=""
                    width={shadow.width}
                    height={shadow.height}
                    sizes="240px"
                  />
                  <Image
                    className={`${base.ink} ${styles.contact}`}
                    src={contactShadow.src}
                    alt=""
                    width={contactShadow.width}
                    height={contactShadow.height}
                    sizes="160px"
                  />
                  <Image
                    className={styles.image}
                    src={item.image}
                    alt={copy("{name} bottle", { name: item.name })}
                    width={item.size.width}
                    height={item.size.height}
                    sizes="(max-width: 720px) 52vw, 290px"
                    loading="eager"
                  />
                </span>
              </ProductAction>
              <button
                type="button"
                aria-pressed={active === i}
                aria-controls="ink-product-panel"
                className={styles.name}
                onClick={() => setActive(i)}
              >
                {copy(item.name)}
              </button>
            </div>
          ))}
        </div>

        <div
          id="ink-product-panel"
          className={styles.panel}
          aria-live="polite"
          data-brush="product-panel"
        >
          {/* Where the brush line passes these words, out in the margin (brush-route.ts). */}
          <span className={styles.pass} aria-hidden="true" data-brush="product-pass" />
          <div key={`head-${active}`} className={styles.panelHead}>
            <h3 className={styles.headline}>{copy(product.headline)}</h3>
            <p className={styles.focus}>{copy(product.focus)}</p>
            <ul className={styles.highlights}>
              {product.highlights.map((highlight) => (
                <li key={highlight}>{copy(highlight)}</li>
              ))}
            </ul>
          </div>
          <div key={`body-${active}`} className={styles.panelBody}>
            <p className={base.body}>{copy(product.description)}</p>
            <p className={styles.credit}>{copy(product.credit)}</p>
            <ProductAction
              name={product.name}
              onOpen={() => dialogs.openProduct(product.index)}
              className={base.pill}
            >
              {copy("Discover {name}", { name: product.name })}{" "}
              <ArrowRight size={18} aria-hidden="true" />
            </ProductAction>
          </div>
        </div>
      </div>
    </section>
  );
}
