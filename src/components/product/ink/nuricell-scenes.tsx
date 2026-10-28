"use client";

import Image from "next/image";
import { useCallback, useEffect, useRef, type CSSProperties } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { ProductSynergy, ProductSynergyLink } from "../product-types";
import { CAPTIONS } from "./ink-chapter";
import styles from "./nuricell-inside.module.css";
import { nuricellPairs } from "./nuricell-pairs";

// "Why these four work together" on NuriCell's ink page as three scenes from an old California ranch
// (Mo picked B, October 27, 2026; ideas reference/ink-pages/mockups/nuricell-pairs/). They replaced
// 1A's powder heaps, which read as drugs. Firewood and the stove (fuel in, energy out), the windmill
// filling its tank (energy kept on hand), the Pony Express rider and his horse carrying a letter (two
// halves of a messenger); gold marks the energy. Each scene plays as it comes into view (three across:
// one after another), and again on "Play again": the stove's gold fire catches the light; the
// windmill's wheel turns once, its water pours and light spreads across the tank; the rider's gold
// letter catches the light. The motion is CSS (nuricell-inside.module.css), started by data-play on
// the stage ("wait" until its turn, then "on"). Reduced motion and no script: the paintings, still.

type Box = readonly [number, number, number, number];

/** The paintings fill their card: the whole width on phones, a third of the row from 900px. */
const SIZES = "(max-width: 899px) 92vw, 400px";

const pct = (n: number) => `${+(n * 100).toFixed(3)}%`;

/** A box of the painting, as left, top, width and height. */
const placed = ([l, t, w, h]: Box): CSSProperties => ({
  left: pct(l),
  top: pct(t),
  width: pct(w),
  height: pct(h),
});

/** The scene's gold cut to a box of the painting: masks and clips act on the box, and the gold lies
 *  in it exactly where it is painted. */
function Gold({
  src,
  box,
  className,
  style,
}: {
  src: { src: string; width: number; height: number };
  box: Box;
  className: string;
  style?: CSSProperties;
}) {
  const [l, t, w, h] = box;
  return (
    <span className={`${styles.cut} ${className}`} style={{ ...placed(box), ...style }}>
      <Image
        src={src.src}
        alt=""
        width={src.width}
        height={src.height}
        sizes={SIZES}
        style={{ left: pct(-l / w), top: pct(-t / h), width: pct(1 / w) }}
      />
    </span>
  );
}

function Picture({ kind }: { kind: keyof typeof nuricellPairs }) {
  const art = nuricellPairs[kind];
  const { still, gold, glint } = art;
  return (
    <>
      <Image
        className={styles.still}
        src={still.src}
        alt=""
        width={still.width}
        height={still.height}
        sizes={SIZES}
      />
      {"fan" in art ? (
        <Image
          className={styles.fan}
          src={art.fan.src}
          alt=""
          width={art.fan.width}
          height={art.fan.height}
          sizes="(max-width: 899px) 22vw, 96px"
          style={{
            ...placed(art.fan.box),
            height: "auto",
            transformOrigin: `${pct(art.fan.hub[0])} ${pct(art.fan.hub[1])}`,
          }}
        />
      ) : null}
      {"stream" in art ? <Gold src={gold} box={art.stream} className={styles.stream} /> : null}
      <Gold
        src={gold}
        box={glint}
        className={styles.glint}
        style={
          "foot" in art
            ? ({ "--fx": pct(art.foot[0]), "--fy": pct(art.foot[1]) } as CSSProperties)
            : undefined
        }
      />
    </>
  );
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
  // From the start: the attribute off, a reflow, then on again, so the CSS animations restart.
  const play = useCallback(() => {
    const box = stage.current;
    if (!box) return;
    box.removeAttribute("data-play");
    void box.offsetWidth;
    box.setAttribute("data-play", "on");
  }, []);

  // Plays as the scene comes into view (three across: one after another); until then it waits. If
  // motion turns off (reduced motion is read after the first render), the painting shows still.
  useEffect(() => {
    const box = stage.current;
    if (!box || !motion) return;
    box.setAttribute("data-play", "wait");
    let timer = 0;
    const seen = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        seen.disconnect();
        const across = window.matchMedia("(min-width: 900px)").matches;
        timer = window.setTimeout(play, across ? order * 900 : 200);
      },
      { threshold: 0.6 },
    );
    seen.observe(box);
    return () => {
      seen.disconnect();
      window.clearTimeout(timer);
      box.removeAttribute("data-play");
    };
  }, [motion, order, play]);

  return (
    <li className={styles.scene} data-scene={link.gold}>
      <div
        ref={stage}
        className={styles.stage}
        onClick={motion ? play : undefined}
        aria-hidden="true"
      >
        {link.gold ? <Picture kind={link.gold} /> : null}
      </div>
      <p className={`${base.caption} ${styles.foot}`}>
        <span>{copy(CAPTIONS.illustration)}</span>
        {motion ? (
          <button type="button" className={styles.again} onClick={play}>
            {copy("Play again")}
          </button>
        ) : null}
      </p>
      <p className={styles.pair}>
        {copy(names[link.from] ?? link.from)} <span aria-hidden="true">+</span>{" "}
        {copy(names[link.to] ?? link.to)}
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
