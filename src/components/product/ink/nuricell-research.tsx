"use client";

import { useRef, useState, type CSSProperties } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct } from "../product-types";
import { InkChapter, InkFigure, titleId } from "./ink-chapter";
import { nuricellSizes } from "./nuricell-layout";
import styles from "./product-ink.module.css";
import s from "./nuricell-research.module.css";

// Mockup (October 26, 2026): NuriCell's research as plain questions, each tied to its book in the
// painting. Seven books, seven studies, nearest (oldest) first; the two 2003 reviews share one
// question and light their two books together. Answers follow each paper's abstract (PubMed).

const P = "https://pubmed.ncbi.nlm.nih.gov/";

/** Each book's outline in % of the painting (find_books.py), nearest first. */
const BOOKS = [
  "46.3% 81.5%, 32.6% 85.7%, 21.0% 87.8%, 4.4% 74.0%, 3.2% 71.9%, 6.3% 67.1%, 19.9% 63.4%, 25.0% 63.0%, 45.7% 73.3%",
  "59.6% 61.5%, 58.6% 63.0%, 44.7% 67.7%, 41.7% 67.7%, 35.9% 66.7%, 29.3% 64.2%, 26.0% 61.4%, 25.7% 58.2%, 26.3% 55.7%, 27.3% 54.7%, 41.1% 50.8%, 58.8% 55.4%",
  "69.2% 40.3%, 69.1% 45.0%, 61.0% 48.4%, 53.3% 48.4%, 49.7% 46.9%, 47.2% 45.2%, 46.3% 43.7%, 46.5% 41.1%, 47.1% 39.8%, 56.4% 37.3%, 58.5% 37.2%, 62.5% 38.1%, 68.7% 39.6%",
  "78.6% 28.5%, 78.4% 32.6%, 75.1% 33.7%, 66.3% 35.1%, 60.7% 34.8%, 59.0% 31.1%, 59.5% 28.9%, 59.9% 28.4%, 69.3% 26.1%",
  "69.9% 20.0%, 70.1% 18.3%, 70.7% 17.5%, 78.0% 16.3%, 83.9% 18.0%, 84.1% 21.0%, 83.1% 22.0%, 79.5% 23.0%, 71.6% 23.1%",
  "90.4% 12.9%, 89.7% 13.5%, 82.5% 13.6%, 79.2% 12.5%, 78.8% 11.0%, 79.5% 9.8%, 84.4% 9.0%, 89.8% 10.2%, 90.4% 10.9%",
  "88.3% 5.9%, 88.6% 4.9%, 90.5% 4.0%, 91.7% 3.9%, 96.0% 4.6%, 96.5% 5.3%, 96.5% 6.5%, 95.2% 6.9%, 88.7% 6.6%",
];

/** A book's tap area: its outline grown from its centre, so the far, small books stay tappable. */
function tapArea(outline: string, grow: number) {
  const points = outline.split(", ").map((pair) => pair.split(" ").map(parseFloat));
  const cx = points.reduce((sum, [x]) => sum + x, 0) / points.length;
  const cy = points.reduce((sum, [, y]) => sum + y, 0) / points.length;
  return `polygon(${points
    .map(([x, y]) => `${(cx + (x - cx) * grow).toFixed(1)}% ${(cy + (y - cy) * grow).toFixed(1)}%`)
    .join(", ")})`;
}

type Finding = { label?: string; verdict: string; line: string; url: string };
type Row = {
  books: number[];
  year: string;
  question: string;
  meta: string;
  verdict: string;
  findings: Finding[];
  after?: string;
};

