"use client";

import Image from "next/image";
import {
  type CSSProperties,
  type KeyboardEvent,
  useId,
  useRef,
  useState,
  useSyncExternalStore,
} from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { ProductPage } from "../product-types";
import styles from "./product-ink.module.css";

// The questions (Mo's pick A, October 26, 2026): each answer has its own painting. From 960px the
// questions are a list on the left and the picked one's painting and answer stand on the right, one
// at a time; the first is picked as the page opens, and picking another cross-fades to it. Below
// 960px each question opens in place, its painting above its answer, and closes again. Every answer
// is in the page (an accordion: aria-expanded, aria-controls); Up and Down move between questions,
// Home and End go to the first and last.
const WIDE = "(min-width: 960px)";

function onWideChange(change: () => void) {
  const query = window.matchMedia(WIDE);
  query.addEventListener("change", change);
  return () => query.removeEventListener("change", change);
}

export function Questions({ faq }: { faq: ProductPage["faq"] }) {
  const copy = useCopy();
  const baseId = useId();
  // The server renders the wide layout's state: the first question open, as a phone opens it too.
  const wide = useSyncExternalStore(
    onWideChange,
    () => window.matchMedia(WIDE).matches,
    () => true,
  );
  const [pick, setPick] = useState<number | null>(0);
  // Wide, one answer always stands on the right; a phone's last open question can be closed.
  const shown = wide ? (pick ?? 0) : pick;
  const buttons = useRef<(HTMLButtonElement | null)[]>([]);

  function move(event: KeyboardEvent<HTMLButtonElement>, index: number) {
    const last = faq.length - 1;
    const target =
      event.key === "ArrowDown"
        ? index === last
          ? 0
          : index + 1
        : event.key === "ArrowUp"
          ? index === 0
            ? last
            : index - 1
          : event.key === "Home"
            ? 0
            : event.key === "End"
              ? last
              : null;
    if (target === null) return;
    event.preventDefault();
    buttons.current[target]?.focus();
  }

  return (
    <ol
      className={styles.qaList}
      style={{ "--n": faq.length, "--rows": faq.length + 1 } as CSSProperties}
    >
      {faq.map((item, index) => {
        const questionId = `${baseId}q${index}`;
        const answerId = `${baseId}a${index}`;
        const open = shown === index;
        return (
          <li key={item.question} data-open={open ? "" : undefined}>
            <h3 className={styles.qaQuestion}>
              <button
                ref={(node) => {
                  buttons.current[index] = node;
                }}
                id={questionId}
                type="button"
                className={styles.qaButton}
                aria-expanded={open}
                aria-controls={answerId}
                onClick={() => setPick(!wide && open ? null : index)}
                onKeyDown={(event) => move(event, index)}
              >
                <span className={styles.qaWords}>{copy(item.question)}</span>
                <span className={styles.toggle} aria-hidden="true">
                  +
                </span>
              </button>
            </h3>
            <div
              id={answerId}
              role="region"
              aria-labelledby={questionId}
              className={styles.qaPanel}
            >
              {item.art ? (
                <Image
                  className={`${base.ink} ${styles.qaArt}`}
                  src={item.art.src}
                  alt=""
                  width={item.art.width}
                  height={item.art.height}
                  sizes="(min-width: 960px) 640px, 100vw"
                />
              ) : null}
              <p className={styles.qaAnswer}>{copy(item.answer)}</p>
            </div>
          </li>
        );
      })}
    </ol>
  );
}
