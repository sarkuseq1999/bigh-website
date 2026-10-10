"use client";

import Image from "next/image";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct } from "../product-types";
import { monthPlan, titleFor } from "../template-chapters-daily";
import { InkChapter, InkFigure, titleId } from "./ink-chapter";
import styles from "./product-ink.module.css";

const LABELS = ["capsules a day", "days", "capsules in each bottle"] as const;

// Chapter 6: when (a light breakfast, three capsules beside it, the yolk the only gold) and how
// much (the serving as one painted sum, a caption under each number). The painted sum is shown
// only when its numbers are the serving's; otherwise the sum is set in type, so a changed label
// can never show a wrong painting.
export function Daily({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const plan = monthPlan(product.serving);
  const { picture, sum } = product.ink.daily;
  const numbers = [plan.perDay, plan.days, plan.total];
  const painted = sum.numbers.length === 3 && sum.numbers.every((n, i) => n === numbers[i]);
  const centres = painted ? sum.centres : [1 / 6, 1 / 2, 5 / 6];
  return (
    <InkChapter id="daily" picture={<InkFigure art={picture} alt={picture.alt} />}>
      <p className={`${base.label} ${styles.label}`}>{copy("How to take it")}</p>
      <h2 id={titleId("daily")} className={`${base.display} ${styles.heading}`}>
        {copy(titleFor(plan.days), { days: plan.days })}
      </h2>
      <figure className={styles.sum} data-sum="" data-centres={JSON.stringify(centres)}>
        {painted ? (
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
        ) : (
          <p className={styles.sumType} aria-hidden="true">
            {plan.perDay} × {plan.days} = {plan.total}
          </p>
        )}
        <figcaption>
          <span className={base.visuallyHidden} data-sum-text="">
            {copy("{perDay} capsules a day for {days} days: {total} capsules in each bottle.", {
              perDay: plan.perDay,
              days: plan.days,
              total: plan.total,
            })}
          </span>
          {LABELS.map((label, i) => (
            <span
              key={label}
              className={styles.sumLabel}
              data-sum-label=""
              aria-hidden="true"
              style={{
                left: `${(centres[i] * 100).toFixed(2)}%`,
                maxWidth: `${(Math.min(0.34, 2 * Math.min(centres[i], 1 - centres[i])) * 100).toFixed(2)}%`,
              }}
            >
              {copy(label)}
            </span>
          ))}
        </figcaption>
      </figure>
      <p className={styles.text}>{copy(product.serving.use)}</p>
    </InkChapter>
  );
}
