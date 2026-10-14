"use client";

import { InkPage } from "@/components/ink/ink-page";
import { Ask, Health, Research } from "./explore";
import { Journey } from "./journey";
import { Formulas, Liu } from "./people";
import styles from "./science-ink.module.css";

/** The Science page: the handscroll, Dr. Liu, the formulas, the research, health explained and
 *  Ask BiGH Science, on the kit's paper with the shared menu bar and footer. */
export function ScienceInk({ fontClass }: { fontClass: string }) {
  return (
    <InkPage current="science" className={`${fontClass} ${styles.page}`}>
      {(motion) => (
        <>
          <Journey motion={motion} />
          <Liu />
          <Formulas />
          <Research />
          <Health />
          <Ask />
        </>
      )}
    </InkPage>
  );
}
