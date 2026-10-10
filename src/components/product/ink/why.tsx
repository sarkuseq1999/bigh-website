"use client";

import Image from "next/image";
import { useEffect, useRef, useState, type CSSProperties, type RefObject } from "react";
import { CountUp } from "@/components/about/count-up";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct } from "../product-types";
import { CAPTIONS, InkChapter, InkFigure, PICTURE_SIZES, titleId } from "./ink-chapter";
import styles from "./product-ink.module.css";

/** How long after the unlit lantern starts to bloom its light starts to come on (the blot is then
 *  well over half grown; the light takes one and a quarter breaths, product-ink.module.css). */
const LIGHT_AFTER = 1800;

/**
 * The signature moment: the light comes on once, a breath after the lantern starts to bloom. It
 * watches the unlit picture's data-bloom, which the kit's useBloom sets as it enters the window.
 * Reduced motion: lit from the first paint (derived, not set in the effect). No script: the
 * stylesheet shows it lit.
 */
function useLightComesOn(unlit: RefObject<HTMLImageElement | null>, motion: boolean) {
  const [on, setOn] = useState(false);
  useEffect(() => {
    const img = unlit.current;
    if (!img || !motion) return;
    let timer = 0;
    const observer = new MutationObserver(() => check());
    const check = () => {
      if (img.dataset.bloom !== "in" && img.dataset.bloom !== "done") return;
      observer.disconnect();
      timer = window.setTimeout(() => setOn(true), LIGHT_AFTER);
    };
    observer.observe(img, { attributes: true, attributeFilter: ["data-bloom"] });
    check();
    return () => {
      observer.disconnect();
      window.clearTimeout(timer);
    };
  }, [unlit, motion]);
  return on || !motion;
}

export function Why({ product, motion }: { product: InkProduct; motion: boolean }) {
  const copy = useCopy();
  const why = product.why;
  const art = product.ink.why;
  const unlit = useRef<HTMLImageElement>(null);
  const on = useLightComesOn(unlit, motion);
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
          <Image
            className={styles.lit}
            src={art.lit.src}
            alt=""
            width={art.lit.width}
            height={art.lit.height}
            sizes={PICTURE_SIZES}
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
      <h2 id={titleId("why")} className={`${base.display} ${styles.heading}`}>
        {copy(why.title)}
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
