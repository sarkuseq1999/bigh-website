"use client";

import { useRef, type ReactNode } from "react";
import { useSmoothScroll } from "@/components/science/smooth-scroll";
import { useCopy } from "@/i18n/use-copy";
import { BrushLine } from "./brush";
import { SiteFooter, SiteHeader, type Current } from "./chrome";
import { ClosingCrane } from "./closing-crane";
import { useBloom, useInkFill, useMotionOk } from "./motion";
import type { Layout, Waypoint } from "./route-kit";
import styles from "./ink.module.css";

// Any page in the Ink & Gold look (October 5, 2026): rice paper, the site header (clear over the
// opening, paper once scrolled), the page's sections, the footer that closes on the crane at
// rest, and the page's own brush line drawing itself down the page. Paintings marked
// [data-bloom] bloom as they enter; outlined pills fill like ink in water. Reduced motion: a
// complete still page with the whole line. Keyboard: the first Tab shows "Skip to content".
// Render it inside <SiteDialogs> (and <ProductPagesProvider> where products link to pages).
export function InkPage({
  current,
  route,
  children,
}: {
  current: Current;
  /**
   * The page's brush route for each layout. Pass a stable reference (a module-level function):
   * the brush layer is rebuilt whenever the route's identity changes.
   */
  route: (layout: Layout) => Waypoint[];
  /** The page's sections; given whether motion is allowed. */
  children: (motion: boolean) => ReactNode;
}) {
  const copy = useCopy();
  const root = useRef<HTMLDivElement>(null);
  const main = useRef<HTMLElement>(null);
  const motion = useMotionOk();
  useSmoothScroll(motion);
  useBloom(root, motion);
  useInkFill(root);

  return (
    <div ref={root} className={styles.look} data-look="ink" data-page={current}>
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
      <SiteHeader current={current} overlay solidAfter={48} />
      <main ref={main} id="main" tabIndex={-1}>
        {children(motion)}
      </main>
      <SiteFooter closing={<ClosingCrane />} />
      <BrushLine motion={motion} route={route} />
    </div>
  );
}
