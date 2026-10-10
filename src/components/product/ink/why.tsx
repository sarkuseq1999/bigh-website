"use client";

import Image from "next/image";
import { useEffect, useRef, useState, type CSSProperties, type RefObject } from "react";
import { CountUp } from "@/components/about/count-up";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct } from "../product-types";
import { CAPTIONS, InkChapter, InkFigure, PICTURE_SIZES, sentences, titleId } from "./ink-chapter";
import styles from "./product-ink.module.css";

/** How long after the unlit lantern starts to bloom (with half of it in the window) its light
 *  starts to come on: the blot is then well over half grown; the light takes one and a quarter
 *  breaths (product-ink.module.css). */
const LIGHT_AFTER = 1800;

/** The longest the light waits for its loaded picture to finish decoding. */
const DECODE_WAIT = 2500;

/**
 * The signature moment: the light comes on once, a breath after the lantern starts to bloom. It
 * waits for three things: the unlit picture's bloom has started (its data-bloom, which the kit's
 * useBloom sets as it enters the window), at least half of the lantern's figure is in the window
 * (a slow scroller sees the lantern before its light), and the lit picture has loaded and decoded,
 * so on a slow link the light still fades up instead of popping in when its picture arrives (a
 * lit picture that never loads leaves the lantern unlit). Reduced motion: lit from the first paint
 * (derived, not set in the effect). No script: the stylesheet shows it lit.
 */
function useLightComesOn(
  unlit: RefObject<HTMLImageElement | null>,
  lit: RefObject<HTMLImageElement | null>,
  motion: boolean,
) {
  const [on, setOn] = useState(false);
  useEffect(() => {
    const img = unlit.current;
    const light = lit.current;
    const figure = img?.closest("figure");
    if (!img || !light || !figure || !motion) return;
    let alive = true;
    let timer = 0;
    let wait = 0;
    let bloomed = false;
    let seen = false;
    const listening = new AbortController();
    const loaded = new Promise<void>((resolve) => {
      if (light.complete && light.naturalWidth > 0) resolve();
      else
        light.addEventListener("load", () => resolve(), { once: true, signal: listening.signal });
    }).then(() =>
      Promise.race([
        light.decode().catch(() => {}),
        new Promise<void>((resolve) => (wait = window.setTimeout(resolve, DECODE_WAIT))),
      ]),
    );
    const start = () => {
      if (!bloomed || !seen || timer) return;
      blooming.disconnect();
      view.disconnect();
      timer = window.setTimeout(() => loaded.then(() => alive && setOn(true)), LIGHT_AFTER);
    };
    const blooming = new MutationObserver(() => {
      bloomed = img.dataset.bloom === "in" || img.dataset.bloom === "done";
      start();
    });
    const view = new IntersectionObserver(
      ([entry]) => {
        seen = entry.isIntersecting && entry.intersectionRatio >= 0.49;
        start();
      },
      { threshold: [0, 0.5] },
    );
    blooming.observe(img, { attributes: true, attributeFilter: ["data-bloom"] });
    view.observe(figure);
    bloomed = img.dataset.bloom === "in" || img.dataset.bloom === "done";
    return () => {
      alive = false;
      blooming.disconnect();
      view.disconnect();
      listening.abort();
      window.clearTimeout(timer);
      window.clearTimeout(wait);
    };
  }, [unlit, lit, motion]);
  return on || !motion;
}

export function Why({ product, motion }: { product: InkProduct; motion: boolean }) {
  const copy = useCopy();
  const why = product.why;
  const art = product.ink.why;
  const unlit = useRef<HTMLImageElement>(null);
  const lit = useRef<HTMLImageElement>(null);
  const on = useLightComesOn(unlit, lit, motion);
  if (!why) return null;
  return (
    <InkChapter
      id="why"
      picture={
        <InkFigure
          art={art.unlit}
          alt={art.alt}
          caption={CAPTIONS.illustration}
          imgRef={unlit}
          attrs={{ "data-lantern": "", "data-light": on ? "on" : "off" }}
        >
          {/* Loaded at once, not lazily: the light waits for it (useLightComesOn). */}
          <Image
            ref={lit}
            className={styles.lit}
            src={art.lit.src}
            alt=""
            width={art.lit.width}
            height={art.lit.height}
            sizes={PICTURE_SIZES}
            loading="eager"
            data-lit=""
          />
          {art.lit.gold ? (
            <span
              className={`${base.gold} ${styles.litGold}`}
              style={{ ["--gold" as string]: `url(${art.lit.gold})` } as CSSProperties}
            />
          ) : null}
        </InkFigure>
      }
    >
      <p className={`${base.label} ${styles.label}`}>{copy(why.label)}</p>
      {/* One line per sentence (the kit's .display > span is a block): balance alone strands
          "A" at the end of the first line. Each sentence is translated on its own (the catalogs
          have them one by one), and a space between them keeps the text, to a screen reader or a
          copy, one sentence after the other, not "plants.A big". */}
      <h2 id={titleId("why")} className={`${base.display} ${styles.heading}`}>
        {sentences(why.title).map((sentence, i) => (
          <span key={sentence}>
            {i > 0 ? " " : null}
            {copy(sentence)}
          </span>
        ))}
      </h2>
      {why.lines.map((line) => (
        <p key={line} className={styles.text}>
          {copy(line)}
        </p>
      ))}
      {why.facts?.length ? (
        <dl className={styles.facts}>
          {why.facts.map((fact) => (
            <div key={fact.line}>
              <dt className={styles.figureNumber}>
                <CountUp to={fact.figure} suffix={fact.unit} />
              </dt>
              <dd>{copy(fact.line)}</dd>
            </div>
          ))}
        </dl>
      ) : null}
      {why.comparison ? <p className={styles.comparison}>{copy(why.comparison)}</p> : null}
      {why.source ? <p className={`${base.caption} ${styles.source}`}>{copy(why.source)}</p> : null}
    </InkChapter>
  );
}
