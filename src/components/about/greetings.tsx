"use client";

import { useLocale } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { useCopy } from "@/i18n/use-copy";
import { drafts } from "./about-content";
import styles from "./greetings.module.css";

// "Answers in your language", shown: hello in the site's five languages. When it scrolls into
// view it plays through them once, one word at a time, slowly enough to read: each word stays
// wholly in for 1.4s, fades out (0.35s), a short beat, and the next fades in (0.35s); never two at
// once. It ends on the visitor's own language and rests there (the play lasts about nine seconds
// from the moment it is seen). With reduced motion all five sit side by side, still; with no
// script the visitor's own word stands alone. Screen readers hear the language list instead.
const LOCALE_TO_LANG: Record<string, string> = {
  en: "en",
  cns: "zh-Hans",
  hken: "zh-Hans",
  kr: "ko",
  vn: "vi",
  jp: "ja",
};
// Out 0.35s, a beat of 0.15s, in 0.35s (greetings.module.css): a word is wholly in 850ms after
// it is called; then it holds.
const IN_MS = 850;
const HOLD_MS = 1400;
const STEP_MS = IN_MS + HOLD_MS;

export function Greetings({ className = "" }: { className?: string }) {
  const copy = useCopy();
  const locale = useLocale();
  const own = Math.max(
    0,
    drafts.greetings.findIndex((greeting) => greeting.lang === (LOCALE_TO_LANG[locale] ?? "en")),
  );
  // The rest first, the visitor's own language last.
  const order = [...drafts.greetings.keys()].filter((i) => i !== own).concat(own);
  const root = useRef<HTMLSpanElement>(null);
  const [step, setStep] = useState(order.length - 1);

  useEffect(() => {
    const element = root.current;
    if (!element || window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
    // Before it is seen, the first of the other words takes the stage (unseen, off screen), so the
    // play opens on a word already in, not on the visitor's own word leaving as they arrive.
    const first = window.setTimeout(() => setStep(0), 0);
    const ready = performance.now() + IN_MS;
    let timer = 0;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        observer.disconnect();
        let next = 0;
        const advance = () => {
          next += 1;
          setStep(next);
          if (next < order.length - 1) timer = window.setTimeout(advance, STEP_MS);
        };
        // The first word holds its full 1.4s from the moment it is wholly in (or is seen).
        timer = window.setTimeout(advance, Math.max(0, ready - performance.now()) + HOLD_MS);
      },
      { threshold: 0.8 },
    );
    observer.observe(element);
    return () => {
      observer.disconnect();
      window.clearTimeout(first);
      window.clearTimeout(timer);
    };
  }, [order.length]);

  const shown = order[step];
  return (
    <span ref={root} className={`${styles.greetings} ${className}`}>
      <span className={styles.sr}>{copy(drafts.languages)}</span>
      <span className={styles.stage} aria-hidden="true">
        {drafts.greetings.map((greeting, i) => (
          <span
            key={greeting.lang}
            lang={greeting.lang}
            className={styles.word}
            data-state={i === shown ? "in" : "out"}
          >
            {greeting.text}
          </span>
        ))}
      </span>
    </span>
  );
}
