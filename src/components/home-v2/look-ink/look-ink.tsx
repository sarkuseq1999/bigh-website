"use client";

import { useRef } from "react";
import { useSmoothScroll } from "@/components/science/smooth-scroll";
import { useCopy } from "@/i18n/use-copy";
import { HomeFooter, HomeHeader } from "@/components/ink/chrome";
import { BrushLine } from "@/components/ink/brush";
import { route } from "./brush-route";
import { Cellular } from "./cellular";
import { ClosingCrane } from "@/components/ink/closing-crane";
import { useBloom, useInkFill, useMotionOk } from "@/components/ink/motion";
import { OpeningCrane } from "./opening-crane";
import { Products } from "./products";
import { Purpose } from "./purpose";
import { Research } from "./research";
import { Science } from "./science";
import { Scientists } from "./scientists";
import { Stories } from "./stories";
import styles from "@/components/ink/ink.module.css";

// The homepage, "Ink & Gold" (round 4, October 2, 2026; Mo picked the crane): one ink-painting
// world on warm rice paper with a single gold leaf for energy. The crane of long life over misty
// mountains opens it. One continuous brush line draws itself down the page as you read
// (brush.tsx) and comes to rest as the stroke under the closing promise, where the crane stands
// at rest; each painting blooms
// into the paper as it enters; mist drifts through the opening's mountains and light crosses the
// gold leaf; every motion breathes at the same slow pace. Reduced motion: a complete still page
// with the whole brush line.
// Keyboard: the first Tab shows "Skip to content" (as on the About, Science and product pages),
// which puts focus at the start of the page's words, past the header's links.
export function LookInk() {
  const copy = useCopy();
  const root = useRef<HTMLDivElement>(null);
  const main = useRef<HTMLElement>(null);
  const motion = useMotionOk();
  useSmoothScroll(motion);
  useBloom(root, motion);
  useInkFill(root);

  return (
    <div ref={root} className={styles.look} data-look="ink">
      <a
        href="#main"
        className={styles.skip}
        onClick={(event) => {
          // Focus moves by hand: the page's smooth scrolling takes over links to #anchors.
          event.preventDefault();
          window.scrollTo(0, 0);
          main.current?.focus({ preventScroll: true });
        }}
      >
        {copy("Skip to content")}
      </a>
      <HomeHeader overlay solidAfter={48} />
      <main ref={main} id="main" tabIndex={-1}>
        <OpeningCrane motion={motion} />
        <Cellular />
        <Scientists />
        <Products />
        <Stories />
        <Science />
        <Research />
        <Purpose />
      </main>
      <HomeFooter closing={<ClosingCrane />} />
      <BrushLine motion={motion} route={route} />
    </div>
  );
}
