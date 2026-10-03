"use client";

import Image from "next/image";
import { Plus } from "lucide-react";
import { useId, useRef, useState } from "react";
import { useCopy } from "@/i18n/use-copy";
import type { ProductIngredient, ProductPage } from "./product-types";
import { CapsuleCutaway } from "./signature/capsule-cutaway";
import { anchorId, useArrivals, type Chapter } from "./template-chapters-kit";
import styles from "./template-chapters.module.css";

/** Long formulas show this many rows first, then offer the rest. */
const FIRST_ROWS = 6;
const LONG_LIST = 8;
/** Small counts read better as words ("Four ingredients"); larger ones stay figures. */
const COUNT_WORDS = [
  "",
  "One",
  "Two",
  "Three",
  "Four",
  "Five",
  "Six",
  "Seven",
  "Eight",
  "Nine",
  "Ten",
];

function formatAmount(ingredient: ProductIngredient) {
  return ingredient.amount.toLocaleString("en-US");
}

// Chapter 3, what's inside. The product's signature moment when it has one (NuriCell: the capsule
// opens), then every ingredient with its amount, label form and role, the full label on request,
// and the note that the roles describe the nutrients in general.
export function InsideChapter({
  product,
  chapter,
  reduced,
}: {
  product: ProductPage;
  chapter: Chapter;
  reduced: boolean;
}) {
  const copy = useCopy();
  const root = useRef<HTMLElement>(null);
  const titleId = useId();
  const moreId = useId();
  const labelId = useId();
  const [showAll, setShowAll] = useState(false);
  const [labelOpen, setLabelOpen] = useState(false);
  useArrivals(root, reduced);

  const long = product.ingredients.length > LONG_LIST;
  // A single-ingredient formula (Green Bee Propolis) shows its one amount large, on its own.
  const single = product.ingredients.length === 1;
  const first = long ? product.ingredients.slice(0, FIRST_ROWS) : product.ingredients;
  const rest = long ? product.ingredients.slice(FIRST_ROWS) : [];
  const pictured = product.ingredients.some((ingredient) => ingredient.picture);

  const row = (ingredient: ProductIngredient) => (
    <li key={ingredient.key} className={styles.ingredient} data-reveal>
      {pictured && (
        <span className={styles.ingredientPicture} aria-hidden="true">
          {ingredient.picture && (
            <Image
              src={ingredient.picture.src}
              width={ingredient.picture.width}
              height={ingredient.picture.height}
              alt=""
              sizes="(max-width: 860px) 60px, 88px"
            />
          )}
        </span>
      )}
      <p className={styles.amount}>
        {formatAmount(ingredient)}
        <span className={styles.unit}>{ingredient.unit}</span>
      </p>
      <div className={styles.ingredientText}>
        <h3 className={styles.ingredientName}>{copy(ingredient.name)}</h3>
        {ingredient.form !== ingredient.name && (
          <p className={styles.ingredientForm}>
            {copy("On the label: {form}", { form: copy(ingredient.form) })}
          </p>
        )}
      </div>
      {ingredient.role && <p className={styles.ingredientRole}>{copy(ingredient.role)}</p>}
    </li>
  );

  return (
    <section
      ref={root}
      id={anchorId(chapter.id)}
      data-chapter={chapter.id}
      data-tone={chapter.tone}
      tabIndex={-1}
      aria-labelledby={titleId}
      className={`${styles.chapter} ${styles.inside}`}
    >
      {/* The signature is full-bleed with its own sticky stage: nothing around it may clip or transform. */}
      {product.signature === "capsule" && <CapsuleCutaway product={product} />}
      <div className={styles.insideBody}>
        <header className={styles.chapterHead}>
          <h2 id={titleId} className={styles.statement} data-heading>
            {copy("What’s inside")}
          </h2>
          <p className={styles.lede} data-reveal>
            {product.ingredients.length === 1
              ? copy("One ingredient, and the amount in each serving.")
              : copy("{count} ingredients, and the amount of each in one serving.", {
                  count: COUNT_WORDS[product.ingredients.length]
                    ? copy(COUNT_WORDS[product.ingredients.length])
                    : product.ingredients.length,
                })}
          </p>
        </header>
        {first.length > 0 && (
          <ol
            className={`${styles.ingredients} ${single ? styles.single : ""}`}
            data-pictured={pictured || undefined}
          >
            {first.map(row)}
          </ol>
        )}
        {rest.length > 0 && (
          <ol
            id={moreId}
            className={styles.ingredients}
            data-pictured={pictured || undefined}
            start={first.length + 1}
            hidden={!showAll}
          >
            {rest.map(row)}
          </ol>
        )}
        <div className={styles.insideActions}>
          {rest.length > 0 && (
            <button
              type="button"
              className={styles.disclosure}
              aria-expanded={showAll}
              aria-controls={moreId}
              onClick={() => setShowAll((value) => !value)}
            >
              {showAll
                ? copy("Show fewer ingredients")
                : copy("Show all {count} ingredients", { count: product.ingredients.length })}
              <Plus size={20} strokeWidth={2} aria-hidden="true" />
            </button>
          )}
          <button
            type="button"
            className={styles.disclosure}
            aria-expanded={labelOpen}
            aria-controls={labelId}
            onClick={() => setLabelOpen((value) => !value)}
          >
            {copy("See the full label")}
            <Plus size={20} strokeWidth={2} aria-hidden="true" />
          </button>
        </div>
        <div id={labelId} className={`${styles.labelPanel} ${styles.panel}`} hidden={!labelOpen}>
          <table className={styles.labelTable}>
            <caption>{copy(product.notes.label)}</caption>
            <thead>
              <tr>
                <th scope="col">{copy("Ingredient")}</th>
                <th scope="col">{copy("Per serving")}</th>
              </tr>
            </thead>
            <tbody>
              {product.ingredients.map((ingredient) => (
                <tr key={ingredient.key}>
                  <th scope="row">{copy(ingredient.form)}</th>
                  <td>
                    {formatAmount(ingredient)} {ingredient.unit}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          <p className={styles.other}>{copy(product.otherIngredients)}</p>
        </div>
        <p className={styles.note} data-reveal>
          {copy(product.notes.science)}
        </p>
      </div>
    </section>
  );
}
