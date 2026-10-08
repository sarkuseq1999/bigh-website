"use client";

import { useLocale } from "next-intl";
import { Fragment, useRef, type CSSProperties } from "react";
import { useArrival, useMotionOk } from "@/components/ink/motion";
import { useCopy } from "@/i18n/use-copy";
import { drafts } from "./about-content";
import styles from "./greetings.module.css";

// "Answers in your language", shown: hello in the site's five languages, all together on one calm
// line (balanced over two where it is narrow), the visitor's own language last and in the darker
// ink. When it first comes into view the words arrive one by one (greetings.module.css: 180ms
// apart, a soft fade and a few pixels of rise; over in about 1.4s) and nothing moves after that (a
// word cycle that ran nine seconds would have needed a pause control). The kit's useArrival keeps
// the finished line as the default: with reduced motion, with no script, or when the line is
// already in view as the page opens, all five simply stand there. Screen readers hear the language
// list instead.
const LOCALE_TO_LANG: Record<string, string> = {
  en: "en",
  cns: "zh-Hans",
  hken: "zh-Hans",
  kr: "ko",
  vn: "vi",
  jp: "ja",
};
// When the arrival is over: the last word's delay (4 x 180ms) and its rise (0.7s), and a little.
const ARRIVAL_MS = 1600;

export function Greetings({ className = "" }: { className?: string }) {
  const copy = useCopy();
  const locale = useLocale();
  const motion = useMotionOk();
  const own = Math.max(
    0,
    drafts.greetings.findIndex((greeting) => greeting.lang === (LOCALE_TO_LANG[locale] ?? "en")),
  );
  // The rest first, the visitor's own language last.
  const order = [...drafts.greetings.keys()].filter((i) => i !== own).concat(own);
  const root = useRef<HTMLSpanElement>(null);
  useArrival(root, motion, 0.8, ARRIVAL_MS);

  return (
    <span ref={root} className={`${styles.greetings} ${className}`}>
      <span className={styles.sr}>{copy(drafts.languages)}</span>
      <span className={styles.line} aria-hidden="true">
        {order.map((index, step) => {
          const greeting = drafts.greetings[index];
          // A space between the words: where the line may break (between bare inline blocks the
          // balanced wrap left "Hello." alone on a line in Vietnamese).
          return (
            <Fragment key={greeting.lang}>
              {step > 0 ? " " : null}
              <span
                lang={greeting.lang}
                className={styles.word}
                data-own={index === own ? "" : undefined}
                style={{ "--step": step } as CSSProperties}
              >
                {greeting.text}
              </span>
            </Fragment>
          );
        })}
      </span>
    </span>
  );
}
