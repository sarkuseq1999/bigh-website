"use client";

import { useRef } from "react";
import { useSmoothScroll } from "@/components/science/smooth-scroll";
import { HomeFooter, HomeHeader } from "../chrome";
import { BrushLine } from "./brush";
import { Cellular } from "./cellular";
import { useBloom, useInkFill, useMotionOk } from "./motion";
import { OpeningCrane } from "./opening-crane";
import { Products } from "./products";
import { Purpose } from "./purpose";
import { Research } from "./research";
import { Science } from "./science";
import { Scientists } from "./scientists";
import { Stories } from "./stories";
import styles from "./look-ink.module.css";

// The homepage, "Ink & Gold" (round 4, October 2, 2026; Mo picked the crane): one ink-painting
// world on warm rice paper with a single gold leaf for energy. The crane of long life over misty
// mountains opens it. One continuous brush line draws itself down the page as you read
// (brush.tsx) and comes to rest as the stroke under the closing promise; each painting blooms
// into the paper as it enters; mist drifts through the opening's mountains and light crosses the
// gold leaf; every motion breathes at the same slow pace. Reduced motion: a complete still page
// with the whole brush line.
export function LookInk() {
  const root = useRef<HTMLDivElement>(null);
  const motion = useMotionOk();
  useSmoothScroll(motion);
  useBloom(root, motion);
  useInkFill(root);

  return (
    <div ref={root} className={styles.look} data-look="ink">
      <HomeHeader overlay solidAfter={48} />
      <main>
        <OpeningCrane motion={motion} />
        <Cellular />
        <Scientists />
        <Products />
        <Stories />
        <Science />
        <Research />
        <Purpose />
      </main>
      <HomeFooter />
      <BrushLine motion={motion} />
    </div>
  );
}
