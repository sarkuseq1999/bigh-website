"use client";

import Image from "next/image";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { about, drafts } from "./about-content";
import page from "./about-page.module.css";
import { madeArt as art } from "./made-art";
import styles from "./made.module.css";

// Our home, "Proudly made in California." (Mo picked F, the valley at dawn, November 9, 2026, of
// five ideas without the bottles; mockups reference/ink-pages/mockups/about-made/). One painting
// across the chapter: California's Central Valley in the first light from a golden foothill, some
// of its fields laid in gold leaf, the snowy Sierra behind (a Codex painting,
// reference/ink-pages/about-made/). The heading stands in its empty sky; GMP in plain words and
// its three rules in a row under it. Under 960px the words stand over the painting and its empty
// sky is cut away.

export function MadeInCalifornia() {
  const copy = useCopy();
  return (
    <section
      id="home"
      className={`${page.part} ${styles.part}`}
      data-part="home"
      aria-labelledby="home-title"
    >
      <div className={base.wrap}>
        <figure className={styles.valley} data-picture="">
          <span className={styles.body}>
            <Image
              className={base.ink}
              src={art.valley.src}
              alt={copy(about.home.alt)}
              width={art.valley.width}
              height={art.valley.height}
              sizes="(max-width: 1440px) 92vw, 1300px"
              data-bloom="waiting"
            />
            <span className={styles.sky}>
              <p className={`${base.label} ${page.label}`} data-label="">
                {copy(about.home.label)}
              </p>
              <h2 id="home-title" className={`${base.display} ${page.heading}`}>
                {copy(about.home.title)}
              </h2>
              <p className={`${page.body} ${styles.lead}`}>{copy(about.home.text)}</p>
            </span>
          </span>
          <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
        </figure>
        <div className={styles.row}>
          <p className={styles.gmp}>{copy(about.home.gmp)}</p>
          <ul>
            {about.home.rules.map((rule) => (
              <li key={rule}>{copy(rule)}</li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
