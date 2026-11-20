"use client";

import { useRef, useState } from "react";
import base from "@/components/ink/ink.module.css";
import { useCopy } from "@/i18n/use-copy";
import type { InkProduct } from "../product-types";
import { InkChapter, InkFigure, titleId } from "./ink-chapter";
import { nuricellSizes } from "./nuricell-layout";
import styles from "./product-ink.module.css";
import s from "./nuricell-research.module.css";

// NuriCell's research as plain questions, each tied to its book in the painting (Mo picked A, "tap a
// book, read its study", October 26, 2026; mockups: reference/ink-pages/mockups/nuricell-research/).
// Seven books, seven studies, oldest first; the two 2003 reviews share one question and
// light their two books together. Answers follow each paper's abstract (PubMed).

const P = "https://pubmed.ncbi.nlm.nih.gov/";

/** Spines from left to right. The tap target and its watercolor fade follow the same outline. */
const BOOKS = [
  "polygon(7.56% 44.65%, 11.84% 42.16%, 22.61% 41.62%, 20.26% 45.01%, 20.19% 85.65%, 19.04% 86.72%, 8.35% 86.81%)",
  "polygon(19.97% 45.28%, 23.04% 42.96%, 32.74% 43.05%, 32.03% 45.81%, 32.31% 85.83%, 30.74% 86.72%, 20.68% 86.63%)",
  "polygon(32.10% 45.37%, 33.88% 42.25%, 43.58% 42.51%, 44.22% 44.56%, 44.29% 85.20%, 43.22% 86.54%, 33.10% 86.54%)",
  "polygon(44.01% 42.16%, 44.65% 39.13%, 55.21% 39.39%, 56.35% 41.98%, 56.35% 85.03%, 55.42% 86.36%, 45.01% 86.45%)",
  "polygon(56.28% 41.80%, 56.06% 39.75%, 65.55% 39.57%, 67.62% 41.98%, 67.62% 84.76%, 66.83% 86.01%, 56.99% 85.92%)",
  "polygon(67.55% 43.32%, 66.90% 41.09%, 75.68% 40.55%, 78.60% 42.96%, 79.17% 84.49%, 78.25% 86.01%, 68.19% 85.56%)",
  "polygon(78.67% 44.47%, 84.02% 40.73%, 88.80% 41.98%, 95.29% 83.33%, 93.08% 85.12%, 85.95% 86.10%, 79.53% 81.73%)",
];

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
          {BOOKS.map((clipPath, i) => (
            <span
              key={`fade-${i}`}
              className={s.fade}
              data-fade={i + 1}
              data-dim={lit && !lit.includes(i) ? "" : undefined}
              style={{ clipPath }}
              aria-hidden="true"
            />
          ))}
          {BOOKS.map((clipPath, i) => {
            const row = rowOfBook(i);
            return (
              <button
                key={`book-${i}`}
                type="button"
                className={s.book}
                style={{ clipPath }}
                aria-label={`${ROWS[row].year}: ${copy(ROWS[row].question)}`}
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
      <p className={styles.small}>{copy(product.notes.research)}</p>
      <p className={s.hint}>{copy("Each book is one study. Tap one to read it.")}</p>
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
                  <span className={s.question}>{copy(row.question)}</span>
                  <span className={s.meta}>{copy(row.meta)}</span>
                </span>
                <span className={s.mark} aria-hidden="true">
                  +
                </span>
              </button>
              <div
                id={`research-answer-${i}`}
                className={s.answer}
                data-open={isOpen ? "" : undefined}
              >
                <div className={s.answerClip}>
                  <div className={s.answerBody}>
                    <p className={s.verdict}>{copy(row.verdict)}</p>
                    {row.findings.length === 1 ? (
                      <>
                        <p className={s.line}>{copy(row.findings[0].line)}</p>
                        <ReadLink url={row.findings[0].url} />
                      </>
                    ) : (
                      <>
                        <div className={s.sides}>
                          {row.findings.map((finding) => (
                            <div key={finding.url} className={s.side}>
                              <span className={s.meta}>{copy(finding.label ?? "")}</span>
                              <p className={s.sideVerdict}>{copy(finding.verdict)}</p>
                              <p className={s.line}>{copy(finding.line)}</p>
                              <ReadLink url={finding.url} />
                            </div>
                          ))}
                        </div>
                        {row.after ? <p className={s.line}>{copy(row.after)}</p> : null}
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
