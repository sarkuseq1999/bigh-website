"use client";

import gsap from "gsap";
import { SplitText } from "gsap/SplitText";
import { useEffect, type RefObject } from "react";

// Shared pieces for Template 2, "Chapters": the chapter model (pure, in template-chapters-model.ts,
// re-exported here) and the calm arrivals every chapter uses.

export {
  anchorId,
  byYear,
  splitName,
  WORDS,
  type Chapter,
  type ChapterId,
  type Tone,
} from "./template-chapters-model";

/** SplitText line and word classes; their "-mask" wrappers get room for descenders in the CSS. */
export const lineClass = "tc-line";
export const wordClass = "tc-word";

/**
 * Calm arrivals for one chapter. [data-reveal] items rise and fade in; [data-heading] titles rise
 * line by line behind a mask (SplitText), then the split is undone so the text reflows normally.
 * Each runs once, the first time it comes into view (an IntersectionObserver, so late layout
 * changes such as a long 3D section above cannot leave anything hidden). Reduced motion: nothing
 * runs and the chapter is simply there.
 *
 * Every fade in this template uses opacity, never visibility (GSAP's autoAlpha): text waiting for
 * its moment stays in the accessibility tree, so screen readers can read ahead.
 */
export function useArrivals(root: RefObject<HTMLElement | null>, reduced: boolean) {
  useEffect(() => {
    const element = root.current;
    if (reduced || !element) return;
    gsap.registerPlugin(SplitText);
    let cancelled = false;
    let observer: IntersectionObserver | undefined;
    const ctx = gsap.context(() => {}, element);

    const start = () => {
      if (cancelled) return;
      const plays = new Map<Element, (delay: number) => void>();
      ctx.add(() => {
        gsap.utils.toArray<HTMLElement>("[data-reveal]", element).forEach((item) => {
          gsap.set(item, { opacity: 0, y: 26 });
          plays.set(item, (delay) =>
            ctx.add(() =>
              gsap.to(item, { opacity: 1, y: 0, duration: 1.1, delay, ease: "power3.out" }),
            ),
          );
        });
        gsap.utils.toArray<HTMLElement>("[data-heading]", element).forEach((heading) => {
          const split = SplitText.create(heading, {
            type: "lines",
            mask: "lines",
            linesClass: lineClass,
          });
          gsap.set(split.lines, { yPercent: 130 });
          plays.set(heading, (delay) =>
            ctx.add(() =>
              gsap.to(split.lines, {
                yPercent: 0,
                duration: 1.15,
                delay,
                ease: "expo.out",
                stagger: 0.1,
                onComplete: () => {
                  split.revert();
                },
              }),
            ),
          );
        });
      });
      observer = new IntersectionObserver(
        (entries) => {
          let order = 0;
          entries.forEach((entry) => {
            if (!entry.isIntersecting) return;
            observer?.unobserve(entry.target);
            plays.get(entry.target)?.(Math.min(order, 4) * 0.08);
            order += 1;
          });
        },
        { rootMargin: "0px 0px -8% 0px" },
      );
      plays.forEach((_, target) => observer?.observe(target));
    };

    // Split only once the fonts are in, so the line breaks are the real ones.
    void document.fonts.ready.then(start);
    return () => {
      cancelled = true;
      observer?.disconnect();
      ctx.revert();
    };
  }, [root, reduced]);
}
