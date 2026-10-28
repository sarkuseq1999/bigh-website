"use client";

import Image from "next/image";
import { useEffect, useRef, type ReactNode } from "react";
import { ProductAction } from "@/components/home/product-action";
import { useCopy } from "@/i18n/use-copy";
import { hero } from "../content";
import { useSiteDialogs } from "@/components/ink/dialogs";
import { opening } from "./assets";
import { useInkColor } from "./ink-color";
import { useMist } from "./mist";
import base from "@/components/ink/ink.module.css";
import styles from "./opening.module.css";

// The opening, laid out on the crane comp (Mo's approved comp, October 2, 2026): a painting across
// the first screen, a bird in flight, a gold-leaf sun; the three-line headline at the lower left
// on calm paper, the intro and two pills under it. The brush line that leaves the bird is the
// page's own (brush.tsx). October 28, 2026 (Mo): the misty peaks and the red-crowned crane read as
// Chinese, so the painting is now giant sequoias in the morning (they live 3,000 years), the sun
// standing in a clearing beside one giant trunk, and the bird Anna's hummingbird (for its size it
// burns energy faster than almost any animal). The crane's place, anchors and float are the
// bird's. The painting is alive: mist drifts through the grove (mist.ts), light crosses the gold
// leaf, the sun sits at its own depth, and the bird rides the air in a slow float of its own
// (opening.module.css).

// The headline's one gold word (Mo, October 13, 2026: colour for an ink-and-paper page): "cells" in
// each language, wherever its line puts it (Korean and Japanese on the second line). Only the first
// match is gilded.
const GOLD_WORDS = ["cells.", "세포", "細胞", "细胞", "tế bào"];

function gild(lines: string[], className: string): ReactNode[] {
  let done = false;
  return lines.map((text) => {
    if (done) return text;
    const word = GOLD_WORDS.find((candidate) => text.includes(candidate));
    if (!word) return text;
    done = true;
    const at = text.indexOf(word);
    return (
      <>
        {text.slice(0, at)}
        <span className={className}>{word}</span>
        {text.slice(at + word.length)}
      </>
    );
  });
}

export function OpeningCrane({ motion }: { motion: boolean }) {
  const color = useInkColor();
  const copy = useCopy();
  const dialogs = useSiteDialogs();
  const art = useRef<HTMLDivElement>(null);
  const landscape = useRef<HTMLImageElement>(null);
  const mist = useRef<HTMLCanvasElement>(null);
  useMist(art, landscape, mist, motion);

  // Depth as you leave the opening: the sun sinks slowly behind the trees and the grove settles
  // a little, while the bird (its own gentle float in CSS) stays on its flight path. With a
  // mouse, the sun also leans a few pixels against the pointer, as far things do when you move
  // your head. (The bird stays put: the brush line is pinned to its tail.)
  useEffect(() => {
    const element = art.current;
    if (!element || !motion) return;
    let raf = 0;
    let lean = { x: 0, y: 0 };
    let goal = { x: 0, y: 0 };
    const update = () => {
      raf = 0;
      const y = Math.min(window.scrollY, window.innerHeight * 1.2);
      element.style.setProperty("--sink", `${(y * 0.16).toFixed(1)}px`);
      element.style.setProperty("--settle", `${(y * 0.05).toFixed(1)}px`);
      lean = { x: lean.x + (goal.x - lean.x) * 0.06, y: lean.y + (goal.y - lean.y) * 0.06 };
      element.style.setProperty("--lean-x", lean.x.toFixed(4));
      element.style.setProperty("--lean-y", lean.y.toFixed(4));
      if (Math.abs(goal.x - lean.x) + Math.abs(goal.y - lean.y) > 0.002) schedule();
    };
    const schedule = () => {
      if (!raf) raf = requestAnimationFrame(update);
    };
    const onPointer = (event: PointerEvent) => {
      if (event.pointerType !== "mouse" || window.scrollY > window.innerHeight) return;
      goal = {
        x: (event.clientX / window.innerWidth) * 2 - 1,
        y: (event.clientY / window.innerHeight) * 2 - 1,
      };
      schedule();
    };
    update();
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("pointermove", onPointer, { passive: true });
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("scroll", schedule);
      window.removeEventListener("pointermove", onPointer);
    };
  }, [motion]);

  return (
    <section
      id="top"
      className={styles.opening}
      aria-labelledby="opening-title"
      data-brush="opening"
    >
      <div ref={art} className={styles.art} aria-hidden="true" data-brush="opening-art">
        {/* What the brush line measures the opening's stroke on (see opening.module.css). */}
        <span className={styles.stage} data-brush="opening-stage" />
        <span className={styles.flightPath} data-brush="opening-flight" />
        {/* The painting's own box (it covers the opening), so the line can walk its forest floor. */}
        <span className={styles.land} data-brush="opening-land" />
        <span className={styles.sun}>
          <Image
            className={styles.leaf}
            src={opening.sun.src}
            alt=""
            width={opening.sun.width}
            height={opening.sun.height}
            sizes="(max-width: 720px) 34vw, 20vw"
            loading="eager"
            data-bloom="waiting"
          />
          {/* Light crossing the gold leaf, inside the leaf's own torn edge. */}
          <span className={styles.glint} />
          {/* Green spring: a warm haze around the sun, behind the hills. */}
          {color === "spring" && <span className={styles.glow} />}
        </span>
        <Image
          ref={landscape}
          className={`${base.ink} ${styles.landscape}`}
          src={opening.landscape.src}
          alt=""
          width={opening.landscape.width}
          height={opening.landscape.height}
          sizes="(max-width: 720px) 150vw, 100vw"
          loading="eager"
          fetchPriority="high"
          data-bloom="waiting"
          style={{ ["--bloom-delay" as string]: 200, ["--bloom-origin" as string]: "72% 60%" }}
        />
        <canvas ref={mist} className={`${base.ink} ${styles.landscape} ${styles.mist}`} />
        <span className={styles.crane} data-brush="crane">
          <Image
            className={styles.bird}
            src={opening.bird.src}
            alt=""
            width={opening.bird.width}
            height={opening.bird.height}
            sizes="(max-width: 720px) 64vw, 23vw"
            loading="eager"
            data-bloom="waiting"
            style={{ ["--bloom-delay" as string]: 600 }}
          />
        </span>
      </div>

      <div className={styles.copy}>
        <h1 id="opening-title" className={styles.title}>
          {gild(
            hero.title.map((line) => copy(line)),
            styles.gold,
          ).map((line, i) => (
            <span key={hero.title[i]} style={{ ["--i" as string]: i }}>
              {line}
            </span>
          ))}
        </h1>
        <p className={styles.intro}>{copy(hero.text)}</p>
        <div className={styles.actions}>
          <ProductAction
            name="NuriCell"
            onOpen={() => dialogs.openProduct(0)}
            className={base.pill}
          >
            {copy(hero.primary)}
          </ProductAction>
          <a href="#scientists" className={`${base.pill} ${base.pillGhost}`}>
            {copy(hero.secondary)}
          </a>
        </div>
      </div>
    </section>
  );
}