const ROWS: Row[] = [
  {
    books: [0],
    year: "2002",
    question: "Can two nutrients help an aging brain?",
    meta: "Animal study · PNAS",
    verdict: "In old rats, yes.",
    findings: [
      {
        verdict: "",
        line: "Old rats fed acetyl-L-carnitine and lipoic acid did better on memory tests, and the pair worked best. Rats, not people, and not NuriCell itself.",
        url: `${P}11854529/`,
      },
    ],
  },
  {
    books: [1],
    year: "2002",
    question: "Do they help old cells make energy?",
    meta: "Animal study · PNAS",
    verdict: "In old rats, yes.",
    findings: [
      {
        verdict: "",
        line: "Their cells made energy better and showed less wear, and the rats moved about more. The two together did more than either one alone. Rats, not people.",
        url: `${P}11854487/`,
      },
    ],
  },
  {
    books: [2, 3],
    year: "2003",
    question: "Does acetyl-L-carnitine help people with memory problems?",
    meta: "Two reviews of trials",
    verdict: "Scientists disagree.",
    findings: [
      {
        label: "Pooled trials",
        verdict: "A small benefit.",
        line: "Over a placebo, in people with mild memory problems or mild Alzheimer’s.",
        url: `${P}12598816/`,
      },
      {
        label: "Cochrane review",
        verdict: "No clear benefit.",
        line: "On memory tests, in people with Alzheimer’s. Not enough to recommend it.",
        url: `${P}12804452/`,
      },
    ],
    after: "Both looked at patients, not healthy adults.",
  },
  {
    books: [4],
    year: "2008",
    question: "What does lipoic acid do in an aging brain?",
    meta: "Review · Neurochem Res",
    verdict: "In animals, it helped memory.",
    findings: [
      {
        verdict: "",
        line: "Dr. Liu’s own overview: in aging animals, lipoic acid helped memory and the cells’ power plants. Mostly animal work.",
        url: `${P}17605107/`,
      },
    ],
  },
  {
    books: [5],
    year: "2009",
    question: "What do we know about lipoic acid as a supplement?",
    meta: "Review · BBA",
    verdict: "How it works is clearer than what it does for people.",
    findings: [
      {
        verdict: "",
        line: "A review of lab, animal and human studies. Trials in people were still under way.",
        url: `${P}19664690/`,
      },
    ],
  },
  {
    books: [6],
    year: "2018",
    question: "Does creatine help healthy people think?",
    meta: "Review of trials · Exp Gerontol",
    verdict: "Maybe, for short-term memory and reasoning.",
    findings: [
      {
        verdict: "",
        line: "Six small trials, 281 people. Other results were mixed, and young people saw no change.",
        url: `${P}29704637/`,
      },
    ],
  },
];

const rowOfBook = (book: number) => ROWS.findIndex((row) => row.books.includes(book));

function ReadLink({ url }: { url: string }) {
  const copy = useCopy();
  return (
    <a href={url} target="_blank" rel="noopener noreferrer" className={base.textLink}>
      {copy("Read the study")}
      <span className={base.visuallyHidden}> {copy("(opens in a new tab)")}</span>
    </a>
  );
}

