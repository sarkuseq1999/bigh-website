"use client";

import Image from "next/image";
import { useCallback, useEffect, useRef } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { ProductSynergy, ProductSynergyLink } from "../product-types";
import { CAPTIONS } from "./ink-chapter";
import { nuricellGold } from "./nuricell-gold";
import styles from "./nuricell-inside.module.css";

// "Why these four work together" on NuriCell's ink page as three little scenes (Mo picked A,
// October 26, 2026; mockups reference/ink-pages/mockups/nuricell-inside/). Each pair: its two powder
// heaps from the painting (sized by amount), and a few flakes of its gold leaf doing what the two do
// together (the link's `gold`): carried from one heap to the other and lit there; settling on the
// second heap, kept in reserve, one now and then jumping up; or half from each heap, made one. Each
// scene plays as it comes into view (three across: one after another), and again on "Play again".
// Reduced motion: each scene shows its last frame, still. No script: the heaps and the words.

const { leaf, flakes } = nuricellGold.capsule;
const HEAPS = nuricellGold.heaps;
type HeapKey = keyof typeof HEAPS;

/** The flakes each scene uses (the leaf sheet's order: biggest first). */
const CAST = {
  lights: { main: 0, flecks: [16, 17, 19] },
  stores: { main: 4, flecks: [14, 16, 17, 19, 24, 25] },
  joins: { halves: [8, 10], whole: 1 },
} as const;

/** One flake of the leaf, `width` px wide, drawn from the sheet. */
function sprite(layer: HTMLElement, index: number, width: number) {
  const [x, y, w, h] = flakes[index];
  const k = width / w;
  const el = document.createElement("span");
  el.className = styles.flake;
  Object.assign(el.style, {
    width: `${width}px`,
    height: `${h * k}px`,
    backgroundImage: `url(${leaf.src})`,
    backgroundSize: `${leaf.width * k}px ${leaf.height * k}px`,
    backgroundPosition: `${-x * k}px ${-y * k}px`,
  } satisfies Partial<CSSStyleDeclaration>);
  layer.appendChild(el);
  return { el, w: width, h: h * k };
}
type Sprite = ReturnType<typeof sprite>;

/** A transform placing a sprite's centre at (x, y), scaled and turned (degrees). */
const at = (s: Sprite, x: number, y: number, scale = 1, r = 0, ry = 0) =>
  `translate(${x - s.w / 2}px, ${y - s.h / 2}px) scale(${scale}) rotate(${r}deg) rotateY(${ry}deg)`;

/** A heap's tip, width and height in the layer's own coordinates. */
function tip(layer: HTMLElement, heap: HTMLElement) {
  const a = heap.getBoundingClientRect();
  const b = layer.getBoundingClientRect();
  return {
    x: a.left + a.width / 2 - b.left,
    y: a.top + a.height * 0.12 - b.top,
    w: a.width,
    h: a.height,
  };
}

