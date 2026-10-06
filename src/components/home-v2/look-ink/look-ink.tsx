"use client";

import { InkPage } from "@/components/ink/ink-page";
import type { NavFollow } from "@/components/ink/nav/nav-inscription";
import { route } from "./brush-route";
import { Cellular } from "./cellular";
import { OpeningCrane } from "./opening-crane";
import { Products } from "./products";
import { Purpose } from "./purpose";
import { Research } from "./research";
import { Science } from "./science";
import { Scientists } from "./scientists";
import { Stories } from "./stories";

// The parts of the page that belong to the bar's two drop-downs: while one is being read, its word
// in the bar carries the painted stroke (none over the opening, the scientists, the stories or the
// purpose). A module-level constant: the bar watches the parts again whenever its identity changes.
const FOLLOW: NavFollow = { products: ["products"], science: ["cellular", "science", "research"] };

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
  return (
    <InkPage current="home" route={route} follow={FOLLOW}>
      {(motion) => (
        <>
          <OpeningCrane motion={motion} />
          <Cellular />
          <Scientists />
          <Products />
          <Stories />
          <Science />
          <Research />
          <Purpose />
        </>
      )}
    </InkPage>
  );
}
