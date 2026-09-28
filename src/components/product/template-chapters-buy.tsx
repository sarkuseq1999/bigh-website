"use client";

import Image from "next/image";
import { Plus } from "lucide-react";
import { useId, useRef, useState, type CSSProperties, type KeyboardEvent } from "react";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { AddToCart } from "./add-to-cart";
import { getSummary } from "./catalog";
import { BottleStage } from "./signature/bottle-stage";
import type { ProductPage, ProductSummary } from "./product-types";
import { anchorId, useArrivals, type Chapter } from "./template-chapters-kit";
import styles from "./template-chapters.module.css";

// Chapter 7, buy (Design Vault #019: one object, one line, calm). The 3D bottle on the product's
// tint, turning a little toward the pointer (its photo for products without a 3D bottle yet), beside its name, how to take it, the supply, Add to cart and the credit; then the questions, and
// the rest of the range.
export function BuyChapter({
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
  useArrivals(root, reduced);
  const related = product.related
    .map((slug) => getSummary(slug))
    .filter((summary): summary is ProductSummary => Boolean(summary));

  return (
    <section
      ref={root}
      id={anchorId(chapter.id)}
      data-chapter={chapter.id}
      data-tone={chapter.tone}
      tabIndex={-1}
      aria-labelledby={titleId}
      className={styles.chapter}
    >
      <div className={styles.buyStage}>
        <figure className={styles.buyFigure} data-reveal>
          <span className={styles.buyStage3d}>
            <BottleStage product={product} reduced={reduced} />
          </span>
        </figure>
        <div className={styles.buyText}>
          <p className={styles.buyEyebrow} data-reveal>
            {copy(product.eyebrow)}
          </p>
          <h2 id={titleId} className={styles.buyName} data-reveal>
            {product.name}
          </h2>
          <p className={styles.buyFocus} data-reveal>
            {copy(product.focus)}
          </p>
          <dl className={styles.buyFacts} data-reveal>
            <div>
              <dt>{copy("How to take it")}</dt>
              <dd>{copy(product.serving.use)}</dd>
            </div>
            <div>
              <dt>{copy("In each bottle")}</dt>
              <dd>{copy(product.serving.supply)}</dd>
            </div>
          </dl>
          <div className={styles.buyCart} data-reveal>
            <AddToCart wide />
            {product.credit && <p className={styles.credit}>{copy(product.credit)}</p>}
          </div>
        </div>
      </div>

      {product.faq.length > 0 && <Questions faq={product.faq} />}

      {related.length > 0 && (
        <div className={styles.more} data-tone="paper">
          <h2 className={styles.blockTitle} data-heading>
            {copy("More from BiGH")}
          </h2>
          <ul className={styles.cards}>
            {related.map((summary) => (
              <li key={summary.slug} data-reveal>
                <Link
                  href="/#products"
                  className={styles.card}
                  style={
                    { "--card-tint": summary.tint, "--card-ink": summary.ink } as CSSProperties
                  }
                >
                  <span className={styles.cardPlate}>
                    <Image
                      src={summary.bottle.src}
                      width={summary.bottle.width}
                      height={summary.bottle.height}
                      alt=""
                      sizes="(max-width: 700px) 112px, 200px"
                    />
                  </span>
                  <span className={styles.cardName}>{summary.name}</span>
                  <span className={styles.cardFocus}>{copy(summary.focus)}</span>
                </Link>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}

// An accordion: each question is a button that opens its answer (aria-expanded, aria-controls).
// Up and Down move between questions; Home and End go to the first and last.
function Questions({ faq }: { faq: ProductPage["faq"] }) {
  const copy = useCopy();
  const baseId = useId();
  const titleId = `${baseId}title`;
  const [open, setOpen] = useState<Set<number>>(() => new Set());
  const buttons = useRef<(HTMLButtonElement | null)[]>([]);

  function toggle(index: number) {
    setOpen((current) => {
      const next = new Set(current);
      if (next.has(index)) next.delete(index);
      else next.add(index);
      return next;
    });
  }

  function move(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    const last = faq.length - 1;
    const target =
      event.key === "ArrowDown"
        ? index === last
          ? 0
          : index + 1
        : event.key === "ArrowUp"
          ? index === 0
            ? last
            : index - 1
          : event.key === "Home"
            ? 0
            : event.key === "End"
              ? last
              : null;
    if (target === null) return;
    event.preventDefault();
    buttons.current[target]?.focus();
  }

  return (
    <div className={styles.questions} data-tone="paper">
      <h2 id={titleId} className={styles.blockTitle} data-heading>
        {copy("Questions")}
      </h2>
      <ul className={styles.faq} aria-labelledby={titleId}>
        {faq.map((item, index) => {
          const questionId = `${baseId}q${index}`;
          const answerId = `${baseId}a${index}`;
          const expanded = open.has(index);
          return (
            <li key={index} className={styles.faqItem}>
              <h3>
                <button
                  ref={(node) => {
                    buttons.current[index] = node;
                  }}
                  id={questionId}
                  type="button"
                  className={styles.faqButton}
                  aria-expanded={expanded}
                  aria-controls={answerId}
                  onClick={() => toggle(index)}
                  onKeyDown={(event) => move(event, index)}
                >
                  <span>{copy(item.question)}</span>
                  <span className={styles.faqIcon} aria-hidden="true">
                    <Plus size={20} strokeWidth={2} />
                  </span>
                </button>
              </h3>
              <div
                id={answerId}
                role="region"
                aria-labelledby={questionId}
                className={`${styles.faqAnswer} ${styles.panel}`}
                hidden={!expanded}
              >
                <p>{copy(item.answer)}</p>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
