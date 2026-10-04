"use client";

import Image from "next/image";
import { useEffect, useRef } from "react";
import { ProductAction } from "@/components/home/product-action";
import { useCopy } from "@/i18n/use-copy";
import { hero } from "../content";
import { useHomeDialogs } from "../dialogs";
import { crane } from "./assets";
import { useMist } from "./mist";
import base from "./look-ink.module.css";
import styles from "./opening.module.css";

// Opening 2, "the crane" (Mo's approved comp, October 2, 2026): a full-width ink landscape of
// misty mountains, the crane of long life in flight, a gold-leaf sun; the three-line headline at
// the lower left on calm paper, the intro and two pills under it. The brush line that leaves the
// crane is the page's own (brush.tsx). The painting is alive: mist drifts through the mountains
// (mist.ts), light crosses the gold leaf, and the crane and the sun sit at their own depths.
export function OpeningCrane({ motion }: { motion: boolean }) {
  const copy = useCopy();
  const dialogs = useHomeDialogs();
  const art = useRef<HTMLDivElement>(null);
  const landscape = useRef<HTMLImageElement>(null);
  const mist = useRef<HTMLCanvasElement>(null);
  useMist(art, landscape, mist, motion);

  // Depth as you leave the opening: the sun sinks slowly behind the ridges and the mountains
  // settle a little, while the crane (its own gentle float in CSS) stays on its flight path.
  // With a mouse, the sun also leans a few pixels against the pointer, as far things do when you
  // move your head. (The crane stays put: the brush line is pinned to its trailing legs.)
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
        <span className={styles.sun}>
          <Image
            className={styles.leaf}
            src={crane.sun.src}
            alt=""
            width={crane.sun.width}
            height={crane.sun.height}
            sizes="(max-width: 720px) 34vw, 20vw"
            loading="eager"
            data-bloom="waiting"
          />
          {/* Light crossing the gold leaf, inside the leaf's own torn edge. */}
          <span className={styles.glint} />
        </span>
        <Image
          ref={landscape}
          className={`${base.ink} ${styles.landscape}`}
          src={crane.landscape.src}
          alt=""
          width={crane.landscape.width}
          height={crane.landscape.height}
          sizes="100vw"
          loading="eager"
          fetchPriority="high"
          data-bloom="waiting"
          style={{ ["--bloom-delay" as string]: 200, ["--bloom-origin" as string]: "72% 60%" }}
        />
        <canvas ref={mist} className={`${base.ink} ${styles.landscape} ${styles.mist}`} />
        <Image
          className={styles.crane}
          src={crane.crane.src}
          alt=""
          width={crane.crane.width}
          height={crane.crane.height}
          sizes="(max-width: 720px) 70vw, 40vw"
          loading="eager"
          data-brush="crane"
          data-bloom="waiting"
          style={{ ["--bloom-delay" as string]: 600 }}
        />
      </div>

      <div className={styles.copy}>
        <h1 id="opening-title" className={styles.title}>
          {hero.title.map((line, i) => (
            <span key={line} style={{ ["--i" as string]: i }}>
              {copy(line)}
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
