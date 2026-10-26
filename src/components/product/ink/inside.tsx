"use client";

import { Fragment } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct, ProductSynergy } from "../product-types";
import { WORDS } from "../template-chapters-model";
import { InkChapter, InkFigure, titleId } from "./ink-chapter";
import { nuricellGold } from "./nuricell-gold";
import inside from "./nuricell-inside.module.css";
import { isNuricell } from "./nuricell-layout";
import { NuricellLeaf } from "./nuricell-leaf";
import { NuricellScenes } from "./nuricell-scenes";
import styles from "./product-ink.module.css";

// Chapter 3: the capsule open, its four heaps sized by amount, beside the ingredients (amount,
// name, what it does, the label's form when it differs) and how they work together. A
// single-ingredient formula (Green Bee Propolis) says so in the singular. NuriCell's (Mo picked 1A,
// October 26, 2026): no label over the heading (it said what the heading says), the amounts' "per
// serving of 3 capsules" right under the heading, its gold leaf moving (nuricell-leaf.tsx), the
// label's other lines as a card, and the pairs as scenes (nuricell-scenes.tsx), whose note at the
// chapter's end now also says what notes.science said.
export function Inside({ product, motion }: { product: InkProduct; motion: boolean }) {
  const copy = useCopy();
  const count = product.ingredients.length;
  const names = Object.fromEntries(product.ingredients.map((item) => [item.key, item.name]));
  const own = isNuricell(product);
  // NuriCell's picture is the painting without its leaf; the leaf is laid over it, and moves.
  const art = own
    ? { ...product.ink.inside, src: nuricellGold.capsule.ink.src, gold: undefined }
    : product.ink.inside;
  return (
    <InkChapter
      id="inside"
      picture={
        <InkFigure art={art} alt={product.ink.inside.alt}>
          {own ? <NuricellLeaf motion={motion} /> : null}
        </InkFigure>
      }
    >
      {own ? null : <p className={`${base.label} ${styles.label}`}>{copy("What’s inside")}</p>}
      <h2 id={titleId("inside")} className={`${base.display} ${styles.heading}`}>
        {count === 1
          ? copy("Inside every capsule, one ingredient.")
          : copy("Inside every capsule, {count} ingredients.", {
              count: copy(WORDS[count] ?? String(count)),
            })}
      </h2>
      {/* The rows are laid out as a grid (the amount beside the name, what it does under the
          name), which some browsers treat as the end of the table's meaning, so the table's parts
          name their own roles; NuriCell's table itself is laid out away (display: contents, its rows
          placed round the capsule: nuricell.module.css), so it names its role too. */}
      <table className={styles.ingredients} role="table">
        <caption className={`${base.caption} ${styles.tableNote}`}>
          {copy(product.notes.label)}
        </caption>
        <thead className={base.visuallyHidden} role="rowgroup">
          <tr role="row">
            <th scope="col" role="columnheader">
              {copy("Per serving")}
            </th>
            <th scope="col" role="columnheader">
              {copy("Ingredient")}
            </th>
            <th scope="col" role="columnheader">
              {copy("About it")}
            </th>
          </tr>
        </thead>
        <tbody role="rowgroup">
          {product.ingredients.map((item) => (
            <tr key={item.key} role="row">
              <td className={styles.amount} role="cell">
                {item.amount.toLocaleString("en-US")}
                <span className={styles.unit}> {item.unit}</span>
              </td>
              <th scope="row" role="rowheader" className={styles.ingredient}>
                {copy(item.name)}
              </th>
              <td className={styles.about} role="cell">
                {item.role ? <span className={styles.role}>{copy(item.role)}</span> : null}
                {item.form !== item.name ? (
                  <span className={styles.form}>
                    {copy("On the label: {form}", { form: copy(item.form) })}
                  </span>
                ) : null}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      {own && product.labelCard ? (
        <div className={inside.labelCard} data-label-card="">
          <p className={inside.cardTitle}>{copy("Also on the label")}</p>
          <dl>
            {product.labelCard.map((line) => (
              <Fragment key={line.term}>
                <dt>{copy(line.term)}</dt>
                <dd>{copy(line.value)}</dd>
              </Fragment>
            ))}
          </dl>
        </div>
      ) : (
        <p className={styles.small}>{copy(product.otherIngredients)}</p>
      )}
      {own ? null : <p className={styles.small}>{copy(product.notes.science)}</p>}
      {product.synergy && own ? (
        <NuricellScenes synergy={product.synergy} names={names} motion={motion} />
      ) : product.synergy ? (
        <Synergy synergy={product.synergy} names={names} />
      ) : null}
    </InkChapter>
  );
}

function Synergy({ synergy, names }: { synergy: ProductSynergy; names: Record<string, string> }) {
  const copy = useCopy();
  return (
    <div className={styles.synergy} data-synergy="">
      <h3 className={styles.subheading}>{copy(synergy.title)}</h3>
      <ul className={styles.pairs}>
        {synergy.links.map((link) => (
          <li key={link.title}>
            <p className={styles.pairOf}>
              {copy(names[link.from] ?? link.from)} + {copy(names[link.to] ?? link.to)}
            </p>
            <h4 className={styles.pairTitle}>{copy(link.title)}</h4>
            <p className={styles.pairLine}>{copy(link.line)}</p>
            {link.evidence ? <p className={styles.small}>{copy(link.evidence)}</p> : null}
          </li>
        ))}
      </ul>
      <p className={`${base.caption} ${styles.note}`}>{copy(synergy.note)}</p>
    </div>
  );
}
