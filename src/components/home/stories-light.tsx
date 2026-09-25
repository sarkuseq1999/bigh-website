"use client";

import Image from "next/image";
import { ArrowDown, ArrowUpRight } from "lucide-react";
import { useLocale } from "next-intl";
import { useEffect, useRef, type CSSProperties } from "react";
import { useCopy } from "@/i18n/use-copy";
import { stories, type StoriesDesignProps } from "./stories-data";
import styles from "./stories-light.module.css";
import { useReducedMotion } from "./use-reduced-motion";

const segmenterLocale: Record<string, string> = {
  en: "en",
  kr: "ko",
  jp: "ja",
  cns: "zh-Hans",
  hken: "zh-Hant",
  vn: "vi",
};

type Piece = { text: string; index: number };

// Word pieces for the light-up effect. Intl.Segmenter handles Chinese and Japanese, which have no spaces.
function splitWords(text: string, locale: string, offset: number) {
  const pieces: Piece[] = [];
  let count = 0;
  const add = (segment: string, wordLike: boolean) => {
    if (wordLike) count += 1;
    pieces.push({ text: segment, index: offset + Math.max(0, count - 1) });
  };
  if (typeof Intl.Segmenter === "function") {
    const segmenter = new Intl.Segmenter(segmenterLocale[locale] ?? "en", { granularity: "word" });
    for (const part of segmenter.segment(text)) add(part.segment, Boolean(part.isWordLike));
  } else {
    for (const part of text.split(/(\s+)/)) add(part, part.trim().length > 0);
  }
  return { pieces, count };
}

function Words({ pieces }: { pieces: Piece[] }) {
  return pieces.map((piece, key) => (
    <span key={key} className={styles.w} style={{ "--i": piece.index } as CSSProperties}>
      {piece.text}
    </span>
  ));
}

// Design 3 — each story lights up word by word as the visitor scrolls, and its scene brightens with it.
export function StoriesLight({ onOpenProduct }: StoriesDesignProps) {
  const copy = useCopy();
  const locale = useLocale();
  // Plain, fully lit text is the default; the scroll effect switches on only when motion is welcome.
  const live = !useReducedMotion();
  const chapters = useRef<(HTMLElement | null)[]>([]);

  const texts = stories.map((story) => {
    const title = splitWords(copy(story.title), locale, 0);
    const quote = splitWords(copy(story.quote), locale, title.count);
    return { title: title.pieces, quote: quote.pieces, total: title.count + quote.count };
  });

  useEffect(() => {
    if (!live) return;
    let frame = 0;
    const update = () => {
      frame = 0;
      const height = window.innerHeight;
      chapters.current.forEach((chapter) => {
        if (!chapter) return;
        const total = Number(chapter.style.getPropertyValue("--i-end")) || 0;
        const pin = chapter.firstElementChild as HTMLElement | null;
        if (!pin) return;
        const bounds = chapter.getBoundingClientRect();
        const pinStyle = getComputedStyle(pin);
        let progress: number;
        if (pinStyle.position === "sticky") {
          const travel = bounds.height - pin.offsetHeight;
          progress = travel > 0 ? ((parseFloat(pinStyle.top) || 0) - bounds.top) / travel : 1;
        } else {
          progress = (height * 0.8 - bounds.top) / (bounds.height + height * 0.05);
        }
        progress = Math.min(1, Math.max(0, progress));
        const lit = Math.min(1, progress / 0.8) * (total + 2.5);
        chapter.style.setProperty("--lit", lit.toFixed(2));
        chapter.style.setProperty("--reveal", Math.min(1, progress / 0.55).toFixed(3));
      });
    };
    const schedule = () => {
      if (!frame) frame = requestAnimationFrame(update);
    };
    update();
    window.addEventListener("scroll", schedule, { passive: true });
    window.addEventListener("resize", schedule);
    return () => {
      window.removeEventListener("scroll", schedule);
      window.removeEventListener("resize", schedule);
      cancelAnimationFrame(frame);
    };
  }, [live]);

  return (
    <div className={styles.light} data-live={live || undefined}>
      <header className={styles.head}>
        <h2 id="stories-title">{copy("In their own words.")}</h2>
        <p>{copy("The routines, questions, and choices behind everyday wellbeing.")}</p>
        <p className={styles.note}>
          {copy("Design draft — all testimonials and reviewer names below are fictional samples.")}
        </p>
        <p className={styles.hint}>
          <ArrowDown size={18} aria-hidden="true" />
          {copy("Scroll to read each story")}
        </p>
      </header>

      {stories.map((story, index) => (
        <article
          key={story.id}
          ref={(element) => {
            chapters.current[index] = element;
          }}
          className={styles.chapter}
          style={{ "--i-end": texts[index].total } as CSSProperties}
          aria-label={copy("Sample story {number} of {count}: {name}", {
            number: index + 1,
            count: stories.length,
            name: story.name,
          })}
        >
          <div className={styles.pin}>
            <figure className={styles.visual}>
              <span className={styles.glow} aria-hidden="true" />
              <span className={styles.window}>
                <Image src={story.still} fill sizes="(max-width: 899px) 78vw, 36vw" alt="" />
              </span>
              <figcaption>{copy("Illustrative scene")}</figcaption>
            </figure>
            <div className={styles.copy}>
              <blockquote>
                <p className={styles.title}>
                  {live ? <Words pieces={texts[index].title} /> : copy(story.title)}
                </p>
                <p className={styles.quote}>
                  {live ? <Words pieces={texts[index].quote} /> : copy(story.quote)}
                </p>
              </blockquote>
              <p className={styles.byline}>
                <span>{story.name}</span>
                <span className={styles.tag}>{copy("Fictional sample")}</span>
              </p>
              <button
                type="button"
                className={styles.cta}
                onClick={() => onOpenProduct(story.productIndex)}
              >
                <span className={styles.bottle}>
                  <Image src={story.productImage} width={96} height={96} sizes="48px" alt="" />
                </span>
                <span>{copy("Discover {name}", { name: story.product })}</span>
                <ArrowUpRight size={19} aria-hidden="true" />
              </button>
            </div>
          </div>
        </article>
      ))}
    </div>
  );
}
