"use client";

import Image from "next/image";
import { Fragment, useSyncExternalStore } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct } from "../product-types";
import { monthPlan, titleFor } from "../template-chapters-model";
import { InkChapter, InkFigure, keepTogether, titleId } from "./ink-chapter";
import styles from "./product-ink.module.css";

const LABELS = ["capsules a day", "days", "capsules in each bottle"] as const;

// Development only: ?ink-sum=type shows the sum set in type (what a label that no longer matches
// the painting gets); ?ink-sum=odd does too, for a bottle whose capsules are not a day's times its
// days (91 for 3 x 30), which drops the operators. Production builds always show the product as
// given. (The same way as the other template's ?chapters-fixture=.)
const noSubscription = () => () => {};
function useSumFixture() {
  return useSyncExternalStore(
    noSubscription,
    () =>
      process.env.NODE_ENV === "production"
        ? null
        : new URLSearchParams(window.location.search).get("ink-sum"),
    () => null,
  );
}

// Chapter 6: when (a light breakfast, three capsules beside it, the yolk the only gold) and how
// much (the serving as one painted sum, a caption under each number). A product without a sum
// (Green Bee Propolis: one a day, so "1 × 60 = 60" would say nothing new) shows none. The painted
// sum is shown only when its numbers are the serving's (and it has a centre for each); otherwise
// the sum is set in type, three cells each with its numeral and its caption under it, so a changed
// label can never show a wrong painting, nor a caption under the wrong number. The "x" and "=" are
// shown only when the numbers really make that sum. A product with a `story` (NuriCell) says that
// instead: its heading, a lead in ink and a note on its painting, no label and no sum.
export function Daily({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const fixture = useSumFixture();
  const serving =
    fixture === "odd"
      ? { ...product.serving, perBottle: product.serving.perBottle + 1 }
      : product.serving;
  const plan = monthPlan(serving);
  const { picture, sum, story } = product.ink.daily;
  // NuriCell's (October 27, 2026): what has stayed the same, beside the redwood round.
  if (story) {
    return (
      <InkChapter id="daily" picture={<InkFigure art={picture} alt={picture.alt} />}>
        <h2 id={titleId("daily")} className={`${base.display} ${styles.heading}`}>
          {copy(story.title)}
        </h2>
        <p className={styles.chapterLead}>{copy(story.lead)}</p>
        <p className={styles.text}>{keepTogether(copy(story.note))}</p>
      </InkChapter>
    );
  }
  const numbers = [plan.perDay, plan.days, plan.total];
  const painted =
    !!sum &&
    fixture !== "type" &&
    fixture !== "odd" &&
    sum.numbers.length === 3 &&
    sum.centres.length === 3 &&
    sum.numbers.every((n, i) => n === numbers[i]);
  const operators = plan.perDay * plan.days === plan.total;
  return (
    <InkChapter id="daily" picture={<InkFigure art={picture} alt={picture.alt} />}>
      <p className={`${base.label} ${styles.label}`}>{copy("How to take it")}</p>
      <h2 id={titleId("daily")} className={`${base.display} ${styles.heading}`}>
        {copy(titleFor(plan.days), { days: plan.days })}
      </h2>
      {sum ? (
        <figure
          className={styles.sum}
          data-sum=""
          data-sum-kind={painted ? "painted" : "type"}
          data-centres={painted ? JSON.stringify(sum.centres) : undefined}
        >
          <span className={base.visuallyHidden} data-sum-text="">
            {copy("{perDay} capsules a day for {days} days: {total} capsules in each bottle.", {
              perDay: plan.perDay,
              days: plan.days,
              total: plan.total,
            })}
          </span>
          {painted ? (
            <>
              <Image
                className={`${base.ink} ${styles.sumArt}`}
                src={sum.src}
                alt=""
                width={sum.width}
                height={sum.height}
                sizes="(max-width: 959px) 88vw, 560px"
                data-bloom="waiting"
                aria-hidden="true"
              />
              <figcaption>
                {LABELS.map((label, i) => (
                  <span
                    key={label}
                    className={styles.sumLabel}
                    data-sum-label=""
                    aria-hidden="true"
                    style={{
                      left: `${(sum.centres[i] * 100).toFixed(2)}%`,
                      maxWidth: `${(Math.min(0.34, 2 * Math.min(sum.centres[i], 1 - sum.centres[i])) * 100).toFixed(2)}%`,
                    }}
                  >
                    {copy(label)}
                  </span>
                ))}
              </figcaption>
            </>
          ) : (
            <div className={styles.sumType} data-sum-type="" aria-hidden="true">
              {numbers.map((number, i) => (
                <Fragment key={LABELS[i]}>
                  {operators && i > 0 ? (
                    <span className={styles.sumOperator}>{i === 1 ? "×" : "="}</span>
                  ) : null}
                  <span className={styles.sumCell}>
                    <span className={styles.sumNumeral} data-sum-numeral="">
                      {number}
                    </span>
                    <span className={styles.sumCaption} data-sum-label="">
                      {copy(LABELS[i])}
                    </span>
                  </span>
                </Fragment>
              ))}
            </div>
          )}
        </figure>
      ) : null}
      <p className={styles.text}>{copy(product.serving.use)}</p>
    </InkChapter>
  );
}
