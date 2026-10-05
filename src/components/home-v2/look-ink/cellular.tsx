"use client";

import Image from "next/image";
import { ArrowRight } from "lucide-react";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { cellular } from "../content";
import { gold, mito } from "./assets";
import base from "./look-ink.module.css";
import styles from "./cellular.module.css";

// "Tiny power plants." The opening dives from the landscape into the cell: the words at the left
// with the three numbered lines on hairlines, the ink mitochondrion (its two gold-leaf folds where
// energy is made) at the right, the page's biggest painting after the opening, running off the
// edge of the window; the brush line passes between them.
export function Cellular() {
  const copy = useCopy();
  const lines = [cellular.opening, cellular.explanation, cellular.closing];

  return (
    <section
      id="cellular"
      className={styles.cellular}
      aria-labelledby="cellular-title"
      data-brush="cellular"
    >
      <div className={`${base.wrap} ${styles.grid}`}>
        <div className={styles.words} data-brush="cellular-words">
          <p
            className={`${base.station} ${styles.station}`}
            data-station=""
            data-side="right"
            data-brush="st-cellular"
          >
            {copy(cellular.eyebrow)}
          </p>
          <h2 id="cellular-title" className={`${base.display} ${styles.title}`}>
            {cellular.title.map((line) => (
              <span key={line}>{copy(line)}</span>
            ))}
          </h2>
          <ol className={styles.lines}>
            {lines.map((line, i) => (
              <li key={line}>
                <span className={styles.number}>0{i + 1}</span>
                <span className={styles.text}>{copy(line)}</span>
              </li>
            ))}
          </ol>
          <Link href="/science#health" className={`${base.textLink} ${styles.link}`}>
            {copy(cellular.link)} <ArrowRight size={18} aria-hidden="true" />
          </Link>
        </div>

        <figure className={styles.figure} data-brush="cellular-mito">
          <span className={styles.body}>
            <Image
              className={`${base.ink} ${styles.mito}`}
              src={mito.glow.src}
              alt={copy(
                "A mitochondrion, painted in ink, with two gold folds where energy is made",
              )}
              width={mito.glow.width}
              height={mito.glow.height}
              sizes="(max-width: 899px) 124vw, min(72vw, 1280px)"
              data-bloom=""
            />
            <span className={base.gold} style={{ ["--gold" as string]: `url(${gold.mito})` }} />
          </span>
          <figcaption className={base.caption}>{copy(cellular.caption)}</figcaption>
        </figure>
      </div>
    </section>
  );
}
