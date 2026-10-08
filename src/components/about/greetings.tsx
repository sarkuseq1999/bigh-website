"use client";

import { useLocale } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { useCopy } from "@/i18n/use-copy";
import { drafts } from "./about-content";
import styles from "./greetings.module.css";

// "Answers in your language", shown: hello in the site's five languages. When it scrolls into
// view it plays through them once, one word at a time (each fades out before the next comes in;
// five changes a second apart, the last word in at 4.75s: under five seconds, so it needs no
// pause button) and settles on the visitor's own language. With reduced motion all five sit side
// by side. Screen readers hear the language list instead.
const LOCALE_TO_LANG: Record<string, string> = {
  en: "en",
  cns: "zh-Hans",
  hken: "zh-Hans",
  kr: "ko",
  vn: "vi",
  jp: "ja",
};
const STEP_MS = 1000;

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
    let timer = 0;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (!entry.isIntersecting) return;
        observer.disconnect();
        let next = 0;
        setStep(0);
        timer = window.setInterval(() => {
          next += 1;
          setStep(next);
          if (next >= order.length - 1) window.clearInterval(timer);
        }, STEP_MS);
      },
      { threshold: 0.8 },
    );
    observer.observe(element);
    return () => {
      observer.disconnect();
      window.clearInterval(timer);
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
