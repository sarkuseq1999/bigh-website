"use client";

import { ArrowRight, ArrowUpRight } from "lucide-react";
import { useSiteDialogs } from "@/components/ink/dialogs";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { why } from "../science-content";
import styles from "./why.module.css";

/**
 * Under the zoom's last view ("Why start with the cell?", zoom.tsx, which holds the heading, its
 * lead and the cell): three numbered lines, each opening the kit's explainer sheet (the sheets
 * "Make sense of the science." opened before), and the cell count's source.
 */
export function Why() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  return (
    <section id="why-lines" className={styles.why} aria-labelledby="why-title">
      <div className={base.wrap}>
        <ol className={styles.lines} role="list">
          {why.lines.map((line, index) => (
            <li key={line.link} className={styles.item}>
              <span className={styles.number}>{index + 1}</span>
              <p className={styles.text} id={`why-line-${index}`}>
                {copy(line.text)}
              </p>
              <button
                type="button"
                className={styles.go}
                aria-describedby={`why-line-${index}`}
                onClick={() => dialogs.openArticle(index)}
              >
                {copy(line.link)} <ArrowRight size={16} aria-hidden="true" />
              </button>
            </li>
          ))}
        </ol>
        <p className={styles.source}>
          <a href={why.sourceUrl} target="_blank" rel="noreferrer">
            {/* No space before the arrow, so it stays with the last word on a phone. */}
            {copy(why.source)}
            <ArrowUpRight size={14} aria-hidden="true" className={styles.arrow} />
          </a>
        </p>
      </div>
    </section>
  );
}
