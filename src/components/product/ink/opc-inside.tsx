"use client";

import Image from "next/image";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct } from "../product-types";
import { WORDS } from "../template-chapters-model";
import { InkChapter, titleId } from "./ink-chapter";
import styles from "./opc-inside.module.css";

const imageRoot = "/images/products/advanced-opc/ink/field-v1/";
const plates: Record<string, readonly [number, number]> = {
  "grape-seed": [253, 203],
  "pine-bark": [310, 271],
  "red-wine": [280, 285],
  bilberry: [257, 241],
  tea: [272, 246],
  citrus: [271, 261],
  noni: [280, 314],
  lutein: [284, 318],
  melilotus: [269, 336],
};
type Item = InkProduct["ingredients"][number];
const amount = (item: Item) => item.amount.toLocaleString("en-US") + " " + item.unit;

export function OpcInside({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const count = product.ingredients.length;
  const heading = copy("Inside every capsule, {count} ingredients.", {
    count: copy(WORDS[count] ?? String(count)),
  });
  const prefix = "Inside every capsule, ";
  return (
    <InkChapter id="inside" picture={null} className={styles.chapter}>
      <div className={styles.opener}>
        <div className={styles.lead}>
          <p className={styles.kicker}>{copy(product.name)}</p>
          <h2 id={titleId("inside")} className={styles.heading}>
            {heading.startsWith(prefix) ? (
              <>
                <span>{prefix.trim()}</span>{" "}
                <span className={styles.gold}>{heading.slice(prefix.length)}</span>
              </>
            ) : (
              heading
            )}
          </h2>
          <p className={styles.intro}>{copy(product.notes.label)}</p>
        </div>
        <figure className={styles.heroArt}>
          <Image
            src={imageRoot + "grape-study.webp"}
            alt=""
            width={770}
            height={603}
            sizes="(max-width: 680px) 110px, 420px"
          />
          <figcaption>
            <i lang="la">Vitis vinifera</i>
            <span>{copy("Illustration")}</span>
          </figcaption>
        </figure>
      </div>
      <nav className={styles.index} aria-label={copy("In this chapter")}>
        <span className={styles.indexTitle}>{copy("In this chapter")}</span>
        <a href="#opc-botanicals">{copy("Botanicals")}</a>
        <a href="#opc-nutrients">{copy("Vitamins & minerals")}</a>
        <a href="#opc-label">{copy("Label notes")}</a>
      </nav>
      <section className={styles.group} id="opc-botanicals" aria-labelledby="opc-botanicals-title">
        <h3 className={styles.groupHeading} id="opc-botanicals-title">
          <i aria-hidden="true">I.</i>
          {copy("Botanicals")}
        </h3>
        <ol className={styles.plates} role="list">
          {product.ingredients
            .filter((item) => Object.hasOwn(plates, item.key))
            .map((item) => {
              const [width, height] = plates[item.key];
              return (
                <li key={item.key} className={styles.plate}>
                  <div className={styles.stage}>
                    <Image
                      src={imageRoot + item.key + ".webp"}
                      alt=""
                      width={width}
                      height={height}
                      sizes="(max-width: 680px) 110px, 240px"
                    />
                  </div>
                  <div>
                    <h4 className={styles.itemName}>{copy(item.name)}</h4>
                    <p className={styles.amount}>{amount(item)}</p>
                    {item.role && <p className={styles.itemNote}>{copy(item.role)}</p>}
                  </div>
                </li>
              );
            })}
        </ol>
      </section>
      <section
        className={styles.group + " " + styles.nutrients}
        id="opc-nutrients"
        aria-labelledby="opc-nutrients-title"
      >
        <h3 className={styles.groupHeading} id="opc-nutrients-title">
          <i aria-hidden="true">II.</i>
          {copy("Vitamins & minerals")}
        </h3>
        <ol className={styles.vitamins} start={10} role="list">
          {product.ingredients
            .filter((item) => !Object.hasOwn(plates, item.key))
            .map((item) => (
              <li key={item.key} className={styles.vit}>
                <h4 className={styles.itemName}>{copy(item.name)}</h4>
                <p className={styles.amount}>{amount(item)}</p>
                {item.role && <p className={styles.itemNote}>{copy(item.role)}</p>}
              </li>
            ))}
        </ol>
      </section>
      <section className={styles.label} id="opc-label" aria-label={copy("Label notes")}>
        <details className={styles.labelBlock}>
          <summary>
            {copy("Read the complete ingredient list")}
            <span aria-hidden="true">+</span>
          </summary>
          <table className={styles.labelTable}>
            <caption>{copy(product.notes.label)}</caption>
            <thead>
              <tr>
                <th scope="col">{copy("Ingredient")}</th>
                <th scope="col">{copy("Per serving")}</th>
                <th scope="col">{copy("On the label")}</th>
              </tr>
            </thead>
            <tbody>
              {product.ingredients.map((item) => (
                <tr key={item.key}>
                  <th scope="row">{copy(item.name)}</th>
                  <td className={styles.qty}>{amount(item)}</td>
                  <td>{copy(item.form)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </details>
        <p className={styles.small}>{copy(product.otherIngredients)}</p>
        <p className={styles.small}>{copy(product.notes.science)}</p>
      </section>
    </InkChapter>
  );
}
