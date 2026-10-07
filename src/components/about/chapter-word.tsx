"use client";

import Image from "next/image";
import base from "@/components/ink/ink.module.css";
import { letters } from "./letter-art";
import styles from "./about-letter.module.css";

// A part's chapter word (October 6, 2026): its initial painted with the brush, the rest of the word
// in the page's type ("B" + "e"). Together they spell the brand's name, like the logo, so the word
// stays English in every language and is hidden from screen readers: the part's heading carries
// the meaning in the reader's language.
export function ChapterWord({
  initial,
  rest,
  size = "chapter",
  className = "",
}: {
  initial: keyof typeof letters;
  rest: string;
  /** "closing": the big H of Health, about the height of the written name. */
  size?: "chapter" | "closing";
  className?: string;
}) {
  const art = letters[initial];
  const dot = "dot" in art ? art.dot : null;
  return (
    <span
      className={`${styles.chapter} ${className}`}
      data-chapter={initial}
      data-size={size}
      lang="en"
      aria-hidden="true"
    >
      <span className={styles.initial}>
        <Image
          className={`${base.ink} ${styles.paint}`}
          src={art.src}
          alt=""
          width={art.width}
          height={art.height}
          sizes={
            size === "closing" ? "(max-width: 899px) 44vw, 300px" : "(max-width: 899px) 36vw, 240px"
          }
        />
        {dot ? (
          <Image
            className={styles.dot}
            src={dot.src}
            alt=""
            width={dot.width}
            height={dot.height}
            sizes="64px"
            data-dot=""
            style={{
              left: `${dot.left * 100}%`,
              top: `${dot.top * 100}%`,
              width: `${dot.size * 100}%`,
            }}
          />
        ) : null}
      </span>
      <span className={styles.rest}>{rest}</span>
    </span>
  );
}
