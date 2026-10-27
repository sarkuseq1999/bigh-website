"use client";

import { InkPage } from "@/components/ink/ink-page";
import { Ask, Health, Research } from "./explore";
import { OpeningWords } from "./opening";
import { Path } from "./path";
import { Formulas, Liu } from "./people";
import styles from "./science-ink.module.css";

/** The Science page (Mo's pick B, October 26, 2026): the title and Dr. Liu, his path one place per
 *  screen going down, then the research, health explained, the formulas and Ask BiGH Science, on
 *  the kit's paper with the shared menu bar and footer. */
export function ScienceInk({ fontClass }: { fontClass: string }) {
  return (
    <InkPage current="science" className={`${fontClass} ${styles.page}`}>
      {() => (
        <>
          <section id="scientists" className={styles.scientists} aria-labelledby="science-title">
            <OpeningWords />
            <Liu />
            <Path />
          </section>
          <Research />
          <Health />
          <Formulas />
          <Ask />
        </>
      )}
    </InkPage>
  );
}
