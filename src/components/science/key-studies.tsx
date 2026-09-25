"use client";

import { ArrowUpRight, Minus, Plus } from "lucide-react";
import { useState } from "react";
import { researchItems } from "@/components/home/research-data";
import { useCopy } from "@/i18n/use-copy";
import { ResearchGroups } from "./research-library";
import { research } from "./science-content";
import styles from "./key-studies.module.css";

// Round 2's research section. Mo found 36 rows too many (September 25), so three key studies lead
// as cards and the full list opens only on request. Colors come from the look's tokens.
export function KeyStudies() {
  const copy = useCopy();
  const [all, setAll] = useState(false);
  const key = research.key
    .map((url) => researchItems.find((item) => item.url === url))
    .filter((item) => item !== undefined);

  return (
    <section id="research" className={styles.studies} data-tone="light">
      <div className={styles.head}>
        <p className={styles.eyebrow}>{copy(research.eyebrow)}</p>
        <h2 className={styles.title}>{copy(research.title)}</h2>
        <p className={styles.text}>{copy(research.text)}</p>
      </div>

      <div className={styles.cards}>
        {key.map((item) => (
          <a
            key={item.url}
            href={item.url}
            target="_blank"
            rel="noreferrer"
            className={styles.card}
          >
            <span className={styles.year}>{copy(item.year)}</span>
            <span className={styles.meta}>
              {copy(item.category)}
              {research.byLiu.includes(item.url) && (
                <span className={styles.tag}>{copy(research.tag)}</span>
              )}
            </span>
            <span className={styles.cardTitle}>{copy(item.title)}</span>
            <span className={styles.cardText}>{copy(item.text)}</span>
            <span className={styles.foot}>
              <span className={styles.journal}>{item.journal}</span>
              <ArrowUpRight size={22} aria-hidden="true" />
            </span>
          </a>
        ))}
      </div>

      <div className={styles.more}>
        <button type="button" aria-expanded={all} onClick={() => setAll(!all)}>
          {/* A string without a catalog key comes back as written, so fill {count} here too. */}
          {all
            ? copy(research.hideAll)
            : copy(research.seeAll, { count: researchItems.length }).replace(
                "{count}",
                String(researchItems.length),
              )}
          {all ? <Minus size={18} /> : <Plus size={18} />}
        </button>
      </div>

      {all && (
        <div className={styles.all}>
          <ResearchGroups everything />
        </div>
      )}

      <p className={styles.note}>{copy(research.note)}</p>
    </section>
  );
}
