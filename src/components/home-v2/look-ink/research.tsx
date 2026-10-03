"use client";

import { ArrowUpRight, Plus } from "lucide-react";
import { useState } from "react";
import { useCopy } from "@/i18n/use-copy";
import { research, researchItems, researchTypes } from "../content";
import base from "./look-ink.module.css";
import styles from "./research.module.css";

// "Curiosity, with references." The brush line becomes the index's spine: it runs down the
// middle of the sources, and every source is pinned to it by a fine leader line from its year,
// like notes pinned along a scroll. The title and the words sit either side of the spine at the
// top, the filters under the words. A source opens to what it actually tells us and a link to
// it. Six at first, then all.
const FIRST = 6;

export function Research() {
  const copy = useCopy();
  const [filter, setFilter] = useState<string>("All");
  const [all, setAll] = useState(false);
  const list = researchItems.filter((item) => filter === "All" || item.type === filter);
  const shown = all ? list : list.slice(0, FIRST);

  return (
    <section
      id="research"
      className={styles.research}
      aria-labelledby="research-title"
      data-brush="research"
    >
      <div className={base.wrap}>
        <div className={styles.top}>
          <div className={styles.titleRow}>
            <h2 id="research-title" className={`${base.display} ${styles.title}`}>
              {research.title.map((line) => (
                <span key={line}>{copy(line)}</span>
              ))}
            </h2>
            <p
              className={`${base.station} ${styles.station}`}
              data-station=""
              data-side="left"
              data-brush="st-research"
            >
              {copy(research.eyebrow)}
            </p>
          </div>
          <div className={styles.side}>
            <p className={`${base.body} ${styles.intro}`}>{copy(research.text)}</p>
            <div className={styles.filters} role="group" aria-label={copy("Filter research")}>
              {["All", ...researchTypes].map((type) => {
                const count = researchItems.filter(
                  (item) => type === "All" || item.type === type,
                ).length;
                return (
                  <button
                    key={type}
                    type="button"
                    className={styles.filter}
                    aria-pressed={filter === type}
                    onClick={() => {
                      setFilter(type);
                      setAll(false);
                    }}
                  >
                    <span>{copy(type)}</span>
                    <span className={styles.count}>{count}</span>
                  </button>
                );
              })}
            </div>
          </div>
        </div>

        <ul className={styles.list} data-brush="research-list">
          {shown.map((item) => (
            <li key={item.url} className={styles.entry}>
              <details className={styles.item}>
                <summary className={styles.summary}>
                  <span className={styles.year}>{copy(item.year)}</span>
                  <span className={styles.what}>
                    <span className={styles.category}>{copy(item.category)}</span>
                    <span className={styles.itemTitle}>{copy(item.title)}</span>
                    <span className={styles.journal}>{item.journal}</span>
                  </span>
                  <span className={styles.toggle} aria-hidden="true">
                    <Plus size={20} />
                  </span>
                </summary>
                <div className={styles.more}>
                  <p>{copy(item.text)}</p>
                  <a href={item.url} target="_blank" rel="noreferrer" className={base.textLink}>
                    {copy(research.readSource)} <ArrowUpRight size={18} aria-hidden="true" />
                  </a>
                </div>
              </details>
            </li>
          ))}
        </ul>

        <div className={styles.foot}>
          {list.length > FIRST && (
            <button
              type="button"
              className={`${base.pill} ${base.pillGhost} ${styles.showAll}`}
              aria-expanded={all}
              onClick={() => setAll(!all)}
            >
              {copy(all ? research.showFewer : research.showAll)}
              {!all && <span className={styles.showCount}>{list.length}</span>}
            </button>
          )}
          <p className={styles.note}>{copy(research.note)}</p>
        </div>
      </div>
    </section>
  );
}
