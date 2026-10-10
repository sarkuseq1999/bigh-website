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
export const PICTURE_SIZES = "(max-width: 599px) 88vw, (max-width: 959px) 520px, 520px";

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
          sizes={PICTURE_SIZES}
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
