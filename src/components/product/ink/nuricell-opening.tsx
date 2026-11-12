"use client";

import Image, { getImageProps } from "next/image";
import { useEffect, useRef, useState, type CSSProperties } from "react";
import { nuricellOpening as art } from "./nuricell-opening-art";
import { nuricellSun as sun } from "./nuricell-sun-art";
import styles from "./nuricell.module.css";

// NuriCell's opening, "A clear day" (Mo picked A of three, November 10, 2026; mockups
// reference/ink-pages/mockups/nuricell-opening/round6/): one loose painting behind the name and
// the bottle, a clear California morning sky over the Pacific and a low grassy bluff. From 960px
// the name sits on the horizon and the bottle stands on the bluff; in one column the bottle stands
// on the bluff under the name. As the page opens the morning fog lifts, once. The words and the buy
// box stay on bare paper under the grass. NuriCell only: the other products keep the plain opening.
//
// It lives inside the bottle's box (opening.tsx `.stand`), so it is sized and placed in bottle
// boxes and follows the bottle at every width and in every language (nuricell.module.css), and
// behind the page's content (z-index -1 inside the page root's own stacking context), multiplied
// onto the paper as one group: the painting, its side pieces and the fog. Two tufts of its own
// grass are laid in front of the bottle's foot, so the bottle stands in the grass (AGENTS.md: "a
// front layer seats it in the painting").
//
// Its sunshine (Mo picked A, "light from the corner", November 11, 2026; mockups
// reference/ink-pages/mockups/nuricell-opening/round7/): the sun is just out of the picture. Its
// warm light pours into the sky from beyond the window's top right corner, and its sparkle lies on
// the sea under that corner: two layers of Codex paint laid in the painting's blend group, over
// the painting and its side pieces and under the fog, placed against the window's right edge so
// the light is in the corner at every width.

// From 960px the painting is 6.48 name-sizes wide (nuricell.module.css), the name at most
// 16.4vw, 30svh and 250px (product-ink.module.css).
const WIDE = "min(107vw, 195vh, 1620px)";
// One column: 3.06 bottle boxes wide (1000 of the painting's 1536 columns, the painting 4.7
// boxes), the box 64vw and at most 320px.
const NARROW = "min(196vw, 980px)";
// A side piece against the painting's width.
const SIDE = "min(88vw, 160vh, 1329px)";
// The sun's light: 42% of the painting's width from 960px, 44% of its middle's in one column. Its
// sparkle on the sea: 17.8% and 20.4% (nuricell.module.css).
const LIGHT = "(min-width: 960px) min(45vw, 82vh, 680px), min(86vw, 431px)";
const GLINT = "(min-width: 960px) min(19vw, 35vh, 288px), min(40vw, 200px)";
// The front grass: 356 of the painting's 1536 columns from 960px, of its 4.7 boxes in one column.
const FRONT = "(min-width: 960px) min(25vw, 46vh, 376px), min(70vw, 349px)";
// The windows wider than the painting, which need its side pieces: wider than 1600px, or more
// than 1.9 times as wide as tall (the name shrinks with a short window). The stylesheet shows the
// pieces at the same windows.
const WIDER = "(min-width: 1601px), (min-width: 960px) and (min-aspect-ratio: 19/10)";
// The painting's numbers for the stylesheet, set on the opening's section (opening.tsx), so both
// the painting and the words under it can use them: its width, its middle's width (one column),
// a side piece's width and how far it lies over the painting, its rows, the rows of its horizon, of
// the bluff's top and of its last paint, and where the front grass lies on it; the sun's light's
// width and its mirrored top, the sparkle's width and its column under the sun.
export const clearDayVars = {
  "--sky-w": art.sky.width,
  "--sky-rows": art.sky.height,
  "--sky-phone-w": art.phone.width,
  "--sky-side-w": art.right.width,
  "--sky-lap": art.lap,
  "--sky-horizon": art.horizon,
  "--sky-bluff": art.bluff,
  "--sky-end": art.end,
  "--sky-front-x": art.front.x,
  "--sky-front-y": art.front.y,
  "--sky-front-w": art.front.width,
  "--light-w": sun.light.width,
  "--light-pad": sun.light.pad,
  "--glint-w": sun.glint.width,
  "--glint-sun": sun.glint.sun,
} as CSSProperties;
// One transparent pixel: what a window that needs no side piece loads in its place.
const NOTHING = "data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw==";

function Side({ which }: { which: "left" | "right" }) {
  const piece = art[which];
  const { props } = getImageProps({
    src: piece.src,
    alt: "",
    width: piece.width,
    height: piece.height,
    sizes: SIDE,
    loading: "eager",
  });
  return (
    <picture className={`${styles.skySide} ${which === "left" ? styles.skyLeft : styles.skyRight}`}>
      <source
        media={WIDER}
        srcSet={props.srcSet}
        sizes={props.sizes}
        width={piece.width}
        height={piece.height}
      />
      {/* Art direction: Next's own srcSet in a window that needs the piece, nothing in any other
          (getImageProps, as ink-chapter.tsx's FramedPicture). */}
      <img src={NOTHING} alt="" width={piece.width} height={piece.height} decoding="async" />
    </picture>
  );
}

/** The painting, its sunshine, its fog, the bottle's shadow on the grass and the grass in front of
 *  its foot: the first children of the bottle's box. The fog waits for the painting ([data-sky="ready"], set when its picture is in, also when
 *  it was in before the page came alive), then lifts once; with scripts off nothing waits; with
 *  reduced motion there is no fog. */
export function ClearDay() {
  const picture = useRef<HTMLImageElement>(null);
  const [ready, setReady] = useState(false);
  useEffect(() => {
    const img = picture.current;
    if (img?.complete && img.naturalWidth) setReady(true);
  }, []);
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
      <span className={styles.sky} data-sky={ready ? "ready" : "waiting"}>
        <picture className={styles.skyArt}>
          <source
            media="(min-width: 960px)"
            srcSet={wide.srcSet}
            sizes={wide.sizes}
            width={art.sky.width}
            height={art.sky.height}
          />
          {/* Art direction: the whole painting from 960px, its middle in one column
              (getImageProps). */}
          <img
            {...narrow}
            ref={picture}
            alt=""
            onLoad={(event) => {
              if (event.currentTarget.naturalWidth) setReady(true);
            }}
          />
        </picture>
        <Side which="left" />
        <Side which="right" />
        <Image
          className={styles.skyLight}
          src={sun.light.src}
          alt=""
          width={sun.light.width}
          height={sun.light.height}
          sizes={LIGHT}
          loading="eager"
        />
        <Image
          className={styles.skyGlint}
          src={sun.glint.src}
          alt=""
          width={sun.glint.width}
          height={sun.glint.height}
          sizes={GLINT}
          loading="eager"
        />
        <span className={styles.skyFog} />
      </span>
      <span className={styles.skyShadow} />
      <Image
        className={styles.skyFront}
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
