"use client";

import { useRef } from "react";
import { useSmoothScroll } from "@/components/science/smooth-scroll";
import { useCopy } from "@/i18n/use-copy";
import { HomeFooter, HomeHeader } from "../chrome";
import { BrushLine } from "./brush";
import { Cellular } from "./cellular";
import { ClosingCrane } from "./closing-crane";
import { useBloom, useInkFill, useMotionOk } from "./motion";
import { OpeningCrane } from "./opening-crane";
import { Products } from "./products";
import { Purpose } from "./purpose";
import { Research } from "./research";
import { Science } from "./science";
import { Scientists } from "./scientists";
import { Stories } from "./stories";
import styles from "./look-ink.module.css";

// The parts of the page that belong to the bar's two drop-downs: while one is being read, its word
// in the bar carries the painted stroke (none over the opening, the scientists, the stories or the
// purpose).
const FOLLOW = { products: ["products"], science: ["cellular", "science", "research"] } as const;

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
      <HomeHeader overlay solidAfter={48} settledBy={240} follow={FOLLOW} />
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
      <BrushLine motion={motion} />
    </div>
  );
}
