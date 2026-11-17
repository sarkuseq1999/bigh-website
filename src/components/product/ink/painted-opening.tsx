"use client";

import Image, { getImageProps } from "next/image";
import type { CSSProperties } from "react";
import { opcOpening } from "./opc-opening-art";
import styles from "./painted-opening.module.css";
import { turmerificOpening } from "./turmerific-opening-art";

// A product's opening painted as a California place (Advanced OPC Formula's vineyard at harvest,
// Mo picked B, November 16, 2026; Turmerific's turmeric field, Mo picked A the same day; mockups
// reference/ink-pages/mockups/<product>-opening/): one loose ink-and-wash painting behind the name
// and the bottle. From 960px the name rests over the painting's far land and the bottle stands on
// its ground; in one column the bottle stands on the ground under the name. The words and the buy
// box stay on bare paper under the painting. NuriCell's clear day (nuricell-opening.tsx) came
// first and has its own code (its fog and sunshine); Green Bee Propolis keeps its own opening.
//
// The painting lies inside the bottle's box (opening.tsx `.stand`), so it is sized and placed in
// bottle boxes and follows the bottle at every width and in every language
// (painted-opening.module.css), behind the page's content (z-index -1 inside the page root's own
// stacking context), multiplied onto the paper. In a window wider than it would be at the name's
// size it is drawn as wide as the window (no side pieces: mirrored ones made a "V" of vine posts at
// the joint). A little of its own ground is laid in front of the bottle's foot, so the bottle
// stands in the painting (AGENTS.md: "a front layer seats it in the painting").

/** A product's opening painting, as its build script writes it (<product>-opening-art.ts). */
type OpeningPainting = {
  sky: { src: string; width: number; height: number };
  phone: { src: string; width: number; height: number };
  front: { src: string; width: number; height: number; x: number; y: number };
  /** Rows of `sky`: the land under the name, the ground the bottle stands on, the last paint. */
  hills: number;
  ground: number;
  end: number;
  /** Where the name's baseline sits in the bottle's box, as a share of its height (measured for
   *  the product's name), and how far the name is lifted off the land, in name-sizes. */
  base: number;
  lift: number;
};

const PAINTINGS: Record<string, OpeningPainting> = {
  "advanced-opc": opcOpening,
  turmerific: turmerificOpening,
};

/** The product's opening painting, or undefined (the plain opening). */
export function openingPainting(slug: string): OpeningPainting | undefined {
  return PAINTINGS[slug];
}

// From 960px the painting is about four bottle boxes wide while the name is set by the window's
// width, and at least the window's width.
const WIDE = "108vw";
// One column: 3.06 bottle boxes wide (1000 columns of the painting drawn closer, at the scale of
// the painting 4.7 boxes wide), the box 64vw and at most 320px.
const NARROW = "min(196vw, 980px)";

/** The painting's numbers for the stylesheet, set on the opening's section (opening.tsx), so both
 *  the painting and the words under it can use them: its width and rows, its middle's width (one
 *  column), the rows of the land under the name, of the ground the bottle stands on and of its
 *  last paint, where the front ground lies on it, and the name's baseline and lift. */
export function paintedVars(art: OpeningPainting) {
  return {
    "--paint-w": art.sky.width,
    "--paint-rows": art.sky.height,
    "--paint-phone-w": art.phone.width,
    "--paint-hills": art.hills,
    "--paint-ground": art.ground,
    "--paint-end": art.end,
    "--paint-front-x": art.front.x,
    "--paint-front-y": art.front.y,
    "--paint-front-w": art.front.width,
    "--paint-base": art.base,
    "--paint-lift": art.lift,
  } as CSSProperties;
}

/** The painting, the bottle's shadow on the ground and the ground in front of its foot: the first
 *  children of the bottle's box. */
export function PaintedOpening({ art }: { art: OpeningPainting }) {
  const { props: wide } = getImageProps({
    src: art.sky.src,
    alt: "",
    width: art.sky.width,
    height: art.sky.height,
    sizes: WIDE,
    loading: "eager",
    fetchPriority: "high",
  });
  const { props: narrow } = getImageProps({
    src: art.phone.src,
    alt: "",
    width: art.phone.width,
    height: art.phone.height,
    sizes: NARROW,
    loading: "eager",
    fetchPriority: "high",
  });
  // The front ground: its share of the painting's columns, at the painting's widths.
  const share = art.front.width / art.sky.width;
  const front = `(min-width: 960px) ${Math.ceil(108 * share)}vw, min(${Math.ceil(196 * share * (art.sky.width / art.phone.width))}vw, ${Math.ceil(980 * share * (art.sky.width / art.phone.width))}px)`;
  return (
    <>
      <span className={styles.painting} data-opening-painting="">
        <picture>
          <source
            media="(min-width: 960px)"
            srcSet={wide.srcSet}
            sizes={wide.sizes}
            width={art.sky.width}
            height={art.sky.height}
          />
          {/* Art direction: the whole painting from 960px, its middle in one column. */}
          <img {...narrow} alt="" />
        </picture>
      </span>
      <span className={styles.paintingShadow} />
      <Image
        className={styles.paintingFront}
        src={art.front.src}
        alt=""
        width={art.front.width}
        height={art.front.height}
        sizes={front}
        loading="eager"
      />
    </>
  );
}
