"use client";

import { getImageProps } from "next/image";
import { ArrowUpRight } from "lucide-react";
import type { CSSProperties } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { ink, places } from "../science-content";
import { scienceArt } from "./science-art";
import styles from "./path.module.css";

// From 960px the paintings take turns: Okayama left, Berkeley right, Salzburg left, Today wide.
const SIDE = ["left", "right", "left", "wide"] as const;
const SIZES = {
  left: "(max-width: 959px) 100vw, 60vw",
  right: "(max-width: 959px) 100vw, 60vw",
  wide: "(max-width: 959px) 100vw, min(1120px, 86vw)",
};

/**
 * Dr. Liu's path (Mo's pick B, October 26, 2026): one place per screen, going down the page, each
 * painting (cut from the old handscroll's band, science-art.ts places) beside its words. Phones get
 * a tighter cut of each place, one column, the painting over its words. Each painting blooms in as
 * it arrives, like the strips' (the server marks it "waiting"; path.module.css shows it whole where
 * no bloom will come).
 */
export function Path() {
  const copy = useCopy();
  return (
    <ol className={styles.places} role="list">
      {places.map((place, i) => {
        const art = scienceArt.places[place.key];
        const side = SIDE[i];
        const common = { alt: copy(place.alt), sizes: SIZES[side] };
        const wide = getImageProps({
          ...common,
          src: art.src,
          width: art.width,
          height: art.height,
        });
        const narrow = getImageProps({
          ...common,
          src: art.phone.src,
          width: art.phone.width,
          height: art.phone.height,
        });
        // The painting's box comes from the stylesheet (path.module.css, .art), whichever picture
        // loads, so nothing below moves when the phone cut (another ratio) arrives.
        const ratios = {
          "--ar-wide": `${art.width} / ${art.height}`,
          "--ar-narrow": `${art.phone.width} / ${art.phone.height}`,
        } as CSSProperties;
        return (
          <li key={place.key} className={styles.place} data-side={side} data-place={place.key}>
            <figure className={styles.figure} style={ratios}>
              <picture>
                <source
                  media="(max-width: 959px)"
                  srcSet={narrow.props.srcSet}
                  sizes={common.sizes}
                />
                {/* A plain img inside a picture: art direction through getImageProps. */}
                <img
                  {...wide.props}
                  alt={common.alt}
                  className={`${base.ink} ${styles.art}`}
                  loading="lazy"
                  data-bloom="waiting"
                />
              </picture>
              <figcaption className={`${base.caption} ${styles.caption}`}>
                {copy(ink.illustration)}
              </figcaption>
            </figure>
            <div className={styles.words}>
              {place.when ? <p className={styles.when}>{copy(place.when)}</p> : null}
              <h3 className={styles.name} data-place-name="">
                {copy(place.name)}
              </h3>
              {place.title ? <p className={styles.title}>{copy(place.title)}</p> : null}
              <p className={styles.text}>{copy(place.text)}</p>
              {place.links.length ? (
                <p className={styles.links}>
                  {place.links.map((link) => (
                    <a
                      key={link.url}
                      className={base.textLink}
                      href={link.url}
                      target="_blank"
                      rel="noreferrer"
                    >
                      {copy(link.label)}
                      <ArrowUpRight size={15} aria-hidden="true" />
                    </a>
                  ))}
                </p>
              ) : null}
            </div>
          </li>
        );
      })}
    </ol>
  );
}
