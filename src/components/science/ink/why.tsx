"use client";

import { ArrowRight, ArrowUpRight } from "lucide-react";
import { getImageProps } from "next/image";
import { useEffect, useRef, useState, type CSSProperties, type RefObject } from "react";
import { useSiteDialogs } from "@/components/ink/dialogs";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { ink, why } from "../science-content";
import { scienceArt } from "./science-art";
import styles from "./why.module.css";

const SIZES = "(max-width: 959px) 100vw, min(100vw, 1600px)";

/** How long after the town starts to bloom (with 40% of it in the window) its first lamps come on:
 *  the blot is then well grown, so the windows light in a painting you can already see. */
const LAMPS_AFTER = 1300;

/** The longest the lamps wait for their pictures to finish decoding. */
const DECODE_WAIT = 2500;

/**
 * The signature moment (round 3): the town's windows light up, a few at a time (why.module.css
 * staggers the six layers), once. It waits for the town's bloom to start (the kit's useBloom sets
 * data-bloom as it enters the window), for 40% of the figure to be in the window, and for the lamp
 * pictures to be decoded, so on a slow link they still fade up instead of popping in. Reduced
 * motion: lit from the first paint. No script: the stylesheet shows it lit.
 */
function useLampsOn(figure: RefObject<HTMLElement | null>, motion: boolean) {
  const [on, setOn] = useState(false);
  useEffect(() => {
    const element = figure.current;
    const art = element?.querySelector<HTMLElement>("[data-bloom]");
    if (!element || !art || !motion) return;
    let alive = true;
    let timer = 0;
    let wait = 0;
    let bloomed = false;
    let seen = false;
    // Only the lamps this layout shows (the six layers from 960px, the phone's lit cut under it): a
    // lazy picture that is not displayed never loads, so it would never decode.
    const decoded = () =>
      Promise.race([
        Promise.all(
          [...element.querySelectorAll<HTMLImageElement>("img[data-lamp]")]
            .filter((img) => getComputedStyle(img).display !== "none")
            .map((img) => img.decode().catch(() => {})),
        ),
        new Promise<void>((resolve) => (wait = window.setTimeout(resolve, DECODE_WAIT))),
      ]);
    const start = () => {
      if (!bloomed || !seen || timer) return;
      blooming.disconnect();
      view.disconnect();
      const loaded = decoded();
      timer = window.setTimeout(() => loaded.then(() => alive && setOn(true)), LAMPS_AFTER);
    };
    const blooming = new MutationObserver(() => {
      bloomed = art.dataset.bloom === "in" || art.dataset.bloom === "done";
      start();
    });
    const view = new IntersectionObserver(
      (entries) => {
        const entry = entries[entries.length - 1];
        seen = entry.isIntersecting && entry.intersectionRatio >= 0.39;
        start();
      },
      { threshold: [0, 0.4] },
    );
    blooming.observe(art, { attributes: true, attributeFilter: ["data-bloom"] });
    view.observe(element);
    bloomed = art.dataset.bloom === "in" || art.dataset.bloom === "done";
    return () => {
      alive = false;
      blooming.disconnect();
      view.disconnect();
      window.clearTimeout(timer);
      window.clearTimeout(wait);
    };
  }, [figure, motion]);
  return on || !motion;
}

/**
 * "Why start with the cell?" (round 3, Mo, November 4, 2026: say why BiGH's science is cell
 * science). The heading and its lead, then San Francisco's houses at dusk across the window, their
 * windows lighting one group at a time in gold leaf (each house lights its own lamp, as each cell
 * makes its own energy), the line that says so, and three numbered lines, each opening the kit's
 * explainer sheet (the sheets "Make sense of the science." opened before). On a phone the town is
 * its own tighter cut and its lit picture fades in whole.
 */
export function Why({ motion }: { motion: boolean }) {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  const figure = useRef<HTMLElement>(null);
  const on = useLampsOn(figure, motion);
  const art = scienceArt.town;
  const common = { alt: copy(why.alt), sizes: SIZES };
  const wide = getImageProps({ ...common, src: art.src, width: art.width, height: art.height });
  const narrow = getImageProps({
    ...common,
    src: art.phone.src,
    width: art.phone.width,
    height: art.phone.height,
  });
  const lamp = (src: string) =>
    getImageProps({ alt: "", sizes: SIZES, src, width: art.width, height: art.height }).props;
  const phoneLit = getImageProps({
    alt: "",
    sizes: SIZES,
    src: art.phoneLit.src,
    width: art.phoneLit.width,
    height: art.phoneLit.height,
  }).props;
  const ratios = {
    "--ar-wide": `${art.width} / ${art.height}`,
    "--ar-narrow": `${art.phone.width} / ${art.phone.height}`,
  } as CSSProperties;
  return (
    // id "health": the address the footer's "Cellular health" and "Health, explained", the
    // homepage's science and the switched-off Science menu link to (it was "Make sense of the
    // science." until round 3; this chapter took its explainers).
    <section id="health" className={styles.why} aria-labelledby="why-title">
      <div className={`${base.wrap} ${styles.head}`}>
        <h2 id="why-title" className={styles.title}>
          {copy(why.title)}
        </h2>
        <p className={styles.lead}>{copy(why.lead)}</p>
      </div>
      <figure ref={figure} className={styles.figure} style={ratios} data-lamps={on ? "on" : "off"}>
        {/* One group, multiplied onto the paper as a whole (the kit's .ink), and bloomed as one, so
            the lamps never show before the town or as boxes of their own. */}
        <div className={`${base.ink} ${styles.art}`} data-bloom="waiting">
          <picture>
            <source media="(max-width: 959px)" srcSet={narrow.props.srcSet} sizes={SIZES} />
            <img {...wide.props} alt={common.alt} className={styles.town} loading="lazy" />
          </picture>
          {/* The lamps are plain imgs from getImageProps (the optimizer's srcSet, the town's size):
              layers over the town's picture, not pictures of their own. */}
          {art.lamps.map((src, k) => (
            // eslint-disable-next-line @next/next/no-img-element
            <img
              key={src}
              {...lamp(src)}
              alt=""
              className={styles.lamp}
              loading="lazy"
              data-lamp=""
              style={{ "--k": k } as CSSProperties}
            />
          ))}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img {...phoneLit} alt="" className={styles.phoneLit} loading="lazy" data-lamp="" />
        </div>
        <figcaption className={`${base.wrap} ${styles.caption}`}>
          <span className={styles.line}>{copy(why.caption)}</span>
          <span className={base.caption}>{copy(ink.illustration)}</span>
        </figcaption>
      </figure>
      <div className={base.wrap}>
        <ol className={styles.lines} role="list">
          {why.lines.map((line, index) => (
            <li key={line.link} className={styles.item}>
              <span className={styles.number}>{index + 1}</span>
              <p className={styles.text} id={`why-line-${index}`}>
                {copy(line.text)}
              </p>
              <button
                type="button"
                className={styles.go}
                aria-describedby={`why-line-${index}`}
                onClick={() => dialogs.openArticle(index)}
              >
                {copy(line.link)} <ArrowRight size={16} aria-hidden="true" />
              </button>
            </li>
          ))}
        </ol>
        <p className={styles.source}>
          <a href={why.sourceUrl} target="_blank" rel="noreferrer">
            {/* No space before the arrow, so it stays with the last word on a phone. */}
            {copy(why.source)}
            <ArrowUpRight size={14} aria-hidden="true" className={styles.arrow} />
          </a>
        </p>
      </div>
    </section>
  );
}
