"use client";

import { getImageProps } from "next/image";
import { useEffect, useRef, type CSSProperties, type ReactNode } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { ink, opening, why } from "../science-content";
import { scienceArt } from "./science-art";
import styles from "./zoom.module.css";

const SIZES = "100vw";
// A tall painting covers a narrow upright window by its height: two thirds of a window high wide.
const TALL_SIZES = "(max-aspect-ratio: 2/3) 67vh, 100vw";
const INSIDE_SIZES = "(max-width: 959px) 180vw, 115vw";
const CELL_SIZES = "(max-width: 959px) 100vw, 70vw";
// Upright windows get the hands' and the hills' tall paintings (zoom.module.css frames them by
// the same query).
const UPRIGHT = "(orientation: portrait)";

/** Points the view pulls back from, as shares of each painting: the inside view's nucleus, the
 *  whole cell's nucleus (measured from its box's middle), the back of the climber's hand on the
 *  rock, and the back of the same hand in the painting of her climbing (each in its wide painting
 *  and in its tall one). */
const FOCUS = {
  inside: [0.72, 0.62],
  cell: [0.118, -0.051],
  hand: [0.495, 0.391],
  handTall: [0.547, 0.482],
  hills: [0.796, 0.474],
  hillsTall: [0.767, 0.679],
} as const;

// How small the whole cell gets as it goes down into the skin of the hand.
const SPECK = 0.22;
// How near the climb starts: her hand about as large as the hand just seen. Her tall painting
// shows her smaller in its frame than the wide one, so it starts nearer.
const NEAR = { wide: 9, tall: 11 } as const;

const upright = (img: HTMLImageElement) => img.naturalHeight > img.naturalWidth;

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
const mix = (a: number, b: number, t: number) => a + (b - a) * t;
const share = (value: number) => `${(value * 100).toFixed(2)}%`;

/** Where a point of an object-fit: cover picture stands in its box (px): the picture's own share
 *  (`focus`) moved by how the box crops it (its object-position). */
function pointOf(img: HTMLImageElement, focus: readonly number[]) {
  // The box before any scale (offsetWidth ignores transforms).
  const box = { width: img.offsetWidth, height: img.offsetHeight };
  const natural = { w: img.naturalWidth || 3, h: img.naturalHeight || 2 };
  const cover = Math.max(box.width / natural.w, box.height / natural.h);
  const drawn = { w: natural.w * cover, h: natural.h * cover };
  const position = getComputedStyle(img)
    .objectPosition.split(" ")
    .map((v) => parseFloat(v) / 100);
  return {
    x: (box.width - drawn.w) * (position[0] ?? 0.5) + drawn.w * focus[0],
    y: (box.height - drawn.h) * (position[1] ?? 0.5) + drawn.h * focus[1],
    box,
  };
}

/**
 * The page's first screens as one slow zoom. Since November 10, 2026 it starts inside the cell
 * and pulls back (Mo picked A of four ideas for the first screen: on the walker's hills the
 * picture said "hiking" while the words said "cell", and nothing moved until you scrolled). The
 * inside of one cell fills the window, its mitochondria as slivers of gold adrift, the h1 in its
 * pale corner. As the page scrolls the view pulls back: the cell seen whole, a climber's hand
 * gripping warm granite, then the climber, a woman in her sixties high on a sunlit wall above
 * Yosemite Valley, where "Why start with the cell?" and its lead stand in the sky (Mo picked her
 * on November 12, 2026, of three; a lone small walker and then a grandfather and grandchild
 * walking away had read as plain). The stage is pinned while the track scrolls by;
 * the script only sets each layer's scale, place and opacity from the scroll. Reduced motion and
 * no script: no pinning and no drift, the inside view with the h1, then the climber with "Why start
 * with the cell?" (zoom.module.css).
 */
