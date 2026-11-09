"use client";

import { getImageProps } from "next/image";
import { useEffect, useRef, type CSSProperties, type ReactNode } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { ink, opening, why } from "../science-content";
import { scienceArt } from "./science-art";
import styles from "./zoom.module.css";

const SIZES = "100vw";
const CELL_SIZES = "(max-width: 959px) 100vw, 56vw";

/** The point of each full-window painting the view moves in on (shares of the painting): the
 *  walker's swinging hand, then the back of that hand. */
const FOCUS = { hills: [0.662, 0.755], hand: [0.44, 0.66] } as const;

// The headline's one gold word, as on the homepage ("cells." there): "cell" in each language. Only
// the first match is gilded.
const GOLD_WORDS = ["cell.", "细胞", "세포", "tế bào", "細胞"];

function gild(text: string, className: string): ReactNode {
  const word = GOLD_WORDS.find((candidate) => text.includes(candidate));
  if (!word) return text;
  const at = text.indexOf(word);
  return (
    <>
      {text.slice(0, at)}
      <span className={className}>{word}</span>
      {text.slice(at + word.length)}
    </>
  );
}

const clamp = (x: number, a: number, b: number) => Math.min(b, Math.max(a, x));
const seg = (p: number, a: number, b: number) => clamp((p - a) / (b - a), 0, 1);
const ease = (t: number) => t * t * (3 - 2 * t);

/**
 * Where a point of an object-fit: cover picture stands in its box, as a transform-origin: the
 * picture's own share (`focus`) moved by how the box crops it (its object-position).
 */
function originOf(img: HTMLImageElement, focus: readonly number[]) {
  // The box before any scale (offsetWidth ignores transforms).
  const box = { width: img.offsetWidth, height: img.offsetHeight };
  if (!box.width || !box.height) return "50% 50%";
  const natural = { w: img.naturalWidth || 3, h: img.naturalHeight || 2 };
  const cover = Math.max(box.width / natural.w, box.height / natural.h);
  const drawn = { w: natural.w * cover, h: natural.h * cover };
  const position = getComputedStyle(img)
    .objectPosition.split(" ")
    .map((v) => parseFloat(v) / 100);
  const x = (box.width - drawn.w) * (position[0] ?? 0.5) + drawn.w * focus[0];
  const y = (box.height - drawn.h) * (position[1] ?? 0.5) + drawn.h * focus[1];
  return `${((x / box.width) * 100).toFixed(2)}% ${((y / box.height) * 100).toFixed(2)}%`;
}

/**
 * The page's first screens as one slow zoom (Mo, November 9, 2026: the desk at the window was
 * plain and the town did not say "cell"; he picked the zoom of three ideas). A walker on golden
 * California hills fills the window, the h1 in the painting's sky. As the page scrolls the view
 * moves in on the walker's hand in the dry grass, then on one cell of it, its mitochondria as
 * slivers of gold, where "Why start with the cell?" and its lead stand. The stage is pinned while
 * the track scrolls by; the script only sets each layer's scale and opacity from the scroll.
 * Reduced motion and no script: no pinning, the hills with the h1, then the cell beside its words
 * (zoom.module.css).
 */
