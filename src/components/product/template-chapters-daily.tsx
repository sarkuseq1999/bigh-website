"use client";

import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";
import { useEffect, useId, useRef, useState, type CSSProperties } from "react";
import { useCopy } from "@/i18n/use-copy";
import type { ProductPage } from "./product-types";
import { anchorId, useArrivals, type Chapter } from "./template-chapters-kit";
import { monthPlan, titleFor } from "./template-chapters-model";
import shared from "./template-chapters.module.css";
import styles from "./template-chapters-daily.module.css";

/** Tall enough to pin the month while it fills: the same test as the CSS. */
const PINNED = "(min-height: 600px)";
/** Capsules drawn in a day, one each; more than this show as one capsule with a count. */
const MAX_GLYPHS = 6;
/** The share of the pinned scroll the month takes to fill; the rest is the full month, resting. */
const FILL = 0.84;

// Chapter 6, how to take it: one bottle drawn as a month you can read at a glance (Timeline's
// "familiar comparison", made tangible). A day for every day the bottle lasts, each with that
// day's capsules. As you scroll, the days fill one after another and the count climbs to the
// bottle's capsules and days; on the last day, a quiet line. Reduced motion, and windows too short
// to pin it, show the whole month filled.
export function DailyChapter({
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
  const plan = monthPlan(product.serving);
  const { perDay, days, total, drawn } = plan;
  // Days filled so far while scrolling. null: the whole month (the still layouts).
  const [filled, setFilled] = useState<number | null>(null);
  useArrivals(root, reduced);

  // Pinned: the stage sticks for a tall section, and the scroll position alone says how many days
  // are filled, so fast scrolling either way always lands on the right day.
  useEffect(() => {
    const section = root.current;
    if (reduced || !section || days === 0) return;
    gsap.registerPlugin(ScrollTrigger);
    const mm = gsap.matchMedia(section);
    mm.add(PINNED, () => {
      const show = (progress: number) =>
        setFilled(Math.min(days, Math.floor((progress / FILL) * days + 0.0001)));
      const trigger = ScrollTrigger.create({
        trigger: section,
        start: "top 30%",
        end: "bottom bottom",
        onUpdate: (self) => show(self.progress),
        onRefresh: (self) => show(self.progress),
      });
      show(trigger.progress);
      return () => setFilled(null);
    });
    return () => mm.revert();
  }, [reduced, days]);

  const shown = filled === null ? days : filled;
  const cells = drawn === days ? shown : Math.round((shown / Math.max(days, 1)) * drawn);
  const done = shown >= days;
  const capsulesSoFar = done ? total : Math.round((total * shown) / Math.max(days, 1));
  const glyphs = perDay > MAX_GLYPHS ? 1 : perDay;

  const count = (daysSoFar: number, capsules: number) => {
    const dayText = daysSoFar === 1 ? copy("1 day") : copy("{count} days", { count: daysSoFar });
    if (!total) return dayText;
    const capsuleText =
      capsules === 1 ? copy("1 capsule") : copy("{count} capsules", { count: capsules });
    return `${capsuleText} · ${dayText}`;
  };

  return (
    <section
      ref={root}
      id={anchorId(chapter.id)}
      data-chapter={chapter.id}
      data-tone={chapter.tone}
      tabIndex={-1}
      aria-labelledby={titleId}
      className={`${shared.chapter} ${styles.daily}`}
      data-motion={reduced ? "off" : "on"}
      style={
        {
          "--cols-wide": plan.wide,
          "--rows-wide": plan.wideRows,
          "--cols-narrow": plan.narrow,
          "--rows-narrow": plan.narrowRows,
          "--extra": `${40 + Math.min(150, Math.max(90, drawn * 3))}svh`,
        } as CSSProperties
      }
    >
      <div className={styles.stage}>
        <p className={styles.eyebrow}>{copy(chapter.name)}</p>
        <h2 id={titleId} className={styles.title} data-heading>
          {days > 0 ? copy(titleFor(days), { days }) : copy(chapter.name)}
        </h2>
        {product.serving?.use && (
          <p className={styles.use} data-reveal>
            {copy(product.serving.use)}
          </p>
        )}

        {days > 0 && (
          <>
            {/* The month is a picture of the count below, which says it in words. */}
            <div className={styles.calendar} aria-hidden="true">
              <ol className={styles.grid}>
                {Array.from({ length: drawn }, (_, index) => (
                  <li
                    key={index}
                    className={styles.day}
                    data-filled={index < cells}
                    data-today={index === cells - 1}
                  >
                    <span className={styles.number}>{index + 1}</span>
                    {glyphs > 0 && (
                      <span className={styles.pills} style={{ "--n": glyphs } as CSSProperties}>
                        {Array.from({ length: glyphs }, (_, capsule) => (
                          <span
                            key={capsule}
                            className={styles.pill}
                            style={{ "--i": capsule } as CSSProperties}
                          />
                        ))}
                        {perDay > MAX_GLYPHS && <span className={styles.times}>×{perDay}</span>}
                      </span>
                    )}
                  </li>
                ))}
              </ol>
            </div>
            <p className={styles.count}>
              <span aria-hidden="true">{count(shown, capsulesSoFar)}</span>
              <span className={shared.srOnly}>{count(days, total)}</span>
            </p>
            <p className={styles.then} data-shown={done}>
              {copy("Then a new bottle.")}
            </p>
          </>
        )}
      </div>
    </section>
  );
}