export function Zoom({ motion }: { motion: boolean }) {
  const copy = useCopy();
  const track = useRef<HTMLDivElement>(null);
  const inside = useRef<HTMLDivElement>(null);
  const cell = useRef<HTMLDivElement>(null);
  const hand = useRef<HTMLImageElement>(null);
  const hills = useRef<HTMLImageElement>(null);
  const first = useRef<HTMLElement>(null);
  const second = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const el = {
      track: track.current,
      inside: inside.current,
      cell: cell.current,
      hand: hand.current,
      hills: hills.current,
      first: first.current,
      second: second.current,
    };
    if (
      !motion ||
      !el.track ||
      !el.inside ||
      !el.cell ||
      !el.hand ||
      !el.hills ||
      !el.first ||
      !el.second
    )
      return;
    const { hills: hillsImg, hand: handImg, inside: insideBox, cell: cellBox } = el;
    // Measured once per size: how large the whole cell must be to fill the window, and where its
    // middle stands at the start (its nucleus on the inside view's nucleus) and at the end (on
    // the back of the hand), as px from the middle of the stage.
    let fill = 4;
    let start = { x: 0, y: 0 };
    let end = { x: 0, y: 0 };
    // From her hand in the painting of her climbing to where the hand just seen stood (px), and
    // how near that painting starts (NEAR, by the painting in use).
    let slide = { x: 0, y: 0 };
    let near: number = NEAR.wide;
    let frame = 0;
    const draw = () => {
      frame = 0;
      const box = el.track!.getBoundingClientRect();
      const run = box.height - window.innerHeight;
      const p = run > 0 ? clamp(-box.top / run, 0, 1) : 0;
      el.track!.dataset.zoomAt =
        p < 0.1 ? "inside" : p < 0.38 ? "cell" : p < 0.66 ? "hand" : "hills";

      // Inside the cell: held, then the view begins to pull back and the whole cell takes over.
      insideBox.style.scale = String(1 - 0.085 * ease(seg(p, 0.05, 0.2)));
      insideBox.style.opacity = String(1 - seg(p, 0.1, 0.2));

      // The cell whole: from so near that it fills the window, to the middle of the window where
      // it is seen whole for a moment, then down into the skin of the hand.
      const whole = ease(seg(p, 0.1, 0.25));
      const down = ease(seg(p, 0.29, 0.42));
      cellBox.style.scale = String(Math.pow(fill, 1 - whole) * Math.pow(SPECK, down));
      cellBox.style.translate = `${mix(mix(start.x, 0, whole), end.x, down).toFixed(1)}px ${mix(mix(start.y, 0, whole), end.y, down).toFixed(1)}px`;
      cellBox.style.opacity = String(seg(p, 0.1, 0.2) * (1 - seg(p, 0.35, 0.42)));

      // The hands: come up out of the skin and settle, then give way as the view widens.
      const arrive = ease(seg(p, 0.3, 0.54));
      const leave = ease(seg(p, 0.56, 0.7));
      handImg.style.scale = String(Math.pow(7, 1 - arrive) * (1.25 - 0.25 * leave));
      handImg.style.opacity = String(seg(p, 0.35, 0.42) * (1 - seg(p, 0.62, 0.7)));

      // The climb: from her hand on the rock out to the whole wall and the valley below. It
      // starts where the hand just seen stood and about as large, and settles as the view
      // widens; then its words, all there a little before the end (the #health link lands just
      // short of it).
      const wide = ease(seg(p, 0.6, 0.9));
      hillsImg.style.scale = String(Math.pow(near, 1 - wide));
      hillsImg.style.translate = `${(slide.x * (1 - wide)).toFixed(1)}px ${(slide.y * (1 - wide)).toFixed(1)}px`;
      hillsImg.style.opacity = String(seg(p, 0.62, 0.7));
      const words = seg(p, 0.86, 0.93);
      el.second!.style.setProperty("--words", String(words));
      el.second!.style.visibility = p < 0.84 ? "hidden" : "visible";
      const title = 1 - seg(p, 0.05, 0.13);
      el.first!.style.opacity = String(title);
      el.first!.style.visibility = title === 0 ? "hidden" : "visible";
    };
    const queue = () => {
      if (!frame) frame = window.requestAnimationFrame(draw);
    };
    const measure = () => {
      const stage = insideBox.offsetParent as HTMLElement | null;
      if (!stage) return;
      const middle = { x: stage.clientWidth / 2, y: stage.clientHeight / 2 };
      // Each painting in use: the tall one on an upright window.
      const handAt = pointOf(handImg, upright(handImg) ? FOCUS.handTall : FOCUS.hand);
      const hillsAt = pointOf(hillsImg, upright(hillsImg) ? FOCUS.hillsTall : FOCUS.hills);
      handImg.style.transformOrigin = `${handAt.x.toFixed(1)}px ${handAt.y.toFixed(1)}px`;
      hillsImg.style.transformOrigin = `${hillsAt.x.toFixed(1)}px ${hillsAt.y.toFixed(1)}px`;
      // The whole cell is an oval about 0.47 of its box wide and 0.46 tall (from its middle): it
      // fills the window once that oval, wherever it stands, reaches the window's far corners.
      const size = { w: cellBox.offsetWidth, h: cellBox.offsetHeight };
      const nucleus = {
        x: insideBox.offsetLeft + insideBox.offsetWidth * FOCUS.inside[0],
        y: insideBox.offsetTop + insideBox.offsetHeight * FOCUS.inside[1],
      };
      let need = 1;
      for (let i = 0; i < 4; i++) {
        // The cell's middle, were it this large with its nucleus on the inside view's.
        const at = {
          x: nucleus.x - size.w * FOCUS.cell[0] * need,
          y: nucleus.y - size.h * FOCUS.cell[1] * need,
        };
        const far = [0, stage.clientWidth].flatMap((x) =>
          [0, stage.clientHeight].map((y) =>
            Math.hypot((x - at.x) / (size.w * 0.47), (y - at.y) / (size.h * 0.46)),
          ),
        );
        need = Math.max(...far) * 1.12;
      }
      fill = Math.max(2, need);
      start = {
        x: nucleus.x - size.w * FOCUS.cell[0] * fill - middle.x,
        y: nucleus.y - size.h * FOCUS.cell[1] * fill - middle.y,
      };
      end = { x: handAt.x - middle.x, y: handAt.y - middle.y };
      slide = { x: handAt.x - hillsAt.x, y: handAt.y - hillsAt.y };
      near = upright(hillsImg) ? NEAR.tall : NEAR.wide;
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
      for (const node of [insideBox, cellBox, handImg, hillsImg, el.first!, el.second!]) {
        node.style.scale = "";
        node.style.translate = "";
        node.style.opacity = "";
        node.style.visibility = "";
        node.style.transformOrigin = "";
      }
      el.second!.style.removeProperty("--words");
    };
  }, [motion]);

  const art = scienceArt.zoom;
  // The first screen's picture: fetched at once and first.
  const insideProps = getImageProps({
    alt: copy(opening.alt),
    sizes: INSIDE_SIZES,
    src: art.inside.src,
    width: art.inside.width,
    height: art.inside.height,
    loading: "eager",
    fetchPriority: "high",
  }).props;
  // The whole cell and the hand are views on the way out to the climber, not
  // pictures of their own: no alt.
  const cellProps = getImageProps({
    alt: "",
    sizes: CELL_SIZES,
    src: art.cell.src,
    width: art.cell.width,
    height: art.cell.height,
  }).props;
  const handProps = getImageProps({
    alt: "",
    sizes: SIZES,
    src: art.hand.src,
    width: art.hand.width,
    height: art.hand.height,
  }).props;
  const handTallProps = getImageProps({
    alt: "",
    sizes: TALL_SIZES,
    src: art.hand.phone.src,
    width: art.hand.phone.width,
    height: art.hand.phone.height,
  }).props;
  const hillsProps = getImageProps({
    alt: copy(why.alt),
    sizes: SIZES,
    src: art.hills.src,
    width: art.hills.width,
    height: art.hills.height,
  }).props;
  const hillsTallProps = getImageProps({
    alt: "",
    sizes: TALL_SIZES,
    src: art.hills.phone.src,
    width: art.hills.phone.width,
    height: art.hills.phone.height,
  }).props;
  const gold = art.inside.gold;
  const sheet = { "--sheet": `url("${gold.src}")` } as CSSProperties;
  const ratio = { "--ar-cell": `${art.cell.width} / ${art.cell.height}` } as CSSProperties;

  return (
    <div ref={track} className={styles.zoom} data-zoom="" data-zoom-at="inside">
      <div className={styles.stage}>
        {/* The last view, under the others until the view has pulled all the way back: the wide
            painting, or the tall one on an upright window (art direction through getImageProps). */}
        <picture>
          <source media={UPRIGHT} srcSet={hillsTallProps.srcSet} sizes={TALL_SIZES} />
          <img
            {...hillsProps}
            ref={hills}
            alt={hillsProps.alt}
            className={`${base.ink} ${styles.plate} ${styles.hills}`}
            data-zoom-layer="hills"
          />
        </picture>
        <picture>
          <source media={UPRIGHT} srcSet={handTallProps.srcSet} sizes={TALL_SIZES} />
          <img
            {...handProps}
            ref={hand}
            alt=""
            className={`${base.ink} ${styles.plate} ${styles.hand}`}
            data-zoom-layer="hand"
          />
        </picture>
        <div
          ref={cell}
          className={`${base.ink} ${styles.cell}`}
          style={ratio}
          data-zoom-layer="cell"
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img {...cellProps} alt="" className={styles.cellArt} />
        </div>
        {/* The first view: the inside of the cell, a little larger than the window so the view
            can begin to pull back, its gold in pieces above it. The box only clips it. */}
        <div className={styles.view}>
          <div
            ref={inside}
            className={`${base.ink} ${styles.inside}`}
            data-bloom="waiting"
            data-zoom-layer="inside"
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img {...insideProps} alt={insideProps.alt} className={styles.wash} />
            <div className={styles.slivers} style={sheet} aria-hidden="true">
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
          </div>
        </div>
        <header ref={first} className={styles.first}>
          <h1 id="science-title" className={styles.title}>
            {gild(copy(opening.title), styles.gold)}
          </h1>
          <p className={styles.lead}>{copy(opening.lead)}</p>
          <p className={styles.foot}>
            <span className={styles.line}>{copy(opening.caption)}</span>
            <span className={base.caption}>{copy(ink.illustration)}</span>
          </p>
        </header>
        <div ref={second} className={styles.second}>
          <div className={styles.words}>
            <h2 id="why-title" className={styles.subtitle}>
              {copy(why.title)}
            </h2>
            <p className={styles.sublead}>{copy(why.lead)}</p>
          </div>
          <p className={`${base.caption} ${styles.label}`}>{copy(ink.illustration)}</p>
        </div>
      </div>
      {/* id "health": the address the footer's "Cellular health" and "Health, explained", the
          homepage's science and the switched-off Science menu link to. It stands where the view
          has pulled back to the climber and "Why start with the cell?". */}
      <span id="health" className={styles.anchor} aria-hidden="true" />
    </div>
  );
}
