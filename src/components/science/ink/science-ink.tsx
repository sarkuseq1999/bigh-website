"use client";

import { InkPage } from "@/components/ink/ink-page";
import { OpeningWords } from "./opening";
import { Formulas, Liu } from "./people";
import styles from "./science-ink.module.css";

/** The Science page: the handscroll, Dr. Liu, the formulas, the research, health explained and
 *  Ask BiGH Science, on the kit's paper with the shared menu bar and footer. */
export function ScienceInk({ fontClass }: { fontClass: string }) {
  return (
    <InkPage current="science" className={`${fontClass} ${styles.page}`}>
      {() => (
        <>
          <section id="scientists" aria-labelledby="science-title" style={{ paddingTop: 110 }}>
            <OpeningWords />
          </section>
          <Liu />
          <Formulas />
          <section id="research" />
          <section id="health" />
          <section id="ask" />
        </>
      )}
    </InkPage>
  );
}
