"use client";

import { useRef, type ReactNode } from "react";
import { useSmoothScroll } from "@/components/science/smooth-scroll";
import { useCopy } from "@/i18n/use-copy";
import { BrushLine } from "./brush";
import { SiteFooter, SiteHeader, type Current } from "./chrome";
import { ClosingCrane } from "./closing-crane";
import { useBloom, useInkFill, useMotionOk } from "./motion";
import type { NavFollow } from "./nav/nav-inscription";
import type { Layout, Waypoint } from "./route-kit";
import styles from "./ink.module.css";

// Any page in the Ink & Gold look (October 5, 2026): rice paper, the site header (clear over the
// opening, paper once scrolled), the page's sections, the footer that closes on the crane at
// rest, and, where the page has one, its own brush line drawing itself down the page. Paintings marked
// [data-bloom] bloom as they enter; outlined pills fill like ink in water. Reduced motion: a
// complete still page, with the whole line where the page has one. Keyboard: the first Tab shows
// "Skip to content".
// Render it inside <SiteDialogs> (and <ProductPagesProvider> where products link to pages).
export function InkPage({
  current,
  route,
  follow,
  className = "",
  children,
}: {
  current: Current;
  /**
   * The page's brush route for each layout. Pass a stable reference (a module-level function):
   * the brush layer is rebuilt whenever the route's identity changes. Leave it out for a page
   * without a brush line (About's folded letter: its folds divide the page).
   */
  route?: (layout: Layout) => Waypoint[];
  /**
   * The homepage only: its parts that belong to the menu bar's drop-downs (section ids), so the
   * word whose part is being read carries the painted stroke. Pass a stable (module-level) object.
   * Pages with a link of their own leave it out (their word carries the stroke).
   */
  follow?: NavFollow;
  /** A class for the page's root, for a page that dresses the shared paper (About ages it). */
  className?: string;
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
    <div
      ref={root}
      className={className ? `${styles.look} ${className}` : styles.look}
      data-look="ink"
      data-page={current}
    >
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
      <SiteHeader current={current} follow={follow} overlay solidAfter={48} settledBy={240} />
      <main ref={main} id="main" tabIndex={-1}>
        {children(motion)}
      </main>
      <SiteFooter closing={<ClosingCrane />} />
      {route ? <BrushLine motion={motion} route={route} /> : null}
    </div>
  );
}
