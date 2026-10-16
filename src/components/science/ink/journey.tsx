"use client";

import { ArrowUpRight } from "lucide-react";
import { useRef, type CSSProperties } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { ink, pathStops } from "../science-content";
import { OpeningWords } from "./opening";
import { scienceArt } from "./science-art";
import { useJourney } from "./use-journey";
import styles from "./journey.module.css";

const ART = scienceArt.scroll;
const AT = [
  ART.stops.okayama,
  ART.stops.berkeley,
  ART.stops.y2002,
  ART.stops.salzburg,
  ART.stops.today,
] as const;

/**
 * The handscroll (Mo, October 13-14, 2026): the title, then Dr. Liu's path as one ink painting
 * that travels sideways while the page scrolls down (Okayama, the ocean, Berkeley, Salzburg,
 * California under a gold sun), its five stops under their places. Phones get a shorter picture
 * (the same painting, 400px tall). Reduced motion, no script, print and a window too short for the
 * pinned box or too wide for the painting to travel (journey.module.css, useJourney): the still
 * scroll, whose band the visitor scrolls sideways.
 */
export function Journey({ motion }: { motion: boolean }) {
  const copy = useCopy();
  const section = useRef<HTMLElement>(null);
  const short = useJourney(section, motion, AT);
  const still = !motion || short;
  return (
    <section
      ref={section}
      id="scientists"
      className={styles.journey}
      data-now="0"
      aria-labelledby="science-title"
      style={{ "--ratio": ART.width / ART.height } as CSSProperties}
    >
      <div className={styles.pin} data-pin="">
        <OpeningWords />
        <div
          className={styles.band}
          data-band=""
          role={still ? "region" : undefined}
          tabIndex={still ? 0 : undefined}
          aria-label={still ? copy(ink.scrollStill) : undefined}
        >
          <picture>
            <source
              media="(max-width: 959px)"
              srcSet={ART.phone.src}
              width={ART.phone.width}
              height={ART.phone.height}
            />
            {/* A plain picture: the painting is wider than next/image serves (3840px). */}
            <img
              className={styles.painting}
              data-painting=""
              src={ART.src}
              width={ART.width}
              height={ART.height}
              alt={copy(ink.scrollAlt)}
              fetchPriority="high"
              decoding="async"
              data-bloom="waiting"
            />
          </picture>
        </div>
        <div className={`${base.wrap} ${styles.foot}`} style={{ maxWidth: "none" }}>
          <div className={styles.dots} aria-hidden="true">
            <i />
            <i />
            <i />
            <i />
            <i />
          </div>
          <p className={styles.hint} aria-hidden="true">
            {copy(ink.scrollHint)}
          </p>
          <p className={base.caption}>{copy(ink.illustration)}</p>
        </div>
        <div className={styles.track}>
          <div className={styles.rail} aria-hidden="true">
            <span />
          </div>
          {/* role="list": list-style none drops the list in Safari/VoiceOver. */}
          <ol className={styles.stops} role="list">
            {pathStops.map((stop, i) => (
              <li key={stop.mark} data-stop={i} style={{ "--at": AT[i] } as CSSProperties}>
                <i className={styles.dot} aria-hidden="true" />
                <span className={styles.mark}>{copy(stop.mark)}</span>
                <span className={styles.stopTitle}>{copy(stop.title)}</span>
                <p className={styles.stopText}>
                  {copy(stop.text)}{" "}
                  {stop.url ? (
                    <a href={stop.url} target="_blank" rel="noreferrer">
                      {copy(stop.link)}
                      <ArrowUpRight size={14} aria-hidden="true" />
                    </a>
                  ) : null}
                </p>
              </li>
            ))}
          </ol>
        </div>
      </div>
      <div className={styles.room} data-room="" aria-hidden="true" />
    </section>
  );
}
