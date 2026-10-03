"use client";

import Image from "next/image";
import { useEffect, useRef } from "react";
import { ProductAction } from "@/components/home/product-action";
import { useCopy } from "@/i18n/use-copy";
import { hero } from "../content";
import { useHomeDialogs } from "../dialogs";
import { crane } from "./assets";
import base from "./look-ink.module.css";
import styles from "./opening.module.css";

// Opening 2, "the crane" (Mo's approved comp, October 2, 2026): a full-width ink landscape of
// misty mountains, the crane of long life in flight, a gold-leaf sun; the three-line headline at
// the lower left on calm paper, the intro and two pills under it. The brush line that leaves the
// crane is the page's own (brush.tsx).
export function OpeningCrane({ motion }: { motion: boolean }) {
  const copy = useCopy();
  const dialogs = useHomeDialogs();
  const art = useRef<HTMLDivElement>(null);

  // Depth as you leave the opening: the sun sinks slowly behind the ridges and the mountains
  // settle a little, while the crane (its own gentle float in CSS) stays on its flight path.
  useEffect(() => {
    const element = art.current;
    if (!element || !motion) return;
    let raf = 0;
    const update = () => {
      raf = 0;
      const y = Math.min(window.scrollY, window.innerHeight * 1.2);
      element.style.setProperty("--sink", `${(y * 0.16).toFixed(1)}px`);
      element.style.setProperty("--settle", `${(y * 0.05).toFixed(1)}px`);
    };
    const schedule = () => {
      if (!raf) raf = requestAnimationFrame(update);
    };
    update();
    window.addEventListener("scroll", schedule, { passive: true });
    return () => {
      cancelAnimationFrame(raf);
      window.removeEventListener("scroll", schedule);
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
        <Image
          className={styles.sun}
          src={crane.sun.src}
          alt=""
          width={crane.sun.width}
          height={crane.sun.height}
          sizes="(max-width: 720px) 34vw, 20vw"
          loading="eager"
          data-bloom="waiting"
        />
        <Image
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
          {hero.title.map((line) => (
            <span key={line}>{copy(line)}</span>
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
