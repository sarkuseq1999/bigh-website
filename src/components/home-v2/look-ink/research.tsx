"use client";

import { ArrowUpRight, Plus } from "lucide-react";
import { type CSSProperties, useState } from "react";
import { flushSync } from "react-dom";
import { useCopy } from "@/i18n/use-copy";
import { research, researchItems, researchTypes } from "../content";
import base from "./look-ink.module.css";
import styles from "./research.module.css";

// "Curiosity, with references." The brush line becomes the index's spine: it runs down the
// middle of the sources, and every source is pinned to it by a fine leader line at the height
// of its year, like notes pinned along a scroll. The title and the words sit either side of the
// spine at the top, the filters under the words. A note is its year, then its title, then two
// quiet lines (what kind of source, and where it was published); it opens to what the source
// actually tells us and a link to it, and its leader answers in ink. Six at first, then all.
const FIRST = 6;
// Rows that arrive (another filter, "show all") settle in one after another; past this many
// the rest arrive together.
const STAGGER = 8;
// The sources' words are typed with straight apostrophes (they are the translation keys); on
// the page they are set like the rest of the page's: "Curcumin’s".
const set = (words: string) => words.replace(/([\p{L}\p{N}])'(\p{L})/gu, "$1’$2");

export function Research() {
  const copy = useCopy();
  const [filter, setFilter] = useState<string>("All");
  const [all, setAll] = useState(false);
  // The first six are simply there when the page loads; once a filter has been chosen, the
  // rows it brings settle in.
  const [chosen, setChosen] = useState(false);
  const list = researchItems.filter((item) => filter === "All" || item.type === filter);
  const shown = all ? list : list.slice(0, FIRST);

  // "Show fewer" takes away the rows above the button: keep the button where the reader's
  // pointer is (browsers that anchor the scroll have already done it; then nothing moves).
  const toggleAll = (button: HTMLButtonElement) => {
    const before = button.getBoundingClientRect().top;
    flushSync(() => setAll(!all));
    const moved = button.getBoundingClientRect().top - before;
    if (all && Math.abs(moved) > 1) window.scrollBy({ top: moved, behavior: "instant" });
  };

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
                      if (type !== filter) setChosen(true);
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
          {shown.map((item, i) => (
            <li
              key={`${filter}:${item.url}`}
              className={styles.entry}
              data-in={chosen || i >= FIRST ? "" : undefined}
              style={{ "--i": Math.min(i < FIRST ? i : i - FIRST, STAGGER) } as CSSProperties}
            >
              <details className={styles.item}>
                <summary className={styles.summary}>
                  {/* A year is a figure; a guide has a word in its place, set as a label. */}
                  <span
                    className={styles.year}
                    data-word={/^\d+$/.test(item.year) ? undefined : ""}
                  >
                    {copy(item.year)}
                  </span>
                  <span className={styles.what}>
                    <span className={styles.itemTitle}>{set(copy(item.title))}</span>
                    <span className={styles.category}>{copy(item.category)}</span>
                    <span className={styles.journal}>{item.journal}</span>
                  </span>
                  <span className={styles.toggle} aria-hidden="true">
                    <Plus size={20} />
                  </span>
                </summary>
                <div className={styles.more}>
                  <p>{set(copy(item.text))}</p>
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
              onClick={(event) => toggleAll(event.currentTarget)}
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