/** Plays a pair's scene in `layer`. Still: every flake straight to its last place, no loops. */
function play(
  layer: HTMLElement,
  heaps: [HTMLElement, HTMLElement],
  kind: ProductSynergyLink["gold"],
  still: boolean,
) {
  layer.replaceChildren();
  const timers: number[] = [];
  const A = tip(layer, heaps[0]);
  const B = tip(layer, heaps[1]);
  const big = Math.max(28, Math.min(56, B.w * 0.46));
  const top =
    Math.min(A.y, B.y) - Math.max(70, Math.abs(B.x - A.x) * 0.3) - Math.abs(B.y - A.y) * 0.2;
  const mx = (A.x + B.x) / 2;
  const go = (s: Sprite, frames: Keyframe[], timing: KeyframeAnimationOptions) =>
    s.el.animate(
      frames,
      still ? { duration: 0, fill: "forwards" } : { fill: "forwards", ...timing },
    );
  // Hanging in the air, turning slowly: lit as it turns towards you, darker as it turns away.
  const hover = (s: Sprite, x: number, y: number, light = 1) => {
    if (still) return;
    s.el.animate(
      [
        { transform: at(s, x, y), filter: `brightness(${light})` },
        {
          transform: at(s, x + 2, y - 5, 1, 6, 28),
          filter: `brightness(${light * 1.22})`,
          offset: 0.45,
        },
        {
          transform: at(s, x - 2, y + 2, 1, -4, -20),
          filter: `brightness(${light * 0.88})`,
          offset: 0.8,
        },
        { transform: at(s, x, y), filter: `brightness(${light})` },
      ],
      { duration: 6000 + Math.random() * 1400, iterations: Infinity, easing: "ease-in-out" },
    );
  };
  const later = (ms: number, fn: () => void) =>
    still ? fn() : timers.push(window.setTimeout(fn, ms));

  if (kind === "lights" || kind === "stores") {
    const cast = CAST[kind];
    const f = sprite(layer, cast.main, big);
    const end = { x: B.x, y: B.y - big * (kind === "lights" ? 1.1 : 0.9) };
    const dull = kind === "lights" ? "brightness(0.6) saturate(0.45)" : "brightness(1.2)";
    go(
      f,
      [
        { transform: at(f, A.x, A.y + 4, 0.3, -30, 70), opacity: 0, filter: dull },
        {
          transform: at(f, A.x, A.y - big * 0.8, 0.75, -12, 30),
          opacity: 1,
          offset: 0.2,
          filter: dull,
        },
        { transform: at(f, mx, top, 0.95, 10, -40), opacity: 1, offset: 0.55, filter: dull },
        kind === "lights"
          ? {
              transform: at(f, end.x, end.y, 1),
              opacity: 1,
              offset: 0.8,
              filter: "brightness(0.7) saturate(0.6)",
            }
          : {
              transform: at(f, end.x, end.y, 1),
              opacity: 1,
              offset: 1,
              filter: "brightness(1.15)",
            },
        ...(kind === "lights"
          ? [
              {
                transform: at(f, end.x, end.y - 4, 1.06, -3),
                opacity: 1,
                filter: "brightness(1.45) saturate(1.1)",
              },
            ]
          : []),
      ],
      { duration: kind === "lights" ? 3000 : 2600, easing: "ease-in-out" },
    );
    later(kind === "lights" ? 3000 : 2600, () => {
      if (kind === "lights") {
        hover(f, end.x, end.y - 4, 1.2);
        // Energy out: a few bright flecks lift off the lit leaf.
        const spots = [
          [-0.55, -0.75],
          [0.5, -1.0],
          [0.05, -1.4],
        ];
        cast.flecks.forEach((index, j) => {
          const s = sprite(layer, index, big * 0.34);
          const to = { x: end.x + spots[j][0] * big, y: end.y + spots[j][1] * big };
          go(
            s,
            [
              { transform: at(s, end.x, end.y, 0.4), opacity: 0, filter: "brightness(1.4)" },
              { transform: at(s, to.x, to.y, 1, 30, 40), opacity: 1, filter: "brightness(1.25)" },
            ],
            { duration: 1300, delay: j * 220, easing: "cubic-bezier(.2,.7,.3,1)" },
          );
          later(1300 + j * 220, () => hover(s, to.x, to.y, 1.2));
        });
        return;
      }
      // Kept in reserve: the flake breaks into flecks that settle on the heap's slopes.
      go(f, [{ opacity: 1 }, { opacity: 0, transform: at(f, end.x, end.y + 8, 0.5, 20, 60) }], {
        duration: 600,
      });
      const spots = [
        [-0.2, 0.42],
        [-0.06, 0.2],
        [0.1, 0.36],
        [0.24, 0.62],
        [-0.32, 0.7],
        [0.02, 0.6],
      ];
      const kept = cast.flecks.map((index, j) => {
        const s = sprite(layer, index, Math.max(8, big * 0.36));
        const to = { x: B.x + spots[j][0] * B.w, y: B.y + spots[j][1] * B.h };
        go(
          s,
          [
            { transform: at(s, end.x, end.y, 0.6), opacity: 0 },
            {
              transform: at(s, end.x + (to.x - end.x) * 0.5, end.y - 8, 1, 90, 120),
              opacity: 1,
              offset: 0.35,
            },
            { transform: at(s, to.x, to.y, 1, 160), opacity: 1 },
          ],
          { duration: 1500 + j * 150, delay: 150 + j * 90, easing: "cubic-bezier(.4,0,.6,1)" },
        );
        return { s, to };
      });
      // Ready fast: now and then one fleck jumps up, catches the light and drops back.
      const jump = (n: number) => {
        const { s, to } = kept[n % kept.length];
        s.el.animate(
          [
            { transform: at(s, to.x, to.y, 1, 160), filter: "brightness(1)" },
            {
              transform: at(s, to.x + 4, to.y - big * 1.1, 1.15, 200, 60),
              filter: "brightness(1.5)",
              offset: 0.3,
            },
            { transform: at(s, to.x, to.y, 1, 160), filter: "brightness(1)" },
          ],
          { duration: 1100, easing: "cubic-bezier(.2,.8,.4,1)" },
        );
        later(3200, () => jump(n + 2));
      };
      if (!still) later(2600, () => jump(1));
    });
  } else if (kind === "joins") {
    // Two halves of a messenger: half a leaf from each heap meets the other in the middle.
    const M = { x: mx, y: top + 16 };
    CAST.joins.halves.forEach((index, i) => {
      const s = sprite(layer, index, big * 0.55);
      const P = i ? B : A;
      const d = i ? 1 : -1;
      go(
        s,
        [
          { transform: at(s, P.x, P.y + 4, 0.3, 40 * d, 60), opacity: 0 },
          { transform: at(s, P.x, P.y - big * 0.8, 0.8, 20 * d, 20), opacity: 1, offset: 0.25 },
          { transform: at(s, M.x + big * 0.2 * d, M.y, 1), opacity: 1, offset: 0.9 },
          { transform: at(s, M.x + big * 0.2 * d, M.y, 1), opacity: 0 },
        ],
        { duration: 2700, easing: "ease-in-out" },
      );
    });
    const one = sprite(layer, CAST.joins.whole, big * 1.1);
    go(
      one,
      [
        { transform: at(one, M.x, M.y, 0.55, 0, 80), opacity: 0, filter: "brightness(1)" },
        { transform: at(one, M.x, M.y, 1.06), opacity: 1, offset: 0.5, filter: "brightness(1.45)" },
        { transform: at(one, M.x, M.y, 1), opacity: 1, filter: "brightness(1.1)" },
      ],
      { duration: 1100, delay: 2100, easing: "ease-out" },
    );
    later(3200, () => hover(one, M.x, M.y, 1.1));
  }
  return () => timers.forEach((timer) => window.clearTimeout(timer));
}

