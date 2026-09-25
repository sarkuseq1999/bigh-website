"use client";

import { ScienceGlass } from "./science-glass";
import type { ScienceDesignProps } from "./science-data";
import styles from "./science-section.module.css";

// "Make sense of the science." follows the customer stories, as in Mo's approved homepage plan.
// Mo chose the Glass cell look on September 24 and asked for clearer topics and topic-matched
// visuals. Earlier looks are kept in reference/science-section/ (round-1, round-2).
export function ScienceSection(props: ScienceDesignProps) {
  return (
    <section id="learn" className={styles.section} aria-labelledby="science-title">
      <ScienceGlass {...props} />
    </section>
  );
}
