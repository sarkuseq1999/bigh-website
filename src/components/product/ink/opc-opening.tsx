"use client";

import Image, { getImageProps } from "next/image";
import type { CSSProperties } from "react";
import type { ProductPage } from "../product-types";
import { opcOpening as art } from "./opc-opening-art";
import styles from "./opc.module.css";

// Advanced OPC Formula's opening, a vineyard at harvest (Mo picked B of three, November 16, 2026;
// mockups reference/ink-pages/mockups/opc-opening/): one loose ink-and-wash painting behind the
// name and the bottle, golden California hills with valley oaks under a clear sky, and in front
// the ends of vine rows heavy with dark grapes. From 960px the name rests over the hills and the
// bottle stands on the dry grass between the rows; in one column the bottle stands on the grass
// under the name. The words and the buy box stay on bare paper under the grass.
//
// It is laid as NuriCell's clear day is (nuricell-opening.tsx): inside the bottle's box
// (opening.tsx `.stand`), so it is sized and placed in bottle boxes and follows the bottle at every
// width and in every language (opc.module.css), behind the page's content (z-index -1 inside the
// page root's own stacking context), multiplied onto the paper. In a window wider than it would be
// at the name's size it is drawn as wide as the window (no side pieces: mirrored ones made a "V" of
// vine posts at the joint). A little of its own dry grass is laid in front of the bottle's foot, so
// the bottle stands in the grass (AGENTS.md: "a front layer seats it in the painting").

export function isOpc(product: Pick<ProductPage, "slug">) {
  return product.slug === "advanced-opc";
}

// From 960px the painting is about 3.98 bottle boxes wide (opc.module.css), the box about 27vw
// while the name is set by the window's width, and at least the window's width.
const WIDE = "108vw";
// One column: 3.06 bottle boxes wide (1000 columns of the painting drawn closer, at the scale of
// the painting 4.7 boxes wide), the box 64vw and at most 320px.
const NARROW = "min(196vw, 980px)";
// The front grass: 156 of the painting's 1536 columns.
const FRONT = "(min-width: 960px) 11vw, min(31vw, 153px)";

/** The painting's numbers for the stylesheet, set on the opening's section (opening.tsx), so both
 *  the painting and the words under it can use them: its width and rows, its middle's width (one
 *  column), the rows of the hills under the name, of the ground the bottle stands on and of its
 *  last paint, and where the front grass lies on it. */
export const vineyardVars = {
  "--vine-w": art.sky.width,
  "--vine-rows": art.sky.height,
  "--vine-phone-w": art.phone.width,
  "--vine-hills": art.hills,
  "--vine-ground": art.ground,
  "--vine-end": art.end,
  "--vine-front-x": art.front.x,
  "--vine-front-y": art.front.y,
  "--vine-front-w": art.front.width,
} as CSSProperties;

/** The painting, the bottle's shadow on the grass and the grass in front of its foot: the first
 *  children of the bottle's box. */
export function Vineyard() {
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
  return (
    <>
      <span className={styles.vines} data-vineyard="">
        <picture className={styles.vineArt}>
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
      <span className={styles.vineShadow} />
      <Image
        className={styles.vineFront}
        src={art.front.src}
        alt=""
        width={art.front.width}
        height={art.front.height}
        sizes={FRONT}
        loading="eager"
      />
    </>
  );
}
