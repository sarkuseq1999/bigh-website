"use client";

import Image, { getImageProps } from "next/image";
import { ArrowRight } from "lucide-react";
import { useEffect, useRef, type CSSProperties } from "react";
import { useProductPage } from "@/components/home/product-action";
import { useSiteDialogs } from "@/components/ink/dialogs";
import base from "@/components/ink/ink.module.css";
import { Link } from "@/i18n/navigation";
import { useCopy } from "@/i18n/use-copy";
import { formulas, formulasLine, formulasTitle, ink, iris, liu } from "../science-content";
import { liuArt } from "./liu-art";
import styles from "./people.module.css";

const BOTTLE = { width: 1230, height: 1278 };

// The wide plate is drawn as wide as the window (at most 1800px, and no taller than the window
// under the menu bar: people.module.css); a phone's is the window's width, at most 620px.
const WIDE = "min(100vw, 1800px)";
const TALL = "min(100vw, 620px)";
const share = (value: number) => `${(value * 100).toFixed(2)}%`;

type Gold = (typeof liuArt)["wide" | "phone"]["gold"];

/** A plate's drifting gold: each sliver a piece of one picture, laid where it was painted (the
 *  opening's way: zoom.tsx). The stylesheet shows the set that belongs to the plate in use. */
function Slivers({ gold, className }: { gold: Gold; className: string }) {
  return (
    <div
      className={`${styles.slivers} ${className}`}
      style={{ "--sheet": `url("${gold.src}")` } as CSSProperties}
      aria-hidden="true"
    >
      {gold.slivers.map((sliver, index) => (
        <span
          key={index}
          style={
            {
              left: share(sliver.box[0]),
              top: share(sliver.box[1]),
              width: share(sliver.box[2]),
              height: share(sliver.box[3]),
              backgroundSize: `${share(1 / sliver.at[2])} ${share(1 / sliver.at[3])}`,
              backgroundPosition: `${share(sliver.at[0] / (1 - sliver.at[2]))} ${share(sliver.at[1] / (1 - sliver.at[3]))}`,
              "--dx": sliver.drift[0],
              "--dy": sliver.drift[1],
              "--turn": `${sliver.turn}deg`,
              animationDelay: `${(-sliver.delay[0] * 12).toFixed(2)}s, ${(-sliver.delay[1] * 6).toFixed(2)}s`,
            } as CSSProperties
          }
        />
      ))}
    </div>
  );
}

/** Dr. Liu, after "Why start with the cell?": "the gold he studies" (Mo, November 11, 2026: he
 *  found the part plain, a small dark photograph on bare paper, and picked C of five ideas mocked
 *  on the real page). His painted portrait (his real face, the one NuriCell shows) sits in front
 *  of one huge cell, its mitochondria slivers of gold that drift slowly, as on the page's first
 *  screen; one line says what the gold is. From 960px the painting runs off the window's right
 *  edge and his words stand on the bare paper at its left; a phone gets a tall painting over the
 *  words. The slivers drift only while the painting is in the window, and not at all with reduced
 *  motion or without script. His name with his role under it (no label over the name), the
 *  approved headline and intro, his story sheet. His dated record (280+ papers, 1994, 2025) is
 *  told by his path below, with its sources. */
export function Liu() {
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  const plate = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const node = plate.current;
    if (!node) return;
    const watch = new IntersectionObserver(
      ([entry]) => {
        node.dataset.adrift = entry.isIntersecting ? "on" : "off";
      },
      { rootMargin: "12% 0px" },
    );
    watch.observe(node);
    return () => {
      watch.disconnect();
      delete node.dataset.adrift;
    };
  }, []);

  const wide = getImageProps({
    alt: copy(liu.alt),
    sizes: WIDE,
    src: liuArt.wide.src,
    width: liuArt.wide.width,
    height: liuArt.wide.height,
  }).props;
  const tall = getImageProps({
    alt: "",
    sizes: TALL,
    src: liuArt.phone.src,
    width: liuArt.phone.width,
    height: liuArt.phone.height,
  }).props;
  // The painting's box comes from the stylesheet, whichever picture loads (as the path's).
  const ratios = {
    "--ar-wide": `${liuArt.wide.width} / ${liuArt.wide.height}`,
    "--ar-narrow": `${liuArt.phone.width} / ${liuArt.phone.height}`,
  } as CSSProperties;

  return (
    <div id="liu" className={styles.liu}>
      <figure className={styles.scene} style={ratios}>
        {/* One group on the paper: the painting and its gold multiply together, and bloom in
            together. */}
        <div
          ref={plate}
          className={`${base.ink} ${styles.plate}`}
          data-bloom="waiting"
          data-liu-plate=""
        >
          <picture>
            <source media="(max-width: 959px)" srcSet={tall.srcSet} sizes={TALL} />
            {/* A plain img inside a picture: art direction through getImageProps. */}
            <img {...wide} alt={wide.alt} className={styles.art} loading="lazy" />
          </picture>
          <Slivers gold={liuArt.wide.gold} className={styles.wideGold} />
          <Slivers gold={liuArt.phone.gold} className={styles.tallGold} />
        </div>
        <figcaption className={`${base.caption} ${styles.caption}`}>
          {copy(ink.portrait)} · {copy(ink.illustration)}
        </figcaption>
      </figure>
      <div className={`${base.wrap} ${styles.words}`}>
        <div className={styles.column}>
          <h2 id="liu-name" className={styles.name}>
            {copy(liu.name)}
          </h2>
          <p className={styles.role}>{copy(liu.role)}</p>
          <p className={styles.headline}>{copy(liu.headline)}</p>
          <p className={`${base.body} ${styles.intro}`}>{copy(liu.intro)}</p>
          <p className={styles.goldLine}>
            <span className={styles.leaf} aria-hidden="true" />
            {copy(liu.gold)}
          </p>
          <button
            type="button"
            className={`${base.textLink} ${styles.story}`}
            onClick={dialogs.openScientist}
          >
            {copy(liu.button)} <ArrowRight size={18} aria-hidden="true" />
          </button>
        </div>
      </div>
    </div>
  );
}

/** The five formulas: who developed each one, each bottle linking to its own page. Round 3: after
 *  his path's "Today", a short heading of its own, the credit line as its lead (no label). */
export function Formulas() {
  const copy = useCopy();
  const pageOf = useProductPage();
  return (
    <section id="formulas" className={styles.formulas} aria-labelledby="formulas-title">
      <div className={base.wrap}>
        <header className={styles.head}>
          <h2 id="formulas-title" className={styles.title}>
            {copy(formulasTitle)}
          </h2>
          <p className={base.body}>
            {copy(formulasLine)} {copy(iris.text)}
          </p>
        </header>
        <ul className={styles.bottles}>
          {formulas.map((formula, index) => {
            const href = pageOf(formula.name);
            const body = (
              <>
                <Image
                  src={formula.image}
                  width={BOTTLE.width}
                  height={BOTTLE.height}
                  alt=""
                  sizes="(max-width: 959px) 40vw, 240px"
                />
                <span className={styles.bottleName}>{copy(formula.name)}</span>
              </>
            );
            return (
              <li key={formula.name} data-lead={index === 0 ? "" : undefined}>
                {href ? (
                  <Link href={href} className={styles.bottleLink}>
                    {body}
                  </Link>
                ) : (
                  <div className={styles.bottleLink}>{body}</div>
                )}
                <p className={styles.credit}>{copy(formula.credit)}</p>
              </li>
            );
          })}
        </ul>
      </div>
    </section>
  );
}
