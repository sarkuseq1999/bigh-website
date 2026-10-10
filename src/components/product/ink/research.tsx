"use client";

import { useId, useMemo, useState } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct } from "../product-types";
import { byYear } from "../template-chapters-kit";
import { InkChapter, InkFigure, titleId } from "./ink-chapter";
import styles from "./product-ink.module.css";

/** Studies shown before "Show all": the list stays about as tall as its painting. */
const FIRST = 5;

// Chapter 4: seven books as stepping stones (seven studies) beside the studies on hairlines, oldest
// first like the Chapters template's timeline; each opens with its round toggle to what it found
// and a link to it.
export function Research({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const [all, setAll] = useState(false);
  const listId = useId();
  const studies = useMemo(() => byYear(product.studies), [product.studies]);
  return (
    <InkChapter
      id="research"
      picture={<InkFigure art={product.ink.research} alt={product.ink.research.alt} />}
    >
      <p className={`${base.label} ${styles.label}`}>{copy("The research")}</p>
      <h2 id={titleId("research")} className={`${base.display} ${styles.heading}`}>
        {copy(product.researchTitle ?? "The research on the ingredients")}
      </h2>
      <p className={styles.small}>{copy(product.notes.research)}</p>
      <ul id={listId} className={styles.studies} data-studies="" data-all={all ? "" : undefined}>
        {studies.map((study, i) => (
          <li key={study.url} data-study="" data-extra={i >= FIRST ? "" : undefined}>
            <details>
              <summary className={styles.summary}>
                <span className={styles.year}>{study.year}</span>
                <span>
                  <span className={styles.studyTitle}>{copy(study.title)}</span>
                  <span className={styles.meta}>
                    {copy(study.kind)} · {study.journal}
                  </span>
                </span>
                <span className={styles.toggle} aria-hidden="true">
                  +
                </span>
              </summary>
              <div className={styles.open}>
                <p className={styles.small}>{copy(study.note)}</p>
                <a
                  href={study.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className={base.textLink}
                >
                  {copy("Read the study")}
                  <span className={base.visuallyHidden}> {copy("(opens in a new tab)")}</span>
                </a>
              </div>
            </details>
          </li>
        ))}
      </ul>
      {studies.length > FIRST ? (
        <button
          type="button"
          className={`${base.pill} ${base.pillGhost} ${styles.showAll}`}
          aria-expanded={all}
          aria-controls={listId}
          onClick={() => setAll((open) => !open)}
        >
          {copy(all ? "Show fewer studies" : "Show all {count} studies", { count: studies.length })}
        </button>
      ) : null}
    </InkChapter>
  );
}
