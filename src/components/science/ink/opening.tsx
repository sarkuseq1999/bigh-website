"use client";

import { getImageProps } from "next/image";
import type { CSSProperties } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { ink, opening } from "../science-content";
import { scienceArt } from "./science-art";
import styles from "./opening.module.css";

const SIZES = "(max-width: 959px) 100vw, 58vw";

/**
 * The page's first screen (round 3, Mo, November 4, 2026: start with what science BiGH focuses on):
 * the one h1 and its two questions, which name the scientist who has spent his career on them, beside
 * a scientist's desk at an open window over golden California hills. From 960px the words stand at
 * the left under the logo's edge and the painting runs out to the window's right edge; on a phone
 * the painting comes first, then the words. The painting blooms in as the page opens (marked
 * "waiting" by the server).
 */
export function Opening() {
  const copy = useCopy();
  const art = scienceArt.desk;
  // The first screen's picture: fetched at once and first (two pictures, one per layout, so no
  // head preload; next/image's docs warn against preloading art-directed images).
  const common = {
    alt: copy(opening.alt),
    sizes: SIZES,
    loading: "eager" as const,
    fetchPriority: "high" as const,
  };
  const wide = getImageProps({ ...common, src: art.src, width: art.width, height: art.height });
  const narrow = getImageProps({
    ...common,
    src: art.phone.src,
    width: art.phone.width,
    height: art.phone.height,
  });
  const ratios = {
    "--ar-wide": `${art.width} / ${art.height}`,
    "--ar-narrow": `${art.phone.width} / ${art.phone.height}`,
  } as CSSProperties;
  return (
    <header className={styles.opening}>
      <div className={styles.words}>
        <h1 id="science-title" className={styles.title}>
          {copy(opening.title)}
        </h1>
        <p className={styles.lead}>{copy(opening.lead)}</p>
      </div>
      <figure className={styles.figure} style={ratios}>
        <picture>
          <source media="(max-width: 959px)" srcSet={narrow.props.srcSet} sizes={SIZES} />
          {/* A plain img inside a picture: art direction through getImageProps (the phone cut). */}
          <img
            {...wide.props}
            alt={common.alt}
            className={`${base.ink} ${styles.art}`}
            data-bloom="waiting"
          />
        </picture>
        <figcaption className={`${base.caption} ${styles.caption}`}>
          {copy(ink.illustration)}
        </figcaption>
      </figure>
    </header>
  );
}
