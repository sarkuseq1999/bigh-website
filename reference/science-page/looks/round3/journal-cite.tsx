"use client";

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { researchItems, type ResearchItem } from "@/components/home/research-data";
import { useCopy } from "@/i18n/use-copy";
import { research } from "./science-content";
import styles from "./look-journal.module.css";

// Look C's inline citations. The three key studies are the page's numbered references, in the
// order the text first cites them: [1] Dr. Liu's 2002 PNAS animal study, [2] his 2008 review of
// lipoic acid and the aging brain, [3] the 2023 Hallmarks of Aging review. A superscript number
// links to its reference further down; pointing at it (or focusing it) shows a small preview.
export const journalRefs: ResearchItem[] = research.key
  .map((url) => researchItems.find((item) => item.url === url))
  .filter((item) => item !== undefined);

type Tip = { n: number; x: number; top: number; bottom: number; vw: number } | null;
const TipContext = createContext<(tip: Tip) => void>(() => {});

// Marks the reference a citation points to for a moment, so the eye lands on it.
function flash(n: number) {
  const target = document.getElementById(`ref-${n}`);
  if (!target) return;
  target.dataset.flash = "true";
  window.setTimeout(() => delete target.dataset.flash, 1800);
}

export function Cite({ n }: { n: number[] | number }) {
  const copy = useCopy();
  const show = useContext(TipContext);
  const numbers = Array.isArray(n) ? n : [n];

  return (
    <sup className={styles.cite}>
      {numbers.map((number, index) => {
        const item = journalRefs[number - 1];
        const open = (element: HTMLElement) => {
          const rect = element.getBoundingClientRect();
          show({
            n: number,
            x: rect.left + rect.width / 2,
            top: rect.top,
            bottom: rect.bottom,
            vw: document.documentElement.clientWidth,
          });
        };
        return (
          <span key={number}>
            {index > 0 && ","}
            <a
              href={`#ref-${number}`}
              aria-label={`${copy("Reference")} ${number}: ${item ? copy(item.title) : ""}`}
              onPointerEnter={(event) => event.pointerType === "mouse" && open(event.currentTarget)}
              onPointerLeave={() => show(null)}
              onFocus={(event) => open(event.currentTarget)}
              onBlur={() => show(null)}
              onClick={() => {
                show(null);
                flash(number);
              }}
            >
              {number}
            </a>
          </span>
        );
      })}
    </sup>
  );
}

// One preview for the whole page, fixed to the screen and kept inside it. It hides on scroll.
export function CiteProvider({ children }: { children: ReactNode }) {
  const copy = useCopy();
  const [tip, setTip] = useState<Tip>(null);

  useEffect(() => {
    if (!tip) return;
    const hide = () => setTip(null);
    window.addEventListener("scroll", hide, { passive: true });
    window.addEventListener("resize", hide);
    return () => {
      window.removeEventListener("scroll", hide);
      window.removeEventListener("resize", hide);
    };
  }, [tip]);

  const item = tip ? journalRefs[tip.n - 1] : undefined;
  const width = tip?.vw ?? 1440;
  const boxWidth = Math.min(360, width - 32);
  const above = tip ? tip.top > 240 : true;

  return (
    <TipContext.Provider value={setTip}>
      {children}
      {tip && item && (
        <div
          role="tooltip"
          className={styles.tip}
          style={{
            width: boxWidth,
            left: Math.max(16, Math.min(tip.x - boxWidth / 2, width - boxWidth - 16)),
            top: above ? tip.top - 12 : tip.bottom + 12,
            transform: above ? "translateY(-100%)" : undefined,
          }}
        >
          <p className={styles.tipMeta}>
            <span className={styles.tipNo}>{tip.n}</span>
            <em>{item.journal}</em>, {copy(item.year)}
          </p>
          <p className={styles.tipTitle}>{copy(item.title)}</p>
          <p className={styles.tipKind}>{copy(item.category)}</p>
        </div>
      )}
    </TipContext.Provider>
  );
}
