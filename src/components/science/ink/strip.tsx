"use client";

import { getImageProps } from "next/image";
import type { CSSProperties, ReactNode } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import { ink } from "../science-content";
import styles from "./strip.module.css";

type Pic = { readonly src: string; readonly width: number; readonly height: number };

/**
 * One part below Dr. Liu: the header row, one wide painting (its phone crop under 960px, or no
 * painting under 960px at all with `wideOnly`, where the part shows its own scenes), then `children`.
 * The painting multiplies onto the page's paper (the kit's .ink) and blooms in as it arrives. The
 * server marks it "waiting" (the page's stylesheet shows it whole where no bloom will come).
 */
export function Strip({
  id,
  label,
  title,
  lead,
  art,
  phone,
  alt,
  wideOnly = false,
  children,
}: {
  id: string;
  label: string;
  title: string;
  lead: string;
  art: Pic;
  phone?: Pic;
  alt: string;
  wideOnly?: boolean;
  children: ReactNode;
}) {
  const copy = useCopy();
  const common = { alt: copy(alt), sizes: "(max-width: 959px) 92vw, 1176px" };
  const wide = getImageProps({ ...common, src: art.src, width: art.width, height: art.height });
  const narrow = phone
    ? getImageProps({ ...common, src: phone.src, width: phone.width, height: phone.height })
    : null;
  // The painting's box comes from the stylesheet (strip.module.css, .art), whichever picture loads.
  const ratios = {
    "--ar-wide": `${art.width} / ${art.height}`,
    ...(phone ? { "--ar-narrow": `${phone.width} / ${phone.height}` } : {}),
  } as CSSProperties;
  return (
    <section id={id} className={styles.strip} aria-labelledby={`${id}-title`}>
      <div className={base.wrap}>
        <header className={styles.head}>
          <div>
            <p className={base.caption}>{copy(label)}</p>
            <h2 id={`${id}-title`} className={styles.title}>
              {copy(title)}
            </h2>
          </div>
          <p className={base.body}>{copy(lead)}</p>
        </header>
        <figure
          className={styles.figure}
          style={ratios}
          data-picture=""
          data-wide-only={wideOnly ? "" : undefined}
        >
          <picture>
            {narrow ? (
              <source
                media="(max-width: 959px)"
                srcSet={narrow.props.srcSet}
                sizes={common.sizes}
              />
            ) : null}
            {/* A plain img inside a picture: art direction through getImageProps (the phone crop). */}
            <img
              {...wide.props}
              alt={common.alt}
              className={`${base.ink} ${styles.art}`}
              loading="lazy"
              data-bloom="waiting"
            />
          </picture>
          <figcaption className={base.caption}>{copy(ink.illustration)}</figcaption>
        </figure>
        {children}
      </div>
    </section>
  );
}