function Scene({
  link,
  names,
  motion,
  order,
}: {
  link: ProductSynergyLink;
  names: Record<string, string>;
  motion: boolean;
  order: number;
}) {
  const copy = useCopy();
  const stage = useRef<HTMLDivElement>(null);
  const layer = useRef<HTMLSpanElement>(null);
  const stop = useRef<() => void>(() => {});
  const run = useCallback(
    (still: boolean) => {
      const box = stage.current;
      const into = layer.current;
      const heaps = box ? [...box.querySelectorAll<HTMLElement>("[data-heap] img")] : [];
      if (!into || heaps.length !== 2) return;
      stop.current();
      stop.current = play(into, [heaps[0], heaps[1]], link.gold, still) ?? (() => {});
    },
    [link.gold],
  );

  // Plays as the scene comes into view (three across: one after another); still, the last frame.
  useEffect(() => {
    const box = stage.current;
    if (!box) return;
    let timer = 0;
    const seen = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        seen.disconnect();
        if (!motion) return run(true);
        const across = window.matchMedia("(min-width: 900px)").matches;
        timer = window.setTimeout(() => run(false), across ? order * 900 : 200);
      },
      { threshold: 0.6 },
    );
    seen.observe(box);
    return () => {
      seen.disconnect();
      window.clearTimeout(timer);
      stop.current();
    };
  }, [motion, order, run]);

  const pair = [link.from, link.to] as HeapKey[];
  return (
    <li className={styles.scene} data-scene={link.gold}>
      <div
        ref={stage}
        className={styles.stage}
        onClick={() => motion && run(false)}
        aria-hidden="true"
      >
        <span className={styles.duo}>
          {pair.map((key, i) => (
            <span key={key} className={styles.who} data-heap={key} style={{ order: i * 2 }}>
              <Image
                src={HEAPS[key].src}
                alt=""
                width={HEAPS[key].width}
                height={HEAPS[key].height}
                sizes="240px"
                style={{ width: `calc(${HEAPS[key].width}px * var(--heap))` }}
              />
              <span className={styles.whoName}>{copy(names[key] ?? key)}</span>
            </span>
          ))}
          <span className={styles.plus} style={{ order: 1 }}>
            +
          </span>
        </span>
        <span ref={layer} className={styles.layer} />
      </div>
      <p className={`${base.caption} ${styles.foot}`}>
        <span>{copy(CAPTIONS.illustration)}</span>
        {motion ? (
          <button type="button" className={styles.again} onClick={() => run(false)}>
            {copy("Play again")}
          </button>
        ) : null}
      </p>
      <p className={base.visuallyHidden}>
        {copy(names[link.from] ?? link.from)} + {copy(names[link.to] ?? link.to)}
      </p>
      <h4 className={styles.title}>{copy(link.title)}</h4>
      <p className={styles.line}>{copy(link.line)}</p>
      {link.evidence ? <p className={styles.evidence}>{copy(link.evidence)}</p> : null}
    </li>
  );
}

/** The pairs as scenes, then the note that says what the lines are (and are not). */
export function NuricellScenes({
  synergy,
  names,
  motion,
}: {
  synergy: ProductSynergy;
  names: Record<string, string>;
  motion: boolean;
}) {
  const copy = useCopy();
  return (
    <div className={styles.scenes} data-synergy="">
      <h3 className={styles.scenesTitle}>{copy(synergy.title)}</h3>
      <ul className={styles.sceneList}>
        {synergy.links.map((link, i) => (
          <Scene key={link.title} link={link} names={names} motion={motion} order={i} />
        ))}
      </ul>
      <p className={`${base.caption} ${styles.note}`}>{copy(synergy.note)}</p>
    </div>
  );
}
