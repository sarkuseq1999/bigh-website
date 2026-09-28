"use client";

import { useEffect, useRef } from "react";
import { useCopy } from "@/i18n/use-copy";
import { about } from "./about-content";
import styles from "./acronym.module.css";

// The About page's signature moment, shared by every round-2 look: the name "BiGH" unfolds into
// what it stands for, "Be in Good Health." The four initials stay put (in the look's accent
// color) while the rest of each word opens out of them. It plays once on load; with reduced
// motion it shows open. The heading's text is the full sentence, so screen readers and search
// read "Be in Good Health." Where a translation isn't the English sentence, the translated title
// shows as it is (the acronym only works in English).
//
// Style it from the look with className (font, size, color) and --acronym-accent (the initials).

const PARTS = [
  ["B", "e"],
  ["i", "n"],
  ["G", "ood"],
  ["H", "ealth."],
] as const;

export function Acronym({
  className = "",
  id = "about-title",
  delay = 650,
}: {
  className?: string;
  id?: string;
  /** Milliseconds "BiGH" holds before it unfolds. */
  delay?: number;
}) {
  const copy = useCopy();
  const title = copy(about.hero.title);
  const heading = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    const element = heading.current;
    if (!element) return;
    const reduced = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    const timer = window.setTimeout(() => (element.dataset.open = "true"), reduced ? 0 : delay);
    return () => window.clearTimeout(timer);
  }, [delay]);

  if (title !== about.hero.title) {
    return (
      <h1 id={id} className={className}>
        {title}
      </h1>
    );
  }

  // The visible letters are split into pieces, so the heading carries the sentence as its label.
  return (
    <h1 ref={heading} id={id} className={`${styles.acronym} ${className}`} aria-label={title}>
      <span aria-hidden="true">
        {PARTS.map(([initial, rest], index) => (
          <span
            key={initial}
            className={styles.word}
            style={{ "--i": index } as React.CSSProperties}
          >
            <span className={styles.initial}>{initial}</span>
            <span className={styles.rest}>
              <span>{rest}</span>
            </span>
            {index < PARTS.length - 1 ? " " : null}
          </span>
        ))}
      </span>
    </h1>
  );
}