export function Zoom({ motion }: { motion: boolean }) {
  const copy = useCopy();
  const track = useRef<HTMLDivElement>(null);
  const hills = useRef<HTMLImageElement>(null);
  const hand = useRef<HTMLImageElement>(null);
  const cell = useRef<HTMLDivElement>(null);
  const first = useRef<HTMLElement>(null);
  const second = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = {
      track: track.current,
      hills: hills.current,
      hand: hand.current,
      cell: cell.current,
      first: first.current,
      second: second.current,
    };
    if (!motion || !el.track || !el.hills || !el.hand || !el.cell || !el.first || !el.second)
      return;
    const { hills: hillsImg, hand: handImg } = el;
    let frame = 0;
    const draw = () => {
      frame = 0;
      const box = el.track!.getBoundingClientRect();
      const run = box.height - window.innerHeight;
      const p = run > 0 ? clamp(-box.top / run, 0, 1) : 0;
      el.track!.dataset.zoomAt = p < 0.36 ? "hills" : p < 0.76 ? "hand" : "cell";

      // The walk: held, then in on the walker's hand.
      hillsImg.style.scale = String(Math.pow(9, ease(seg(p, 0.08, 0.4))));
      hillsImg.style.opacity = String(1 - seg(p, 0.33, 0.4));

      // The hand: arrives a little wide and settles, then in on its skin.
      const settle = ease(seg(p, 0.28, 0.46));
      const into = ease(seg(p, 0.56, 0.8));
      handImg.style.scale = String((1.25 - 0.25 * settle) * Math.pow(7, into));
      handImg.style.opacity = String(seg(p, 0.33, 0.4) * (1 - seg(p, 0.72, 0.8)));

      // The cell: comes up out of the skin and settles; then its words.
      el.cell!.style.scale = String(0.45 + 0.55 * ease(seg(p, 0.7, 0.9)));
      el.cell!.style.opacity = String(seg(p, 0.7, 0.84));
      const words = seg(p, 0.82, 0.92);
      el.second!.style.setProperty("--words", String(words));
      el.second!.style.visibility = p < 0.7 ? "hidden" : "visible";
      const title = 1 - seg(p, 0.06, 0.16);
      el.first!.style.opacity = String(title);
      el.first!.style.visibility = title === 0 ? "hidden" : "visible";
    };
    const queue = () => {
      if (!frame) frame = window.requestAnimationFrame(draw);
    };
    const measure = () => {
      hillsImg.style.transformOrigin = originOf(hillsImg, FOCUS.hills);
      handImg.style.transformOrigin = originOf(handImg, FOCUS.hand);
      queue();
    };
    measure();
    window.addEventListener("scroll", queue, { passive: true });
    window.addEventListener("resize", measure);
    hillsImg.addEventListener("load", measure);
    handImg.addEventListener("load", measure);
    return () => {
      window.cancelAnimationFrame(frame);
      window.removeEventListener("scroll", queue);
      window.removeEventListener("resize", measure);
      hillsImg.removeEventListener("load", measure);
      handImg.removeEventListener("load", measure);
      for (const node of [hillsImg, handImg, el.cell!, el.first!, el.second!]) {
        node.style.scale = "";
        node.style.opacity = "";
        node.style.visibility = "";
        node.style.transformOrigin = "";
      }
      el.second!.style.removeProperty("--words");
    };
  }, [motion]);

  const art = scienceArt.zoom;
  // The first screen's picture: fetched at once and first.
  const hillsProps = getImageProps({
    alt: copy(opening.alt),
    sizes: SIZES,
    src: art.hills.src,
    width: art.hills.width,
    height: art.hills.height,
    loading: "eager",
    fetchPriority: "high",
  }).props;
  // The hand is a view on the way from the walker to the cell, not a picture of its own: no alt.
  const handProps = getImageProps({
    alt: "",
    sizes: SIZES,
    src: art.hand.src,
    width: art.hand.width,
    height: art.hand.height,
  }).props;
  const cellProps = getImageProps({
    alt: copy(why.alt),
    sizes: CELL_SIZES,
    src: art.cell.src,
    width: art.cell.width,
    height: art.cell.height,
  }).props;
  const ratio = { "--ar-cell": `${art.cell.width} / ${art.cell.height}` } as CSSProperties;

  return (
    <div ref={track} className={styles.zoom} data-zoom="" data-zoom-at="hills">
      <div className={styles.stage}>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          {...hillsProps}
          ref={hills}
          alt={hillsProps.alt}
          className={`${base.ink} ${styles.plate} ${styles.hills}`}
          data-bloom="waiting"
          data-zoom-layer="hills"
        />
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          {...handProps}
          ref={hand}
          alt=""
          className={`${base.ink} ${styles.plate} ${styles.hand}`}
          data-zoom-layer="hand"
        />
        <header ref={first} className={styles.first}>
          <h1 id="science-title" className={styles.title}>
            {gild(copy(opening.title), styles.gold)}
          </h1>
          <p className={styles.lead}>{copy(opening.lead)}</p>
          <p className={`${base.caption} ${styles.label}`}>{copy(ink.illustration)}</p>
        </header>
        <div ref={second} className={styles.second} style={ratio}>
          <div className={styles.words}>
            <h2 id="why-title" className={styles.subtitle}>
              {copy(why.title)}
            </h2>
            <p className={styles.sublead}>{copy(why.lead)}</p>
          </div>
          <figure className={styles.figure}>
            <div ref={cell} className={`${base.ink} ${styles.cell}`} data-zoom-layer="cell">
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img {...cellProps} alt={cellProps.alt} className={styles.cellArt} />
            </div>
            <figcaption className={styles.caption}>
              <span className={styles.line}>{copy(why.caption)}</span>
              <span className={base.caption}>{copy(ink.illustration)}</span>
            </figcaption>
          </figure>
        </div>
      </div>
      {/* id "health": the address the footer's "Cellular health" and "Health, explained", the
          homepage's science and the switched-off Science menu link to. It stands where the zoom
          has arrived at the cell and "Why start with the cell?". */}
      <span id="health" className={styles.anchor} aria-hidden="true" />
    </div>
  );
}
