"use client";

import Image from "next/image";
import type { CSSProperties, ReactNode, Ref } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkArt } from "../product-types";
import { anchorId, type ChapterId } from "../template-chapters-kit";
import styles from "./product-ink.module.css";

/** The honesty tags (DESIGN.md): "Illustration" (catalog m574) and Dr. Liu's "Portrait painting". */
export const CAPTIONS = { illustration: "Illustration", portrait: "Portrait painting" } as const;

/** Every chapter painting is drawn the same size: its column up to --picture-width (520px). */
const PICTURE_SIZES = "(max-width: 599px) 88vw, (max-width: 959px) 520px, 520px";

/**
 * The width a painting is drawn at, for its pictures' `sizes`. A tall one (the lantern, Dr. Liu)
 * is held by the window's height, not its column (product-ink.module.css: 46% of the window over
 * its words, the window less 220px beside them, times its width over its height), so asking for
 * 520px would fetch a picture two or three times too wide. Plain calc() with vh, which every
 * browser reads in `sizes` (the CSS's 220px floor matters only on a short landscape window). A
 * painting nearly as wide as it is tall (the breakfast, 0.94) is held by its column in most
 * windows, so it keeps the column's sizes.
 */
export function pictureSizes(art: { width: number; height: number }) {
  const aspect = art.width / art.height;
  if (aspect >= 0.8) return PICTURE_SIZES;
  const a = aspect.toFixed(3);
  return `(max-width: 959px) calc(46vh * ${a}), calc((100vh - 220px) * ${a})`;
}

/**
 * Keeps a short line's pieces together where a narrow column would split them: each hyphenated
 * word ("30-day", not "30-" / "day supply") and a "·" separator with the item after it (not
 * "90 vegetarian capsules ·" / "30-day supply"; the line may still break before the dot). The
 * words are unchanged: the space after the dot becomes a no-break space.
 */
export function keepTogether(text: string): ReactNode {
  const parts = text.replace(/ · /gu, " ·\u00a0").split(/(\S*\w-\w\S*)/u);
  if (parts.length === 1) return parts[0];
  return parts.map((part, i) =>
    i % 2 === 1 ? (
      <span key={i} className={styles.nowrap}>
        {part}
      </span>
    ) : (
      part
    ),
  );
}

export function titleId(id: ChapterId) {
  return `${anchorId(id)}-title`;
}

/** A heading's sentences, one line each (DESIGN's Set Lines Rule), split after . ! ? and the CJK
 *  stops, as About's opening does (about-ink.tsx). */
export function sentences(text: string) {
  return text.match(/[^.!?。！？]+[.!?。！？]*\s*/gu)?.map((part) => part.trim()) ?? [text];
}

/**
 * One painting as its own blend group: the figure multiplies onto the page's paper and its pictures
 * draw normally inside it, so the figure may be sticky, and a lit layer may cross-fade over an
 * unlit one, without a white box or a lighter flash. The painting blooms in (the kit's useBloom,
 * server-marked "waiting" so it never paints whole first); gold leaf takes the kit's glint. The
 * figure carries the painting's --aspect, so a tall one shrinks to fit the window with its caption.
 */
export function InkFigure({
  art,
  alt,
  caption = CAPTIONS.illustration,
  imgRef,
  attrs,
  eager = false,
  children,
}: {
  art: InkArt;
  /** English source of the painting's description (translated through the catalogs). */
  alt: string;
  caption?: string | null;
  imgRef?: Ref<HTMLImageElement>;
  attrs?: Record<string, string | undefined>;
  eager?: boolean;
  /** Layers drawn over the painting, inside its blend group (the lantern's light). */
  children?: ReactNode;
}) {
  const copy = useCopy();
  return (
    <figure
      className={styles.figure}
      style={{ ["--aspect" as string]: art.width / art.height } as CSSProperties}
      data-picture=""
      {...attrs}
    >
      <span className={styles.body}>
        <Image
          ref={imgRef}
          className={styles.art}
          src={art.src}
          alt={copy(alt)}
          width={art.width}
          height={art.height}
          sizes={pictureSizes(art)}
          loading={eager ? "eager" : undefined}
          data-bloom="waiting"
        />
        {art.gold ? (
          <span
            className={base.gold}
            style={{ ["--gold" as string]: `url(${art.gold})` } as CSSProperties}
          />
        ) : null}
        {children}
      </span>
      {caption ? (
        <figcaption className={`${base.caption} ${styles.caption}`}>{copy(caption)}</figcaption>
      ) : null}
    </figure>
  );
}

/** One chapter: its painting (left from 960px, first on phones) and its words. */
export function InkChapter({
  id,
  picture,
  children,
  className = "",
  labelledBy,
}: {
  id: ChapterId;
  picture: ReactNode;
  children: ReactNode;
  className?: string;
  /** The ids that name the chapter's region, when its heading alone is not a unique name (the
   *  buy chapter's heading is the product's name, which the opening's region already has). */
  labelledBy?: string;
}) {
  return (
    <section
      id={anchorId(id)}
      className={`${styles.chapter} ${className}`}
      data-chapter={id}
      aria-labelledby={labelledBy ?? titleId(id)}
    >
      <div className={`${base.wrap} ${styles.spread}`}>
        {picture}
        <div className={styles.words} data-words="">
          {children}
        </div>
      </div>
    </section>
  );
}