export function NuricellResearch({ product }: { product: InkProduct }) {
  const copy = useCopy();
  const [open, setOpen] = useState<number | null>(0);
  const [peek, setPeek] = useState<number | null>(null);
  const rows = useRef<(HTMLLIElement | null)[]>([]);
  const shown = peek ?? open;
  const lit = shown === null ? null : ROWS[shown].books;

  // A book always opens its question. Once the rows have settled (the one closing and the one
  // opening, 0.6s), bring the open one into view if it is not: on a phone it sits under the
  // painting. As little as it takes, never under the menu bar.
  function openFromBook(row: number) {
    setOpen(row);
    window.setTimeout(() => {
      const li = rows.current[row];
      if (!li) return;
      const bar = document.querySelector("header")?.getBoundingClientRect().bottom ?? 0;
      const { top, bottom } = li.getBoundingClientRect();
      const toTop = top - bar - 16;
      let by = 0;
      if (top < bar + 8) by = toTop;
      // One column (under 960px): the question to the top, to be read from its start. Beside the
      // painting: only as far as the answer's end, so the painting stays in view.
      else if (bottom > window.innerHeight - 8)
        by = window.innerWidth < 960 ? toTop : Math.min(bottom - window.innerHeight + 24, toTop);
      if (by === 0) return;
      const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
      window.scrollBy({ top: by, behavior: still ? "auto" : "smooth" });
    }, 650);
  }

  const peekAt = (row: number | null) => (event: { pointerType: string }) => {
    if (event.pointerType === "mouse") setPeek(row);
  };

  return (
    <InkChapter
      id="research"
      className={s.research}
      picture={
        <InkFigure
          art={product.ink.research}
          alt={product.ink.research.alt}
          sizes={nuricellSizes(product, "research", product.ink.research)}
        >
          {BOOKS.map((_, i) => (
            <span
              key={`fade-${i}`}
              className={s.fade}
              data-dim={lit && !lit.includes(i) ? "" : undefined}
              style={
                {
                  ["--mask" as string]: `url(/images/products/nuricell/ink/books-mask-v1-${i + 1}.png)`,
                } as CSSProperties
              }
              aria-hidden="true"
            />
          ))}
          {BOOKS.map((outline, i) => {
            const row = rowOfBook(i);
            return (
              <button
                key={`book-${i}`}
                type="button"
                className={s.book}
                style={{ clipPath: tapArea(outline, i < 2 ? 1.05 : 1.6) }}
                aria-label={`${ROWS[row].year}: ${ROWS[row].question}`}
                aria-controls={`research-answer-${row}`}
                aria-expanded={open === row}
                onClick={() => openFromBook(row)}
                onPointerEnter={peekAt(row)}
                onPointerLeave={peekAt(null)}
                onFocus={() => setPeek(row)}
                onBlur={() => setPeek(null)}
                data-book={i + 1}
              />
            );
          })}
        </InkFigure>
      }
    >
      <h2 id={titleId("research")} className={`${base.display} ${styles.heading}`}>
        {copy(product.researchTitle ?? "The research on the ingredients")}
      </h2>
      <p className={styles.small}>
        These studies are about NuriCell’s ingredients, not the finished product.
      </p>
      <p className={s.hint}>Each book is one study. Tap one to read it.</p>
      <ul className={s.rows} data-studies="">
        {ROWS.map((row, i) => {
          const isOpen = open === i;
          return (
            <li
              key={row.question}
              ref={(node) => {
                rows.current[i] = node;
              }}
              data-study=""
              data-open={isOpen ? "" : undefined}
            >
              <button
                type="button"
                className={s.q}
                aria-expanded={isOpen}
                aria-controls={`research-answer-${i}`}
                onClick={() => setOpen(isOpen ? null : i)}
                onPointerEnter={peekAt(i)}
                onPointerLeave={peekAt(null)}
              >
                <span className={s.year}>{row.year}</span>
                <span>
                  <span className={s.question}>{row.question}</span>
                  <span className={s.meta}>{row.meta}</span>
                </span>
                <span className={s.mark} aria-hidden="true">
                  +
                </span>
              </button>
              <div
                id={`research-answer-${i}`}
                className={s.answer}
                data-open={isOpen ? "" : undefined}
                inert={!isOpen}
              >
                <div className={s.answerClip}>
                  <div className={s.answerBody}>
                    <p className={s.verdict}>{row.verdict}</p>
                    {row.findings.length === 1 ? (
                      <>
                        <p className={s.line}>{row.findings[0].line}</p>
                        <ReadLink url={row.findings[0].url} />
                      </>
                    ) : (
                      <>
                        <div className={s.sides}>
                          {row.findings.map((finding) => (
                            <div key={finding.url} className={s.side}>
                              <span className={s.meta}>{finding.label}</span>
                              <p className={s.sideVerdict}>{finding.verdict}</p>
                              <p className={s.line}>{finding.line}</p>
                              <ReadLink url={finding.url} />
                            </div>
                          ))}
                        </div>
                        {row.after ? <p className={s.line}>{row.after}</p> : null}
                      </>
                    )}
                  </div>
                </div>
              </div>
            </li>
          );
        })}
      </ul>
    </InkChapter>
  );
}
