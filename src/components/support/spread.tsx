"use client";

import Image from "next/image";
import type { CSSProperties, ReactNode } from "react";
import base from "@/components/ink/ink.module.css";
import type { Art, Steam } from "./support-art";
import page from "./support-page.module.css";

// The Support page's one rhythm (as About's, kept here so the live About page is untouched): one
// painting, its words beside it, the sides taking turns from 960px; on one column the painting
// comes first. Paintings multiply onto the page's paper and bloom in as they arrive (the kit's
// useBloom); the server marks them "waiting" so none paints whole first.

export function Painting({
  art,
  alt,
  sizes,
  eager = false,
  preload = false,
  steam,
  className = "",
}: {
  art: Art;
  alt: string;
  sizes: string;
  /** Reaches into the first screen on some windows: loading="eager". */
  eager?: boolean;
  /** The first screen's main painting: Next's preload and fetchPriority="high". */
  preload?: boolean;
  /** The gold steam over this painting (support-art.ts), which rises after the bloom. */
  steam?: Steam;
  className?: string;
}) {
  return (
    <figure className={`${page.painting} ${className}`} data-picture="">
      <span className={page.paintingBody}>
        <Image
          className={base.ink}
          src={art.src}
          alt={alt}
          width={art.width}
          height={art.height}
          sizes={sizes}
          preload={preload}
          fetchPriority={preload ? "high" : undefined}
          loading={eager && !preload ? "eager" : undefined}
          data-bloom="waiting"
        />
        {steam ? (
          <Image
            className={page.steam}
            src={steam.src}
            alt=""
            width={steam.width}
            height={steam.height}
            sizes="200px"
            loading="eager"
            data-steam=""
            style={
              {
                left: `${(steam.left * 100).toFixed(2)}%`,
                top: `${(steam.top * 100).toFixed(2)}%`,
                width: `${(steam.size * 100).toFixed(2)}%`,
              } as CSSProperties
            }
          />
        ) : null}
      </span>
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
  part: string;
  /** Where the painting stands from 960px. */
  side: "left" | "right";
  labelledBy: string;
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
