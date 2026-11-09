"use client";

import { InkPage } from "@/components/ink/ink-page";
import { Ask, Research } from "./explore";
import { Opening } from "./opening";
import { Path } from "./path";
import { Formulas, Liu } from "./people";
import { Why } from "./why";
import styles from "./science-ink.module.css";

/** The Science page, round 3 (Mo, November 4, 2026: start broader, with what science BiGH focuses
 *  on and why; spec docs/superpowers/specs/2026-11-04-science-california-design.md): what we study
 *  (the opening), why the cell (the town whose lamps light up), the scientist and his path, the
 *  formulas that came of it, the research, and Ask BiGH Science, on the kit's paper with the shared
 *  menu bar and footer. */
export function ScienceInk({ fontClass }: { fontClass: string }) {
  return (
    <InkPage current="science" className={`${fontClass} ${styles.page}`}>
      {(motion) => (
        <>
          <Opening />
          <Why motion={motion} />
          <section id="scientists" className={styles.scientists} aria-labelledby="liu-name">
            <Liu />
            <Path />
          </section>
          <Formulas />
          <Research />
          <Ask />
        </>
      )}
    </InkPage>
  );
}
