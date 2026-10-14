"use client";

import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { ink, opening } from "../science-content";
import styles from "./science-ink.module.css";

/** The page's title block: "Science", the one h1, the film's two lines as its lead. */
export function OpeningWords() {
  const copy = useCopy();
  return (
    <header className={`${base.wrap} ${styles.opening}`}>
      <p className={base.caption}>{copy(opening.eyebrow)}</p>
      <h1 id="science-title">{copy(opening.title)}</h1>
      <p className={base.body}>{ink.lead.map((line) => copy(line)).join(" ")}</p>
    </header>
  );
}
