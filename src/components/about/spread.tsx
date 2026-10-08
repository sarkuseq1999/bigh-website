"use client";

import Image from "next/image";
import type { CSSProperties, ReactNode } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { drafts } from "./about-content";
import type { Art } from "./about-art";
import page from "./about-page.module.css";

// The About page's one rhythm (Mo, October 7, 2026: every part paired the same way): one picture,
// its words beside it, the sides swapping part by part. `side` is where the picture stands from
// 960px; on one column the picture always comes first. Paintings multiply onto the page's paper
// and bloom in as they arrive (the kit's useBloom). Every painting is marked "waiting" by the
// server: one marked later showed whole for a moment, vanished when the script marked it, then
// bloomed (the purpose painting at 1440x900). With no script the page's stylesheet shows them.

export function Painting({
  art,
  alt,
  sizes,
  caption = false,
  gold,
  delay = 0,
  preload = false,
  eager = false,
  waiting = true,
  className = "",
}: {
  art: Art;
  /** The painting's description (English source; translated through the catalogs), or "" when it only decorates. */
  alt: string;
  sizes: string;
  /** "Illustration" under a painting that pictures something (DESIGN.md honesty tags). */
  caption?: boolean;
  /** The painting's gold-leaf light mask (about-art.ts), for the kit's glint. */
  gold?: string;
  /** Milliseconds its bloom waits (the kit's --bloom-delay). */
  delay?: number;
  /** The first screen's main painting: Next's preload (a `<link rel="preload">` in the head),
      and fetchPriority="high" on that link and on the img. */
  preload?: boolean;
  /** A painting that reaches into the first screen on some windows: loading="eager", so it loads
      at once (lazy, it was the window's largest painting while the opening's still waited to
      bloom). Next adds no preload for it, but React's server render writes a
      `<link rel="preload" as="image">` for every img that is not lazy, this one included, without
      the high fetch priority the `preload` painting asks for. */
  eager?: boolean;
  /** Marked "waiting" by the server, so it never paints whole before its bloom (default true). */
  waiting?: boolean;
  className?: string;
}) {
  const copy = useCopy();
  return (
    <figure className={`${page.painting} ${className}`} data-picture="">
      <span className={page.paintingBody}>
        <Image
          className={base.ink}
          src={art.src}
          alt={alt ? copy(alt) : ""}
          width={art.width}
          height={art.height}
          sizes={sizes}
          preload={preload}
          fetchPriority={preload ? "high" : undefined}
          loading={eager && !preload ? "eager" : undefined}
          data-bloom={waiting ? "waiting" : ""}
          style={delay ? ({ "--bloom-delay": delay } as CSSProperties) : undefined}
        />
        {gold ? (
          <span className={base.gold} style={{ ["--gold" as string]: `url(${gold})` }} />
        ) : null}
      </span>
      {caption ? (
        <figcaption className={base.caption}>{copy(drafts.illustration)}</figcaption>
      ) : null}
    </figure>
  );
}

export function Spread({
  id,
  part,
  side,
  labelledBy,
  picture,
  children,
}: {
  id: string;
  /** The part's name, for its hooks and its page's styles. */
  part: string;
  /** Where the picture stands from 960px. */
  side: "left" | "right";
  labelledBy: string;
  /** A Painting, or a figure marked data-picture. */
  picture: ReactNode;
  children: ReactNode;
}) {
  return (
    <section id={id} className={page.part} data-part={part} aria-labelledby={labelledBy}>
      <div className={`${base.wrap} ${page.spread}`} data-side={side}>
        {picture}
        <div className={page.words} data-words="">
          {children}
        </div>
      </div>
    </section>
  );
}
